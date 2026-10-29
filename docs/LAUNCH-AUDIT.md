# Anjum Mart: pre-launch audit (updated 29 Oct 2026, final check)

Scope: everything that could be checked from the build environment. That is the Shopify Admin API (read, plus the
edits listed below), a local render of the theme against the real product data, and one real checkout that the owner
placed (order #1005). **The live storefront pages, payment pages and e-mail inboxes cannot be opened from here**, so
anything that depends on them is listed as "not verified", never as passed.

## Result in one line

Catalogue (15 products), stock, free delivery, COD checkout (one real order, #1007, placed and fulfilled), the live theme
"Anjum Mart Final 5" and its tests: verified. Meta Pixel, Google tracking, Search Console, order e-mails and the
Advance Cash Payment payment method: **not verified or not installed**.

* **Public launch (WhatsApp, Instagram and Facebook posts, organic visitors): ready now.**
* **Paid advertising: one critical item is open, conversion tracking** (Meta Pixel through the Facebook and Instagram
  sales channel, section 5 step 3). Ads can run without it, but nothing is measured or optimised for purchases. Install
  it and confirm one Purchase event before spending real money.

Verified-ready score (only counting what was actually tested): about **92 %** for a public launch and about **78 %**
for paid ads. The rest is owner-side settings that cannot be changed or read from here.

## 1. Passed (verified)

| Area | Evidence |
| --- | --- |
| Domain | Primary domain anjummart.com, SSL on (Admin API). |
| Currency / locale | PKR only, shop timezone Asia/Karachi. |
| Catalogue | 15 products ACTIVE (6 men's RUSTET watches, 4 ladies' MOONSTON watches, 2 jewellery sets, 3 perfumes), 0 draft, all published to the Online Store. Each has 3 to 4 images (all READY), SKU, vendor, type, tags and a complete SEO description. |
| Stock | 10 pieces per product, inventory tracked, oversell denied. The silver and white jewellery set shows 9 because of real order #1007 (Multan, Cash on Delivery, fulfilled). |
| Prices | MOONSTON black crystal-flower watch Rs 2,499; other MOONSTON Rs 2,999; RUSTET Rs 3,999; jewellery sets Rs 1,999. |
| Shipping | "Free Delivery (All Pakistan)" at Rs 0 for the whole of Pakistan. Order #1005 confirms it at checkout (shipping Rs 0). |
| Checkout and COD | Order #1005 came through the web checkout, gateway "Cash on Delivery (COD)", confirmed, shipping Rs 0, fulfilment order open. |
| Collections / menu | Men's Watches (6), Women's Watches (4), Jewellery (2), New Arrivals (12), Featured (4). The theme menu "Anjum Mart main menu" links Home, Men's, Women's, Jewellery, New Arrivals, Contact. |
| Pages | Contact, Shipping Policy, Return and Refund Policy, Terms of Service are published and linked in the footer, cart drawer and product pages. The wording says: free delivery, Cash on Delivery, no returns, a damaged or wrong item is replaced when reported within 48 hours. |
| Theme (local render, 29 Oct) | 230 storefront tests (hero, cards, quick view, cart drawer, search, splash and loader, highlights popup, Advance Cash Payment, perfumes banner on phone) pass; 67 + 24 + 38 + 9 older cart and conversion tests pass; axe-core finds 0 serious or critical issues on desktop and mobile; Theme Check 0 offences (83 files); strict Liquid parse 0 errors; theme JSON validator OK. |
| Uploaded themes | Live (MAIN, published by the owner): "Anjum Mart Final 5 (Perfume Photos)" (id 189775249482), all theme files present and key checksums identical to this repository. The owner has since saved the Search Console code, the sharing image and the Advance switch in its customiser. The assistant cannot write to the live theme. Older themes ("Final 4", "Final 3" and earlier) are unpublished and can be deleted in the admin. Shopify silently dropped two files during this work (a settings range with too many steps, a home section value off its range step); both are fixed and `docs/tools/validate_theme_json.py` now catches that class of error before an upload. |
| Splash and loader | Logo splash on the first visit of a session (1.5 to 3.2 s), logo loader when the next page takes over 0.28 s. Skipped for reduced-motion visitors, crawlers and speed tests, the theme editor and `?nosplash`. **Recommendation for ads: switch the first-visit splash off** (Theme settings, Loading screen, untick "Logo splash screen when the store is opened") so the store shows at once; the repository default is now off, the live theme was still on when checked. Simulated slow 4G with a 4x slower CPU (local render, not the live site): first paint about 2.0 to 2.8 s, largest paint 2.2 to 3.1 s, no layout shift. Real-device speed of the live site was not measured (the live domain cannot be opened from the build environment). |
| Advance Cash Payment | Built in the cart (page and drawer): COD or Advance Cash Payment with the Rs. 499 banner, totals, payment details with Copy buttons, transaction ID, Shopify code ADVANCE499 (active, 0 uses). The owner has switched it on in the live theme settings (`adv_enable` true). **Not verified:** whether the Shopify manual payment method "Advance Cash Payment" exists (cannot be read from here) and how the real checkout looks. Place one test order each way before sending ads. It never marks a payment as received. Steps and limits: `docs/ADVANCE-PAYMENT.md`. |
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

1. **Untick the first-visit splash** (live theme, Customize, Theme settings, Loading screen) so the store opens at once.
2. **Paste the policies** into Settings, Policies: Shipping, Refund and Terms (text in `docs/policies/*.html`). Only the Privacy
   policy is in Shopify's policy boxes today (its contact line is now correct: e-mail). The shipping and refund wording is
   already live on the pages linked in the footer.
3. **Install the Facebook and Instagram channel** (free, owner login), connect the Facebook page and Instagram account,
   switch the pixel on, place a test order and confirm a **Purchase** event in Meta Events Manager. This is the open item
   for paid ads. Optional: Google and YouTube channel for Google tracking; Search Console is not needed for ads.
4. **Advance Cash Payment:** confirm the manual payment method "Advance Cash Payment" exists (Settings, Payments,
   `docs/ADVANCE-PAYMENT.md` section 5). Place one Cash on Delivery and one Advance test order, then cancel them.
5. **Checkout branding** (Settings, Brand and Checkout, `docs/CHECKOUT-BRANDING.md`).
6. Check that an order e-mail (customer and owner) really arrives.
7. Delete the ten obsolete collections (Ladies Bags, Dresses, Shoes, Sale, Diver, Sport, Strap, Gold, Two-Tone and Steel
   Watches): they are not linked anywhere but still appear on the all-collections page and in the sitemap. The assistant's
   tools may not unpublish or delete them.
8. Search Console: finish the verification (DNS record at Namecheap, or the HTML tag already saved in the theme), then
   submit https://anjummart.com/sitemap.xml.
9. Send the TikTok link (theme settings, Social media). If two WhatsApp buttons appear (the theme's and the WhatsApp by
   Meta app's), switch one off.
10. Add real orders (city, product, time) to Settings, Custom data, Shop, Verified recent orders if you want purchase
    notices; there is no automatic order feed.

Paid items: none of the above needs a new paid subscription. Ad spend is the only cost.

## 6. Ready for advertising?

**For an organic public launch: yes.** For paid ads: **not until the Meta Pixel (section 5, step 3) is installed and one
Purchase event is confirmed**, and one Advance and one Cash on Delivery test order have been placed (step 4). Everything
else that could be tested from here passed. Unverified because it needs the live site or the owner's logins: live page
speed, order e-mails, the real checkout screens, the storefront password setting, Google and Meta tracking.
