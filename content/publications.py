"""Render the catalogue and its France–Canada coauthorship bibliography."""

from collections import Counter
from functools import lru_cache
from html import escape
import json
from pathlib import Path
from datetime import date
from urllib.parse import urlencode
import unicodedata
import re


@lru_cache(maxsize=1)
def catalogue():
    return json.loads(Path(__file__).with_name('publication_catalogue.json').read_text(encoding='utf-8'))


@lru_cache(maxsize=1)
def member_ids():
    return {p['name']: p['pid'].removeprefix('https://dblp.org/pid/') for p in catalogue()['people']}


def member_link(name, parent=''):
    pid = member_ids().get(name)
    return parent + 'research.html?' + urlencode({'member': pid}) + '#publications' if pid else ''


PUBLICATION_AREAS = (
    ('vision', 'Vision & visual computing', 'Vision et informatique visuelle',
     'Image understanding, visual recognition, video, graphics and 3D perception.',
     'Compréhension des images, reconnaissance visuelle, vidéo, graphisme et perception 3D.'),
    ('language', 'Language & speech', 'Langage et parole',
     'Natural language, text, speech and audio processing.',
     'Traitement du langage naturel, du texte, de la parole et de l’audio.'),
    ('core-ml', 'Core machine learning & general AI', 'Apprentissage automatique et IA générale',
     'Learning theory, optimization, statistics, reinforcement learning and general AI.',
     'Théorie de l’apprentissage, optimisation, statistiques, apprentissage par renforcement et IA générale.'),
    ('medical', 'Medical & health AI', 'IA médicale et santé',
     'Medical imaging, clinical AI, health data and biomedical applications.',
     'Imagerie médicale, IA clinique, données de santé et applications biomédicales.'),
    ('networks', 'Communications, networks & IoT', 'Communications, réseaux et objets connectés',
     'Wireless communications, network management, IoT and connected systems.',
     'Communications sans fil, gestion des réseaux, objets connectés et systèmes interconnectés.'),
    ('engineering', 'AI for engineering systems', 'IA pour les systèmes d’ingénierie',
     'Control, smart grids, energy, transportation and industrial systems.',
     'Commande, réseaux électriques intelligents, énergie, transport et systèmes industriels.'),
    ('responsible', 'Responsible, private & secure AI', 'IA responsable, privée et sécurisée',
     'Fairness, privacy, security, accountability, robustness and trustworthy AI.',
     'Équité, vie privée, sécurité, responsabilité, robustesse et fiabilité de l’IA.'),
    ('human', 'Human-centered AI & interaction', 'IA centrée sur l’humain et interaction',
     'Human-computer interaction, affective computing, haptics and robotics.',
     'Interaction humain-machine, informatique affective, haptique et robotique.'),
    ('other', 'Other & cross-disciplinary AI', 'Autres travaux et IA interdisciplinaire',
     'Work whose title and venue do not indicate a clear primary area, including interdisciplinary applications.',
     'Travaux dont le titre et la revue ne révèlent pas un axe principal clair, y compris les applications interdisciplinaires.'),
)


def _normalized(value):
    normalized = unicodedata.normalize('NFKD', (value or '').casefold())
    return ''.join(c for c in normalized if c.isalnum())


def _authors_key(paper):
    return tuple(_normalized(author) for author in paper.get('authors', ()))


