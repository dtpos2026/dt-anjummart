"""Captions, hashtags, alt text and SEO keywords for every Anjum Mart post, plus the ad copy library.

Rules: only catalogue facts (names, colours, "Day & Date Display", quartz, crystal-style, prices), Free Delivery All Pakistan and
Cash on Delivery. No discounts, urgency, ratings, reviews, "original", "best" or returns claims. Perfume longevity is left out.
"""

SITE = 'anjummart.com'
WA = '+92 371 4661514'
FREE = 'Free delivery all over Pakistan · Cash on Delivery'

CITIES = '#Multan #Lahore #Karachi #Islamabad'

TAGS = {
    'brand': '#AnjumMart #AnjumMartPakistan',
    'shop': '#OnlineShoppingPakistan #FreeDeliveryPakistan #CashOnDelivery',
    'men': '#MensWatches #WatchesForMen #WatchesPakistan #MensFashionPakistan #RustetWatch',
    'women': '#LadiesWatches #WatchesForWomen #WatchesPakistan #WomensFashionPakistan #MoonstonWatch',
    'jewellery': '#BridalJewellery #JewelleryPakistan #ArtificialJewellery #MaangTikka #WeddingSeason',
    'perfume': '#PerfumesPakistan #EauDeParfum #FragranceLovers #AnjumPerfumes',
}

