"""Public sources for chairs, grants and industry collaborations involving ILLS members."""

from dataclasses import dataclass
from html import escape

from content.people import MEMBERS


TITLE = ('Funding & Research Chairs', 'Financements et chaires de recherche')


@dataclass(frozen=True)
class Entry:
    title: tuple[str, str]
    description: tuple[str, str]
    source: str
    members: tuple[str, ...]


@dataclass(frozen=True)
class Organization:
    name: str
    website: str
    logo: str
    members: tuple[str, ...]
    french_name: str = ''


CENTORIA = 'https://www.dataia.eu/index.php/en/node/1394'
ETS_CHAIRS = 'https://www.etsmtl.ca/en/research/chairs-laboratories-institutes-centres/research-chairs/'
DIAGNOS = 'https://www.etsmtl.ca/actualites/chaire-intelligence-artificielle-imagerie-medicale'
SUMMIT = ETS_CHAIRS + 'summit-tech-research-chair-immersive-interactive-video'
ZEBRA = ETS_CHAIRS + 'zebra'
DISTECH = ETS_CHAIRS + 'distech-controls'
ULTRA = ETS_CHAIRS + 'ultra-tcs'

CHAIRS = (
    Entry(('CentOrIA', 'CentOrIA'),
          ('This joint DataIA chair at Paris-Saclay studies how attention models learn from sequences and how AI agents exchange information.',
           'Cette chaire de l’Institut DataIA à Paris-Saclay étudie comment les modèles d’attention apprennent à partir de séquences et comment des agents d’IA échangent de l’information.'),
          CENTORIA, ('pablo-piantanida',)),
    Entry(('Canada CIFAR AI Chair', 'Chaire en IA Canada-CIFAR'),
          ('At McGill and Mila, Jackie Chi Kit Cheung studies how computers understand and generate language, including how they summarize text.',
           'À McGill et à Mila, Jackie Chi Kit Cheung étudie la compréhension et la génération du langage par ordinateur, notamment le résumé automatique de textes.'),
          'https://mila.quebec/en/directory/jackie-cheung', ('jackie-chi-kit-cheung',)),
    Entry(('Canada Research Chair in Unlocking the Power of the IoT 6G-Networks', 'Chaire de recherche du Canada sur l’Internet des objets et les réseaux 6G'),
          ('A Canada Research Chair at ÉTS on wireless networks that connect large numbers of devices. The chair was renewed in 2024.',
           'Cette chaire à l’ÉTS porte sur les réseaux sans fil qui relient un grand nombre d’objets connectés. Son mandat a été renouvelé en 2024.'),
          'https://www.chairs-chaires.gc.ca/media-medias/lists-listes/2024/fall-automne-eng.aspx', ('georges-kaddoum',)),
    Entry(('Werner Graupe Distinguished Chair in Automation Engineering', 'Chaire Werner Graupe en génie de l’automatisation'),
          ('McGill appointed Jeremy R. Cooperstock to this endowed chair for the 2024–2029 term.',
           'L’Université McGill a nommé Jeremy R. Cooperstock titulaire de cette chaire pour le mandat 2024–2029.'),
          'https://www.mcgill.ca/provost/academics/distinguished-professorships/named-chairs', ('jeremy-r-cooperstock',)),
    Entry(('Institut universitaire de France Chair in Fundamental Research', 'Chaire fondamentale de l’Institut universitaire de France'),
          ('At Sorbonne Université, this chair studies how a surgical robot can perceive the operating field and reason about the surgeon’s instructions.',
           'À Sorbonne Université, cette chaire étudie comment un robot peut percevoir le champ opératoire et interpréter les instructions du chirurgien.'),
          'https://sciences.sorbonne-universite.fr/actualites/lia-au-chevet-des-robots-chirurgicaux', ('nicolas-thome',)),
    Entry(('Double Research Chair in AI and Digital Health for Health Behaviour Change', 'Chaire double en IA et en santé numérique pour le changement des comportements de santé'),
          ('Awarded in 2021 for three years, this joint chair studied how to recognize and address ambivalence when people consider changing their health habits.',
           'Attribuée en 2021 pour trois ans, cette chaire double a étudié comment reconnaître et prendre en compte l’ambivalence des personnes qui envisagent de changer leurs habitudes de santé.'),
          'https://www.concordia.ca/news/stories/2021/07/22/concordia-professor-lands-unique-co-chair-in-artificial-intelligence-and-health.html', ('eric-granger',)),
    Entry(('DIAGNOS Research Chair in AI for Medical Imaging', 'Chaire de recherche DIAGNOS en IA appliquée à l’imagerie médicale'),
          ('At ÉTS, the chair develops methods for analysing medical images, including retinal images used in eye disease screening.',
           'À l’ÉTS, la chaire développe des méthodes d’analyse d’images médicales, notamment des images de la rétine utilisées pour le dépistage des maladies oculaires.'),
          DIAGNOS, ('ismail-ben-ayed',)),
    Entry(('Distech Controls Research Chair', 'Chaire de recherche Distech Controls'),
          ('Co-held at ÉTS from 2021 to 2026, this chair studied how to run neural networks on building controllers with limited computing power.',
           'Codirigée à l’ÉTS de 2021 à 2026, cette chaire a étudié comment exécuter des réseaux de neurones sur des contrôleurs de bâtiment à capacité de calcul limitée.'),
          DISTECH, ('eric-granger', 'marco-pedersoli')),
    Entry(('Summit Tech Research Chair in Immersive Interactive Video', 'Chaire de recherche Summit Tech sur la vidéo immersive et interactive'),
          ('Stéphane Coulombe co-holds this ÉTS chair on capturing, processing and delivering immersive video.',
           'Stéphane Coulombe est cotitulaire de cette chaire de l’ÉTS consacrée à la capture, au traitement et à la diffusion de vidéos immersives.'),
          SUMMIT, ('stephane-coulombe',)),
    Entry(('Ultra TCS Research Chair in Tactical Wireless Networks', 'Chaire de recherche Ultra TCS sur les réseaux tactiques sans fil'),
          ('The ÉTS chair investigated how wireless networks can maintain communication under interference and changing conditions.',
           'Les travaux de cette chaire de l’ÉTS ont porté sur le maintien des communications sans fil en présence d’interférences et de conditions changeantes.'),
          ULTRA, ('georges-kaddoum',)),
    Entry(('Zebra Research Chair in Computer Vision for Industrial Applications', 'Chaire de recherche Zebra en vision par ordinateur pour les applications industrielles'),
          ('The ÉTS chair develops computer vision methods for industrial settings where training images can be scarce.',
           'Cette chaire de l’ÉTS développe des méthodes de vision par ordinateur pour des applications industrielles où les images d’entraînement peuvent être rares.'),
          ZEBRA, ('christian-desrosiers',)),
)

