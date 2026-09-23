#!/usr/bin/env python3
"""Learn article QA linter — Manh Long Optical.

Usage:
  python3 tools/learn_lint.py en/learn/photochromic-vs-polarized-sunglasses.html
  python3 tools/learn_lint.py --all          # every page that links /assets/learn.css
  python3 tools/learn_lint.py --audit        # legacy pages: report which still need migrating

Automates the mechanical half of the publishing checklist in
docs/learn-editorial-system.md. ERROR = must fix before publishing.
WARN = needs a human decision. Editorial checks (intent, cannibalisation,
fact accuracy) still need a person.
"""
import glob, json, os, re, sys
from bs4 import BeautifulSoup

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MARKERS = re.compile(r"\[(VERIFY[^\]]*|CONFIRM[^\]]*|ADD:[^\]]*|CẦN[^\]]*|STATUS: DRAFT[^\]]*)\]|\{\{")
FAKE_TEST = re.compile(r"\b(we|our team) (independently )?tested\b|our lab|chúng tôi đã (thử nghiệm|test)", re.I)
HYPE = re.compile(r"\b(the absolute best|number one|#1|perfect for everyone|best in (the world|hanoi))\b|tốt nhất thế giới|số 1", re.I)
WEAK_ANCHOR = re.compile(r"^(click here|learn more|read more|read this|here|xem thêm|tại đây|bấm vào đây)$", re.I)


def page_exists(href):
    if not href.startswith("/") or href.startswith("//"):
        return True
    path = href.split("#")[0].split("?")[0]
    if path.endswith("/"):
        path += "index.html"
    return os.path.exists(os.path.join(ROOT, path.lstrip("/")))


