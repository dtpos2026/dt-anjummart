"""Shared product table: id, kind, category, cut-out or photo file, eyebrow, title, subtitle, price."""

W_EYE = "LADIES WATCH · MOONSTON"
M_EYE = "MEN'S WATCH · RUSTET"

# id, kind, cat, cut/photo, eyebrow, title, sub, price
PRODUCTS = [
    ('M1', 'watch', 'men', 'M1.png', M_EYE, 'Gold · Black Dial', 'Roman Numerals · Day & Date Display', 'Rs. 3,999'),
    ('M2', 'watch', 'men', 'M2.png', M_EYE, 'Royal Blue Dial', 'Gold & Silver · Day & Date Display', 'Rs. 3,999'),
    ('M3', 'watch', 'men', 'M3.png', M_EYE, 'All-Black Watch', 'Black Dial · Day & Date Display', 'Rs. 3,999'),
    ('M4', 'watch', 'men', 'M4.png', M_EYE, 'Silver · Green Dial', 'Roman Numerals · Day & Date Display', 'Rs. 3,999'),
    ('M5', 'watch', 'men', 'M5.png', M_EYE, 'Silver · Emerald Dial', 'Green Sunburst · Day & Date Display', 'Rs. 3,999'),
    ('M6', 'watch', 'men', 'M6.png', M_EYE, 'Two-Tone · White Dial', 'Gold & Silver Quartz Watch', 'Rs. 3,999'),
    ('M7', 'watch', 'men', 'M7.png', M_EYE, 'Ice Blue · Oyster Series', 'Full Silver Steel · Day & Date Display', 'Rs. 4,000'),
    ('M8', 'watch', 'men', 'M8.png', 'RUSTET · QUARTZ WATCH', 'Royal Blue · Classic Series', 'Silver Steel · Day & Date Display', 'Rs. 4,450'),
    ('M9', 'watch', 'men', 'M9.png', M_EYE, 'Black Vertical Texture', 'Gold Bezel · Two-Tone Bracelet', 'Rs. 3,990'),
    ('M10', 'watch', 'men', 'M10.png', 'RUSTET · QUARTZ WATCH', 'White Textured Dial', 'XII Roman Numeral · Two-Tone', 'Rs. 4,000'),
    ('W1', 'watch', 'women', 'W1.png', W_EYE, 'Black Ladies Watch', 'Dark Green Dial · Crystal Flower Design', 'Rs. 2,499'),
    ('W2', 'watch', 'women', 'W2.png', W_EYE, 'Rose Gold · Pink Dial', 'Crystal-Style Luxury Design', 'Rs. 2,999'),
    ('W3', 'watch', 'women', 'W3.png', W_EYE, 'Pink-Lavender Dial', 'Crystal-Style Studded Bracelet', 'Rs. 2,999'),
    ('W4', 'watch', 'women', 'W4.png', W_EYE, 'Two-Tone · Emerald Dial', 'Crystal-Style Bezel', 'Rs. 2,999'),
    ('W5', 'watch', 'women', 'W5.png', 'LADIES WATCH · RUSTET', 'Golden Shine Dial', 'Stone Markers · Two-Tone Chain', 'Rs. 4,000'),
    ('J1', 'jewellery', 'jewellery', 'J1.png', 'BRIDAL JEWELLERY SET', 'Silver & White Mirror Stone', 'Necklace · Earrings · Maang Tikka', 'Rs. 1,999'),
    ('J2', 'jewellery', 'jewellery', 'J2.png', 'BRIDAL JEWELLERY SET', 'Green & Gold Traditional', 'Necklace · Earrings · Maang Tikka', 'Rs. 1,999'),
    ('P1', 'photo', 'perfume', 'lady-portrait.jpg', 'EAU DE PARFUM · 50 ML', 'Lady Aura', 'Premium Floral Fragrance · For Women', 'Rs. 3,450'),
    ('P2', 'photo', 'perfume', 'oud-portrait.jpg', 'EAU DE PARFUM · 50 ML', 'Oud Aura', 'Premium Oud Fragrance · Unisex', 'Rs. 3,450'),
    ('P3', 'photo', 'perfume', 'tea-portrait.jpg', 'EAU DE PARFUM · 50 ML', 'Tea Rose', 'Premium Fragrance Oil · For Women', 'Rs. 3,450'),
]
# store handle of each cut-out piece: the first (white background) photo of the product is the source of the cut-out
HANDLES = {
    'M1': 'rustet-gold-mens-watch-black-dial-roman-numerals',
    'M2': 'rustet-gold-silver-mens-watch-royal-blue-dial',
    'M3': 'rustet-all-black-mens-watch-black-dial',
    'M4': 'rustet-silver-mens-watch-green-dial-roman-numerals',
    'M5': 'rustet-silver-mens-watch-emerald-green-dial',
    'M6': 'rustet-two-tone-gold-silver-mens-watch-white-dial',
    'M7': 'watch-1',
    'M8': 'watch',
    'M9': 'mens-watch',
    'M10': 'watch-2',
    'W1': 'moonston-black-ladies-watch-dark-green-dial-crystal-flower-design',
    'W2': 'moonston-rose-gold-ladies-watch-pink-dial-crystal-style-luxury',
    'W3': 'moonston-rose-gold-ladies-watch-pink-dial-luxury-crystal-style',
    'W4': 'moonston-two-tone-ladies-watch-emerald-green-dial',
    'W5': 'watches',
    'J1': 'silver-white-mirror-stone-jewellery-set-necklace-earrings-maang-tikka',
    'J2': 'green-gold-traditional-bridal-jewellery-set-necklace-earrings-maang-tikka',
}
BY = {p[0]: p for p in PRODUCTS}


