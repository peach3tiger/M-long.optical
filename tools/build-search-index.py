#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Sinh /search-index.json cho o tim kiem tren trang chu.

Chay:  python3 tools/build-search-index.py
Chay lai moi khi them trang moi hoac doi tieu de.
"""
import json, re, unicodedata, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT  = ROOT / "search-index.json"

BO_QUA = {"404.html", "trang-chu-moi.html", "mang-long-optical-since-2000.html"}

# Nhan hien thi ben canh ket qua
NHAN = [
    (r"^(trong-kinh|essilor|zeiss|varilux|crizal|transitions|photochromic|lens-coatings|blue-light|chiet-suat|so-sanh-trong|so-sanh-essilor|so-sanh-doi-mau|why-phones)", "Tròng kính"),
    (r"^(lookbook|cua-hang|gong-kinh|choosing-frames|chon-kinh-mat)", "Gọng kính"),
    (r"^(do-mat|cat-kinh|kinh-ram-can|kinh-mat-gan-day|uu-dai|khuyen-mai)", "Dịch vụ"),
]

# Tu khoa them tay: tim bang ten hang, ten dong, tu khoa khach hay go
THEM = {
    "essilor-eyezen.html": "eyezen start boost stock crizal sapphire hr blueuv capture dualoptim mo i mat may tinh man hinh 1780000 2980000",
    "trong-kinh-essilor-stellest.html": "stellest kiem soat can thi tre em halt airwear crizal rock 7200000 7500000",
    "essilor-transitions-gen-s.html": "transitions gen s doi mau photochromic xtractive",
    "transitions-gen-s-advantages.html": "transitions gen s uu diem doi mau",
    "varilux-comfort-max.html": "varilux comfort max da trong progressive lao thi",
    "varilux-physio-extensee-review.html": "varilux physio extensee da trong danh gia",
    "zeiss-smartlife-individual.html": "zeiss smartlife individual may do da trong",
    "zeiss-lenses.html": "zeiss da trong progressive",
    "zeiss-uvprotect.html": "zeiss uvprotect uv tia cuc tim",
    "trong-kinh-chemi.html": "chemi trong san trong danh han quoc",
    "trong-kinh-tokai.html": "tokai nhat ban 1.76 chiet suat cao",
    "crizal-natural-look.html": "crizal natural look vang phu chong choi",
    "crizal-easy-pro.html": "crizal easy pro vang phu",
    "lens-coatings-explained.html": "vang phu coating chong xuoc chong choi prevencia sapphire drive",
    "chiet-suat-trong-kinh.html": "chiet suat 1.56 1.60 1.67 1.74 index trong mong",
    "cua-hang.html": "gong kinh bo suu tap titanium acetate kim loai thu gong",
    "lookbook.html": "gong kinh anh mau phoi do",
    "do-mat-mien-phi-tron-doi.html": "do mat do khuc xa mien phi kham mat pd",
    "cat-kinh-can-lay-ngay.html": "cat kinh lay ngay trong ngay nhanh",
    "kinh-ram-can.html": "kinh ram kinh mat co do polarized",
    "cach-doc-don-kinh.html": "sph cyl axis add pd doc don kinh",
    "uu-dai.html": "khuyen mai combo gia uu dai thang 9",
    "index.html": "trang chu kinh mat manh long 147a le duan cua nam",
    "cau-hoi-thuong-gap.html": "faq hoi dap bao hanh doi tra ship",
    "ve-alvin.html": "alvin dao quan ly cua hang",
    "kinh-mat-gan-day.html": "gan ga ha noi hoan kiem cua nam ban do duong di",
}

def bo_dau(s: str) -> str:
    s = unicodedata.normalize("NFD", s)
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return s.replace("đ", "d").replace("Đ", "D").lower()

def go_the(s: str) -> str:
    s = re.sub(r"<(script|style|svg)\b.*?</\1>", " ", s, flags=re.S | re.I)
    s = re.sub(r"<!--.*?-->", " ", s, flags=re.S)
    s = re.sub(r"<[^>]+>", " ", s)
    s = (s.replace("&amp;", "&").replace("&nbsp;", " ")
          .replace("&quot;", '"').replace("&#39;", "'")
          .replace("&lt;", "<").replace("&gt;", ">"))
    return re.sub(r"\s+", " ", s).strip()

def nhan_cho(ten: str) -> str:
    for pat, lab in NHAN:
        if re.search(pat, ten):
            return lab
    return "Bài viết"

def main() -> int:
    muc = []
    for f in sorted(ROOT.glob("*.html")):
        if f.name in BO_QUA or f.name.startswith("google"):
            continue
        html = f.read_text(encoding="utf-8", errors="ignore")
        mt = re.search(r"<title>(.*?)</title>", html, re.S)
        if not mt:
            continue
        tieu_de = go_the(mt.group(1))
        tieu_de = re.sub(r"\s*[|–-]\s*(Manh Long Optical|Mạnh Long.*)$", "", tieu_de).strip()
        md = re.search(r'<meta name="description" content="(.*?)"', html, re.S)
        mo_ta = go_the(md.group(1)) if md else ""
        mo_ta = mo_ta[:150]
        h2 = " ".join(go_the(x) for x in re.findall(r"<h2[^>]*>(.*?)</h2>", html, re.S)[:8])
        url = "/" if f.name == "index.html" else "/" + f.name
        kho = " ".join([tieu_de, mo_ta, h2, THEM.get(f.name, "")])
        muc.append({
            "u": url,
            "t": tieu_de,
            "d": mo_ta,
            "c": "Trang chủ" if f.name == "index.html" else nhan_cho(f.name),
            "k": bo_dau(kho)[:600],
        })
    data = {"cap_nhat": __import__("datetime").date.today().isoformat(), "muc": muc}
    OUT.write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(f"{len(muc)} muc -> {OUT.name} ({OUT.stat().st_size} bytes)")
    return 0

if __name__ == "__main__":
    sys.exit(main())
