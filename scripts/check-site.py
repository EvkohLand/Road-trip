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
assert len(json.loads((root/'content/guides.json').read_text()))==10
assert 'fonts.googleapis.com' not in (dist/'style.css').read_text()
print(f'{len(pages)} HTML pages: local links, image alternatives, language and Amazon disclosure verified.')
