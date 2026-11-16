"""Builds the post pictures: a feed picture (4:5) and a story picture (9:16) for every product, the four collection carousels
(cover, one slide per piece, closing slide), the info posts (how to order, free delivery, wedding season, FAQ, gift ideas, brand)
and a thumbnail (first frame look) used by the calendar PDF.

Usage: python3 make_posts.py <cutouts_dir> <perfume_photos_dir> <out_dir>
Writes HTML pages + jobs.json under <out_dir>; render with ../ads/render.mjs <out_dir> (PLAYWRIGHT_FROM=/opt/node22/lib/node_modules/).
"""
import html
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from catalog import PRODUCTS, BY  # noqa: E402
from copytext import INFO, PRODUCTS as COPY  # noqa: E402
import post_styles as ps  # noqa: E402

CUT, PERF, OUT = [os.path.abspath(a) for a in sys.argv[1:4]]
FONTS = os.path.abspath(os.path.join(HERE, '..', 'fonts'))
LOGO = os.path.abspath(os.path.join(HERE, '..', '..', 'brand', 'editable', 'anjum-mart-logo-for-dark-background.svg'))

FEED = (1080, 1350)
STORY = (1080, 1920)
ps.setup(CUT, PERF)

WA_ICON = ('<svg viewBox="0 0 32 32" fill="#111"><path d="M16.04 3C9.4 3 4 8.38 4 15.02c0 2.12.55 4.2 1.6 6.03L4 29l8.14-1.56a12.02 12.02 0 0 0 3.9.65C22.68 28.09 28 22.7 28 16.07 28 9.4 22.7 3 16.04 3zm0 22.1c-1.2 0-2.38-.3-3.42-.87l-.5-.27-4.83.93.96-4.7-.3-.52a9.1 9.1 0 0 1-1.4-4.84c0-5.03 4.1-9.1 9.15-9.1 5.02 0 9.1 4.07 9.1 9.1 0 5.04-4.08 9.27-8.76 9.27zm5.1-6.9c-.28-.14-1.65-.82-1.9-.9-.26-.1-.44-.14-.63.14-.19.28-.72.9-.88 1.1-.16.18-.32.2-.6.07-.28-.14-1.18-.44-2.25-1.4-.83-.74-1.4-1.66-1.56-1.94-.16-.28-.02-.43.12-.57.13-.12.28-.32.42-.48.14-.16.19-.28.28-.47.1-.19.05-.35-.02-.5-.07-.14-.63-1.5-.86-2.06-.23-.54-.46-.47-.63-.48h-.54c-.19 0-.5.07-.76.35-.26.28-1 .97-1 2.38s1.03 2.76 1.17 2.95c.14.19 2.02 3.08 4.9 4.32.68.3 1.22.47 1.63.6.69.22 1.31.19 1.8.11.55-.08 1.65-.67 1.88-1.32.23-.65.23-1.2.16-1.32-.07-.12-.26-.19-.54-.33z"/></svg>')

