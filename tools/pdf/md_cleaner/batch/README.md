# Batch Runner: PDF → Clean Markdown

Run the routine on all PDFs in one or more folders, skipping duplicates by file name, and write results to a `doneProcess` folder with a summary report.

Example:
```bash
python3 operating/pdf_md_cleaner/batch/run_folder.py \
  --inputs \
    projects/goal-setting-chatbot-paper/literature/papersToAddressinDiscussion \
    projects/goal-setting-chatbot-paper/literature/references \
  --output projects/goal-setting-chatbot-paper/literature/doneProcess \
  --model anthropic/claude-3.2 \
  --chunk-chars 4000 \
  --max-tokens 900 \
  --delete-raw-md
```
- Duplicates are skipped across inputs by case-insensitive basename match.
- The cleaned outputs are moved to `--output`, and an index file `BATCH_REPORT.md` is created.
- Use `--move-pdf` to copy the original PDFs into `--output` as well.
