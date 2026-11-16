#!/usr/bin/env bash
# Zips the theme (only the folders Shopify reads) for Online Store, Themes, Add theme, Upload zip file.
# Usage: docs/tools/build_theme_zip.sh <output.zip>
set -euo pipefail
cd "$(dirname "$0")/../.."
python3 docs/tools/validate_theme_json.py
out="$(realpath -m "$1")"; rm -f "$out"
zip -qr "$out" assets config layout locales sections snippets templates -x '*.DS_Store'
echo "$out  $(du -h "$out" | cut -f1)  $(unzip -Z1 "$out" | wc -l) files"
