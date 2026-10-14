#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Sinh luoi anh "Danh gia khach hang" / "Customer Feedback" tu data/customer-feedback.json.

Chay:  python3 tools/build-customer-feedback.py
Ghi de cac doan nam giua marker trong /lookbook.html va /en/lookbook.html:
    <!-- feedback-rating:start -->  ... <!-- feedback-rating:end -->
    <!-- feedback-photos:start -->  ... <!-- feedback-photos:end -->
    <!-- feedback-text:start -->    ... <!-- feedback-text:end -->
Khong sua tay phan nam giua marker — sua JSON roi chay lai.

URL giu nguyen lookbook.html de khong mat thu hang (canonical cu).

LUAT DU LIEU (khong noi long):
- Chi dang khach THAT. Khong anh AI, khong anh stock, khong ten bia, khong quoc tich doan.
- Anh khach: chi dang khi "permission" la "confirmed" (chu shop da hoi khach)
  hoac "homepage-published" (anh da len trang chu truoc do — van can chu shop xac nhan
  lai, script se canh bao). Gia tri khac => script DUNG, khong ghi file.
- Ghep anh voi mot danh gia Google: "review_link" phai la "confirmed" hoac
  "homepage-published". Khong chac => de "photo": null, danh gia van hien o phan chu.
- "country": chi dien khi da xac minh VA khach dong y cong khai. Mac dinh null.
- Khong lay anh dai dien tu Google Reviews.
- Khong them schema Review / AggregateRating.

Them mot khach co anh:
  1. Anh doc 3:4, xuat WebP (va AVIF neu duoc) vao /uploads-opt/, ten khach-<ten>-480w.webp|.avif
  2. Them muc vao "customers" trong JSON (xem cac muc co san), "photo.w/h" la kich thuoc that.
  3. Chay script nay, mo trang kiem tra, roi moi commit.