def unique_works(papers):
    """Collapse preprint/published copies and duplicate venue records for overview counts."""
    parent = list(range(len(papers)))

    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    def union(a, b):
        a, b = find(a), find(b)
        if a != b:
            parent[b] = a

    seen = {}
    for i, paper in enumerate(papers):
        title_key = _normalized(paper.get('title'))
        arxiv = re.search(r'arxiv\.org/(?:abs|pdf)/([^?#]+)', paper.get('arxiv') or '', re.I)
        arxiv_key = re.sub(r'v\d+$', '', arxiv.group(1).removesuffix('.pdf')) if arxiv else ''
        paper_key = _normalized(paper.get('paper')) if paper.get('paper') else ''
        # Title plus ordered author list is stable across CoRR and published entries; URLs
        # also connect records when DBLP shortens or changes their displayed titles.
        identities = []
        if arxiv_key:
            identities.append(('arxiv', arxiv_key))
        if paper_key:
            identities.append(('paper', paper_key))
        if title_key:
            identities.append(('title-authors', title_key, _authors_key(paper)))
        for identity in identities:
            if identity in seen:
                union(i, seen[identity])
            else:
                seen[identity] = i

    groups = {}
    for i, paper in enumerate(papers):
        groups.setdefault(find(i), []).append(paper)

    unique = []
    for records in groups.values():
        # Prefer a journal or proceedings citation so an arXiv duplicate counts as a preprint-only
        # work only when the catalogue has no corresponding published edition.
        chosen = max(records, key=lambda p: (
            p.get('category') != 'preprint',
            p.get('category') == 'journal',
            bool(p.get('paper')),
            bool(p.get('arxiv')),
            'poster' not in (p.get('venue') or '').casefold(),
            int(p.get('year') or 0),
        ))
        item = dict(chosen)
        item['members'] = sorted({member for record in records for member in record.get('members', ())})
        if not item.get('arxiv'):
            item['arxiv'] = next((record.get('arxiv') for record in records if record.get('arxiv')), '')
        if not item.get('joint_source'):
            item['joint_source'] = next((record.get('joint_source') for record in records if record.get('joint_source')), '')
        unique.append(item)
    return unique