# pid: hook, facts (3 short lines), occasion, roman urdu line, keywords, alt text, extra tags
PRODUCTS = {
    'M1': dict(
        name="RUSTET Gold Men's Quartz Watch · Black Dial", cat='men', price='Rs. 3,999',
        hook='Black dial. Gold presence.',
        facts=['Deep black dial with gold-tone Roman numerals', 'Full gold-tone case and bracelet', 'Day & Date display · Quartz movement'],
        occasion='Made for formal and festive occasions.',
        ur='Gold case aur black dial ka royal look. Formal aur festive occasions ke liye.',
        kw='gold watch for men Pakistan, black dial watch, Roman numeral watch, day date watch, RUSTET watch',
        alt="Gold men's wristwatch with a black dial, gold-tone Roman numerals and a day and date window on a black and gold background",
        tags='#GoldWatch #BlackDial #RomanNumerals',
        tt='Gold + black dial = instant upgrade'),
    'M2': dict(
        name="RUSTET Gold & Silver Men's Watch · Royal Blue Dial", cat='men', price='Rs. 3,999',
        hook='Royal blue, rounded-square, two-tone.',
        facts=['Royal blue dial with gold-tone hour markers', 'Gold & silver two-tone metal bracelet', 'Day & Date display · Analog time'],
        occasion='Easy to wear to the office and just as sharp for gifting.',
        ur='Royal blue dial aur two-tone bracelet: office se lekar gift tak, har jagah fit.',
        kw='royal blue dial watch, two tone watch for men, gold silver watch Pakistan, day date watch, RUSTET',
        alt="Two-tone gold and silver men's watch with a royal blue dial and a rounded-square case",
        tags='#BlueDialWatch #TwoToneWatch #GiftForHim',
        tt='Royal blue dial. Two-tone bracelet.'),
    'M3': dict(
        name="RUSTET All-Black Men's Quartz Watch", cat='men', price='Rs. 3,999',
        hook='All black. All attitude.',
        facts=['Black dial with silver-tone Roman numerals', 'Geometric-pattern black metal bracelet', 'Day & Date display · Quartz movement'],
        occasion='A bold everyday watch that works casual or formal.',
        ur='All-black design, faceted bezel aur geometric bracelet. Casual aur formal dono mein bold.',
        kw='all black watch for men, black quartz watch, geometric bracelet watch, day date watch Pakistan',
        alt="All-black men's wristwatch with a black dial, faceted bezel and a geometric-pattern metal bracelet",
        tags='#AllBlackWatch #BlackWatch #MensStyle',
        tt='All-black. No explanation needed.'),
    'M4': dict(
        name="RUSTET Silver Men's Quartz Watch · Green Dial", cat='men', price='Rs. 3,999',
        hook='A green dial that does the talking.',
        facts=['Rich green sunburst dial with Roman numerals', 'Polished silver-tone ridged bezel', 'Day & Date display · Quartz movement'],
        occasion='Sharp for work, weekends and formal dinners.',
        ur='Green sunburst dial aur silver bracelet. Everyday aur formal wear ke liye.',
        kw='green dial watch, silver watch for men, Roman numeral watch, sunburst dial, day date watch Pakistan',
        alt="Silver men's wristwatch with a green sunburst dial, Roman numerals and a ridged silver bezel",
        tags='#GreenDialWatch #SilverWatch #SunburstDial',
        tt='Green sunburst dial, silver finish'),
    'M5': dict(
        name="RUSTET Silver Men's Quartz Watch · Emerald Green Dial", cat='men', price='Rs. 3,999',
        hook='Emerald green. Textured. Polished.',
        facts=['Emerald green sunburst dial with a textured pattern', 'Full silver-tone finish and metal link bracelet', 'Day & Date display at 3 o’clock'],
        occasion='Casual and formal wear, one watch.',
        ur='Emerald green textured dial aur polished silver finish. Casual aur formal dono ke liye.',
        kw='emerald green watch, silver quartz watch men, textured dial, day date watch, metal bracelet watch',
        alt="Silver men's wristwatch with an emerald green textured dial and a day and date window at three o'clock",
        tags='#EmeraldGreen #QuartzWatch #WatchLover',
        tt='Emerald green dial in silver'),
    'M6': dict(
        name="RUSTET Two-Tone Gold & Silver Men's Quartz Watch · White Dial", cat='men', price='Rs. 3,999',
        hook='Clean white dial. Warm gold bezel.',
        facts=['White dial with a gold-tone bezel', 'Silver-and-gold metal bracelet', 'Quartz movement · Date window'],
        occasion='Smart for the office, meetings and everyday wear.',
        ur='White dial, gold bezel aur two-tone bracelet. Office aur everyday look ke liye.',
        kw='white dial watch men, two tone gold silver watch, quartz watch Pakistan, date window watch',
        alt="Two-tone gold and silver men's wristwatch with a white dial and a gold-tone bezel",
        tags='#WhiteDialWatch #TwoToneWatch #OfficeStyle',
        tt='White dial + gold bezel'),
    'W1': dict(
        name='MOONSTON Black Ladies Quartz Watch · Dark Green Dial', cat='women', price='Rs. 2,499',
        hook='A bracelet that looks like jewellery.',
        facts=['Dark green textured dial with crystal-style markers', 'Black bracelet with crystal-style flower links', 'Quartz movement · Faceted case'],
        occasion='A thoughtful gift, or a treat for yourself.',
        ur='Dark green dial aur crystal-style flower bracelet. Gift ya apne liye, dono perfect.',
        kw='black ladies watch Pakistan, flower bracelet watch, dark green dial watch women, crystal style watch, gift for her',
        alt="Black ladies wristwatch with a dark green dial and a bracelet of crystal-style flower links",
        tags='#BlackWatch #GiftForHer #CrystalStyle',
        tt='This bracelet is basically jewellery'),
    'W2': dict(
        name='MOONSTON Rose Gold Ladies Quartz Watch · Pink Dial', cat='women', price='Rs. 2,999',
        hook='Pink dial. Rose-gold glow.',
        facts=['Pink-lavender sunburst dial', 'Crystal-style studded bezel and bracelet', 'Decorative Roman numeral markers · Quartz'],
        occasion='Made for weddings, parties and everyday sparkle.',
        ur='Pink dial, rose-gold finish aur crystal-style bezel. Weddings aur parties ke liye.',
        kw='rose gold ladies watch Pakistan, pink dial watch, crystal style bezel, wedding watch for women, MOONSTON',
        alt="Rose gold ladies wristwatch with a pink-lavender dial and a crystal-style studded bezel and bracelet",
        tags='#RoseGold #PinkDial #WeddingStyle',
        tt='Rose gold + pink dial'),
    'W3': dict(
        name='MOONSTON Ladies Quartz Watch · Pink-Lavender Dial', cat='women', price='Rs. 2,999',
        hook='Pink-lavender, serious sparkle.',
        facts=['Pink-lavender sunburst dial with Roman numerals', 'Crystal-style studded bezel and bracelet', 'Quartz movement · Analog display'],
        occasion='Perfect for weddings, parties and special days.',
        ur='Pink-lavender dial aur crystal-style studded bracelet. Weddings aur special occasions ke liye.',
        kw='pink lavender dial watch, ladies watch Pakistan, crystal bezel watch, jewellery inspired watch, ladies quartz watch, MOONSTON',
        alt='Ladies wristwatch with a pink-lavender dial, Roman numerals and a crystal-style studded bezel and bracelet',
        tags='#PinkLavender #CrystalStyle #LadiesStyle',
        tt='Pink-lavender, serious sparkle'),
    'W4': dict(
        name='MOONSTON Two-Tone Ladies Quartz Watch · Emerald Green Dial', cat='women', price='Rs. 2,999',
        hook='Emerald dial. Silver and rose gold.',
        facts=['Emerald green dial with crystal-style Roman numerals', 'Silver & rose gold two-tone bracelet', 'Sparkling decorative bezel · Quartz'],
        occasion='Glamorous for weddings, parties and every day.',
        ur='Emerald green dial aur two-tone bracelet. Weddings, parties aur everyday wear.',
        kw='emerald green ladies watch, two tone watch for women, silver rose gold watch, crystal style watch Pakistan',
        alt="Two-tone silver and rose gold ladies wristwatch with an emerald green dial and a sparkling bezel",
        tags='#EmeraldGreenWatch #TwoToneWatch #GlamStyle',
        tt='Emerald dial, rose-gold accents'),
    'J1': dict(
        name='Silver & White Mirror Stone Jewellery Set', cat='jewellery', price='Rs. 1,999',
        hook='Mirror stones, pearl-white drops.',
        facts=['Statement necklace, earrings and maang tikka', 'Mirror-style stone work with intricate floral detail', 'Delicate pearl-white bead drops'],
        occasion='For bridal looks, parties, weddings and festive days.',
        ur='Necklace, earrings aur maang tikka ka mukammal set. Bridal aur party looks ke liye.',
        kw='mirror stone jewellery set, silver bridal jewellery Pakistan, maang tikka set, artificial jewellery set, wedding jewellery',
        alt="Silver and white mirror stone jewellery set: a statement necklace, matching earrings and a maang tikka with pearl-white bead drops",
        tags='#MirrorStone #SilverJewellery #BridalLook',
        tt='The whole set. One price.'),
    'J2': dict(
        name='Green & Gold Traditional Bridal Jewellery Set', cat='jewellery', price='Rs. 1,999',
        hook='Emerald green meets gold.',
        facts=['Traditional choker necklace, earrings and maang tikka', 'Gold-tone detailing with emerald-green stones', 'Green bead drops and crystal-style accents'],
        occasion='Ideal for weddings, Mehndi and festive events.',
        ur='Green aur gold ka traditional set: choker, earrings aur maang tikka. Mehndi aur wedding ke liye.',
        kw='green gold bridal jewellery set, traditional choker set, Mehndi jewellery, emerald green jewellery, artificial jewellery Pakistan',
        alt="Green and gold traditional bridal jewellery set with a choker necklace, earrings and a maang tikka",
        tags='#MehndiJewellery #GreenAndGold #TraditionalJewellery',
        tt='Mehndi-ready: green & gold set'),
    'P1': dict(
        name='Lady Aura by Anjum · Eau de Parfum 50 ml', cat='perfume', price='Rs. 3,450',
        hook='Meet Lady Aura.',
        facts=['50 ml Eau de Parfum for women', 'A premium floral fragrance oil', 'Red box, frosted bottle, gold detail'],
        occasion='A gift she will actually use.',
        ur='Lady Aura: 50 ml Eau de Parfum, premium floral fragrance oil. Khaas logon ke liye gift.',
        kw='women perfume Pakistan, floral fragrance, eau de parfum 50ml, perfume gift for her, Anjum perfume',
        alt="Lady Aura by Anjum, a 50 ml Eau de Parfum for women: a frosted red bottle with a black cap standing on a red box",
        tags='#LadyAura #FloralFragrance #GiftForHer',
        tt='Meet Lady Aura'),
    'P2': dict(
        name='Oud Aura by Anjum · Eau de Parfum 50 ml', cat='perfume', price='Rs. 3,450',
        hook='Oud, for everyone.',
        facts=['50 ml Eau de Parfum, unisex', 'A premium oud fragrance oil', 'White tube, frosted bottle, gold lettering'],
        occasion='A fragrance to share, gift or keep.',
        ur='Oud Aura: 50 ml unisex Eau de Parfum, premium oud fragrance oil.',
        kw='oud perfume Pakistan, unisex fragrance, eau de parfum 50ml, perfume gift, Anjum perfume',
        alt="Oud Aura by Anjum, a 50 ml unisex Eau de Parfum: a frosted bottle with a black cap beside a white presentation tube",
        tags='#OudAura #OudPerfume #UnisexFragrance',
        tt='Oud Aura. Unisex. 50 ml.'),
    'P3': dict(
        name='Tea Rose by Anjum · Eau de Parfum 50 ml', cat='perfume', price='Rs. 3,450',
        hook='Tea Rose: soft, red, 50 ml.',
        facts=['50 ml Eau de Parfum for women', 'A premium fragrance oil', 'Red bottle and gift tube'],
        occasion='Wrapped and ready to give.',
        ur='Tea Rose: 50 ml Eau de Parfum for women, premium fragrance oil.',
        kw='tea rose perfume, women perfume Pakistan, eau de parfum 50ml, perfume gift for her, Anjum Mart',
        alt="Tea Rose by Anjum, a 50 ml Eau de Parfum for women: a red frosted bottle beside a red presentation tube",
        tags='#TeaRose #RosePerfume #PerfumeGift',
        tt='Tea Rose in red'),
    'M7': dict(
        name="RUSTET Ice Blue Oyster Series Men's Watch", cat='men', price='Rs. 4,000',
        hook='Ice blue. Oyster steel.',
        facts=['Ice blue dial with a brushed texture', 'Full silver stainless steel case and oyster chain', 'Day & Date display · Quartz · Luminous hands and markers'],
        occasion='A fresh colour for everyday and office wear.',
        ur='Ice blue dial aur full silver steel oyster chain. Roz ke use aur office ke liye.',
        kw='ice blue dial watch, oyster series watch, silver watch for men Pakistan, day date watch, RUSTET',
        alt="Men's silver stainless steel wristwatch with an ice blue brushed dial, luminous hands and a day and date window",
        tags='#IceBlue #OysterSeries #SilverWatch',
        tt='Ice blue dial, full steel'),
    'M8': dict(
        name='RUSTET Royal Blue Classic Series Watch', cat='men', price='Rs. 4,450',
        hook='Royal blue. Classic steel.',
        facts=['Royal blue sunburst dial with 3D diamond-cut arrow markers', 'Silver stainless steel case and chain', 'Day & Date display · Quartz movement'],
        occasion='A classic look for the office and formal days.',
        ur='Royal blue sunburst dial aur full silver steel chain. Office aur formal use ke liye.',
        kw='royal blue dial watch, classic series watch, silver steel watch Pakistan, day date watch, RUSTET',
        alt='Silver stainless steel wristwatch with a royal blue sunburst dial, arrow-shaped markers and a day and date window',
        tags='#RoyalBlue #ClassicSeries #SteelWatch',
        tt='Royal blue sunburst dial'),
    'M9': dict(
        name="RUSTET Black Vertical-Texture Men's Watch", cat='men', price='Rs. 3,990',
        hook='Vertical texture. Gold bezel.',
        facts=['Black dial with a vertical texture and luminous markers', 'Gold-plated bezel and crown', 'Two-tone silver and gold bracelet · Day & Date display · Quartz'],
        occasion='Easy to wear from work to dinner.',
        ur='Black vertical-texture dial, gold bezel aur two-tone bracelet. Office se dinner tak.',
        kw='black dial watch for men Pakistan, two tone watch, gold bezel watch, day date watch, RUSTET',
        alt="Men's two-tone wristwatch with a black vertically textured dial, a gold bezel and a silver and gold bracelet",
        tags='#BlackDial #TwoToneWatch #GoldBezel',
        tt='Black texture + gold bezel'),
    'M10': dict(
        name='RUSTET White Textured Dial Watch · XII Roman Numeral', cat='men', price='Rs. 4,000',
        hook='White dial. XII at the top.',
        facts=['White textured dial with an XII Roman numeral at the top', 'Two-tone stainless steel case, gold bezel and jubilee chain', 'Day & Date display · Quartz movement'],
        occasion='A clean look for business and formal wear.',
        ur='White textured dial, gold bezel aur two-tone jubilee chain. Formal aur business use ke liye.',
        kw='white dial watch Pakistan, two tone jubilee watch, Roman numeral watch, formal watch, day date watch, RUSTET',
        alt='Two-tone wristwatch with a white textured dial, an XII Roman numeral at the top, a gold bezel and a jubilee chain',
        tags='#WhiteDial #JubileeChain #FormalWatch',
        tt='White textured dial, XII on top'),
    'W5': dict(
        name='RUSTET Ladies Watch · Golden Shine Dial', cat='women', price='Rs. 4,000',
        hook='Golden shine. Stone markers.',
        facts=['Golden shine dial with stone markers', 'Gold fluted bezel and a two-tone jubilee chain (silver and gold)', 'Date display with magnifier at 3 o\'clock · Quartz'],
        occasion='A little gold for everyday and festive days.',
        ur='Golden shine dial, gold fluted bezel aur two-tone jubilee chain. Roz ke use aur festive days ke liye.',
        kw='ladies gold watch Pakistan, golden dial watch, two tone jubilee chain, date magnifier watch, RUSTET ladies watch',
        alt='Ladies two-tone wristwatch with a golden shine dial, stone markers, a gold fluted bezel and a jubilee chain',
        tags='#GoldenShine #LadiesWatch #TwoTone',
        tt='Golden shine dial'),
}

