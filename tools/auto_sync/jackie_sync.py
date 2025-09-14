#!/usr/bin/env python3
"""
Auto-sync script for DailyAssistant repository to GitHub.

This script automatically commits and pushes the entire DailyAssistant folder
to the GitHub repo every 10 minutes.

Usage:
  python tools/auto_sync/dailyassistant_sync.py

Environment variables needed:
  GITHUB_TOKEN - Personal access token with repo permissions
  
Or configure git credentials manually:
  git config --global user.name "Your Name"
  git config --global user.email "your.email@example.com"
"""

import os
import subprocess
import sys
import time
import logging
from datetime import datetime
from pathlib import Path

# Configuration
REPO_URL = "https://github.com/tesolchina/DailyAssistant.git"
SOURCE_FOLDER = "/Users/simonwang/Documents/Usage/VibeCoding/DailyAssistant"
SYNC_INTERVAL = 600  # 10 minutes in seconds
BRANCH = "main"
EXCLUDE_PATTERNS = [
    ".git/",
    "__pycache__/",
    "*.pyc",
    ".DS_Store",
    "node_modules/",
    ".env",
    "*.log",
    ".vscode/",
    "venv/",
    ".pytest_cache/",
    "*.tmp"
]

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('jackie_sync.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


def run_command(cmd, cwd=None, capture_output=True):
    """Run a shell command and return the result."""
    try:
        result = subprocess.run(
            cmd, 
            shell=True, 
            cwd=cwd, 
            capture_output=capture_output,
            text=True,
            check=True
        )
        return result.stdout.strip() if capture_output else ""
    except subprocess.CalledProcessError as e:
        logger.error(f"Command failed: {cmd}")
        logger.error(f"Error: {e.stderr if e.stderr else str(e)}")
        raise


def setup_git_auth():
    """Setup git authentication using GitHub token if available."""
    github_token = os.environ.get('GITHUB_TOKEN')
    if github_token:
        # Use token-based authentication
        authenticated_url = REPO_URL.replace(
            'https://github.com/', 
            f'https://{github_token}@github.com/'
        )
        return authenticated_url
    else:
        logger.warning("No GITHUB_TOKEN found. Make sure git credentials are configured.")
        return REPO_URL


def clone_or_update_repo(repo_url):
    """Clone the repo if it doesn't exist, otherwise pull latest changes."""
    if os.path.exists(LOCAL_CLONE_DIR):
        logger.info(f"Updating existing repo at {LOCAL_CLONE_DIR}")
        run_command("git fetch origin", cwd=LOCAL_CLONE_DIR)
        run_command(f"git reset --hard origin/{BRANCH}", cwd=LOCAL_CLONE_DIR)
    else:
        logger.info(f"Cloning repo to {LOCAL_CLONE_DIR}")
        run_command(f"git clone {repo_url} {LOCAL_CLONE_DIR}")
        run_command(f"git checkout {BRANCH}", cwd=LOCAL_CLONE_DIR)


def sync_files():
    """Copy files from source to target directory."""
    source_path = Path(SOURCE_FOLDER)
    target_path = Path(LOCAL_CLONE_DIR) / TARGET_FOLDER
    
    if not source_path.exists():
        logger.error(f"Source folder does not exist: {SOURCE_FOLDER}")
        return False
    
    # Create target directory if it doesn't exist
    target_path.mkdir(parents=True, exist_ok=True)
    
    # Copy all files from source to target
    run_command(f"rsync -av --delete {source_path}/ {target_path}/")
    logger.info(f"Synced files from {source_path} to {target_path}")
    return True


def commit_and_push():
    """Commit changes and push to GitHub."""
    # Check if there are any changes
    try:
        run_command("git diff --exit-code", cwd=LOCAL_CLONE_DIR)
        run_command("git diff --cached --exit-code", cwd=LOCAL_CLONE_DIR)
        logger.info("No changes to commit")
        return False
    except subprocess.CalledProcessError:
        # There are changes, proceed with commit
        pass
    
    # Stage all changes
    run_command("git add .", cwd=LOCAL_CLONE_DIR)
    
    # Commit with timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    commit_message = f"Auto-sync GCAP3187 Emily bot - {timestamp}"
    run_command(f'git commit -m "{commit_message}"', cwd=LOCAL_CLONE_DIR)
    
    # Push to remote
    run_command(f"git push origin {BRANCH}", cwd=LOCAL_CLONE_DIR)
    logger.info(f"Committed and pushed changes: {commit_message}")
    return True


def main():
    """Main sync loop."""
    logger.info("Starting Jackie auto-sync service...")
    logger.info(f"Source: {SOURCE_FOLDER}")
    logger.info(f"Target: {REPO_URL} -> {TARGET_FOLDER}")
    logger.info(f"Sync interval: {SYNC_INTERVAL} seconds")
    
    # Setup authentication
    repo_url = setup_git_auth()
    
    try:
        while True:
            try:
                logger.info("Starting sync cycle...")
                
                # Clone/update repo
                clone_or_update_repo(repo_url)
                
                # Sync files
                if sync_files():
                    # Commit and push
                    if commit_and_push():
                        logger.info("✅ Sync completed successfully")
                    else:
                        logger.info("📝 No changes to sync")
                else:
                    logger.error("❌ File sync failed")
                
            except Exception as e:
                logger.error(f"Sync cycle failed: {str(e)}")
            
            # Wait for next cycle
            logger.info(f"Waiting {SYNC_INTERVAL} seconds until next sync...")
            time.sleep(SYNC_INTERVAL)
            
    except KeyboardInterrupt:
        logger.info("Auto-sync service stopped by user")
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()