def publication_area(paper):
    """Assign one primary area using the venue and title available in the DBLP catalogue."""
    title = (paper.get('title') or '').casefold()
    venue = ((paper.get('venue') or '') + ' ' + (paper.get('volume') or '')).casefold()
    text = f'{title} {venue}'
    has = lambda pattern: re.search(pattern, text, re.I) is not None

    # TMLR is grouped under the lab's core machine learning area for the overview,
    # even when an individual paper focuses on an application such as vision or fairness.
    if has(r'\btmlr\b|\btrans\.\s*mach\.\s*learn\.\s*res\.|\btransactions? on machine learning research\b'):
        return 'core-ml'

    # Specific application domains take priority over broad methods venues such as AAAI.
    if has(r'\b(miccai|midl|ipmi|isbi|medical image|medical imaging|biomedical|health informatics|trans\. medical imaging|j\. biomed)\b') or has(
        r'\b(medical|clinical|healthcare|health care|digital health|breast cancer|radiolog|patholog|mri|computed tomography|patient data|histopathology|mammograph|echocardi|retina|diagnos|brain model)'):
        return 'medical'
    if has(r'\b(acl|emnlp|eacl|naacl|coling|taln|interspeech|eusipco|asru|icassp)\b') or has(
        r'\b(natural language|language[- ]models?|large language|\bllms?\b|text|speech|audio|acoustic|spoken language|machine translation|dialogue|sentiment analysis|linguistic|speaker recognition|voice conversion|sound event|sound effects|sfx generation|grammar|rhetorical|summari[sz]|prompt)\b'):
        return 'language'
    if has(r'\b(wacv|cvpr|iccv|eccv|bmvc|3dv|siggraph|icip|icpr|accv|tpami|pattern recognit|comput\. vis|int\. j\. comput\. vis|trans\. vis\. comput\. graph|comput\. graph|acm trans\. graph)') or has(
        r'\b(computer vision|visual recognition|images?|videos?|visual|graphics|3d|object detection|person re-identification|scene reconstruction|point cloud|visual question answering|face recognition|facial expression|pose estimation|image understanding|rendering|segmentation|tracking|lightstage|stereoscopic|vision ssm|spatial-awareness)\b'):
        return 'vision'
    if has(r'\b(facct|aies|ccs|csf|asiaccs|pets|inf\. forensics|trans\. dependable secur)') or has(
        r'\b(fair|privacy|private|cybersecurity|security|secure|trustworthy|responsible ai|algorithmic accountability|ai ethics|explainab|robustness certification|unlearning|model stealing|adversarial|calibration|uncertainty|conformal|distribution shift|out-of-distribution|audit|disclosure risk|differential privacy|harm)\b'):
        return 'responsible'
    if has(r'\b(chi|hri|ro-man|humanoids|automotiveui|whc|haptics|affect\. comput|human-machine syst|robotics autom)') or has(
        r'\b(human-computer interaction|human-robot interaction|haptic|affective|user experience|user-centred|user-centered|social robot|robotics|robotic|gesture|human factors|workload|operator|fatigue|behavio[u]?r|emotion recognition|digital behavioural change)\b'):
        return 'human'
    if has(r'\b(smart grid|power grid|electric grid|energy system|energy management|energy consumption|net-zero energy|industrial system|industrial control|traffic management|transportation system|vehicle routing|model predictive control|cyber-physical|building energy|power system|control system|controller|scheduling|scheduler|task-based linear algebra)\b'):
        return 'engineering'
    if has(r'\b(icc|globecom|wcnc|iwcmc|pimrc|milcom|internet things|commun\. lett|commun\. soc|trans\. commun|wirel|veh\. technol|netw\. serv|mob\. comput|commun\. netw|cogn\. commun|consumer electron|comput\. networks|netw\. lett|comput\. commun)') or has(
        r'\b(wireless communication|wireless network|mobile network|communication network|network slicing|internet of things|iot|edge computing|network traffic|network management|telecommunication|radio resource|spectrum allocation|mimo|6g network|lorawan|lora network|cell-free|uav-assisted|unmanned aerial|connected vehicle|resource allocation|channel estimation)\b'):
        return 'networks'
    if has(r'\b(cdc|control\. netw|autom\. control|ind\. informatics|green commun|intell\. transp|transp\. syst|control\. syst\. lett)'):
        return 'engineering'
    if has(r'\b(neurips|nips|iclr|icml|aistats|aaai|ijcai|collas|ecml|aamas|jmlr|tmlr|mach\. learn|neural netw|automl|ijcnn|uai)\b') or has(
        r'\b(machine learning|learning theory|statistical learning|reinforcement learning|meta-learning|meta learning|generalization|generalisation|sample complexity|bayesian learning|optimization|gradient descent|few-shot|test-time adaptation|domain generalization|self-supervised|semi-supervised|deep learning|graph neural|foundation model|generative model|diffusion model|transformer|information theory|information-theoretic|multi-agent|decision-theoretic|markov decision|probabilistic|stochastic|inference|classification|prediction|forecasting|distillation|adaptation|world model|web agents?|reasoning|planning|expert aggregation|policy iteration|learning-augmented|continual learning|task switching|catastrophic forgetting)\b'):
        return 'core-ml'
    if has(r'\b(comput\. speech|speech lang|signal process)'):
        return 'language'
    if has(r'\b(medical image|medical imaging|trans\. medical imaging|health informatics|biomed)'):
        return 'medical'
    if has(r'\b(pattern recognit|comput\. vis|int\. j\. comput\. vis|trans\. pattern anal|trans\. vis\. comput\. graph|comput\. graph|acm trans\. graph)'):
        return 'vision'
    if has(r'\b(neurocomputing|trans\. mach\. learn|j\. mach\. learn)'):
        return 'core-ml'
    return 'other'


def publication_overview(papers):
    works = unique_works(papers)
    counts = {key: Counter() for key, *_ in PUBLICATION_AREAS}
    for paper in works:
        counts[publication_area(paper)][paper.get('category', 'preprint')] += 1
    return works, counts


