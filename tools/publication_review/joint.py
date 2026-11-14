"""Identify works with distinct France- and Canada-affiliated coauthors.

Use the lab's reviewed references and publication-level authorship metadata.
Do not infer affiliations from nationality, venue or current directory entries.
"""
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path
import re
import unicodedata
from urllib.error import HTTPError
from urllib.parse import urlencode, quote

REPORTED = Path(__file__).resolve().parents[2] / 'content' / 'joint_references.json'
API = 'https://api.openalex.org/works'
FIELDS = 'id,doi,display_name,authorships'


def norm(value):
    return ''.join(c for c in unicodedata.normalize('NFKD', value.casefold()) if c.isalnum())


def paper_doi(p):
    m = re.search(r'^  doi = \{([^}]+)\}', p['bibtex'], re.M)
    return m[1].lower() if m else ''


def author_id(a):
    return a.get('author', {}).get('id') or norm(a.get('raw_author_name') or a['author']['display_name'])


def paper_countries(a):
    codes = {i.get('country_code') for i in a.get('institutions', [])} | set(a.get('countries', []))
    # Some publisher affiliations explicitly end in a country even when the
    # registry has not assigned a country code (e.g. "ETS Montréal, Canada").
    for raw in a.get('raw_affiliation_strings', []):
        m = re.search(r'(?:^|[,;])\s*(france|canada)\s*[.;]?\s*$', raw, re.I)
        if m:
            codes.add({'france': 'FR', 'canada': 'CA'}[m[1].lower()])
    return codes


def has_joint_byline(work):
    groups = {'FR': set(), 'CA': set()}
    for a in work.get('authorships', []):
        who = author_id(a)
        if not who:
            continue
        for country in paper_countries(a):
            if country in groups:
                groups[country].add(who)
    return any(f != c for f in groups['FR'] for c in groups['CA'])


def by_title(p, work):
    # A title search alone, especially for short titles, is not an identity match.
    if norm(work.get('display_name') or '') != norm(p['title']):
        return False
    authors = work.get('authorships', [])
    if not authors or not p['authors']:
        return False
    def family(name):
        return norm(name.split()[-1]) if name.strip() else ''
    return any(family(a.get('raw_author_name') or '') == family(p['authors'][0]) or
               family(a['author'].get('display_name') or '') == family(p['authors'][0])
               for a in authors[:1])


def hal_evidence(papers, read_json):
    # HAL exposes a specific author-to-structure relation. A paper-level
    # list of two countries alone could refer to one dual-appointed author.
    index = defaultdict(list)
    for p in papers:
        index[norm(p['title'])].append(p)
    records = {}
    api = 'https://api.archives-ouvertes.fr/'
    def query(endpoint, query, fields, rows, filters=()):
        params = [('q', query), ('fl', fields), ('wt', 'json'), ('rows', rows)]
        params += [('fq', f) for f in filters]
        output = []
        while True:
            data = read_json(api + endpoint + '?' + urlencode(params + [('start', len(output))]))['response']
            output.extend(data['docs'])
            if len(output) >= data['numFound']:
                return output
            if not data['docs']:
                raise ValueError('Incomplete HAL response')
    def batches(items, size):
        for i in range(0, len(items), size):
            yield items[i:i+size]
    # Titles are paper identifiers here; never look up a researcher's current country.
    titles = sorted({re.sub(r'[^\w ]', ' ', p['title']).strip() for p in papers})
    for batch in batches(titles, 18):
        q = 'title_t:(' + ' OR '.join('"' + title + '"' for title in batch) + ')'
        fields = 'halId_s,title_s,doiId_s,arxivId_s,authFullName_s,authIdHasStructure_fs'
        for w in query('search/', q, fields, 100, ('structCountry_s:fr', 'structCountry_s:ca')):
            records[w['halId_s']] = w
    def pairs(w):
        for relation in w.get('authIdHasStructure_fs', []):
            left, sep, right = relation.partition('_JoinSep_')
            if sep:
                author = left.partition('_FacetSep_')[2]
                org = right.partition('_FacetSep_')[0]
                if author and org.isdecimal():
                    yield norm(author), org
    orgs = sorted({org for w in records.values() for _, org in pairs(w)})
    countries = {}
    for batch in batches(orgs, 100):
        for entry in query('ref/structure/', 'docid:(' + ' OR '.join(batch) + ')', 'docid,country_s', 100):
            countries[str(entry['docid'])] = entry.get('country_s')
    for w in records.values():
        affiliations = [(a, countries.get(i)) for a,i in pairs(w)]
        if not any(f != c for f,fc in affiliations if fc == 'fr'
                   for c,cc in affiliations if cc == 'ca'):
            continue
        for title in w['title_s']:
            for p in index[norm(title)]:
                doi = paper_doi(p)
                source_names = {norm(n) for n in w.get('authFullName_s', [])}
                if ((doi and doi == str(w.get('doiId_s', '')).lower())
                    or (p.get('arxiv') and p['arxiv'].endswith('/' + str(w.get('arxivId_s', '--'))))
                    or (norm(p['authors'][0]) in source_names and
                        len(source_names & {norm(n) for n in p['authors']}) >= 2)):
                    p.setdefault('joint_source', 'https://hal.science/' + w['halId_s'])


