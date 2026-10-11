# Anjum Mart — Shopify theme

A custom Online Store 2.0 theme for **Anjum Mart** (`anjummart-mux.myshopify.com`), built for selling
watches, ladies bags, artificial jewellery, dresses and shoes from one store.

It is a native Shopify theme (Liquid + vanilla JavaScript, no build step, no third-party apps), so the
cart, checkout, customer accounts, search, filters and product recommendations all run on Shopify itself.
No API keys or secrets are stored in this repository.

## Brand system (Ivory & Indigo)

| Token | Value | Use |
| --- | --- | --- |
| Background / surface | `#FBF8F3` / `#F3EDE4` | Page and soft sections |
| Text / muted | `#1C1F2A` / derived | Copy |
| Primary (indigo, from the logo blue) | `#14284B` | Buttons, links, announcement bar |
| Detail accent (antique gold) | `#B08D57` | Hairlines and icons only |
| Accent text | `#80602C` | Small labels (AA contrast) |
| Sale and error (crimson) | `#A51C30` | Sale price, badges, errors |
| Success | `#1F6A43` | Discounts, confirmations |
| Fonts | Cormorant (headings) + Jost (body) | Shopify font library |

All are theme settings (*Customize → Theme settings → Colors / Typography*). The logo keeps its own colours and
always sits on a light background. Corners are near-square, shadows are replaced by hairlines, and buttons are
uppercase with letter-spacing.

## What's included

| Area | Details |
| --- | --- |
| Header | Official logo, product search with live suggestions, account link, cart with live item count, mobile drawer menu |
| Homepage | Announcement bar → hero banner → category cards → Featured Products → New Arrivals → promo banner → Best Sellers → Special Offers → service highlights → footer |
| Collections | Banner, Shopify filters (availability, price, product type, plus anything set in Search & Discovery), sorting, numbered pagination, empty states |
| Product page | Gallery with thumbnails/swipe (selected variant's image first), variant buttons that update price, compare-at price, stock and image, quantity, Add to cart, Shopify *Buy it now*, shipping & returns links once policies exist, related products |
| Cart | Branded slide-out cart drawer and full cart page: update quantity (safe with fast taps on several lines), remove, Subtotal → Shopify discounts → Total, savings line, free-shipping progress (from a setting that must match your shipping rates), "Complete your look" recommendations with variant choice and Add to cart, Continue shopping, policy links once policies exist, Shopify checkout |
| Search | Predictive search in the header and a full results page with filters and sorting |
| Other pages | Collections list, contact form, generic pages, blog/article, 404, password page, gift card, classic customer account pages |
| Logo on product photos | The store logo is layered on every product photo (product cards, product gallery, homepage collage), including photos added later. Position, size, opacity and background are theme settings. The image files in Shopify are not changed |
| Animations | Sections and products fade in on scroll, hero entrance, gently moving background shapes, hover lift on cards and buttons, cart count bump. Off automatically for visitors who prefer reduced motion; both can be switched off in theme settings |
| SEO | Canonical URLs, meta descriptions with a store-wide fallback, Open Graph/Twitter tags, Product, Organization, WebSite (search box) and Breadcrumb structured data, image alt text, Google Search Console verification field, fast-loading images |

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
| Best Sellers | `best-sellers` | All priced products, ranked by Shopify's real sales data (newest products until orders exist) |
| Sale | `sale` | Products whose compare-at price is higher than the price |
| Featured Products | `frontpage` | Shopify's existing "Home page" collection, renamed — add products manually |

A navigation menu **Anjum Mart main menu** (`anjum-main-menu`) links Home, the five categories, New Arrivals
and Best Sellers. The live Horizon theme and its menus were not changed.

### Demo catalog

So the store can be previewed fully, 40 demo products were added from Shopify's sample catalogs
(mock.shop photos) and renamed for Anjum Mart: 9 watches (men and women), 8 bags, 9 jewellery pieces,
7 dresses and 7 shoes. Prices are placeholder amounts in PKR, all Rs. 2,000 or more, and a few have a
compare-at price so the Sale section can be seen. Every demo product is tagged **`demo`**; 24 unused
sample items are set to *Draft* and tagged **`demo-unused`**.

To replace them: *Products* → search `tag:demo` → edit or delete. Delete the `demo-unused` drafts the same way.
Review titles, prices, variants and descriptions before selling — they are examples, not real stock.

## Installing / previewing

The theme is uploaded to the store as an **unpublished** theme named *Anjum Mart*:
**Online Store → Themes → Anjum Mart → Preview / Customize → Publish** when ready.

To keep the store in sync with this repository you can instead connect it from GitHub:
**Online Store → Themes → Add theme → Connect from GitHub** → repository `dtpos2026/dt-anjummart`, this branch.
With Shopify CLI: `shopify theme dev --store anjummart-mux` (local preview) or `shopify theme push --unpublished`.

## Checkout on the Basic plan

Shopify only allows checkout styling through code (Checkout Branding API, checkout UI extensions on the
information/shipping/payment steps) on **Shopify Plus**. On Basic:

* Set the logo, colours and fonts in **Settings → Checkout → Customize** (checkout editor). Use the palette above.
* Thank-you and Order status page extensions are allowed on Basic but need a Shopify app (built with Shopify CLI).
* The theme never replaces or simulates checkout; the cart sends shoppers to Shopify's secure checkout.

## Things the store owner needs to do

1. **Add products.** Give each one a product type (or tag) from the table above so it lands in the right
   category. Add compare-at prices only for real discounts — the Sale badge and *x% off* are calculated from them.
2. **Write store policies** in *Settings → Policies*. Only a Privacy policy exists today. Shipping, Refund and
   Terms of Service links appear in the footer and on product pages automatically once written.
3. **Payments, Cash on Delivery, shipping rates and taxes** are configured in Shopify *Settings*. The theme
   makes no delivery or payment promises of its own.
4. **Remove the storefront password** (*Online Store → Preferences*) when ready to sell. Search engines
   cannot see the store while it is password protected.
5. **Connect the domain anjummart.com** in *Settings → Domains → Connect existing domain* and follow the DNS
   steps for your domain provider, then set it as the primary domain. Canonical links, sitemap and structured
   data switch to it automatically.
6. **Google:** add the domain in Google Search Console (DNS verification, or paste the HTML-tag code into
   *Theme settings → SEO and sharing*), then submit `https://anjummart.com/sitemap.xml`. Shopify generates the
   sitemap and robots.txt. Set the homepage title and description in *Online Store → Preferences*. Indexing
   takes from a few days to a few weeks; rankings depend on content and links and cannot be guaranteed.
7. **Theme settings** (*Customize → Theme settings*): phone number, WhatsApp number (WhatsApp links stay hidden
   until a number is entered), address, support hours, social profile links (icons appear only for profiles entered).
8. **Homepage images** (*Customize → Home page*): upload campaign photos for the hero and promo banner and,
   optionally, category images. Until then the hero shows a collage of real product photos from New Arrivals,
   and category cards use the collection's first product image or a branded tile.
9. Optional: install Shopify **Search & Discovery** to add filters (colour, size, brand) and tune related products.

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
