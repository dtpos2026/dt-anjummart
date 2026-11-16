"""White studio pictures for the store (first gallery image of each watch and jewellery product).

Usage: python3 make_store_images.py <cutouts_dir> <out_dir>
1600 x 1600, white, the piece centred with a soft contact shadow and the Anjum Mart logo as a small watermark (bottom right), JPEG q88.
Colour backgrounds are for social posts only; the store keeps the clean white marketplace look.
File name: <product handle>-01-white-studio.jpg  (the second image of each product is the info card, INFO-<code>-1600.jpg).
"""
import os
import sys

from PIL import Image, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from catalog import HANDLES, BY  # noqa: E402

CUTS, OUT = [os.path.abspath(a) for a in sys.argv[1:3]]
LOGO = os.path.abspath(os.path.join(HERE, '..', '..', 'brand', 'editable', 'anjum-mart-logo-for-light-background.png'))
os.makedirs(OUT, exist_ok=True)
S = 1600


def studio(code, handle):
    piece = Image.open(os.path.join(CUTS, code + '.png')).convert('RGBA')
    kind = BY[code][1]
    max_h = S * (0.88 if kind == 'watch' else 0.80)
    max_w = S * (0.62 if kind == 'watch' else 0.88)
    r = min(max_h / piece.height, max_w / piece.width)
    piece = piece.resize((int(piece.width * r), int(piece.height * r)), Image.LANCZOS)
    cv = Image.new('RGBA', (S, S), (255, 255, 255, 255))
    x = (S - piece.width) // 2
    y = int((S - piece.height) / 2 - S * 0.015)
    # soft contact shadow under the piece
    sh = Image.new('RGBA', (S, S), (0, 0, 0, 0))
    ell = Image.new('L', (S, S), 0)
    from PIL import ImageDraw
    d = ImageDraw.Draw(ell)
    cx, cy = S // 2, y + piece.height + 10
    d.ellipse((cx - piece.width * 0.38, cy - 16, cx + piece.width * 0.38, cy + 16), fill=70)
    ell = ell.filter(ImageFilter.GaussianBlur(20))
    sh.putalpha(ell)
    cv.alpha_composite(sh)
    cv.alpha_composite(piece, (x, y))
    logo = Image.open(LOGO).convert('RGBA')
    lw = int(S * 0.20)
    logo = logo.resize((lw, int(logo.height * lw / logo.width)), Image.LANCZOS)
    a = logo.getchannel('A').point(lambda v: int(v * 0.55))
    logo.putalpha(a)
    cv.alpha_composite(logo, (S - lw - int(S * 0.035), S - logo.height - int(S * 0.035)))
    cv.convert('RGB').save(os.path.join(OUT, f'{handle}-01-white-studio.jpg'), quality=88, optimize=True)


for code, handle in HANDLES.items():
    studio(code, handle)
    print(code, handle[:50])
print('store images written to', OUT)