# Colour story: one colour world per product (the reel and the colour posts). word = big watermark word behind the product.
# bg = (top, bottom) gradient, dark = True for a light background with dark text, acc = accent for the small line and the price.
THEMES = {
    'M1': dict(word='GOLD', bg=('#7a5514', '#241706'), acc='#f1d98a', dark=False, hook='Black dial. Gold presence.'),
    'M2': dict(word='ROYAL', bg=('#2350b0', '#0b1c4d'), acc='#f1d98a', dark=False, hook='Royal blue, two-tone.'),
    'M3': dict(word='NOIR', bg=('#4a4a4e', '#0d0d0f'), acc='#e0e0e0', dark=False, hook='All black. All attitude.'),
    'M4': dict(word='GREEN', bg=('#23805a', '#0a2e20'), acc='#f1d98a', dark=False, hook='A green dial that talks.'),
    'M5': dict(word='EMERALD', bg=('#15906a', '#06382b'), acc='#f1d98a', dark=False, hook='Emerald. Textured. Polished.'),
    'M6': dict(word='IVORY', bg=('#f6ecd4', '#d4b36a'), acc='#7a5514', dark=True, hook='Clean dial. Warm gold bezel.'),
    'W1': dict(word='BLOOM', bg=('#22696b', '#0a2a2c'), acc='#f6e4a0', dark=False, hook='A bracelet like jewellery.'),
    'W2': dict(word='ROSE', bg=('#f0a0b8', '#b02e58'), acc='#fff3c4', dark=False, hook='Pink dial. Rose-gold glow.'),
    'W3': dict(word='LILAC', bg=('#c4aaf0', '#6d41ae'), acc='#fff3c4', dark=False, hook='Pink-lavender. Serious sparkle.'),
    'W4': dict(word='JADE', bg=('#238c70', '#0a3f37'), acc='#f6e4a0', dark=False, hook='Emerald dial, rose-gold accents.'),
    'J1': dict(word='SILVER', bg=('#e4e8ef', '#8f9bb0'), acc='#4b3a10', dark=True, hook='Mirror stones, pearl-white drops.'),
    'J2': dict(word='MEHNDI', bg=('#23864f', '#0a3b24'), acc='#f1d98a', dark=False, hook='Emerald green meets gold.'),
    'P1': dict(word='LADY', bg=('#b3223a', '#4d0c17'), acc='#f6e4a0', dark=False, hook='Meet Lady Aura.'),
    'P2': dict(word='OUD', bg=('#333333', '#060606'), acc='#f1d98a', dark=False, hook='Oud, for everyone.'),
    'P3': dict(word='ROSE', bg=('#cc3a56', '#600f24'), acc='#f6e4a0', dark=False, hook='Tea Rose: soft, red, 50 ml.'),
    'M7': dict(word='ICE', bg=('#6cc3e6', '#1d5f8a'), acc='#fff3c4', dark=False, hook='Ice blue. Oyster steel.'),
    'M8': dict(word='CLASSIC', bg=('#3b4f7a', '#0f1830'), acc='#e0e6f2', dark=False, hook='Royal blue. Classic steel.'),
    'M9': dict(word='TEXTURE', bg=('#8a6f55', '#2b2018'), acc='#f1d98a', dark=False, hook='Vertical texture. Gold bezel.'),
    'M10': dict(word='FORMAL', bg=('#c9d3e0', '#5d6f8a'), acc='#2a1f08', dark=True, hook='White dial. XII at the top.'),
    'W5': dict(word='SHINE', bg=('#f2d58a', '#b07a1c'), acc='#4b3a10', dark=True, hook='Golden shine. Stone markers.'),
}
