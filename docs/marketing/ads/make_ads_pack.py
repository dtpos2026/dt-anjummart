"""Builds the Meta (Facebook / Instagram) ad creatives and caption files for Anjum Mart.

Usage:
  python3 make_ads_pack.py <cutouts_dir> <perfume_photos_dir> <out_dir>

  cutouts_dir          folder with cut-01.png ... cut-12.png (transparent product cut-outs, see docs/catalog/art)
  perfume_photos_dir   docs/catalog/art/perfume-photos (lady-portrait.jpg, oud-portrait.jpg, tea-portrait.jpg)
  out_dir              receives <set>/<format>/ HTML pages, caption files and jobs.json for render.mjs

Only facts from the store catalogue are used (prices, product details, free delivery, Cash on Delivery).
No discounts, urgency, ratings, reviews or authenticity claims.
"""
import json
import os
import sys

CUT, PERF, OUT = [os.path.abspath(a) for a in sys.argv[1:4]]
FONTS = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'fonts'))
LOGO = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'brand', 'editable',
                                    'anjum-mart-logo-for-dark-background.svg'))

FORMATS = {
    'feed': dict(w=1080, h=1350, folder='Feed-4x5', logo=44, eyebrow=142, title=176, sub=266,
                 zone=(335, 1065), price=1086, line=1196, cta=1246),
    'story': dict(w=1080, h=1920, folder='Story-Reels-9x16', logo=272, eyebrow=374, title=410, sub=500,
                  zone=(595, 1295), price=1322, line=1432, cta=1492),
}

