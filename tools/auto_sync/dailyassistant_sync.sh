#!/bin/bash
# Auto-sync daemon for DailyAssistant repository
# This script automatically commits and pushes the entire repo every 10 minutes

set -e

# Configuration
REPO_PATH="/Users/simonwang/Documents/Usage/VibeCoding/DailyAssistant"
SYNC_INTERVAL=600  # 10 minutes
BRANCH="main"
LOG_FILE="$REPO_PATH/auto_sync.log"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log_error() {
    echo -e "${RED}[$(date '+%Y-%m-%d %H:%M:%S')] ERROR: $1${NC}" | tee -a "$LOG_FILE"
}

log_success() {
    echo -e "${GREEN}[$(date '+%Y-%m-%d %H:%M:%S')] SUCCESS: $1${NC}" | tee -a "$LOG_FILE"
}

log_info() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')] INFO: $1${NC}" | tee -a "$LOG_FILE"
}

log_warning() {
    echo -e "${YELLOW}[$(date '+%Y-%m-%d %H:%M:%S')] WARNING: $1${NC}" | tee -a "$LOG_FILE"
}

check_git_repo() {
    cd "$REPO_PATH" || {
        log_error "Cannot access repository path: $REPO_PATH"
        return 1
    }
    
    if ! git rev-parse --git-dir >/dev/null 2>&1; then
        log_error "Directory is not a git repository: $REPO_PATH"
        return 1
    fi
    
    local current_branch
    current_branch=$(git branch --show-current)
    if [ "$current_branch" != "$BRANCH" ]; then
        log_warning "Current branch is '$current_branch', expected '$BRANCH'"
    fi
    
    if ! git remote get-url origin >/dev/null 2>&1; then
        log_error "No remote origin configured"
        return 1
    fi
    
    local remote_url
    remote_url=$(git remote get-url origin)
    log_info "Remote origin: $remote_url"
    return 0
}

has_changes() {
    cd "$REPO_PATH"
    
    # Check for unstaged changes
    if ! git diff --exit-code >/dev/null 2>&1; then
        return 0  # Has changes
    fi
    
    # Check for staged changes
    if ! git diff --cached --exit-code >/dev/null 2>&1; then
        return 0  # Has changes
    fi
    
    # Check for untracked files (that aren't ignored)
    local untracked
    untracked=$(git ls-files --others --exclude-standard)
    if [ -n "$untracked" ]; then
        return 0  # Has changes
    fi
    
    return 1  # No changes
}

commit_and_push() {
    cd "$REPO_PATH"
    
    # Pull latest changes first to avoid conflicts
    log_info "Pulling latest changes..."
    if ! git pull --rebase; then
        log_error "Failed to pull latest changes"
        return 1
    fi
    
    # Stage all changes
    git add .
    
    # Create commit message with timestamp
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    local commit_message="Auto-sync: $timestamp"
    
    # Commit changes
    if ! git commit -m "$commit_message"; then
        log_error "Failed to commit changes"
        return 1
    fi
    
    # Push to remote
    log_info "Pushing changes..."
    if ! git push; then
        log_error "Failed to push changes"
        return 1
    fi
    
    log_success "✅ Successfully committed and pushed: $commit_message"
    return 0
}

sync_cycle() {
    log_info "🔄 Starting sync cycle..."
    
    if ! has_changes; then
        log_info "📝 No changes detected"
        return 0
    fi
    
    log_info "📁 Changes detected, committing..."
    if commit_and_push; then
        return 0
    else
        log_error "❌ Sync cycle failed"
        return 1
    fi
}

main() {
    log_info "🚀 Starting DailyAssistant auto-sync service..."
    log_info "📂 Repository: $REPO_PATH"
    log_info "⏱️  Sync interval: $SYNC_INTERVAL seconds ($((SYNC_INTERVAL/60)) minutes)"
    log_info "📝 Log file: $LOG_FILE"
    
    # Verify git repository
    if ! check_git_repo; then
        log_error "❌ Git repository check failed"
        exit 1
    fi
    
    # Handle Ctrl+C gracefully
    trap 'log_info "⏹️  Auto-sync service stopped by user"; exit 0' INT
    
    # Initial sync
    sync_cycle
    
    # Main loop
    while true; do
        log_info "💤 Waiting $SYNC_INTERVAL seconds until next sync..."
        sleep "$SYNC_INTERVAL"
        sync_cycle
    done
}

# Check if script is being sourced or executed
if [ "${BASH_SOURCE[0]}" = "${0}" ]; then
    main "$@"
fi