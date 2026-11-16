#!/usr/bin/env bash
# Builds the whole Anjum Mart launch kit (reels, pictures, PDFs, zips).
#
# Usage:
#   build_all.sh --store <out_dir>                 final kit; downloads the product photos from the public storefront (anjummart.com)
#   build_all.sh <photos_dir> <out_dir>            final kit from your own photos: white-background shots named
#                                                  M1.jpg ... M10, W1 ... W5, J1, J2 (or by store product handle)
#   build_all.sh --preview <cutouts_dir> <out_dir> placeholder kit for checking the look: every reel gets a PREVIEW ribbon
# Needs: python3 (pillow, numpy, scipy, rembg for the final kit), node + playwright, ffmpeg, zip.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
export PLAYWRIGHT_FROM="${PLAYWRIGHT_FROM:-/opt/node22/lib/node_modules/}"
PREVIEW=""
if [ "${1:-}" = "--preview" ]; then PREVIEW="--preview"; shift; fi
FROM_STORE=""
if [ "${1:-}" = "--store" ]; then FROM_STORE=1; set -- "" "$2"; fi
SRC="$1"; OUT="$(mkdir -p "$2" && cd "$2" && pwd)"
PERF="$HERE/../catalog/art/perfume-photos"
W="$OUT/work"; mkdir -p "$W"

if [ -n "$PREVIEW" ]; then CUTS="$SRC"; else
  if [ -n "$FROM_STORE" ]; then echo "== 0. photos from the store"; python3 "$HERE/video/fetch_store_photos.py" "$W/photos"; SRC="$W/photos"; fi
  echo "== 1. cut-outs"; python3 "$HERE/video/make_cutouts.py" "$SRC" "$W/cuts"; CUTS="$W/cuts"
fi

bash "$HERE/build_reels.sh" "$CUTS" "$W" $PREVIEW

echo "== 4. pictures"
rm -rf "$W/posts"
python3 "$HERE/content/make_posts.py" "$CUTS" "$PERF" "$W/posts"
node "$HERE/ads/render.mjs" "$W/posts"
python3 "$HERE/content/make_store_images.py" "$CUTS" "$W/store-white-studio"

echo "== 4b. launch kit"
rm -rf "$W/launch"; mkdir -p "$W/launch"
python3 "$HERE/content/make_launch_kit.py" "$W/posts/final" "$W/posters" "$W/reels" "$W/launch"
node "$HERE/ads/render.mjs" "$W/launch"

echo "== 5. PDFs and caption files"
python3 "$HERE/content/build_calendar.py" "$W/posts/final" "$W/posters" "$W/calendar"
python3 "$HERE/content/build_playbook.py" "$W/posts/final" "$W/posters" "$W/playbook"

echo "== 6. zips"
python3 "$HERE/content/package.py" "$W" "$OUT" $PREVIEW
echo "done: $OUT"
