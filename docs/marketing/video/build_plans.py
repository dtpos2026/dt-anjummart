"""Writes one plan (plans/<id>.json) for each reel: 15 product reels, 4 collection reels and 1 brand reel.

Usage: python3 build_plans.py <cutouts_dir> <perfume_photos_dir> <out_plans_dir> [--preview]

Only catalogue facts are used: names, dial colours, "Day & Date Display" and similar details from the product listings,
the prices, Free Delivery All Pakistan and Cash on Delivery. No discounts, urgency, ratings or authenticity claims.
"""
import json
import os
import sys

CUT, PERF, OUT = [os.path.abspath(a) for a in sys.argv[1:4]]
PREVIEW = '--preview' in sys.argv[4:]  # marks every reel with a PREVIEW ribbon (use while the product photos are placeholders)
HERE = os.path.dirname(os.path.abspath(__file__))
LOGO = os.path.abspath(os.path.join(HERE, '..', '..', 'brand', 'editable', 'anjum-mart-logo-for-dark-background.svg'))
MARK = os.path.abspath(os.path.join(HERE, '..', '..', 'brand', 'icon', 'anjum-mart-logo-mark-transparent-1024.png'))
ASSETS = {'logo': 'file://' + LOGO, 'mark': 'file://' + MARK}

sys.path.insert(0, os.path.join(HERE, '..', 'content'))
from catalog import PRODUCTS, BY, THEMES  # noqa: E402



def src(p):
    kind, f = p[1], p[3]
    base = PERF if kind == 'photo' else CUT
    return 'file://' + os.path.join(base, f)


def item(pid):
    p = BY[pid]
    return {'id': pid, 'kind': p[1], 'src': src(p), 'eyebrow': p[4], 'title': p[5], 'sub': p[6], 'price': p[7]}


def write(plan):
    os.makedirs(OUT, exist_ok=True)
    plan.setdefault('fps', 30)
    plan['assets'] = ASSETS
    plan['cy'] = 940
    if PREVIEW:
        plan['preview'] = True
    json.dump(plan, open(os.path.join(OUT, plan['id'] + '.json'), 'w'), indent=1)


def product_reel(pid):
    bpm = 96
    style = 'gold' if BY[pid][2] == 'men' else 'noir'
    write({
        'id': 'R-' + pid, 'type': 'product', 'duration': 10.0, 'bpm': bpm, 'style': style, 'kick_from': 2.5,
        'product': item(pid),
        't': {'reveal': 1.25, 'text': 2.5, 'price': 5.0, 'shine2': 5.4, 'out': 7.3},
        'endStart': 7.5,
        'cues': [[0.15, 'sparkle'], [1.25, 'whoosh'], [1.25, 'boom'], [2.5, 'tick'], [5.0, 'tick'], [7.5, 'chime'], [7.5, 'boom']],
    })


def collection_reel(cid, title, eyebrow, sub, ids, bars_each):
    bpm = 108
    bar = 60.0 / bpm * 4
    intro = bar
    slot = bar * bars_each
    n = len(ids)
    end_start = intro + n * slot
    total = end_start + bar * 2
    slots = [{'start': intro + i * slot, 'end': intro + (i + 1) * slot} for i in range(n)]
    cues = [[0.15, 'sparkle'], [intro, 'riser'], [intro, 'boom']]
    for s in slots:
        cues.append([s['start'] + 0.05, 'whoosh'])
        cues.append([s['start'] + 0.05, 'tick'])
    cues += [[end_start, 'chime'], [end_start, 'boom']]
    write({
        'id': cid, 'type': 'collection', 'duration': round(total, 3), 'bpm': bpm, 'style': 'pulse', 'kick_from': intro,
        'coll': {'title': title, 'eyebrow': eyebrow, 'sub': sub},
        'items': [item(i) for i in ids], 'slots': slots, 'endStart': round(end_start, 3),
        't': {'introOut': intro - 0.4, 'chipsOut': end_start - 0.3},
        'cues': cues, 'rays': 0.5,
    })


