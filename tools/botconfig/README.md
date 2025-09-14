# Bot Config Converter (Markdown → JSON)

This tiny tool lets teachers edit a friendly Markdown file and convert it back into the JSON bot config used by the platform.

## Files
- `md_to_json.py` — converter script

## Editable Markdown format
The Markdown must include YAML front-matter and three sections:
- `## Welcome prompt`
- `## Report generation instructions`
- `## System prompt`

Example file: `projects/Jackie/botConfig/GCAP3187-emily.EDITABLE.md`

## Usage

Run from the repo root:

```bash
python tools/botconfig/md_to_json.py \
  --in projects/Jackie/botConfig/GCAP3187-emily.EDITABLE.md \
  --out projects/Jackie/botConfig/GCAP3187-emily.json
```

- The converter reads name/style/model/teacherEmail from the YAML block.
- The three sections populate `welcomePrompt`, `reportGenerationInstructions`, and `systemPrompt` in JSON.

## Dependencies
- Optional: `pyyaml` to parse YAML front-matter. If not installed, conversion will still run only if you avoid changing the YAML (existing content is preserved in the MD, but front-matter parsing is required). Install with:

```bash
pip install pyyaml
```

## Tips
- Keep the headings unchanged so the converter can find them.
- Preserve special tokens like `_3Q3Q_` and `ok` exactly.
- Commit both the `.EDITABLE.md` and the generated `.json` so changes are transparent in reviews.