def enrich_joint(papers, read_json):
    reported = json.loads(REPORTED.read_text(encoding='utf-8'))
    dois = defaultdict(list)
    for p in papers:
        p.pop('joint_source', None)
        if p['key'] in reported:
            p['joint_source'] = reported[p['key']]
        doi = paper_doi(p)
        if doi:
            dois[doi].append(p)
    hal_evidence(papers, read_json)
    ids = sorted(dois)
    found = set()
    for i in range(0, len(ids), 40):
        batch = ids[i:i+40]
        q = urlencode({'filter': 'doi:' + '|'.join(batch), 'select': FIELDS, 'per_page': 100})
        result = read_json(API + '?' + q)
        if result['meta']['count'] > len(result['results']):
            raise ValueError('Incomplete OpenAlex DOI response')
        for w in result['results']:
            doi = (w.get('doi') or '').lower().removeprefix('https://doi.org/')
            candidates = list(dois.get(doi, []))
            if has_joint_byline(w):
                candidates.extend(p for key in batch if key != doi for p in dois[key] if by_title(p, w))
                for p in candidates:
                    p['joint_source'] = w['id']
            found.update(p['key'] for p in candidates)
    # OpenAlex often merges an arXiv DOI into the publisher record. A bulk
    # DOI lookup returns only the canonical DOI; exact singleton lookups also
    # resolve aliases. Require matching authors when using another edition.
    pending = defaultdict(list)
    for p in papers:
        if p.get('joint_source'):
            continue
        doi = paper_doi(p)
        if doi and p['key'] not in found:
            pending[doi].append(p)
        if p.get('arxiv'):
            pending['10.48550/arxiv.' + p['arxiv'].rsplit('/', 1)[1].lower()].append(p)

    def lookup(doi):
        try:
            return doi, read_json(API + '/doi:' + quote(doi, safe='/') + '?' + urlencode({'select': FIELDS}))
        except HTTPError as exc:
            if exc.code == 404:
                return doi, None
            raise

    with ThreadPoolExecutor(max_workers=3) as pool:
        remaining = sorted(pending)
        for off in range(0, len(remaining), 12):
            try:
                for doi, w in pool.map(lookup, remaining[off:off + 12]):
                    if w and has_joint_byline(w):
                        for p in pending[doi]:
                            if by_title(p, w) or ((w.get('doi') or '').lower().endswith('/' + doi) and doi == paper_doi(p)):
                                p['joint_source'] = w['id']
            except HTTPError as exc:
                if exc.code != 429:
                    raise
                print('OpenAlex alias lookup limit reached; keeping verified references.')
                break
    # Exact title and first author fallback for publications without an indexed DOI.
    for p in papers:
        if p.get('joint_source') or p['key'] in found:
            continue
        q = urlencode({'filter': 'title.search:' + ' '.join(re.findall(r'[^\W_]+', p['title'])),
                       'select': FIELDS, 'per_page': 5})
        try:
            results = read_json(API + '?' + q)['results']
        except HTTPError as exc:
            if exc.code != 429:
                raise
            # This optional title fallback may exhaust the anonymous search quota.
            # The full DOI and HAL passes above have already completed.
            print('OpenAlex title-search limit reached; using DOI, HAL and lab evidence.')
            break
        for w in results:
            if by_title(p, w) and has_joint_byline(w):
                p['joint_source'] = w['id']
                break
    # Only transfer evidence between editions when both the complete author list
    # and an edition identifier (or complete title) match.
    editions = defaultdict(list)
    for p in papers:
        authors = tuple(sorted(norm(a) for a in p['authors']))
        for token in (p.get('arxiv'), p.get('paper'), norm(p['title'])):
            if token:
                editions[(token, authors)].append(p)
    for group in editions.values():
        source = next((p['joint_source'] for p in group if p.get('joint_source')), None)
        if source:
            for p in group:
                p.setdefault('joint_source', source)