def brand_reel():
    bpm = 108
    bar = 60.0 / bpm * 4
    words = [
        {'word': 'WATCHES', 'kind': 'watch', 'src': src(BY['M1'])},
        {'word': 'JEWELLERY', 'kind': 'jewellery', 'src': src(BY['J2'])},
        {'word': 'PERFUMES', 'kind': 'photo', 'src': src(BY['P2'])},
    ]
    slots = [{'start': bar * (1 + i), 'end': bar * (2 + i)} for i in range(3)]
    tag = bar * 4
    end_start = bar * 5
    cues = [[0.15, 'sparkle'], [bar, 'riser'], [bar, 'boom']]
    cues += [[s['start'] + 0.05, 'whoosh'] for s in slots[1:]]
    cues += [[tag, 'boom'], [tag, 'whoosh'], [end_start, 'chime'], [end_start, 'boom']]
    write({
        'id': 'R-BRAND', 'type': 'brand', 'duration': round(bar * 7, 3), 'bpm': bpm, 'style': 'pulse', 'kick_from': bar,
        'brand': {'line1': 'Timeless Style.', 'line2': 'Everyday Luxury.', 'sub': 'Watches · Jewellery · Perfumes'},
        'words': words, 'slots': slots, 'endStart': round(end_start, 3), 't': {'words': bar, 'tag': tag}, 'cues': cues,
    })


ALL_ORDER = ['M1', 'W1', 'P1', 'J1', 'M2', 'W2', 'P2', 'M4', 'W3', 'M3', 'J2', 'M6', 'M5', 'P3', 'W4']


def montage_reel(rid, order):
    """Fast colour-story montage: cream intro, one 2-beat slide per product, cream tagline, end card."""
    bpm = 120
    beat = 60.0 / bpm
    intro = beat * 4
    slot = beat * 2
    n = len(order)
    tag_start = intro + n * slot
    tag_len = beat * 4
    end_start = tag_start + tag_len
    total = end_start + 4.0
    slots = [{'start': 0.0, 'end': intro}]
    slots += [{'start': intro + i * slot, 'end': intro + (i + 1) * slot} for i in range(n)]
    slots.append({'start': tag_start, 'end': end_start})
    slides = []
    for pid in order:
        it = item(pid)
        it['theme'] = THEMES[pid]
        slides.append(it)
    cues = [[0.15, 'sparkle'], [intro - 0.5, 'riser']]
    for s in slots[1:-1]:
        cues.append([max(0.0, s['start'] - 0.22), 'whoosh'])
        cues.append([s['start'], 'tick'])
    cues += [[tag_start - 0.22, 'whoosh'], [tag_start, 'chime'], [tag_start, 'boom'], [end_start, 'chime'], [end_start, 'boom']]
    write({
        'id': rid, 'type': 'montage', 'duration': round(total, 3), 'bpm': bpm, 'style': 'pulse', 'kick_from': intro,
        'montage': {'intro': {'line1': 'Timeless Style.', 'line2': 'Everyday Luxury.', 'sub': 'Anjum Mart · New Collection'},
                    'tag': {'line1': 'Watches · Jewellery · Perfumes', 'line2': 'From Multan, Pakistan', 'line3': 'Delivery all over Pakistan'}},
        'slides': slides, 'slots': slots, 'endStart': round(end_start, 3), 'endPhone': '+92 371 4661514',
        'cues': cues,
    })


def main():
    for p in PRODUCTS:
        product_reel(p[0])
    collection_reel('R-MEN', "The Men's Collection", 'RUSTET · QUARTZ WATCHES', 'Gold · Silver · Black', ['M1', 'M2', 'M3', 'M6'], 1)
    collection_reel('R-WOMEN', 'The Ladies Collection', 'MOONSTON · CRYSTAL-STYLE', 'Black · Pink · Emerald', ['W1', 'W2', 'W3', 'W4'], 1)
    collection_reel('R-JEWELLERY', 'Bridal Jewellery', 'NECKLACE · EARRINGS · MAANG TIKKA', 'Complete Sets', ['J1', 'J2'], 2)
    collection_reel('R-PERFUMES', 'Anjum Perfumes', 'EAU DE PARFUM · 50 ML', 'Lady Aura · Oud Aura · Tea Rose', ['P1', 'P2', 'P3'], 1.5)
    brand_reel()
    montage_reel('R-ALL', ALL_ORDER)
    print('plans written to', OUT)


main()
