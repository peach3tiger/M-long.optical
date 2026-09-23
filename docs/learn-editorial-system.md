# Manh Long Optical — Learn Editorial System (v1, 23 Sep 2026)

One visual system, ten intent templates, one QA gate. This file is the rulebook for every Learn article, existing or new, EN and VI.

| File | Role |
|---|---|
| `assets/learn.css` | Shared article component library (`.la-*`). Body only; header, nav, footer and sticky CTA are untouched. |
| `templates/learn-article.html` | Copy-paste skeleton. Each block is tagged `[ALL]` or `[OPT: intents]`. |
| `tools/learn_lint.py` | Automated QA. `--audit` lists pages still on the old layout. |
| `en/learn/photochromic-vs-polarized-sunglasses.html` | Pilot: Template A (comparison), validated desktop 1280 px and mobile 390 px. |

Data rules from `mlong-seo` still apply. Business facts come only from confirmed shop data. Unknown facts get `[VERIFY BUSINESS FACT]` in drafts, and the linter blocks publishing while any marker remains.

---

## 1. Audit of the reference article

Reference: `manhlongoptical.byryze.com/best-transitions-photochromic-lenses-compared` (Ryze-hosted, read 23 Sep 2026). Its **information architecture** is strong. Its **execution** has issues that must not be copied.

| Element | Verdict | Why |
|---|---|---|
| "Back to all articles" | KEEP | Clear way back to the library. Now `.la-back`, placed above the breadcrumb. |
| Clear H1 | KEEP + IMPROVE | The reference uses an English H1 over a Vietnamese body and meta title. **Use one language per page.** VI pages get VI H1s, EN pages get EN H1s. |
| Subtitle / deck | KEEP + IMPROVE | Rewrite as "question answered + what you'll be able to decide", not a keyword string. |
| Author · date · read time | KEEP + IMPROVE | "MAContent Team" is not a real person. **Use Alvin Dao, Store Manager** (the real author, with a bio page). Add an **Updated** date. Only show a reviewer if a real one exists. |
| Hero image | KEEP + IMPROVE | Reference alt text = the H1, which is weak. The alt must describe the picture. Fixed 16:9 crop. 29 of 79 current articles have no hero (see §6). |
| Immediate practical answer | KEEP + IMPROVE | Tighten to 40–90 words, answer first, with a "Short answer" label for AI extraction. |
| TL;DR | KEEP | Works well for readers and for AI answers. 3–6 bullets, each a real conclusion. |
| Key numbers | OPTIONAL BY INTENT | Useful only when the numbers are verified and relevant. The reference repeats generic shop numbers (hours, frame count) on a lens comparison. Numbers should be **topic numbers** (price floor/ceiling, SPH range) with a source/date note. |
| Explanation ("why this matters") | KEEP | The main authority-building section: explain the confusion before the options. |
| Selection criteria | KEEP + IMPROVE | Criteria must be specific to the topic. Never reuse one generic list. Styled `.la-criteria`. |
| Comparison table | KEEP + IMPROVE | Short cells, `Option · Best for · Main strengths · Limitations`, scrollable on mobile with a swipe hint and caption. Only for intents A/B/C. |
| Numbered deep-dives | OPTIONAL BY INTENT | Only when several options are really being compared. Add a **Consider instead if** line. |
| "Tốt nhất cho…" in every H2 + "Verdict: Nên mua" | REMOVE | Reads as ranking without evidence. Use situation-based "Best for" inside the section instead. |
| Ranking methodology ("Cách xếp hạng") | KEEP + IMPROVE | Rename to "How we compared these options". Label each source type (business info, manufacturer, professional body, store experience). Never imply lab testing. |
| Decision guide | KEEP | "If you… → consider…". Styled `.la-decide`. |
| Contextual CTA | KEEP + IMPROVE | The reference button points to the **homepage**. It must point to the matching service page, with a CTA matched to intent (§5). |
| FAQ | KEEP + IMPROVE | Visible H3 questions (not hidden), plus FAQPage JSON-LD that mirrors them exactly. The reference has no schema. |
| Final takeaway | KEEP | "One thing to remember", one sentence. |
| Related articles + You might also like | KEEP + IMPROVE | Related = exactly 3 cards chosen by cluster role (pillar, sibling, next step), not "latest". You-might-also-like = 2–4 links including the commercial page. |
| Sources | ADD | The reference cites nothing. Add sources, labelled by type, wherever a technical or product claim benefits from them. |
| Table of contents | ADD | For 5+ H2s or more than ~1,200 words. |
| Breadcrumb (visible + schema) | ADD | Home › Learn › Pillar › Article. |
| Article / Breadcrumb / FAQ schema | ADD | The reference has none. |
| Author box | ADD | Real bio with a link to `/en/about-alvin.html`. |
| Health note | OPTIONAL BY INTENT | Only on health-adjacent topics. |

