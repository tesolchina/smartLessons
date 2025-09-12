from __future__ import annotations

from typing import Tuple


def get_last_end_index(doc: dict) -> int:
    body = doc.get('body', {})
    content = body.get('content', [])
    if not content:
        return 1
    last = content[-1]
    return int(last.get('endIndex', 1))


def append_markdown_formatted(docs, document_id: str, md: str, build_replace_requests):
    document = docs.documents().get(documentId=document_id).execute()
    end_index = max(1, get_last_end_index(document) - 1)
    reqs = build_replace_requests("\n" + md.strip() + "\n", initial_index=end_index)
    CHUNK = 100
    for i in range(0, len(reqs), CHUNK):
        docs.documents().batchUpdate(documentId=document_id, body={'requests': reqs[i:i+CHUNK]}).execute()