def _publication_overview_html(fr, papers):
    works, counts = publication_overview(papers)
    categories = ('journal', 'proceedings', 'preprint')
    labels = {
        'journal': ('Journals', 'Revues'),
        'proceedings': ('Conferences', 'Conférences'),
        'preprint': ('Preprint only', 'Prépublications seules'),
    }
    fmt = lambda number: f'{number:,}'.replace(',', ' ' if fr else ',')
    def outlet_name(paper):
        venue = (paper.get('venue') or '').strip()
        if paper.get('category') == 'proceedings':
            venue = re.sub(r'\s+\(\d+\)$', '', venue)
        return {
            'Trans. Mach. Learn. Res.': 'TMLR',
            'J. Mach. Learn. Res.': 'JMLR',
            'Medical Image Anal.': 'Medical Image Analysis',
            'Pattern Recognit.': 'Pattern Recognition',
            'Comput. Vis. Image Underst.': 'Computer Vision and Image Understanding',
            'IEEE Internet Things J.': 'IEEE Internet of Things Journal',
            'IEEE Commun. Lett.': 'IEEE Communications Letters',
            'IEEE Open J. Commun. Soc.': 'IEEE Open Journal of the Communications Society',
            'IEEE Trans. Commun.': 'IEEE Transactions on Communications',
            'IEEE Trans. Medical Imaging': 'IEEE Transactions on Medical Imaging',
            'IEEE Trans. Netw. Serv. Manag.': 'IEEE Transactions on Network and Service Management',
            'IEEE Wirel. Commun. Lett.': 'IEEE Wireless Communications Letters',
            'IEEE Trans. Veh. Technol.': 'IEEE Transactions on Vehicular Technology',
            'IEEE Trans. Intell. Transp. Syst.': 'IEEE Transactions on Intelligent Transportation Systems',
            'IEEE Trans. Green Commun. Netw.': 'IEEE Transactions on Green Communications and Networking',
        }.get(venue, venue)

    parts = [
        '<details class="funding-group publication-overview" id="publication-overview" aria-labelledby="publication-overview-heading">',
        f'<summary class="publication-overview-head"><div><h3 id="publication-overview-heading">{"Aperçu des publications" if fr else "Publication overview"}</h3>',
        f'<p>{"Œuvres uniques réparties par domaine et type de publication." if fr else "Unique works grouped by research area and publication type."}</p></div>',
        f'<div class="publication-overview-total"><strong>{fmt(len(works))}</strong><span>{"œuvres uniques" if fr else "unique works"}</span></div></summary>',
        '<div class="publication-overview-content">',
        f'<p class="publication-overview-note">{"Chaque œuvre est comptée une seule fois; lorsqu’une prépublication correspond à un article de revue ou à des actes, la version publiée est privilégiée. Les domaines sont estimés à partir des titres et des lieux de publication." if fr else "Each work is counted once; when a preprint matches a journal or proceedings record, the published version is used. Areas are inferred from titles and publication venues."}</p>',
        '<div class="publication-overview-legend" aria-hidden="true">',
    ]
    for category in categories:
        parts.append(f'<span class="overview-key overview-key-{category}">{escape(labels[category][fr])}</span>')
    parts.append('</div><div class="publication-area-grid">')
    for key, en, french, description_en, description_fr in PUBLICATION_AREAS:
        area_counts = counts[key]
        total = sum(area_counts.values())
        area_works = [paper for paper in works if publication_area(paper) == key]
        parts.append(
            f'<article class="publication-area-card"><div class="publication-area-title"><h4>{escape(french if fr else en)}</h4>'
            f'<strong>{fmt(total)}</strong></div><p>{escape(description_fr if fr else description_en)}</p>'
            f'<div class="publication-area-meter" role="img" aria-label="{fmt(area_counts["journal"])} {labels["journal"][fr]}, '
            f'{fmt(area_counts["proceedings"])} {labels["proceedings"][fr]}, {fmt(area_counts["preprint"])} {labels["preprint"][fr]}">'
        )
        for category in categories:
            width = (100 * area_counts[category] / total) if total else 0
            parts.append(f'<span class="overview-meter-{category}" style="width:{width:.2f}%"></span>')
        parts.append('</div><dl>')
        for category in categories:
            parts.append(f'<div><dt>{labels[category][fr]}</dt><dd>{fmt(area_counts[category])}</dd></div>')
        parts.append('</dl><div class="publication-area-outlets">')
        for category in ('proceedings', 'journal'):
            outlets = Counter(outlet_name(paper) for paper in area_works
                              if paper.get('category') == category and outlet_name(paper))
            top = outlets.most_common(2)
            if top:
                label = ('Conférences' if fr else 'Conference venues') if category == 'proceedings' else ('Revues' if fr else 'Journal venues')
                entries = ' · '.join(f'{escape(name)} ({fmt(count)})' for name, count in top)
                parts.append(f'<p><span>{label}</span> {entries}</p>')
        parts.append('</div></article>')
    parts.append('</div></div></details>')
    return ''.join(parts)