### Problems in the reference to escalate (not just styling)

1. **Duplicate domain.** The byryze page self-canonicalises on `manhlongoptical.byryze.com`. Its siblings (`prescription-glasses-in-hanoi-complete-guide-for-travelers`, `best-polarized-sunglasses-in-hanoi`) target the same intents as `/en/prescription-glasses-hanoi.html` and `/en/sunglasses-hanoi.html` on the main domain. Two domains are competing for the same queries. **Recommended fix:** publish Ryze articles into this repo (Ryze has a GitHub integration) or point their canonical to the main-domain equivalent. Ryze's own docs say that once an article is published, edits happen in your CMS, so this has to be fixed on the Ryze/hosting side.
2. **Product availability not verified.** The reference covers Transitions Signature GEN 8, XTRActive, Vantage and Style Mirrors. The main site documents **Transitions Gen S** (Essilor). `[VERIFY BUSINESS FACT]`: which Transitions lines does the shop actually order?
3. **Opening hours conflict.** The whole site and the reference say **8:00–21:30**. The `mlong-seo` NAP block (confirmed 30/08/2026) and the GBP plan say **8:30–21:30**. `[VERIFY BUSINESS FACT]`, then fix it everywhere at once.

---

## 2. The shared frame (every article)

Order is fixed. Blocks marked *intent* are chosen by the template in §3.

1. Back link + breadcrumb
2. Eyebrow (cluster · intent), H1, deck
3. Meta: author · published · updated · read time
4. Hero (16:9, descriptive alt)
5. Direct answer (40–90 words)
6. TL;DR (3–6)
7. *Key numbers* · *TOC*
8. **Intent body** (§3)
9. CTA (one, intent-matched)
10. FAQ (4–8, visible + schema)
11. One thing to remember
12. *Health note* · *Sources*
13. Author box
14. Related articles (3 cards) · You might also like (2–4)

The first screen must answer: what is this, what question does it answer, is it for me, what is the short answer, and what will I learn. H1 + deck + direct answer do that job.

---

## 3. Intent templates

Every article has **one** primary intent, and that intent picks the body. Visual components stay the same across all of them.

### A. Comparison (X vs Y)
Body: why they get confused → criteria → table → numbered option sections (strengths / limitations / best for / consider instead) → how we compared → decision guide.
- **KEEP:** table before deep-dives, decision guide.
- **IMPROVE:** criteria specific to the pair.
- **ADD:** "Consider instead if" line and source types.
- **REMOVE:** winner declarations.
- Pilot: `en/learn/photochromic-vs-polarized-sunglasses.html`.

### B. "Best" / top options
Body: criteria first → options grouped **by use case** (not 1–10) → strengths / limitations / best for → method → decision guide.
- **KEEP:** criteria and method.
- **IMPROVE:** ordering must follow the stated criteria.
- **ADD:** "if no single option wins, say so".
- **REMOVE:** "number one" and "best in Hanoi" claims (the linter flags them).

### C. Price / cost
Body: price range with its source and date → what changes the price (index, brand, coating, prescription) → price table → what's included / what costs extra → choosing by budget → local context.
- **KEEP:** real shop prices.
- **IMPROVE:** label each figure as **shop list price (date)**, **market context** or **ask the store**.
- **ADD:** a "what's included" block.
- **REMOVE:** "giá tốt" and "giá rẻ nhất" in titles and H1s.

### D. How-to
Body: what you need → `.la-steps` → common problems → when to get professional help.
- **KEEP:** short steps.
- **IMPROVE:** one action per step.
- **ADD:** "what to bring".
- **REMOVE:** TOC when there are fewer than 5 sections.

