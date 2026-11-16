# Store upgrade: 11.11 Sale ended, premium look for ad visitors (16 Nov 2026)

Scope and limits. The Shopify connection in this session points at a different shop (Zuaja.pk), so **the Anjum Mart admin and the live
storefront were not opened**. The analysis below comes from the theme code in this repository, the earlier audit (`LAUNCH-AUDIT.md`)
and local parse checks. Nothing here was published: the owner uploads and publishes the theme.

## 1. 11.11 Sale: ended

| Item | State |
| --- | --- |
| Sale window | 11 Nov 2026, 00:00 to 23:59:59 Pakistan time. The theme switches the strip, banner and card tags off by itself after the end time, so visitors have not seen the sale since 12 Nov even on the old theme. |
| This package | The sale banner is **removed from the home page template**, and "Show the 11.11 Sale" is off in the theme settings. The sale code stays in the theme, dormant, so a future sale can reuse it (`docs/SALE-1111.md`). |
| Shopify discount | "11.11 Sale: 11% off everything" was scheduled to end at the same time. **Owner check:** Admin, Discounts, it should say Expired. If it still shows Active, deactivate it. |
| `ADVANCE499` | Unchanged (Advance Cash Payment, Rs. 499 off). Keep it only if you still want to offer it. |

## 2. Analysis: what makes an international-level store, and where Anjum Mart stands

| Area | Today | Verdict |
| --- | --- | --- |
| Look | Cormorant headings, Jost body, champagne and cream, one gold accent (#D4AF37), thin gold frames, tall product cards | Already premium. Keep it; do not add more colours or badges. |
| First screen | Slideshow with the three categories, then trust points, then category tiles | Good. The new brand film adds motion right after the tiles. |
| Photography | Studio shots, but the colours and backdrops differ from product to product | The biggest gap. The new reels and colour-story posts use one consistent look (cut-out piece, one colour world, one hook line, price pill). Use the same pictures on the store (see section 4). |
| Motion and video | None on the home page | Added: Brand film section (muted loop, pause and sound buttons, reduced motion respected). |
| Social presence | Footer icons only | Added: Instagram gallery section (up to six pictures that link to the profile). |
| Trust | Free delivery, COD, WhatsApp, policies, Advance Cash Payment, no fake reviews or purchase popups | Strong and honest. **Do not add review stars or "sold" counters until they are real.** |
| Speed | Splash off by default, lazy images, no heavy scripts | Good. Keep the splash off for ads. The brand film loads its video only near the viewport (`preload="metadata"`). |
| Open owner items from the audit | Meta Pixel and Purchase event, "Bank Deposit" vs "Advance Cash Payment" naming, policies pasted in Settings, empty collections | Still open, see `LAUNCH-AUDIT.md`. The Pixel matters most before Phase 2 ads. |

## 3. What changed in the theme (this package: "Anjum Mart Final 10")

* `templates/index.json`: sale banner removed; **Brand film** added after the category tiles; **Instagram gallery** added before the newsletter.
* `sections/brand-film.liquid` (new): shows nothing until a video is set. Settings: video (upload an MP4) or an MP4 link, cover picture, heading, text, three points, button.
* `sections/social-gallery.liquid` (new): up to six pictures (alt text per picture) that open the Instagram profile from Theme settings (`@anjummart.co` today). Shows nothing until a picture is added.
* `assets/home.css`: styles for both sections (phone first, one column; two columns from 750 px).

Checks run: theme JSON validator OK; both new sections parse as Liquid and were rendered with test data (video present, video missing, gallery with and without pictures); section schemas are valid JSON. Not run: Shopify Theme Check and a visual check on the live store (the CLI and the store are not reachable from this session). Open the preview in the theme editor before publishing.

## 4. What you do (about 10 minutes)

1. Online Store, Themes, Add theme, **Upload zip file**: `Anjum-Mart-Theme-Final-10.zip`. Open Customise on the new theme.
2. Home page, **Brand film**: upload `R-BRAND.mp4` (or `R-ALL.mp4`) from the Reels folder, upload its cover from `Reels/covers`, Save.
3. Home page, **Instagram gallery**: add six pictures from `Posts/Color-Series/` (the feed pictures, for example K-M1, K-W2, K-J2, K-P1, K-M4, K-P3). Write a short description for each. Save.
4. Check Theme settings: "Show the 11.11 Sale" is off, splash is off.
5. Look at the preview on a phone, then **Publish**. (The assistant cannot publish.)
6. Upload the colour-story pictures as the first image of each product if you like the look (Products, the product, Media). Keep the existing photos after it.

## 5. Next upgrades worth doing (not done here)

* Real customer photos and reviews, once they exist (Shopify Product Reviews app). No placeholders.
* A short "About Anjum Mart" page (who you are, Multan, how orders are packed) linked in the footer.
* Product videos: the reels per product (`R-M1`, `R-W2`...) can be added to each product's media.
* Meta Pixel and Purchase event verified, then Phase 2 "Shop Now" ads (`Meta-Ads-Playbook.pdf`).
