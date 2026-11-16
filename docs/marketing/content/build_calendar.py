"""Builds the 30-day content calendar PDF (Instagram, Facebook, TikTok) and the caption files.

Usage: python3 build_calendar.py <posts_final_dir> <posters_dir> <out_dir>
  posts_final_dir  .../posts/final   (from make_posts.py + ../ads/render.mjs)
  posters_dir      folder with R-<id>.jpg poster frames of the reels
  out_dir          receives Content-Calendar-and-Captions.pdf, captions/*.txt and captions.csv
"""
import csv
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from plan30 import STORY_TIMES, entries  # noqa: E402
from copytext import PRODUCTS, COLLECTIONS, INFO, caption, hashtags, first_comment  # noqa: E402
from pdfcommon import page, cover, to_pdf, e  # noqa: E402

POSTS, POSTERS, OUT = [os.path.abspath(a) for a in sys.argv[1:4]]
os.makedirs(os.path.join(OUT, 'captions'), exist_ok=True)


def copy_of(key):
    return PRODUCTS.get(key) or COLLECTIONS.get(key) or INFO.get(key)


def thumb(asset):
    if asset.startswith('R-'):
        f = os.path.join(POSTERS, asset + '.jpg')
    elif asset[0] in 'CG':
        f = os.path.join(POSTS, 'Carousels', asset, asset + '-slide-01.jpg')
    elif asset.startswith('I-'):
        f = os.path.join(POSTS, 'Info', asset + '-feed-1080x1350.jpg')
    elif asset.startswith('K-'):
        f = os.path.join(POSTS, 'Color-Series', asset + '-feed-1080x1350.jpg')
    elif asset.startswith('E-'):
        f = os.path.join(POSTS, 'Engagement', asset + '-feed-1080x1350.jpg')
    else:
        f = os.path.join(POSTS, 'Feed-4x5', asset + '-feed-1080x1350.jpg')
    return f if os.path.exists(f) else None


FILES = {
    'R': 'Reels/{a}.mp4',
    'C': 'Carousels/{a}/ (slides 01 to last, in order)',
    'G': 'Carousels/{a}/ (slides 01 to last, in order)',
    'I': 'Info/{a}-feed-1080x1350.jpg (story: {a}-story-1080x1920.jpg)',
    'K': 'Color-Series/{a}-feed-1080x1350.jpg (story: {a}-story-1080x1920.jpg)',
    'E': 'Engagement/{a}-feed-1080x1350.jpg (story: {a}-story-1080x1920.jpg)',
}


def file_hint(asset):
    return FILES[asset[0]].format(a=asset)


def story_for(entry):
    """Morning story: the story picture of the day. Evening story: a poll story (Poll sticker in the empty band)."""
    a = entry['asset']
    if a[0] in 'KIE':
        pic = a + '-story-1080x1920.jpg'
    elif a[0] == 'R':
        pic = 'the reel poster (or the matching colour-story picture)'
    else:
        pic = 'the first carousel slide'
    poll = f"P-POLL{(entry['day'] - 1) % 6 + 1}-story-1080x1920.jpg (add the Poll sticker in the empty band)"
    return pic, poll


FORMAT = {
    'reel': {'ig': 'Reel', 'fb': 'Reel', 'tt': 'Video'},
    'carousel': {'ig': 'Carousel', 'fb': 'Album', 'tt': 'Photo mode (swipe)'},
    'feed': {'ig': 'Feed post', 'fb': 'Photo post', 'tt': 'not needed'},
    'engage': {'ig': 'Feed post + story sticker', 'fb': 'Photo post', 'tt': 'not needed'},
}


def tm(en, plat):
    return en['times'].get(plat, '-')