COLLECTIONS = {
    'MEN': dict(title="The Men's Collection", cat='men', price='From Rs. 3,990', hook='Ten watches. Every dial colour.',
                facts=['Gold, silver, two-tone and black', 'Day & Date display on most styles', 'Quartz movement · Metal link bracelets'],
                ur="Men's collection: gold, silver, two-tone, black, blue aur green. Rs. 3,990 se shuru.",
                kw="men's watches Pakistan, RUSTET quartz watch, gold watch, black watch, watches online Pakistan",
                alt="A selection of RUSTET men's watches in gold, silver, two-tone and black",
                tags='#MensCollection'),
    'WOMEN': dict(title='The Ladies Collection', cat='women', price='From Rs. 2,499', hook='Black, pink and emerald.',
                  facts=['Crystal-style bezels and bracelets', 'Rose gold, two-tone and black finishes', 'From Rs. 2,499'],
                  ur='Ladies collection: black, pink aur emerald. Rs. 2,499 se shuru.',
                  kw='ladies watches Pakistan, rose gold watch for women, crystal style watch, MOONSTON watch, watches for women online',
                  alt='A selection of MOONSTON ladies watches in black, rose gold with a pink dial, and two-tone with an emerald dial',
                  tags='#LadiesCollection'),
    'JEWELLERY': dict(title='Bridal Jewellery', cat='jewellery', price='Rs. 1,999 each', hook='Two sets. Complete looks.',
                      facts=['Necklace, earrings and maang tikka in every set', 'Silver & white mirror stone, or green & gold traditional', 'Rs. 1,999 each'],
                      ur='Do bridal sets: silver-white mirror stone aur green-gold traditional. Rs. 1,999 each.',
                      kw='bridal jewellery Pakistan, jewellery set with maang tikka, wedding jewellery online, Mehndi jewellery',
                      alt='Two bridal jewellery sets: silver and white mirror stone, and green and gold traditional',
                      tags='#BridalCollection'),
    'PERFUMES': dict(title='Anjum Perfumes', cat='perfume', price='Rs. 3,450 each', hook='Three fragrances. 50 ml each.',
                     facts=['Lady Aura, Oud Aura and Tea Rose', '50 ml Eau de Parfum each', 'Rs. 3,450 each'],
                     ur='Anjum Perfumes: Lady Aura, Oud Aura aur Tea Rose. 50 ml, Rs. 3,450 each.',
                     kw='perfumes Pakistan, eau de parfum 50ml, oud perfume, floral perfume, perfume gift set',
                     alt='Three Anjum Eau de Parfum bottles with their gift packaging: Lady Aura, Oud Aura and Tea Rose',
                     tags='#PerfumeCollection'),
}

