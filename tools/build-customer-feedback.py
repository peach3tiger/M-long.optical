#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Sinh noi dung trang "Danh gia khach hang" / "Customer Feedback" tu data/customer-feedback.json.

Chay:  python3 tools/build-customer-feedback.py          (ghi trang)
       python3 tools/build-customer-feedback.py --check  (chi kiem du lieu, khong ghi)

Ghi de cac doan giua marker trong /lookbook.html va /en/lookbook.html:
    feedback-rating   dong diem Google co ngay
    feedback-stories  "Cau chuyen khach hang": the CO ANH (chi khi khach da dong y)
    feedback-reviews  "Danh gia tren Google": the CHU, khong anh
    feedback-invite   loi moi gui anh (chi hien rieng khi chua co cau chuyen nao)
    feedback-topics   "Danh gia ve kinh da trong & Varilux": the CHU co bo loc theo chu de
Khong sua tay giua marker — sua JSON roi chay lai.
URL giu nguyen lookbook.html de khong mat thu hang.

HAI LOAI NOI DUNG, TACH RIENG:
1. "stories" — anh khach + loi chia se. Chi hien khi:
     publish = true  VA  consent = "confirmed"  (chu shop da hoi khach, ghi lai ngay/kenh)
   Ten chi hien khi name_consent = true.
   Chi duoc gan voi mot danh gia Google (google_review_id) khi identity_verified = true,
   tuc la chu shop da xac minh nguoi trong anh chinh la nguoi viet danh gia do.
   Khong co danh gia da xac minh thi phai co story_orig: loi khach chia se truc tiep voi
   cua hang va dong y cho dang.
2. "google_reviews" — chi chu. Ten ghi dung nhu tren Google, kem link ve Google Maps.
   Khong bao gio gan anh vao day. Chi hien khi verification = "verified" VA reuse = "approved".
   "topics" (progressive / varilux): CHI gan khi chinh nguyen van danh gia (quote_orig) chua
   tu khoa trong "topic_keywords". Script tu kiem; khong duoc tu suy loai trong tu loi khen chung.
   Danh gia trung nhau (cung id, hoac noi dung trung/chua trong nhau) => script DUNG.

