#!/usr/bin/env python3
"""Build both language editions of the ILLS website. No dependencies."""
from pathlib import Path
from html import escape
from functools import lru_cache
from hashlib import sha256
from content import programme, network, laboratory, people, listings

ROMAN_NUMERALS = ("I", "II", "III", "IV")
from content.research import AXES, FR_AXES

OUT=Path(__file__).resolve().parent/'site'
NAV=[
 ('index','Overview','Accueil'),
 ('people','People','Équipe'),
 ('research','Research','Recherche'),
 ('seminars-events', *listings.CALENDAR_TITLE),
 ('openings', *listings.OPENINGS_TITLE),
 ('cnrs-applications', *listings.APPLICATIONS_TITLE),
 ('news', *listings.NEWS_TITLE),
]
DESCRIPTIONS={
 'index':('A France–Canada laboratory connecting the mathematical foundations of machine learning with trustworthy AI in practice.','Un laboratoire franco-canadien qui relie les fondements mathématiques de l’apprentissage automatique à la fiabilité de l’IA en pratique.'),
 'people':('Explore the ILLS directory of members, visiting researchers, students and visitors.','Parcourez l’annuaire de l’ILLS pour découvrir ses membres, ses chercheurs invités, sa communauté étudiante et ses visiteurs.'),
 'research':('Explore the ILLS research areas, research chairs, funding, industry collaborations and member publications.','Découvrez les axes de recherche de l’ILLS ainsi que les chaires, les financements, les collaborations industrielles et les publications de ses membres.'),
 'seminars-events': listings.CALENDAR_INTRO,
 'openings': listings.OPENINGS_INTRO,
 'cnrs-applications': listings.APPLICATIONS_INTRO,
 'news': listings.NEWS_INTRO,
}


@lru_cache(maxsize=None)
def asset_url(name):
    path = 'assets/' + name
    version = sha256((OUT / path).read_bytes()).hexdigest()[:10]
    return f'{path}?v={version}'


def icon(name='arrow',small=False):
    paths={'arrow':'<path d="M3 12h16m-6-6 6 6-6 6"/>','out':'<path d="M5 18 18 5M6 5h12v12"/>','globe':'<circle cx="12" cy="12" r="9"/><ellipse cx="12" cy="12" rx="4" ry="9"/><path d="M3 12h18"/>','file':'<path d="M6 3h8l4 4v14H6z M14 3v5h4 M9 12h6 M9 15h6"/>','menu':'<path d="M2 6h20M2 12h20M2 18h20"/>','down':'<path d="M12 3v15m-6-6 6 6 6-6"/>'}
    return '<svg aria-hidden="true" class="arrow'+(' small-arr' if small else '')+'" viewBox="0 0 24 24">'+paths[name]+'</svg>'

