"""One-off: move en/learn/photochromic-vs-polarized-sunglasses.html onto the Learn template.
Replaces <main>, drops legacy article-body CSS (keeps chrome), links /assets/learn.css,
rebuilds FAQ + breadcrumb JSON-LD from the visible page. Run from repo root."""
import json, re
from bs4 import BeautifulSoup
P = 'en/learn/photochromic-vs-polarized-sunglasses.html'
s = open(P, encoding='utf-8').read()
m = open('tools/pilot/main.html', encoding='utf-8').read().strip()
s = re.sub(r'<main>.*?</main>', lambda _: m, s, count=1, flags=re.S)
a0 = 'main{max-width:760px'
a1 = '.listing .cat{font-size:11px;letter-spacing:.2em;color:var(--brass)}'
i, j = s.index(a0), s.index(a1) + len(a1)
keep = [l for l in s[i:j].split('\n') if l.startswith(('footer', '.stickycta'))]
s = s[:i] + '\n'.join(keep) + s[j:]
s = re.sub(r'\.author-box[^\n]*\n', '', s)
s = s.replace('&display=swap" rel="stylesheet">', '&display=swap" rel="stylesheet">\n<link rel="stylesheet" href="/assets/learn.css">', 1)
tag = '<script type="application/ld+json">'
a = s.index(tag) + len(tag); b = s.index('</script>', a)
d = json.loads(s[a:b]); g = d['@graph']
soup = BeautifulSoup(m, 'html.parser')
art = g[0]; url = art['mainEntityOfPage']['@id']
art['dateModified'] = '2026-09-23'
art['image'] = ['https://manhlongoptical.com/uploads-opt/learn-photochromic-s1.jpg']
art['about'] = [{"@type": "Thing", "name": "Photochromic lens"}, {"@type": "Thing", "name": "Polarized lens"}]
art['wordCount'] = len(soup.get_text(' ').split())
g[1]['mainEntity'] = [{"@type": "Question", "name": q.h3.get_text(strip=True), "acceptedAnswer": {"@type": "Answer", "text": q.p.get_text(' ', strip=True)}} for q in soup.select('.la-faq > div')]
g[2]['itemListElement'] = [
    {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://manhlongoptical.com/en/"},
    {"@type": "ListItem", "position": 2, "name": "Learn", "item": "https://manhlongoptical.com/en/learn/"},
    {"@type": "ListItem", "position": 3, "name": "Lenses", "item": "https://manhlongoptical.com/en/lenses.html"},
    {"@type": "ListItem", "position": 4, "name": "Photochromic vs polarized", "item": url}]
s = s[:a] + json.dumps(d, ensure_ascii=False) + s[b:]
s = s.replace('content="https://manhlongoptical.com/uploads-opt/cua-hang-cat-kinh-147-le-duan.jpg"', 'content="https://manhlongoptical.com/uploads-opt/learn-photochromic-s1.jpg"')
open(P, 'w', encoding='utf-8').write(s)
print('applied', P)
