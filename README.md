# Anjum Mart — Shopify theme

A custom Online Store 2.0 theme for **Anjum Mart** (`mhwk5r-ks.myshopify.com`), built for selling
watches (RUSTET for men, MOONSTON for women) and bridal jewellery sets.

It is a native Shopify theme (Liquid + vanilla JavaScript, no build step, no third-party apps), so the
cart, checkout, customer accounts, search, filters and product recommendations all run on Shopify itself.
No API keys or secrets are stored in this repository.

## Brand system (Black, Gold & White)

| Token | Value | Use |
| --- | --- | --- |
| Background / soft surface | `#FFFFFF` / `#F6F4EF` | Pages and soft sections |
| Text / muted | `#111111` / derived | Copy |
| Primary (ink black) | `#0B0B0B` | Buttons, announcement bar, hero, promo and footer backgrounds |
| Detail accent (gold) | `#C9A24B` | Hairlines, icons, hero and promo buttons, cart badge |
| Accent text | `#7A5C14` | Small gold labels on white (6.2:1 contrast) |
| Gold on black | `#E8CF8A` | Labels and italic headings on dark areas (12.9:1) |
| Sale and error (crimson) | `#A51C30` | Sale price, badges, errors |
| Success | `#1F6A43` | Stock and confirmations |
| Fonts | Cormorant (headings) + Jost (body) | Shopify font library |

All are theme settings (*Customize → Theme settings → Colors / Typography*). The dark layer ("Noir") is the
last block of `assets/base.css`. Corners are near-square, shadows are replaced by hairlines, and buttons are
uppercase with letter-spacing.

**Logo.** `assets/anjum-mart-logo.png` is the Anjum Mart logo recoloured black + gold for light backgrounds;
`assets/anjum-mart-logo-dark.png` is white + gold for dark backgrounds (footer). Only the colours changed;
the shapes are the original artwork. Upload a logo in *Theme settings → Logo* to override both. The favicon,
app icon and social share image are rebuilt from the same artwork.

## What's included

| Area | Details |
| --- | --- |
| Header | Official logo, product search with live suggestions, account link, cart with live item count, mobile drawer menu |
| Homepage | Announcement bar → slideshow (3 slides, arrows, dots, pause button, swipe) → category tiles (Men's, Women's, Jewellery) → Men's Watches grid → "Shop smart / Free delivery" banner → Women's Watches grid → Bridal Jewellery grid → service highlights → footer |
| Product cards | Category label, title, price, "In stock" (from real inventory). On desktop, hovering shows an **ADD TO CART \| QUICK VIEW** bar; on phones a normal Add to cart button sits under the card. Quick view opens a modal (loaded from `sections/quick-view.liquid`) and falls back to the product page if it cannot load |
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
| Men's Watches | `mens-watches` | Tag `mens-watches` |
| Women's Watches | `womens-watches` | Tag `womens-watches` |
| Jewellery | `artificial-jewellery` | Product type **Artificial Jewellery** or tag `artificial-jewellery` |
| Watches | `watches` | Product type **Watches** or tag `watches` |
| New Arrivals | `new-arrivals` | All priced products, newest first |
| Sale | `sale` | Products whose compare-at price is higher than the price (empty until you set one) |

The navigation menu **Anjum Mart main menu** (`anjum-main-menu`) links Home, Men's Watches, Women's Watches,
Jewellery, New Arrivals and Contact. There is deliberately no "Best Sellers" collection: nothing has been sold yet,
so the theme never claims one.

### Catalogue

Eleven products are **Active**, published to the Online Store, priced from the owner's product posts and stocked at
**10 pieces each** (inventory tracked, oversell blocked): six RUSTET men's watches at Rs 3,999, three MOONSTON ladies
watches at Rs 2,999 and two bridal jewellery sets (necklace, earrings, maang tikka) at Rs 1,999. Descriptions are the
owner's own text (the two RUSTET models without a post are described only from what their photos show). The photo
of every product has a pure white background. Catalogue source: `docs/catalog/products-v2.py`. The earlier 14 RUSTET
listings were not confirmed in stock and are kept as **Draft**.

### Shipping and policies

