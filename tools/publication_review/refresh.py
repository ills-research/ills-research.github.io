"""Regenerate the local DBLP review using the inclusive windows in content/publication_periods.json."""
import base64
import json
import re
import tempfile
import time
from urllib.error import HTTPError
import urllib.parse
import urllib.request
from collections import Counter, defaultdict
from datetime import date
from html import escape
from pathlib import Path

from references import enrich
from joint import enrich_joint

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ENDPOINT = 'https://sparql.dblp.org/sparql'
FRONT_MATTER = {
    'conf/coria/BechetCPFMN25',
    'journals/tmc/SarkerHKF26a',
    'journals/ni/AbramsBDEGGGKHK22a',
    'journals/tcs/AngelopoulosFNT24',
}
APPROVED_PROCEEDINGS = {
    'conf/taln/AissiRCLOSST25', 'conf/taln/DuboisPY25', 'conf/taln/AkaniFBG24',
    'conf/taln/KhodjaBBNL24', 'conf/taln/AntoineBDL24', 'conf/ictcs/GorlaJGPP23',
    'conf/taln/AntoineKRABD23',
}
TYPES = 'VALUES ?type { d:Article d:Inproceedings d:Informal } ?rec a ?type .'


def read_json(url):
    request = urllib.request.Request(url, headers={'User-Agent': 'ILLS publications review/1.0'})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(request, timeout=80) as response:
                return json.load(response)
        except OSError as exc:
            if attempt == 2 or (isinstance(exc, HTTPError) and exc.code in (400, 403, 404)):
                raise
            time.sleep(2 ** attempt)


def query(body):
    params = {'query': 'PREFIX d: <https://dblp.org/rdf/schema#>\n' + body, 'format': 'json'}
    data = read_json(ENDPOINT + '?' + urllib.parse.urlencode(params))
    bindings = data['results']['bindings']
    if data.get('meta', {}).get('result-size-total', len(bindings)) != len(bindings):
        raise ValueError('Incomplete DBLP query result')
    return [{key: obj['value'] for key, obj in row.items()} for row in bindings]


def snapshot_date():
    name = read_json(ENDPOINT + '?cmd=stats')['name-index']
    return date.fromisoformat(re.search(r'publication data .*?version (\d{4}-\d{2}-\d{2})', name)[1])


def build_roster(periods):
    directory = {p['name']: p['status'] for p in json.loads((ROOT / 'content/members.json').read_text())}
    people = []
    for period in periods:
        start, end = period['first_year'], period['last_year']
        if start > end:
            raise ValueError(f'Invalid publication window {start}–{end}')
        for name, pid in period['members'].items():
            if not re.fullmatch(r'[\w-]+/[\w-]+', pid):
                raise ValueError(f'Invalid DBLP identifier for {name}')
            people.append(dict(name=name, pid='https://dblp.org/pid/' + pid,
                               status=directory[name], start=start, end=end))
    if len({p['pid'] for p in people}) != len(people) or len({p['name'] for p in people}) != len(people):
        raise ValueError('Repeated DBLP profile or member')
    return sorted(people, key=lambda person: person['name'].casefold())


def category(record, key, venues):
    kind = record['type'].rsplit('#', 1)[1]
    if key in FRONT_MATTER:
        return None
    if record.get('stream') == 'https://dblp.org/streams/journals/corr':
        return 'preprint'
    if kind == 'Article' or key == 'journals/f1000research/KumarCQPGKGHK22':
        return 'journal'
    if kind == 'Inproceedings':
        series = key.rsplit('/', 1)[0]
        return 'proceedings' if series in venues or key in APPROVED_PROCEEDINGS else 'check'
    return None


