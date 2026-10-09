# Anjum Mart — Shopify theme

A custom Online Store 2.0 theme for **Anjum Mart** (`anjummart-mux.myshopify.com`), built for selling
watches, ladies bags, artificial jewellery, dresses and shoes from one store.

It is a native Shopify theme (Liquid + vanilla JavaScript, no build step, no third-party apps), so the
cart, checkout, customer accounts, search, filters and product recommendations all run on Shopify itself.
No API keys or secrets are stored in this repository.

## What's included

| Area | Details |
| --- | --- |
| Header | Official logo, product search with live suggestions, account link, cart with live item count, mobile drawer menu |
| Homepage | Announcement bar → hero banner → category cards → Featured Products → New Arrivals → promo banner → Best Sellers → Special Offers → service highlights → footer |
| Collections | Banner, Shopify filters (availability, price, product type, plus anything set in Search & Discovery), sorting, numbered pagination, empty states |
| Product page | Gallery with thumbnails/swipe, variant buttons that update price, compare-at price, stock and image, quantity, Add to cart, Shopify *Buy it now*, shipping & returns info, related products |
| Cart | Slide-out cart drawer and full cart page: update quantity, remove, subtotal, Shopify checkout |
| Search | Predictive search in the header and a full results page with filters and sorting |
| Other pages | Collections list, contact form, generic pages, blog/article, 404, password page, gift card, classic customer account pages |

Everything shown to shoppers comes from real Shopify data. Sections that would be empty (for example
**Special Offers** when nothing is on sale) hide themselves on the live store instead of showing placeholders.

## Store setup already done

Created in Shopify admin through the Admin API:

| Collection | Handle | How products get in |
| --- | --- | --- |
| Watches | `watches` | Product type **Watches** *or* tag `watches` |
| Ladies Bags | `ladies-bags` | Product type **Ladies Bags** *or* tag `ladies-bags` |
| Artificial Jewellery | `artificial-jewellery` | Product type **Artificial Jewellery** *or* tag `artificial-jewellery` |
| Dresses | `dresses` | Product type **Dresses** *or* tag `dresses` |
| Shoes | `shoes` | Product type **Shoes** *or* tag `shoes` |
| New Arrivals | `new-arrivals` | All priced products, newest first |
| Best Sellers | `best-sellers` | All priced products, ranked by Shopify's real sales data |
| Sale | `sale` | Products whose compare-at price is higher than the price |
| Featured Products | `frontpage` | Shopify's existing "Home page" collection, renamed — add products manually |

A navigation menu **Anjum Mart main menu** (`anjum-main-menu`) links Home, the five categories, New Arrivals
and Best Sellers. The live Horizon theme and its menus were not changed.

## Installing / previewing

The theme is uploaded to the store as an **unpublished** theme named *Anjum Mart*:
**Online Store → Themes → Anjum Mart → Preview / Customize → Publish** when ready.

To keep the store in sync with this repository you can instead connect it from GitHub:
**Online Store → Themes → Add theme → Connect from GitHub** → repository `dtpos2026/dt-anjummart`, this branch.
With Shopify CLI: `shopify theme dev --store anjummart-mux` (local preview) or `shopify theme push --unpublished`.

## Things the store owner needs to do

1. **Add products.** Give each one a product type (or tag) from the table above so it lands in the right
   category. Add compare-at prices only for real discounts — the Sale badge and *x% off* are calculated from them.
2. **Write store policies** in *Settings → Policies*. Only a Privacy policy exists today. Shipping, Refund and
   Terms of Service links appear in the footer and on product pages automatically once written.
3. **Payments, Cash on Delivery, shipping rates and taxes** are configured in Shopify *Settings*. The theme
   makes no delivery or payment promises of its own.
4. **Upgrade from the trial plan** and remove the storefront password before selling.
5. **Theme settings** (*Customize → Theme settings*): phone number, WhatsApp number (WhatsApp links stay hidden
   until a number is entered), address, support hours, social profile links (icons appear only for profiles entered).
6. **Homepage images** (*Customize → Home page*): upload campaign photos for the hero and promo banner and,
   optionally, category images. Until then the hero shows a collage of real product photos from New Arrivals,
   and category cards use the collection's first product image or a branded tile.
7. Optional: install Shopify **Search & Discovery** to add filters (colour, size, brand) and tune related products.

Not built on purpose: **wishlist** (no wishlist integration exists — install a wishlist app if needed) and
**product reviews** (no review app; the theme never shows ratings it doesn't have).

## Development

```
assets/      base.css, collection.css, product.css, theme.js, logo + favicons
config/      settings_schema.json, settings_data.json
layout/      theme.liquid, password.liquid
locales/     en.default.json (all storefront text)
sections/    page sections + header/footer groups
snippets/    product card, price, cart line, facets, icons, logo …
templates/   JSON templates (+ customers/*, gift_card.liquid)
```

Lint with `shopify theme check`. Brand colours, fonts, card image ratio and cart behaviour are theme
settings, so they can be changed in the theme editor without code.
