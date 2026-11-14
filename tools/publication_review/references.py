"""Find edition-specific reading links and build a citation for each DBLP record."""
import json
import re
import time
import unicodedata
import urllib.parse
import urllib.request
from collections import defaultdict
from urllib.error import HTTPError
from xml.etree import ElementTree

ARXIV_ID = r'(?:[a-z-]+(?:\.[a-z-]+)?/\d{7}|\d{4}\.\d{4,5})'
# Published editions confirmed directly with the venue outside the member's publication window.
KNOWN_EDITIONS = {
    'conf/nips/VeilleuxBPA21':
        'https://proceedings.neurips.cc/paper_files/paper/2021/hash/4d7a968bb636e25818ff2a3941db08c1-Abstract.html',
}
ARXIV_HOSTS = {'arxiv.org', 'www.arxiv.org', 'export.arxiv.org'}


def batches(values, size):
    values = sorted(set(values))
    for start in range(0, len(values), size):
        yield values[start:start + size]


def doi_id(value):
    return re.sub(r'^https?://(?:dx\.)?doi\.org/', '', value, flags=re.I).lower()


def arxiv_id(value):
    url = urllib.parse.urlsplit(value)
    if url.hostname in ARXIV_HOSTS:
        match = re.fullmatch(r'/(?:abs|pdf|html)/(' + ARXIV_ID + r')(?:v\d+)?(?:\.pdf)?/?', url.path, re.I)
    else:
        match = re.fullmatch(r'10\.48550/arxiv\.(' + ARXIV_ID + r')(?:v\d+)?', doi_id(value), re.I)
    return match[1] if match else ''


def publication_url(value):
    url = urllib.parse.urlsplit(value)
    if url.scheme not in ('http', 'https') or not url.hostname or not url.path.strip('/'):
        return ''
    if any(url.hostname == host or url.hostname.endswith('.' + host)
           for host in ('doi.org', 'dblp.org', 'dblp.uni-trier.de', 'arxiv.org')):
        return ''
    if url.hostname == 'papers.nips.cc':
        return url._replace(scheme='https').geturl()
    return value


def get_json(url, params, read_json):
    return read_json(url + '?' + urllib.parse.urlencode(params))


def publisher_links(dois, read_json):
    """Crossref supplies the publisher's registered resource, including case-sensitive paths."""
    # The DOI registry delegates this item back to another resolver. Its society
    # library supplies the actual journal landing page.
    links = {'10.1111/cgf.70533': 'https://diglib.eg.org/items/55363661-e76b-4d9d-8bc0-d8835ccec2e7'}
    for batch in batches(dois, 32):
        data = get_json('https://api.crossref.org/works', {
            'filter': ','.join('doi:' + identifier for identifier in batch),
            'select': 'DOI,resource', 'rows': len(batch),
        }, read_json)
        for item in data['message']['items']:
            url = publication_url(item.get('resource', {}).get('primary', {}).get('URL', ''))
            if url:
                links[doi_id(item['DOI'])] = url
    for identifier in sorted(set(dois) - links.keys()):
        # Some DOI registrars only expose the landing page in the Handle record.
        try:
            data = read_json('https://doi.org/api/handles/' + urllib.parse.quote(identifier, safe='/'))
        except HTTPError as error:
            if error.code == 404:
                continue
            raise
        for value in data.get('values', []):
            if value['type'] == 'URL':
                url = publication_url(value['data']['value'])
                if url:
                    links[identifier] = url
                    break
    return links


def archived_editions(dois, read_json):
    """Look for arXiv repository locations indexed for the published DOI."""
    result = {}
    for batch in batches(dois, 40):
        data = get_json('https://api.openalex.org/works', {
            'filter': 'doi:' + '|'.join(batch), 'select': 'doi,locations', 'per_page': len(batch),
        }, read_json)
        for work in data['results']:
            ids = {arxiv_id(location.get(field) or '') for location in work['locations']
                   for field in ('landing_page_url', 'pdf_url')} - {''}
            if len(ids) == 1:
                result[doi_id(work['doi'])] = ids.pop()
    return result


