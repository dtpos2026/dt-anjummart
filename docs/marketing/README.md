# Anjum Mart marketing kit generator

Everything that makes the reels, pictures, PDFs and zips is code here, so the kit can be rebuilt when products or prices change.

```
docs/marketing/build_all.sh <photos_dir> <out_dir>               # final kit (12 watch/jewellery photos: M1..M6, W1..W4, J1, J2)
docs/marketing/build_all.sh --preview <cutouts_dir> <out_dir>    # look-check kit with a PREVIEW ribbon on every reel
```

| Folder | Content |
| --- | --- |
| `video/make_cutouts.py` | photos to transparent cut-outs (rembg, needs `pip install rembg onnxruntime pillow`) |
| `video/build_plans.py` | one JSON plan per reel: 15 product reels, 4 collection reels, the brand reel, the all-products montage (`R-ALL`) |
| `video/engine/` | deterministic HTML/CSS/JS scene (`scene.js`), frames by Chromium (`render.mjs`) |
| `video/audio/make_music.py` | original music synthesised from the plan (no third-party audio, no copyright claim) |
| `video/make_video.sh` | plan, music, frames, MP4 (H.264 + AAC, about -15 LUFS) |
| `content/catalog.py`, `copytext.py`, `plan30.py` | product table and colour themes, captions/hashtags/alt text/keywords, the 30-day plan |
| `content/make_posts.py`, `post_styles.py` | feed 4:5 and story 9:16 pictures, carousels, guides, info and engagement posts |
| `content/build_calendar.py`, `build_playbook.py` | Content Calendar and Captions PDF, Meta Ads Playbook PDF, caption files, Ads Copy Sheet |
| `content/package.py` | the two zips: ADS package and POSTING package |

Rules the copy follows: only catalogue facts (names, dial colours, prices, Day & Date display, 50 ml), free delivery all over Pakistan and Cash on Delivery.
No discounts, urgency, ratings, reviews, "original" or "best" claims. Contact details are the real ones from the theme settings.
Generated media (MP4, JPG, PDF, zip) is not committed; rebuild it with the commands above.