CSS = '''
@font-face{font-family:Cormorant;font-weight:600;src:url(file://FONTS/cormorant-latin-600-normal.woff2)}
@font-face{font-family:Jost;font-weight:400;src:url(file://FONTS/jost-latin-400-normal.woff2)}
@font-face{font-family:Jost;font-weight:500;src:url(file://FONTS/jost-latin-500-normal.woff2)}
@font-face{font-family:Jost;font-weight:600;src:url(file://FONTS/jost-latin-600-normal.woff2)}
*{box-sizing:border-box}html,body{margin:0;padding:0}
body{width:WPXpx;height:HPXpx;position:relative;overflow:hidden;color:#fff;font-family:Jost,sans-serif;
background:radial-gradient(ellipse 78% 50% at 50% 50%,#4d3910 0%,#1f170a 46%,#090909 80%)}
.bk{position:absolute;border-radius:50%;background:radial-gradient(circle,rgba(236,208,128,.55),rgba(236,208,128,0) 68%)}
.frame{position:absolute;inset:22px;border:1.5px solid rgba(212,175,55,.6)}
.logo{position:absolute;left:50%;transform:translateX(-50%);height:84px}
.t{position:absolute;left:70px;right:70px;text-align:center;white-space:nowrap}
.eyebrow{font:500 26px/1 Jost;letter-spacing:7px;color:#e6c875}
.title{font:600 76px/1.05 Cormorant,serif;letter-spacing:1px}
.sub{font:400 30px/1.2 Jost;color:#e0e0e0;letter-spacing:.6px}
.zone{position:absolute;left:0;right:0}
.glow{position:absolute;left:50%;top:50%;width:920px;height:920px;transform:translate(-50%,-50%);background:radial-gradient(circle,rgba(212,175,55,.28),rgba(212,175,55,0) 62%)}
.floor{position:absolute;left:50%;bottom:-8px;width:760px;height:60px;transform:translateX(-50%);background:radial-gradient(ellipse,rgba(0,0,0,.75),rgba(0,0,0,0) 70%)}
.prod{position:absolute;width:auto;filter:drop-shadow(0 22px 28px rgba(0,0,0,.65))}
.card{position:absolute;background-size:cover;background-position:center;border:5px solid #d4af37;border-radius:3px;box-shadow:0 26px 40px rgba(0,0,0,.62),0 0 46px rgba(212,175,55,.2)}
.price{font:600 98px/1 Cormorant,serif;color:#f1d98a;letter-spacing:1px}
.line{font:500 27px/1 Jost;color:#f1f1f1;letter-spacing:1px}
.cta{position:absolute;left:50%;transform:translateX(-50%);height:80px;padding:0 44px;border-radius:40px;background:#d4af37;color:#111;display:flex;align-items:center;gap:16px;font:600 30px/1 Jost;letter-spacing:2.5px;white-space:nowrap;box-shadow:0 10px 26px rgba(0,0,0,.5)}
.cta svg{width:42px;height:42px}
.num{position:absolute;font:500 26px/1 Jost;letter-spacing:5px;color:#e6c875}
.swipe{position:absolute;right:70px;font:500 26px/1 Jost;letter-spacing:5px;color:#e6c875}
.rule{position:absolute;height:2px;background:linear-gradient(90deg,transparent,#d4af37,transparent)}
.step{position:absolute;left:90px;right:90px;display:flex;gap:30px;align-items:flex-start}
.step b{font:600 84px/0.9 Cormorant,serif;color:#d4af37;min-width:70px}
.step span{font:400 38px/1.3 Jost;color:#f0f0f0}
'''
SCRIPT = '''<script>
function fit(){document.querySelectorAll('.fit').forEach(function(e){var fs=parseFloat(getComputedStyle(e).fontSize);while(e.scrollWidth>e.clientWidth&&fs>30){fs-=2;e.style.fontSize=fs+'px'}})}
document.fonts.ready.then(function(){fit();document.body.setAttribute('data-ready','1')});
</script>'''


def head(w, h):
    css = CSS.replace('FONTS', FONTS).replace('WPX', str(w)).replace('HPX', str(h))
    return f'<!doctype html><html><head><meta charset="utf-8"><style>{css}</style></head><body>'


def bokeh(w, h, z0, zh):
    pos = [(90, z0 + 60, 70), (w - 170, z0 + 160, 48), (w - 250, z0 + zh - 140, 90), (150, z0 + zh - 220, 44)]
    return ''.join(f'<div class="bk" style="left:{x}px;top:{y}px;width:{s}px;height:{s}px"></div>' for x, y, s in pos)


def img_for(p):
    kind, f = p[1], p[3]
    return ('file://' + os.path.join(PERF if kind == 'photo' else CUT, f))


