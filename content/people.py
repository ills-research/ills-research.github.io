"""Render the bilingual ILLS member directory as static, locally browsable HTML."""

import json
from html import escape
from pathlib import Path

from content.publications import member_link

MEMBERS = json.loads(Path(__file__).with_name('members.json').read_text(encoding='utf-8'))
VISITORS = json.loads(Path(__file__).with_name('visitors.json').read_text(encoding='utf-8'))
STUDENTS = json.loads(Path(__file__).with_name('students.json').read_text(encoding='utf-8'))


INSTITUTION_COUNTRIES = {
    **dict.fromkeys(('McGill University', 'Mila', 'ÉTS', 'The Neuro',
                     'Université du Québec à Montréal'), 'ca'),
    **dict.fromkeys(('CNRS', 'Sorbonne Université', 'Aix-Marseille Université', 'LIS',
                     'IRT Saint Exupéry', 'ENS de Lyon', 'LIP', 'Université de Toulon',
                     'Université de Nice', 'CentraleSupélec', 'Université Paris-Saclay',
                     'Université Grenoble Alpes'), 'fr'),
}


def mila_logo(assets):
    return f'<img class="mila-wordmark" src="{assets}partners/mila.png" width="404" height="164" alt="Mila">'


LAB_LOGOS = {
    'livia': {
        'label': 'LIVIA',
        'image': 'partners/livia.png',
    },
    'cim': {
        'label': 'CIM — Centre for Intelligent Machines',
        'image': 'partners/cim.png',
    },
}


def lab_logo_links(member, assets=''):
    logos = []
    for key in member.get('lab_logos', ()):
        if key == 'livia' and 'ÉTS' in member['affiliation']:
            continue
        logo = LAB_LOGOS[key]
        logo_class = 'member-lab-logo member-lab-logo--' + key
        label = escape(logo['label'])
        logos.append(
            f'<span class="{logo_class}" title="{label}">'
            f'<img src="{assets}{escape(logo["image"])}" alt="{label}" loading="lazy" decoding="async"></span>'
        )
    return f'<div class="member-lab-logos">{"".join(logos)}</div>' if logos else ''


def flagged_affiliation(text, country, fr, assets, member=None):
    member = member or {}
    flag = ''
    if country not in member.get('hide_country_flags', ()):
        label = {'ca': 'Canada', 'fr': 'France'}[country]
        description = ('Pays de l’institution : ' if fr else 'Institution country: ') + label
        flag = (f'<img class="institution-flag" src="{assets}flags/{country}.svg" '
                f'alt="{description}" title="{description}">')
    label = escape(text)
    if 'Mila' in text:
        label = label.replace('Mila', mila_logo(assets))
    neuro_name = 'Le Neuro' if fr else 'The Neuro'
    if neuro_name in text:
        neuro_alt = escape(neuro_name + ' — Montreal Neurological Institute-Hospital')
        neuro_mark = (
            f'<img class="neuro-wordmark" '
            f'src="{assets}partners/neuro.png" '
            f'alt="{neuro_alt}" title="{neuro_alt}" loading="lazy" decoding="async">'
        )
        label = label.replace(escape(neuro_name), neuro_mark)
    if country == 'ca' and 'livia' in member.get('lab_logos', ()) and 'ÉTS' in text:
        logo = LAB_LOGOS['livia']
        alt = escape(logo['label'])
        inline_logo = (
            f'<span class="member-lab-logo member-lab-logo--inline" title="{alt}">'
            f'<img src="{assets}{escape(logo["image"])}" alt="{alt}" '
            f'loading="lazy" decoding="async"></span>'
        )
        label = label.replace('ÉTS', 'ÉTS' + inline_logo, 1)
    return f'<span class="institution-group">{flag}{label}</span>'


