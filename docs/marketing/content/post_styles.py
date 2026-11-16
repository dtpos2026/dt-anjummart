"""Colour-story post pictures (the "colour series"), cream guide carousels, the "Meet Anjum Mart" post and the engagement posts
(this-or-that, tag-someone, comment-a-word). Same look as the reels: one colour world per product, a giant watermark word behind
the piece, one hook line, the name and a price pill.  Only catalogue facts: names, dial colours, prices, free delivery, COD.

Used by make_posts.py:  import post_styles as ps;  ps.setup(cutouts_dir, perfume_photos_dir)
"""
import html
import os

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.abspath(os.path.join(HERE, '..', 'fonts'))
MARK = os.path.abspath(os.path.join(HERE, '..', '..', 'brand', 'icon', 'anjum-mart-logo-mark-transparent-1024.png'))
from catalog import BY, THEMES  # noqa: E402

FEED = (1080, 1350)
STORY = (1080, 1920)
CUT = PERF = ''

# positions per format: mark, watermark top, product centre y, product height, hook, name, pill, line
POS = {
    'feed': dict(mark=46, wm=250, cy=640, ph=640, hook=1000, name=1100, pill=1176, line=1286, counter=62),
    'story': dict(mark=262, wm=520, cy=870, ph=760, hook=1290, name=1394, pill=1476, line=1610, counter=290),
}

CSS = '''
@font-face{font-family:Cormorant;font-weight:600;src:url(file://FONTS/cormorant-latin-600-normal.woff2)}
@font-face{font-family:Cormorant;font-weight:500;src:url(file://FONTS/cormorant-latin-500-normal.woff2)}
@font-face{font-family:Jost;font-weight:400;src:url(file://FONTS/jost-latin-400-normal.woff2)}
@font-face{font-family:Jost;font-weight:500;src:url(file://FONTS/jost-latin-500-normal.woff2)}
@font-face{font-family:Jost;font-weight:600;src:url(file://FONTS/jost-latin-600-normal.woff2)}
*{box-sizing:border-box}html,body{margin:0;padding:0}
body{width:WPXpx;height:HPXpx;position:relative;overflow:hidden;font-family:Jost,sans-serif;BODYBG}
.abs{position:absolute}
.t{position:absolute;left:50px;right:50px;text-align:center;white-space:nowrap}
.wm{position:absolute;left:-40px;right:-40px;text-align:center;font:600 380px/1 Cormorant,serif;letter-spacing:4px;white-space:nowrap}
.mark{position:absolute;left:50%;transform:translateX(-50%);height:96px}
.prod{position:absolute;filter:drop-shadow(0 26px 34px rgba(0,0,0,.5));transform:translate(-50%,-50%)}
.card{position:absolute;transform:translate(-50%,-50%);background-size:cover;background-position:center;border:5px solid #d4af37;border-radius:3px;box-shadow:0 28px 44px rgba(0,0,0,.5)}
.hook{font:italic 600 76px/1.1 Cormorant,serif}
.name{font:500 28px/1 Jost;letter-spacing:7px;text-transform:uppercase}
.pill{position:absolute;left:50%;transform:translateX(-50%);height:90px;padding:0 54px;border-radius:45px;display:flex;align-items:center;font:600 38px/1 Jost;letter-spacing:2px;white-space:nowrap;box-shadow:0 14px 34px rgba(0,0,0,.3)}
.small{font:400 24px/1 Jost;letter-spacing:1.5px}
.rule{position:absolute;height:2px;background:linear-gradient(90deg,transparent,#b98d1c,transparent)}
.cnt{position:absolute;font:500 26px/1 Jost;letter-spacing:5px}
.big{font:600 96px/1.04 Cormorant,serif}
.cta{position:absolute;left:50%;transform:translateX(-50%);height:84px;padding:0 48px;border-radius:42px;background:#d4af37;color:#111;display:flex;align-items:center;gap:16px;font:600 30px/1 Jost;letter-spacing:2.5px;white-space:nowrap}
.cta svg{width:42px;height:42px}
'''
SCRIPT = '''<script>
function fit(){document.querySelectorAll('.fit').forEach(function(e){var fs=parseFloat(getComputedStyle(e).fontSize);var min=parseFloat(e.getAttribute('data-min')||30);while(e.scrollWidth>e.clientWidth&&fs>min){fs-=2;e.style.fontSize=fs+'px'}})}
function fitwm(){document.querySelectorAll('.wm').forEach(function(e){var fs=parseFloat(getComputedStyle(e).fontSize);var s=document.createElement('span');s.style.cssText='position:absolute;visibility:hidden;white-space:nowrap;font:600 '+fs+'px Cormorant;letter-spacing:4px';s.textContent=e.textContent;document.body.appendChild(s);while(s.offsetWidth>1000&&fs>200){fs-=10;s.style.fontSize=fs+'px'}e.style.fontSize=fs+'px';document.body.removeChild(s)})}
document.fonts.ready.then(function(){fitwm();fit();document.body.setAttribute('data-ready','1')});
</script>'''
WA_ICON = ('<svg viewBox="0 0 32 32" fill="#111"><path d="M16.04 3C9.4 3 4 8.38 4 15.02c0 2.12.55 4.2 1.6 6.03L4 29l8.14-1.56a12.02 12.02 0 0 0 3.9.65C22.68 28.09 28 22.7 28 16.07 28 9.4 22.7 3 16.04 3zm0 22.1c-1.2 0-2.38-.3-3.42-.87l-.5-.27-4.83.93.96-4.7-.3-.52a9.1 9.1 0 0 1-1.4-4.84c0-5.03 4.1-9.1 9.15-9.1 5.02 0 9.1 4.07 9.1 9.1 0 5.04-4.08 9.27-8.76 9.27zm5.1-6.9c-.28-.14-1.65-.82-1.9-.9-.26-.1-.44-.14-.63.14-.19.28-.72.9-.88 1.1-.16.18-.32.2-.6.07-.28-.14-1.18-.44-2.25-1.4-.83-.74-1.4-1.66-1.56-1.94-.16-.28-.02-.43.12-.57.13-.12.28-.32.42-.48.14-.16.19-.28.28-.47.1-.19.05-.35-.02-.5-.07-.14-.63-1.5-.86-2.06-.23-.54-.46-.47-.63-.48h-.54c-.19 0-.5.07-.76.35-.26.28-1 .97-1 2.38s1.03 2.76 1.17 2.95c.14.19 2.02 3.08 4.9 4.32.68.3 1.22.47 1.63.6.69.22 1.31.19 1.8.11.55-.08 1.65-.67 1.88-1.32.23-.65.23-1.2.16-1.32-.07-.12-.26-.19-.54-.33z"/></svg>')

