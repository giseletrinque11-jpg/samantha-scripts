#!/bin/bash
# backup_brain.sh — Samantha full brain backup to GitHub
# Backs up all critical state (~2MB) to samantha-brain private repo
# Run manually or via cron

set -e

BRAIN_DIR="/tmp/samantha-brain"
OPENCLAW="$HOME/.openclaw"
WORKSPACE="$OPENCLAW/workspace"
DATE=$(date +%Y-%m-%d)
TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")

echo "[$TIMESTAMP] Starting brain backup..."

# ── 1. Sync critical OpenClaw config ──────────────────────────────────
mkdir -p "$BRAIN_DIR/openclaw"
cp "$OPENCLAW/openclaw.json" "$BRAIN_DIR/openclaw/"
rsync -a --delete "$OPENCLAW/cron/"        "$BRAIN_DIR/openclaw/cron/"
rsync -a --delete "$OPENCLAW/credentials/" "$BRAIN_DIR/openclaw/credentials/"
rsync -a --delete "$OPENCLAW/identity/"    "$BRAIN_DIR/openclaw/identity/"
rsync -a --delete "$OPENCLAW/adapters/"    "$BRAIN_DIR/openclaw/adapters/"

# ── 2. Sync workspace brain (memory + scripts + md files) ─────────────
mkdir -p "$BRAIN_DIR/workspace"
rsync -a --delete "$WORKSPACE/memory/"  "$BRAIN_DIR/workspace/memory/"
rsync -a --delete "$WORKSPACE/scripts/" "$BRAIN_DIR/workspace/scripts/"
rsync -a --delete "$WORKSPACE/archive/" "$BRAIN_DIR/workspace/archive/"

# Markdown brain files
for f in MEMORY.md SOUL.md AGENTS.md USER.md TOOLS.md IDENTITY.md HEARTBEAT.md; do
    [ -f "$WORKSPACE/$f" ] && cp "$WORKSPACE/$f" "$BRAIN_DIR/workspace/"
done

# .env (secrets — private repo only)
[ -f "$WORKSPACE/.env" ] && cp "$WORKSPACE/.env" "$BRAIN_DIR/workspace/"
[ -f "$WORKSPACE/.env.example" ] && cp "$WORKSPACE/.env.example" "$BRAIN_DIR/workspace/"

# ── 3. Sync SSH keys ──────────────────────────────────────────────────
mkdir -p "$BRAIN_DIR/ssh"
cp "$HOME/.ssh/id_ed25519"     "$BRAIN_DIR/ssh/" 2>/dev/null || true
cp "$HOME/.ssh/id_ed25519.pub" "$BRAIN_DIR/ssh/" 2>/dev/null || true

# ── 4. Sync ngrok config ──────────────────────────────────────────────
mkdir -p "$BRAIN_DIR/ngrok"
cp "$HOME/.config/ngrok/ngrok.yml" "$BRAIN_DIR/ngrok/"

# ── 5. Write restore script ───────────────────────────────────────────
cat > "$BRAIN_DIR/RESTORE.md" << 'RESTORE'
# Samantha Restore Guide

## Requirements
- Ubuntu/Debian machine
- Node.js + npm
- Python 3

## Steps

### 1. Install OpenClaw
```bash
npm install -g openclaw
```

### 2. Restore config
```bash
cp openclaw/openclaw.json ~/.openclaw/
cp -r openclaw/cron/ ~/.openclaw/
cp -r openclaw/credentials/ ~/.openclaw/
cp -r openclaw/identity/ ~/.openclaw/
cp -r openclaw/adapters/ ~/.openclaw/
```

### 3. Restore workspace
```bash
mkdir -p ~/.openclaw/workspace
cp -r workspace/memory/ ~/.openclaw/workspace/
cp -r workspace/scripts/ ~/.openclaw/workspace/
cp -r workspace/archive/ ~/.openclaw/workspace/
cp workspace/*.md ~/.openclaw/workspace/
cp workspace/.env ~/.openclaw/workspace/
```

### 4. Restore SSH + ngrok
```bash
cp ssh/id_ed25519 ~/.ssh/
cp ssh/id_ed25519.pub ~/.ssh/
chmod 600 ~/.ssh/id_ed25519
cp ngrok/ngrok.yml ~/.config/ngrok/
```

### 5. Install Python dependencies
```bash
pip3 install blinkpy flask requests opencv-python-headless
```

### 6. Start OpenClaw
```bash
openclaw start
```

Samantha is restored. Full memory, cron jobs, integrations — all back.
RESTORE

# ── 6. Git commit and push ────────────────────────────────────────────
cd "$BRAIN_DIR"
git add -A
git diff --cached --quiet && echo "[$TIMESTAMP] No changes — backup up to date." && exit 0

git commit -m "Brain backup — $DATE"
git push -u origin master 2>&1

echo "[$TIMESTAMP] Brain backup complete ✅"