def deposited_dois(identifiers):
    """Read the published DOI reported by arXiv itself, when supplied by its authors."""
    result = {}
    for batch in batches(identifiers, 60):
        params = urllib.parse.urlencode({'id_list': ','.join(batch), 'max_results': len(batch)})
        request = urllib.request.Request('https://export.arxiv.org/api/query?' + params,
                                         headers={'User-Agent': 'ILLS publications review/1.0'})
        for attempt in range(3):
            try:
                with urllib.request.urlopen(request, timeout=60) as response:
                    feed = ElementTree.parse(response)
                break
            except OSError:
                if attempt == 2:
                    raise
                time.sleep(5 * (attempt + 1))
        for entry in feed.findall('{http://www.w3.org/2005/Atom}entry'):
            identifier = arxiv_id(entry.findtext('{http://www.w3.org/2005/Atom}id', ''))
            doi = doi_id(entry.findtext('{http://arxiv.org/schemas/atom}doi', '').strip())
            if identifier in batch and re.fullmatch(r'10\.\d{4,9}/\S+', doi) and not arxiv_id(doi):
                result[identifier] = doi
        time.sleep(3.1)
    return result


def corpus_editions(papers):
    """Resolve edition identifiers indexed together by Semantic Scholar."""
    work_ids = {}
    for p in papers:
        if p['category'] == 'preprint' and arxiv_id(p['doi']):
            work_ids[p['key']] = 'ARXIV:' + arxiv_id(p['doi'])
        elif p['doi']:
            work_ids[p['key']] = 'DOI:' + doi_id(p['doi'])
        elif urllib.parse.urlsplit(p['primary']).hostname == 'aclanthology.org':
            work_ids[p['key']] = 'ACL:' + urllib.parse.urlsplit(p['primary']).path.strip('/')
    result = {}
    for keys in batches(work_ids, 100):
        request = urllib.request.Request(
            'https://api.semanticscholar.org/graph/v1/paper/batch?fields=externalIds',
            data=json.dumps({'ids': [work_ids[key] for key in keys]}).encode(),
            headers={'User-Agent': 'ILLS publications review/1.0', 'Content-Type': 'application/json'})
        for attempt in range(4):
            try:
                with urllib.request.urlopen(request, timeout=60) as response:
                    works = json.load(response)
                break
            except HTTPError as error:
                if attempt == 3 or error.code not in (429, 500, 502, 503, 504):
                    raise
                time.sleep(5 * (attempt + 1))
        if len(works) != len(keys):
            raise ValueError('Incomplete Semantic Scholar batch')
        for key, work in zip(keys, works):
            if work:
                result[key] = work.get('externalIds') or {}
        time.sleep(1)
    return result


def normalized(value):
    return ''.join(c for c in unicodedata.normalize('NFKD', value.casefold()) if c.isalnum())


def citation(paper):
    category = paper['category']
    kind = {'journal': 'article', 'preprint': 'misc'}.get(category, 'inproceedings')
    def tex(text):
        # Preserve DBLP's inline TeX math. Protect prose characters that TeX interprets.
        return ''.join(piece if piece.startswith('$') and piece.endswith('$') else
                       re.sub(r'([&%#_{}])', r'\\\1', piece)
                       for piece in re.split(r'(\$[^$]+\$)', text))
    title = paper['title'].removesuffix('.')
    fields = {'author': tex(' and '.join(paper['authors'])), 'title': '{' + tex(title) + '}',
              'year': str(paper['year'])}
    if kind == 'article':
        fields.update(journal=tex(paper['venue']), volume=paper['journalVolume'], number=paper['issue'])
    elif kind == 'inproceedings':
        fields['booktitle'] = tex((paper['volume'] or paper['venue']).removesuffix('.'))
    if paper['pages'] and kind != 'misc':
        fields['pages'] = re.sub(r'(?<=\d)-(?=\d)', '--', paper['pages'])
    if paper['doi']:
        fields['doi'] = paper['doi'].split('doi.org/', 1)[-1]
    if paper['arxiv']:
        fields.update(eprint=arxiv_id(paper['arxiv']), archivePrefix='arXiv')
    fields['url'] = (paper['arxiv'] if kind == 'misc' else paper['paper']) or paper['arxiv']
    lines = [f'  {key} = {{{value}}}' for key, value in fields.items() if value]
    return '@' + kind + '{DBLP:' + paper['key'] + ',\n' + ',\n'.join(lines) + '\n}'