# (cut file, dx, dy, height at feed size, rotation, z)
SETS = {
    '01-WOMEN-Instagram': [
        dict(id='W1-black-ladies-watch', eyebrow='LADIES WATCH · MOONSTON', title='Black Ladies Watch',
             sub='Dark Green Dial · Crystal Flower Design', price='Rs. 2,499', items=[('cut-12.png', 0, 0, 730, -14, 1)],
             name='MOONSTON black ladies quartz watch', url='moonston-black-ladies-watch-dark-green-dial-crystal-flower-design',
             about='a dark green textured dial and a crystal flower bracelet'),
        dict(id='W2-rose-gold-pink-dial', eyebrow='LADIES WATCH · MOONSTON', title='Rose Gold · Pink Dial',
             sub='Crystal-Style Luxury Design', price='Rs. 2,999',
             items=[('cut-08.png', -150, 0, 680, -5, 1), ('cut-09.png', 150, 0, 680, 6, 2)],
             name='MOONSTON rose gold ladies quartz watch', url='moonston-rose-gold-ladies-watch-pink-dial-crystal-style-luxury',
             about='a pink-lavender dial and a crystal-style design'),
        dict(id='W3-emerald-two-tone', eyebrow='LADIES WATCH · MOONSTON', title='Two-Tone · Emerald Dial',
             sub='Crystal-Style Bezel', price='Rs. 2,999', items=[('cut-05.png', 0, 0, 700, 0, 1)],
             name='MOONSTON two-tone ladies quartz watch', url='moonston-two-tone-ladies-watch-emerald-green-dial',
             about='an emerald green dial and a crystal-style bezel'),
        dict(id='W4-ladies-collection', eyebrow='LADIES WATCHES · MOONSTON', title='Ladies Watches',
             sub='Black · Pink · Emerald', price='From Rs. 2,499',
             items=[('cut-08.png', -290, 20, 600, -8, 1), ('cut-05.png', 290, 20, 600, 8, 1), ('cut-12.png', 0, 0, 700, 0, 2)],
             name='MOONSTON ladies quartz watches', url=None, about='crystal-style designs in black, pink and emerald'),
        dict(id='W5-bridal-jewellery-sets', eyebrow='BRIDAL JEWELLERY SETS', title='Bridal Jewellery Sets',
             sub='Necklace · Earrings · Maang Tikka', price='Rs. 1,999 each',
             items=[('cut-10.png', -200, 40, 560, 0, 1), ('cut-11.png', 150, 0, 660, 0, 2)],
             name='bridal jewellery sets', url=None, about='a necklace, earrings and maang tikka'),
    ],
    '02-MEN-Instagram-Facebook': [
        dict(id='M1-gold-black-dial', eyebrow="MEN'S WATCH · RUSTET", title='Gold · Black Dial',
             sub='Roman Numerals · Day & Date Display', price='Rs. 3,999', items=[('cut-03.png', 0, 0, 700, 0, 1)],
             name="RUSTET gold men's quartz watch", url='rustet-gold-mens-watch-black-dial-roman-numerals',
             about='a black dial, Roman numerals and a day and date display'),
        dict(id='M2-royal-blue-dial', eyebrow="MEN'S WATCH · RUSTET", title='Royal Blue Dial',
             sub='Gold & Silver · Day & Date Display', price='Rs. 3,999', items=[('cut-02.png', 0, 0, 700, 0, 1)],
             name="RUSTET gold and silver men's watch", url='rustet-gold-silver-mens-watch-royal-blue-dial',
             about='a royal blue dial and a day and date display'),
        dict(id='M3-all-black', eyebrow="MEN'S WATCH · RUSTET", title='All-Black Watch',
             sub='Black Dial · Day & Date Display', price='Rs. 3,999', items=[('cut-06.png', 0, 0, 700, 0, 1)],
             name="RUSTET all-black men's quartz watch", url='rustet-all-black-mens-watch-black-dial',
             about='a black dial and a day and date display'),
        dict(id='M4-silver-green-dial', eyebrow="MEN'S WATCHES · RUSTET", title='Silver · Green Dial',
             sub='Two Styles · Day & Date Display', price='Rs. 3,999',
             items=[('cut-04.png', -165, 0, 690, -5, 1), ('cut-07.png', 165, 0, 690, 6, 2)],
             name="RUSTET silver men's quartz watches", url='rustet-silver-mens-watch-emerald-green-dial',
             about='a green sunburst dial and a day and date display'),
        dict(id='M5-two-tone-white-dial', eyebrow="MEN'S WATCH · RUSTET", title='Two-Tone · White Dial',
             sub='Gold & Silver Quartz Watch', price='Rs. 3,999', items=[('cut-01.png', 0, 0, 700, 0, 1)],
             name="RUSTET two-tone gold and silver men's quartz watch", url='rustet-two-tone-gold-silver-mens-watch-white-dial',
             about='a white dial and a gold-tone bezel'),
        dict(id='M6-mens-collection', eyebrow="MEN'S WATCHES · RUSTET", title="Men's Quartz Watches",
             sub='Gold · Silver · Black', price='Rs. 3,999',
             items=[('cut-02.png', -290, 25, 600, -8, 1), ('cut-06.png', 290, 25, 600, 8, 1), ('cut-03.png', 0, 0, 700, 0, 2)],
             name="RUSTET men's quartz watches", url=None, about='gold, silver and black styles'),
    ],
    '03-BONUS-Perfumes': [
        dict(id='P1-anjum-perfumes', eyebrow='50 ML EAU DE PARFUM', title='Anjum Perfumes',
             sub='Lady Aura · Oud Aura · Tea Rose', price='Rs. 3,450', items='perfume',
             name='Anjum perfumes (Lady Aura, Oud Aura, Tea Rose)', url=None, about='three 50 ml Eau de Parfum fragrances'),
    ],
}


def perfume_cards(sf):
    w = 270 * sf
    h = w * 4 / 3
    step = w - 24 * sf
    out = ''
    for name, dx, rot, lift, sc in (('lady', -step, -3, 0, 1.0), ('tea', step, 3, 0, 1.0), ('oud', 0, 0, -h * 0.05, 1.1)):
        out += (f'<div class="card" style="left:calc(50% + {dx}px);top:calc(50% + {lift}px);width:{w * sc}px;height:{h * sc}px;'
                f'transform:translate(-50%,-50%) rotate({rot}deg);z-index:{2 if sc > 1 else 1};'
                f'background-image:url(file://{PERF}/{name}-portrait.jpg)"></div>')
    return out