### E. Problem-solving
Body: the problem → why it happens → possible causes → what you can do → what not to do → when to see an optician → the relevant service.
- **KEEP:** direct answer.
- **ADD:** a "when to see an optician / doctor" section and the health note.
- **REMOVE:** anything that reads as a diagnosis.

### F. Product / product family
Body: what it is → who it suits / who may not need it (`.la-audience`) → main features → strengths / limitations → variants → compatibility → alternatives → how to choose.
- **KEEP:** manufacturer sources.
- **IMPROVE:** label manufacturer claims as manufacturer claims.
- **ADD:** an alternatives block with links to sibling products.
- **REMOVE:** spec-sheet paste.

### G. Definition / educational
Body: short definition → simple explanation → how it works → examples → what it is NOT → vs related concepts → who benefits → common misunderstandings.
- **ADD:** "what it is not" and a comparison with the nearest concept. These are the most extractable blocks for AI answers.
- **REMOVE:** a comparison table unless one is actually needed.

### H. Local / Hanoi service
Body: the service → who it is for → what to bring (`.la-steps`) → typical process → verified store facts → how to visit → related local pages.
- **KEEP:** NAP from the `mlong-seo` block only.
- **ADD:** a "what to bring" list.
- **REMOVE:** "Hanoi" in every heading.

### I. Audience-specific (children, expats, tourists, screen workers)
Body: the audience's situation → what matters differently for them → options with best-for → decision guide → CTA for that audience (e.g. tourists: "contact before visiting to confirm turnaround").

### J. FAQ / long-tail
Body: direct answer → 2–4 short supporting sections → FAQ.
- Skip the TOC. Key numbers only if central.
- Target 600–900 words. Don't pad.

**Length is set by intent, never by a target word count.** J runs about 600–900 words. A and C can reach 1,500–2,500 when the evidence supports it.

---

## 4. Component reference (`assets/learn.css`)

| Class | Use |
|---|---|
| `.la` | `<main>` wrapper, 704 px reading column |
| `.la-back` `.la-crumb` `.la-eyebrow` `.la-deck` `.la-meta` | Header |
| `.la-hero` | Figure, 16:9 cover crop, full-bleed on mobile |
| `.la-answer` | Direct answer with "Short answer" label |
| `.la-tldr` | TL;DR box |
| `.la-facts` + `.la-facts-note` | 3–4 verified numbers plus where they come from |
| `.la-toc` | `<details open>` contents, 2 columns on desktop, 1 on mobile |
| `.la-key` / `.la-note` | Key-takeaway box / health or policy note |
| `.la-criteria` | Numbered criteria |
| `.la-table` + `.la-scroll-hint` + `.la-table-note` | Scrollable table, caption, source note |
| `.la-num` `.la-proscons` `.la-bestfor` | Option deep-dive |
| `.la-audience` | Who it suits / who may not need it |
| `.la-steps` | How-to steps |
| `.la-decide` | If → consider decision guide |
| `.la-cta` `.la-btn` `.la-btn.ghost` | One CTA block, tap targets ≥ 46 px |
| `.la-faq` | Visible FAQ (H3 + P) |
| `.la-remember` | Final takeaway |
| `.la-sources` `.la-srctype` | Sources labelled by type |
| `.la-authorbox` | Author |
| `.la-related` `.la-cards` / `.la-more` | 3 related cards / extra links |

---

## 5. CTA matrix (one per article)

| Intent | Heading pattern | Primary button → page |
|---|---|---|
| Educational / definition | Get your eyes checked before choosing lenses | Free eye test → `/en/eye-test-hanoi.html` · VI `/do-mat-mien-phi-tron-doi.html` |
| Comparison / best | Ask which option fits your prescription and routine | Free eye test page, plus WhatsApp/Zalo |
| Price | Get a quote for your prescription | `/en/lenses.html` · VI `/trong-kinh.html` |
| Premium brand (Essilor, ZEISS) | Ask about the Essilor / ZEISS options for your prescription | `/en/lenses.html` or the brand article |
| Same-day | Check your prescription and same-day availability | `/en/same-day-glasses-hanoi.html` · VI `/cat-kinh-can-lay-ngay.html` |
| Sunglasses | See prescription-capable sun options | `/en/sunglasses-hanoi.html` · VI `/kinh-ram-can.html` |
| Tourist / expat | Contact the store before visiting to confirm turnaround | `/en/prescription-glasses-hanoi.html` + WhatsApp |
| Frames | Try frames in store | `/en/frames.html` · VI `/cua-hang.html` |
| Children | Book an eye test for your child | Eye test page |