INFO = {
    'ORDER': dict(
        title='How to order in 3 steps',
        hook='Ordering from Anjum Mart takes two minutes.',
        lines=['1. Pick your piece on anjummart.com (or message us on WhatsApp).', '2. Send your name, phone number, address and city.', '3. Pay when it arrives. Cash on Delivery, free delivery all over Pakistan.'],
        ur='Order karna aasan hai: pasand chunein, apna address bhejein, parcel aane par cash dein. Delivery free hai.',
        kw='how to order online Pakistan, cash on delivery watches, free delivery Pakistan, order on WhatsApp',
        alt='Graphic with three steps to order from Anjum Mart: choose, send your details, pay on delivery',
        tags='#HowToOrder #CashOnDelivery'),
    'DELIVERY': dict(
        title='Free delivery. Every order. Every city.',
        hook='Free delivery all over Pakistan, on every order.',
        lines=['Dispatched within 1–2 working days after confirmation.', 'Usually 3–5 working days to major cities, 5–7 to other areas (estimates).', 'Cash on Delivery: check the parcel, then pay.'],
        ur='Poore Pakistan mein free delivery. Cash on Delivery: parcel check karein, phir payment dein.',
        kw='free delivery Pakistan, cash on delivery, online shopping Pakistan, courier delivery all Pakistan',
        alt='Graphic: Free delivery all over Pakistan and Cash on Delivery on every Anjum Mart order',
        tags='#FreeDelivery #COD'),
    'WEDDING': dict(
        title='Wedding season: complete the look',
        hook='Jewellery, a watch and a fragrance. One look.',
        lines=['A bridal set with necklace, earrings and maang tikka: Rs. 1,999.', 'A crystal-style ladies watch from Rs. 2,499.', 'A 50 ml Eau de Parfum: Rs. 3,450.'],
        ur='Wedding season ke liye mukammal look: jewellery set, watch aur perfume. Delivery free.',
        kw='wedding season jewellery, bridal look Pakistan, Mehndi jewellery, wedding gift ideas, jewellery watch perfume',
        alt='Graphic: a bridal jewellery set, a ladies watch and a perfume bottle styled as one wedding look',
        tags='#WeddingSeason #BridalLook'),
    'FAQ': dict(
        title='Your questions, answered',
        hook='Three things people ask us most.',
        lines=['Is delivery really free? Yes, all over Pakistan.', 'Can I pay when it arrives? Yes, Cash on Delivery.', 'What if the parcel arrives damaged or wrong? Tell us within 48 hours with photos or a short video and we replace it.'],
        ur='Delivery free hai. Cash on Delivery available hai. Damaged ya ghalat item ho to 48 ghante mein bata dein, replace karte hain.',
        kw='free delivery Pakistan, cash on delivery, replacement policy, online shopping questions',
        alt='Graphic with three frequently asked questions and short answers about delivery, payment and replacement',
        tags='#FAQ #OnlineShopping'),
    'GIFTHIM': dict(
        title='Gift ideas for him',
        hook='Gifts for him that he will actually wear.',
        lines=["A RUSTET quartz watch with Day & Date display: from Rs. 3,990.", 'Or a 50 ml Oud Aura unisex fragrance: Rs. 3,450.', 'Free delivery all over Pakistan.'],
        ur='Unke liye gift: RUSTET watch (Rs. 3,990 se) ya Oud Aura perfume (Rs. 3,450). Delivery free.',
        kw='gift for him Pakistan, men watch gift, oud perfume gift, birthday gift for husband',
        alt="Graphic: gift ideas for him, a men's watch and an oud perfume with prices",
        tags='#GiftForHim #GiftIdeas'),
    'GIFTHER': dict(
        title='Gift ideas for her',
        hook='Gifts for her that feel personal.',
        lines=['A crystal-style MOONSTON watch from Rs. 2,499.', 'A bridal or party jewellery set: Rs. 1,999.', 'Lady Aura or Tea Rose Eau de Parfum: Rs. 3,450.'],
        ur='Unke liye gift: MOONSTON watch (Rs. 2,499 se), jewellery set (Rs. 1,999) ya perfume (Rs. 3,450).',
        kw='gift for her Pakistan, ladies watch gift, jewellery set gift, perfume gift for women',
        alt='Graphic: gift ideas for her, a ladies watch, a jewellery set and a perfume with prices',
        tags='#GiftForHer #GiftIdeas'),
    'BRAND': dict(
        title='Timeless Style. Everyday Luxury.',
        hook='Watches. Jewellery. Perfumes.',
        lines=['Anjum Mart brings watches, bridal jewellery and perfumes to your door.', 'Free delivery all over Pakistan. Cash on Delivery.', 'Order on anjummart.com or WhatsApp.'],
        ur='Anjum Mart: watches, jewellery aur perfumes. Poore Pakistan mein free delivery aur Cash on Delivery.',
        kw='watches jewellery perfumes Pakistan, online shopping Pakistan, free delivery, cash on delivery, Anjum Mart',
        alt='Anjum Mart logo with the words Timeless Style. Everyday Luxury. on a black and gold background',
        tags='#TimelessStyle #EverydayLuxury'),
}