def affiliation_for(member, fr, assets):
    groups = {}
    for institution in member['affiliation'].split(' · '):
        country = INSTITUTION_COUNTRIES[institution]
        if fr:
            institution = {'McGill University': 'Université McGill',
                           'The Neuro': 'Le Neuro'}.get(institution, institution)
        groups.setdefault(country, []).append(institution)
    labels = []
    for country, names in groups.items():
        if labels and country in member.get('hide_country_flags', ()):
            labels.append('·')
        labels.append(flagged_affiliation(' · '.join(names), country, fr, assets, member))
    return ' '.join(labels)


def profile_card(member, fr, assets):
    given_names, surname = (escape(part) for part in member['name'].rsplit(' ', 1))
    role = escape(member['role'][fr])
    affiliation = affiliation_for(member, fr, assets)
    image = escape(member['image'])
    bio = member.get('biography')
    profile = 'people/' + escape(bio['slug']) + '.html' if bio else escape(member['profile'])
    card_id = f' id="{escape(bio["slug"])}"' if bio else ''
    arrow = '→' if bio else '↗'
    leadership = 'leadership_order' in member
    card_class = 'member-card leader-card' if leadership else 'member-card'
    publications = member_link(member['name']) if member['status'] != 'current' else None
    label = ('Publications de ' if fr else 'Publications by ') + member['name']
    paper_link = (f'<a class="member-publications" href="{escape(publications)}" aria-label="{escape(label)}">Publications</a>'
                  if publications else '')
    return f'''
      <li class="{card_class}"{card_id}>
        <img class="member-photo" src="{assets}people/{image}" width="184" height="184"
             loading="lazy" decoding="async" alt="">
        <div class="member-info">
          <h3><a href="{profile}">{given_names} <span class="name-tail">{surname}<span class="profile-arrow" aria-hidden="true">{arrow}</span></span></a></h3>
          <p class="member-role">{role}</p>
          <p class="member-affiliation">{affiliation}</p>{lab_logo_links(member, assets)}{paper_link}
        </div>
      </li>'''


def render_profile(member, fr, prefix):
    bio = member['biography']
    def t(en, french):
        return french if fr else en
    assets = escape(f'{prefix}assets/')
    appointments = ''.join(f'<li>{flagged_affiliation(pair[fr], pair[2], fr, assets, member)}</li>'
                           for pair in bio.get('appointments', []))
    if not appointments:
        appointments = f'<li>{affiliation_for(member, fr, assets)}</li>'
    membership = t('ILLS member', 'Membre de l’ILLS')
    if member['status'] == 'associate':
        membership = t('ILLS associate member', 'Membre associé de l’ILLS')
    role = member['role'][fr]
    if 'leadership_order' in member:
        role += t(', ILLS', ' de l’ILLS')
    topics = ''.join(f'<li>{escape(pair[fr])}</li>' for pair in bio['topics'])
    website_label = bio.get('website_label', ['Personal website', 'Site personnel'])[fr]
    profiles = [(escape(website_label), bio.get('website', member['profile'])),
                ('Google Scholar', bio.get('scholar')), ('LinkedIn', bio.get('linkedin'))]
    links = ''.join(f'<li><a href="{escape(url)}">{label} <span aria-hidden="true">↗</span></a></li>'
                    for label, url in profiles if url)
    papers = member_link(member['name'], '../')
    if papers:
        label = t('ILLS publications', 'Publications à l’ILLS')
        links += f'<li><a href="{escape(papers)}">{label} <span aria-hidden="true">→</span></a></li>'
    return f'''
      <article class="researcher-profile">
        <header class="researcher-head"><div class="wrap">
          <a class="researcher-back" href="../people.html#{escape(bio['slug'])}"><span aria-hidden="true">←</span> {t('People', 'Équipe')}</a>
          <div class="researcher-identity">
            <img src="{prefix}assets/people/{escape(member['image'])}" alt="" width="192" height="192">
            <div><p class="eyebrow">{membership}</p>
              <h1>{escape(member['name'])}</h1>
              <p class="researcher-role">{escape(role)}</p>
              <ul class="researcher-appointments">{appointments}</ul>
              {lab_logo_links(member, assets)}
            </div>
          </div>
        </div></header>
        <div class="wrap researcher-body">
          <section aria-labelledby="biography"><h2 id="biography">{t('Biography', 'Biographie')}</h2>
            <p class="researcher-bio">{escape(bio['text'][fr])}</p>
            <h3 class="micro">{t('Research topics', 'Thèmes de recherche')}</h3>
            <ul class="researcher-topics">{topics}</ul>
          </section>
          <aside aria-labelledby="profiles"><h2 id="profiles">{t('Find me online', 'Liens professionnels')}</h2>
            <ul class="researcher-links">{links}</ul>
          </aside>
        </div>
      </article>'''