CREAM = ('#f8f1e1', '#e8d8b3')


def setup(cut, perf):
    global CUT, PERF
    CUT, PERF = cut, perf


def esc(s):
    return html.escape(s)


def src_of(row):
    return 'file://' + os.path.join(PERF if row[1] == 'photo' else CUT, row[3])


def head(w, h, bg, extra=''):
    css = CSS.replace('FONTS', FONTS).replace('WPX', str(w)).replace('HPX', str(h)).replace('BODYBG', f'background:{bg}')
    return f'<!doctype html><html><head><meta charset="utf-8"><style>{css}{extra}</style></head><body>'


def grad(bg):
    return f'linear-gradient(180deg,{bg[0]} 0%,{bg[1]} 100%)'


def glow(th, w, cy, size=1300):
    a = '.42' if th['dark'] else '.22'
    return (f'<div class="abs" style="left:{w / 2 - size / 2}px;top:{cy - size / 2}px;width:{size}px;height:{size}px;'
            f'background:radial-gradient(circle,rgba(255,255,255,{a}),rgba(255,255,255,0) 60%)"></div>')


def piece(row, cx, cy, ph, rot=0, z=1):
    """A cut-out piece (height ph px) or a framed perfume photo card (3:4)."""
    if row[1] == 'photo':
        h = ph * 0.9
        return (f'<div class="card" style="left:{cx}px;top:{cy}px;width:{h * 0.75}px;height:{h}px;z-index:{z};'
                f'transform:translate(-50%,-50%) rotate({rot}deg);background-image:url({src_of(row)})"></div>')
    return f'<img class="prod" src="{src_of(row)}" style="left:{cx}px;top:{cy}px;height:{ph}px;z-index:{z};transform:translate(-50%,-50%) rotate({rot}deg)">'


def pill(th, text, top):
    bg, fg = ('#1b1307', '#f1d98a') if th['dark'] else ('#f8f1e1', '#1b1307')
    return f'<div class="pill" style="top:{top}px;background:{bg};color:{fg}">{esc(text)}</div>'


