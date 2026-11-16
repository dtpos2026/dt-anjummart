"""6-week posting calendar (Instagram, Facebook, TikTok) starting Tue 17 Nov 2026.

Every day has one feed post (a colour-story picture, a carousel, an info picture or an engagement picture) and, on 27 of the 42 days, a reel as well.
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

DAYS = 42

# one feed post per day: (asset, copy key, theme)
FEED = [
    ('I-MEET', 'MEET', 'Meet Anjum Mart'),
    ('K-M1', 'K-M1', 'Colour story: gold & black'),
    ('K-W2', 'K-W2', 'Colour story: pink & rose gold'),
    ('C-MEN', 'MEN', "Men's collection carousel"),
    ('K-P1', 'K-P1', 'Colour story: Lady Aura'),
    ('I-ORDER', 'ORDER', 'How to order'),
    ('K-J1', 'K-J1', 'Colour story: silver & white jewellery'),
    ('G-MEN', 'GMEN', 'Guide: which dial suits you?'),
    ('K-M7', 'K-M7', 'Colour story: ice blue'),
    ('K-W5', 'K-W5', 'Colour story: golden shine'),
    ('C-WOMEN', 'WOMEN', 'Ladies collection carousel'),
    ('I-DELIVERY', 'DELIVERY', 'Free delivery and COD'),
    ('K-P2', 'K-P2', 'Colour story: Oud Aura'),
    ('G-LADIES', 'GLADIES', 'Guide: pink, emerald, black or gold?'),
    ('K-J2', 'K-J2', 'Colour story: green & gold jewellery'),
    ('K-M4', 'K-M4', 'Colour story: green dial'),
    ('C-JEWELLERY', 'JEWELLERY', 'Bridal jewellery carousel'),
    ('K-W3', 'K-W3', 'Colour story: pink-lavender'),
    ('I-WEDDING', 'WEDDING', 'Wedding season: complete the look'),
    ('K-M6', 'K-M6', 'Colour story: ivory & gold'),
    ('G-SCENT', 'GSCENT', 'Guide: find your fragrance'),
    ('K-P3', 'K-P3', 'Colour story: Tea Rose'),
    ('I-GIFTHER', 'GIFTHER', 'Gift ideas for her'),
    ('K-M2', 'K-M2', 'Colour story: royal blue'),
    ('C-PERFUMES', 'PERFUMES', 'Perfumes carousel'),
    ('K-M10', 'K-M10', 'Colour story: white textured dial'),
    ('I-FAQ', 'FAQ', 'Your questions, answered'),
    ('K-W4', 'K-W4', 'Colour story: jade'),
    ('K-M3', 'K-M3', 'Colour story: all-black'),
    ('I-GIFTHIM', 'GIFTHIM', 'Gift ideas for him'),
    ('K-W1', 'K-W1', 'Colour story: the flower bracelet'),
    ('K-M9', 'K-M9', 'Colour story: vertical texture'),
    ('K-M8', 'K-M8', 'Colour story: royal blue classic'),
    ('K-M5', 'K-M5', 'Colour story: emerald'),
    ('I-BRAND', 'BRAND', 'Timeless Style. Everyday Luxury.'),
]
# five or more engagement pictures take the feed slot of quiet days (no reel)
ENGAGE = {5: ('E-THIS1', 'ETHIS1', 'Engagement: gold or blue?'), 12: ('E-WORD', 'EWORD', 'Engagement: comment a word'),
          19: ('E-THIS2', 'ETHIS2', 'Engagement: pink or golden shine?'), 26: ('E-TAG', 'ETAG', 'Engagement: tag someone'),
          33: ('E-THIS3', 'ETHIS3', 'Engagement: Lady Aura or Tea Rose?'), 38: ('E-THIS4', 'ETHIS4', 'Engagement: black or ice blue?'),
          40: ('E-THIS5', 'ETHIS5', 'Engagement: silver or green & gold?')}
REELS = [
    ('R-ALL', 'ALL', 'Reel: everything in one place (launch reel)'),
    ('R-BRAND', 'BRAND', 'Reel: brand film'),
    ('R-M1', 'M1', "Reel: men's gold & black"),
    ('R-WOMEN', 'WOMEN', 'Reel: ladies collection'),
    ('R-W2', 'W2', 'Reel: rose gold & pink'),
    ('R-MEN', 'MEN', "Reel: men's collection"),
    ('R-P1', 'P1', 'Reel: Lady Aura'),
    ('R-J2', 'J2', 'Reel: green & gold jewellery'),
    ('R-M2', 'M2', "Reel: men's royal blue"),
    ('R-W5', 'W5', 'Reel: golden shine'),
    ('R-M7', 'M7', "Reel: men's ice blue"),
    ('R-JEWELLERY', 'JEWELLERY', 'Reel: bridal jewellery'),
    ('R-M3', 'M3', "Reel: men's all-black"),
    ('R-W1', 'W1', 'Reel: flower bracelet'),
    ('R-P2', 'P2', 'Reel: Oud Aura'),
    ('R-MEN2', 'MEN', "Reel: more men's watches"),
    ('R-M8', 'M8', "Reel: royal blue classic"),
    ('R-J1', 'J1', 'Reel: silver & white jewellery'),
    ('R-W3', 'W3', 'Reel: pink-lavender dial'),
    ('R-PERFUMES', 'PERFUMES', 'Reel: perfumes'),
    ('R-M9', 'M9', "Reel: black vertical texture"),
    ('R-M4', 'M4', "Reel: men's green dial"),
    ('R-W4', 'W4', 'Reel: emerald two-tone'),
    ('R-M10', 'M10', 'Reel: white textured dial'),
    ('R-P3', 'P3', 'Reel: Tea Rose'),
    ('R-M6', 'M6', "Reel: men's white dial"),
    ('R-M5', 'M5', "Reel: men's emerald"),
]
# days without a reel
NO_REEL = [3, 5, 10, 12, 14, 17, 19, 22, 24, 26, 29, 31, 33, 36, 40]


def _kind(asset):
    return {'R': 'Reel', 'K': 'Colour-series picture', 'C': 'Carousel', 'G': 'Guide carousel', 'I': 'Info picture', 'E': 'Engagement picture'}[asset[0]]


def entries():
    out = []
    reel_days = [d for d in range(DAYS) if d not in NO_REEL]
    assert len(reel_days) == len(REELS), (len(reel_days), len(REELS))
    reel_at = dict(zip(reel_days, REELS))
    n = 0
    feed_i = 0
    for off in range(DAYS):
        d = START + datetime.timedelta(days=off)
        day = dict(day=off + 1, date=d, weekday=d.strftime('%a'))
        if off in ENGAGE:
            parts = [(ENGAGE[off], 'engage')]
        else:
            parts = [(FEED[feed_i], 'carousel' if FEED[feed_i][0][0] in 'CG' else 'feed')]
            feed_i += 1
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
    print(len(es), 'posts in', DAYS, 'days; feed items used', len([e for e in es if e['slot'] in ('feed', 'carousel')]), 'of', len(FEED))
    # a feed post and a reel on the same day must not be the same product
    by_day = {}
    for e in es:
        by_day.setdefault(e['day'], []).append(e)
    for dday, items in by_day.items():
        codes = [i['key'].replace('K-', '') for i in items]
        if len(set(codes)) < len(codes):
            print('same product twice on day', dday, codes)