def product_visual(items, w, zh, sf):
    """items: list of (catalog row, dx, dy, height_at_feed, rotation, z). Photos are drawn as framed cards."""
    out = ''
    for row, dx, dy, h, rot, z in items:
        if row[1] == 'photo':
            ch = h * sf * 0.92
            cw = ch * 3 / 4
            out += (f'<div class="card" style="left:calc(50% + {dx * sf}px);top:calc(50% + {dy * sf}px);width:{cw}px;height:{ch}px;'
                    f'transform:translate(-50%,-50%) rotate({rot}deg);z-index:{z};background-image:url({img_for(row)})"></div>')
        else:
            out += (f'<img class="prod" src="{img_for(row)}" style="left:calc(50% + {dx * sf}px);top:calc(50% + {dy * sf}px);'
                    f'height:{h * sf}px;transform:translate(-50%,-50%) rotate({rot}deg);z-index:{z}">')
    return out


LAYOUT = {
    'feed': dict(size=FEED, logo=44, eyebrow=142, title=176, sub=266, zone=(335, 1065), price=1086, line=1196, cta=1246),
    'story': dict(size=STORY, logo=272, eyebrow=374, title=410, sub=500, zone=(595, 1295), price=1322, line=1432, cta=1492),
}


def single(fmt, eyebrow, title, sub, price, items, extra_line=None):
    L = LAYOUT[fmt]
    w, h = L['size']
    z0, z1 = L['zone']
    zh = z1 - z0
    sf = zh / 730.0
    body = head(w, h)
    body += bokeh(w, h, z0, zh)
    body += '<div class="frame"></div>'
    body += f'<img class="logo" style="top:{L["logo"]}px" src="file://{LOGO}">'
    body += f'<div class="t eyebrow" style="top:{L["eyebrow"]}px">{html.escape(eyebrow)}</div>'
    body += f'<div class="t title fit" style="top:{L["title"]}px">{html.escape(title)}</div>'
    body += f'<div class="t sub fit" style="top:{L["sub"]}px">{html.escape(sub)}</div>'
    body += f'<div class="zone" style="top:{z0}px;height:{zh}px"><div class="glow"></div><div class="floor"></div>{product_visual(items, w, zh, sf)}</div>'
    body += f'<div class="t price" style="top:{L["price"]}px">{html.escape(price)}</div>'
    body += f'<div class="t line" style="top:{L["line"]}px">{html.escape(extra_line or "Free Delivery All Pakistan  ·  Cash on Delivery")}</div>'
    body += f'<div class="cta" style="top:{L["cta"]}px">{WA_ICON}ORDER ON WHATSAPP</div>'
    body += SCRIPT + '</body></html>'
    return body


def slide(idx, total, eyebrow, title, sub, price, items):
    """Carousel slide (4:5) with a counter and a swipe hint."""
    w, h = FEED
    z0, z1 = 335, 1065
    zh = z1 - z0
    sf = zh / 730.0
    body = head(w, h) + bokeh(w, h, z0, zh) + '<div class="frame"></div>'
    body += f'<img class="logo" style="top:44px" src="file://{LOGO}">'
    body += f'<div class="num" style="left:70px;top:96px">{idx:02d} / {total:02d}</div>'
    if idx < total:
        body += '<div class="swipe" style="top:96px">SWIPE &rarr;</div>'
    body += f'<div class="t eyebrow" style="top:142px">{html.escape(eyebrow)}</div>'
    body += f'<div class="t title fit" style="top:176px">{html.escape(title)}</div>'
    body += f'<div class="t sub fit" style="top:266px">{html.escape(sub)}</div>'
    body += f'<div class="zone" style="top:{z0}px;height:{zh}px"><div class="glow"></div><div class="floor"></div>{product_visual(items, w, zh, sf)}</div>'
    body += f'<div class="t price" style="top:1086px">{html.escape(price)}</div>'
    body += '<div class="t line" style="top:1196px">Free Delivery All Pakistan  ·  Cash on Delivery</div>'
    body += f'<div class="cta" style="top:1246px">{WA_ICON}ORDER ON WHATSAPP</div>'
    return body + SCRIPT + '</body></html>'