Only verified services go in a CTA. Keep 80–90% of the article useful information and 10–20% commercial guidance. No promo banners inside Learn articles.

---

## 6. Clusters, pillars and roles (from the current inventory)

Inventory as of 23 Sep 2026: **36 EN** articles in `/en/learn/` and **43 VI** article pages at the root (79 in total). All 79 already have Article, FAQPage and BreadcrumbList schema. Gaps: hero 50/79, sources 10/79, category labels spread over 20 inconsistent values.

| Cluster | Pillar (EN / VI) | Commercial page | Supporting articles (role) |
|---|---|---|---|
| **Lens brands & premium** | `/en/lens-brands-compared.html` / `so-sanh-trong-kinh-theo-hang.html` | `/en/lenses.html` · `trong-kinh.html` | essilor-lenses (product family), zeiss-lenses, chemi, tokai, essilor-crizal-rock, essilor-authentic-check (how-to), why-phones-use-zeiss (educational), premium-lenses-what-are-you-paying-for (price), `/en/essilor-vs-zeiss.html` · so-sanh-essilor-vs-zeiss (comparison) |
| **Progressive / multifocal** | `en/learn/multifocal-lenses-explained.html` (**no VI version**) | lenses page | varilux-comfort-max, varilux-physio-extensee, zeiss-smartlife-individual (product), photochromic-progressive-lenses (product) |
| **Photochromic & sun** | `/en/lenses.html` (photochromic section) / `trong-kinh.html` | `/en/sunglasses-hanoi.html` · `kinh-ram-can.html` | photochromic-vs-polarized (comparison, pilot), essilor-transitions-price (price), transitions-gen-s-advantages (product) |
| **Coatings & protection** | `lens-coatings-explained` (EN + VI) | lenses page | is-anti-reflective-coating-worth-it (problem/decision), crizal-easy-pro, crizal-natural-look, zeiss-uvprotect (product), blue-light-vs-uv (comparison), kinh-chong-anh-sang-xanh-co-can-thiet (VI, decision), essilor-eyezen (audience: screen users) |
| **Materials & index** | `/en/lens-index-guide.html` / `chiet-suat-trong-kinh.html` | lenses page | lens-materials-explained · chat-lieu-trong-kinh (definition) |
| **Eye exam & prescription** | `/en/eye-test-hanoi.html` / `do-mat-mien-phi-tron-doi.html` | same | how-to-read-your-prescription · cach-doc-don-kinh (how-to), when-do-you-need-glasses · khi-nao-can-deo-kinh-can (FAQ/long-tail), astigmatism-night-vision (problem), contacts-vs-glasses (comparison) |
| **Children & myopia** | choosing-glasses-for-nearsighted-children · chon-kinh-cho-tre-em-can-thi | eye test page | essilor-stellest (product), myopia-statistics-vietnam-2026 (data/educational) |
| **Frames & fit** | how-to-choose-glasses-that-fit · chon-kinh-mat-phu-hop | `/en/frames.html` · `cua-hang.html` | choosing-frames-face-shape, gong-kinh-phu-hop-mat-tron (long-tail), caring-for-your-glasses (how-to) |
| **Same-day & foreigners** | `/en/same-day-glasses-hanoi.html` · `cat-kinh-can-lay-ngay.html`; `/en/prescription-glasses-hanoi.html` | same | `/en/glasses-in-hanoi-vs-at-home.html` (audience) |
| **About / trust** | why-choose-manh-long-optical · vi-sao-chon-manh-long-optical | store page | manh-long-optical-since-2000 |

