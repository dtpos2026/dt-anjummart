"""Cuts the watch and jewellery photos out of their white backgrounds (transparent PNG, trimmed, edge colours cleaned).

Usage: python3 make_cutouts.py <photos_dir> <out_dir>

Name each photo with the product code (M1.jpg ... M10, W1 ... W5, J1, J2; see fetch_store_photos.py) or with the store handle.
The result is <code>.png in <out_dir>. Uses the BiRefNet model through rembg (downloaded once, about 1 GB) and pymatting to
remove the white fringe on soft edges. Each photo runs in its own process so the model never exhausts memory.
Needs:  pip install rembg onnxruntime pillow pymatting numpy
"""
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'content'))
from catalog import HANDLES, PRODUCTS  # noqa: E402


def key(s):
    return re.sub(r'[^a-z0-9]', '', s.lower())


def code_for(stem):
    k = key(stem)
    for code in HANDLES:
        if k == key(code):
            return code
    for code, h in HANDLES.items():
        if k and (k == key(h) or key(h).startswith(k) or k.startswith(key(h)[:40])):
            return code
    return None


def one(src, dst):
    import numpy as np
    from PIL import Image
    from rembg import new_session, remove
    from pymatting import estimate_foreground_ml
    session = new_session('birefnet-general')
    im = Image.open(src).convert('RGB')
    mask = remove(im, session=session, only_mask=True)
    a = np.asarray(mask, dtype=np.float32) / 255.0
    a[a < 0.03] = 0.0
    a[a > 0.97] = 1.0
    fg = estimate_foreground_ml(np.asarray(im, dtype=np.float64) / 255.0, a.astype(np.float64))
    rgba = np.dstack([np.clip(fg, 0, 1), a]).astype(np.float32)
    out = Image.fromarray((rgba * 255 + 0.5).astype(np.uint8), 'RGBA')
    box = out.getchannel('A').point(lambda v: 255 if v > 24 else 0).getbbox()
    if box:
        m = 8
        out = out.crop((max(0, box[0] - m), max(0, box[1] - m), min(out.width, box[2] + m), min(out.height, box[3] + m)))
    if max(out.size) > 1600:
        r = 1600 / max(out.size)
        out = out.resize((int(out.width * r), int(out.height * r)), Image.LANCZOS)
    out.save(dst)
    print('ok', dst, out.size)


def main():
    if sys.argv[1] == '--one':
        return one(sys.argv[2], sys.argv[3])
    photos, out = [os.path.abspath(a) for a in sys.argv[1:3]]
    os.makedirs(out, exist_ok=True)
    done, skipped = set(), []
    for name in sorted(os.listdir(photos)):
        stem, ext = os.path.splitext(name)
        if ext.lower() not in ('.jpg', '.jpeg', '.png', '.webp'):
            continue
        code = code_for(stem)
        if not code:
            skipped.append(name)
            continue
        dst = os.path.join(out, code + '.png')
        if not os.path.exists(dst):
            subprocess.run([sys.executable, os.path.abspath(__file__), '--one', os.path.join(photos, name), dst], check=True)
        done.add(code)
    if skipped:
        print('NOT MATCHED (rename to the product code):', ', '.join(skipped))
    missing = sorted(set(HANDLES) - done)
    if missing:
        print('MISSING cut-outs:', ', '.join(missing))
        sys.exit(1)
    print('all', len(done), 'cut-outs written to', out)


main()
