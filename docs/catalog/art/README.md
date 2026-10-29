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

## Perfumes on the home page (29 Oct 2026)

* **Main banner (`slide-brand-*.jpg`)**: `make_perfume_scene.py` adds three **drawn** bottles (Lady Aura, Oud Aura, Tea Rose:
  frosted glass, black ribbed cap, gold label) next to the watches and jewellery. They are illustrations. The owner approved
  this banner as it is, so it stays unchanged.
* **Perfumes banner section (`promo-perfumes.jpg`, `promo-perfumes-mobile.jpg`)**: `make_perfume_photo_promo.py` shows the
  owner's **real photos** (`perfume-photos/*-portrait.jpg`, also attached to the three products in Shopify) as three framed
  prints. Run it after `make_scenes.py` has written `scenes.json`, then render with `art-render.mjs`.
* The product photos in Shopify come from the same files (3 to 4 images per perfume: portrait, original, label, cards).
