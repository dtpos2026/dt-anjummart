"""Cuts the 12 watch and jewellery photos out of their backgrounds (transparent PNG, trimmed) for the reels and posts.

Usage: python3 make_cutouts.py <photos_dir> <out_dir>

Name each photo with the product code (M1.jpg ... M6, W1 ... W4, J1, J2) or with the product handle from the store (the text in the
product link), any image type. The result is written with the file names the other scripts expect (cut-01.png ... cut-12.png).
Needs:  pip install rembg onnxruntime pillow   (downloads the 176 MB u2net model once from GitHub).
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'content'))
from catalog import PRODUCTS  # noqa: E402
from PIL import Image  # noqa: E402

PHOTOS, OUT = [os.path.abspath(a) for a in sys.argv[1:3]]
os.makedirs(OUT, exist_ok=True)
V2 = json.load(open(os.path.abspath(os.path.join(HERE, '..', '..', 'catalog', 'products-v2.json'))))
HANDLE_TO_FILE = {p['handle']: 'cut-%02d.png' % p['img'] for p in V2}
CODE_TO_FILE = {p[0]: p[3] for p in PRODUCTS if p[1] != 'photo'}


def key(s):
    return re.sub(r'[^a-z0-9]', '', s.lower())


def find_target(stem):
    k = key(stem)
    for code, f in CODE_TO_FILE.items():
        if k == key(code):
            return f
    for h, f in HANDLE_TO_FILE.items():
        if k and (k == key(h) or key(h).startswith(k) or k.startswith(key(h)[:40])):
            return f
    return None


def main():
    from rembg import new_session, remove
    session = new_session('u2net')
    done, skipped = set(), []
    for name in sorted(os.listdir(PHOTOS)):
        stem, ext = os.path.splitext(name)
        if ext.lower() not in ('.jpg', '.jpeg', '.png', '.webp'):
            continue
        target = find_target(stem)
        if not target:
            skipped.append(name)
            continue
        im = Image.open(os.path.join(PHOTOS, name)).convert('RGB')
        cut = remove(im, session=session, alpha_matting=False)
        box = cut.getchannel('A').point(lambda v: 255 if v > 24 else 0).getbbox()
        if box:
            m = 6
            cut = cut.crop((max(0, box[0] - m), max(0, box[1] - m), min(cut.width, box[2] + m), min(cut.height, box[3] + m)))
        # keep the file a sensible size for 1080-px video frames
        if max(cut.size) > 1600:
            r = 1600 / max(cut.size)
            cut = cut.resize((int(cut.width * r), int(cut.height * r)), Image.LANCZOS)
        cut.save(os.path.join(OUT, target))
        done.add(target)
        print(name, '->', target, cut.size)
    missing = sorted(set(CODE_TO_FILE.values()) - done)
    if skipped:
        print('NOT MATCHED (rename to the product code):', ', '.join(skipped))
    if missing:
        print('MISSING cut-outs:', ', '.join(missing))
        sys.exit(1)
    print('all 12 cut-outs written to', OUT)


main()
