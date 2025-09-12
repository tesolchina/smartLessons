#!/usr/bin/env python3
"""
Ingest an exported email (.eml) and create a Google Drive subfolder + discussion doc.

Workflow:
1. Parse the .eml file (subject, from, to, date, body, attachments)
2. Create a subfolder under the provided parent folder ID (default: SCMP Letters parent)
3. Upload original .eml and any attachments
4. Create a Google Doc with a structured discussion template
5. Set sharing so anyone with the link can comment (role=commenter)

Usage:
  python3 operating/GoogleDocsAPI/email_to_drive_discussion.py \
    --eml /path/to/exported_email.eml \
    --parent-id 1Papf6OOc1_PC2Z480hraBfqbcKJZvi74

Optional:
  --subfolder-name "Custom Folder"  (otherwise auto from subject/date)
  --permission commenter|writer|reader (default commenter)
  --dry-run (no Drive/Doc creation, parse only)

Exporting an email from Apple Mail:
  Select the email → File → Save As… → Format: Raw Message Source (.eml)
"""
from __future__ import annotations

import argparse
import base64
import os
import re
import sys
from pathlib import Path
from datetime import datetime
from typing import List, Optional, Dict

from email import policy
from email.parser import BytesParser
from email.message import EmailMessage

sys.path.append(str(Path(__file__).parent))
try:
    from auth_setup import authenticate_google_apis
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaFileUpload
    GOOGLE_OK = True
except Exception as e:
    print(f"[WARN] Google API libs not available: {e}")
    GOOGLE_OK = False

DEFAULT_PARENT_ID = "1Papf6OOc1_PC2Z480hraBfqbcKJZvi74"


def sanitize_filename(name: str) -> str:
    name = re.sub(r"[\\/:*?\"<>|]", "_", name)
    name = re.sub(r"\s+", " ", name).strip()
    if len(name) > 120:
        name = name[:117] + '...'
    return name or 'email'


def parse_eml(path: Path) -> Dict:
    with open(path, 'rb') as f:
        msg: EmailMessage = BytesParser(policy=policy.default).parse(f)
    subject = msg.get('Subject', '(no subject)')
    mail_from = msg.get('From', '')
    to = msg.get('To', '')
    date_raw = msg.get('Date')
    try:
        date_obj = datetime.strptime(date_raw[:25], '%a, %d %b %Y %H:%M:%S') if date_raw else None
    except Exception:
        date_obj = None

    # Extract body preference text/plain then fallback to text/html
    body_text = ''
    html_part = ''
    if msg.is_multipart():
        for part in msg.walk():
            ctype = part.get_content_type()
            disp = part.get_content_disposition()
            if disp == 'attachment':
                continue
            if ctype == 'text/plain' and not body_text:
                try:
                    body_text = part.get_content()
                except Exception:
                    pass
            elif ctype == 'text/html' and not html_part:
                try:
                    html_part = part.get_content()
                except Exception:
                    pass
    else:
        body_text = msg.get_content()

    if not body_text and html_part:
        # Try to use BeautifulSoup if available; otherwise fallback to naive tag strip.
        try:
            # Local import inside try so missing dependency doesn't raise linter/runtime error.
            import importlib
            bs4_spec = importlib.util.find_spec('bs4')  # type: ignore
            if bs4_spec is not None:
                from bs4 import BeautifulSoup  # type: ignore
                body_text = BeautifulSoup(html_part, 'html.parser').get_text("\n")
            else:
                raise ImportError('bs4 not installed')
        except Exception:
            body_text = re.sub('<[^>]+>', '', html_part)

    attachments: List[Dict] = []
    for part in msg.walk():
        if part.get_content_disposition() == 'attachment':
            fname = part.get_filename() or 'attachment'
            data = part.get_payload(decode=True) or b''
            attachments.append({'filename': fname, 'data': data, 'mime': part.get_content_type()})

    return {
        'subject': subject,
        'from': mail_from,
        'to': to,
        'date': date_raw,
        'date_obj': date_obj,
        'body': body_text.strip(),
        'attachments': attachments,
    }


def ensure_services():
    if not GOOGLE_OK:
        return None, None
    creds = authenticate_google_apis()
    if not creds:
        print("❌ Authentication failed.")
        return None, None
    drive = build('drive', 'v3', credentials=creds)
    docs = build('docs', 'v1', credentials=creds)
    return drive, docs


def create_subfolder(drive, parent_id: str, name: str) -> Optional[str]:
    meta = {
        'name': name,
        'mimeType': 'application/vnd.google-apps.folder',
        'parents': [parent_id]
    }
    try:
        folder = drive.files().create(body=meta, fields='id').execute()
        return folder.get('id')
    except Exception as e:
        print(f"❌ Failed to create subfolder: {e}")
        return None


def upload_file(drive, folder_id: str, local_path: Path, mime: str = 'application/octet-stream') -> Optional[str]:
    try:
        meta = {'name': local_path.name, 'parents': [folder_id]}
        media = MediaFileUpload(str(local_path), mimetype=mime, resumable=True)
        f = drive.files().create(body=meta, media_body=media, fields='id').execute()
        return f.get('id')
    except Exception as e:
        print(f"❌ Upload failed for {local_path.name}: {e}")
        return None