INFO.update({
    'ALL': dict(
        title='Everything in one place',
        hook='Watches. Jewellery. Perfumes. All at Anjum Mart.',
        lines=["Men's watches from Rs. 3,990 · ladies watches from Rs. 2,499.", 'Bridal jewellery sets Rs. 1,999 · 50 ml perfumes Rs. 3,450.', 'Free delivery all over Pakistan. Cash on Delivery.'],
        ur='Anjum Mart par watches, jewellery aur perfumes ek hi jagah. Delivery free, payment parcel milne par.',
        kw='watches jewellery perfumes Pakistan, online shopping Pakistan, free delivery, cash on delivery, Anjum Mart',
        alt='A fast colour montage of Anjum Mart watches, bridal jewellery sets and perfumes, each on its own coloured background with the price',
        tags='#TimelessStyle #WatchesJewelleryPerfumes'),
    'MEET': dict(
        title='Meet Anjum Mart',
        hook='Meet Anjum Mart: Timeless Style. Everyday Luxury.',
        lines=["Watches for him and for her, from Rs. 2,499.", 'Bridal jewellery sets with necklace, earrings and maang tikka: Rs. 1,999.', '50 ml Eau de Parfum: Rs. 3,450. Free delivery all over Pakistan.'],
        ur='Anjum Mart se milein: watches, jewellery aur perfumes. Poore Pakistan mein free delivery.',
        kw='Anjum Mart, watches jewellery perfumes Pakistan, online shopping Pakistan, free delivery Pakistan',
        alt='Introduction graphic: a gold men\'s watch, a rose-gold ladies watch, a green and gold jewellery set and a perfume bottle on a cream background with the words Timeless Style. Everyday Luxury.',
        tags='#MeetAnjumMart #TimelessStyle'),
    'GMEN': dict(
        title="Which dial suits you?", cat='men',
        hook="Black, blue, green or white? Pick your dial.",
        lines=['Black: gold Roman numerals, all-black or vertical texture. From Rs. 3,990.', 'Blue: royal blue two-tone, royal blue classic or ice blue oyster. From Rs. 3,999.', 'Green: silver with Roman numerals, or emerald sunburst. Rs. 3,999.', 'White: two-tone gold & silver, or textured with an XII on top. From Rs. 3,999.'],
        ur='Apna dial chunein: black, blue, green ya white. RUSTET quartz watches Rs. 3,990 se shuru.',
        kw="men's watch dial guide, black dial watch, blue dial watch, green dial watch, white dial watch Pakistan, RUSTET",
        alt="Guide to men's RUSTET watch dials: black, blue, green and white watches with prices",
        tags='#WatchGuide #DialColour'),
    'GLADIES': dict(
        title='Pink, emerald, black or gold?', cat='women',
        hook='Pink, emerald, black or gold? Which one is yours?',
        lines=['Rose gold with a pink dial: Rs. 2,999.', 'Crystal-style with a pink-lavender dial: Rs. 2,999.', 'Two-tone with an emerald dial: Rs. 2,999.', 'Black with a dark green dial and flower bracelet: Rs. 2,499.', 'Golden shine dial with a two-tone jubilee chain: Rs. 4,000.'],
        ur='Ladies watches: pink, emerald, black ya golden shine. Rs. 2,499 se shuru. Delivery free.',
        kw='ladies watch colours, rose gold watch for women, pink dial watch, emerald dial watch, MOONSTON watch Pakistan',
        alt='Guide to ladies watches in pink, pink-lavender, emerald, black and golden shine with prices',
        tags='#LadiesWatchGuide #CrystalStyle'),
    'GSCENT': dict(
        title='Find your Anjum fragrance', cat='perfume',
        hook='Floral, oud or tea rose? Find your fragrance.',
        lines=['Lady Aura: a premium floral fragrance for women.', 'Oud Aura: a premium oud fragrance, unisex.', 'Tea Rose: a premium fragrance oil for women.', '50 ml each · Rs. 3,450 each.'],
        ur='Apni fragrance chunein: Lady Aura (floral), Oud Aura (oud, unisex) ya Tea Rose. 50 ml, Rs. 3,450 each.',
        kw='perfume guide Pakistan, floral perfume, oud perfume unisex, tea rose perfume, eau de parfum 50ml',
        alt='Guide to the three Anjum 50 ml perfumes: Lady Aura, Oud Aura and Tea Rose with prices',
        tags='#FragranceGuide #PerfumeCollection'),
    'ETHIS1': dict(
        title='This or that? Gold or blue', cat='men',
        hook='Gold & black, or royal blue? Comment 1 or 2.',
        lines=['1: Gold case, black dial, Roman numerals.', '2: Gold & silver, royal blue dial.', 'Both Rs. 3,999 with Day & Date display.'],
        ur='Aap kaunsi lenge? 1 ya 2 comment karein.',
        kw="men's watches Pakistan, gold watch, blue dial watch, this or that, RUSTET",
        alt='Split picture: a gold watch with a black dial marked 1 on a brown background, and a gold and silver watch with a royal blue dial marked 2 on a blue background',
        tags='#ThisOrThat #WatchPoll'),
    'ETHIS2': dict(
        title='This or that? Pink or golden shine', cat='women',
        hook='Rose-gold pink or golden shine? Comment 1 or 2.',
        lines=['1: Rose gold, pink dial, crystal-style bezel. Rs. 2,999.', '2: Golden shine dial, two-tone jubilee chain. Rs. 4,000.', 'Free delivery all over Pakistan.'],
        ur='Pink ya golden shine? 1 ya 2 comment karein.',
        kw='ladies watches Pakistan, pink dial watch, golden dial watch, rose gold watch, this or that',
        alt='Split picture: a rose-gold watch with a pink dial marked 1 on pink, and a two-tone watch with a golden dial marked 2 on amber',
        tags='#ThisOrThat #LadiesWatch'),
    'ETHIS3': dict(
        title='This or that? Lady Aura or Tea Rose', cat='perfume',
        hook='Lady Aura or Tea Rose? Comment 1 or 2.',
        lines=['1: Lady Aura, a premium floral fragrance.', '2: Tea Rose, a premium fragrance oil.', '50 ml each · Rs. 3,450 each.'],
        ur='Lady Aura ya Tea Rose? 1 ya 2 comment karein.',
        kw='perfumes Pakistan, floral perfume, tea rose perfume, eau de parfum 50ml, this or that',
        alt='Split picture of two red perfume photos: Lady Aura marked 1 and Tea Rose marked 2',
        tags='#ThisOrThat #PerfumePoll'),
    'ETHIS4': dict(
        title='This or that? Black or ice blue', cat='men',
        hook='All-black or ice blue? Comment 1 or 2.',
        lines=['1: All-black watch, black dial, Day & Date display. Rs. 3,999.', '2: Ice blue Oyster Series, full silver steel. Rs. 4,000.', 'Free delivery all over Pakistan.'],
        ur='Black ya ice blue? 1 ya 2 comment karein.',
        kw="men's watches Pakistan, all black watch, ice blue dial watch, this or that, RUSTET",
        alt='Split picture: an all-black watch marked 1 on a dark grey background, and a silver watch with an ice blue dial marked 2 on a blue background',
        tags='#ThisOrThat #WatchPoll'),
    'ETHIS5': dict(
        title='This or that? Silver or green and gold', cat='jewellery',
        hook='Silver and white, or green and gold? Comment 1 or 2.',
        lines=['1: Silver & white mirror stone set.', '2: Green & gold traditional set.', 'Necklace, earrings and maang tikka · Rs. 1,999 each.'],
        ur='Silver-white ya green-gold? 1 ya 2 comment karein.',
        kw='bridal jewellery Pakistan, jewellery set with maang tikka, silver mirror stone set, green gold jewellery set, this or that',
        alt='Split picture of two jewellery sets: silver and white mirror stone marked 1, green and gold traditional marked 2',
        tags='#ThisOrThat #BridalSet'),
    'ETAG': dict(
        title='Tag someone who needs a new watch', cat='men',
        hook='Tag someone who needs a new watch.',
        lines=['The all-black RUSTET quartz watch with Day & Date display: Rs. 3,999.', 'Tag them in the comments and send them anjummart.com.', 'Free delivery all over Pakistan · Cash on Delivery.'],
        ur='Kisi aise dost ko tag karein jise nayi watch chahiye. Delivery free hai.',
        kw="men's watch gift, all black watch Pakistan, tag a friend, RUSTET watch",
        alt='An all-black men\'s watch on a dark grey background with the words Tag someone who needs a new watch',
        tags='#TagAFriend #GiftIdeas'),
    'EWORD': dict(
        title='Comment a word, get the details', 
        hook='Comment WATCH, JEWELLERY or PERFUME and we will reply with the details.',
        lines=['WATCH: men\'s and ladies watches. JEWELLERY: bridal sets with maang tikka. PERFUME: Lady Aura, Oud Aura, Tea Rose.', 'We reply with prices, colours and how to order.', 'Or message us on WhatsApp +92 371 4661514.'],
        ur='WATCH, JEWELLERY ya PERFUME comment karein, hum price aur details bhejte hain.',
        kw='watches jewellery perfumes Pakistan, how to order, WhatsApp order, Anjum Mart',
        alt='Cream graphic with three boxes: WATCH, JEWELLERY and PERFUME, and a WhatsApp button',
        tags='#AskUs #AnjumMart'),
})