def page(fmt, s):
    f = FORMATS[fmt]
    W, H = f['w'], f['h']
    z0, z1 = f['zone']
    zh = z1 - z0
    sf = zh / 730.0
    if s['items'] == 'perfume':
        prod = perfume_cards(sf)
    else:
        prod = ''
        for cut, dx, dy, h, rot, z in s['items']:
            prod += (f'<img class="prod" src="file://{CUT}/{cut}" style="left:calc(50% + {dx * sf}px);top:calc(50% + {dy * sf}px);'
                     f'height:{h * sf}px;transform:translate(-50%,-50%) rotate({rot}deg);z-index:{z}">')
    return f'''<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:Cormorant;font-weight:600;src:url(file://{FONTS}/cormorant-latin-600-normal.woff2)}}
@font-face{{font-family:Jost;font-weight:400;src:url(file://{FONTS}/jost-latin-400-normal.woff2)}}
@font-face{{font-family:Jost;font-weight:500;src:url(file://{FONTS}/jost-latin-500-normal.woff2)}}
@font-face{{font-family:Jost;font-weight:600;src:url(file://{FONTS}/jost-latin-600-normal.woff2)}}
*{{box-sizing:border-box}}html,body{{margin:0;padding:0}}
body{{width:{W}px;height:{H}px;position:relative;overflow:hidden;color:#fff;font-family:Jost,sans-serif;
background:radial-gradient(ellipse 75% 50% at 50% {(z0 + zh / 2) / H * 100:.1f}%,#40300f 0%,#17120a 52%,#090909 100%)}}
.bk{{position:absolute;border-radius:50%;background:radial-gradient(circle,rgba(230,200,117,.55),rgba(230,200,117,0) 70%);filter:blur(2px)}}
.frame{{position:absolute;inset:22px;border:1.5px solid rgba(212,175,55,.6)}}
.logo{{position:absolute;left:50%;top:{f['logo']}px;height:78px;transform:translateX(-50%)}}
.t{{position:absolute;left:70px;right:70px;text-align:center;white-space:nowrap}}
.eyebrow{{top:{f['eyebrow']}px;font:500 26px/1 Jost;letter-spacing:5px;color:#e6c875}}
.title{{top:{f['title']}px;font:600 76px/1.05 Cormorant,serif;letter-spacing:1px}}
.sub{{top:{f['sub']}px;font:400 30px/1.2 Jost;color:#dcdcdc;letter-spacing:.5px}}
.zone{{position:absolute;left:0;right:0;top:{z0}px;height:{zh}px}}
.glow{{position:absolute;left:50%;top:50%;width:900px;height:900px;transform:translate(-50%,-50%);background:radial-gradient(circle,rgba(212,175,55,.26),rgba(212,175,55,0) 62%)}}
.floor{{position:absolute;left:50%;bottom:-6px;width:760px;height:60px;transform:translateX(-50%);background:radial-gradient(ellipse,rgba(0,0,0,.75),rgba(0,0,0,0) 70%)}}
.prod{{position:absolute;width:auto;filter:drop-shadow(0 22px 28px rgba(0,0,0,.65))}}
.card{{position:absolute;background-size:cover;background-position:center;border:4px solid #d4af37;border-radius:3px;box-shadow:0 24px 34px rgba(0,0,0,.6),0 0 40px rgba(212,175,55,.2)}}
.price{{top:{f['price']}px;font:600 100px/1 Cormorant,serif;color:#e6c875;letter-spacing:1px}}
.line{{top:{f['line']}px;font:500 28px/1 Jost;color:#f1f1f1;letter-spacing:1px}}
.cta{{position:absolute;top:{f['cta']}px;left:50%;transform:translateX(-50%);height:80px;padding:0 44px;border-radius:40px;background:#d4af37;color:#111;
display:flex;align-items:center;gap:16px;font:600 31px/1 Jost;letter-spacing:2.5px;white-space:nowrap;box-shadow:0 10px 26px rgba(0,0,0,.5)}}
.cta svg{{width:42px;height:42px}}
</style></head><body>
<div class="bk" style="left:90px;top:{z0 + 60}px;width:70px;height:70px"></div>
<div class="bk" style="left:{W - 170}px;top:{z0 + 160}px;width:48px;height:48px"></div>
<div class="bk" style="left:{W - 250}px;top:{z0 + zh - 140}px;width:90px;height:90px"></div>
<div class="bk" style="left:150px;top:{z0 + zh - 220}px;width:44px;height:44px"></div>
<div class="frame"></div>
<img class="logo" src="file://{LOGO}">
<div class="t eyebrow">{s['eyebrow']}</div>
<div class="t title fit">{s['title']}</div>
<div class="t sub fit">{s['sub']}</div>
<div class="zone"><div class="glow"></div><div class="floor"></div>{prod}</div>
<div class="t price">{s['price']}</div>
<div class="t line">Free Delivery All Pakistan &nbsp;·&nbsp; Cash on Delivery</div>
<div class="cta"><svg viewBox="0 0 32 32" fill="#111"><path d="M16.04 3C9.4 3 4 8.38 4 15.02c0 2.12.55 4.2 1.6 6.03L4 29l8.14-1.56a12.02 12.02 0 0 0 3.9.65C22.68 28.09 28 22.7 28 16.07 28 9.4 22.7 3 16.04 3zm0 22.1c-1.2 0-2.38-.3-3.42-.87l-.5-.27-4.83.93.96-4.7-.3-.52a9.1 9.1 0 0 1-1.4-4.84c0-5.03 4.1-9.1 9.15-9.1 5.02 0 9.1 4.07 9.1 9.1 0 5.04-4.08 9.27-8.76 9.27zm5.1-6.9c-.28-.14-1.65-.82-1.9-.9-.26-.1-.44-.14-.63.14-.19.28-.72.9-.88 1.1-.16.18-.32.2-.6.07-.28-.14-1.18-.44-2.25-1.4-.83-.74-1.4-1.66-1.56-1.94-.16-.28-.02-.43.12-.57.13-.12.28-.32.42-.48.14-.16.19-.28.28-.47.1-.19.05-.35-.02-.5-.07-.14-.63-1.5-.86-2.06-.23-.54-.46-.47-.63-.48h-.54c-.19 0-.5.07-.76.35-.26.28-1 .97-1 2.38s1.03 2.76 1.17 2.95c.14.19 2.02 3.08 4.9 4.32.68.3 1.22.47 1.63.6.69.22 1.31.19 1.8.11.55-.08 1.65-.67 1.88-1.32.23-.65.23-1.2.16-1.32-.07-.12-.26-.19-.54-.33z"/></svg>ORDER ON WHATSAPP</div>
<script>
function fit(){{document.querySelectorAll('.fit').forEach(function(e){{var fs=parseFloat(getComputedStyle(e).fontSize);e.style.left='70px';e.style.right='70px';while(e.scrollWidth>e.clientWidth&&fs>34){{fs-=2;e.style.fontSize=fs+'px'}}}})}}
document.fonts.ready.then(function(){{fit();document.body.setAttribute('data-ready','1')}});
</script></body></html>'''