FUNDING = (
    Organization('French National Research Agency (ANR)', 'https://anr.fr/', 'funders/anr.png',
                 ('spyros-angelopoulos', 'heber-h-arcolezi', 'magali-richard', 'ricard-marxer'),
                 'Agence nationale de la recherche (ANR)'),
    Organization('Canada Foundation for Innovation', 'https://www.innovation.ca/', 'funders/cfi.svg',
                 ('audrey-a-sedal',), 'Fondation canadienne pour l’innovation'),
    Organization('Canadian Institutes of Health Research (CIHR)', 'https://cihr-irsc.gc.ca/e/193.html', 'funders/cihr.jpg',
                 ('ismail-ben-ayed', 'jose-dolz'), 'Instituts de recherche en santé du Canada (IRSC)'),
    Organization('Fonds de recherche du Québec – Santé (FRQS)', 'https://frq.gouv.qc.ca/sante/organisation/', 'funders/frqs.png',
                 ('jose-dolz', 'pablo-piantanida')),
    Organization('France 2030', 'https://www.info.gouv.fr/grand-dossier/france-2030', 'funders/france-2030.jpg',
                 ('pablo-piantanida', 'mark-coates')),
    Organization('French Health Data Hub', 'https://health-data-hub.fr/', 'funders/health-data-hub.png',
                 ('jose-dolz', 'pablo-piantanida'), 'Plateforme des données de santé'),
    Organization('IVADO', 'https://ivado.ca/', 'funders/ivado.png',
                 ('ulrich-aivodji', 'jackie-chi-kit-cheung', 'pablo-piantanida')),
    Organization('Natural Sciences and Engineering Research Council of Canada (NSERC)', 'https://nserc-crsng.canada.ca/en',
                 'funders/nserc.svg', ('mark-coates', 'ajung-moon', 'aditya-mahajan', 'mohammadhadi-shateri'),
                 'Conseil de recherches en sciences naturelles et en génie du Canada (CRSNG)'),
    Organization('Social Sciences and Humanities Research Council (SSHRC)', 'https://sshrc-crsh.canada.ca/en.aspx',
                 'funders/sshrc.png', ('jackie-chi-kit-cheung', 'pablo-piantanida'),
                 'Conseil de recherches en sciences humaines (CRSH)'),
)

