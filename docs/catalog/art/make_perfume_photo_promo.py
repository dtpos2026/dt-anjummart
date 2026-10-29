"""Adds the home "Perfumes" banner scenes (promo-perfumes, promo-perfumes-mobile) to scenes.json.

The scenes show the owner's three real perfume photos (perfume-photos/*-portrait.jpg, 3:4) as framed prints in a slight
fan: Lady Aura, Oud Aura (centre, a little larger) and Tea Rose. Render with art-render.mjs. On phones the section
stacks (text first, then promo-perfumes-mobile.jpg), see assets/home.css.
"""
import json
import os

PHOTOS = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'perfume-photos') + '/'


def cards(cx, cy, w, overlap, tilt=3, z=10):
    h = w * 4 / 3
    step = w - overlap
    out = ''
    for name, x, rot, lift, sc in (('lady', cx - step, -tilt, 0, 1.0), ('tea', cx + step, tilt, 0, 1.0), ('oud', cx, 0, -h * 0.05, 1.1)):
        zi = z if sc == 1.0 else z + 2
        out += (f'<div style="position:absolute;left:{x - w*sc/2}px;top:{cy - h*sc/2 + lift}px;width:{w*sc}px;height:{h*sc}px;z-index:{zi};'
                f'transform:rotate({rot}deg);border:{max(2, w*0.012)}px solid #d4af37;border-radius:3px;'
                f'box-shadow:0 {w*0.07}px {w*0.12}px rgba(0,0,0,.62),0 0 {w*0.12}px rgba(212,175,55,.18);'
                f'background:url(file://{PHOTOS}{name}-portrait.jpg) center/cover"></div>')
    return out


d = json.load(open('scenes.json'))
d['promo-perfumes'] = {'dir': 'promo', 'w': 1800, 'h': 560, 'items': [], 'q': 82,
                       'bg': {'glowX': 0.78, 'glowY': 0.5, 'glowR': 0.5, 'bokeh': 12},
                       'extra': cards(1330, 285, 250, 24)}
d['promo-perfumes-mobile'] = {'dir': 'promo', 'w': 900, 'h': 700, 'items': [], 'q': 82,
                              'bg': {'glowX': 0.5, 'glowY': 0.5, 'glowR': 0.8, 'bokeh': 8},
                              'extra': cards(450, 350, 230, 20)}
json.dump(d, open('scenes.json', 'w'))
print('promo-perfumes scenes written')
