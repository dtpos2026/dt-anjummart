#!/usr/bin/env bash
# Plans and reels only.   Usage: build_reels.sh <cutouts_dir> <work_dir> [--preview]
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
export PLAYWRIGHT_FROM="${PLAYWRIGHT_FROM:-/opt/node22/lib/node_modules/}"
CUTS="$1"; W="$2"; PREVIEW="${3:-}"
PERF="$HERE/../catalog/art/perfume-photos"
mkdir -p "$W"

echo "== 2. plans"; python3 "$HERE/video/build_plans.py" "$CUTS" "$PERF" "$W/plans" $PREVIEW

echo "== 3. reels (one at a time, 4 browser workers each)"
mkdir -p "$W/reels" "$W/posters"
for plan in "$W"/plans/R-*.json; do
  id="$(basename "$plan" .json)"
  if [ -s "$W/reels/$id.mp4" ]; then echo "$id exists"; else bash "$HERE/video/make_video.sh" "$plan" "$W/reels/$id.mp4" 4; fi
  if [ ! -s "$W/posters/$id.jpg" ]; then
    t="$(python3 - "$plan" <<'PY'
import json, sys
p = json.load(open(sys.argv[1]))
ty = p['type']
if ty == 'product':
    t = p['t']['price'] + 0.6
elif ty == 'collection':
    t = p['slots'][0]['start'] + 1.2
elif ty == 'brand':
    t = p['slots'][1]['start'] + 0.8
else:
    t = p['slots'][7]['start'] + 0.6
print(t)
PY
)"
    ffmpeg -y -hide_banner -loglevel error -ss "$t" -i "$W/reels/$id.mp4" -frames:v 1 -q:v 2 "$W/posters/$id.jpg"
  fi
done

