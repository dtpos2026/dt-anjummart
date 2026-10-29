# Perfumes supplied by the owner on 29 Oct 2026 (stock arriving; created as DRAFT with inventory 0, photos added separately).
# Text comes only from the owner's posts. "Original Luxury Scent" is deliberately NOT repeated (authenticity claim).
import json

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


def html(p):
    h = ''.join(f'<p>{t}</p>' for t in p['intro'])
    h += '<h3>Product Specifications</h3>' + specs(p['specs'])
    h += '<h3>Key Features</h3>' + ul(p['features'])
    return h + DELIVERY.format(price=p['price'])


PERFUMES = [
    {'handle': 'lady-aura-by-anjum-eau-de-parfum-50ml-for-women', 'sku': 'LADY-AURA-50', 'price': 3450,
     'title': 'Lady Aura by Anjum – Eau de Parfum 50ml for Women | Premium Floral Fragrance',
     'tags': ['perfume', 'fragrance', 'eau-de-parfum', 'womens-fragrance', 'floral', 'lady-aura', 'anjum', '50ml'],
     'seo_title': 'Lady Aura by Anjum – Eau de Parfum 50ml for Women | Anjum Mart',
     'seo_desc': 'Lady Aura by Anjum: 50 ml Eau de Parfum for women, a premium floral fragrance oil, 10-12 hours long lasting. Free delivery all over Pakistan, Cash on Delivery.',
     'intro': ['Lady Aura by Anjum is a 50 ml Eau de Parfum for women, a premium floral fragrance oil with a luxury feel.',
               'Made to last: 10 to 12 hours of long-lasting fragrance (as stated by the brand; how long a scent lasts varies from person to person).'],
     'specs': [('Brand', 'Anjum'), ('Name', 'Lady Aura'), ('Type', 'Eau de Parfum'), ('Size', '50 ml (1.7 fl oz)'), ('For', 'Women'),
               ('Fragrance', 'Premium floral fragrance oil'), ('Longevity', '10 to 12 hours')],
     'features': ['10 to 12 hours long lasting', '50 ml Eau de Parfum', 'For women', 'Premium floral fragrance oil', 'Luxury scent']},
    {'handle': 'oud-aura-by-anjum-eau-de-parfum-50ml-unisex', 'sku': 'OUD-AURA-50', 'price': 3450,
     'title': 'Oud Aura by Anjum – Eau de Parfum 50ml Unisex | Premium Oud Fragrance',
     'tags': ['perfume', 'fragrance', 'eau-de-parfum', 'unisex-fragrance', 'oud', 'oud-aura', 'anjum', '50ml'],
     'seo_title': 'Oud Aura by Anjum – Eau de Parfum 50ml Unisex | Anjum Mart',
     'seo_desc': 'Oud Aura by Anjum: 50 ml unisex Eau de Parfum, a premium oud fragrance oil, 10-12 hours long lasting. Free delivery all over Pakistan, Cash on Delivery.',
     'intro': ['Oud Aura by Anjum is a 50 ml unisex Eau de Parfum, a premium oud fragrance oil with a luxury feel.',
               'Made to last: 10 to 12 hours of long-lasting fragrance (as stated by the brand; how long a scent lasts varies from person to person).'],
     'specs': [('Brand', 'Anjum'), ('Name', 'Oud Aura'), ('Type', 'Eau de Parfum'), ('Size', '50 ml (1.7 fl oz)'), ('For', 'Unisex (men and women)'),
               ('Fragrance', 'Premium oud fragrance oil'), ('Longevity', '10 to 12 hours')],
     'features': ['10 to 12 hours long lasting', '50 ml Eau de Parfum', 'Unisex', 'Premium oud fragrance oil', 'Luxury scent']},
    {'handle': 'tea-rose-by-anjum-eau-de-parfum-50ml-for-women', 'sku': 'TEA-ROSE-50', 'price': 3450,
     'title': 'Tea Rose by Anjum – Eau de Parfum 50ml for Women | Premium Fragrance Oil',
     'tags': ['perfume', 'fragrance', 'eau-de-parfum', 'womens-fragrance', 'tea-rose', 'anjum', '50ml'],
     'seo_title': 'Tea Rose by Anjum – Eau de Parfum 50ml for Women | Anjum Mart',
     'seo_desc': 'Tea Rose by Anjum: 50 ml Eau de Parfum for women, a premium fragrance oil, 10-12 hours long lasting. Free delivery all over Pakistan, Cash on Delivery.',
     'intro': ['Tea Rose by Anjum is a 50 ml Eau de Parfum for women, a premium fragrance oil with a luxury feel.',
               'Made to last: 10 to 12 hours of long-lasting fragrance (as stated by the brand; how long a scent lasts varies from person to person).'],
     'specs': [('Brand', 'Anjum'), ('Name', 'Tea Rose'), ('Type', 'Eau de Parfum'), ('Size', '50 ml (1.7 fl oz)'), ('For', 'Women'),
               ('Fragrance', 'Premium fragrance oil'), ('Longevity', '10 to 12 hours')],
     'features': ['10 to 12 hours long lasting', '50 ml Eau de Parfum', 'For women', 'Premium fragrance oil', 'Luxury scent']},
]

if __name__ == '__main__':
    for p in PERFUMES:
        assert len(p['seo_desc']) <= 160, (len(p['seo_desc']), p['seo_desc'])
        print(p['handle'], len(p['seo_desc']), len(html(p)))
    json.dump([{**p, 'descriptionHtml': html(p)} for p in PERFUMES], open('products-perfumes.json', 'w'), ensure_ascii=False, indent=1)