# colour-series posts: same pieces as the product posts, a different hook line and alt text
from catalog import THEMES  # noqa: E402
for _pid in list(PRODUCTS):
    _p = PRODUCTS[_pid]
    _t = THEMES[_pid]
    PRODUCTS['K-' + _pid] = dict(
        _p, hook=_t['hook'], occasion='Colour story: ' + _t['word'].title() + '.',
        alt=_p['alt'] + ', on a ' + _t['word'].lower() + '-coloured background with the word ' + _t['word'] + ' behind it',
        tt=_t['hook'])


ASK = {
    'men': 'Which dial do you like? Tell us below 👇',
    'women': 'Which colour is yours? Tell us below 👇',
    'jewellery': 'Which set would you wear? Tell us below 👇',
    'perfume': 'Floral or oud: which do you love? Tell us below 👇',
    'shop': 'Save this post for later 🔖 and tag someone who needs it.',
}


def _entry(key):
    return PRODUCTS.get(key) or COLLECTIONS.get(key) or INFO.get(key)


def hashtags(pid_or_key, platform):
    """Instagram: exactly 5 hashtags (the current limit). Facebook: 3. TikTok: 5."""
    p = _entry(pid_or_key)
    cat = p.get('cat', 'shop')
    base = TAGS.get(cat, '').split()
    own = p.get('tags', '').split()

    def uniq(items, n):
        seen, out = set(), []
        for h in items:
            if h.lower() not in seen:
                seen.add(h.lower())
                out.append(h)
        return ' '.join(out[:n])
    if platform == 'ig':
        return uniq(['#AnjumMart'] + own[:2] + base[:2] + ['#FreeDeliveryPakistan', '#OnlineShoppingPakistan', '#ShopOnline', '#Pakistan'], 5)
    if platform == 'fb':
        return uniq(['#AnjumMart'] + own[:1] + ['#FreeDeliveryPakistan', '#OnlineShoppingPakistan'], 3)
    return uniq(['#AnjumMart'] + own[:2] + ['#Pakistan', '#FYP', '#OnlineShopping', '#ShopOnline'], 5)


