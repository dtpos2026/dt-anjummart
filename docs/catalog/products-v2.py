# Anjum Mart: in-stock catalogue (supplied by the owner on 17 Oct 2026). Text comes from the owner's product posts;
# the two items without a post (RUSTET gold/black-roman and silver/green-roman) are described only from what the photo shows.
# Stock: 10 pieces each. Photos: PDF pages 1-11, normalised to 1200x1600 on white.
import json, re

DELIVERY = ('<h3>Price &amp; Delivery</h3><ul>'
            '<li><strong>Price:</strong> Rs. {price:,}</li>'
            '<li><strong>Delivery charges:</strong> FREE</li>'
            '<li><strong>Delivery coverage:</strong> All over Pakistan</li>'
            '<li><strong>Payment:</strong> Cash on Delivery available</li>'
            '<li><strong>Return policy:</strong> No returns accepted (a damaged or wrong item is replaced when reported within 48 hours, see our '
            '<a href="/pages/refund-policy">Return and Refund Policy</a>)</li></ul>'
            '<p><strong>Anjum Mart &ndash; Premium Style at Affordable Prices!</strong></p>')


def ul(items):
    return '<ul>' + ''.join(f'<li>{i}</li>' for i in items) + '</ul>'


def specs(rows):
    return '<ul>' + ''.join(f'<li><strong>{k}:</strong> {v}</li>' for k, v in rows) + '</ul>'


def build_html(p):
    h = ''.join(f'<p>{t}</p>' for t in p['intro'])
    h += '<h3>Product Specifications</h3>' + specs(p['specs'])
    if p.get('includes'):
        h += '<h3>Set Includes</h3>' + ul(p['includes'])
    h += '<h3>Key Features</h3>' + ul(p['features'])
    h += DELIVERY.format(price=p['price'])
    return h


MENS = ['watches', 'mens-watches', 'men', 'rustet']
LADIES = ['watches', 'womens-watches', 'women', 'moonston']
JEW = ['artificial-jewellery', 'jewellery', 'women', 'bridal', 'necklace-set']