Rules: every article belongs to exactly one cluster. Related card 1 = the cluster's pillar **article** where one exists, otherwise the closest parent topic (commercial pillars go in the body and in You-might-also-like). Card labels use the cluster name. Card 2 = the closest sibling. Card 3 = the next logical step. You-might-also-like must include the commercial page.

**Replace the 20 category labels with the 10 cluster names** in each article's eyebrow (VI: Tròng kính & thương hiệu · Đa tròng · Đổi màu & kính mát · Lớp phủ · Chất liệu & chiết suất · Đo mắt & đơn kính · Trẻ em & cận thị · Gọng & độ vừa · Lấy nhanh & khách nước ngoài · Về cửa hàng).

---

## 7. Cannibalisation register

| Risk | Pages | Action |
|---|---|---|
| **High** | VI `choosing-frames-face-shape.html` ↔ `chon-kinh-mat-phu-hop.html` (both "chọn gọng theo khuôn mặt") ↔ `gong-kinh-phu-hop-mat-tron.html` | **Differentiate.** chon-kinh-mat-phu-hop = pillar (face shape + prescription + fit). choosing-frames-face-shape → rename/reposition to the face-shape quick guide and link up. gong-kinh-phu-hop-mat-tron stays long-tail (round face only). If they can't be differentiated, **merge** into the pillar and add `rel=canonical` + a meta refresh (GitHub Pages can't do 301s). |
| **High** | EN `how-to-choose-glasses-that-fit` ↔ `choosing-frames-face-shape` | Same split: fit = pillar, face shape = supporting. |
| **High** | VI `essilor-transitions-gen-s.html` (price, "giá bao nhiêu") ↔ `photochromic-progressive-lenses.html` (H1 "…Giá Tốt…") | Remove the price angle from photochromic-progressive's H1/title ("Kính đa tròng đổi màu: hai việc trong một tròng"). The price intent belongs to essilor-transitions-gen-s. |
| **High (cross-domain)** | byryze `best-transitions-…`, `best-polarized-sunglasses-in-hanoi`, `prescription-glasses-in-hanoi-complete-guide-for-travelers` ↔ main-domain equivalents | See §1: consolidate onto manhlongoptical.com. |
| Medium | `blue-light-vs-uv` ↔ `kinh-chong-anh-sang-xanh-co-can-thiet` ↔ `essilor-eyezen` | Definition vs decision vs product. Keep, but each links to the other two with distinct anchors. |
| Medium | `so-sanh-essilor-vs-zeiss` ↔ `so-sanh-trong-kinh-theo-hang` ↔ `tron-kinh-cao-cap…` | Theo-hang = pillar, essilor-vs-zeiss = two-brand comparison, cao-cap = price/value. Titles must reflect this. |
| Medium | `lens-coatings-explained` ↔ `is-anti-reflective-coating-worth-it` | Overview vs single-coating decision. |
| Low | `manh-long-optical-since-2000` ↔ `why-choose-manh-long-optical`; stray `mang-long-optical-since-2000.html` (1 KB typo URL) | Check the stray file is a redirect only and excluded from the sitemap. |
| Gap | `multifocal-lenses-explained` has no VI version | Candidate new VI pillar ("Kính đa tròng là gì"), then run the cannibalisation check against `photochromic-progressive-lenses` and the Varilux pages. |

---

## 8. Internal linking

Path: Learn article → pillar → commercial service page → lens/product page → contact/store. Each article needs:

- 1 pillar link (in the body, not only in the cards)
- 1 commercial/service link
- 2–4 related Learn links, placed where the concept comes up
- 1 store/contact route (the CTA covers this)

Anchors must be descriptive and varied, e.g. "photochromic in progressive lenses", "what Essilor Transitions lenses cost", "lens index guide". Never "click here", "learn more" or "xem thêm" (the linter blocks them). Cross-language links get a "(page in Vietnamese)" note.

Entity chains to express naturally:

- Essilor → Varilux → progressive → presbyopia → fitting → adaptation
- Transitions → photochromic → UV activation → driving → polarized → prescription
- ZEISS → SmartLife / UVProtect → UV 400 nm → clear lens

---

## 9. Verified business facts (use only these)