def student_card(student, fr, assets):
    name = escape(student['name'])
    heading = name
    if student.get('website'):
        first, last = name.rsplit(' ', 1)
        heading = (f'<a href="{escape(student["website"])}">{first} <span class="name-tail">{last}'
                   '<span class="profile-arrow" aria-hidden="true">↗</span></span></a>')
    if student.get('image'):
        portrait = (f'<img class="member-photo" src="{assets}students/{escape(student["image"])}" '
                    'width="184" height="184" loading="lazy" decoding="async" alt="">')
    else:
        words = student['name'].split()
        initials = escape(words[0][0] + words[-1][0])
        portrait = f'<span class="member-photo student-initials" aria-hidden="true">{initials}</span>'
    institutions = []
    for country, institution in student['institutions']:
        if institution == student.get('supervising_partner'):
            institution += ' (codirection)' if fr else ' (co-supervision)'
        if fr and institution == 'McGill University':
            institution = 'Université McGill'
        institutions.append(flagged_affiliation(institution, country, fr, assets))
    supervisors = ', '.join(escape(advisor) for advisor in student['advisors'])
    badge = ''
    if student.get('mila_profile'):
        badge = f'<a href="{escape(student["mila_profile"])}" class="student-mila">{mila_logo(assets)}</a>'
    linkedin = ''
    if student.get('linkedin'):
        linkedin = (f'<a class="student-profile-link" href="{escape(student["linkedin"])}" '
                    f'aria-label="LinkedIn · {name}">LinkedIn <span aria-hidden="true">↗</span></a>')
    return f'''
      <li class="member-card student-card">
        {portrait}
        <div class="member-info">
          <h4>{heading}</h4>
          <p class="member-role">{escape(student['topic'][fr])}</p>
          <p class="member-affiliation">{' '.join(institutions)}</p>{badge}
          <p class="student-advisors"><strong>{'Codirection' if fr else 'Co-advisors'}</strong> {supervisors}</p>{linkedin}
        </div>
      </li>'''


