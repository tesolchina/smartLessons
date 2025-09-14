#!/bin/bash
# Auto-sync daemon for GCAP3187 Emily bot
# This is a simpler shell script version of the Python auto-sync

set -e

# Configuration
REPO_URL="https://github.com/tesolchina/smartLessons.git"
LOCAL_CLONE_DIR="/tmp/smartLessons_auto_sync"
SOURCE_FOLDER="/Users/simonwang/Documents/Usage/VibeCoding/DailyAssistant/projects/Jackie/GCAP3187-emily"
TARGET_FOLDER="GCAPJackie"
SYNC_INTERVAL=600  # 10 minutes
BRANCH="main"
LOG_FILE="jackie_sync.log"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
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
    echo -e "${YELLOW}[$(date '+%Y-%m-%d %H:%M:%S')] INFO: $1${NC}" | tee -a "$LOG_FILE"
}

setup_git_auth() {
    if [ -n "$GITHUB_TOKEN" ]; then
        echo "https://$GITHUB_TOKEN@github.com/tesolchina/smartLessons.git"
    else
        log_info "No GITHUB_TOKEN found. Using default authentication."
        echo "$REPO_URL"
    fi
}

clone_or_update_repo() {
    local repo_url=$1
    
    if [ -d "$LOCAL_CLONE_DIR" ]; then
        log_info "Updating existing repo at $LOCAL_CLONE_DIR"
        cd "$LOCAL_CLONE_DIR"
        git fetch origin
        git reset --hard "origin/$BRANCH"
    else
        log_info "Cloning repo to $LOCAL_CLONE_DIR"
        git clone "$repo_url" "$LOCAL_CLONE_DIR"
        cd "$LOCAL_CLONE_DIR"
        git checkout "$BRANCH"
    fi
}

sync_files() {
    if [ ! -d "$SOURCE_FOLDER" ]; then
        log_error "Source folder does not exist: $SOURCE_FOLDER"
        return 1
    fi
    
    local target_path="$LOCAL_CLONE_DIR/$TARGET_FOLDER"
    mkdir -p "$target_path"
    
    # Use rsync to sync files (with delete to remove files not in source)
    if command -v rsync >/dev/null 2>&1; then
        rsync -av --delete "$SOURCE_FOLDER/" "$target_path/"
    else
        # Fallback to cp if rsync is not available
        rm -rf "$target_path"/*
        cp -r "$SOURCE_FOLDER"/* "$target_path"/
    fi
    
    log_info "Synced files from $SOURCE_FOLDER to $target_path"
    return 0
}

commit_and_push() {
    cd "$LOCAL_CLONE_DIR"
    
    # Check if there are any changes
    if git diff --exit-code >/dev/null 2>&1 && git diff --cached --exit-code >/dev/null 2>&1; then
        log_info "No changes to commit"
        return 1
    fi
    
    # Stage all changes
    git add .
    
    # Commit with timestamp
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    local commit_message="Auto-sync GCAP3187 Emily bot - $timestamp"
    git commit -m "$commit_message"
    
    # Push to remote
    git push origin "$BRANCH"
    log_success "Committed and pushed changes: $commit_message"
    return 0
}

sync_cycle() {
    log_info "Starting sync cycle..."
    
    local repo_url
    repo_url=$(setup_git_auth)
    
    if clone_or_update_repo "$repo_url" && sync_files; then
        if commit_and_push; then
            log_success "✅ Sync completed successfully"
        else
            log_info "📝 No changes to sync"
        fi
    else
        log_error "❌ Sync cycle failed"
        return 1
    fi
}

main() {
    log_info "Starting Jackie auto-sync service..."
    log_info "Source: $SOURCE_FOLDER"
    log_info "Target: $REPO_URL -> $TARGET_FOLDER"
    log_info "Sync interval: $SYNC_INTERVAL seconds"
    log_info "Log file: $LOG_FILE"
    
    # Handle Ctrl+C gracefully
    trap 'log_info "Auto-sync service stopped by user"; exit 0' INT
    
    while true; do
        if ! sync_cycle; then
            log_error "Sync cycle failed, continuing..."
        fi
        
        log_info "Waiting $SYNC_INTERVAL seconds until next sync..."
        sleep "$SYNC_INTERVAL"
    done
}

# Check if script is being sourced or executed
if [ "${BASH_SOURCE[0]}" = "${0}" ]; then
    main "$@"
fi