def colour_post(fmt, pid):
    """The colour series post for one product: watermark word, the piece, a hook line, the name and a price pill."""
    row, th = BY[pid], THEMES[pid]
    w, h = FEED if fmt == 'feed' else STORY
    P = POS[fmt]
    fg = '#1b1307' if th['dark'] else '#ffffff'
    wmc = 'rgba(27,19,7,.12)' if th['dark'] else 'rgba(255,255,255,.2)'
    b = head(w, h, grad(th['bg'])) + glow(th, w, P['cy'])
    b += f'<div class="wm" style="top:{P["wm"]}px;color:{wmc}">{esc(th["word"])}</div>'
    b += f'<img class="mark" style="top:{P["mark"]}px" src="file://{MARK}">'
    b += piece(row, w / 2, P['cy'], P['ph'], 0, 2)
    b += f'<div class="t hook fit" data-min="44" style="top:{P["hook"]}px;color:{fg}">{esc(th["hook"])}</div>'
    b += f'<div class="t name fit" data-min="20" style="top:{P["name"]}px;color:{th["acc"]}">{esc(row[5])}</div>'
    b += pill(th, f'{row[7]}  ·  anjummart.com', P['pill'])
    b += f'<div class="t small" style="top:{P["line"]}px;color:{fg};opacity:.85">Free Delivery All Pakistan  ·  Cash on Delivery</div>'
    return b + SCRIPT + '</body></html>'


# ---- guides on cream -----------------------------------------------------------------------------------------------
GUIDE_CSS = '.g-title{font:600 84px/1.05 Cormorant,serif;color:#241706}.g-kick{font:500 26px/1 Jost;letter-spacing:8px;color:#7a5414;text-transform:uppercase}.g-text{font:400 34px/1.3 Jost;color:#3d3217}.g-num{font:500 26px/1 Jost;letter-spacing:5px;color:#7a5414}'


def _cream(w, h):
    return head(w, h, grad(CREAM), GUIDE_CSS) + glow(dict(dark=True), w, h * 0.45)


def guide_cover(kicker, title, sub, rows, total):
    w, h = FEED
    b = _cream(w, h)
    b += f'<img class="mark" style="top:50px" src="file://{MARK}">'
    b += f'<div class="t g-kick" style="top:170px">{esc(kicker)}</div>'
    b += f'<div class="t g-title fit" style="top:214px;font-size:104px">{esc(title)}</div>'
    n = len(rows)
    xs = [w / 2 + (i - (n - 1) / 2) * (min(300, 820 / n)) for i in range(n)]
    for r, x in zip(rows, xs):
        ph = 560 if n <= 3 else 470
        b += piece(BY[r], x, 760, ph, (x - w / 2) / 60, 2)
    b += f'<div class="t g-text fit" style="top:1110px">{esc(sub)}</div>'
    b += f'<div class="t g-num" style="top:1230px">SWIPE TO SEE ALL {total} &rarr;</div>'
    return b + SCRIPT + '</body></html>'


def guide_slide(idx, total, label, title, lines, pids):
    """One slide of a guide: a coloured band for the colour, the piece(s), a short line each."""
    w, h = FEED
    th = THEMES[pids[0]]
    b = head(w, h, grad(th['bg']), GUIDE_CSS) + glow(th, w, 600)
    fg = '#1b1307' if th['dark'] else '#ffffff'
    wmc = 'rgba(27,19,7,.12)' if th['dark'] else 'rgba(255,255,255,.2)'
    b += f'<div class="wm" style="top:240px;color:{wmc}">{esc(label)}</div>'
    b += f'<img class="mark" style="top:46px" src="file://{MARK}">'
    b += f'<div class="cnt" style="left:60px;top:76px;color:{th["acc"]}">{idx:02d} / {total:02d}</div>'
    n = len(pids)
    for i, pid in enumerate(pids):
        x = w / 2 + (i - (n - 1) / 2) * 380
        b += piece(BY[pid], x, 640, 600 if n == 1 else 520, (i - (n - 1) / 2) * 5, 2)
    b += f'<div class="t hook fit" data-min="44" style="top:980px;color:{fg}">{esc(title)}</div>'
    for i, ln in enumerate(lines):
        b += f'<div class="t name fit" data-min="18" style="top:{1078 + i * 46}px;color:{th["acc"]};letter-spacing:4px;font-size:25px">{esc(ln)}</div>'
    prices = sorted(int(''.join(ch for ch in BY[q][7] if ch.isdigit())) for q in pids)
    ptxt = f'Rs. {prices[0]:,}' if prices[0] == prices[-1] else f'From Rs. {prices[0]:,}'
    b += pill(th, f'{ptxt}{" each" if n > 1 and prices[0] == prices[-1] else ""}  ·  anjummart.com', 1210)
    return b + SCRIPT + '</body></html>'


