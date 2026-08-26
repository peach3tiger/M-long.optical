# M-LonG.Optical

Korean-minimal eyewear storefront for M-LonG.Optical — Hanoi.

## Live site

Served by GitHub Pages from `index.html` at the repo root.

To enable: **Settings → Pages → Source: Deploy from a branch → `main` / `/ (root)` → Save.**
The site appears at `https://peach3tiger.github.io/M-long.optical/` within a minute or two.

## Files

| Path | What it is |
| --- | --- |
| `index.html` | The published site — same file as `M-LonG Optical.dc.html`, loaded directly by GitHub Pages. It references `support.js`, `image-slot.js` and `uploads-opt/` as plain relative files (not inlined), which keeps it small and avoids upload-size limits. |
| `M-LonG Optical.dc.html` | Editable source, identical to `index.html`. Open it directly in a browser. |
| `support.js`, `image-slot.js` | Runtime helpers the site loads. |
| `uploads/`, `uploads-opt/` | Product photography and article imagery (`-opt` = web-optimised versions used by the site). |

## Editing

Edit `M-LonG Optical.dc.html`, then copy it over `index.html` (same content) so the
published site picks up the change.

## Sections

Hero · Trending · Product list (search + pagination) · Product detail · Learn (6 articles,
EN/VI) · Checkin W Us (scrolling gallery) · Store locator (map) · Footer

Language toggle covers English and Vietnamese throughout.
