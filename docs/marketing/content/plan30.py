"""30-day posting calendar (Instagram, Facebook, TikTok) starting Tue 17 Nov 2026.

Every day has one feed post (a colour-series picture, a carousel or an info picture) and, on 21 of the 30 days, a reel as well.
On five of the reel-free days an engagement post (this-or-that, tag someone, comment a word) goes out in the evening.
Times are starting guesses in Pakistan time; check Insights after two weeks and move the posts to the hours your own followers are online.
Asset codes: R- reel, K- colour-series picture, C-/G- carousel, I- info picture, E- engagement picture.
"""
import datetime

START = datetime.date(2026, 11, 17)

# (platform: time) per kind of post
T = {
    'reel': {'ig': '8:30 PM', 'fb': '9:00 PM', 'tt': '9:30 PM'},
    'feed': {'ig': '1:00 PM', 'fb': '1:30 PM'},
    'carousel': {'ig': '1:00 PM', 'fb': '1:30 PM', 'tt': '2:00 PM'},
    'engage': {'ig': '7:00 PM', 'fb': '7:15 PM'},
}
STORY_TIMES = '11:00 AM and 6:00 PM'
TIMES = {'ig': '1:00 PM / 8:30 PM', 'fb': '1:30 PM / 9:00 PM', 'tt': '9:30 PM', 'story': STORY_TIMES}

# day offset -> (feed asset, copy key, theme)   (asset, key, theme)
FEED = [
    ('I-MEET', 'MEET', 'Meet Anjum Mart'),
    ('K-M1', 'K-M1', "Colour story: gold & black"),
    ('K-W2', 'K-W2', 'Colour story: pink & rose gold'),
    ('C-MEN', 'MEN', "Men's collection carousel"),
    ('K-P1', 'K-P1', 'Colour story: Lady Aura'),
    ('I-ORDER', 'ORDER', 'How to order'),
    ('K-J1', 'K-J1', 'Colour story: silver & white jewellery'),
    ('G-MEN', 'GMEN', 'Guide: which dial suits you?'),
    ('K-M3', 'K-M3', 'Colour story: all-black'),
    ('K-W1', 'K-W1', 'Colour story: the flower bracelet'),
    ('C-WOMEN', 'WOMEN', 'Ladies collection carousel'),
    ('I-DELIVERY', 'DELIVERY', 'Free delivery and COD'),
    ('K-P2', 'K-P2', 'Colour story: Oud Aura'),
    ('G-LADIES', 'GLADIES', 'Guide: pink, lavender or emerald?'),
    ('K-J2', 'K-J2', 'Colour story: green & gold jewellery'),
    ('K-M4', 'K-M4', 'Colour story: green dial'),
    ('C-JEWELLERY', 'JEWELLERY', 'Bridal jewellery carousel'),
    ('K-W3', 'K-W3', 'Colour story: lavender'),
    ('I-WEDDING', 'WEDDING', 'Wedding season: complete the look'),
    ('K-M6', 'K-M6', 'Colour story: ivory & gold'),
    ('G-SCENT', 'GSCENT', 'Guide: find your fragrance'),
    ('K-P3', 'K-P3', 'Colour story: Tea Rose'),
    ('I-GIFTHER', 'GIFTHER', 'Gift ideas for her'),
    ('K-M2', 'K-M2', 'Colour story: royal blue'),
    ('C-PERFUMES', 'PERFUMES', 'Perfumes carousel'),
    ('K-M5', 'K-M5', 'Colour story: emerald'),
    ('I-FAQ', 'FAQ', 'Your questions, answered'),
    ('K-W4', 'K-W4', 'Colour story: jade'),
    ('I-GIFTHIM', 'GIFTHIM', 'Gift ideas for him'),
    ('I-BRAND', 'BRAND', 'Timeless Style. Everyday Luxury.'),
]
# reel-free days get no reel
NO_REEL = [3, 5, 10, 12, 17, 19, 24, 26, 29]
REELS = [
    ('R-ALL', 'ALL', 'Reel: everything in one place (launch reel)'),
    ('R-BRAND', 'BRAND', 'Reel: brand film'),
    ('R-M1', 'M1', "Reel: men's gold & black"),
    ('R-WOMEN', 'WOMEN', 'Reel: ladies collection'),
    ('R-M2', 'M2', "Reel: men's royal blue"),
    ('R-J2', 'J2', 'Reel: green & gold jewellery'),
    ('R-W2', 'W2', 'Reel: rose gold & pink'),
    ('R-P1', 'P1', 'Reel: Lady Aura'),
    ('R-MEN', 'MEN', "Reel: men's collection"),
    ('R-M3', 'M3', "Reel: men's all-black"),
    ('R-J1', 'J1', 'Reel: silver & white jewellery'),
    ('R-W1', 'W1', 'Reel: flower bracelet'),
    ('R-P2', 'P2', 'Reel: Oud Aura'),
    ('R-JEWELLERY', 'JEWELLERY', 'Reel: bridal jewellery'),
    ('R-M4', 'M4', "Reel: men's green dial"),
    ('R-W3', 'W3', 'Reel: lavender dial'),
    ('R-PERFUMES', 'PERFUMES', 'Reel: perfumes'),
    ('R-M5', 'M5', "Reel: men's emerald"),
    ('R-W4', 'W4', 'Reel: emerald two-tone'),
    ('R-M6', 'M6', "Reel: men's white dial"),
    ('R-P3', 'P3', 'Reel: Tea Rose'),
]
ENGAGE = {5: ('E-THIS1', 'ETHIS1', 'Engagement: gold or blue?'), 12: ('E-WORD', 'EWORD', 'Engagement: comment a word'),
          19: ('E-THIS2', 'ETHIS2', 'Engagement: pink or lavender?'), 24: ('E-THIS3', 'ETHIS3', 'Engagement: Lady Aura or Tea Rose?'),
          26: ('E-TAG', 'ETAG', 'Engagement: tag someone')}


def _kind(asset):
    return {'R': 'Reel', 'K': 'Colour-series picture', 'C': 'Carousel', 'G': 'Guide carousel', 'I': 'Info picture', 'E': 'Engagement picture'}[asset[0]]


def entries():
    out = []
    reel_days = [d for d in range(30) if d not in NO_REEL]
    assert len(reel_days) == len(REELS), (len(reel_days), len(REELS))
    reel_at = dict(zip(reel_days, REELS))
    n = 0
    for off in range(30):
        d = START + datetime.timedelta(days=off)
        day = dict(day=off + 1, date=d, weekday=d.strftime('%a'))
        parts = [(FEED[off], 'carousel' if FEED[off][0][0] in 'CG' else 'feed')]
        if off in ENGAGE:
            parts.append((ENGAGE[off], 'engage'))
        if off in reel_at:
            parts.append((reel_at[off], 'reel'))
        for (asset, key, theme), kind in parts:
            n += 1
            t = T[kind]
            out.append(dict(day, no=n, theme=theme, asset=asset, key=key, kind=_kind(asset), slot=kind,
                            platforms=list(t.keys()), times=t))
    return out


if __name__ == '__main__':
    es = entries()
    print(len(es), 'posts in 30 days')
    # a feed post and a reel on the same day must not be the same product
    by_day = {}
    for e in es:
        by_day.setdefault(e['day'], []).append(e)
    for dday, items in by_day.items():
        codes = [i['key'].replace('K-', '') for i in items]
        if len(set(codes)) < len(codes):
            print('same product twice on day', dday, codes)
