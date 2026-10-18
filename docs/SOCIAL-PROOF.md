# Store highlights popup

A small card in the bottom-left corner that rotates every 14 to 28 seconds (about 20 s on average, random), at most
8 per visit, and stops for the rest of the visit when the shopper closes it. It never takes focus, pauses while the
pointer or keyboard focus is on it, hides while a drawer or quick view is open, lifts above the sticky Add to cart bar
on phones and is not rendered on the cart page or in the theme editor.

## What it shows

| Kind | Source | Wording | Can it claim a purchase? |
| --- | --- | --- | --- |
| Product highlight | The first 12 products of the catalogue that are in stock | "In stock", product name, price, "Free delivery" | **No** |
| Delivery fact | Store policy | "Free delivery all over Pakistan", "Cash on Delivery available" | **No** |
| Verified order | The shop metafield `custom.recent_orders` (below) | "Verified order. Someone from Lahore ordered ... 3 hours ago" | Yes, only for a real order |

There are **no demo or sample purchase messages**. "Someone from Lahore just purchased ..." for an order that did not
happen would be a false statement to shoppers (and counts as a misleading claim under consumer-protection and ad
rules), so the popup is built so that it cannot produce one: the purchase wording exists only in the verified-order
path, and that path reads only the metafield. An empty metafield shows no purchase notice at all.

## Verified orders: where the data comes from

Admin, Settings, Custom data, Shop, **Verified recent orders (popup)** (`custom.recent_orders`, JSON). One entry per
real order, newest first, only city, product and time (no names, e-mails or phone numbers):

```json
[
  { "city": "Lahore", "handle": "rustet-gold-mens-watch-black-dial-roman-numerals", "at": "2026-10-18T10:15:00Z" }
]
```

* `handle` is the product's URL handle; entries for products that are not published are ignored.
* `at` is the order time (ISO 8601). Entries older than the number of days set in Theme settings, Store highlights
  popup (default 14), in the future, or with a missing or over-long city are ignored by the theme.
* The list is **not filled automatically yet.** Shopify themes cannot read orders, so an order feed needs either an
  app or a small order-webhook service with its signing secret. Until that is connected, add entries from real
  customer orders (not your own test orders) or ask the assistant to refresh the list from the Admin API.
* Mention in the Privacy policy that recent orders (city and product only) may be shown on the store.

## Theme settings

Theme settings, **Store highlights popup**: on or off, include verified orders, show on phones, notices per visit,
average seconds between notices, days of order history.

## Files

`snippets/social-proof.liquid` (data and strings), `assets/theme.js` `initSocialProof()` (rotation, timing),
`assets/base.css` end of file (`.proof` styles), `layout/theme.liquid` (render), `locales/en.default.json`
(`general.social_proof`). Tests: section 2d of the local suite.