def _seo_line(p, key):
    kws = [k.strip() for k in p.get('kw', '').split(',') if k.strip()]
    first = kws[0] if kws else p.get('title', '')
    if 'pakistan' not in first.lower():
        first += ' in Pakistan'
    return first[0].upper() + first[1:]


def caption(pid, platform):
    """Instagram caption formula: search line, hook, facts, price and delivery, one Roman Urdu line, order line, one question, 5 hashtags."""
    p = _entry(pid)
    price = p.get('price', '')
    ask = ASK.get(p.get('cat', 'shop'), ASK['shop'])
    if pid in INFO:
        body = '\n'.join(p['lines'])
        tail = f"Order: {SITE} or WhatsApp {WA}"
        if platform == 'ig':
            return f"{_seo_line(p, pid)} ✨\n{p['hook']}\n\n{body}\n\n{p['ur']}\n📍 {tail}\n💬 {ask}\n\n{hashtags(pid, 'ig')}"
        if platform == 'fb':
            return f"{p['hook']}\n\n{body}\n\nOrder on {SITE} or message us on WhatsApp {WA}.\n\n{hashtags(pid, 'fb')}"
        return f"{p['hook']} {p['lines'][0]} {hashtags(pid, 'tt')}"
    facts = '\n'.join('• ' + f for f in p['facts'])
    name = p.get('name') or p['title']
    if platform == 'ig':
        return (f"{_seo_line(p, pid)} ✨\n{p['hook']}\n\n{name}\n{facts}\n{price} · {FREE}\n\n"
                f"{p['ur']}\n📍 Order: tap the WhatsApp button or visit {SITE}\n💬 {ask}\n\n{hashtags(pid, 'ig')}")
    if platform == 'fb':
        return (f"{p['hook']}\n\n{name}\n{facts}\n{price} · {FREE}\n\n"
                f"Order on {SITE} or message us on WhatsApp {WA}.\n\n{hashtags(pid, 'fb')}")
    hook = p.get('tt') or p['hook']
    return f"{hook} · {price} · Free delivery all Pakistan 🇵🇰 {hashtags(pid, 'tt')}"