def render(fr: bool, prefix: str) -> str:
    assets = escape(f'{prefix}assets/')
    title = 'Équipe' if fr else 'People'
    current_title = 'Membres' if fr else 'Members'
    associate_title = 'Membres associés' if fr else 'Associate members'
    past_title = 'Anciens membres' if fr else 'Past members'
    student_title = 'Étudiantes et étudiants' if fr else 'Students'
    visitors_title = 'Chercheuses et chercheurs invités' if fr else 'Visiting researchers'
    team_alt = (
        'Les membres de l’ILLS posent sur plusieurs rangs dans un escalier baigné de lumière.'
        if fr else 'Members of ILLS stand together in rows on a sunlit staircase.'
    )
    current = [member for member in MEMBERS if member['status'] == 'current']
    associates = [member for member in MEMBERS if member['status'] == 'associate']
    past = [member for member in MEMBERS if member['status'] == 'past']
    visiting = [member for member in MEMBERS if member['status'] == 'visiting']
    doctoral_names = {student['name'].casefold() for student in STUDENTS}
    other_students = [m for m in MEMBERS if m['status'] == 'student' and m['name'].casefold() not in doctoral_names]
    student_groups = []
    for kind, title_en, title_fr in [('cotutelle', 'Joint doctorates (cotutelle)', 'Doctorats en cotutelle'),
                                     ('co-advised', 'Co-advised doctorates', 'Doctorats en codirection')]:
        group = ''.join(student_card(s, fr, assets) for s in STUDENTS if s['type'] == kind)
        student_groups.append(f'<h3 class="student-group-heading">{title_fr if fr else title_en}</h3>'
                              f'<ul class="directory-grid student-grid">{group}</ul>')
    leaders = sorted((m for m in current if 'leadership_order' in m), key=lambda m: m['leadership_order'])
    researchers = [m for m in current if 'leadership_order' not in m]

    def cards(members):
        return ''.join(profile_card(member, fr, assets) for member in members)

    def directory_grid(members):
        return f'<ul class="directory-grid">{cards(members)}</ul>' if members else ''

    visiting_names = {member['name'].casefold() for member in visiting}
    listed_visitors = [visitor for visitor in VISITORS if visitor['name'].casefold() not in visiting_names]
    visitor_links = ''.join(
        f'<li><a href="{escape(visitor["website"])}">{escape(visitor["name"])}'
        ' <span class="profile-arrow" aria-hidden="true">↗</span></a></li>'
        for visitor in listed_visitors
    )

    return f'''
      <div class="wrap team-block">
        <header id="team" class="team-portrait">
          <div>
            <h1>{title}</h1>
            <nav class="directory-nav" aria-label="{'Annuaire' if fr else 'Member directory'}">
              <a href="#current-members">{current_title} <span aria-hidden="true">↓</span></a>
              <a href="#associate-members">{associate_title} <span aria-hidden="true">↓</span></a>
              <a href="#past-members">{past_title} <span aria-hidden="true">↓</span></a>
              <a href="#students">{student_title} <span aria-hidden="true">↓</span></a>
              <a href="#visiting-researchers">{visitors_title} <span aria-hidden="true">↓</span></a>
            </nav>
          </div>
          <img src="{assets}photos/ills-team-2024-800.webp"
               srcset="{assets}photos/ills-team-2024-800.webp 800w, {assets}photos/ills-team-2024-1600.webp 1600w"
               sizes="(max-width: 740px) 92vw, (min-width: 1600px) 1000px, 64vw"
               width="1600" height="1067" alt="{team_alt}" fetchpriority="high" decoding="async">
        </header>
      </div>
      <section class="section directory-section" aria-labelledby="current-members"><div class="wrap">
        <h2 id="current-members">{current_title} <span class="member-count">({len(current)})</span></h2>
        <ul class="directory-grid">{cards(researchers)}
        </ul>
        <div id="leadership-heading" class="leaders">
          <ul class="leadership-grid" aria-label="{'Direction du laboratoire' if fr else 'Laboratory leadership'}">{cards(leaders)}
          </ul>
        </div>
      </div></section>
      <section class="section directory-section" aria-labelledby="associate-members"><div class="wrap">
        <h2 id="associate-members">{associate_title} <span class="member-count">({len(associates)})</span></h2>
        <ul class="directory-grid">{cards(associates)}
        </ul>
      </div></section>
      <section class="section directory-section past-directory" aria-labelledby="past-members"><div class="wrap">
        <h2 id="past-members">{past_title} <span class="member-count">({len(past)})</span></h2>
        <ul class="directory-grid">{cards(past)}
        </ul>
      </div></section>
      <section class="section directory-section" aria-labelledby="students"><div class="wrap">
        <h2 id="students">{student_title} <span class="member-count">({len(STUDENTS) + len(other_students)})</span></h2>
        {''.join(student_groups)}
        {directory_grid(other_students)}
      </div></section>
      <section class="section directory-section" aria-labelledby="visiting-researchers"><div class="wrap" id="visitors">
        <h2 id="visiting-researchers">{visitors_title} <span class="member-count">({len(visiting) + len(listed_visitors)})</span></h2>
        {directory_grid(visiting)}
        <ul class="visitor-list">{visitor_links}</ul>
      </div></section>'''
