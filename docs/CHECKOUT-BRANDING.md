# Checkout branding (logo, colours): do this in the Shopify admin

The Shopify checkout (the page with Contact, Delivery, Payment) is hosted by Shopify. It cannot be changed from the theme,
and the store's API access does not include checkout branding ("access denied"), so these settings are made in the admin.
It takes about 3 minutes. Files are in `docs/brand/checkout/`.

## 1. Brand settings (logo for checkout, e-mails and invoices)

**Settings, Brand**

| Field | Upload / value |
| --- | --- |
| Default logo | `anjum-mart-checkout-logo-light-background.png` (wide, black + gold, transparent) |
| Square logo | `anjum-mart-square-logo-512.png` |
| Slogan | Premium Style at Affordable Prices |
| Primary colour | `#111111` |
| Secondary / accent colour | `#D4AF37` |

## 2. Checkout editor (the page layout and colours)

**Settings, Checkout, Customize** (opens the checkout editor), then the **Branding** (paint-brush) tab.

| Setting | Value |
| --- | --- |
| Logo | the same wide logo (light background version). Size: Medium or Large; position: left or centre |
| Header background | White |
| Main area background | White `#FFFFFF` |
| Order summary background | Cream `#F8F7F4` |
| Accent colour (links, focus) | Deep gold `#8A6A12` |
| Primary button | Background `#111111`, text white |
| Corner radius | None or Small (the store uses about 2 px) |
| Headings font | A serif, ideally Cormorant if it is in the list |
| Body font | Jost if it is in the list, otherwise a clean sans-serif |
| Favicon | `anjum-mart-store-icon-512.png` (Settings, Brand, or Online Store, Preferences) |

Also in the editor: under **Checkout**, check that **Phone number** is set to *Required* (helps the confirmation call),
and that the payment methods show **Cash on Delivery (COD)** and, after you create it, **Advance Cash Payment**.

## 3. What cannot be done on this plan

Custom banners, the "Save Rs. 499" bold promo, Copy buttons and a transaction ID box inside checkout need Shopify Plus or an
app. The Rs. 499 banner, Copy buttons and transaction ID are therefore in the cart (see `docs/ADVANCE-PAYMENT.md`); at
checkout, the payment details appear as plain text under the Advance Cash Payment method.
