"""Render the public research programme from its bilingual editorial source."""

from html import escape

from content import funding, publications
from content.research import AXES, FR_AXES, FOUNDATIONS_PAPERS
from content.research_papers import AXIS_PAPERS


def render_axis_papers(fr: bool, prefix: str, axis_slug: str, papers: list) -> str:
    section_title = 'Publications sélectionnées' if fr else 'Selected publications'
    intro = (
        'Quelques travaux de membres et d’étudiants de l’ILLS illustrent les questions de cet axe.'
        if fr else
        'A selection of ILLS member and student research connected to this axis.'
    )
    authors_label = 'Auteurs de l’ILLS' if fr else 'ILLS authors'
    pause_label = 'Mettre le carrousel en pause' if fr else 'Pause carousel'
    read_label = 'Lire l’article' if fr else 'Read paper'
    position_label = 'sur' if fr else 'of'
    cards = []
    papers = sorted(papers, key=lambda paper: int(paper['year']))
    total = len(papers)
    for i, paper in enumerate(papers, 1):
        title = escape(paper['title'])
        authors = ', '.join(
            f'<a href="{escape(author.get("url") or prefix + author["path"], quote=True)}">{escape(author["name"])}</a>'
            for author in paper['ills_authors']
        )
        figure_src = paper.get('figure_url') or (prefix + 'assets/' + paper['figure'])
        cards.append(
            f'<article class="axis-paper-card" role="group" aria-roledescription="slide" '
            f'aria-label="{i} {position_label} {total}">'
            f'<a class="axis-paper-visual" href="{escape(paper["url"], quote=True)}" '
            f'aria-label="{read_label}: {title}"><img src="{escape(figure_src, quote=True)}" '
            f'alt="{escape(paper["figure_alt"][int(fr)], quote=True)}" loading="lazy" decoding="async"></a>'
            f'<p class="axis-paper-credit"><a href="{escape(paper["url"], quote=True)}">'
            f'{escape(paper["credit"])}</a><span aria-hidden="true">·</span>'
            f'<a href="{escape(paper["license_url"], quote=True)}">{escape(paper["license"])}</a></p>'
            f'<div class="axis-paper-copy"><p class="axis-paper-meta">{escape(paper["year"])} '
            f'<span aria-hidden="true">·</span> {escape(paper["venue"])}</p>'
            f'<h4><a href="{escape(paper["url"], quote=True)}">{title}</a></h4>'
            f'<p class="axis-paper-summary">{escape(paper["summary"][int(fr)])}</p>'
            f'<p class="axis-paper-authors"><span>{authors_label}:</span> {authors}</p></div>'
            '</article>'
        )
    return (
        f'<section class="axis-papers" aria-labelledby="{axis_slug}-papers-title" data-paper-carousel>'
        '<div class="axis-papers-head"><div>'
        f'<p class="eyebrow">{("Research in action" if not fr else "La recherche en pratique")}</p>'
        f'<h3 id="{axis_slug}-papers-title">{section_title}</h3><p>{intro}</p></div>'
        '<div class="axis-papers-controls">'
        f'<button type="button" data-paper-toggle aria-label="{pause_label}">'
        f'{("Pause" if not fr else "Pause")}</button></div></div>'
        f'<div class="axis-paper-track" data-paper-track role="region" tabindex="0" '
        f'aria-label="{section_title}" aria-roledescription="carousel">{"".join(cards)}</div>'
        '</section>'
    )


def render(fr: bool, prefix: str) -> str:
    axes = FR_AXES if fr else AXES
    assets = escape(f'{prefix}assets/', quote=True)
    title = 'Programme scientifique' if fr else 'Research programme'
    intro = (
        'Comment concevoir des systèmes d’apprentissage fiables malgré l’incertitude ? Dans quatre axes '
        'complémentaires, l’ILLS étudie les fondements de l’apprentissage automatique, l’IA générative digne '
        'de confiance, les systèmes multi-agents et les applications en santé et dans les systèmes d’ingénierie '
        'critiques. L’évaluation, la protection de la vie privée et le déploiement responsable traversent ces travaux.'
        if fr else
        'How can we build learning systems that remain reliable under uncertainty? Across four connected research '
        'areas, ILLS studies machine learning foundations, trustworthy generative AI, multi-agent systems, and '
        'applications in healthcare and critical engineering. Evaluation, privacy and responsible deployment run '
        'through this work.'
    )
    axis_word = 'Axe' if fr else 'Axis'
    roman_numerals = ('I', 'II', 'III', 'IV')
    nav_heading = 'Axes de recherche' if fr else 'Research areas'
    parts = [
        '<header class="inner-hero"><div class="wrap programme-heading">',
        f'<h1>{title}</h1><p class="lead">{intro}</p>',
        f'<nav class="section-jumps" aria-label="{"Sur cette page" if fr else "On this page"}">'
        f'<a href="#research-areas">{nav_heading}</a>'
        f'<a href="#funding-research-chairs">{escape(funding.TITLE[fr])}</a>'
        '<a href="#publications">Publications</a>'
        f'<a href="?joint=1#publications">{"Publications conjointes France–Canada" if fr else "France–Canada joint publications"}</a></nav>',
        '</div></header>',
        '<div class="wrap programme-layout" id="research-areas">',
        '<nav class="programme-nav" aria-labelledby="axes-nav-title">',
        f'<h2 id="axes-nav-title">{nav_heading}</h2><ol>',
    ]
    for n, axis in enumerate(axes, 1):
        parts.append(
            f'<li><a href="#{axis["slug"]}">'
            f'<span class="programme-index-number" aria-hidden="true">{roman_numerals[n - 1]}</span>'
            f'<span>{escape(axis["short_title"])}</span></a></li>'
        )
    parts.append('</ol></nav><div class="programme-chapters">')
    for n, axis in enumerate(axes, 1):
        slug = axis['slug']
        parts.extend([
            f'<article class="programme-chapter" id="{slug}" aria-labelledby="chapter-{n}">',
            '<div class="programme-chapter-head no-illustration"><div>',
            f'<p class="eyebrow">{axis_word} {roman_numerals[n - 1]}</p>',
            f'<h2 id="chapter-{n}">{escape(axis["title"])}</h2></div>',
            '</div>',
            f'<p class="programme-body">{escape(axis["description"])}</p>',
            '<div class="programme-examples">',
        ])
        for example in axis['projects']:
            heading = escape(example['title'])
            if 'url' in example:
                heading = f'<a href="{escape(example["url"])}">{heading}</a>'
            logos = ''.join(
                f'<a href="{escape(logo["url"])}" aria-label="{escape(logo["label"])}" '
                f'title="{escape(logo["label"])}"><img src="{assets}{escape(logo["image"], quote=True)}" '
                f'alt="{escape(logo["label"])}" loading="lazy" decoding="async"></a>'
                for logo in example.get('logos', ())
            )
            project_logos = f'<span class="research-project-logos">{logos}</span>' if logos else ''
            parts.append(
                f'<section><h3 class="research-project-heading">{heading}{project_logos}</h3>'
                f'<p>{escape(example["description"])}</p></section>'
            )
        parts.append('</div></article>')
        papers = FOUNDATIONS_PAPERS if slug == 'foundations' else AXIS_PAPERS.get(slug, ())
        if papers:
            parts.append(render_axis_papers(fr, prefix, slug, papers))
    parts.append('</div></div>')
    parts.append(funding.render(fr, prefix))
    parts.append(publications.render(fr))
    return '\n'.join(parts)