LUAT KHONG NOI LONG:
- Khong anh AI, anh stock, anh nguoi mau, khong lay anh dai dien tu Google Reviews.
- Khong bia ten, quoc tich, loi nhan xet. Khong them schema Review / AggregateRating.
Script DUNG (khong ghi file) neu mot muc vi pham.
"""
import html, json, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "customer-feedback.json"
PAGES = {"vi": ROOT / "lookbook.html", "en": ROOT / "en" / "lookbook.html"}

T = {
    "vi": {
        "stories_h": "Câu chuyện khách hàng",
        "reviews_h": "Đánh giá trên Google",
        "open": "Xem ảnh lớn và toàn bộ chia sẻ của {name}",
        "hint": "Xem ảnh lớn và toàn bộ chia sẻ ›",
        "anon": "Khách của cửa hàng",
        "google": "Đánh giá trên Google",
        "direct": "Chia sẻ trực tiếp với cửa hàng, đăng khi khách đồng ý",
        "maps": "Xem trên Google Maps",
        "translated": "Dịch từ tiếng Anh. Nguyên văn:",
        "rating": '<strong>{score} trên 5</strong> từ {count} đánh giá trên Google, tính tới {as_of}.',
        "rating_link": "Đọc tất cả đánh giá",
        "invite_kicker": "Ảnh của bạn",
        "invite_h": "Bạn đã cắt kính ở Mạnh Long?",
        "invite_p": "Gửi bên mình một tấm ảnh bạn đeo kính qua Zalo hoặc WhatsApp 0777 986 999. Ảnh chỉ lên trang khi bạn đồng ý, tên ghi theo cách bạn muốn, và bên mình gỡ ngay khi bạn yêu cầu.",
        "invite_a1": ("https://zalo.me/0777986999", "Gửi ảnh qua Zalo"),
        "invite_a2": ("https://wa.me/84777986999", "WhatsApp"),
        "topics_h": "Đánh giá khách hàng về kính đa tròng & Varilux",
        "topics_p": "Chỉ gồm những đánh giá mà chính khách nhắc tới đa tròng hoặc Varilux trong lời viết. Bên mình không tự gán loại tròng cho lời khen chung chung.",
        "topics_h_progressive": "Đánh giá khách hàng về kính đa tròng",
        "topics_p_progressive": "Chỉ gồm những đánh giá mà chính khách nhắc tới kính đa tròng trong lời viết. Bên mình không tự gán loại tròng cho lời khen chung chung.",
        "filter_label": "Lọc đánh giá theo loại tròng",
        "f_all": "Tất cả", "f_progressive": "Đa tròng / Progressive", "f_varilux": "Essilor Varilux",
        "tag_progressive": "Đa tròng", "tag_varilux": "Varilux",
        "status": "Đang hiện {n} đánh giá.",
        "empty": "Chưa có đánh giá công khai nào nhắc trực tiếp tới mục này.",
        "more": "Xem thêm đánh giá",
    },
    "en": {
        "stories_h": "Customer stories",
        "reviews_h": "Reviews on Google",
        "open": "View the larger photo and full story from {name}",
        "hint": "View larger photo and full story ›",
        "anon": "A customer of the shop",
        "google": "Google review",
        "direct": "Shared directly with the shop, published with permission",
        "maps": "See it on Google Maps",
        "translated": "",
        "rating": '<strong>{score} out of 5</strong> from {count} Google reviews, as of {as_of}.',
        "rating_link": "Read every review",
        "invite_kicker": "Your photo",
        "invite_h": "Got your glasses here?",
        "invite_p": "Send us a photo of you wearing them on WhatsApp or Zalo, 0777 986 999. It goes on this page only with your permission, with your name shown the way you choose, and we take it down whenever you ask.",
        "invite_a1": ("https://wa.me/84777986999", "Send on WhatsApp"),
        "invite_a2": ("https://zalo.me/0777986999", "Zalo"),
        "topics_h": "Customer Reviews: Progressive Lenses & Varilux",
        "topics_p": "Only reviews in which the customer mentions progressive lenses or Varilux in their own words. We never assign a lens type to general praise.",
        "topics_h_progressive": "Customer Reviews: Progressive Lenses",
        "topics_p_progressive": "Only reviews in which the customer mentions progressive lenses in their own words. We never assign a lens type to general praise.",
        "filter_label": "Filter reviews by lens type",
        "f_all": "All reviews", "f_progressive": "Multifocal / Progressive", "f_varilux": "Essilor Varilux",
        "tag_progressive": "Progressive", "tag_varilux": "Varilux",
        "status": "Reviews shown: {n}",
        "empty": "No public review mentions this directly yet.",
        "more": "Show more reviews",
    },
}
TOPICS = ("progressive", "varilux")

e = lambda s: html.escape(s, quote=True)


def text_in(orig, orig_lang, vi, lang):
    """Return (text, lang_of_text, original_note_html)."""
    if lang == "vi" and orig_lang and orig_lang != "vi" and vi:
        note = f'<p class="fborig">{T["vi"]["translated"]} <span lang="{orig_lang}">“{e(orig)}”</span></p>'
        return vi, "vi", note
    return orig, orig_lang or lang, ""


def maps_link(lang, maps):
    return (f'<a href="{e(maps)}" target="_blank" rel="noopener nofollow">{T[lang]["maps"]}</a>')


# ---------- the CO ANH: cau chuyen khach hang ----------
def story_card(s, i, lang, maps, reviews):
    t = T[lang]
    p = s["photo"]
    name = s["display_name"] if s.get("name_consent") and s.get("display_name") else t["anon"]
    if s.get("google_review_id"):
        r = reviews[s["google_review_id"]]
        q, ql, note = text_in(r["quote_orig"], r["quote_orig_lang"], r.get("quote_vi"), lang)
        src = f'<p class="fbsrc">{t["google"]} · {maps_link(lang, maps)}</p>'
    else:
        q, ql, note = text_in(s["story_orig"], s["story_orig_lang"], s.get("story_vi"), lang)
        src = f'<p class="fbsrc">{t["direct"]}</p>'
    base = p["base"]
    avif = (ROOT / "uploads-opt" / f"{base}.avif").exists()
    load = ' loading="eager" fetchpriority="high"' if i == 0 else ' loading="lazy"'
    pic = ('<picture>'
           + (f'<source type="image/avif" srcset="/uploads-opt/{base}.avif">' if avif else "")
           + f'<img src="/uploads-opt/{base}.webp" width="{p["w"]}" height="{p["h"]}" alt="{e(p["alt_" + lang])}"{load} decoding="async">'
           + '</picture>')
    return (
        f'<article class="fbcard" id="kh-{e(s["id"])}" data-i="{i}">\n'
        f'  <button type="button" class="fbphoto" data-i="{i}" aria-haspopup="dialog" '
        f'aria-label="{e(t["open"].format(name=name))}">{pic}</button>\n'
        '  <div class="fbbody">\n'
        f'    <blockquote class="fbquote" lang="{ql}"><p>“{e(q)}”</p></blockquote>\n'
        f'    <p class="fbwho">{e(name)}</p>\n'
        f'    {src}\n'
        + (f'    <div class="fbmore" hidden>{note}</div>\n' if note else "")
        + f'    <p class="fbhint" aria-hidden="true">{t["hint"]}</p>\n'
        '  </div>\n</article>'
    )


def invite_card(lang, solo=False):
    t = T[lang]
    return (
        f'<aside class="fbinvite{" fbinvite-solo" if solo else ""}">\n'
        f'  <p class="fbkick">{t["invite_kicker"]}</p>\n'
        f'  <h2>{t["invite_h"]}</h2>\n'
        f'  <p>{t["invite_p"]}</p>\n'
        f'  <p class="fbbtns"><a class="fbbtn" href="{t["invite_a1"][0]}" target="_blank" rel="noopener">{t["invite_a1"][1]}</a>'
        f'<a class="fbbtn ghost" href="{t["invite_a2"][0]}" target="_blank" rel="noopener">{t["invite_a2"][1]}</a></p>\n'
        '</aside>'
    )


# ---------- the CHU: danh gia Google ----------
def review_card(r, lang, maps, tagged=False):
    t = T[lang]
    q, ql, note = text_in(r["quote_orig"], r["quote_orig_lang"], r.get("quote_vi"), lang)
    topics = [x for x in r.get("topics", []) if x in TOPICS]
    attr = f' data-topics="{e(" ".join(topics))}"' if tagged else ""
    tags = ("  <p class=\"fbtags\">" + "".join(f'<span class="fbtag">{t["tag_" + x]}</span>' for x in topics) + "</p>\n") if tagged and topics else ""
    return (
        f'<figure class="fbtext"{attr}>\n' + tags
        + f'  <blockquote class="fbquote" lang="{ql}"><p>“{e(q)}”</p></blockquote>\n'
        f'  <figcaption><span class="fbwho">{e(r["name"])}</span>'
        f'<p class="fbsrc">{t["google"]} · {maps_link(lang, maps)}</p></figcaption>\n'
        + (f'  {note}\n' if note else "")
        + '</figure>'
    )


def topics_section(revs, lang, maps):
    t = T[lang]
    items = [r for r in revs if any(x in TOPICS for x in r.get("topics", []))]
    if not items:
        return ""
    cnt = {"all": len(items), **{x: sum(1 for r in items if x in r.get("topics", [])) for x in TOPICS}}
    # 15/10/2026: chu de nao chua co danh gia thi KHONG hien nut loc / tieu de cho chu de do.
    # Chi hien thanh loc khi co tu 2 chu de tro len co danh gia (1 chu de thi loc la thua).
    live = [x for x in TOPICS if cnt[x]]
    key = "" if len(live) > 1 else "_" + live[0]
    filters = ""
    if len(live) > 1:
        chips = "".join(
            f'<button type="button" class="fbchip" data-filter="{k}" aria-pressed="{"true" if k == "all" else "false"}">'
            f'{t["f_" + k]} <span class="fbcount-n">({cnt[k]})</span></button>' for k in ["all"] + live)
        filters = (f'<div class="fbfilters" role="group" aria-label="{e(t["filter_label"])}" hidden>{chips}</div>\n'
                   f'<p class="fbstatus" role="status" aria-live="polite" data-tpl="{e(t["status"])}"></p>\n')
    return (
        '<section class="fbtopics" id="danh-gia-da-trong" aria-labelledby="fb-topics-h">\n'
        f'<h2 id="fb-topics-h" class="fbh2">{t["topics_h" + key]}</h2>\n'
        f'<p class="fbtopics-p">{t["topics_p" + key]}</p>\n'
        + filters +
        '<div class="fbtexts fbtopiclist">\n'
        + "\n".join(review_card(r, lang, maps, tagged=True) for r in items)
        + "\n</div>\n"
        f'<p class="fbempty" hidden>{t["empty"]}</p>\n'
        f'<button type="button" class="fbmorebtn" hidden>{t["more"]}</button>\n'
        '</section>')


def check(data):
    errs, held = [], []
    reviews = {r["id"]: r for r in data.get("google_reviews", [])}
    kws = data.get("topic_keywords", {})
    seen_ids, seen_txt = set(), []
    norm = lambda x: re.sub(r"[^\w]+", " ", (x or "").lower(), flags=re.U).strip()
    for r in data.get("google_reviews", []):
        rid = r.get("id", "?")
        if rid in seen_ids:
            errs.append(f"review {rid}: id bi trung")
        seen_ids.add(rid)
        nt = norm(r.get("quote_orig"))
        for oid, ot in seen_txt:
            if nt and ot and (nt == ot or (min(len(nt), len(ot)) > 40 and (nt in ot or ot in nt))):
                errs.append(f"review {rid}: noi dung trung voi {oid} (danh gia sao chep/trung lap)")
        seen_txt.append((rid, nt))
        if r.get("verification") not in ("verified", "pending") or r.get("reuse") not in ("approved", "pending"):
            errs.append(f"review {rid}: verification/reuse phai la verified|pending va approved|pending")
        for tp in r.get("topics", []):
            if tp not in TOPICS:
                errs.append(f"review {rid}: topic {tp!r} khong hop le")
            elif not any(k.lower() in (r.get("quote_orig") or "").lower() for k in kws.get(tp, [])):
                errs.append(f"review {rid}: gan topic {tp!r} nhung nguyen van khong nhac tu khoa nao — khong duoc tu suy")
        for k in ("id", "name", "quote_orig", "quote_orig_lang"):
            if not r.get(k):
                errs.append(f"review {r.get('id', '?')}: thieu '{k}'")
        if r.get("quote_orig_lang") != "vi" and not r.get("quote_vi"):
            errs.append(f"review {r['id']}: thieu ban dich 'quote_vi'")
        if "photo" in r:
            errs.append(f"review {r['id']}: danh gia Google khong duoc co anh — chuyen sang 'stories'")
    for s in data.get("stories", []):
        sid = s.get("id", "?")
        if s.get("google_review_id") and not s.get("identity_verified"):
            errs.append(f"story {sid}: gan voi danh gia Google nhung chua xac minh danh tinh (identity_verified=false)")
        if not s.get("publish"):
            held.append(f"{sid} (consent={s.get('consent')}, identity_verified={s.get('identity_verified')})")
            continue
        if s.get("consent") != "confirmed":
            errs.append(f"story {sid}: publish=true nhung consent={s.get('consent')!r} — chi dang khi 'confirmed'")
        if s.get("display_name") and not s.get("name_consent"):
            errs.append(f"story {sid}: co display_name nhung name_consent=false")
        rid = s.get("google_review_id")
        if rid and rid not in reviews:
            errs.append(f"story {sid}: google_review_id {rid!r} khong co trong google_reviews")
        if not rid and not s.get("story_orig"):
            errs.append(f"story {sid}: khong co loi chia se (story_orig) va khong co danh gia da xac minh")
        if not rid and s.get("story_orig_lang") not in (None, "vi") and not s.get("story_vi"):
            errs.append(f"story {sid}: thieu ban dich story_vi")
        p = s.get("photo") or {}
        if not p:
            errs.append(f"story {sid}: thieu anh")
        else:
            if not (ROOT / "uploads-opt" / f"{p.get('base')}.webp").exists():
                errs.append(f"story {sid}: khong thay /uploads-opt/{p.get('base')}.webp")
            if not (p.get("w") and p.get("h")):
                errs.append(f"story {sid}: thieu w/h (chong giat trang)")
            if not (p.get("alt_vi") and p.get("alt_en")):
                errs.append(f"story {sid}: thieu alt_vi/alt_en")
    return errs, held, reviews


def replace_block(src, name, body, path):
    pat = re.compile(rf"(<!-- {name}:start[^>]*-->)(.*?)(<!-- {name}:end -->)", re.S)
    if not pat.search(src):
        sys.exit(f"Khong thay marker {name} trong {path}")
    return pat.sub(lambda m: m.group(1) + ("\n" + body + "\n" if body else "\n") + m.group(3), src, count=1)


def main():
    data = json.loads(DATA.read_text(encoding="utf-8"))
    errs, held, reviews = check(data)
    for h in held:
        print("CHUA DANG (cho xac nhan):", h)
    if errs:
        for x in errs:
            print("LOI:", x)
        sys.exit(1)
    if "--check" in sys.argv:
        print("Du lieu hop le.")
        return
    maps = data["google_maps_url"]
    stories = [s for s in data.get("stories", []) if s.get("publish")]
    revs = [x for x in data.get("google_reviews", []) if x.get("verification") == "verified" and x.get("reuse") == "approved"]
    r = data["rating"]
    for lang, path in PAGES.items():
        t = T[lang]
        rating = (f'<p class="fbrating">{t["rating"].format(score=r["score_" + lang], count=r["count"], as_of=r["as_of_" + lang])} '
                  f'<a href="{e(maps)}" target="_blank" rel="noopener nofollow">{t["rating_link"]} &#8594;</a></p>')
        if stories:
            st = (f'<section aria-labelledby="fb-stories-h">\n<h2 id="fb-stories-h" class="fbh2">{t["stories_h"]}</h2>\n'
                  '<div class="fbgrid" id="fbgrid">\n'
                  + "\n".join(story_card(s, i, lang, maps, reviews) for i, s in enumerate(stories))
                  + "\n" + invite_card(lang) + "\n</div>\n</section>")
            invite = ""
        else:
            # 14/10/2026: chu shop yeu cau tam an loi moi gui anh khi chua co cau chuyen nao.
            # Muon hien lai: doi thanh  invite = invite_card(lang, solo=True)
            st = ""
            invite = ""
        rv = (f'<section aria-labelledby="fb-reviews-h">\n<h2 id="fb-reviews-h" class="fbh2">{t["reviews_h"]}</h2>\n'
              '<div class="fbtexts">\n'
              + "\n".join(review_card(x, lang, maps) for x in revs)
              + "\n</div>\n</section>")
        src = path.read_text(encoding="utf-8")
        src = replace_block(src, "feedback-rating", rating, path)
        src = replace_block(src, "feedback-stories", st, path)
        src = replace_block(src, "feedback-reviews", rv, path)
        src = replace_block(src, "feedback-invite", invite, path)
        src = replace_block(src, "feedback-topics", topics_section(revs, lang, maps), path)
        path.write_text(src, encoding="utf-8")
        nt = sum(1 for x in revs if x.get("topics"))
        print(f"{path.relative_to(ROOT)}: {len(stories)} cau chuyen co anh, {len(revs)} danh gia Google, {nt} danh gia theo chu de")


if __name__ == "__main__":
    main()