def cover(eyebrow, title, sub, items, total):
    w, h = FEED
    z0, z1 = 360, 1180
    zh = z1 - z0
    sf = zh / 730.0
    body = head(w, h) + bokeh(w, h, z0, zh) + '<div class="frame"></div>'
    body += f'<img class="logo" style="top:44px" src="file://{LOGO}">'
    body += f'<div class="t eyebrow" style="top:150px">{html.escape(eyebrow)}</div>'
    body += f'<div class="t title fit" style="top:192px;font-size:92px">{html.escape(title)}</div>'
    body += f'<div class="t sub fit" style="top:296px">{html.escape(sub)}</div>'
    body += f'<div class="zone" style="top:{z0}px;height:{zh}px"><div class="glow"></div><div class="floor"></div>{product_visual(items, w, zh, sf)}</div>'
    body += f'<div class="swipe" style="top:1262px;left:0;right:0;text-align:center">SWIPE TO SEE ALL {total} &rarr;</div>'
    return body + SCRIPT + '</body></html>'


def closing(title, lines):
    w, h = FEED
    body = head(w, h) + '<div class="frame"></div>'
    body += f'<img class="logo" style="top:150px;height:230px" src="file://{LOGO}">'
    body += f'<div class="t title fit" style="top:470px">{html.escape(title)}</div>'
    body += '<div class="rule" style="left:360px;width:360px;top:570px"></div>'
    for i, ln in enumerate(lines):
        body += f'<div class="t sub fit" style="top:{620 + i * 62}px;font-size:36px">{html.escape(ln)}</div>'
    body += '<div class="t eyebrow" style="top:880px;font-size:34px;letter-spacing:6px;color:#f1d98a">ANJUMMART.COM</div>'
    body += f'<div class="cta" style="top:970px">{WA_ICON}ORDER ON WHATSAPP</div>'
    body += '<div class="t line" style="top:1110px">Free Delivery All Pakistan  ·  Cash on Delivery</div>'
    return body + SCRIPT + '</body></html>'


def info(fmt, title, lines, footer_items=None):
    """Text post: big title, up to three numbered lines, optional pieces under the text."""
    L = LAYOUT[fmt]
    w, h = L['size']
    story = fmt == 'story'
    top = 330 if not story else 520
    gap = (170 if footer_items else 240) if not story else (200 if footer_items else 290)
    fs = 40 if not story else 46
    body = head(w, h) + '<div class="frame"></div>'
    body += f'<img class="logo" style="top:{44 if not story else 272}px" src="file://{LOGO}">'
    body += f'<div class="t title fit" style="top:{top - 130}px;font-size:80px">{html.escape(title)}</div>'
    body += f'<div class="rule" style="left:360px;width:360px;top:{top - 22}px"></div>'
    y = top + 30
    for i, ln in enumerate(lines):
        n = ln.split('. ', 1)
        txt = n[1] if len(n) == 2 and n[0].isdigit() else ln
        label = n[0] if len(n) == 2 and n[0].isdigit() else str(i + 1)
        body += f'<div class="step" style="top:{y}px"><b>{label}</b><span style="font-size:{fs}px">{html.escape(txt)}</span></div>'
        y += gap
    cta_top = 1246 if not story else 1492
    if footer_items:
        z0 = y + 10
        zh = max(cta_top - 30 - z0, 220)
        body += f'<div class="zone" style="top:{z0}px;height:{zh}px">{product_visual(footer_items, w, zh, zh / 560.0)}</div>'
    else:
        body += f'<div class="t eyebrow" style="top:{cta_top - 90}px;font-size:30px;letter-spacing:4px;color:#f1d98a">WHATSAPP +92 371 4661514  ·  ANJUMMART.COM</div>'
    body += f'<div class="cta" style="top:{cta_top}px">{WA_ICON}ORDER ON WHATSAPP</div>'
    return body + SCRIPT + '</body></html>'


