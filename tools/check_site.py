"""Check both language editions, all local assets and all HTML fragment links."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
root=Path(__file__).resolve().parents[1]/'site'
private_assets = {'scientific_project_ills.pdf', 'scientific-project-cover.webp'}
for asset in root.rglob('*'):
    if asset.name.casefold() in private_assets:
        raise ValueError(f'Private scientific project asset in website: {asset.relative_to(root)}')
class Page(HTMLParser):
    def __init__(self):
        self.ids=set();self.links=[];self.h1=0;self.alternates=[]; self.lang=None;super().__init__()
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'id' in a:
            assert a['id'] not in self.ids, f'duplicate id {a["id"]}'
            self.ids.add(a['id'])
        if tag=='img':assert 'alt' in a,'missing image alt'
        if tag=='h1':self.h1+=1
        if tag=='html':self.lang=a.get('lang')
        if tag=='link' and a.get('rel')=='alternate':self.alternates.append(a['href'])
        self.links += [a[key] for key in ('href','src') if key in a]
pages={}
for path in root.rglob('*.html'):
    p=Page();p.feed(path.read_text());pages[path]=p
    assert p.h1==1 and p.lang in ('en','fr') and len(p.alternates)==1,path
assert {p.name for p in pages if p.parent==root}=={p.name for p in pages if p.parent==root/'fr'}
checks=0
for path,p in pages.items():
    assert pages[(path.parent/p.alternates[0]).resolve()].lang!=p.lang
    for link in p.links:
        u=urlsplit(link)
        if u.scheme or u.netloc:continue
        target=(path.parent/unquote(u.path)).resolve() if u.path else path
        assert target.is_relative_to(root) and target.is_file(),(path,link)
        if u.fragment and target.suffix=='.html':assert u.fragment in pages[target].ids,(path,link)
        checks+=1
print(f'{len(pages)} pages: {checks} local references, reciprocal language editions and section links verified.')
