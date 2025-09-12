#!/usr/bin/env python3
"""Create project sub-folders and copied Google Docs from a template.

Primary use-case (derived from notes):
  - Base Google Drive folder: 1vI96VXDrJvdnqegFfJ5y8zOnHxGPHxVV
  - Template Doc ID: 1polOm2WKjwlAGe_YGsffkIJ2a1mGXDMm0IFoKb7ZNoA
  - Projects (examples):
       Emergency Alert System | https://www.scmp.com/comment/letters/article/3208166/hong-kongs-emergency-alert-system-white-elephant
       Anti-scamming Education | https://www.adcc.gov.hk/en-hk/home.html ; https://www.adcc.gov.hk/en-hk/report.html

Features:
  - Creates (or reuses) a folder per project under the base folder.
  - Copies the template doc into that folder, renamed with the project title.
  - Inserts a metadata header with source links at top of the copied doc.
  - Idempotent: if a doc with exact title already exists in that folder, it will skip copy unless --force.

Usage:
  python3 create_project_docs.py --base-folder 1vI96VXDrJvdnqegFfJ5y8zOnHxGPHxVV \
      --template 1polOm2WKjwlAGe_YGsffkIJ2a1mGXDMm0IFoKb7ZNoA \
      --project "Emergency Alert System|https://www.scmp.com/comment/letters/article/3208166/hong-kongs-emergency-alert-system-white-elephant" \
      --dry-run

Multiple projects:
  --project "Anti-scamming Education|https://www.adcc.gov.hk/en-hk/home.html,https://www.adcc.gov.hk/en-hk/report.html" --project "Chronic disease co-care pilot scheme|https://www.primaryhealthcare.gov.hk/cdcc/en/"

Note: Requires existing auth setup (credentials.json / token) as per other scripts.
"""
from __future__ import annotations
import argparse, os, sys, datetime as dt
from typing import List, Tuple, Dict

sys.path.append(os.path.dirname(__file__))
from auth_setup import authenticate_google_apis  # type: ignore
from googleapiclient.discovery import build  # type: ignore
from googleapiclient.errors import HttpError  # type: ignore


def parse_args():
    ap = argparse.ArgumentParser(description="Create project folders + copied docs from template")
    ap.add_argument('--base-folder', required=True, help='Parent Google Drive folder ID')
    ap.add_argument('--template', required=True, help='Template Google Doc ID')
    ap.add_argument('--project', action='append', help='Project spec: Title|url1,url2,...')
    ap.add_argument('--force', action='store_true', help='Force new copy even if one exists')
    ap.add_argument('--dry-run', action='store_true')
    return ap.parse_args()


def parse_project_specs(specs: List[str] | None) -> List[Tuple[str,List[str]]]:
    if not specs:
        return []
    out: List[Tuple[str,List[str]]] = []
    for s in specs:
        if '|' in s:
            title, rest = s.split('|',1)
            links = [u.strip() for u in rest.replace(';',',').split(',') if u.strip()]
        else:
            title = s.strip(); links = []
        if title:
            out.append((title.strip(), links))
    return out


def drive_find_existing(drive, parent_id: str, name: str) -> str | None:
    safe_name = name.replace("'", "\'")
    q = f"name = '{safe_name}' and '{parent_id}' in parents and trashed = false"
    resp = drive.files().list(q=q, spaces='drive', fields='files(id,name)').execute()
    files = resp.get('files', [])
    return files[0]['id'] if files else None


def ensure_folder(drive, parent_id: str, name: str) -> str:
    existing = drive_find_existing(drive, parent_id, name)
    if existing:
        return existing
    meta = {
        'name': name,
        'mimeType': 'application/vnd.google-apps.folder',
        'parents': [parent_id]
    }
    new = drive.files().create(body=meta, fields='id').execute()
    return new['id']


def copy_doc(drive, template_id: str, parent_id: str, new_title: str) -> str:
    body = {'name': new_title, 'parents': [parent_id]}
    new = drive.files().copy(fileId=template_id, body=body, fields='id').execute()
    return new['id']


def insert_metadata(docs, doc_id: str, title: str, links: List[str]):
    if not links:
        return
    ts = dt.datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')
    link_lines = '\n'.join(f"- {u}" for u in links)
    text = f"[Project: {title}]\nSources (captured {ts}):\n{link_lines}\n\n"
    # Insert at start (index 1)
    requests = [
        {'insertText': {'location': {'index': 1}, 'text': text}}
    ]
    docs.documents().batchUpdate(documentId=doc_id, body={'requests': requests}).execute()


def main():
    args = parse_args()
    projects = parse_project_specs(args.project)
    if not projects:
        print('No --project entries supplied (nothing to do).')
        return 0
    creds = authenticate_google_apis()
    if not creds:
        print('Auth failed.')
        return 1
    drive = build('drive','v3',credentials=creds)
    docs = build('docs','v1',credentials=creds)
    summary: List[Dict[str,str]] = []
    for title, links in projects:
        print(f"Processing project: {title}")
        folder_id = ensure_folder(drive, args.base_folder, title)
        existing_doc_id = drive_find_existing(drive, folder_id, title)
        doc_id = existing_doc_id
        action = 'skip-existing'
        if args.force or not existing_doc_id:
            if args.dry_run:
                action = 'would-copy'
            else:
                doc_id = copy_doc(drive, args.template, folder_id, title)
                action = 'copied'
                insert_metadata(docs, doc_id, title, links)
        summary.append({'title': title, 'folder_id': folder_id, 'doc_id': doc_id or '', 'action': action})
    print('\nSummary:')
    for item in summary:
        print(f"- {item['title']}: folder={item['folder_id']} doc={item['doc_id']} action={item['action']}")
    return 0


if __name__ == '__main__':  # pragma: no cover
    raise SystemExit(main())
