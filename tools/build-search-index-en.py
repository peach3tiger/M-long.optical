#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate /en/search-index.json for the EN homepage search box.

Mirrors tools/build-search-index.py (VN) but walks the English pages:
en/*.html (flat) plus en/learn/*.html (nested hub articles).

Run:  python3 tools/build-search-index-en.py
Re-run whenever an EN page is added or its title/description changes.
"""
import json, re, unicodedata, pathlib, sys, datetime

ROOT = pathlib.Path(__file__).resolve().parent.parent
EN = ROOT / "en"
OUT = EN / "search-index.json"

SKIP = {"404.html"}

LABELS = [
    (r"^(essilor|zeiss|varilux|crizal|transitions|photochromic|lens-|lenses)", "Lenses"),
    (r"^(lookbook|frames|choosing-frames)", "Frames"),
    (r"^offers", "Offers"),
    (r"^(eye-test|same-day|prescription-glasses|glasses-in-hanoi)", "Service"),
    (r"^faq", "FAQ"),
]

def strip_accents(s: str) -> str:
    s = unicodedata.normalize("NFD", s)
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return s.lower()

def strip_tags(s: str) -> str:
    s = re.sub(r"<(script|style|svg)\b.*?</\1>", " ", s, flags=re.S | re.I)
    s = re.sub(r"<!--.*?-->", " ", s, flags=re.S)
    s = re.sub(r"<[^>]+>", " ", s)
    s = (s.replace("&amp;", "&").replace("&nbsp;", " ")
          .replace("&quot;", '"').replace("&#39;", "'")
          .replace("&lt;", "<").replace("&gt;", ">"))
    return re.sub(r"\s+", " ", s).strip()

def label_for(name: str) -> str:
    for pat, lab in LABELS:
        if re.search(pat, name):
            return lab
    return "Article"

def collect(files, url_prefix):
    out = []
    for f in sorted(files):
        if f.name in SKIP:
            continue
        html = f.read_text(encoding="utf-8", errors="ignore")
        mt = re.search(r"<title>(.*?)</title>", html, re.S)
        if not mt:
            continue
        title = strip_tags(mt.group(1))
        title = re.sub(r"\s*[|–-]\s*Manh Long Optical.*$", "", title).strip()
        md = re.search(r'<meta name="description" content="(.*?)"', html, re.S)
        desc = strip_tags(md.group(1)) if md else ""
        desc = desc[:150]
        h2 = " ".join(strip_tags(x) for x in re.findall(r"<h2[^>]*>(.*?)</h2>", html, re.S)[:8])
        is_home = f.name == "index.html" and url_prefix.rstrip("/") == "/en"
        if f.name == "index.html":
            url = url_prefix if url_prefix.endswith("/") else url_prefix + "/"
        else:
            url = url_prefix.rstrip("/") + "/" + f.name
        cat = "Home" if is_home else label_for(f.name)
        kw = " ".join([title, desc, h2])
        out.append({
            "u": url,
            "t": title,
            "d": desc,
            "c": cat,
            "k": strip_accents(kw)[:600],
        })
    return out

def main() -> int:
    muc = []
    muc += collect(EN.glob("*.html"), "/en")
    muc += collect((EN / "learn").glob("*.html"), "/en/learn")
    data = {"cap_nhat": datetime.date.today().isoformat(), "muc": muc}
    OUT.write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(f"{len(muc)} items -> {OUT.relative_to(ROOT)} ({OUT.stat().st_size} bytes)")
    return 0

if __name__ == "__main__":
    sys.exit(main())
