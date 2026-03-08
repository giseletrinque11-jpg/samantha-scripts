#!/bin/bash
# rsync_backup.sh — Samantha local rotating snapshot backup
# Uses hardlinks for space-efficient daily + weekly snapshots
# Keeps: 7 daily snapshots + 4 weekly snapshots
#
# Destination is configurable — point to external drive or NAS by changing BACKUP_ROOT
# e.g. BACKUP_ROOT="/mnt/external/samantha" for USB drive
#      BACKUP_ROOT="/mnt/nas/samantha" for network share

set -uo pipefail

# ── Config ────────────────────────────────────────────────────────────
BACKUP_ROOT="${SAMANTHA_BACKUP_DIR:-$HOME/backup/samantha}"
SOURCE_OPENCLAW="$HOME/.openclaw"
SOURCE_SSH="$HOME/.ssh"
SOURCE_NGROK="$HOME/.config/ngrok"

DAILY_KEEP=7
WEEKLY_KEEP=4
LOG_FILE="$BACKUP_ROOT/backup.log"
TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")
DATE=$(date +%Y-%m-%d)
DOW=$(date +%u)  # 1=Monday ... 7=Sunday

# ── Exclusions (large/reinstallable items) ────────────────────────────
EXCLUDES=(
    --exclude=".venv/"
    --exclude=".git/"
    --exclude="workspace/data/"
    --exclude="workspace/snaps/"
    --exclude="workspace/camera_checks/"
    --exclude="workspace/*.jpg"
    --exclude="workspace/*.mp4"
    --exclude="workspace/projects/"
    --exclude="browser/"
    --exclude="media/"
    --exclude="logs/"
    --exclude="subagents/"
    --exclude="delivery-queue/"
    --exclude="agents/main/sessions/"
    --exclude="completions/"
    --exclude="*.log"
    --exclude="node_modules/"
)

# ── Helpers ───────────────────────────────────────────────────────────
log() { echo "[$TIMESTAMP] $*" | tee -a "$LOG_FILE"; }

rotate_snapshots() {
    local prefix=$1
    local keep=$2

    # Drop oldest
    [ -d "$BACKUP_ROOT/${prefix}.${keep}" ] && rm -rf "$BACKUP_ROOT/${prefix}.${keep}"

    # Rotate: .N-1 → .N
    for (( i=keep-1; i>=1; i-- )); do
        [ -d "$BACKUP_ROOT/${prefix}.$((i-1))" ] && \
            mv "$BACKUP_ROOT/${prefix}.$((i-1))" "$BACKUP_ROOT/${prefix}.${i}"
    done
}

# ── Main ──────────────────────────────────────────────────────────────
mkdir -p "$BACKUP_ROOT"
log "Starting rsync backup..."

# Determine link-dest (previous snapshot to hardlink against)
LINK_DEST=""
if [ -d "$BACKUP_ROOT/daily.0" ]; then
    LINK_DEST="--link-dest=$BACKUP_ROOT/daily.0"
fi

# Rotate daily snapshots
rotate_snapshots "daily" "$DAILY_KEEP"

# Create new daily.0
mkdir -p "$BACKUP_ROOT/daily.0"

# Sync OpenClaw (the brain)
log "Syncing OpenClaw config..."
rsync -a --delete $LINK_DEST \
    "${EXCLUDES[@]}" \
    "$SOURCE_OPENCLAW/" \
    "$BACKUP_ROOT/daily.0/openclaw/"

# Sync SSH keys
log "Syncing SSH keys..."
rsync -a --delete $LINK_DEST \
    "$SOURCE_SSH/" \
    "$BACKUP_ROOT/daily.0/ssh/"

# Sync ngrok config
log "Syncing ngrok config..."
rsync -a --delete $LINK_DEST \
    "$SOURCE_NGROK/" \
    "$BACKUP_ROOT/daily.0/ngrok/"

# Write snapshot metadata
echo "{\"timestamp\": \"$TIMESTAMP\", \"date\": \"$DATE\"}" > "$BACKUP_ROOT/daily.0/.snapshot_meta.json"

# ── Weekly snapshot (every Sunday = DOW 7) ────────────────────────────
if [ "$DOW" -eq 7 ]; then
    log "Sunday — creating weekly snapshot..."
    rotate_snapshots "weekly" "$WEEKLY_KEEP"
    cp -al "$BACKUP_ROOT/daily.0" "$BACKUP_ROOT/weekly.0"
    log "Weekly snapshot created."
fi

# ── Report ────────────────────────────────────────────────────────────
SNAPSHOT_SIZE=$(du -sh "$BACKUP_ROOT/daily.0" 2>/dev/null | cut -f1)
TOTAL_SIZE=$(du -sh "$BACKUP_ROOT" 2>/dev/null | cut -f1)
DAILY_COUNT=$(ls -d "$BACKUP_ROOT"/daily.* 2>/dev/null | wc -l)
WEEKLY_COUNT=$(ls -d "$BACKUP_ROOT"/weekly.* 2>/dev/null | wc -l)

log "Backup complete ✅"
log "  Snapshot size: $SNAPSHOT_SIZE"
log "  Total backup dir: $TOTAL_SIZE"
log "  Daily snapshots: $DAILY_COUNT / $DAILY_KEEP"
log "  Weekly snapshots: $WEEKLY_COUNT / $WEEKLY_KEEP"

echo "rsync_backup OK | date=$DATE | snapshot=$SNAPSHOT_SIZE | total=$TOTAL_SIZE | daily=$DAILY_COUNT | weekly=$WEEKLY_COUNT"