def home(fr,pre):
    def t(en,frn):return frn if fr else en
    axes=FR_AXES if fr else AXES
    cards=''.join(f'''<a class="axis-card" href="research.html#{a["slug"]}"><img class="axis-image" src="{pre}assets/art/axis-{i}.png" alt="" width="759" height="503" loading="lazy"><div class="axis-card-copy"><span class="micro">{t("Research axis","Axe de recherche")} {ROMAN_NUMERALS[i-1]}</span><h3>{a["short_title"]}</h3><p>{a["teaser"]}</p><span class="card-arrow">{icon('arrow',True)}</span></div></a>''' for i,a in enumerate(axes,1))
    heading=t('<span>International</span> <span>Laboratory on</span> <em>Learning Systems</em>','<span>Laboratoire international</span> <em>sur les systèmes d’apprentissage</em>')
    return f'''
    <section class="hero"><div class="wrap"><div class="hero-main">
      <div class="hero-copy"><div class="eyebrow">{t("CNRS International Research Laboratory","Laboratoire de recherche international du CNRS")}</div>
      <h1>{heading}</h1><p>{t("We study how machines learn, when their predictions can be trusted, and how they can support decisions in the real world.","Nous étudions comment les machines apprennent, quand leurs prédictions sont fiables et comment elles peuvent éclairer les décisions humaines.")}</p>
      <div class="hero-actions"><a class="btn btn-aqua" href="research.html">{t("Explore our research","Explorer nos recherches")}{icon()}</a><a class="link-arrow" href="research.html#publications">Publications{icon("arrow",True)}</a></div></div>
      <figure class="hero-figure" aria-label="{t("A three-dimensional neural network mapped onto a learning surface, with neurons firing and signals traveling along their connections","Un réseau de neurones en trois dimensions tracé sur une surface d’apprentissage, avec des neurones qui s’activent et des signaux qui parcourent leurs connexions")}">
        <img class="hero-surface-fallback" src="{pre}assets/art/learning-surface.webp" alt="" width="1200" height="972" fetchpriority="high">
        <canvas class="hero-surface-motion" aria-hidden="true"></canvas>
      </figure>
    </div><div class="hero-base"><span class="geography">Montréal, Canada <i></i> France</span>
      <nav class="overview-jumps" aria-label="{t("On this page","Sur cette page")}"><a href="#laboratory">{t("Laboratory","Laboratoire")}</a><a href="#partners">{t("Partners","Partenaires")}</a><a href="#contact">Contact</a></nav>
    </div></div></section>
    <section class="section"><div class="wrap"><div class="section-head"><div><p class="eyebrow">{t("Scientific programme","Programme scientifique")}</p><h2>{t("Research directions","Axes de recherche")}</h2><p class="research-intro">{t("How can learning systems stay reliable when data are uncertain or conditions change? Across four connected research areas, ILLS studies machine learning foundations, trustworthy generative AI, multi-agent AI and world models, and applications in healthcare and critical engineering. The programme also asks how to evaluate systems, protect privacy, and support responsible deployment in real settings.","Comment concevoir des systèmes d’apprentissage qui restent fiables lorsque les données sont incertaines ou que les conditions changent ? À travers quatre axes complémentaires, l’ILLS étudie les fondements de l’apprentissage automatique, l’IA générative digne de confiance, l’IA multi-agents et les modèles du monde, ainsi que les applications en santé et dans les systèmes d’ingénierie critiques. Le programme examine aussi l’évaluation, la protection de la vie privée et les conditions d’un déploiement responsable.")}</p></div><a class="link-arrow" href="research.html">{t("View programme","Voir le programme")}{icon()}</a></div><div class="axis-grid">{cards}</div></div></section>
    {laboratory.render(fr,pre)}
    {network.render(fr,pre)}
    {laboratory.render_contact(fr,pre)}'''