def guide_close(title, lines):
    w, h = FEED
    b = _cream(w, h)
    b += f'<img class="mark" style="top:170px;height:200px" src="file://{MARK}">'
    b += f'<div class="t g-title fit" style="top:430px">{esc(title)}</div>'
    b += '<div class="rule" style="left:350px;width:380px;top:550px"></div>'
    for i, ln in enumerate(lines):
        b += f'<div class="t g-text fit" style="top:{600 + i * 62}px">{esc(ln)}</div>'
    b += '<div class="t g-kick" style="top:850px;font-size:32px">ANJUMMART.COM</div>'
    b += f'<div class="cta" style="top:950px">{WA_ICON}ORDER ON WHATSAPP</div>'
    b += '<div class="t g-text" style="top:1090px;font-size:26px">Free Delivery All Pakistan  ·  Cash on Delivery</div>'
    return b + SCRIPT + '</body></html>'


# ---- Meet Anjum Mart ------------------------------------------------------------------------------------------------
def meet(fmt):
    w, h = FEED if fmt == 'feed' else STORY
    s = 1.0 if fmt == 'feed' else 1.42
    top = 0 if fmt == 'feed' else 280
    b = head(w, h, grad(CREAM), GUIDE_CSS) + glow(dict(dark=True), w, h * 0.45)
    b += f'<img class="mark" style="top:{50 + top * 0.6}px;height:150px" src="file://{MARK}">'
    b += f'<div class="t g-kick" style="top:{235 + top * 0.8}px">MEET ANJUM MART</div>'
    b += f'<div class="t g-title fit" style="top:{285 + top * 0.8}px;font-size:92px">Timeless Style.</div>'
    b += f'<div class="t g-title fit" style="top:{385 + top * 0.8}px;font-size:92px;font-style:italic;color:#7a5414">Everyday Luxury.</div>'
    y0 = 760 + top * 1.1
    sc = 1.0
    b += piece(BY['M1'], w / 2 - 300 * sc, y0, 470 * s, -6, 1)
    b += piece(BY['W2'], w / 2 - 70 * sc, y0 + 10, 520 * s, 3, 2)
    b += piece(BY['J2'], w / 2 + 40 * sc, y0 + 190 * s, 300 * s, 0, 3)
    b += piece(BY['P1'], w / 2 + 300 * sc, y0, 430 * s, 5, 2)
    b += f'<div class="t g-text fit" style="top:{1130 + top * 1.45}px;font-size:40px">Watches  ·  Jewellery  ·  Perfumes</div>'
    b += f'<div class="t g-text" style="top:{1190 + top * 1.5}px;font-size:28px;letter-spacing:2px">Free Delivery All Pakistan  ·  Cash on Delivery</div>'
    return b + SCRIPT + '</body></html>'