def enrich(papers, read_json):
    published = [p for p in papers if p['category'] != 'preprint']
    for p in papers:
        editions = [p['doi'], p['primary'], *sorted(p['documents'])]
        p['arxiv'] = next((identifier for url in editions if (identifier := arxiv_id(url))), '')
        p['paper'] = next((dest for url in editions if (dest := publication_url(url))), '')
    declared = deposited_dois(p['arxiv'] for p in papers if p['category'] == 'preprint' and p['arxiv'])
    corpus = corpus_editions(papers)
    for p in papers:
        ids = corpus.get(p['key'], {})
        identifier = ids.get('ArXiv') or ''
        if p['category'] != 'preprint':
            if re.fullmatch(ARXIV_ID, identifier):
                p['arxiv'] = p['arxiv'] or identifier
            continue
        doi = doi_id(ids.get('DOI') or '')
        if re.fullmatch(r'10\.\d{4,9}/\S+', doi) and not arxiv_id(doi):
            declared.setdefault(p['arxiv'], doi)
    indexed = {doi_id(p['doi']) for p in published if p['doi']}
    destinations = publisher_links(indexed | set(declared.values()), read_json)
    archived = archived_editions(indexed, read_json)
    by_doi = defaultdict(set)
    for identifier, doi in declared.items():
        by_doi[doi].add(identifier)
    for p in published:
        doi = doi_id(p['doi'])
        p['paper'] = p['paper'] or destinations.get(doi, '')
        ids = by_doi[doi]
        p['arxiv'] = p['arxiv'] or (next(iter(ids)) if len(ids) == 1 else archived.get(doi, ''))
    by_key = {p['key']: p for p in published}
    for p in papers:
        if p['category'] == 'preprint':
            edition_key = corpus.get(p['key'], {}).get('DBLP')
            p['paper'] = KNOWN_EDITIONS.get(edition_key, p['paper'])
            paired = by_key.get(edition_key)
            if paired and paired['arxiv'] in ('', p['arxiv']):
                paired['arxiv'] = p['arxiv']
                p['paper'] = paired['paper']
    by_title = defaultdict(list)
    for p in papers:
        by_title[normalized(p['title'])].append(p)
    for p in papers:
        is_preprint = p['category'] == 'preprint'
        # Match reciprocal editions by complete title and author byline; never by title alone.
        names = {normalized(a) for a in p['authors']}
        matches = [q for q in by_title[normalized(p['title'])]
                   if (q['category'] == 'preprint') != is_preprint
                   and names == {normalized(a) for a in q['authors']}]
        if is_preprint:
            p['paper'] = p['paper'] or destinations.get(declared.get(p['arxiv']), '')
        field = 'paper' if is_preprint else 'arxiv'
        values = {q[field] for q in matches if q[field]}
        if not p[field] and len(values) == 1:
            p[field] = values.pop()
    for p in papers:
        if p['arxiv']:
            p['arxiv'] = 'https://arxiv.org/abs/' + p['arxiv']
        p['bibtex'] = citation(p)
        for key in ('primary', 'documents', 'journalVolume', 'issue', 'pages', 'doi'):
            del p[key]