def main():
    jobs = []

    def add(name, folder, size, htm):
        d = os.path.join(OUT, 'html', folder)
        os.makedirs(d, exist_ok=True)
        hp = os.path.join(d, name + '.html')
        open(hp, 'w').write(htm)
        jobs.append(dict(html=hp, out=os.path.join(OUT, 'final', folder, name + '.jpg'), w=size[0], h=size[1]))

    # per-product feed + story
    for p in PRODUCTS:
        pid = p[0]
        main_item = [(p, 0, 0, 700 if p[1] != 'photo' else 700, 0, 1)]
        if p[1] == 'jewellery':
            main_item = [(p, 0, 0, 700, 0, 1)]
        add(f'F-{pid}-feed-1080x1350', 'Feed-4x5', FEED, single('feed', p[4], p[5], p[6], p[7], main_item))
        add(f'S-{pid}-story-1080x1920', 'Story-9x16', STORY, single('story', p[4], p[5], p[6], p[7], main_item))

    def row(i):
        return BY[i]

    # carousels
    carousels = {
        'C-MEN': ("MEN'S WATCHES · RUSTET", "The Men's Collection", 'Gold · Silver · Black · Blue · Green', ['M1', 'M2', 'M3', 'M4', 'M5', 'M6', 'M7', 'M8', 'M9', 'M10'], [('M1', -170, 10, 640, -8, 1), ('M2', 170, 10, 640, 8, 1), ('M3', 0, -10, 700, 0, 2)]),
        'C-WOMEN': ('LADIES WATCHES · MOONSTON · RUSTET', 'The Ladies Collection', 'Black · Pink · Emerald · Gold', ['W1', 'W2', 'W3', 'W4', 'W5'], [('W2', -190, 10, 640, -8, 1), ('W4', 190, 10, 640, 8, 1), ('W1', 0, -10, 700, 0, 2)]),
        'C-JEWELLERY': ('BRIDAL JEWELLERY SETS', 'Bridal Jewellery', 'Necklace · Earrings · Maang Tikka', ['J1', 'J2'], [('J1', -150, 40, 540, 0, 1), ('J2', 170, 0, 660, 0, 2)]),
        'C-PERFUMES': ('EAU DE PARFUM · 50 ML', 'Anjum Perfumes', 'Lady Aura · Oud Aura · Tea Rose', ['P1', 'P2', 'P3'], [('P1', -215, 20, 520, -4, 1), ('P3', 215, 20, 520, 4, 1), ('P2', 0, -10, 620, 0, 2)]),
    }
    for cid, (eb, title, sub, ids, cover_items) in carousels.items():
        total = len(ids) + 2
        add(f'{cid}-slide-01', f'Carousels/{cid}', FEED, cover(eb, title, sub, [(row(i), dx, dy, h, rot, z) for i, dx, dy, h, rot, z in cover_items], len(ids)))
        for n, pid in enumerate(ids, start=2):
            r = row(pid)
            add(f'{cid}-slide-{n:02d}', f'Carousels/{cid}', FEED, slide(n, total, r[4], r[5], r[6], r[7], [(r, 0, 0, 700, 0, 1)]))
        add(f'{cid}-slide-{total:02d}', f'Carousels/{cid}', FEED, closing('Order in two minutes', ['Message us on WhatsApp +92 371 4661514', 'Free delivery all over Pakistan', 'Cash on Delivery']))

    # info posts
    pieces = {
        'I-ORDER': [],
        'I-DELIVERY': [],
        'I-WEDDING': [('J2', -230, 20, 460, 0, 1), ('W2', 20, 10, 560, 4, 2), ('P1', 270, 20, 480, 0, 1)],
        'I-FAQ': [],
        'I-GIFTHER': [('W1', -250, 10, 520, 0, 1), ('J2', 10, 20, 430, 0, 1), ('P3', 260, 20, 520, 3, 2)],
        'I-GIFTHIM': [('M1', -170, 10, 560, -6, 1), ('P2', 190, 20, 560, 4, 2)],
        'I-BRAND': [('M1', -280, 10, 480, -6, 1), ('J2', 0, 40, 400, 0, 1), ('P2', 280, 20, 480, 4, 2)],
    }
    keymap = {'I-ORDER': 'ORDER', 'I-DELIVERY': 'DELIVERY', 'I-WEDDING': 'WEDDING', 'I-FAQ': 'FAQ', 'I-GIFTHER': 'GIFTHER', 'I-GIFTHIM': 'GIFTHIM', 'I-BRAND': 'BRAND'}
    for iid, key in keymap.items():
        c = INFO[key]
        fi = [(row(i), dx, dy, h, rot, z) for i, dx, dy, h, rot, z in pieces[iid]] or None
        add(f'{iid}-feed-1080x1350', 'Info', FEED, info('feed', c['title'], c['lines'], fi))
        add(f'{iid}-story-1080x1920', 'Info', STORY, info('story', c['title'], c['lines'], fi))

    # colour series: one colour-world post (feed + story) for every product, same look as the reels
    for p in PRODUCTS:
        pid = p[0]
        add(f'K-{pid}-feed-1080x1350', 'Color-Series', FEED, ps.colour_post('feed', pid))
        add(f'K-{pid}-story-1080x1920', 'Color-Series', STORY, ps.colour_post('story', pid))

    # guide carousels on cream
    guides = {
        'G-MEN': dict(kicker="MEN'S WATCHES · RUSTET", title='Which dial suits you?', sub='Black, blue, green or white', cover=['M1', 'M2', 'M4', 'M6'],
                      slides=[('BLACK', 'Black dial', ['Gold · Roman Numerals', 'All-Black · Day & Date', 'Gold Bezel · Vertical Texture'], ['M1', 'M3', 'M9']),
                              ('BLUE', 'Blue dial', ['Royal Blue · Gold & Silver', 'Royal Blue · Classic Series', 'Ice Blue · Oyster Series'], ['M2', 'M8', 'M7']),
                              ('GREEN', 'Green dial', ['Silver · Roman Numerals', 'Silver · Emerald Sunburst'], ['M4', 'M5']),
                              ('WHITE', 'White dial', ['Two-Tone · Gold & Silver', 'Textured · XII at the Top'], ['M6', 'M10'])],
                      close=('Pick your dial', ['Ten styles · from Rs. 3,990', 'Free delivery all over Pakistan', 'Cash on Delivery'])),
        'G-LADIES': dict(kicker='LADIES WATCHES · MOONSTON · RUSTET', title='Pink, emerald, black or gold?', sub='Crystal-style watches from Rs. 2,499', cover=['W2', 'W4', 'W1', 'W5'],
                         slides=[('PINK', 'Pink dials', ['Rose Gold · Pink Dial', 'Pink-Lavender · Studded Bracelet'], ['W2', 'W3']),
                                 ('JADE', 'Two-tone, emerald dial', ['Crystal-Style Bezel'], ['W4']),
                                 ('BLOOM', 'Black, dark green dial', ['Crystal Flower Design'], ['W1']),
                                 ('SHINE', 'Golden shine dial', ['Two-Tone Jubilee Chain · Stone Markers'], ['W5'])],
                         close=('Find yours', ['Ladies watches from Rs. 2,499', 'Free delivery all over Pakistan', 'Cash on Delivery'])),
        'G-SCENT': dict(kicker='EAU DE PARFUM · 50 ML', title='Find your Anjum fragrance', sub='Floral, oud or tea rose', cover=['P1', 'P2', 'P3'],
                        slides=[('LADY', 'Lady Aura', ['Premium Floral Fragrance', 'For Women · 50 ml'], ['P1']),
                                ('OUD', 'Oud Aura', ['Premium Oud Fragrance', 'Unisex · 50 ml'], ['P2']),
                                ('ROSE', 'Tea Rose', ['Premium Fragrance Oil', 'For Women · 50 ml'], ['P3'])],
                        close=('Choose your scent', ['Rs. 3,450 each · 50 ml', 'Free delivery all over Pakistan', 'Cash on Delivery'])),
    }
    for gid, g in guides.items():
        total = len(g['slides']) + 2
        add(f'{gid}-slide-01', f'Carousels/{gid}', FEED, ps.guide_cover(g['kicker'], g['title'], g['sub'], g['cover'], len(g['slides'])))
        for n, (label, title, lines, pids) in enumerate(g['slides'], start=2):
            add(f'{gid}-slide-{n:02d}', f'Carousels/{gid}', FEED, ps.guide_slide(n, total, label, title, lines, pids))
        add(f'{gid}-slide-{total:02d}', f'Carousels/{gid}', FEED, ps.guide_close(*g['close']))

    # Meet Anjum Mart and the engagement posts
    for fmt, size, tag in (('feed', FEED, 'feed-1080x1350'), ('story', STORY, 'story-1080x1920')):
        folder = 'Info' if fmt == 'feed' else 'Info'
        add(f'I-MEET-{tag}', folder, size, ps.meet(fmt))
        add(f'E-THIS1-{tag}', 'Engagement', size, ps.this_or_that(fmt, 'M1', 'M2'))
        add(f'E-THIS2-{tag}', 'Engagement', size, ps.this_or_that(fmt, 'W2', 'W5'))
        add(f'E-THIS3-{tag}', 'Engagement', size, ps.this_or_that(fmt, 'P1', 'P3'))
        add(f'E-THIS4-{tag}', 'Engagement', size, ps.this_or_that(fmt, 'M3', 'M7'))
        add(f'E-THIS5-{tag}', 'Engagement', size, ps.this_or_that(fmt, 'J1', 'J2'))
        add(f'E-TAG-{tag}', 'Engagement', size, ps.tag_post(fmt, 'M3', 'Tag someone who', 'needs a new watch'))
        add(f'E-WORD-{tag}', 'Engagement', size, ps.word_post(fmt, 'Want the details?', [('WATCH', "Men's and ladies watches"), ('JEWELLERY', 'Bridal sets with maang tikka'), ('PERFUME', 'Lady Aura, Oud Aura, Tea Rose')], 'We reply with prices, colours and how to order.'))

    # ad statics (evergreen: hook question, benefit chips, price, Shop Now), poll stories and store info cards
    for p in PRODUCTS:
        pid = p[0]
        add(f'AD-{pid}-feed-1080x1350', 'Ad-Statics', FEED, ps.ad_static('feed', pid))
        add(f'AD-{pid}-story-1080x1920', 'Ad-Statics', STORY, ps.ad_static('story', pid))
        add(f'INFO-{pid}-1600', 'Store-Info-Cards', (1600, 1600), ps.info_card(pid))
    polls = [('Black dial or blue dial?', ['M1', 'M2']), ('Pink or golden shine?', ['W2', 'W5']), ('Silver or green and gold?', ['J1', 'J2']),
             ('Floral or oud?', ['P1', 'P2']), ('Gold or silver?', ['M1', 'M4']), ('Green dial: yes or no?', ['M4', 'M5'])]
    for n, (q, pids) in enumerate(polls, 1):
        add(f'P-POLL{n}-story-1080x1920', 'Poll-Stories', STORY, ps.poll_story(q, pids))

    json.dump(jobs, open(os.path.join(OUT, 'jobs.json'), 'w'), indent=1)
    print(len(jobs), 'pictures')


main()
