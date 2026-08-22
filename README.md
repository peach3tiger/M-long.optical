# M-LonG.Optical

Korean-minimal eyewear storefront for M-LonG.Optical — Hanoi.

## Live site

Served by GitHub Pages from `index.html` at the repo root.

To enable: **Settings → Pages → Source: Deploy from a branch → `main` / `/ (root)` → Save.**
The site appears at `https://peach3tiger.github.io/M-long.optical/` within a minute or two.

## Files

| Path | What it is |
| --- | --- |
| `index.html` | The published site — fully self-contained (all images, fonts and scripts inlined). This is the only file GitHub Pages needs. |
| `M-LonG Optical.dc.html` | Editable source of the same site. Open it directly in a browser. |
| `support.js`, `image-slot.js` | Runtime helpers the source file loads. |
| `uploads/`, `uploads-opt/` | Product photography and article imagery (`-opt` = web-optimised versions used by the site). |

## Editing

Edit `M-LonG Optical.dc.html`, then regenerate `index.html` from it so the published
site picks up the change — `index.html` is a build output, not a file to edit by hand.

## Sections

Hero · Trending · Product list (search + pagination) · Product detail · Learn (6 articles,
EN/VI) · Checkin W Us (scrolling gallery) · Store locator (map) · Footer

Language toggle covers English and Vietnamese throughout.