"""
import html, json, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "customer-feedback.json"
PAGES = {"vi": ROOT / "lookbook.html", "en": ROOT / "en" / "lookbook.html"}

OK_PERMISSION = {"confirmed", "homepage-published"}

T = {
    "vi": {
        "open": "Xem ảnh lớn và toàn bộ nhận xét của {name}",
        "hint": "Xem ảnh lớn và toàn bộ nhận xét ›",
        "google": "Đánh giá trên Google",
        "maps": "Xem trên Google Maps",
        "translated": "Dịch từ tiếng Anh. Nguyên văn:",
        "rating": '<strong>{score} trên 5</strong> từ {count} đánh giá trên Google, tính tới {as_of}.',
        "rating_link": "Đọc tất cả đánh giá",
        "invite_kicker": "Ảnh của bạn",
        "invite_h": "Bạn đã cắt kính ở Mạnh Long?",
        "invite_p": "Gửi bên mình một tấm ảnh bạn đeo kính qua Zalo hoặc WhatsApp 0777 986 999. Ảnh chỉ lên trang khi bạn đồng ý, tên ghi theo cách bạn muốn, và bên mình gỡ ngay khi bạn yêu cầu.",
        "invite_a1": ("https://zalo.me/0777986999", "Gửi ảnh qua Zalo"),
        "invite_a2": ("https://wa.me/84777986999", "WhatsApp"),
    },
    "en": {
        "open": "View the larger photo and full feedback from {name}",
        "hint": "View larger photo and full feedback ›",
        "google": "Google review",
        "maps": "See it on Google Maps",
        "translated": "",
        "rating": '<strong>{score} out of 5</strong> from {count} Google reviews, as of {as_of}.',
        "rating_link": "Read every review",
        "invite_kicker": "Your photo",
        "invite_h": "Got your glasses here?",
        "invite_p": "Send us a photo of you wearing them on WhatsApp or Zalo, 0777 986 999. It goes on this page only with your permission, with your name shown the way you choose, and we take it down whenever you ask.",
        "invite_a1": ("https://wa.me/84777986999", "Send on WhatsApp"),
        "invite_a2": ("https://zalo.me/0777986999", "Zalo"),
    },
}

e = lambda s: html.escape(s, quote=True)


def quote_for(c, lang):
    if lang == "vi" and c.get("quote_orig_lang") != "vi":
        return c["quote_vi"], "vi"
    return c["quote_orig"], c.get("quote_orig_lang", "en")


def orig_note(c, lang):
    if lang == "vi" and c.get("quote_orig_lang") == "en":
        return (f'<p class="fborig">{T["vi"]["translated"]} '
                f'<span lang="en">“{e(c["quote_orig"])}”</span></p>')
    return ""


def src_line(c, lang, maps):
    t = T[lang]
    return (f'<p class="fbsrc">{t["google"]} · <a href="{e(maps)}" target="_blank" '
            f'rel="noopener nofollow">{t["maps"]}</a></p>')


def photo_card(c, i, lang, maps):
    p = c["photo"]
    q, ql = quote_for(c, lang)
    alt = p["alt_" + lang]
    base = p["base"]
    avif = (ROOT / "uploads-opt" / f"{base}.avif").exists()
    load = ' loading="eager" fetchpriority="high"' if i == 0 else ' loading="lazy"'
    pic = ('<picture>'
           + (f'<source type="image/avif" srcset="/uploads-opt/{base}.avif">' if avif else "")
           + f'<img src="/uploads-opt/{base}.webp" width="{p["w"]}" height="{p["h"]}" alt="{e(alt)}"{load} decoding="async">'
           + '</picture>')
    return (
        f'<article class="fbcard" id="kh-{e(c["id"])}" data-i="{i}">\n'
        f'  <button type="button" class="fbphoto" data-i="{i}" aria-haspopup="dialog" '
        f'aria-label="{e(T[lang]["open"].format(name=c["name"]))}">{pic}</button>\n'
        f'  <div class="fbbody">\n'
        f'    <blockquote class="fbquote" lang="{ql}"><p>“{e(q)}”</p></blockquote>\n'
        f'    <p class="fbwho">{e(c["name"])}</p>\n'
        f'    {src_line(c, lang, maps)}\n'
        + (f'    <div class="fbmore" hidden>{orig_note(c, lang)}</div>\n' if orig_note(c, lang) else "")
        + f'    <p class="fbhint" aria-hidden="true">{T[lang]["hint"]}</p>\n'
        + '  </div>\n</article>'
    )


def invite_card(lang):
    t = T[lang]
    return (
        '<aside class="fbinvite">\n'
        f'  <p class="fbkick">{t["invite_kicker"]}</p>\n'
        f'  <h2>{t["invite_h"]}</h2>\n'
        f'  <p>{t["invite_p"]}</p>\n'
        f'  <p class="fbbtns"><a class="fbbtn" href="{t["invite_a1"][0]}" target="_blank" rel="noopener">{t["invite_a1"][1]}</a>'
        f'<a class="fbbtn ghost" href="{t["invite_a2"][0]}" target="_blank" rel="noopener">{t["invite_a2"][1]}</a></p>\n'
        '</aside>'
    )


def text_card(c, lang, maps):
    q, ql = quote_for(c, lang)
    return (
        '<figure class="fbtext">\n'
        f'  <blockquote class="fbquote" lang="{ql}"><p>“{e(q)}”</p></blockquote>\n'
        f'  <figcaption><span class="fbwho">{e(c["name"])}</span>{src_line(c, lang, maps)}</figcaption>\n'
        + (f'  {orig_note(c, lang)}\n' if orig_note(c, lang) else "")
        + '</figure>'
    )


def check(data):
    errs, warns = [], []
    for c in data["customers"]:
        if not c.get("publish"):
            continue
        cid = c.get("id", "?")
        if c.get("source") != "google":
            errs.append(f"{cid}: chi ho tro nguon 'google' (co link goc). Nguon khac can them code + link goc.")
        if not c.get("name_shown_as_on_google"):
            errs.append(f"{cid}: ten phai giong het ten hien tren Google.")
        if c.get("country"):
            warns.append(f"{cid}: co 'country' — chi giu neu da xac minh va khach dong y cong khai (hien chua hien len trang).")
        p = c.get("photo")
        if p:
            if p.get("permission") not in OK_PERMISSION:
                errs.append(f"{cid}: anh chua co quyen dang (permission={p.get('permission')!r}).")
            if p.get("review_link") not in OK_PERMISSION:
                errs.append(f"{cid}: chua xac minh nguoi trong anh la nguoi viet danh gia (review_link={p.get('review_link')!r}).")
            if p.get("permission") != "confirmed" or p.get("review_link") != "confirmed":
                warns.append(f"{cid}: anh dang o muc 'homepage-published' — chu shop can xac nhan lai roi doi thanh 'confirmed'.")
            if not (ROOT / "uploads-opt" / f"{p['base']}.webp").exists():
                errs.append(f"{cid}: khong thay /uploads-opt/{p['base']}.webp")
            if not (p.get("w") and p.get("h")):
                errs.append(f"{cid}: thieu w/h (chong giat trang).")
    return errs, warns


def replace_block(src, name, body, path):
    pat = re.compile(rf"(<!-- {name}:start[^>]*-->)(.*?)(<!-- {name}:end -->)", re.S)
    if not pat.search(src):
        sys.exit(f"Khong thay marker {name} trong {path}")
    return pat.sub(lambda m: m.group(1) + "\n" + body + "\n" + m.group(3), src, count=1)


def main():
    data = json.loads(DATA.read_text(encoding="utf-8"))
    errs, warns = check(data)
    for w in warns:
        print("CANH BAO:", w)
    if errs:
        for x in errs:
            print("LOI:", x)
        sys.exit(1)
    maps = data["google_maps_url"]
    pub = [c for c in data["customers"] if c.get("publish")]
    with_photo = [c for c in pub if c.get("photo")]
    text_only = [c for c in pub if not c.get("photo")]
    r = data["rating"]
    for lang, path in PAGES.items():
        t = T[lang]
        rating = (f'<p class="fbrating">{t["rating"].format(score=r["score_" + lang], count=r["count"], as_of=r["as_of_" + lang])} '
                  f'<a href="{e(maps)}" target="_blank" rel="noopener nofollow">{t["rating_link"]} &#8594;</a></p>')
        photos = "\n".join(photo_card(c, i, lang, maps) for i, c in enumerate(with_photo)) + "\n" + invite_card(lang)
        texts = "\n".join(text_card(c, lang, maps) for c in text_only)
        src = path.read_text(encoding="utf-8")
        src = replace_block(src, "feedback-rating", rating, path)
        src = replace_block(src, "feedback-photos", photos, path)
        src = replace_block(src, "feedback-text", texts, path)
        path.write_text(src, encoding="utf-8")
        print(f"{path.relative_to(ROOT)}: {len(with_photo)} the co anh, {len(text_only)} the chu")


if __name__ == "__main__":
    main()
