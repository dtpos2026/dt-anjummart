"""Assembles the two zips from the work folder:  Anjum-Mart-ADS-Package.zip  and  Anjum-Mart-POSTING-Package.zip

Usage: python3 package.py <work_dir> <out_dir> [--preview]
"""
import os
import shutil
import subprocess
import sys

WORK, OUT = [os.path.abspath(a) for a in sys.argv[1:3]]
PREVIEW = '--preview' in sys.argv[3:]
tag = '-PREVIEW' if PREVIEW else ''

ADS_REELS = ['R-ALL', 'R-M1', 'R-W2', 'R-J2', 'R-PERFUMES', 'R-M2', 'R-W1', 'R-M3', 'R-J1', 'R-P1', 'R-P2']
ADS_PICS = ['K-M1', 'K-W2', 'K-J1', 'K-P1']
ADS_CAROUSELS = ['G-MEN', 'G-LADIES', 'G-SCENT', 'C-JEWELLERY']


def cp(src, dst):
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    if os.path.isdir(src):
        shutil.copytree(src, dst, dirs_exist_ok=True)
    elif os.path.exists(src):
        shutil.copy2(src, dst)
    else:
        print('missing', src)


def pics(root, kind, code, dst_root):
    folder = {'K': 'Color-Series', 'E': 'Engagement', 'I': 'Info'}[kind]
    for fmt in ('feed-1080x1350', 'story-1080x1920'):
        cp(f'{WORK}/posts/final/{folder}/{code}-{fmt}.jpg', f'{dst_root}/{folder}/{code}-{fmt}.jpg')


def build(name, fill, readme, urdu=''):
    d = os.path.join(OUT, name + tag)
    shutil.rmtree(d, ignore_errors=True)
    os.makedirs(d)
    fill(d)
    open(os.path.join(d, 'README.txt'), 'w').write(readme)
    if urdu:
        open(os.path.join(d, 'START-HERE-Roman-Urdu.txt'), 'w').write(urdu)
    z = os.path.join(OUT, name + tag + '.zip')
    if os.path.exists(z):
        os.remove(z)
    subprocess.run(['zip', '-qr', z, os.path.basename(d)], cwd=OUT, check=True)
    print('zip', z, round(os.path.getsize(z) / 1e6, 1), 'MB')


def ads(d):
    for r in ADS_REELS:
        cp(f'{WORK}/reels/{r}.mp4', f'{d}/Reels/{r}.mp4')
        cp(f'{WORK}/posters/{r}.jpg', f'{d}/Reels/covers/{r}-cover.jpg')
    for k in ADS_PICS:
        pics(d, 'K', k, f'{d}/Pictures')
    for c in ADS_CAROUSELS:
        cp(f'{WORK}/posts/final/Carousels/{c}', f'{d}/Carousels/{c}')
    cp(f'{WORK}/playbook/Meta-Ads-Playbook.pdf', f'{d}/Meta-Ads-Playbook.pdf')
    cp(f'{WORK}/playbook/Ads-Copy-Sheet.csv', f'{d}/Ads-Copy-Sheet.csv')


def posting(d):
    for f in sorted(os.listdir(f'{WORK}/reels')):
        if f.endswith('.mp4'):
            cp(f'{WORK}/reels/{f}', f'{d}/Reels/{f}')
            cp(f'{WORK}/posters/{f[:-4]}.jpg', f'{d}/Reels/covers/{f[:-4]}-cover.jpg')
    base = f'{WORK}/posts/final'
    for sub in ('Color-Series', 'Carousels', 'Info', 'Engagement', 'Feed-4x5', 'Story-9x16'):
        cp(f'{base}/{sub}', f'{d}/Posts/{sub}')
    cp(f'{WORK}/calendar/Content-Calendar-and-Captions.pdf', f'{d}/Content-Calendar-and-Captions.pdf')
    cp(f'{WORK}/calendar/captions', f'{d}/Captions')
    cp(f'{WORK}/calendar/captions.csv', f'{d}/Captions/captions-all.csv')


PRE = ('THIS IS A PREVIEW. The reels carry a red PREVIEW ribbon and show placeholder watch and jewellery photos. Do not post them.\n\n' if PREVIEW else '')

