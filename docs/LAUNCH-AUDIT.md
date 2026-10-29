# Anjum Mart: pre-launch audit (updated 18 Oct 2026)

Scope: everything that could be checked from the build environment. That is the Shopify Admin API (read, plus the
edits listed below), a local render of the theme against the real product data, and one real checkout that the owner
placed (order #1005). **The live storefront pages, payment pages and e-mail inboxes cannot be opened from here**, so
anything that depends on them is listed as "not verified", never as passed.

## Result in one line

Catalogue (12 products), stock, free delivery, COD checkout and the new theme: verified. Order e-mails, the Meta
Pixel, Google tracking and Search Console: **not verified or not installed**.

* **Public launch (WhatsApp, Instagram and Facebook posts, organic visitors): ready once the owner publishes the new
  theme** (section 5, steps 1 to 3).
* **Paid advertising: not yet cleared.** Install the pixel and confirm one Purchase event first (section 5, steps 6 and 7).

Verified-ready score (only counting what was actually tested): about **90 %** for a public launch and about **75 %**
for paid ads. The rest is owner-side settings that cannot be changed or read from here.

## 1. Passed (verified)

| Area | Evidence |
| --- | --- |
| Domain | Primary domain anjummart.com, SSL on (Admin API). |
| Currency / locale | PKR only, shop timezone Asia/Karachi. |
| Catalogue | Exactly 12 products ACTIVE (6 men's RUSTET watches, 4 ladies' MOONSTON watches, 2 jewellery sets), 0 draft. Each has 3 images (all READY), SKU, vendor, type, tags and a complete SEO title and description. |
| Stock | 10 pieces per product, inventory tracked, oversell denied. The RUSTET gold / black-dial / Roman-numeral watch shows 9 because of order #1005. |
| Prices | MOONSTON black crystal-flower watch Rs 2,499; other MOONSTON Rs 2,999; RUSTET Rs 3,999; jewellery sets Rs 1,999. |
| Shipping | "Free Delivery (All Pakistan)" at Rs 0 for the whole of Pakistan. Order #1005 confirms it at checkout (shipping Rs 0). |
| Checkout and COD | Order #1005 came through the web checkout, gateway "Cash on Delivery (COD)", confirmed, shipping Rs 0, fulfilment order open. |
| Collections / menu | Men's Watches (6), Women's Watches (4), Jewellery (2), New Arrivals (12), Featured (4). The theme menu "Anjum Mart main menu" links Home, Men's, Women's, Jewellery, New Arrivals, Contact. |
| Pages | Contact, Shipping Policy, Return and Refund Policy, Terms of Service are published and linked in the footer, cart drawer and product pages. The wording says: free delivery, Cash on Delivery, no returns, a damaged or wrong item is replaced when reported within 48 hours. |
| Theme (local render) | 181 storefront tests (hero carousel and frame styles, cards, quick view, cart drawer, search, splash and loader, highlights popup) pass; 38 + 67 + 24 + 9 older cart/conversion tests pass; axe-core finds 0 serious or critical issues on desktop and mobile; Theme Check 0 offences (79 files); strict Liquid parse 0 errors. |
| Uploaded themes | Live (MAIN, published by the owner): "Anjum Mart Final 4 (Advance Pay, Perfumes)". Newer, unpublished: "Anjum Mart Final 5 (Perfume Photos)" (id 189775249482): all theme files present, checksums of the key files identical to this repository. It differs from Final 4 only in the Perfumes banner (real photos, Shop Perfumes button, phone layout). The assistant cannot write to the live theme, so Final 5 must be published by the owner. Shopify silently dropped two files during this work (a settings range with too many steps, a home section value off its range step); both are fixed and `docs/tools/validate_theme_json.py` now catches that class of error before an upload. |
| Splash and loader | Logo splash on the first visit of a session (1.5 to 3.2 s), logo loader when the next page takes over 0.28 s (page links and search). Skipped for reduced-motion visitors, crawlers and speed tests, the theme editor and `?nosplash`; a CSS failsafe clears it after 4.4 s even if scripts fail. Switch off in Theme settings, Loading screen. |
| Advance Cash Payment | Built in the cart (page and drawer): COD or Advance Cash Payment with the Rs. 499 banner, totals, on-demand payment details with Copy buttons, transaction ID, Shopify code ADVANCE499 (created, active). **Off by default** in Theme settings until the Shopify manual payment method "Advance Cash Payment" exists. Never marks a payment as received. Steps and limits: `docs/ADVANCE-PAYMENT.md`. 220 local checks pass; the real Shopify checkout screens are not testable from here. |
| Perfumes on the home page | Main banner: drawn bottles next to the watches and jewellery (unchanged). Separate "Anjum Perfumes" banner section with the owner's real photos and a "Shop Perfumes" button, then a Perfumes product section (3 products). "Perfumes" is also in the menu "Anjum Mart main menu" (added 29 Oct). Watches, jewellery and perfumes each have their own section. |
| Perfumes | Lady Aura (women), Oud Aura (unisex) and Tea Rose (women), 50 ml Eau de Parfum, Rs 3,450 each. ACTIVE with stock 10 each (set by the owner), real photos attached (3, 3 and 4 images, all READY) and published to the Online Store on 29 Oct. "Original" was left out of the text (authenticity claim). |
| Store highlights popup | Bottom-left card, random order and timing (about every 14 to 28 s, 8 per visit), closes for the visit, pauses on hover/focus, phone layout above the sticky bar, not on the cart page or in the theme editor. It shows in-stock products and delivery facts and **never claims a purchase**; "Verified order" notices come only from the shop metafield `custom.recent_orders` (empty today, so none appear). No demo purchase messages exist. See `docs/SOCIAL-PROOF.md`. |

## 2. Fixed during this audit

| Finding | Fix |
| --- | --- |
| Product SEO descriptions ended in "..." (cut off mid-sentence). | Rewrote 11 of the 12 as complete sentences (the twelfth was already complete). |
| Splash would also have shown to crawlers and PageSpeed runs. | Skipped when the user agent is a bot, Lighthouse, PageSpeed or GTmetrix. |
| Hero heading with a line break was silently dropped by Shopify on import. | Second line is now a styled block, no `<br>`. |

## 3. Not verified or not installed

| Item | Status |
| --- | --- |
| Order confirmation, shipping and account e-mails | Cannot be read or sent from here. Check the inbox of the customer on order #1005. |
| Other payment gateways | Cannot be read through the API. Only COD is evidenced. |
| Policy links at checkout | Checkout shows only Shopify's own policy boxes. Only the Privacy policy exists there (see section 4). |
| Meta Pixel / Conversions API | **Not installed.** No pixel exists to verify. |
| Google Analytics, conversion tracking, Merchant Center | **Not installed.** |
| Google Search Console | Not connected. Needs the owner's Google login. |
| Sitemap and robots.txt | Generated by Shopify at /sitemap.xml and /robots.txt. Cannot be fetched from here. |
| Store password | Cannot be read through the API. Check Online Store, Preferences, and remove it before launch. |
| Social links | Facebook (facebook.com/anjummartpakistan) and Instagram (instagram.com/anjummart.co) are set in Theme settings, Social media; the footer icons and the structured data (sameAs) use them. TikTok link not given yet, so no TikTok icon. On the live theme the two links must be pasted in Theme settings (the assistant cannot write to the live theme); the unpublished theme "Anjum Mart Final 2 (social icons + icon)" already has them. |
| International shipping | An "International" zone (Rs 5,300) exists for 28 countries. Delete the zone if you only deliver in Pakistan. |
| Empty collections | Ladies Bags, Dresses, Shoes, Sale, Diver, Sport and Strap Watches are published but empty. Unpublish or delete them after the new theme is live. |
| Real-device speed (Lighthouse on the live site) | Not measured. |

## 4. Policies

The four policy pages are live as ordinary pages (source: `docs/policies/*.html`). The assistant has no permission to
write Shopify's own policy boxes, so checkout still shows only the Privacy policy link. Paste the same text in
Settings, Policies. The Privacy policy contact line still shows the old Burewala address and no phone number; edit it
there too. These are the store's commitments to customers: read them once and change anything you cannot keep.

## 5. Manual actions (in this order)

1. **Publish the theme "Anjum Mart Final 5 (Perfume Photos)"** (Online Store, Themes, Publish). Older themes named "OLD ..." are superseded.
   Afterwards the nine unused collections (gold, two-tone, steel, diver, sport, strap, ladies bags, dresses, shoes, plus Sale) can be deleted: the old themes link to some of them, the new one does not.
2. **Remove the storefront password** if one is set (Online Store, Preferences).
3. Open anjummart.com on a phone: splash, hero, a product, add to cart, checkout.
4. **Paste the policies** into Settings, Policies and fix the Privacy contact line.
5. Check that the confirmation e-mail of order #1005 arrived; cancel or fulfil that order as appropriate and restock if it was only a test.
6. **Install the Facebook and Instagram channel** (free), then confirm a Purchase event in Meta Events Manager.
7. **Install the Google and YouTube channel** (free), verify the domain in Search Console, submit https://anjummart.com/sitemap.xml.
8. Send the Instagram, Facebook and TikTok links (theme settings, Social media).
9. If two WhatsApp buttons appear (the theme's and the WhatsApp by Meta app's), switch one off.
10. Delete the empty collections and the obsolete preview themes.
11. Add real orders (city, product, time) to Settings, Custom data, Shop, Verified recent orders if you want purchase notices; there is no automatic order feed yet.

Paid items: none of the above needs a new paid subscription. Ad spend is the only cost.

## 6. Ready for advertising?

**Not yet for paid ads.** Open: no pixel or conversion tracking, policies not yet in Shopify's policy boxes, order
e-mails unchecked. For an organic public launch the store is ready as soon as the new theme is published.