# ---- engagement ---------------------------------------------------------------------------------------------------
def this_or_that(fmt, a, b_, question='THIS OR THAT?'):
    w, h = FEED if fmt == 'feed' else STORY
    ta, tb = THEMES[a], THEMES[b_]
    top = 0 if fmt == 'feed' else 280
    half = w / 2
    b = head(w, h, '#111')
    b += f'<div class="abs" style="left:0;top:0;width:{half}px;height:{h}px;background:{grad(ta["bg"])}"></div>'
    b += f'<div class="abs" style="left:{half}px;top:0;width:{half}px;height:{h}px;background:{grad(tb["bg"])}"></div>'
    for th, x in ((ta, half / 2), (tb, half + half / 2)):
        b += glow(th, 2 * x, 650 + top * 0.6, 900).replace(f'left:{x * 2 / 2 - 450}px', f'left:{x - 450}px')
    b += f'<div class="abs" style="left:{half - 1}px;top:0;width:2px;height:{h}px;background:rgba(255,255,255,.65)"></div>'
    b += f'<img class="mark" style="top:{46 + top * 0.6}px" src="file://{MARK}">'
    b += f'<div class="pill" style="top:{170 + top * 0.8}px;height:72px;padding:0 44px;background:#1b1307;color:#f1d98a;font-size:32px;letter-spacing:8px;z-index:5">{esc(question)}</div>'
    cy = 610 + top * 0.8
    b += piece(BY[a], half / 2, cy, 520, -3, 2)
    b += piece(BY[b_], half + half / 2, cy, 520, 3, 2)
    for th, x, n in ((ta, half / 2, '1'), (tb, half + half / 2, '2')):
        fg = '#1b1307' if th['dark'] else '#fff'
        b += f'<div class="abs" style="left:{x - 60}px;top:{cy + 300}px;width:120px;height:120px;border-radius:60px;border:3px solid {fg};color:{fg};font:600 84px/114px Cormorant,serif;text-align:center">{n}</div>'
        b += f'<div class="abs" style="left:{x - 255}px;top:{cy + 440}px;width:510px;text-align:center;font:500 25px/1.2 Jost;letter-spacing:4px;text-transform:uppercase;color:{fg if th["dark"] else th["acc"]}">{esc(BY[a if n == "1" else b_][5])}</div>'
    b += f'<div class="pill" style="top:{h - 175 - (0 if fmt == "feed" else 230)}px;background:#f8f1e1;color:#1b1307;font-size:36px">COMMENT 1 OR 2</div>'
    return b + SCRIPT + '</body></html>'


def tag_post(fmt, pid, line1, line2):
    th = THEMES[pid]
    w, h = FEED if fmt == 'feed' else STORY
    P = POS[fmt]
    fg = '#1b1307' if th['dark'] else '#ffffff'
    wmc = 'rgba(27,19,7,.12)' if th['dark'] else 'rgba(255,255,255,.2)'
    b = head(w, h, grad(th['bg'])) + glow(th, w, P['cy'] - 40)
    b += f'<div class="wm" style="top:{P["wm"] - 60}px;color:{wmc}">{esc(th["word"])}</div>'
    b += f'<img class="mark" style="top:{P["mark"]}px" src="file://{MARK}">'
    b += piece(BY[pid], w / 2, P['cy'] - 70, P['ph'] * 0.92, 0, 2)
    b += f'<div class="t big fit" data-min="50" style="top:{P["hook"] - 90}px;color:{fg};font-size:88px">{esc(line1)}</div>'
    b += f'<div class="t big fit" data-min="50" style="top:{P["hook"] + 10}px;color:{th["acc"]};font-size:88px;font-style:italic">{esc(line2)}</div>'
    b += pill(th, 'TAG THEM IN THE COMMENTS  ↓', P['pill'] + 20)
    b += f'<div class="t small" style="top:{P["line"] + 20}px;color:{fg};opacity:.85">anjummart.com  ·  Free Delivery All Pakistan</div>'
    return b + SCRIPT + '</body></html>'


def word_post(fmt, title, words, sub):
    """Comment-a-word post on cream: the shopper types a word and we reply by hand with the details."""
    w, h = FEED if fmt == 'feed' else STORY
    top = 0 if fmt == 'feed' else 260
    b = head(w, h, grad(CREAM), GUIDE_CSS) + glow(dict(dark=True), w, h * 0.45)
    b += f'<img class="mark" style="top:{50 + top * 0.5}px;height:130px" src="file://{MARK}">'
    b += f'<div class="t g-title fit" style="top:{230 + top * 0.8}px;font-size:96px">{esc(title)}</div>'
    b += f'<div class="rule" style="left:350px;width:380px;top:{360 + top * 0.8}px"></div>'
    y = 420 + top * 0.9
    for wd, what in words:
        b += f'<div class="abs" style="left:110px;right:110px;top:{y}px;height:150px;border:2.5px solid #7a5414;border-radius:6px;background:rgba(255,255,255,.45);display:flex;align-items:center;gap:34px;padding:0 40px">'
        b += f'<div style="font:600 58px/1 Cormorant,serif;letter-spacing:3px;color:#241706;min-width:290px">{esc(wd)}</div>'
        b += f'<div style="font:400 30px/1.25 Jost;color:#3d3217">{esc(what)}</div></div>'
        y += 176
    b += f'<div class="t g-text fit" style="top:{y + 20}px;font-size:32px">{esc(sub)}</div>'
    b += f'<div class="cta" style="top:{y + 96}px">{WA_ICON}WHATSAPP +92 371 4661514</div>'
    return b + SCRIPT + '</body></html>'