def captions(setname, s, audience):
    coll = {'W4': 'womens-watches', 'W5': 'artificial-jewellery', 'M6': 'mens-watches', 'P1': 'perfumes'}.get(s['id'].split('-')[0])
    cta_url = f"https://anjummart.com/products/{s['url']}" if s['url'] else f"https://anjummart.com/collections/{coll}"
    tags = {
        'women': '#AnjumMart #LadiesWatches #WomensWatch #WatchesForWomen #WatchesPakistan #OnlineShoppingPakistan #FreeDeliveryPakistan #CashOnDelivery #MoonstonWatch #Multan #WatchLovers',
        'men': '#AnjumMart #MensWatches #WatchesForMen #RustetWatch #WatchesPakistan #OnlineShoppingPakistan #FreeDeliveryPakistan #CashOnDelivery #MensFashionPakistan #Multan #WatchLovers',
        'jewellery': '#AnjumMart #BridalJewellery #JewelleryPakistan #ArtificialJewellery #MaangTikka #BridalSet #WeddingJewellery #MehndiJewellery #EidJewellery #FreeDeliveryPakistan #CashOnDelivery #Multan',
        'perfume': '#AnjumMart #AnjumPerfumes #LadyAura #OudAura #TeaRose #EauDeParfum #PerfumesPakistan #FragranceLovers #FreeDeliveryPakistan #CashOnDelivery #Multan',
    }
    key = 'jewellery' if 'jewellery' in s['id'] else 'perfume' if s['id'].startswith('P') else audience
    price = s['price']
    en = (f"{s['title']} ✨\n{s['name'][0].upper() + s['name'][1:]} with {s['about']}.\n"
          f"{price} · Free delivery all over Pakistan · Cash on Delivery.\n"
          f"Tap the WhatsApp button to order or ask us anything.")
    ur = (f"{s['title']} ✨\n{s['name'][0].upper() + s['name'][1:]}: {s['about']}.\n"
          f"Qeemat {price}. Poore Pakistan mein free delivery aur Cash on Delivery.\n"
          f"Order ya sawaal ke liye WhatsApp button dabayein.")
    short = f"{s['title']} · {price}. Free delivery all over Pakistan, Cash on Delivery. Message us on WhatsApp to order."
    head = f"{s['title']} · {price}"[:40]
    greet = (f"Assalamualaikum! I like the {s['title']} ({price}). Please share the details.")
    return f'''==================================================
{s['id']}
==================================================
CAPTION FOR THE POST (English)
{en}

CAPTION FOR THE POST (Roman Urdu)
{ur}

HASHTAGS (paste under the caption)
{tags[key]}

META ADS FIELDS (Click to WhatsApp ad)
Primary text : {short}
Headline     : {head}
Description  : Free delivery all over Pakistan · Cash on Delivery
Call to action: WhatsApp message (Send WhatsApp message)
Customer's pre-filled WhatsApp message: {greet}
Product page (for your replies): {cta_url}

'''


