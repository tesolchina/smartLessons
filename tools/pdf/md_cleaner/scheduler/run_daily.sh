#!/bin/zsh
# Wrapper to run the batch at 12:30pm via launchd. Assumes repo is at fixed path.
# Customize INPUT_DIRS and OUTPUT_DIR as needed.

set -euo pipefail

REPO="/Users/simonwang/Documents/Usage/VibeCoding/DailyAssistant"
cd "$REPO"

INPUT_DIRS=(
  "$REPO/projects/goal-setting-chatbot-paper/literature/papersToAddressinDiscussion"
  "$REPO/projects/goal-setting-chatbot-paper/literature/references"
)
OUTPUT_DIR="$REPO/projects/goal-setting-chatbot-paper/literature/doneProcess"

python3 operating/pdf_md_cleaner/batch/run_folder.py \
  --inputs ${INPUT_DIRS[@]} \
  --output "$OUTPUT_DIR" \
  --model anthropic/claude-3.2 \
  --chunk-chars 4000 \
  --max-tokens 900 \
  --delete-raw-md
