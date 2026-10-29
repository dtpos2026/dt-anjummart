import json

def bottle(cx, base, s, kind, z=10):
    """A drawn perfume bottle (frosted glass, black ribbed cap, gold label) in the style of the supplied
    Anjum packaging. cx = centre x, base = y of the bottom edge, s = scale (1 = 130 px wide body)."""
    W, H, CAP_W, CAP_H, NECK = 104 * s, 188 * s, 64 * s, 44 * s, 5 * s
    col = {'red':  ('#e0434a', '#b3212b', '#7e1119', '#f6d68c'),
           'deep': ('#c7343c', '#9d1e2a', '#6a0f19', '#f6d68c'),
           'white':('#ffffff', '#ece9e2', '#c9c5bb', '#c9a24b')}[kind[0]]
    name, sub = kind[1], 'by ANJUM'
    top = base - H - NECK - CAP_H
    return f'''<div style="position:absolute;left:{cx - W/2}px;top:{top}px;width:{W}px;height:{H + NECK + CAP_H}px;z-index:{z};filter:drop-shadow(0 {10*s}px {16*s}px rgba(0,0,0,.6))">
  <i style="position:absolute;left:50%;bottom:{-14*s}px;width:{W*1.5}px;height:{22*s}px;transform:translateX(-50%);border-radius:50%;background:radial-gradient(ellipse,rgba(0,0,0,.7),transparent 70%);filter:none;z-index:-1"></i>
  <div style="position:absolute;left:{(W-CAP_W)/2}px;top:0;width:{CAP_W}px;height:{CAP_H}px;border-radius:{4*s}px {4*s}px {2*s}px {2*s};background:
      linear-gradient(90deg,rgba(255,255,255,.22),rgba(255,255,255,0) 22%,rgba(0,0,0,.35) 100%),
      repeating-linear-gradient(90deg,#1a1a1a 0 {3*s}px,#0b0b0b {3*s}px {6*s}px)"></div>
  <div style="position:absolute;left:{(W-CAP_W)/2+6*s}px;top:{CAP_H}px;width:{CAP_W-12*s}px;height:{NECK}px;background:linear-gradient(#222,#050505)"></div>
  <div style="position:absolute;left:0;top:{CAP_H+NECK}px;width:{W}px;height:{H}px;border-radius:{10*s}px {10*s}px {7*s}px {7*s};overflow:hidden;background:
      linear-gradient(100deg,rgba(255,255,255,.34) 0,rgba(255,255,255,.04) 18%,rgba(255,255,255,0) 60%,rgba(0,0,0,.28) 100%),
      linear-gradient(180deg,{col[0]} 0%,{col[1]} 55%,{col[2]} 100%)">
    <div style="position:absolute;left:0;right:0;bottom:0;height:{34*s}px;background:linear-gradient(to top,rgba(255,255,255,.28),rgba(255,255,255,0))"></div>
    <div style="position:absolute;left:{9*s}px;top:{6*s}px;width:{9*s}px;bottom:{10*s}px;border-radius:{6*s}px;background:linear-gradient(rgba(255,255,255,.5),rgba(255,255,255,.05))"></div>
    <div style="position:absolute;left:0;right:0;top:{H*0.40}px;text-align:center;font-family:Cormorant,serif;font-weight:500;color:{col[3]};letter-spacing:{1.1*s}px;font-size:{13.5*s}px;line-height:1.05">{name}</div>
    <div style="position:absolute;left:0;right:0;top:{H*0.40+17*s}px;text-align:center;font-family:Cormorant,serif;font-style:italic;color:{col[3]};opacity:.9;font-size:{9.5*s}px">{sub}</div>
  </div>
</div>'''

def trio(cx, base, s):
    return (bottle(cx - 122 * s, base, s, ('red', 'LADY AURA'), 10)
            + bottle(cx + 122 * s, base, s, ('deep', 'TEA ROSE'), 10)
            + bottle(cx, base + 10 * s, s * 1.08, ('white', 'OUD AURA'), 12))

d = json.load(open('scenes.backup.json'))
# desktop 1800x760: watches smaller on the left of the product area, jewellery right, perfumes in front
s = d['slide-brand-desktop']
s['items'] = [
    {'cut': 3, 'x': 885, 'y': 335, 'h': 500, 'rot': -9, 'z': 1},
    {'cut': 8, 'x': 1040, 'y': 350, 'h': 480, 'rot': 6, 'z': 2},
    {'cut': 11, 'x': 1640, 'y': 330, 'h': 350, 'rot': 0, 'z': 3, 'ar': 1.0, 'noGround': True},
]
s['extra'] = trio(1325, 650, 1.32)
# mobile 900x1100 (text on top 40%)
m = d['slide-brand-mobile']
m['items'] = [
    {'cut': 3, 'x': 150, 'y': 740, 'h': 420, 'rot': -9, 'z': 1},
    {'cut': 8, 'x': 290, 'y': 750, 'h': 400, 'rot': 6, 'z': 2},
    {'cut': 11, 'x': 745, 'y': 735, 'h': 290, 'rot': 0, 'z': 3, 'ar': 1.0, 'noGround': True},
]
m['extra'] = trio(520, 990, 1.0)
json.dump(d, open('scenes.json', 'w'))
print('scenes updated')

# ---- promo banner for the home page "Perfumes" section (text sits on the left)
d = json.load(open('scenes.json'))
d['promo-perfumes'] = {'dir': 'promo', 'w': 1800, 'h': 560, 'items': [], 'bg': {'glowX': 0.78, 'glowY': 0.5, 'glowR': 0.5, 'bokeh': 12}, 'q': 82,
                       'extra': trio(1330, 480, 1.55)}
d['promo-perfumes-mobile'] = {'dir': 'promo', 'w': 900, 'h': 700, 'items': [], 'bg': {'glowX': 0.6, 'glowY': 0.55, 'glowR': 0.8, 'bokeh': 8}, 'q': 82,
                              'extra': trio(738, 640, 0.76)}
json.dump(d, open('scenes.json', 'w'))
print('promo scenes added')