The only domestic shipping rate is **Free Delivery (All Pakistan)**, Rs 0 on every order, to match the product posts.
`docs/policies/*.html` hold the Shipping, Return and Refund, and Terms pages (also live as Shopify Pages): free
delivery, Cash on Delivery, **no returns for change of mind**, and a replacement for a damaged or wrong item when
reported within 48 hours.

## Installing / previewing

The theme is uploaded to the store as an **unpublished** theme named *Anjum Mart*:
**Online Store → Themes → Anjum Mart → Preview / Customize → Publish** when ready.

To keep the store in sync with this repository you can instead connect it from GitHub:
**Online Store → Themes → Add theme → Connect from GitHub** → repository `dtpos2026/dt-anjummart`, this branch.
With Shopify CLI: `shopify theme dev --store mhwk5r-ks` (local preview) or `shopify theme push --unpublished`.

## Checkout on the Basic plan

Shopify only allows checkout styling through code (Checkout Branding API, checkout UI extensions on the
information/shipping/payment steps) on **Shopify Plus**. On Basic:

* Set the logo, colours and fonts in **Settings → Checkout → Customize** (checkout editor). Use the palette above.
* Thank-you and Order status page extensions are allowed on Basic but need a Shopify app (built with Shopify CLI).
* The theme never replaces or simulates checkout; the cart sends shoppers to Shopify's secure checkout.

## Things the store owner needs to do

1. **Keep stock in step with the warehouse** (*Products → Inventory*). A product shows "Sold out" at 0. For new
   products use product type **Watches** (or **Artificial Jewellery**) and the tags `mens-watches`,
   `womens-watches` or `artificial-jewellery` so they land in the right collections. Add compare-at prices only for
   real discounts: the Sale badge and *x% off* are calculated from them.
2. **Paste the policies** from `docs/policies/` into *Settings → Policies* (the assistant cannot write them), so the
   checkout links show them too.
3. **Payments, Cash on Delivery, shipping rates and taxes** are configured in Shopify *Settings*. The theme's
   "free delivery all over Pakistan" and "Cash on Delivery" wording (announcement bar, banner, product pages, cart)
   matches the current rates; if you change the shipping rate, update those texts in the theme editor.
4. **Remove the storefront password** (*Online Store → Preferences*) when ready to sell. Search engines
   cannot see the store while it is password protected.
5. **Connect the domain anjummart.com** in *Settings → Domains → Connect existing domain* and follow the DNS
   steps for your domain provider, then set it as the primary domain. Canonical links, sitemap and structured
   data switch to it automatically.
6. **Google:** add the domain in Google Search Console (DNS verification, or paste the HTML-tag code into
   *Theme settings → SEO and sharing*), then submit `https://anjummart.com/sitemap.xml`. Shopify generates the
   sitemap and robots.txt. Set the homepage title and description in *Online Store → Preferences*. Indexing
   takes from a few days to a few weeks; rankings depend on content and links and cannot be guaranteed.
7. **Theme settings** (*Customize → Theme settings*): the phone, WhatsApp number (+92 371 4661514) and Multan office address
   are already set. Still to add: support hours and the social profile links (Facebook, Instagram, TikTok; each icon
   appears only once its link is entered).
8. **Homepage images** (*Customize → Home page*): the slideshow, category tiles and delivery banner use built-in
   black-and-gold artwork made from the product photos (`assets/slide-*.jpg`, `tile-*.jpg`, `promo-*.jpg`). To use
   your own pictures, upload them in the slide, tile or banner settings; they replace the built-in artwork.
9. Optional: install Shopify **Search & Discovery** to add filters (colour, size, brand) and tune related products.

Not built on purpose: **wishlist** (no wishlist integration exists — install a wishlist app if needed) and
**product reviews** (no review app; the theme never shows ratings it doesn't have).

## Development

```
assets/      base.css, home.css, collection.css, product.css, theme.js, logo + favicons, banner artwork
config/      settings_schema.json, settings_data.json
layout/      theme.liquid, password.liquid
locales/     en.default.json (all storefront text)
sections/    page sections + header/footer groups
snippets/    product card, price, cart line, facets, icons, logo …
templates/   JSON templates (+ customers/*, gift_card.liquid)
```

Lint with `shopify theme check`. Brand colours, fonts, card image ratio and cart behaviour are theme
settings, so they can be changed in the theme editor without code.