def lint(path):
    E, W = [], []
    s = BeautifulSoup(open(path, encoding="utf-8").read(), "html.parser")
    main = s.select_one("main.la")
    if not main:
        return ["not migrated: no <main class=\"la\">"], []

    # structure
    h1 = s.find_all("h1")
    if len(h1) != 1: E.append(f"{len(h1)} H1 tags (need exactly 1)")
    for sel, name in [(".la-back", "back link"), (".la-crumb", "breadcrumb"), (".la-deck", "subtitle/deck"),
                      (".la-meta", "author/date/read-time"), (".la-answer", "direct answer"),
                      (".la-cta", "CTA"), (".la-remember", "final takeaway"), (".la-related", "related articles")]:
        if not main.select_one(sel): E.append(f"missing {name} ({sel})")
    if not main.select_one(".la-hero img"): W.append("no hero image")
    if not main.select_one(".la-tldr"): W.append("no TL;DR (ok only for short FAQ/long-tail pages)")
    if len(main.select(".la-cta")) > 1: E.append("more than one CTA block")

    # heading hierarchy
    last = 1
    for h in main.find_all(re.compile("^h[1-6]$")):
        lvl = int(h.name[1])
        if lvl > last + 1: E.append(f"heading jump h{last}→h{lvl}: '{h.get_text(strip=True)[:50]}'")
        if lvl >= 4: W.append(f"h{lvl} used — template stops at h3")
        last = lvl

    # direct answer length
    ans = main.select_one(".la-answer")
    if ans:
        n = len(" ".join(p.get_text(" ", strip=True) for p in ans.find_all("p")).split())
        if not 35 <= n <= 110: W.append(f"direct answer is {n} words (target 40–90)")
    tl = main.select(".la-tldr li")
    if tl and not 3 <= len(tl) <= 6: W.append(f"TL;DR has {len(tl)} bullets (target 3–6)")

    # TOC anchors
    ids = {t.get("id") for t in main.find_all(id=True)}
    for a in main.select(".la-toc a"):
        if a["href"].lstrip("#") not in ids: E.append(f"TOC link to missing anchor {a['href']}")
    h2n = len([h for h in main.find_all("h2") if not h.find_parent(class_=re.compile("la-(tldr|cta|related|more|remember)"))])
    words = len(main.get_text(" ").split())
    if not main.select_one(".la-toc") and (h2n >= 6 or words > 1400): W.append(f"no TOC ({h2n} H2, ~{words} words)")

    # images
    for img in main.find_all("img"):
        alt = (img.get("alt") or "").strip()
        if not alt: E.append(f"img without alt: {img.get('src')}")
        elif s.title and alt.lower() == (h1[0].get_text(strip=True).lower() if h1 else ""): W.append("hero alt text just repeats the H1")
        if not page_exists(img.get("src", "")): E.append(f"image not found: {img.get('src')}")

    # links
    internal = set()
    for a in main.find_all("a", href=True):
        href, txt = a["href"], a.get_text(strip=True)
        if WEAK_ANCHOR.match(txt): E.append(f"weak anchor text '{txt}' → {href}")
        if href.startswith("/"):
            internal.add(href.split("#")[0])
            if not page_exists(href): E.append(f"broken internal link {href}")
    rel = main.select(".la-cards a")
    if not 3 <= len(rel) <= 6: E.append(f"{len(rel)} related cards (need 3–6)")
    self_url = "/" + os.path.relpath(path, ROOT).replace(os.sep, "/")
    if any(a["href"] == self_url for a in rel): E.append("related cards link to the page itself")
    body_links = [a for a in main.find_all("a", href=True) if a["href"].startswith("/") and not a.find_parent(class_=re.compile("la-(related|more|crumb|back|authorbox|cta)"))]
    if len(body_links) < 2: W.append(f"only {len(body_links)} contextual internal links in the body (target 3+)")

    # content integrity
    text = main.get_text(" ")
    if MARKERS.search(str(main)): E.append(f"unresolved marker/placeholder: {MARKERS.search(str(main)).group(0)[:40]}")
    if FAKE_TEST.search(text): E.append(f"testing claim: '{FAKE_TEST.search(text).group(0)}' — only if it really happened")
    if HYPE.search(text): W.append(f"hype phrase: '{HYPE.search(text).group(0)}'")

    # head / SEO
    t = s.title.get_text(strip=True) if s.title else ""
    if not t: E.append("missing <title>")
    elif len(t) > 65: W.append(f"title {len(t)} chars (aim ≤ 60–65)")
    d = s.find("meta", attrs={"name": "description"})
    dl = len(d["content"]) if d else 0
    if not d: E.append("missing meta description")
    elif not 110 <= dl <= 165: W.append(f"meta description {dl} chars (aim 120–160)")
    if not s.find("link", rel="canonical"): E.append("missing canonical")
    if not s.find("link", href="/assets/learn.css"): E.append("learn.css not linked")

    # schema consistency
    types, faq_schema = [], []
    for sc in s.find_all("script", type="application/ld+json"):
        try:
            data = json.loads(sc.string)
        except Exception as ex:
            E.append(f"JSON-LD does not parse: {ex}"); continue
        for node in data.get("@graph", [data]):
            types.append(node.get("@type"))
            if node.get("@type") == "FAQPage":
                faq_schema = [q["name"].strip() for q in node.get("mainEntity", [])]
            if node.get("@type") in ("Article", "BlogPosting"):
                mod = node.get("dateModified")
                shown = [t_["datetime"] for t_ in main.select(".la-meta time")]
                if shown and mod and mod != max(shown): W.append(f"dateModified {mod} ≠ visible updated date {max(shown)}")
    for need in ("Article", "BreadcrumbList"):
        if need not in types and not (need == "Article" and "BlogPosting" in types): E.append(f"missing {need} schema")
    visible_faq = [h.get_text(strip=True) for h in main.select(".la-faq h3")]
    if visible_faq and "FAQPage" not in types: W.append("visible FAQ but no FAQPage schema")
    if faq_schema and faq_schema != visible_faq: E.append("FAQPage schema questions differ from visible FAQ")
    return E, W


def main_():
    args = sys.argv[1:]
    os.chdir(ROOT)
    if "--audit" in args:
        pages = sorted(glob.glob("en/learn/*.html") + glob.glob("*.html"))
        todo = []
        for p in pages:
            html = open(p, encoding="utf-8").read()
            if 'property="og:type" content="article"' in html and 'class="la"' not in html:
                todo.append(p)
        print(f"{len(todo)} article pages still on the legacy layout:")
        print("\n".join("  " + p for p in todo))
        return 0
    if "--all" in args or not args:
        args = [p for p in sorted(glob.glob("en/learn/*.html") + glob.glob("*.html")) if "/assets/learn.css" in open(p, encoding="utf-8").read()]
    bad = 0
    for p in args:
        E, W = lint(p)
        print(f"\n{p}: {len(E)} error(s), {len(W)} warning(s)")
        for e in E: print("  ERROR", e)
        for w in W: print("  WARN ", w)
        bad += bool(E)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main_())