def fetch(people):
    venues = set((HERE / 'international_venues.txt').read_text().splitlines())
    profiles = {p['pid']: i for i, p in enumerate(people)}
    groups = defaultdict(list)
    for p in people:
        groups[p['start'], p['end']].append(p['pid'])
    records, signatures, credits = {}, defaultdict(dict), defaultdict(set)
    for (start, end), pids in groups.items():
        years = ','.join(f'"{year}"' for year in range(start, end + 1))
        for offset in range(0, len(pids), 4):
            batch = pids[offset:offset + 4]
            values = ' '.join(f'<{pid}>' for pid in batch)
            match = f"""
              VALUES ?member {{ {values} }}
              ?rec d:authoredBy ?member ; d:yearOfPublication ?year .
              FILTER(STR(?year) IN ({years}))
              {TYPES}
            """
            metadata = query('SELECT DISTINCT ?rec ?member ?year ?type ?title ?venue ?parent ?doi ?stream ?n ?primary ?document ?pages ?issue ?journalVolume WHERE {' + match + """
                ?rec d:title ?title ; d:numberOfCreators ?n .
                OPTIONAL { ?rec d:publishedIn ?venue } OPTIONAL { ?rec d:doi ?doi }
                OPTIONAL { ?rec d:publishedInStream ?stream }
                OPTIONAL { ?rec d:primaryDocumentPage ?primary } OPTIONAL { ?rec d:documentPage ?document }
                OPTIONAL { ?rec d:pagination ?pages } OPTIONAL { ?rec d:publishedInJournalVolume ?journalVolume }
                OPTIONAL { ?rec d:publishedInJournalVolumeIssue ?issue }
                OPTIONAL { ?rec d:publishedAsPartOf/d:title ?parent }
            }""")
            for row in metadata:
                uri = row['rec']
                if not uri.startswith('https://dblp.org/rec/'):
                    raise ValueError(f'Unexpected record URI {uri}')
                key = uri.removeprefix('https://dblp.org/rec/')
                kind = category(row, key, venues)
                if kind is None:
                    continue
                year = int(row['year'])
                if not start <= year <= end or row['member'] not in batch:
                    raise ValueError(f'Unexpected membership or year on {key}')
                doi = row.get('doi', '')
                if doi and not doi.startswith(('https://doi.org/', 'http://doi.org/')):
                    raise ValueError(f'Unexpected DOI {doi}')
                paper = records.setdefault(key, dict(key=key, category=kind, year=year, title=row['title'],
                                    venue=row.get('venue',''), doi=doi, volume=row.get('parent',''), n=int(row['n']),
                                    pages=row.get('pages', ''), journalVolume=row.get('journalVolume', ''),
                                    issue=row.get('issue', ''), primary=row.get('primary', ''), documents=[]))
                if row.get('document') and row['document'] not in paper['documents']:
                    paper['documents'].append(row['document'])
                credits[key].add(profiles[row['member']])
            if metadata:
                authors = query('SELECT DISTINCT ?rec ?position ?name WHERE { { SELECT DISTINCT ?rec WHERE {' + match + """
                    } } ?rec d:hasSignature ?signature .
                    ?signature a d:AuthorSignature ; d:signatureOrdinal ?position ; d:signatureDblpName ?name .
                }""")
                for row in authors:
                    key = row['rec'].removeprefix('https://dblp.org/rec/')
                    signatures[key][int(row['position'])] = re.sub(r' [0-9]{4}$', '', row['name'])
    for key, paper in records.items():
        authors = signatures[key]
        positions = sorted(authors)
        if positions != list(range(1, paper.pop('n') + 1)):
            raise ValueError(f'Incomplete author list for {key}')
        paper['authors'] = [authors[i] for i in positions]
        paper['members'] = sorted(credits[key])
    return sorted(records.values(), key=lambda p: (-p['year'], p['title'].casefold(), p['key']))


def render(periods, people, papers, as_of):
    start = min(p['start'] for p in people)
    end = max(p['end'] for p in people)
    counts = Counter(p['category'] for p in papers)
    windows = []
    for group in periods:
        first, last = group['first_year'], group['last_year']
        label = str(first) if first == last else f'{first}–{last}'
        names = ', '.join(escape(name) for name in group['members'])
        windows.append(f'<tr><th scope="row">{label}</th><td>{names}</td></tr>')
    check_venues = sorted({p['key'].split('/')[1].upper() for p in papers if p['category'] == 'check'})
    replacements = {
        '__PERIOD__': f'{start}–{end}',
        '__AS_OF__': as_of.strftime('%d %B %Y').lstrip('0'),
        '__WINDOWS__': '\n'.join(windows),
        '__YEARS__': ''.join(f'<option>{y}</option>' for y in range(end, start - 1, -1)),
        '__MEMBERS__': str(len(people)),
        '__TOTAL__': format(len(papers) - counts['check'], ','),
        '__CHECK__': str(counts['check']),
        '__CHECK_VENUES__': escape(', '.join(check_venues)),
        '__PREPRINTS__': str(counts['preprint']), '__JOURNALS__': str(counts['journal']),
        '__PROCEEDINGS__': str(counts['proceedings']),
        '__LOGO__': base64.b64encode((ROOT / 'site/assets/brand/logo-color.png').read_bytes()).decode(),
        '__PAYLOAD__': json.dumps(dict(people=people, papers=papers), ensure_ascii=False,
                                  separators=(',', ':')).replace('<', r'\u003c'),
    }
    page = (HERE / 'review.html').read_text()
    return re.sub(r'__[A-Z_]+__', lambda match: replacements[match[0]], page)


def write_atomic(target, text):
    target.parent.mkdir(exist_ok=True, parents=True)
    with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=target.parent, delete=False) as draft:
        draft.write(text)
    Path(draft.name).replace(target)


def main():
    periods = json.loads((ROOT / 'content/publication_periods.json').read_text())
    people = build_roster(periods)
    as_of = snapshot_date()
    papers = fetch(people)
    if not papers or snapshot_date() != as_of:
        raise RuntimeError('No records returned or the DBLP snapshot changed during retrieval. Retry the review.')
    enrich(papers, read_json)
    public = [p for p in papers if p['category'] != 'check']
    previous_path = ROOT / 'content/publication_catalogue.json'
    previous = json.loads(previous_path.read_text())['papers'] if previous_path.exists() else []
    enrich_joint(public, read_json)
    # Missing affiliation metadata (or a title-search quota) is not a retraction.
    # Retain previously verified sources only for unchanged bibliographic identities.
    previous_evidence = {(p['key'], p['title'], tuple(p['authors'])): p['joint_source'] for p in previous
                         if p.get('joint_source', '').startswith('https://')}
    for p in public:
        evidence = previous_evidence.get((p['key'], p['title'], tuple(p['authors'])))
        if evidence:
            p.setdefault('joint_source', evidence)
    page = render(periods, people, papers, as_of)
    target = ROOT / 'preview/dblp/index.html'
    write_atomic(target, page)
    catalogue = dict(people=people, papers=[p for p in papers if p['category'] != 'check'], as_of=as_of.isoformat())
    write_atomic(ROOT / 'content/publication_catalogue.json',
                 json.dumps(catalogue, ensure_ascii=False, separators=(',', ':')) + '\n')
    print(f'{target} · DBLP {as_of} · {len(people)} members · {dict(Counter(p["category"] for p in papers))}')


if __name__ == '__main__':
    main()