| Fact | Value | Where it's published |
|---|---|---|
| Address | 147A Lê Duẩn, Cửa Nam, Hà Nội | mlong-seo NAP, GBP |
| Phone / Zalo / WhatsApp | 0777 986 999 | NAP |
| Email | mlong.optical@gmail.com | site footer |
| Eye test | free, whether you buy or not; about 20–30 minutes | eye-test pages |
| Frames | ~1,000 styles, 550,000–3,500,000đ | en/frames, lookbook |
| Photochromic prices | 350,000đ (Blick 1.56) → 7,980,000đ (Essilor 1.67) | photochromic-vs-polarized |
| Polarized | non-prescription sunglasses only | same |
| Author | Alvin Dao, Store Manager, 5 years in the trade | en/about-alvin.html |
| **Opening hours** | **CONFLICT: 8:00 (site) vs 8:30 (NAP 30/08)** | `[VERIFY BUSINESS FACT]` |
| **Transitions lines stocked** | Gen S documented; GEN 8 / XTRActive / Vantage / Style Mirrors unverified | `[VERIFY BUSINESS FACT]` |

Never invent certifications, credentials, partnerships, testing, reviews, warranties or turnaround times.

---

## 10. Per-article brief (fill in before writing or redesigning)

Complete these 15 sections before writing:

1. Search intent
2. Article role (pillar / supporting / commercial support / comparison / FAQ-long-tail / problem-solving / local support)
3. Keyword ownership: primary keyword, secondary keywords, competing Manh Long URLs
4. KEEP / IMPROVE / ADD / REMOVE versus the current page
5. Template (A–J) and why
6. H1, SEO title (≤ 60–65 chars), meta description (120–160), URL (keep the existing one if it already owns the intent)
7. Full outline
8. Visual / table / block plan
9. Internal-link plan (pillar, commercial, 2–4 Learn links, anchors)
10. CTA (from §5)
11. FAQ plan (real questions, each adding something new)
12. SEO/AEO/GEO: answer blocks, entities, schema
13. Fact-check list: every number and business claim, with its source
14. Cannibalisation check against §7
15. Final publishing QA (§11)

---

## 11. Publishing checklist

✅ = automated by `tools/learn_lint.py`. 👤 = needs human judgement.

- ✅ exactly one H1 · no heading jumps · no H4+
- ✅ back link, breadcrumb, deck, meta, direct answer (length), CTA (exactly one), takeaway, related (3–6, not self)
- ✅ TL;DR 3–6 bullets · TOC present when long · TOC anchors resolve
- ✅ image alt present and not just the H1 · images exist
- ✅ no broken internal links · no weak anchors · 3+ contextual body links
- ✅ no `[VERIFY…]`, `[CONFIRM…]`, `[ADD:…]`, `{{…}}` markers
- ✅ no "we tested" / "our lab" · hype phrases flagged
- ✅ title and meta length · canonical · learn.css linked
- ✅ JSON-LD parses · Article + BreadcrumbList present · FAQPage mirrors the visible FAQ · dateModified = visible updated date
- 👤 one primary intent, no duplicate intent (§7)
- 👤 every business fact is in §9 or newly confirmed by the owner
- 👤 technical/product claims sourced; manufacturer claims labelled as such
- 👤 CTA matches intent; only verified services
- 👤 hero shows the subject; no decorative stock
- 👤 no medical claims or diagnosis
- 👤 mobile check at 390 px (no horizontal scroll outside tables)

---

## 12. Rollout plan

The pilot is live-ready. Suggested order, one cluster per batch, pillar first:

1. Photochromic & sun: essilor-transitions-price, transitions-gen-s-advantages, photochromic-progressive (+ the VI pair of each, and fix the VI "Giá Tốt" title).
2. Frames & fit: resolve the §7 high-risk trio first, then migrate.
3. Coatings & protection.
4. Lens brands & premium.
5. Progressive (and the new VI multifocal pillar).
6. Eye exam & prescription, children, care, about.

Migrating the layout is not new content, so batches of 8–10 pages are fine. **Rewrites that add new sections** (TL;DR, criteria, FAQ changes) should follow the `anti-spam-scaling` pace and keep the 60/40 human layer. Each migrated page: copy the skeleton, move existing verified content into the blocks, run the linter, then screenshot at 1280 and 390 px.
