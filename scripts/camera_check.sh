#!/usr/bin/env bash
# camera_check.sh — Hourly security check for all Blink cameras
# Captures all cameras and saves snapshots for AI vision analysis
# Run via cron every hour

WORKSPACE=~/.openclaw/workspace
SNAP_SCRIPT="$WORKSPACE/scripts/blink_snap.py"
OUTDIR="$WORKSPACE/camera_checks"
TIMESTAMP=$(date '+%Y-%m-%d_%H%M')

mkdir -p "$OUTDIR"

CAMERAS=(
  "porte arrière"
  "shed extérieur"
  "cour arrière"
  "entré cour"
  "front door ext"
  "cave"
  "salon"
  "tool"
  "garage intérieur"
  "front door intérieur"
  "garage avant porte"
  "grotte"
)

echo "📷 Camera check started — $TIMESTAMP"

for CAM in "${CAMERAS[@]}"; do
  SAFE_NAME=$(echo "$CAM" | tr ' ' '_' | tr -d 'éàâêîôùûç')
  OUTFILE="$OUTDIR/${SAFE_NAME}_${TIMESTAMP}.jpg"
  
  python3 "$SNAP_SCRIPT" "$CAM" --output "$OUTFILE" 2>/dev/null \
    && echo "  ✓ $CAM" \
    || echo "  ✗ $CAM (failed)"
done

echo "Camera check complete. Images saved to $OUTDIR"
echo "CAMERA_CHECK_DONE:$TIMESTAMP"