def upload_attachment_blob(drive, folder_id: str, filename: str, data: bytes, mime: str) -> Optional[str]:
    tmp = Path('/tmp') / f"_email_att_{os.getpid()}_{sanitize_filename(filename)}"
    try:
        tmp.write_bytes(data)
        return upload_file(drive, folder_id, tmp, mime=mime)
    finally:
        try:
            if tmp.exists():
                tmp.unlink()
        except Exception:
            pass


def create_discussion_doc(docs, drive, folder_id: str, subject: str, parsed: Dict, permission_role: str = 'commenter') -> Dict:
    title = f"Discussion - {sanitize_filename(subject)}"
    doc = docs.documents().create(body={'title': title}).execute()
    doc_id = doc.get('documentId')
    # Move doc into folder
    try:
        drive.files().update(fileId=doc_id, addParents=folder_id, fields='id,parents').execute()
    except Exception as e:
        print(f"⚠️ Could not move doc into folder: {e}")

    snippet = (parsed['body'][:1200] + '...') if len(parsed['body']) > 1200 else parsed['body']
    meta_block = f"""Email Metadata\nSubject: {parsed['subject']}\nFrom: {parsed['from']}\nTo: {parsed['to']}\nDate: {parsed['date']}\n\n---\nOriginal Snippet:\n{snippet}\n---\n"""
    template = f"""Letters to the Editor Symposium / Exhibition Discussion
Generated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}

{meta_block}
## Objectives
- Clarify scope and deliverables for November 17 event.
- Identify required assets (letters selection, panel layout, exhibition materials).

## Key Questions
1. Curation criteria?
2. Required approvals?
3. Timeline checkpoints?

## Tasks / Next Actions
- [ ] Draft selection list
- [ ] Venue logistics confirmation
- [ ] Visual layout design

## Stakeholders
- Organizer
- Academic liaison
- Technical support

## Notes

Add comments inline—link sharing is set to allow commenting.
"""

    try:
        docs.documents().batchUpdate(
            documentId=doc_id,
            body={'requests': [{'insertText': {'location': {'index': 1}, 'text': template}}]}
        ).execute()
        # Set sharing
        perm = {'type': 'anyone', 'role': permission_role}
        drive.permissions().create(fileId=doc_id, body=perm).execute()
        info = drive.files().get(fileId=doc_id, fields='webViewLink').execute()
        return {'doc_id': doc_id, 'title': title, 'web_link': info.get('webViewLink')}
    except Exception as e:
        print(f"❌ Failed to populate discussion doc: {e}")
        return {'doc_id': doc_id}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description='Ingest .eml → Drive subfolder + discussion doc')
    ap.add_argument('--eml', required=True, help='Path to exported .eml email file')
    ap.add_argument('--parent-id', default=DEFAULT_PARENT_ID, help='Parent Drive folder ID')
    ap.add_argument('--subfolder-name', help='Optional explicit subfolder name')
    ap.add_argument('--permission', default='commenter', choices=['commenter','writer','reader'], help='Sharing role for the discussion doc')
    ap.add_argument('--dry-run', action='store_true')
    args = ap.parse_args(argv)

    eml_path = Path(args.eml)
    if not eml_path.exists():
        print(f"❌ .eml not found: {eml_path}")
        return 1

    parsed = parse_eml(eml_path)
    print(f"Parsed email: subject='{parsed['subject']}' from='{parsed['from']}' attachments={len(parsed['attachments'])}")

    subfolder_name = args.subfolder_name or sanitize_filename(
        (parsed['date_obj'].strftime('%Y-%m-%d') + ' - ' if parsed.get('date_obj') else '') + parsed['subject']
    )

    if args.dry_run:
        print(f"[DRY-RUN] Would create subfolder '{subfolder_name}' under parent {args.parent_id}")
        return 0

    drive, docs = ensure_services()
    if not drive or not docs:
        print("❌ Google services unavailable.")
        return 1

    folder_id = create_subfolder(drive, args.parent_id, subfolder_name)
    if not folder_id:
        return 1
    print(f"✅ Created subfolder: {subfolder_name} ({folder_id})")

    # Upload original .eml
    upload_file(drive, folder_id, eml_path, mime='message/rfc822')
    # Upload attachments
    for att in parsed['attachments']:
        att_id = upload_attachment_blob(drive, folder_id, att['filename'], att['data'], att['mime'])
        print(f"  • Attachment uploaded: {att['filename']} ({att_id})")

    # Create discussion doc
    doc_info = create_discussion_doc(docs, drive, folder_id, parsed['subject'], parsed, permission_role=args.permission)
    if doc_info.get('web_link'):
        print(f"✅ Discussion doc: {doc_info['web_link']}")
    else:
        print("⚠️ Discussion doc created but link not retrieved.")

    print("🎉 Email ingestion complete.")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
