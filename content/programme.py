"""Render the public research programme from its bilingual editorial source."""

from html import escape

from content import funding, publications
from content.research import AXES, FR_AXES


def render(fr: bool, prefix: str) -> str:
    axes = FR_AXES if fr else AXES
    assets = escape(f'{prefix}assets/', quote=True)
    title = 'Programme scientifique' if fr else 'Research programme'
    intro = (
        'Comment savoir si l’on peut se fier à un système d’apprentissage ? Les équipes de l’ILLS '
        'abordent cette question sous quatre angles, des garanties mathématiques à l’évaluation en milieu clinique.'
        if fr else
        'How do we know when to trust a learning system? ILLS researchers approach this question '
        'through four research axes, from mathematical guarantees to evaluation in clinical settings and critical engineering systems.'
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
        f'<a href="#joint-research-papers">{"Publications conjointes" if fr else "Joint research publications"}</a></nav>',
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
            '<div class="programme-chapter-head"><div>',
            f'<p class="eyebrow">{axis_word} {roman_numerals[n - 1]}</p>',
            f'<h2 id="chapter-{n}">{escape(axis["title"])}</h2></div>',
            f'<img src="{assets}art/axis-{n}.png" width="759" height="503" alt="" loading="lazy"></div>',
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
    parts.append('</div></div>')
    parts.append(funding.render(fr, prefix))
    parts.append(publications.render(fr))
    return '\n'.join(parts)
