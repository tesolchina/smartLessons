# DailyAssistant Auto-Sync

These scripts automatically commit and push the entire DailyAssistant repository to GitHub every 10 minutes.

## Files

- `dailyassistant_sync.py` — Python version with detailed logging
- `dailyassistant_sync.sh` — Shell script version (lighter, faster)
- `jackie_sync.py` — Legacy Jackie-specific sync (deprecated)
- `jackie_sync.sh` — Legacy Jackie shell script (deprecated)

## Usage

### Python Version (Recommended)

```bash
cd /Users/simonwang/Documents/Usage/VibeCoding/DailyAssistant
python tools/auto_sync/dailyassistant_sync.py
```

### Shell Version (Faster startup)

```bash
cd /Users/simonwang/Documents/Usage/VibeCoding/DailyAssistant
chmod +x tools/auto_sync/dailyassistant_sync.sh
./tools/auto_sync/dailyassistant_sync.sh
```

### Background Mode (macOS/Linux)

To run in the background and keep it running:

```bash
# Start in background
nohup python tools/auto_sync/dailyassistant_sync.py > auto_sync_output.log 2>&1 &

# Or with the shell script
nohup ./tools/auto_sync/dailyassistant_sync.sh > auto_sync_output.log 2>&1 &

# Check if it's running
ps aux | grep dailyassistant_sync

# Stop the background process
pkill -f dailyassistant_sync
```

## How it works

1. **Repository Check**: Verifies you're in a git repository with a remote origin
2. **Change Detection**: Checks for:
   - Unstaged changes (`git diff`)
   - Staged changes (`git diff --cached`)
   - Untracked files (`git ls-files --others --exclude-standard`)
3. **Auto-commit**: If changes found:
   - Pulls latest changes with rebase
   - Stages all changes (`git add .`)
   - Commits with timestamp: "Auto-sync: YYYY-MM-DD HH:MM:SS"
   - Pushes to remote
4. **Wait**: Sleeps for 10 minutes, then repeats

## Automatic .gitignore

The Python version automatically adds these patterns to `.gitignore`:

```
# Auto-sync exclusions
*.log
__pycache__/
*.pyc
.DS_Store
node_modules/
.env
venv/
.pytest_cache/
*.tmp
.vscode/settings.json
```

## Configuration

Edit the scripts to change:

- `SYNC_INTERVAL`: Time between syncs (default: 600 seconds = 10 minutes)
- `REPO_PATH`: Path to the DailyAssistant repository
- `BRANCH`: Target branch (default: "main")

## Logs

Both scripts create logs:
- Python: `auto_sync.log` in the repository root + console output
- Shell: `auto_sync.log` in the repository root + colored console output

## Requirements

- Git repository with configured credentials or `GITHUB_TOKEN` environment variable
- Must be run from within the DailyAssistant directory
- Internet connection for pushing to GitHub

## Troubleshooting

### Authentication Issues

If you get authentication errors:

```bash
# Option 1: Set up GitHub token
export GITHUB_TOKEN="your_personal_access_token"

# Option 2: Configure git credentials
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Option 3: Use GitHub CLI
gh auth login
```

### Permission Issues

```bash
chmod +x tools/auto_sync/dailyassistant_sync.sh
```

### Process Management

```bash
# List running auto-sync processes
ps aux | grep -E "(dailyassistant_sync|jackie_sync)"

# Kill all auto-sync processes
pkill -f "dailyassistant_sync"

# Kill specific process by PID
kill <PID>
```

## Safety Features

- **Pull before push**: Always pulls latest changes to avoid conflicts
- **Change detection**: Only commits when there are actual changes
- **Error handling**: Continues running even if individual sync cycles fail
- **Graceful shutdown**: Handles Ctrl+C properly
- **Logging**: Detailed logs for debugging

## Migration from Jackie Sync

If you were using the old Jackie-specific sync scripts, switch to the new ones:

1. Stop the old script: `pkill -f jackie_sync`
2. Start the new script: `python tools/auto_sync/dailyassistant_sync.py`

The new scripts sync the entire repository, including the Jackie folder and everything else.