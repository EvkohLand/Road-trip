from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import json
root=Path(__file__).resolve().parents[1]
dist=root/'dist'
mention='En tant que Partenaire Amazon, je réalise un bénéfice sur les achats remplissant les conditions requises.'
class Check(HTMLParser):
    def __init__(self,path):
        super().__init__(); self.path=path
    def handle_starttag(self,tag,attrs):
        attrs=dict(attrs)
        for key in ('href','src'):
            v=attrs.get(key,''); parsed=urlsplit(v)
            if v and not parsed.scheme and not parsed.netloc and parsed.path:
                target=(self.path.parent/unquote(parsed.path)).resolve()
                assert target.is_relative_to(dist.resolve()), (self.path,v)
                if target.is_dir(): target=target/'index.html'
                assert target.is_file(), (self.path,v)
        if tag=='img': assert 'alt' in attrs, self.path
pages=list(dist.rglob('*.html'))
for p in pages:
    html=p.read_text(); Check(p).feed(html)
    assert mention in html, p
    assert '<html lang="fr">' in html, p
    assert 'fonts.googleapis.com' not in html, p
    # SEO / social preview contract: every page must keep these (see scripts/build-pages.py).
    import re
    SITE='https://evkohland.github.io/Road-trip/'
    head=html[:html.index('</head>')]
    assert html.count('<h1')==1 or p.name=='index.html', (p,'one h1')
    assert re.search(r'<title>[^<]{10,80}</title>',head), (p,'title')
    d=re.search(r'<meta name="description" content="([^"]{50,160})">',head); assert d, (p,'description 50-160')
    canon=re.search(r'<link rel="canonical" href="([^"]+)">',head); assert canon and canon.group(1).startswith(SITE), (p,'canonical')
    for prop in ('og:title','og:description','og:url','og:image','og:type','og:locale','twitter:card'):
        assert f'"{prop}"' in head, (p,prop)
    img=re.search(r'property="og:image" content="([^"]+)"',head).group(1)
    assert (dist/img.removeprefix(SITE)).is_file(), (p,'og:image file',img)
    for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>',head,re.S): json.loads(block)
    if p.name!='404.html': assert 'noindex' not in head, (p,'indexable')
sitemap=(dist/'sitemap.xml').read_text()
for p in pages:
    rel=p.relative_to(dist).as_posix()
    if rel=='404.html': continue
    assert f'<loc>https://evkohland.github.io/Road-trip/{"" if rel=="index.html" else rel}</loc>' in sitemap, (rel,'missing from sitemap')
assert len(json.loads((root/'content/guides.json').read_text()))==11
assert 'fonts.googleapis.com' not in (dist/'style.css').read_text()
print(f'{len(pages)} HTML pages: local links, image alternatives, language, Amazon disclosure, SEO tags, structured data and sitemap verified.')
