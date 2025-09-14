#!/usr/bin/env python3
"""
Auto-sync script for DailyAssistant repository to GitHub.

This script automatically commits and pushes the entire DailyAssistant folder
to the GitHub repo every 10 minutes.

Usage:
  python tools/auto_sync/dailyassistant_sync.py

Requirements:
- Must be run from within the DailyAssistant git repository
- Git credentials must be configured (or GITHUB_TOKEN environment variable)
"""

import os
import subprocess
import sys
import time
import logging
from datetime import datetime
from pathlib import Path

# Configuration
REPO_PATH = "/Users/simonwang/Documents/Usage/VibeCoding/DailyAssistant"
SYNC_INTERVAL = 600  # 10 minutes in seconds
BRANCH = "main"

# Files/patterns to exclude from auto-commits
GITIGNORE_ADDITIONS = [
    "*.log",
    "__pycache__/",
    "*.pyc",
    ".DS_Store",
    "node_modules/",
    ".env",
    "venv/",
    ".pytest_cache/",
    "*.tmp",
    ".vscode/settings.json"
]

# Setup logging
log_file = os.path.join(REPO_PATH, "auto_sync.log")
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


def run_command(cmd, capture_output=True):
    """Run a shell command in the repo directory and return the result."""
    try:
        result = subprocess.run(
            cmd, 
            shell=True, 
            cwd=REPO_PATH,
            capture_output=capture_output,
            text=True,
            check=True
        )
        return result.stdout.strip() if capture_output else ""
    except subprocess.CalledProcessError as e:
        logger.error(f"Command failed: {cmd}")
        logger.error(f"Error: {e.stderr if e.stderr else str(e)}")
        raise


def check_git_repo():
    """Verify we're in a git repository and on the correct branch."""
    try:
        # Check if we're in a git repo
        run_command("git rev-parse --git-dir")
        
        # Check current branch
        current_branch = run_command("git branch --show-current")
        if current_branch != BRANCH:
            logger.warning(f"Current branch is '{current_branch}', expected '{BRANCH}'")
            
        # Check if repo has remote origin
        try:
            remote_url = run_command("git remote get-url origin")
            logger.info(f"Remote origin: {remote_url}")
        except subprocess.CalledProcessError:
            logger.error("No remote origin configured")
            return False
            
        return True
    except subprocess.CalledProcessError:
        logger.error(f"Directory {REPO_PATH} is not a git repository")
        return False


def update_gitignore():
    """Add auto-sync specific patterns to .gitignore if not already present."""
    gitignore_path = os.path.join(REPO_PATH, ".gitignore")
    
    # Read existing .gitignore
    existing_patterns = set()
    if os.path.exists(gitignore_path):
        with open(gitignore_path, 'r') as f:
            existing_patterns = set(line.strip() for line in f if line.strip() and not line.startswith('#'))
    
    # Add new patterns if not already present
    new_patterns = []
    for pattern in GITIGNORE_ADDITIONS:
        if pattern not in existing_patterns:
            new_patterns.append(pattern)
    
    if new_patterns:
        with open(gitignore_path, 'a') as f:
            f.write("\n# Auto-sync exclusions\n")
            for pattern in new_patterns:
                f.write(f"{pattern}\n")
        logger.info(f"Added {len(new_patterns)} patterns to .gitignore")


def has_changes():
    """Check if there are any uncommitted changes."""
    try:
        # Check for unstaged changes
        run_command("git diff --exit-code")
        # Check for staged changes
        run_command("git diff --cached --exit-code")
        # Check for untracked files (that aren't ignored)
        untracked = run_command("git ls-files --others --exclude-standard")
        return bool(untracked.strip())
    except subprocess.CalledProcessError:
        # There are changes
        return True


def commit_and_push():
    """Commit all changes and push to remote."""
    try:
        # Stage all changes first
        logger.info("Staging all changes...")
        run_command("git add .")
        
        # Create commit message with timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        commit_message = f"Auto-sync: {timestamp}"
        
        # Commit changes
        run_command(f'git commit -m "{commit_message}"')
        
        # Pull latest changes with merge strategy (safer than rebase for auto-commits)
        logger.info("Pulling latest changes...")
        try:
            run_command("git pull --no-rebase")
        except subprocess.CalledProcessError:
            # If pull fails due to conflicts, try to push anyway (we're ahead)
            logger.warning("Pull failed, attempting direct push...")
        
        # Push to remote
        logger.info("Pushing changes...")
        run_command("git push")
        
        logger.info(f"✅ Successfully committed and pushed: {commit_message}")
        return True
        
    except subprocess.CalledProcessError as e:
        logger.error(f"❌ Failed to commit/push: {str(e)}")
        return False


def sync_cycle():
    """Perform one sync cycle."""
    logger.info("🔄 Starting sync cycle...")
    
    if not has_changes():
        logger.info("📝 No changes detected")
        return True
    
    logger.info("📁 Changes detected, committing...")
    return commit_and_push()


def main():
    """Main auto-sync loop."""
    logger.info("🚀 Starting DailyAssistant auto-sync service...")
    logger.info(f"📂 Repository: {REPO_PATH}")
    logger.info(f"⏱️  Sync interval: {SYNC_INTERVAL} seconds ({SYNC_INTERVAL//60} minutes)")
    logger.info(f"📝 Log file: {log_file}")
    
    # Verify git repository
    if not check_git_repo():
        logger.error("❌ Git repository check failed")
        sys.exit(1)
    
    # Update .gitignore
    update_gitignore()
    
    # Initial sync
    sync_cycle()
    
    try:
        while True:
            time.sleep(SYNC_INTERVAL)
            sync_cycle()
            
    except KeyboardInterrupt:
        logger.info("⏹️  Auto-sync service stopped by user")
    except Exception as e:
        logger.error(f"💥 Fatal error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()