def first_comment(pid):
    """No extra hashtags (the 5-hashtag limit counts the whole post): the order line goes in the first comment."""
    return f"Order on WhatsApp {WA} or at {SITE} 🛍️  Questions about size, colour or delivery? Ask here and we will reply."


# ---- ad copy library (Meta) -------------------------------------------------------------------------------------
AD = {
    'men': dict(
        primary=[
            "Gold, silver, two-tone, blue, green or all-black: RUSTET quartz watches with Day & Date display, from Rs. 3,990. Free delivery all over Pakistan, Cash on Delivery. Message us on WhatsApp to order.",
            "Looking for a watch that works at the office and at dinner? Ten RUSTET styles from Rs. 3,990. Free delivery, pay when it arrives.",
            "Choose your dial: black, royal blue, green or white. Quartz movement, metal link bracelet, Day & Date. Tap to message us on WhatsApp.",
        ],
        headlines=["Men's Watches from Rs. 3,990", 'Ten Styles, Every Dial Colour', 'Free Delivery All Pakistan'],
        desc='Cash on Delivery · WhatsApp us to order',
    ),
    'women': dict(
        primary=[
            "Crystal-style MOONSTON watches in rose gold, two-tone and black, from Rs. 2,499. Free delivery all over Pakistan, Cash on Delivery. Message us on WhatsApp.",
            "Pink dial, emerald dial or black with a flower bracelet. Ladies watches that look like jewellery, from Rs. 2,499. Pay when it arrives.",
            "A gift she will wear every day: MOONSTON ladies watch, free delivery, Cash on Delivery. Tap to chat on WhatsApp.",
        ],
        headlines=['Ladies Watches from Rs. 2,499', 'Crystal-Style Watches', 'Free Delivery All Pakistan'],
        desc='Cash on Delivery · WhatsApp us to order',
    ),
    'jewellery': dict(
        primary=[
            "Necklace, earrings and maang tikka in one set: Rs. 1,999. Silver & white mirror stone, or green & gold traditional. Free delivery all over Pakistan.",
            "Wedding and Mehndi season is here. Bridal jewellery sets at Rs. 1,999 each, Cash on Delivery. Message us on WhatsApp.",
            "Complete your traditional look: choker, earrings and maang tikka. Free delivery, pay when it arrives.",
        ],
        headlines=['Bridal Jewellery Sets · Rs. 1,999', 'Necklace + Earrings + Tikka', 'Free Delivery All Pakistan'],
        desc='Cash on Delivery · WhatsApp us to order',
    ),
    'perfume': dict(
        primary=[
            "Lady Aura, Oud Aura and Tea Rose: 50 ml Eau de Parfum, Rs. 3,450 each. Free delivery all over Pakistan, Cash on Delivery. Message us on WhatsApp.",
            "Gift a fragrance: floral, oud or tea rose in gift-ready packaging. 50 ml, Rs. 3,450. Pay when it arrives.",
            "Three Anjum fragrances, one easy choice. Tap to message us on WhatsApp and we will help you pick.",
        ],
        headlines=['Anjum Perfumes · Rs. 3,450', '50 ml Eau de Parfum', 'Free Delivery All Pakistan'],
        desc='Cash on Delivery · WhatsApp us to order',
    ),
    'brand': dict(
        primary=[
            "Watches, bridal jewellery and perfumes with free delivery all over Pakistan and Cash on Delivery. Message us on WhatsApp to order.",
            "Anjum Mart: Timeless Style. Everyday Luxury. Order on WhatsApp or anjummart.com. Free delivery, pay when it arrives.",
        ],
        headlines=['Anjum Mart', 'Timeless Style. Everyday Luxury.', 'Free Delivery All Pakistan'],
        desc='Cash on Delivery · WhatsApp us to order',
    ),
}
