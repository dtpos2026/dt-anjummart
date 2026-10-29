# Artwork scripts

The homepage artwork (`assets/slide-*.jpg`, `tile-*.jpg`, `promo-*.jpg`) and the two extra pictures of every product
(a black-and-gold display picture and a "key details" card) were made from the supplied product photos:

1. Each product photo (white background) was cut out with BiRefNet into a transparent PNG (`cut-NN.png`).
2. `art-render.mjs` places the cut-outs on a black and gold backdrop (CSS gradients, soft shadows, grain) and
   screenshots each scene with Chromium. `make_media.py` and `media_meta.py` describe the 22 product pictures
   (text on the details cards comes only from the product listing).
3. When the original white-background PNGs arrive, repeat step 1 with them and run the renderer again; then upload
   the new pictures to the products (Shopify admin, or the Admin API `productUpdate` with `media`).

The cut-out PNGs are not stored in the repository (about 10 MB).

## Perfume bottles in the main banner (29 Oct 2026)

`make_perfume_scene.py` adds three **drawn** bottles (Lady Aura, Oud Aura, Tea Rose: frosted glass, black ribbed cap, gold
label, in the style of the packaging the owner supplied) to the `slide-brand-desktop` and `slide-brand-mobile` scenes
(`scenes.json`) and renders them with `art-render.mjs`. They are illustrations, not photographs: the owner's perfume photos
arrived as chat images only. When the photos arrive as files, cut them out (step 1) and use them as `items` instead of the
drawn bottles. The banner text says "coming soon" because the perfumes are still draft products with no stock.