ADS_README = PRE + '''ANJUM MART: ADS PACKAGE (Facebook and Instagram ads)

1. Open Meta-Ads-Playbook.pdf. Section 1b says which creatives to run first and why; section 5 maps each creative to an ad set; section 6 is the
   Ads Manager click-by-click setup.
2. Ads-Copy-Sheet.csv has every ad row: ad set, file to upload, primary text, headline, description, call to action and the ad name.
3. Reels/ holds the 9:16 MP4 reels (covers in Reels/covers). Pictures/ holds feed (4:5) and story (9:16) pictures. Carousels/ holds the slides in order.
4. Start with the Starter or Standard budget in the playbook. Do not edit the ads for the first 3 to 4 days.
5. Nothing here promises a discount, a rating or a delivery time. Delivery is free all over Pakistan and Cash on Delivery is available; keep it that way in anything you add.
'''
POST_README = PRE + '''ANJUM MART: POSTING PACKAGE (Instagram, Facebook, TikTok)

1. Open Content-Calendar-and-Captions.pdf. It has the launch kit (profile setup before Day 1), the 30-day plan (56 posts) and one page per post with the picture,
   the file to upload, captions for Instagram, Facebook and TikTok, the first comment, alt text and search keywords.
2. Captions/ has the same captions as plain text (Instagram, Facebook, TikTok) and one CSV with everything, for copy and paste.
3. Reels/ (21 MP4, 9:16, own original music) with covers. Posts/Color-Series (a picture for every product, feed and story), Posts/Carousels (collections and guides),
   Posts/Info (how to order, delivery, wedding season, FAQ, gifts, brand, Meet Anjum Mart), Posts/Engagement (this or that, tag someone, comment a word),
   Posts/Feed-4x5 and Posts/Story-9x16 (plain product pictures).
4. Post the reels on Instagram, Facebook and TikTok. Use TikTok photo mode for the carousels.
5. Engagement posts need you to answer every comment by hand. The times in the calendar are starting guesses (Pakistan time): check Insights after two weeks.
'''

ADS_UR = PRE + '''ADS PACKAGE: pehle ye parhein (Roman Urdu)

1. Meta-Ads-Playbook.pdf kholein. Section 1b mein likha hai kaunsi reel/post se ads shuru karni hain aur kyun (R-ALL, R-M1, R-W2, R-J2, R-PERFUMES).
2. Ads-Copy-Sheet.csv mein har ad ki line hai: kaunsi file upload karni hai, primary text, headline, description. Copy-paste karein.
3. Phase 1: WhatsApp message ads. Rs. 350 ya Rs. 700 per ad set se shuru karein. 3-4 din tak ads ko edit na karein.
4. Phase 2 (Shop Now ads) tab karein jab Meta Pixel ka Purchase event verify ho jaye.
5. Sirf wohi likhein jo sach hai: free delivery all Pakistan aur Cash on Delivery. Koi discount, rating ya review apni taraf se na likhein.
'''
POST_UR = PRE + '''POSTING PACKAGE: pehle ye parhein (Roman Urdu)

1. Content-Calendar-and-Captions.pdf kholein. Pehle "Launch kit" (profile setup) karein, phir Day 1 se roz ki post lagayein.
2. Har din ek feed post, 21 din ek reel bhi, aur 5 din engagement post (this or that, tag someone, comment a word). Roz 2 stories.
3. Har page par picture/reel, upload ki file ka naam, Instagram/Facebook/TikTok ke captions, hashtags, first comment, alt text aur SEO keywords hain.
4. Captions folder mein wohi captions plain text mein hain, copy-paste ke liye.
5. Engagement posts par aane wale comments ka khud jawab dein (1 ghante ke andar) aur details WhatsApp par bhejein.
6. Time sirf shuru ka andaza hai (Pakistan time). 2 hafte baad Insights dekh kar apne followers ke online time par shift karein.
'''
build('Anjum-Mart-ADS-Package', ads, ADS_README, ADS_UR)
build('Anjum-Mart-POSTING-Package', posting, POST_README, POST_UR)
