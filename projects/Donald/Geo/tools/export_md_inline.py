#!/usr/bin/env python3
"""Export a Markdown file to a single self-contained HTML file with images inlined.

Usage:
  python3 tools/export_md_inline.py NOTE_FOR_DONALD.md [OUTPUT.html]

This will embed local image files referenced via Markdown image syntax
(![alt](path)) as base64 data URIs so the HTML can be shared without losing visuals.
"""

from __future__ import annotations

import base64
import mimetypes
import re
import sys
from pathlib import Path


IMG_PATTERN = re.compile(r"!\[(?P<alt>[^\]]*)\]\((?P<src>[^)]+)\)")


def to_data_uri(path: Path) -> str:
    mime, _ = mimetypes.guess_type(path.name)
    if not mime:
        mime = "application/octet-stream"
    data = path.read_bytes()
    b64 = base64.b64encode(data).decode("ascii")
    return f"data:{mime};base64,{b64}"


def inline_images(md_text: str, base_dir: Path) -> str:
    def repl(match: re.Match) -> str:
        alt = match.group("alt")
        src = match.group("src").strip()
        # ignore URLs (http/https)
        if src.startswith("http://") or src.startswith("https://"):
            return match.group(0)
        img_path = (base_dir / src).resolve()
        if not img_path.exists():
            return match.group(0)
        data_uri = to_data_uri(img_path)
        return f"<img alt=\"{alt}\" src=\"{data_uri}\" />"

    return IMG_PATTERN.sub(repl, md_text)


def convert_markdown(md_text: str) -> str:
    # Try to use python-markdown, else fallback to a minimal converter
    try:
        import markdown  # type: ignore

        return markdown.markdown(md_text, extensions=["extra", "tables", "sane_lists"])  # type: ignore
    except Exception:
        # very small fallback: handle headings and paragraphs
        html_lines = []
        for line in md_text.splitlines():
            if line.startswith("### "):
                html_lines.append(f"<h3>{line[4:]}</h3>")
            elif line.startswith("## "):
                html_lines.append(f"<h2>{line[3:]}</h2>")
            elif line.startswith("# "):
                html_lines.append(f"<h1>{line[2:]}</h1>")
            elif line.startswith("- "):
                # simple list handling (no nesting)
                if not (html_lines and html_lines[-1].startswith("<ul>")):
                    html_lines.append("<ul>")
                html_lines.append(f"<li>{line[2:]}</li>")
            elif line.strip() == "":
                if html_lines and html_lines[-1] == "<ul>":
                    html_lines.pop()
                    html_lines.append("</ul>")
                else:
                    html_lines.append("")
            else:
                html_lines.append(f"<p>{line}</p>")
        html = "\n".join(html_lines)
        # close list if left open
        if html.endswith("<ul>"):
            html += "</ul>"
        return html


def wrap_html(body_html: str, title: str) -> str:
    return f"""
<!doctype html>
<html lang=\"en\"> 
<head>
  <meta charset=\"utf-8\" />
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
  <title>{title}</title>
  <style>
    body {{
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Helvetica Neue', Arial, sans-serif;
      max-width: 900px; margin: 2rem auto; padding: 0 1rem; line-height: 1.6;
    }}
    img {{ max-width: 100%; height: auto; display: block; margin: 0.5rem 0 1rem; }}
    code, pre {{ background: #f6f8fa; padding: 2px 4px; border-radius: 4px; }}
    blockquote {{ border-left: 4px solid #ddd; margin: 0.5rem 0; padding: 0.5rem 1rem; color: #555; }}
    h1, h2, h3 {{ line-height: 1.25; }}
  </style>
  <meta name=\"generator\" content=\"export_md_inline.py\" />
  <meta name=\"x-single-file\" content=\"true\" />
  <base href=\".\" />
  <meta name=\"color-scheme\" content=\"light dark\" />
  <style media=\"print\"> body {{ color: black; }} </style>
  <script>/* noop */</script>
</head>
<body>
{body_html}
</body>
</html>
"""


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("Usage: export_md_inline.py INPUT.md [OUTPUT.html]")
        return 2
    in_path = Path(argv[1]).resolve()
    if not in_path.exists():
        print(f"Input not found: {in_path}")
        return 2
    out_path = Path(argv[2]).resolve() if len(argv) > 2 else in_path.with_suffix(".html")

    md_raw = in_path.read_text(encoding="utf-8")
    md_with_inline_imgs = inline_images(md_raw, in_path.parent)
    body_html = convert_markdown(md_with_inline_imgs)
    html = wrap_html(body_html, title=in_path.stem)
    out_path.write_text(html, encoding="utf-8")
    print(f"Wrote {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
