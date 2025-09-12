#!/usr/bin/env python3
"""Export an HTML file to PDF using a headless browser or wkhtmltopdf if available.

Usage:
  python3 tools/export_html_to_pdf.py INPUT.html [OUTPUT.pdf]

Tries in order: Google Chrome, Chromium, Microsoft Edge, Brave, wkhtmltopdf.
"""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path


def try_run(cmd: list[str]) -> bool:
    try:
        proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
        return proc.returncode == 0
    except FileNotFoundError:
        return False


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("Usage: export_html_to_pdf.py INPUT.html [OUTPUT.pdf]")
        return 2
    in_path = Path(argv[1]).resolve()
    if not in_path.exists():
        print(f"Input not found: {in_path}")
        return 2
    out_path = Path(argv[2]).resolve() if len(argv) > 2 else in_path.with_suffix(".pdf")

    # Candidate browser executables (macOS app bundles + CLI names)
    candidates = [
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary",
        "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
        "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
        shutil.which("google-chrome"),
        shutil.which("chromium"),
        shutil.which("chromium-browser"),
        shutil.which("chrome"),
        shutil.which("msedge"),
        shutil.which("brave-browser"),
    ]
    candidates = [c for c in candidates if c]

    for exe in candidates:
        cmd = [
            exe,
            "--headless=new",
            "--disable-gpu",
            "--no-sandbox",
            f"--print-to-pdf={str(out_path)}",
            "--print-to-pdf-no-header",
            str(in_path),
        ]
        if try_run(cmd):
            print(f"Wrote {out_path} via {exe}")
            return 0

    # Fallback: wkhtmltopdf if installed
    wk = shutil.which("wkhtmltopdf")
    if wk:
        if try_run([wk, str(in_path), str(out_path)]):
            print(f"Wrote {out_path} via wkhtmltopdf")
            return 0

    print("Could not find a suitable HTML-to-PDF tool. Install Google Chrome or wkhtmltopdf.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