def build_page(slug,fr,member=None,student=None):
    def t(en,frn):return frn if fr else en
    profile = bool(member or student)
    up = ('../../../' if fr else '../../') if student else ('../' if member else '')
    if student:
        prefix = up
    elif member:
        prefix = up + ('../' if fr else '')
    else:
        prefix = '../' if fr else ''
    if student:
        filename=f'people/students/{student["biography"]["slug"]}.html'
    else:
        filename=f'people/{member["biography"]["slug"]}.html' if member else f'{slug}.html'
    altlang='en' if fr else 'fr'
    if student and fr:
        alternate=up+filename
    else:
        alternate=up+('../' if fr else 'fr/')+filename
    page_title='International Laboratory on Learning Systems' if slug=='index' else next(r[1+fr] for r in NAV if r[0]==slug)
    if fr and slug=='index':page_title='Laboratoire international sur les systèmes d’apprentissage'
    if member:page_title=member['name']
    if student:page_title=student['name']
    description=(member or student)['biography']['text'][fr] if profile else DESCRIPTIONS[slug][fr]
    current='location' if profile else 'page'
    nav=''.join('<a href="'+up+r[0]+'.html"'+(f' aria-current="{current}"' if r[0]==slug else '')+'>'+escape(r[1+fr])+'</a>' for r in NAV)
    page_styles = {'index': ('network',), 'research': ('programme', 'publications'), 'people': ('people',),
                   'seminars-events': ('events',), 'news': ('events',)}
    extra = ''.join(f'<link rel="stylesheet" href="{prefix}{asset_url(name + ".css")}">' for name in page_styles.get(slug, ()))
    if slug == 'research':
        extra += f'<script defer src="{prefix}{asset_url("publications.js")}"></script>'
        extra += f'<script defer src="{prefix}{asset_url("papers-carousel.js")}"></script>'
    if slug == 'index':
        extra += f'<script defer src="{prefix}{asset_url("hero-motion.js")}"></script>'
    logo_alt=t('ILLS home','Accueil de l’ILLS')
    if member:
        body = people.render_profile(member, fr, prefix)
    elif student:
        body = people.render_student_profile(student, fr, prefix)
    else:
        render = {
            'index': home, 'people': people.render, 'research': programme.render,
            'seminars-events': listings.render_calendar, 'openings': listings.render_openings,
            'cnrs-applications': listings.render_applications, 'news': listings.render_news,
        }[slug]
        body = render(fr, prefix)
    dest=OUT/('fr' if fr else '')/filename
    dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text(f'''<!doctype html>
<html lang="{t("en","fr")}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(page_title)} | ILLS</title><meta name="description" content="{escape(description)}"><meta name="theme-color" content="#09192f">
<link rel="alternate" hreflang="{altlang}" href="{alternate}"><link rel="icon" type="image/png" sizes="64x64" href="{prefix}assets/brand/favicon.png">
<link rel="stylesheet" href="{prefix}{asset_url("style.css")}">{extra}<script defer src="{prefix}{asset_url("site.js")}"></script></head>
<body><a class="skip" href="#main">{t("Skip to content","Aller au contenu")}</a>
<header class="site-header"><div class="wrap navrow"><a class="brand" href="{up}index.html" aria-label="{logo_alt}"><img src="{prefix}assets/brand/logo-color.png" width="600" height="240" alt="ILLS"></a>
<nav id="main-nav" class="main-nav" aria-label="{t("Main navigation","Navigation principale")}">{nav}</nav>
<div class="nav-end"><a class="lang-link" href="{alternate}" hreflang="{altlang}" lang="{altlang}" aria-label="{t("Version française","English version")}">{icon('globe')}{altlang.upper()}</a>
<a class="btn header-contact" href="{up}index.html#contact">Contact{icon('out',True)}</a>
<button class="menu-toggle" type="button" aria-label="Menu" aria-controls="main-nav" aria-expanded="false">{icon('menu')}</button></div></div></header>
<main id="main">{body}</main>
<footer class="footer"><div class="wrap"><div class="foot-row"><a href="{up}index.html" aria-label="{logo_alt}"><img src="{prefix}assets/brand/logo-dark.png" alt="ILLS" width="600" height="240" loading="lazy"></a><nav class="foot-links" aria-label="{t("Footer","Pied de page")}"><a href="{up}index.html#contact">Contact</a><a href="{up}research.html">{t("Research programme","Programme scientifique")}</a><a href="{up}research.html#publications">Publications</a></nav></div><div class="foot-base"><span>International Laboratory on Learning Systems</span><span>Montréal, Québec · France</span></div></div></footer>
</body></html>''',encoding='utf-8')


LEGACY_PAGES = {
    'laboratory': ('index.html#laboratory', 'The laboratory', 'Le laboratoire'),
    'network': ('index.html#partners', 'Partner institutions', 'Établissements partenaires'),
    'publications': ('research.html#publications', 'Publications', 'Publications'),
    'seminars': ('seminars-events.html#seminars', 'Seminars', 'Séminaires'),
    'events': ('seminars-events.html', *listings.CALENDAR_TITLE),
}


def build_redirect(slug, fr):
    target, en_label, fr_label = LEGACY_PAGES[slug]
    directory = OUT / ('fr' if fr else '')
    other = '../' if fr else 'fr/'
    assets = '../assets/' if fr else 'assets/'
    lang, alternate = ('fr', 'en') if fr else ('en', 'fr')
    label = escape(fr_label if fr else en_label)
    heading = 'Page déplacée' if fr else 'Page moved'
    (directory / f'{slug}.html').write_text(f'''<!doctype html>
<html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{label} | ILLS</title><link rel="canonical" href="{target.split('#')[0]}">
<link rel="alternate" hreflang="{alternate}" href="{other}{slug}.html">
<noscript><meta http-equiv="refresh" content="0;url={target}"></noscript>
<link rel="stylesheet" href="{assets}style.css"><script defer src="{assets}redirect.js"></script>
</head><body><main class="section wrap"><h1>{heading}</h1>
<a class="text-link" id="destination" href="{target}">{label}</a></main></body></html>''', encoding='utf-8')


if __name__=='__main__':
    profiles=[m for m in people.MEMBERS if 'biography' in m]
    for fr in (False,True):
        for slug,*_ in NAV:build_page(slug,fr)
        for member in profiles:build_page('people',fr,member)
        for student in people.STUDENTS:build_page('people',fr,student=student)
        for slug in LEGACY_PAGES:build_redirect(slug,fr)
    print(f'Built {2 * (len(NAV) + len(profiles) + len(people.STUDENTS))} pages and {2 * len(LEGACY_PAGES)} redirects in site/.')
