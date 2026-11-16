"""Builds the Meta Ads Playbook PDF (Facebook and Instagram ads, WhatsApp message ads first, Shop Now sales ads next).

Usage: python3 build_playbook.py <posts_final_dir> <posters_dir> <out_dir>
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from copytext import AD, PRODUCTS  # noqa: E402
from pdfcommon import page, cover, to_pdf, e  # noqa: E402

POSTS, POSTERS, OUT = [os.path.abspath(a) for a in sys.argv[1:4]]
os.makedirs(OUT, exist_ok=True)


def img(asset, w=22):
    if asset.startswith('R-'):
        f = os.path.join(POSTERS, asset + '.jpg')
    elif asset[0] in 'CG':
        f = os.path.join(POSTS, 'Carousels', asset, asset + '-slide-01.jpg')
    elif asset.startswith('K-'):
        f = os.path.join(POSTS, 'Color-Series', asset + '-feed-1080x1350.jpg')
    elif asset.startswith('I-'):
        f = os.path.join(POSTS, 'Info', asset + '-feed-1080x1350.jpg')
    else:
        f = os.path.join(POSTS, 'Feed-4x5', asset + '-feed-1080x1350.jpg')
    if os.path.exists(f):
        return f'<img src="file://{f}" style="width:{w}mm;border:1px solid #d4af37;display:block;margin:1pt 0">'
    return ''


def asset_cell(asset):
    return f'{img(asset)}<code>{asset}</code>'


def ad_set_table(rows):
    t = '<table><tr><th>Ad</th><th>Creative</th><th>Primary text</th><th>Headline</th></tr>'
    for n, (asset, pt, hl) in enumerate(rows, 1):
        t += f'<tr><td>{n}</td><td>{asset_cell(asset)}</td><td>{e(pt)}</td><td>{e(hl)}</td></tr>'
    return t + '</table>'


def block(cat):
    a = AD[cat]
    return ''.join(f'<li>{e(x)}</li>' for x in a['primary']), ' · '.join(e(h) for h in a['headlines']), e(a['desc'])


def write_ads_csv(sets, ad):
    import csv
    cta = 'Send WhatsApp message'
    with open(os.path.join(OUT, 'Ads-Copy-Sheet.csv'), 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['ad_set', 'ad_no', 'creative_code', 'creative_file', 'primary_text', 'headline', 'description', 'call_to_action', 'ad_name'])
        for aset, rows in sets.items():
            for n, (asset, pt, hl) in enumerate(rows, 1):
                kind = {'R': 'Reels/%s.mp4 (9:16)', 'C': 'Carousels/%s/ (slides in order)', 'G': 'Carousels/%s/ (slides in order)',
                        'K': 'Color-Series/%s-feed-1080x1350.jpg and -story-1080x1920.jpg', 'I': 'Info/%s-feed-1080x1350.jpg'}[asset[0]] % asset
                short = {'Women | IG': 'W_IG', 'Men | IG+FB': 'M_IGFB', 'Jewellery | IG+FB': 'J_IGFB', 'Perfumes | IG+FB': 'P_IGFB'}[aset]
                cat = {'Women | IG': 'women', 'Men | IG+FB': 'men', 'Jewellery | IG+FB': 'jewellery', 'Perfumes | IG+FB': 'perfume'}[aset]
                w.writerow([aset, n, asset, kind, pt, hl, ad[cat]['desc'], cta, f'AM_WA_{short}_{asset}_v1'])


def build():
    ad = AD
    br = ad['brand']
    women_rows = [('R-ALL', br['primary'][0], br['headlines'][0]),
                  ('R-W2', ad['women']['primary'][0], ad['women']['headlines'][0]),
                  ('R-W1', ad['women']['primary'][1], ad['women']['headlines'][1]),
                  ('G-LADIES', ad['women']['primary'][2], ad['women']['headlines'][2]),
                  ('K-W2', ad['women']['primary'][0], ad['women']['headlines'][0])]
    men_rows = [('R-ALL', br['primary'][0], br['headlines'][0]),
                ('R-M1', ad['men']['primary'][0], ad['men']['headlines'][0]),
                ('R-M2', ad['men']['primary'][1], ad['men']['headlines'][1]),
                ('G-MEN', ad['men']['primary'][2], ad['men']['headlines'][2]),
                ('K-M1', ad['men']['primary'][0], ad['men']['headlines'][0])]
    jew_rows = [('R-J2', ad['jewellery']['primary'][1], ad['jewellery']['headlines'][0]),
                ('R-JEWELLERY', ad['jewellery']['primary'][0], ad['jewellery']['headlines'][1]),
                ('C-JEWELLERY', ad['jewellery']['primary'][2], ad['jewellery']['headlines'][2]),
                ('K-J1', ad['jewellery']['primary'][0], ad['jewellery']['headlines'][0])]
    per_rows = [('R-PERFUMES', ad['perfume']['primary'][0], ad['perfume']['headlines'][0]),
                ('R-P1', ad['perfume']['primary'][1], ad['perfume']['headlines'][1]),
                ('R-P2', ad['perfume']['primary'][2], ad['perfume']['headlines'][2]),
                ('G-SCENT', ad['perfume']['primary'][2], ad['perfume']['headlines'][1])]
    write_ads_csv({'Women | IG': women_rows, 'Men | IG+FB': men_rows, 'Jewellery | IG+FB': jew_rows, 'Perfumes | IG+FB': per_rows}, ad)

    def copy_block(cat, title):
        pr, hl, ds = block(cat)
        return f'<h3>{title}</h3><div class="lbl">Primary text (use one per ad)</div><ol>{pr}</ol><div class="lbl">Headlines</div><p>{hl}</p><div class="lbl">Description</div><p>{ds}</p>'

    body = cover('Meta Ads Playbook', 'Facebook · Instagram · WhatsApp message ads, then Shop Now ads',
                 'Anjum Mart · November 2026<br>Reels and pictures from the Reels and Posts zips · budgets are suggestions: spend only what you can afford to lose')
    body += f'''
<h2>1. The plan at a glance</h2>
<table>
<tr><th>Phase</th><th>Days</th><th>Goal</th><th>Campaign type</th><th>What you learn</th></tr>
<tr><td><b>1. Test</b></td><td>1 to 10</td><td>Get real conversations and find which product and which video people react to</td><td>Messages: WhatsApp (conversion location: Messaging apps)</td><td>Cost per message, which creative wins, how many messages become orders</td></tr>
<tr><td><b>2. Sell</b></td><td>from day 11, once the Pixel Purchase event is verified</td><td>Orders on the website, "Shop Now"</td><td>Sales: Website, optimise for Purchases, catalog ads</td><td>Cost per order and return on ad spend</td></tr>
<tr><td><b>3. Scale</b></td><td>after 2 weeks of data</td><td>Spend more on what pays, keep winners fresh</td><td>Retargeting + new creatives</td><td>Which audiences and products to push</td></tr>
</table>
<div class="box"><b>Organic and paid work together.</b> The posting calendar keeps the page alive (people check a profile before they message). The same reels run as ads. Everyone who watches a reel or visits the site becomes a retargeting audience in Phase 2.</div>

<h2>1b. My picks: which creatives to run as ads first</h2>
<p>There is no sales data yet (the shop is new on Instagram, Facebook and TikTok), so these are the best bets, not proven winners. Start with them, then let the numbers decide.</p>
<table>
<tr><th>#</th><th>Creative</th><th>Why it goes first</th><th>Where</th></tr>
<tr><td>1</td><td><code>R-ALL</code> (reel, all products)</td><td>Shows the whole shop in under 30 seconds and ends on WhatsApp. The one video every visitor should see once.</td><td>Women and Men ad sets (first ad)</td></tr>
<tr><td>2</td><td><code>R-M1</code> gold and black watch</td><td>The strongest-looking men's piece, and Rs. 3,999 is an easy first order.</td><td>Men</td></tr>
<tr><td>3</td><td><code>R-W2</code> rose gold and pink watch</td><td>Clear colour, crystal-style sparkle, Rs. 2,999: the easiest ladies gift.</td><td>Women</td></tr>
<tr><td>4</td><td><code>R-J2</code> green and gold set</td><td>November and December is wedding and Mehndi season; a full set (necklace, earrings, maang tikka) is Rs. 1,999.</td><td>Jewellery</td></tr>
<tr><td>5</td><td><code>R-PERFUMES</code></td><td>Three 50 ml fragrances at one price; perfumes are an easy gift.</td><td>Perfumes</td></tr>
<tr><td>6</td><td>Pictures: <code>K-M1</code>, <code>K-W2</code>, <code>K-J1</code> and carousels <code>G-MEN</code>, <code>G-LADIES</code>, <code>G-SCENT</code>, <code>C-JEWELLERY</code></td><td>Posts that already did well organically are the cheapest ads (use "Boost" or create the ad from the existing post, so the likes and comments stay on it). Carousels let people compare colours before messaging.</td><td>Every ad set (one picture ad each)</td></tr>
</table>
<div class="box"><b>Rule of thumb:</b> after 3 to 4 days, switch off the ad with the highest cost per message and replace it with the next reel from the list (<code>R-M2</code>, <code>R-W1</code>, <code>R-M3</code>, <code>R-J1</code>, <code>R-P1</code>, <code>R-P2</code>). Never put more than 5 ads in one ad set.</div>

<h2>2. Phase 1 campaign structure</h2>
<p><b>One campaign, four ad sets, three to four ads in each.</b> Placements are set per ad set, so each product group gets its own ad set.</p>
<table>
<tr><th>Level</th><th>Name to use</th><th>Setting</th></tr>
<tr><td>Campaign</td><td><code>AM | WhatsApp | Test | Nov26</code></td><td>Objective: Engagement (or Sales) with conversion location <b>Messaging apps → WhatsApp</b>. Advantage campaign budget <b>off</b>.</td></tr>
<tr><td>Ad set 1</td><td><code>Women | IG</code></td><td>Pakistan · women · Instagram only (Feed, Stories, Reels)</td></tr>
<tr><td>Ad set 2</td><td><code>Men | IG+FB</code></td><td>Pakistan · men · Instagram + Facebook (Feed, Stories, Reels)</td></tr>
<tr><td>Ad set 3</td><td><code>Jewellery | IG+FB</code></td><td>Pakistan · women · Instagram + Facebook (wedding season)</td></tr>
<tr><td>Ad set 4</td><td><code>Perfumes | IG+FB</code></td><td>Pakistan · all genders · Instagram + Facebook</td></tr>
</table>
<h3>Budget: three tiers (suggestions, in Pakistani Rupees per day)</h3>
<table>
<tr><th>Tier</th><th>Ad sets</th><th>Per ad set</th><th>Total per day</th><th>10 days</th><th>Use when</th></tr>
<tr><td>Starter</td><td>2 (Women, Men)</td><td>Rs. 350</td><td>Rs. 700</td><td>Rs. 7,000</td><td>Very small budget: 3 ads per ad set, run 10 days</td></tr>
<tr><td>Standard</td><td>2 (Women, Men)</td><td>Rs. 700</td><td>Rs. 1,400</td><td>Rs. 14,000</td><td>Best balance for the first test</td></tr>
<tr><td>Growth</td><td>4 (all)</td><td>Rs. 700</td><td>Rs. 2,800</td><td>Rs. 28,000</td><td>When messages are turning into orders</td></tr>
</table>
<p class="small">Meta can spend up to about 25% more on a single day but never more than 7 times the daily budget in a week. In an account billed in dollars, convert at that day's rate. Pakistan card payments can add taxes or conversion charges: check Billing and keep those in your numbers.</p>

<h2>3. Break-even in one line</h2>
<div class="box"><b>Maximum cost per message = profit per order ÷ messages needed for one order.</b> Example: profit Rs. 1,000 per watch and 1 order from every 10 messages gives Rs. 100 per message. Track both numbers in the sheet at the end. Judge ads by cost per <b>order</b>, not only by cost per message.</div>

<h2>4. Audiences</h2>
<ul>
<li><b>Location:</b> Pakistan (all cities: delivery is free everywhere). Language: leave open (English and Urdu readers).</li>
<li><b>Age:</b> start broad. Suggested: women 21 to 45, men 21 to 50, perfumes 21 to 50. Narrow only after you see who messages.</li>
<li><b>Targeting:</b> use Advantage+ audience (broad) and give Meta suggestions only: watches, jewellery, perfume, online shopping, weddings. Interest names change, so search them inside Ads Manager.</li>
<li><b>Placements:</b> manual. Women: Instagram only. Men, jewellery, perfumes: Instagram + Facebook. Always include Reels and Stories because the videos are 9:16.</li>
<li><b>Later (Phase 2):</b> website visitors 30 days, Instagram and Facebook engagers 90 days, people who started a WhatsApp chat.</li>
</ul>

<h2>5. Which creative goes where</h2>
<h3>Ad set 1: Women | Instagram</h3>{ad_set_table(women_rows)}
<h3>Ad set 2: Men | Instagram + Facebook</h3>{ad_set_table(men_rows)}
<h3>Ad set 3: Jewellery | Instagram + Facebook</h3>{ad_set_table(jew_rows)}
<h3>Ad set 4: Perfumes | Instagram + Facebook</h3>{ad_set_table(per_rows)}
<div class="box">The other reels in the zip (<code>R-M3</code>, <code>R-M4</code>, <code>R-M5</code>, <code>R-M6</code>, <code>R-W3</code>, <code>R-W4</code>, <code>R-J1</code>, <code>R-P3</code>, <code>R-BRAND</code>, <code>R-MEN</code>, <code>R-WOMEN</code>) are the next tests: swap them in for the weakest ad after day 4. With the Starter budget use ads 1 to 3 in each ad set only. Every row is also in <code>Ads-Copy-Sheet.csv</code> (copy and paste into Ads Manager).</div>

<h2>6. How to set it up (Ads Manager, step by step)</h2>
<ol>
<li><code>business.facebook.com/adsmanager</code> → Create. Choose Engagement (or Sales) and <b>Messaging apps → WhatsApp</b>. Connect the WhatsApp number +92 371 4661514.</li>
<li>Create the four ad sets above (budget, 10 days, audience, manual placements).</li>
<li>In each ad: choose the Facebook Page and the Instagram account, upload the video or picture, paste the Primary text and Headline, set <b>Call to action: Send WhatsApp message</b>.</li>
<li><b>Welcome message</b>: <i>"Assalamualaikum! Anjum Mart mein khush aamdeed. Kaunsi watch, jewellery ya perfume pasand aayi? Apna naam aur city bata dein, hum order confirm kar dete hain."</i><br>Ice breakers: <i>Price kya hai? · Delivery kitne din mein hogi? · Cash on Delivery hai? · Order kaise karun?</i></li>
<li>For videos use the 9:16 file for Stories and Reels placements. For pictures use the 4:5 feed file and the 9:16 story file (customise by placement).</li>
<li>Review, publish, then <b>do not edit for 3 to 4 days</b>. Reply to every message within minutes with the quick replies from the earlier pack.</li>
</ol>

<h2>7. Ad copy library</h2>
{copy_block('women', 'Ladies watches')}{copy_block('men', "Men's watches")}{copy_block('jewellery', 'Bridal jewellery')}{copy_block('perfume', 'Perfumes')}{copy_block('brand', 'Brand')}
<div class="box warn"><b>Never write:</b> a discount, "limited time", "only today", ratings, reviews, "original", "best seller", delivery promises faster than the policy (3 to 5 working days to major cities, 5 to 7 to other areas, as estimates), or anything about returns. The Advance Cash Payment offer (Rs. 499 off) may be mentioned only when the payment method works and has been tested. A sale may be announced only with its real dates and discount.</div>

<h2>8. Reading the numbers</h2>
<table>
<tr><th>Number</th><th>Where</th><th>What it tells you</th><th>Rule</th></tr>
<tr><td>Hook rate (3-second plays ÷ impressions)</td><td>Video columns</td><td>Do the first seconds stop the scroll?</td><td>Below about 25%: change the first frames or the cover.</td></tr>
<tr><td>Cost per message</td><td>Results</td><td>Price of a WhatsApp chat</td><td>Compare with your break-even.</td></tr>
<tr><td>Messages to orders</td><td>Your sheet</td><td>Are the chats real buyers?</td><td>Keep the creative that brings orders, not just chats.</td></tr>
<tr><td>Frequency</td><td>Delivery</td><td>How often one person saw the ad</td><td>Above 3 in a week: add a new creative.</td></tr>
<tr><td>CTR</td><td>Clicks</td><td>Is the ad interesting?</td><td>Use it to rank creatives inside one ad set.</td></tr>
</table>
<ul>
<li><b>Day 4:</b> pause an ad that spent more than twice your break-even cost per message with no messages. Keep at least two ads per ad set.</li>
<li><b>Day 10:</b> keep the ads that brought orders; add two new creatives per ad set from the unused reels.</li>
<li><b>Scale:</b> raise a winning ad set by about 20% every 3 days instead of doubling it overnight, so Meta's learning does not restart.</li>
<li>The hook rate and frequency numbers above are common working guides, not Meta rules: adjust them to your own results.</li>
</ul>

<h2>9. Phase 2: Shop Now (Sales) ads</h2>
<div class="box warn"><b>Start only when</b> the Pixel shows <b>ViewContent, AddToCart, InitiateCheckout and Purchase</b> in Meta Events Manager (test with a demo order) and the Facebook and Instagram channel shows the catalog as Approved (15 products).</div>
<ol>
<li>Campaign <code>AM | Sales | Shop Now</code>: objective <b>Sales</b>, conversion location <b>Website</b>, optimisation event <b>Purchase</b>, call to action <b>Shop now</b>.</li>
<li>Meta advises about 50 optimisation events per ad set per week to leave the learning phase. With few orders, start by optimising for Add to cart or Initiate checkout, then move to Purchase.</li>
<li><b>Advantage+ catalog ads:</b> show the right product to the right person automatically from the synced catalog. Add one reel per category as the creative.</li>
<li><b>Retargeting</b> (separate ad set, a lower budget): ViewContent in the last 7 days, AddToCart in the last 3 days, excluding purchasers. Creative: the product reel they viewed, the "Free delivery · Cash on Delivery" info post and the "How to order" post.</li>
<li>A common split to start from (a heuristic, not a rule): about 70% new people, 20% retargeting, 10% new creative tests.</li>
</ol>

<h2>10. Creative specifications</h2>
<table>
<tr><th>Item</th><th>Spec used in the pack</th></tr>
<tr><td>Reels and Stories video</td><td>MP4 (H.264, AAC), 1080 × 1920 (9:16), 30 fps, 10 to 17 seconds, original music, text readable with the sound off</td></tr>
<tr><td>Feed pictures</td><td>1080 × 1350 (4:5) JPG</td></tr>
<tr><td>Story pictures</td><td>1080 × 1920 (9:16) JPG</td></tr>
<tr><td>Safe zone</td><td>Key text stays between about 270 px from the top and 1580 px (the app buttons sit below that). The reels follow this.</td></tr>
<tr><td>Links</td><td>Add <code>?utm_source=meta&amp;utm_medium=paid&amp;utm_campaign=...</code> to website links in Phase 2</td></tr>
</table>
<h3>Naming</h3>
<p><code>AM_WA_M_IGFB_R-M1_v1</code> = Anjum Mart, WhatsApp campaign, Men ad set, Instagram + Facebook, reel M1, version 1. Name every ad this way so the results are easy to read.</p>

<h2>11. Daily and weekly routine</h2>
<ul>
<li><b>Every day:</b> reply to messages within minutes; look at spend, messages, cost per message; write the day in the sheet.</li>
<li><b>Day 4 and day 7:</b> apply the pause rules above.</li>
<li><b>Every week:</b> upload two new creatives, retire the weakest, post the week's calendar items.</li>
<li><b>Every order:</b> check the payment method. If an order used the ADVANCE499 code but chose Cash on Delivery, ask for advance payment or remove the discount before dispatch.</li>
</ul>

<h2>12. Tracking sheet</h2>
<table>
<tr><th>Date</th><th>Ad set</th><th>Spend</th><th>Messages</th><th>Cost / message</th><th>Orders</th><th>Cost / order</th><th>Notes</th></tr>
''' + ''.join('<tr>' + '<td>&nbsp;</td>' * 8 + '</tr>' for _ in range(16)) + '''
</table>
'''
    hp = os.path.join(OUT, 'playbook.html')
    open(hp, 'w').write(page(body, 'Anjum Mart Meta Ads Playbook'))
    to_pdf(hp, os.path.join(OUT, 'Meta-Ads-Playbook.pdf'))


build()