def main():
    jobs = []
    os.makedirs(OUT, exist_ok=True)
    for setname, specs in SETS.items():
        audience = 'women' if 'WOMEN' in setname else 'men' if 'MEN' in setname else 'perfume'
        txt = ''
        for s in specs:
            for fmt, f in FORMATS.items():
                d = os.path.join(OUT, 'html', setname, f['folder'])
                os.makedirs(d, exist_ok=True)
                name = f"{s['id']}-{fmt}-{f['w']}x{f['h']}"
                hp = os.path.join(d, name + '.html')
                open(hp, 'w').write(page(fmt, s))
                jobs.append(dict(html=hp, out=os.path.join(OUT, 'final', setname, f['folder'], name + '.jpg'), w=f['w'], h=f['h']))
            txt += captions(setname, s, audience)
        cdir = os.path.join(OUT, 'final', setname)
        os.makedirs(cdir, exist_ok=True)
        label = {'01-WOMEN-Instagram': 'Women (Instagram only)', '02-MEN-Instagram-Facebook': 'Men (Instagram + Facebook)',
                 '03-BONUS-Perfumes': 'Bonus: Perfumes'}[setname]
        open(os.path.join(cdir, 'CAPTIONS-' + setname.split('-', 1)[1] + '.txt'), 'w').write(
            f'ANJUM MART: CAPTIONS AND AD TEXTS, {label}\nEach block matches the picture with the same code (feed and story).\n\n' + txt)
    json.dump(jobs, open(os.path.join(OUT, 'jobs.json'), 'w'), indent=1)
    print(len(jobs), 'pictures')


main()