PRODUCTS = [
    {'img': 1, 'handle': 'rustet-two-tone-gold-silver-mens-watch-white-dial', 'vendor': 'RUSTET', 'type': 'Watches', 'price': 3999,
     'sku': 'RST-TT-WHT', 'tags': MENS + ['two-tone', 'gold', 'white-dial'],
     'title': "RUSTET Premium Two-Tone Gold & Silver Men's Quartz Watch – White Dial",
     'intro': ["Enhance your everyday look with the RUSTET Premium Two-Tone Wristwatch, featuring a beautiful white dial, gold-tone bezel and an elegant silver-and-gold metal bracelet.",
               "Powered by quartz movement, this stylish timepiece features an analog display and a convenient date window.",
               "Perfect for office wear, business meetings, casual outings and special occasions."],
     'specs': [('Brand', 'RUSTET'), ('Model / Style', 'Classic Two-Tone Quartz Watch'), ('Movement', 'Quartz'), ('Display', 'Analog'),
               ('Dial colour', 'White / Silver'), ('Case colour', 'Gold tone'), ('Strap colour', 'Silver &amp; Gold'), ('Strap type', 'Metal link bracelet'),
               ('Case shape', 'Rounded octagonal'), ('Special feature', 'Date display'), ('Water resistance', 'Marked water resistant (rating not specified)'),
               ('Style', 'Casual, formal &amp; business wear')],
     'features': ['Beautiful white dial', 'Gold-tone bezel with silver-and-gold bracelet', 'Quartz movement', 'Convenient date window', 'Suitable for office, business and casual wear']},
    {'img': 2, 'handle': 'rustet-gold-silver-mens-watch-royal-blue-dial', 'vendor': 'RUSTET', 'type': 'Watches', 'price': 3999,
     'sku': 'RST-TT-BLU', 'tags': MENS + ['two-tone', 'gold', 'blue-dial', 'day-date'],
     'title': "RUSTET Premium Gold & Silver Men's Watch – Royal Blue Dial | Day & Date Display",
     'intro': ["Make a stylish statement with the RUSTET Premium Two-Tone Men's Wristwatch, featuring a stunning royal blue dial, elegant gold-tone bezel, and sophisticated silver-and-gold metal bracelet.",
               "The distinctive rounded-square case and beautiful gold-tone hour markers create a timeless, luxurious appearance.",
               "Featuring a convenient Day &amp; Date Display, this watch combines everyday practicality with classic elegance.",
               "Perfect for office wear, business meetings, casual outings, special occasions, and gifting."],
     'specs': [('Brand', 'RUSTET'), ('Model / Style', 'Classic Two-Tone Royal Blue Watch'), ('Category', "Men's wristwatch"), ('Display type', 'Analog'),
               ('Dial colour', 'Royal blue'), ('Case colour', 'Gold &amp; Silver'), ('Bracelet colour', 'Silver &amp; Gold'), ('Bracelet type', 'Metal link bracelet'),
               ('Case shape', 'Rounded square / octagonal'), ('Dial markers', 'Gold-tone hour markers'), ('Hands', 'Gold-tone analog hands'),
               ('Special feature', 'Day &amp; Date display'), ('Design', 'Two-tone premium finish'), ('Style', 'Casual, formal &amp; business wear')],
     'features': ['Elegant royal blue dial', 'Premium gold &amp; silver two-tone design', 'Stylish metal link bracelet', 'Convenient Day &amp; Date display', 'Classic analog time display', 'Perfect for casual &amp; formal wear']},
    {'img': 7, 'handle': 'rustet-silver-mens-watch-emerald-green-dial', 'vendor': 'RUSTET', 'type': 'Watches', 'price': 3999,
     'sku': 'RST-SLV-GRN', 'tags': MENS + ['silver', 'steel', 'green-dial', 'day-date'],
     'title': "RUSTET Premium Silver Men's Quartz Watch – Emerald Green Dial | Day & Date Display",
     'intro': ["Experience timeless elegance with the RUSTET Premium Silver Men's Quartz Wristwatch, featuring a striking emerald green sunburst dial and a beautifully polished silver-tone finish.",
               "The eye-catching green dial features a sophisticated textured pattern, elegant silver-tone hour markers and a convenient Day &amp; Date Display positioned at 3 o'clock.",
               "Powered by Quartz Movement, this watch combines classic design with practical everyday functionality.",
               "Its stylish silver metal bracelet and distinctive case design make it an excellent accessory for office wear, business meetings, casual outings, weddings and special occasions."],
     'specs': [('Brand', 'RUSTET'), ('Model / Style', 'Classic Silver Green Dial Quartz Watch'), ('Category', "Men's wristwatch"), ('Movement', 'Quartz'), ('Display type', 'Analog'),
               ('Dial colour', 'Emerald green (sunburst finish)'), ('Case colour', 'Silver tone'), ('Bracelet colour', 'Silver'), ('Bracelet type', 'Metal link bracelet'),
               ('Case shape', 'Angular case with round dial'), ('Dial markers', 'Silver-tone hour markers'), ('Watch hands', 'Silver tone'),
               ('Special feature', 'Day &amp; Date display'), ('Day &amp; Date position', "3 o'clock"), ('Bezel', 'Polished silver-tone decorative bezel'),
               ('Style', 'Casual, formal &amp; business wear')],
     'features': ['Stunning emerald green sunburst dial', 'Elegant full silver-tone finish', 'Reliable quartz movement', 'Convenient Day &amp; Date display', 'Stylish metal link bracelet',
                  'Beautiful textured dial design', 'Classic silver-tone hour markers', 'Suitable for casual &amp; formal wear']},
    {'img': 6, 'handle': 'rustet-all-black-mens-watch-black-dial', 'vendor': 'RUSTET', 'type': 'Watches', 'price': 3999,
     'sku': 'RST-BLK', 'tags': MENS + ['black', 'black-dial', 'day-date'],
     'title': "RUSTET Premium All-Black Men's Quartz Watch – Black Dial | Day & Date Display",
     'intro': ["Upgrade your everyday style with the RUSTET Premium All-Black Men's Quartz Wristwatch, featuring a sophisticated black dial, glossy black case and distinctive geometric-pattern metal bracelet.",
               "The elegant black dial is beautifully detailed with silver-tone Roman numerals, sparkling crystal-style hour markers and polished silver-tone hands, creating a bold and luxurious appearance.",
               "Featuring Quartz Movement and a convenient Day &amp; Date Display, this watch combines classic styling with practical everyday functionality.",
               "Its eye-catching all-black finish and unique diamond-pattern bracelet make it an excellent accessory for office wear, business meetings, formal events, weddings, parties and casual outings."],
     'specs': [('Brand', 'RUSTET'), ('Model / Style', 'Classic All-Black Quartz Watch'), ('Category', "Men's wristwatch"), ('Movement', 'Quartz'), ('Display type', 'Analog'),
               ('Dial colour', 'Classic black'), ('Case colour', 'Glossy black'), ('Bracelet colour', 'Black'), ('Bracelet type', 'Metal link bracelet'),
               ('Bracelet design', 'Geometric diamond-pattern links'), ('Case shape', 'Round dial with faceted angular case'),
               ('Dial markers', 'Roman numerals &amp; crystal-style accents'), ('Watch hands', 'Silver tone'), ('Special feature', 'Day &amp; Date display'),
               ('Day &amp; Date position', "3 o'clock"), ('Bezel', 'Decorative faceted black bezel'), ('Style', 'Casual, formal &amp; business wear')],
     'features': ['Premium all-black design', 'Elegant black dial with silver-tone details', 'Quartz movement', 'Convenient Day &amp; Date display', 'Stylish geometric-pattern metal bracelet',
                  'Roman numeral &amp; crystal-style hour markers', 'Decorative faceted black bezel', 'Suitable for casual &amp; formal wear']},
    {'img': 3, 'handle': 'rustet-gold-mens-watch-black-dial-roman-numerals', 'vendor': 'RUSTET', 'type': 'Watches', 'price': 3999,
     'sku': 'RST-GLD-BLK', 'tags': MENS + ['gold', 'black-dial', 'day-date'],
     'title': "RUSTET Premium Gold Men's Quartz Watch – Black Dial, Roman Numerals | Day & Date Display",
     'intro': ["Make a bold statement with the RUSTET Premium Gold Men's Quartz Wristwatch, featuring a deep black dial, gold-tone Roman numerals and crystal-style hour markers set against a full gold-tone case and bracelet.",
               "The engraved Roman-numeral bezel adds a distinctive look, and the Day &amp; Date window keeps everyday timekeeping convenient.",
               "Perfect for weddings, parties, business meetings, special occasions and gifting."],
     'specs': [('Brand', 'RUSTET'), ('Category', "Men's wristwatch"), ('Movement', 'Quartz'), ('Display type', 'Analog'), ('Dial colour', 'Black'),
               ('Case colour', 'Gold tone'), ('Bracelet colour', 'Gold tone'), ('Bracelet type', 'Metal link bracelet'),
               ('Dial markers', 'Gold-tone Roman numerals &amp; crystal-style accents'), ('Bezel', 'Engraved Roman-numeral bezel'),
               ('Special feature', 'Day &amp; Date display'), ('Style', 'Casual, formal &amp; party wear')],
     'features': ['Bold black dial with gold-tone Roman numerals', 'Full gold-tone case and bracelet', 'Engraved Roman-numeral bezel', 'Quartz movement', 'Day &amp; Date display', 'Suitable for formal and festive occasions']},
    {'img': 4, 'handle': 'rustet-silver-mens-watch-green-dial-roman-numerals', 'vendor': 'RUSTET', 'type': 'Watches', 'price': 3999,
     'sku': 'RST-SLV-GRN2', 'tags': MENS + ['silver', 'steel', 'green-dial', 'day-date'],
     'title': "RUSTET Premium Silver Men's Quartz Watch – Green Dial, Roman Numerals | Day & Date Display",
     'intro': ["Add a refined touch to your wrist with the RUSTET Premium Silver Men's Quartz Wristwatch, featuring a rich green sunburst dial with Roman numerals and crystal-style accents, framed by a polished silver-tone ridged bezel.",
               "The Day &amp; Date window and the full stainless-look silver bracelet make this a practical watch for everyday and formal wear.",
               "Perfect for office wear, business meetings, special occasions and gifting."],
     'specs': [('Brand', 'RUSTET'), ('Category', "Men's wristwatch"), ('Movement', 'Quartz'), ('Display type', 'Analog'), ('Dial colour', 'Green (sunburst finish)'),
               ('Case colour', 'Silver tone'), ('Bracelet colour', 'Silver'), ('Bracelet type', 'Metal link bracelet'),
               ('Dial markers', 'Roman numerals &amp; crystal-style accents'), ('Bezel', 'Ridged silver-tone bezel'), ('Special feature', 'Day &amp; Date display'),
               ('Style', 'Casual, formal &amp; business wear')],
     'features': ['Rich green sunburst dial', 'Roman numerals with crystal-style accents', 'Polished silver-tone finish', 'Quartz movement', 'Day &amp; Date display', 'Suitable for casual &amp; formal wear']},
    {'img': 9, 'handle': 'moonston-rose-gold-ladies-watch-pink-dial-luxury-crystal-style', 'vendor': 'MOONSTON', 'type': 'Watches', 'price': 2999,
     'sku': 'MNS-PNK-1', 'tags': LADIES + ['rose-gold', 'pink-dial', 'crystal-style'],
     'title': 'MOONSTON Premium Rose Gold Ladies Quartz Watch – Pink Dial | Luxury Crystal-Style Design',
     'intro': ["Add a touch of elegance and glamour to your everyday style with the MOONSTON Premium Rose Gold Ladies Quartz Watch, featuring a stunning pink-lavender dial, beautiful rose-gold-tone finish and sparkling crystal-style detailing.",
               "The elegant round dial is decorated with stylish Roman numeral markers, while the crystal-style embellished bezel creates a sophisticated and luxurious appearance.",
               "Its beautifully designed rose-gold-tone metal bracelet features sparkling decorative accents, giving this watch a stunning jewellery-inspired look.",
               "Powered by Quartz Movement, this fashionable timepiece combines classic analog timekeeping with timeless elegance.",
               "Perfect for weddings, parties, formal gatherings, celebrations, special occasions and everyday fashion. It also makes a beautiful gift for birthdays, anniversaries and special moments."],
     'specs': [('Brand', 'MOONSTON'), ('Model / Style', 'Premium Rose Gold Crystal-Style Ladies Watch'), ('Category', "Women's wristwatch"), ('Movement', 'Quartz'), ('Display type', 'Analog'),
               ('Dial colour', 'Pink / Lavender'), ('Case colour', 'Rose gold tone'), ('Bracelet colour', 'Rose gold tone'), ('Bracelet type', 'Decorative metal link bracelet'),
               ('Bracelet design', 'Crystal-style studded links'), ('Case shape', 'Round'), ('Dial markers', 'Crystal-style Roman numerals'), ('Watch hands', 'Rose gold tone'),
               ('Bezel design', 'Sparkling crystal-style bezel'), ('Dial finish', 'Elegant sunburst effect'), ('Style', 'Luxury, casual, formal, party &amp; fashion wear')],
     'features': ['Beautiful pink-lavender sunburst dial', 'Elegant rose gold-tone finish', 'Quartz movement', 'Sparkling crystal-style bezel', 'Crystal-style studded metal bracelet',
                  'Decorative Roman numeral hour markers', 'Elegant rose gold-tone hands', 'Stylish jewellery-inspired design', 'Perfect for weddings, parties &amp; everyday wear']},
    {'img': 8, 'handle': 'moonston-rose-gold-ladies-watch-pink-dial-crystal-style-luxury', 'vendor': 'MOONSTON', 'type': 'Watches', 'price': 2999,
     'sku': 'MNS-PNK-2', 'tags': LADIES + ['rose-gold', 'pink-dial', 'crystal-style'],
     'title': 'MOONSTON Premium Rose Gold Ladies Quartz Watch – Pink Dial | Crystal-Style Luxury Design',
     'intro': ["Add a touch of glamour and sophistication to your style with the MOONSTON Premium Rose Gold Ladies Quartz Watch, featuring a beautiful pink-lavender dial, elegant rose-gold-tone finish and sparkling crystal-style detailing.",
               "The stunning round dial features decorative Roman numeral markers and delicate gold-tone hands, creating a graceful and fashionable appearance.",
               "Its beautifully designed metal bracelet is decorated with sparkling crystal-style accents, giving this watch a luxurious jewellery-inspired look.",
               "Powered by Quartz Movement, this stylish timepiece combines classic analog timekeeping with an elegant design.",
               "Perfect for weddings, parties, celebrations, formal gatherings, special occasions and everyday fashion. It also makes a beautiful gift for someone special."],
     'specs': [('Brand', 'MOONSTON'), ('Model / Style', 'Luxury Rose Gold Crystal-Style Ladies Watch'), ('Category', "Women's wristwatch"), ('Movement', 'Quartz'), ('Display type', 'Analog'),
               ('Dial colour', 'Pink / Lavender'), ('Case colour', 'Rose gold tone'), ('Bracelet colour', 'Rose gold tone'), ('Bracelet type', 'Decorative metal link bracelet'),
               ('Bracelet design', 'Crystal-style studded links'), ('Case shape', 'Round'), ('Dial markers', 'Crystal-style Roman numerals'), ('Watch hands', 'Gold tone'),
               ('Bezel design', 'Sparkling crystal-style decorative bezel'), ('Dial finish', 'Elegant sunburst effect'), ('Style', 'Luxury, fashion, casual, formal &amp; party wear')],
     'features': ['Beautiful pink-lavender sunburst dial', 'Elegant rose gold-tone finish', 'Quartz movement', 'Sparkling crystal-style studded bezel', 'Decorative crystal-style metal bracelet',
                  'Stylish Roman numeral markers', 'Elegant gold-tone watch hands', 'Luxury jewellery-inspired design', 'Perfect for weddings, parties &amp; special occasions']},
    {'img': 5, 'handle': 'moonston-two-tone-ladies-watch-emerald-green-dial', 'vendor': 'MOONSTON', 'type': 'Watches', 'price': 2999,
     'sku': 'MNS-GRN', 'tags': LADIES + ['rose-gold', 'two-tone', 'green-dial', 'crystal-style'],
     'title': 'MOONSTON Premium Two-Tone Ladies Quartz Watch – Emerald Green Dial',
     'intro': ["Add a touch of luxury and elegance to your everyday style with the MOONSTON Premium Two-Tone Ladies Quartz Watch, featuring a stunning emerald green dial, beautiful rose-gold accents and a sophisticated silver-and-rose-gold metal bracelet.",
               "The elegant round dial is decorated with sparkling crystal-style Roman numeral markers, while the beautifully embellished bezel and bracelet create a glamorous, premium appearance.",
               "Powered by Quartz Movement, this fashionable timepiece combines timeless beauty with everyday functionality.",
               "Its eye-catching two-tone design makes it a wonderful choice for weddings, parties, formal gatherings, casual outings and special occasions. A stylish accessory that also makes a beautiful gift for someone special."],
     'specs': [('Brand', 'MOONSTON'), ('Model / Style', 'Premium Two-Tone Ladies Quartz Watch'), ('Category', "Women's wristwatch"), ('Movement', 'Quartz'), ('Display type', 'Analog'),
               ('Dial colour', 'Emerald green'), ('Case colour', 'Rose gold tone'), ('Bracelet colour', 'Silver &amp; Rose gold'), ('Bracelet type', 'Metal link bracelet'),
               ('Case shape', 'Round'), ('Dial markers', 'Crystal-style Roman numerals'), ('Watch hands', 'Rose gold tone'), ('Bezel design', 'Crystal-style studded bezel'),
               ('Bracelet design', 'Crystal-style decorative links'), ('Style', 'Casual, formal, party &amp; fashion wear')],
     'features': ['Beautiful emerald green dial', 'Elegant silver &amp; rose gold two-tone finish', 'Quartz movement', 'Stylish crystal-style Roman numeral markers', 'Sparkling decorative bezel',
                  'Premium-look metal link bracelet', 'Elegant &amp; fashionable ladies design', 'Perfect for weddings, parties &amp; everyday wear']},
    {'img': 10, 'handle': 'silver-white-mirror-stone-jewellery-set-necklace-earrings-maang-tikka', 'vendor': 'Anjum Mart', 'type': 'Artificial Jewellery', 'price': 1999,
     'sku': 'JWL-SLV-WHT', 'tags': JEW + ['silver', 'mirror-stone', 'pearl'],
     'title': 'Premium Silver & White Mirror Stone Jewellery Set – Necklace, Earrings & Maang Tikka | Elegant Bridal Collection',
     'intro': ["Add timeless elegance to your traditional look with this Premium Silver &amp; White Mirror Stone Jewellery Set, featuring a beautifully designed necklace, matching earrings and an elegant maang tikka.",
               "This stunning jewellery set showcases intricate silver-tone detailing, sparkling mirror-style stones, crystal-style accents and delicate pearl-white bead drops.",
               "The beautifully arranged floral patterns and reflective decorative stones create a graceful and sophisticated appearance.",
               "Its elegant silver-and-white colour combination makes it a wonderful accessory for traditional outfits, bridal functions and festive celebrations.",
               "Perfect for weddings, engagements, Mehndi functions, Eid celebrations, parties and other special occasions. This coordinated jewellery set also makes a lovely gift for someone special."],
     'specs': [('Product name', 'Silver &amp; White Mirror Stone Jewellery Set'), ('Category', "Women's fashion jewellery"), ('Jewellery type', 'Traditional necklace set'), ('Colour', 'Silver &amp; White'),
               ('Necklace style', 'Traditional statement necklace'), ('Stone design', 'Reflective mirror-style stones with crystal-style accents'), ('Bead colour', 'Pearl white'),
               ('Finish', 'Elegant silver-tone finish'), ('Earring style', 'Traditional dangling earrings'), ('Maang tikka', 'Matching decorative design'),
               ('Design details', 'Floral patterns, mirror-style stones &amp; white bead drops'), ('Style', 'Bridal, traditional, festive &amp; party wear')],
     'includes': ['1 &times; Elegant silver-tone necklace', '1 &times; Pair of matching earrings', '1 &times; Matching maang tikka'],
     'features': ['Elegant silver &amp; white colour combination', 'Beautiful mirror-style stone work', 'Traditional statement necklace', 'Matching earrings &amp; maang tikka', 'Decorative pearl-white bead drops',
                  'Intricate floral design', 'Sparkling crystal-style accents', 'Suitable for bridal &amp; party wear', 'Perfect for weddings, Eid &amp; festive occasions']},
    {'img': 11, 'handle': 'green-gold-traditional-bridal-jewellery-set-necklace-earrings-maang-tikka', 'vendor': 'Anjum Mart', 'type': 'Artificial Jewellery', 'price': 1999,
     'sku': 'JWL-GRN-GLD', 'tags': JEW + ['gold', 'green', 'choker'],
     'title': 'Premium Green & Gold Traditional Bridal Jewellery Set – Necklace, Earrings & Maang Tikka',
     'intro': ["Complete your traditional look with this Premium Green &amp; Gold Bridal Jewellery Set, featuring an elegant choker necklace, beautifully designed matching earrings and a stunning maang tikka.",
               "This eye-catching jewellery set showcases intricate gold-tone detailing, vibrant emerald-green artificial stones, sparkling crystal-style accents and beautiful green bead drops.",
               "The decorative choker necklace creates a graceful traditional appearance, while the matching earrings and maang tikka complete the coordinated look.",
               "Perfect for brides, wedding guests and anyone who loves elegant ethnic jewellery. Whether you're attending a wedding, Mehndi, engagement, Eid celebration or festive gathering, this stunning jewellery set adds a beautiful finishing touch to your outfit."],
     'specs': [('Product name', 'Green &amp; Gold Traditional Jewellery Set'), ('Category', "Women's fashion jewellery"), ('Jewellery type', 'Traditional choker necklace set'), ('Colour', 'Gold tone &amp; Emerald green'),
               ('Necklace design', 'Traditional choker style'), ('Stone design', 'Emerald-green artificial stones with white crystal-style accents'), ('Bead colour', 'Emerald green'),
               ('Finish', 'Elegant gold-tone finish'), ('Earring style', 'Traditional dangling earrings'), ('Maang tikka', 'Matching traditional design'),
               ('Design details', 'Intricate decorative patterns &amp; green bead drops'), ('Style', 'Bridal, traditional, festive &amp; party wear')],
     'includes': ['1 &times; Traditional choker necklace', '1 &times; Pair of matching earrings', '1 &times; Matching maang tikka'],
     'features': ['Elegant gold &amp; emerald green colour combination', 'Beautiful traditional choker necklace', 'Matching earrings &amp; maang tikka', 'Sparkling crystal-style decorative details',
                  'Stylish green bead drops', 'Intricate traditional design', 'Ideal for weddings, Mehndi &amp; festive events', 'Beautiful jewellery set for gifting']},
]

if __name__ == '__main__':
    for p in PRODUCTS:
        p['title'] = p['title'].replace('&amp;', '&')
        assert p['price'] > 0 and len(p['handle']) < 80
        p['descriptionHtml'] = build_html(p)
    assert len({p['handle'] for p in PRODUCTS}) == len(PRODUCTS) and len({p['sku'] for p in PRODUCTS}) == len(PRODUCTS)
    json.dump(PRODUCTS, open('products-v2.json', 'w'), indent=1, ensure_ascii=False)
    print(len(PRODUCTS), 'products;', sum(len(p['descriptionHtml']) for p in PRODUCTS), 'chars of description HTML')
