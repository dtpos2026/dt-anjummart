#!/usr/bin/env bash
# One reel: plan -> music -> frames -> MP4.   Usage: make_video.sh <plan.json> <out.mp4> [workers]
set -euo pipefail
PLAN="$1"; OUT="$2"; WORKERS="${3:-4}"
HERE="$(cd "$(dirname "$0")" && pwd)"
ID="$(basename "$PLAN" .json)"
TMP="$(mktemp -d)"
python3 "$HERE/audio/make_music.py" "$PLAN" "$TMP/audio.wav" >/dev/null
node "$HERE/engine/render.mjs" "$PLAN" "$TMP/frames" "$WORKERS" >/dev/null
mkdir -p "$(dirname "$OUT")"
ffmpeg -y -hide_banner -loglevel error -framerate 30 -i "$TMP/frames/f_%05d.jpg" -i "$TMP/audio.wav" \
  -af "loudnorm=I=-15:TP=-1.5:LRA=7" -c:v libx264 -preset medium -crf 24 -pix_fmt yuv420p -profile:v high -level 4.2 \
  -r 30 -movflags +faststart -c:a aac -b:a 160k -ar 44100 -shortest "$OUT"
rm -rf "$TMP"
echo "$ID -> $OUT"