def build():
    ents = entries()
    rows = []
    days_html = ''
    txt = {'ig': '', 'fb': '', 'tt': ''}
    for en in ents:
        key = en['key']
        c = copy_of(key)
        d = en['date']
        ds = f"{en['weekday']} {d.day} {d.strftime('%b %Y')}"
        cap_ig, cap_fb, cap_tt = caption(key, 'ig'), caption(key, 'fb'), caption(key, 'tt')
        fc = first_comment(key)
        t = thumb(en['asset'])
        pills = ''.join(f'<span class="pill {p}">{ {"ig": "Instagram", "fb": "Facebook", "tt": "TikTok"}[p] }</span>' for p in en['platforms'])
        pic, sticker = story_for(en)
        rows.append([en['day'], d.isoformat(), en['weekday'], en['theme'], en['kind'], en['asset'], tm(en, 'ig'), tm(en, 'fb'), tm(en, 'tt'),
                     cap_ig.replace('\n', ' | '), cap_fb.replace('\n', ' | '), cap_tt, fc, c['alt'], c['kw']])
        img_tag = f'<img src="file://{t}">' if t else '<div class="small">(preview added when the pictures are rendered)</div>'
        days_html += f'''
<div class="day">
 <h2>Day {en['day']} · {ds} · {e(en['theme'])}</h2>
 <div class="top">
  <div class="thumb">{img_tag}<div class="cap">{e(en['kind'])} · {e(en['asset'])}<br>File: {e(file_hint(en['asset']))}</div></div>
  <div style="flex:1">
   <p>{pills}</p>
   <table>
    <tr><th>Instagram</th><th>Facebook</th><th>TikTok</th></tr>
    <tr><td>{tm(en, 'ig')}<br>{FORMAT[en['slot']]['ig']}</td>
        <td>{tm(en, 'fb')}<br>{FORMAT[en['slot']]['fb']}</td>
        <td>{tm(en, 'tt')}<br>{FORMAT[en['slot']]['tt']}</td></tr>
   </table>
   <div class="lbl">Stories today ({STORY_TIMES})</div>
   <p class="small">Morning: {e(pic)} · Evening: {e(sticker)}</p>
  </div>
 </div>
 <div class="lbl">Instagram caption</div><div class="cap-box">{e(cap_ig)}</div>
 <div class="lbl">First comment (post it right after publishing)</div><div class="cap-box">{e(fc)}</div>
 <div class="cols">
  <div><div class="lbl">Facebook caption</div><div class="cap-box">{e(cap_fb)}</div></div>
  <div><div class="lbl">TikTok caption</div><div class="cap-box">{e(cap_tt)}</div>
   <div class="lbl">TikTok on-screen hook</div><p class="small">{e(c.get('tt') or c['hook'])}</p></div>
 </div>
 <div class="lbl">Alt text (paste into Instagram: Advanced settings, Write alt text; Facebook: Edit photo, Alternative text)</div><p>{e(c['alt'])}</p>
 <div class="lbl">Search keywords used in this post</div><p class="small">{e(c['kw'])}</p>
</div>'''
        for plat in ('ig', 'fb', 'tt'):
            if plat in en['platforms']:
                cap = {'ig': cap_ig, 'fb': cap_fb, 'tt': cap_tt}[plat]
                txt[plat] += f"==== Day {en['day']} · {ds} · {tm(en, plat)} · {en['asset']} ====\n{cap}\n"
                if plat == 'ig':
                    txt[plat] += f"\n[First comment]\n{fc}\n"
                txt[plat] += f"\n[Alt text]\n{c['alt']}\n\n"
    names = {'ig': 'Instagram', 'fb': 'Facebook', 'tt': 'TikTok'}
    for plat, body in txt.items():
        open(os.path.join(OUT, 'captions', f'Captions-{names[plat]}.txt'), 'w').write(f'ANJUM MART: {names[plat].upper()} CAPTIONS, 30 DAYS\n(copy and paste; the hashtags are already included)\n\n' + body)
    with open(os.path.join(OUT, 'captions.csv'), 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['day', 'date', 'weekday', 'theme', 'format', 'asset', 'instagram_time', 'facebook_time', 'tiktok_time',
                    'instagram_caption', 'facebook_caption', 'tiktok_caption', 'first_comment', 'alt_text', 'keywords'])
        w.writerows(rows)

    # overview table
    ov = '<table class="ov"><tr><th>Day</th><th>Date</th><th>Theme</th><th>Format</th><th>Asset</th><th>Post at (IG / FB / TikTok)</th></tr>'
    for en in ents:
        d = en['date']
        ov += f"<tr><td>{en['day']}</td><td>{en['weekday']} {d.day} {d.strftime('%b')}</td><td>{e(en['theme'])}</td><td>{en['kind']}</td><td><code>{en['asset']}</code></td><td>{tm(en, 'ig')} / {tm(en, 'fb')} / {tm(en, 'tt')}</td></tr>"
    ov += '</table>'

    n_posts = len(ents)
    n_days = max(e_['day'] for e_ in ents)
    n_reels = len([e_ for e_ in ents if e_['slot'] == 'reel'])
    n_eng = len([e_ for e_ in ents if e_['slot'] == 'engage'])
    n_feed = n_posts - n_reels - n_eng
    intro = f'''
<h2>How to use this calendar</h2>
<ol>
 <li><b>{n_days} days, {n_posts} posts.</b> Every day has one feed post: {n_feed} colour-story pictures, carousels and info pictures, plus {n_eng} engagement pictures (this or that, tag someone, comment a word) on quiet days. On {n_reels} days a reel goes out too (8:30 PM). Add two stories a day.</li>
 <li>Each page shows the picture or video poster, the file to upload, the captions for Instagram, Facebook and TikTok, the first comment, the alt text and the search keywords. Everything is copy and paste.</li>
 <li>File codes match the zips: <code>R-</code> reels (MP4), <code>K-</code> colour-story pictures (feed 4:5 and story 9:16), <code>C-</code> and <code>G-</code> carousels (slides in order), <code>I-</code> info pictures, <code>E-</code> engagement pictures.</li>
 <li><b>Times are starting guesses</b> (Pakistan time). After two weeks open Insights and move the posts to the hours your own followers are online.</li>
 <li><b>Engagement posts need you</b>: when someone comments 1 or 2 (or WATCH, JEWELLERY, PERFUME), reply by hand within the hour, and send the details on WhatsApp. Comments left unanswered hurt more than no post.</li>
 <li>Nothing in this calendar announces a discount. If you run a sale later, add a separate post with the real dates and only say what the shopper really gets.</li>
</ol>

<h2>Launch kit: before Day 1 (accounts are empty today)</h2>
<table>
<tr><th>Step</th><th>What to do</th></tr>
<tr><td>1. Profiles</td><td>Instagram: name "Anjum Mart | Watches &amp; Jewellery", the logo as the profile picture (<code>docs/brand</code> folder), bio and link from the checklist below, WhatsApp button, category. Facebook Page: same logo and cover (<code>docs/social</code>), WhatsApp as the action button. TikTok: create the account with the same name, logo and bio.</td></tr>
<tr><td>2. Link in bio</td><td>anjummart.com. WhatsApp +92 371 4661514 as the contact button on all three.</td></tr>
<tr><td>3. Fill the grid</td><td>Post Day 1 to Day 5 as written (most carry a picture and a reel), so the profile already shows a full grid when the first visitors from ads arrive.</td></tr>
<tr><td>4. Highlights</td><td>Create Delivery, COD, Men, Ladies and Jewellery highlights with the covers in <code>docs/social</code>, and put the story pictures (<code>-story-1080x1920</code>) inside.</td></tr>
<tr><td>5. Pin</td><td>Pin the launch reel (<code>R-ALL</code>) on Instagram and Facebook, and the "How to order" picture (<code>I-ORDER</code>) as a second pin.</td></tr>
<tr><td>6. Pixel and links</td><td>Meta Pixel on the store must show Purchase events before Phase 2 ads (see the Ads Playbook). Use <code>?utm_source=instagram</code>, <code>facebook</code> or <code>tiktok</code> on the link in each bio to see which platform sells.</td></tr>
<tr><td>7. First week</td><td>Follow and invite friends and customers, share the Facebook Page to your own profile, answer every comment and message the same day.</td></tr>
</table>

<h2>Instagram, Facebook and TikTok: what to do on each</h2>
<h3>Instagram</h3>
<ul><li>Reels get the widest reach: post the video, choose the cover frame (the poster shown here), add the caption, <b>paste the alt text</b>, tag the location (Multan or your city) and post the first comment with the extra hashtags.</li>
<li>Use 8 to 12 hashtags in the caption (already included), mixing the brand tag, the product tags and the shopping tags. Do not copy the same set on every post: the calendar rotates them.</li>
<li>Share every post to your Story with a sticker (poll, question) and reply to every comment within an hour.</li>
<li>Instagram search reads the profile <b>Name</b> field, the caption and the alt text, so keep "Anjum Mart | Watches &amp; Jewellery" as the name and write the product words in the caption.</li></ul>
<h3>Facebook</h3>
<ul><li>Post the same reel as a Facebook Reel and the carousels as an album. Use the shorter Facebook caption (it ends with the site and WhatsApp number). 2 to 4 hashtags are enough.</li>
<li>Pin the best post and keep the WhatsApp button as the Page action button.</li></ul>
<h3>TikTok</h3>
<ul><li>Upload the same MP4 (it carries our own original music, so there is no copyright claim). Keep the caption short; the first words are the hook shown here under "TikTok on-screen hook". Add 4 to 6 hashtags.</li>
<li>For carousels use TikTok <b>photo mode</b>: upload the slides in order and add a sound from the TikTok library.</li>
<li>Reply to comments with a video reply on questions about price and delivery.</li></ul>

<h2>Profile search checklist (SEO)</h2>
<table>
<tr><th>Platform</th><th>Field</th><th>Use</th></tr>
<tr><td>Instagram</td><td>Name (searchable)</td><td>Anjum Mart | Watches &amp; Jewellery</td></tr>
<tr><td>Instagram</td><td>Bio</td><td>Watches · Jewellery · Perfumes<br>Free delivery all Pakistan 🇵🇰 · Cash on Delivery<br>Order on WhatsApp 👇</td></tr>
<tr><td>Instagram</td><td>Category / contact</td><td>Jewelry &amp; Watches Store · WhatsApp button · website anjummart.com</td></tr>
<tr><td>Facebook</td><td>Intro</td><td>Timeless Style. Everyday Luxury. Watches, jewellery &amp; perfumes.</td></tr>
<tr><td>TikTok</td><td>Name / bio</td><td>Anjum Mart · Watches · Jewellery · Perfumes. Free delivery Pakistan. anjummart.com</td></tr>
<tr><td>All</td><td>Link</td><td>anjummart.com (optionally with ?utm_source=instagram / facebook / tiktok)</td></tr>
</table>
<h2 style="break-before:page">{n_days}-day overview ({n_posts} posts)</h2>{ov}
'''
    body = cover('Content Calendar and Captions', 'Instagram · Facebook · TikTok · 30 days',
                 f'Anjum Mart · 17 Nov to 27 Dec 2026 · {len(ents)} posts: {len([e_ for e_ in ents if e_["slot"] == "reel"])} reels, feed pictures and carousels, engagement posts<br>Watches · Jewellery · Perfumes · Free delivery all over Pakistan · Cash on Delivery')
    body += intro + days_html
    hp = os.path.join(OUT, 'calendar.html')
    open(hp, 'w').write(page(body, 'Anjum Mart Content Calendar'))
    to_pdf(hp, os.path.join(OUT, 'Content-Calendar-and-Captions.pdf'))


build()
