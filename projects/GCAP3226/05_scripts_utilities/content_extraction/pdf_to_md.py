import sys
from pathlib import Path

try:
    import fitz  # PyMuPDF
except Exception as e:
    print("ERROR: PyMuPDF not installed. Install with: pip install PyMuPDF", file=sys.stderr)
    sys.exit(2)


def pdf_to_markdown(pdf_path: Path, md_path: Path):
    doc = fitz.open(pdf_path)
    parts = []
    for page in doc:
        # Prefer markdown extraction if available; fall back to plain text
        try:
            parts.append(page.get_text("markdown"))
        except Exception:
            parts.append(page.get_text())
        parts.append("\n\n---\n\n")
    doc.close()
    md_path.write_text("".join(parts), encoding="utf-8")


def main():
    if len(sys.argv) < 3:
        print("Usage: pdf_to_md.py <input.pdf> <output.md>")
        sys.exit(1)
    pdf = Path(sys.argv[1])
    out = Path(sys.argv[2])
    out.parent.mkdir(parents=True, exist_ok=True)
    pdf_to_markdown(pdf, out)
    print(f"Converted {pdf} -> {out}")


if __name__ == "__main__":
    main()
