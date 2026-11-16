"""Launch kit for an empty page: the first six posts (two full grid rows), the profile set and a grid mock-up.

Usage: python3 make_launch_kit.py <posts_final_dir> <posters_dir> <reels_dir> <out_dir>
Writes <out_dir>/Launch-Kit/ (the six posts, captions, profile and cover pictures, highlight covers) and
<out_dir>/launch-grid.html + jobs.json for the grid mock-up (render with ../ads/render.mjs <out_dir>).
Order of posting, oldest to newest: brand intro, hero 1, hero 2 in a contrasting colour, guide carousel, hero 3, the brand reel.
"""
import json
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from copytext import caption, first_comment, WA  # noqa: E402

POSTS, POSTERS, REELS, OUT = [os.path.abspath(a) for a in sys.argv[1:5]]
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
FONTS = os.path.abspath(os.path.join(HERE, '..', 'fonts'))
KIT = os.path.join(OUT, 'Launch-Kit')
shutil.rmtree(KIT, ignore_errors=True)
os.makedirs(KIT + '/1-First-6-posts')

# (order, kind, asset, copy key, file(s), thumbnail for the grid)
SIX = [
    (1, 'Feed picture', 'I-MEET', 'MEET', [f'{POSTS}/Info/I-MEET-feed-1080x1350.jpg'], f'{POSTS}/Info/I-MEET-feed-1080x1350.jpg'),
    (2, 'Feed picture', 'K-M1', 'K-M1', [f'{POSTS}/Color-Series/K-M1-feed-1080x1350.jpg'], f'{POSTS}/Color-Series/K-M1-feed-1080x1350.jpg'),
    (3, 'Feed picture (contrasting colour)', 'K-W2', 'K-W2', [f'{POSTS}/Color-Series/K-W2-feed-1080x1350.jpg'], f'{POSTS}/Color-Series/K-W2-feed-1080x1350.jpg'),
    (4, 'Guide carousel', 'G-MEN', 'GMEN', sorted(os.path.join(POSTS, 'Carousels', 'G-MEN', f) for f in os.listdir(os.path.join(POSTS, 'Carousels', 'G-MEN'))), f'{POSTS}/Carousels/G-MEN/G-MEN-slide-01.jpg'),
    (5, 'Feed picture', 'K-J2', 'K-J2', [f'{POSTS}/Color-Series/K-J2-feed-1080x1350.jpg'], f'{POSTS}/Color-Series/K-J2-feed-1080x1350.jpg'),
    (6, 'Reel (set the cover to the picture shown)', 'R-ALL', 'ALL', [f'{REELS}/R-ALL.mp4'], f'{POSTERS}/R-ALL.jpg'),
]
cap = ''
for n, kind, asset, key, files, thumb in SIX:
    d = os.path.join(KIT, '1-First-6-posts', f'{n}-{asset}')
    os.makedirs(d)
    for f in files:
        shutil.copy2(f, d)
    if asset.startswith('R-'):
        shutil.copy2(thumb, os.path.join(d, asset + '-cover.jpg'))
    cap += f"==== Post {n} of 6 · {kind} · {asset} ====\n[Instagram]\n{caption(key, 'ig')}\n\n[First comment]\n{first_comment(key)}\n\n[Facebook]\n{caption(key, 'fb')}\n\n[TikTok]\n{caption(key, 'tt')}\n\n"
open(os.path.join(KIT, '1-First-6-posts', 'captions-first-6.txt'), 'w').write(
    'ANJUM MART LAUNCH KIT: THE FIRST SIX POSTS\nPost them 20 to 30 minutes apart, oldest first (1 to 6), with Share to Facebook on.\n\n' + cap)

prof = os.path.join(KIT, '2-Profile-pictures')
os.makedirs(prof)
for src in ('docs/brand/anjum-mart-profile-light-1080.png', 'docs/brand/anjum-mart-profile-dark-1080.png', 'docs/social/anjum-mart-facebook-cover-1640x624.png'):
    shutil.copy2(os.path.join(ROOT, src), prof)
hl = os.path.join(KIT, '3-Highlight-covers')
os.makedirs(hl)
for f in sorted(os.listdir(os.path.join(ROOT, 'docs', 'social'))):
    if f.startswith('instagram-highlight') and f.endswith('.png'):
        shutil.copy2(os.path.join(ROOT, 'docs', 'social', f), hl)

# grid mock-up: newest first, three columns, 3:4 tiles
tiles = ''.join(f'<div class="t"><img src="file://{t[5]}"></div>' for t in sorted(SIX, key=lambda s: -s[0]))
profile_pic = os.path.join(ROOT, 'docs', 'brand', 'anjum-mart-profile-light-1080.png')
html = f'''<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:Jost;font-weight:400;src:url(file://{FONTS}/jost-latin-400-normal.woff2)}}
@font-face{{font-family:Jost;font-weight:600;src:url(file://{FONTS}/jost-latin-600-normal.woff2)}}
*{{box-sizing:border-box}}body{{margin:0;width:1080px;height:1500px;background:#fff;font-family:Jost,sans-serif;color:#171717}}
.top{{padding:50px 48px 26px;display:flex;gap:40px;align-items:center}}
.top img{{width:210px;height:210px;border-radius:50%;border:2px solid #d4af37}}
.stats{{display:flex;gap:56px;font-size:30px;text-align:center}}.stats b{{display:block;font-size:40px}}
.bio{{padding:0 48px 24px;font-size:30px;line-height:1.35}}.bio b{{font-size:34px}}
.btns{{display:flex;gap:14px;padding:0 48px 28px}}.btns div{{flex:1;background:#efefef;border-radius:14px;text-align:center;padding:18px 0;font-weight:600;font-size:28px}}
.grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:4px;border-top:1px solid #ddd}}
.t{{aspect-ratio:3/4;overflow:hidden;background:#eee}}.t img{{width:100%;height:100%;object-fit:cover}}
</style></head><body>
<div class="top"><img src="file://{profile_pic}"><div class="stats"><div><b>6</b>posts</div><div><b>0</b>followers</div><div><b>0</b>following</div></div></div>
<div class="bio"><b>Anjum Mart | Watches &amp; Jewellery</b><br>Watches · Jewellery · Perfumes<br>Free delivery all Pakistan 🇵🇰 · Cash on Delivery<br>Order on WhatsApp 👇 anjummart.com</div>
<div class="btns"><div>Message</div><div>WhatsApp</div><div>Email</div></div>
<div class="grid">{tiles}</div>
<script>document.fonts.ready.then(()=>setTimeout(()=>document.body.setAttribute('data-ready','1'),400))</script></body></html>'''
os.makedirs(OUT, exist_ok=True)
hp = os.path.join(OUT, 'launch-grid.html')
open(hp, 'w').write(html)
json.dump([dict(html=hp, out=os.path.join(KIT, 'Grid-preview-first-6-posts.jpg'), w=1080, h=1500)], open(os.path.join(OUT, 'jobs.json'), 'w'))
print('launch kit written to', KIT)