def render(fr: bool) -> str:
    data = catalogue()
    people = data['people']
    works, _ = publication_overview(data['papers'])
    first = min(person['start'] for person in people)
    last = max(person['end'] for person in people)
    counts = Counter(p['category'] for p in works)
    def t(english, french):
        return french if fr else english
    fmt = lambda number: f'{number:,}'.replace(',', ' ' if fr else ',')
    categories = [('preprint', t('Preprints', 'Prépublications')),
                  ('journal', t('Journal papers', 'Articles de revue')),
                  ('proceedings', t('Proceedings of international conferences', 'Actes de conférences internationales'))]
    category_buttons = ''.join(
        f'<button type="button" data-category="{key}" aria-pressed="false"><strong>{fmt(counts[key])}</strong>{label}</button>'
        for key, label in categories
    )
    year_options = ''.join(f'<option>{year}</option>' for year in range(last, first - 1, -1))
    member_options = []
    for person in people:
        pid = member_ids()[person['name']]
        end_date = date(person['end'], 12, 31)
        if person['start'] == person['end'] or end_date > date.today():
            years = str(person['start'])
        else:
            years = f"{person['start']}–{person['end']}"
        member_options.append(f'<option value="{escape(pid)}">{escape(person["name"])} · {years}</option>')
    intro = t('Browse works from member publication windows spanning 2022–Present. Matching preprint and published records are combined.',
              'Parcourez les travaux selon les périodes de publication des membres, de 2022 à aujourd’hui. Les prépublications et versions publiées correspondantes sont regroupées.')
    overview = _publication_overview_html(fr, data['papers'])
    payload_data = {**data, 'papers': works}
    payload = json.dumps(payload_data, ensure_ascii=False, separators=(',', ':')).replace('<', r'\u003c')
    parts = [
        '<section class="section publications-section" id="publications" aria-labelledby="publications-heading"><div class="wrap">',
        '<h2 id="publications-heading">Publications</h2>',
        f'<p class="lead">{intro}</p>',
        f'''<div id="publication-browser" hidden>
          <div class="catalogue-types" role="group" aria-label="{t('Publication category', 'Catégorie de publication')}">{category_buttons}</div>
          <div class="catalogue-filters">
            <label>{t('Search publications', 'Rechercher une publication')}<input type="search" id="pub-search" placeholder="{t('Title, author or venue', 'Titre, auteur ou lieu de publication')}"></label>
            <label>{t('Year', 'Année')}<select id="pub-year"><option value="">{t('All years', 'Toutes les années')}</option>{year_options}</select></label>
            <label>{t('ILLS member', 'Membre de l’ILLS')}<select id="pub-member"><option value="">{t('All members', 'Tous les membres')}</option>{''.join(member_options)}</select></label>
          </div>
          <label class="catalogue-joint-filter"><input type="checkbox" id="pub-joint">
            <span>{t('France–Canada joint publications only', 'Publications conjointes France–Canada uniquement')}</span></label>
          <div class="catalogue-tools"><button type="button" id="pub-reset">{t('Clear filters', 'Effacer les filtres')}</button>
            <button type="button" id="pub-export">{t('Download results (CSV)', 'Télécharger les résultats (CSV)')}</button></div>
          {overview}
          <h3 id="pub-count" role="status" tabindex="-1"></h3><ol id="pub-results" aria-labelledby="pub-count"></ol>
          <nav class="catalogue-pages" aria-label="{t('Publication results pages', 'Pages des résultats')}">
            <button type="button" id="pub-prev">{t('Previous', 'Précédente')}</button>
            <span id="pub-page"></span><button type="button" id="pub-next">{t('Next', 'Suivante')}</button></nav>
        </div><noscript><p>{t('Enable JavaScript to search the full catalogue.', 'Activez JavaScript pour parcourir le catalogue complet.')}</p></noscript>
        <script type="application/json" id="bibliography">{payload}</script>''',
        '</div></section>',
    ]
    return "\n".join(parts)