INDUSTRY = (
    Organization('Air Liquide', 'https://www.airliquide.com/', 'industry/air-liquide.svg', ('pablo-piantanida',)),
    Organization('DIAGNOS', 'https://diagnosmedical.com/', 'industry/diagnos.png', ('ismail-ben-ayed',)),
    Organization('Distech Controls', 'https://www.distech-controls.com/', 'industry/distech-controls.png',
                    ('eric-granger', 'marco-pedersoli')),
    Organization('Ekimetrics', 'https://www.ekimetrics.com/', 'industry/ekimetrics.svg',
                    ('spyros-angelopoulos', 'pablo-piantanida')),
    Organization('GE HealthCare', 'https://www.gehealthcare.com/', 'industry/ge-healthcare.svg', ('pablo-piantanida',)),
    Organization('Safran', 'https://www.safran-group.com/', 'industry/safran.svg', ('pablo-piantanida',)),
    Organization('Summit Tech', 'https://summit-tech.ca/', 'industry/summit-tech.png', ('stephane-coulombe',)),
    Organization('Ubisoft La Forge', 'https://www.ubisoft.com/en-us/studio/laforge', 'industry/ubisoft-la-forge.png',
                    ('eric-granger',)),
    Organization('Ultra TCS', 'https://www.ultra-ic.com/', 'industry/ultra-tcs.png', ('georges-kaddoum',)),
    Organization('Zebra Technologies', 'https://www.zebra.com/', 'industry/zebra-technologies.svg', ('christian-desrosiers',)),
)

GROUPS = (
    (('Research chairs', 'Chaires de recherche'), CHAIRS, None),
    (('Funding agencies and programmes', 'Organismes et programmes de financement'), FUNDING, 'funding-agencies'),
    (('Industry partners', 'Partenaires industriels'), INDUSTRY, 'industry-partners'),
)


def render(fr: bool, prefix: str) -> str:
    current = {m['biography']['slug']: m['name'] for m in MEMBERS
               if m['status'] == 'current' and m.get('biography')}
    intro = ('Ces chaires, organismes de financement et partenaires industriels soutiennent les travaux des membres de l’ILLS.'
             if fr else 'These chairs, funding agencies and industry partners support the work of ILLS members.')
    groups = []
    for title, entries, grid_id in GROUPS:
        items = []
        for entry in entries:
            eligible = [slug for slug in entry.members if slug in current]
            if not eligible:
                continue
            if isinstance(entry, Organization):
                name = entry.french_name if fr and entry.french_name else entry.name
                items.append(
                    f'<li><a href="{escape(entry.website)}"><img class="organization-logo" '
                    f'src="{escape(prefix)}assets/{escape(entry.logo)}" alt="{escape(name)}" '
                    'loading="lazy" decoding="async"></a></li>'
                )
                continue
            profiles = [f'<a href="people/{escape(slug)}.html">{escape(current[slug])}</a>' for slug in eligible]
            items.append(
                f'<li><h4><a href="{escape(entry.source)}">{escape(entry.title[fr])}</a></h4>'
                f'<p>{escape(entry.description[fr])}</p>'
                f'<p class="funding-members">{", ".join(profiles)}</p></li>'
            )
        if items:
            list_attributes = f' id="{grid_id}" class="organization-grid"' if grid_id else ''
            groups.append(
                f'<details class="funding-group"><summary><h3>{escape(title[fr])}</h3></summary>'
                f'<ul{list_attributes}>{"".join(items)}</ul></details>'
            )
    return (f'<section class="section funding-section" id="funding-research-chairs" aria-labelledby="funding-title">'
            f'<div class="wrap"><h2 id="funding-title">{escape(TITLE[fr])}</h2><p class="lead">{intro}</p>'
            f'{"".join(groups)}</div></section>')
