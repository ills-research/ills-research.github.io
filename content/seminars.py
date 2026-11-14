"""Render the ILLS seminar series in both editions of the Events page."""
import json
from datetime import date
from html import escape
from pathlib import Path

SEMINARS = json.loads(Path(__file__).with_name('seminars.json').read_text(encoding='utf-8'))
SPEAKER_PORTRAITS = json.loads(
    Path(__file__).with_name('seminar_speaker_portraits.json').read_text(encoding='utf-8')
)
MEMBERS = json.loads(Path(__file__).with_name('members.json').read_text(encoding='utf-8'))
STUDENTS = json.loads(Path(__file__).with_name('students.json').read_text(encoding='utf-8'))
MONTHS = {
    'en': 'January February March April May June July August September October November December'.split(),
    'fr': 'janvier février mars avril mai juin juillet août septembre octobre novembre décembre'.split(),
}
FORMATS = {
    'in-person': ('In person', 'En présentiel'),
    'online': ('Online', 'En ligne'),
    'hybrid': ('In person and online', 'En présentiel et en ligne'),
    'remote-speaker': ('Remote talk with a group viewing at ILLS', 'À distance avec retransmission à l’ILLS'),
}


def _initials(name):
    parts = name.replace('-', ' ').split()
    return ''.join(part[0] for part in (parts[0], parts[-1]) if part).upper()


def _member_portrait(name, prefix):
    lookup_name = 'Héber H. Arcolezi' if name == 'Héber Hwang Arcolezi' else name
    person = next((item for item in MEMBERS if item.get('name') == lookup_name), None)
    folder = 'people'
    if person is None:
        person = next((item for item in STUDENTS if item.get('name') == name), None)
        folder = 'students'
    if not person or not person.get('image'):
        return None
    image_path = Path(__file__).parent.parent / 'site' / 'assets' / folder / person['image']
    if not image_path.is_file():
        return None
    return {
        'image': f'{prefix}assets/{folder}/{person["image"]}',
        'profile': person.get('profile') or person.get('website') or person.get('portrait_source'),
    }


def render_speakers(talk, prefix, fr):
    people = []
    for name in talk['speaker'].split(' · '):
        person = _member_portrait(name, prefix) or SPEAKER_PORTRAITS.get(name, {})
        initials = escape(_initials(name))
        safe_name = escape(name)
        profile = person.get('profile')
        if person.get('image'):
            image = f'<img class="seminar-speaker-avatar" src="{escape(person["image"], quote=True)}" alt="" width="56" height="56" loading="lazy" decoding="async">'
            label = 'Ouvrir le profil de' if fr else 'Open profile for'
            content = f'<span class="seminar-speaker-avatar-wrap"><span class="seminar-speaker-initials" aria-hidden="true">{initials}</span>{image}</span><span class="seminar-speaker-name">{safe_name}</span>'
            if profile:
                people.append(f'<a class="seminar-speaker-person" href="{escape(profile, quote=True)}" aria-label="{label} {safe_name}">{content}</a>')
            else:
                people.append(f'<span class="seminar-speaker-person">{content}</span>')
        else:
            avatar = f'<span class="seminar-speaker-avatar seminar-speaker-initials" aria-hidden="true">{initials}</span>'
            content = f'{avatar}<span class="seminar-speaker-name">{safe_name}</span>'
            if profile:
                label = 'Ouvrir le profil de' if fr else 'Open profile for'
                people.append(f'<a class="seminar-speaker-person" href="{escape(profile, quote=True)}" aria-label="{label} {safe_name}">{content}</a>')
            else:
                people.append(f'<span class="seminar-speaker-person">{content}</span>')
    return '<div class="seminar-speakers" aria-label="Speakers">' + ''.join(people) + '</div>'


def render_talk(talk, fr, prefix):
    lang = 'fr' if fr else 'en'
    day = date.fromisoformat(talk['date'])
    day_label = '1ᵉʳ' if fr and day.day == 1 else str(day.day)
    date_label = f"{day_label} {MONTHS[lang][day.month - 1]} {day.year}"
    time = talk.get('time', '')
    when = talk['date']
    if time:
        when += 'T' + time
        date_label += ' · ' + time
    format_line = f'<p>{FORMATS[talk["format"]][fr]}</p>' if 'format' in talk else ''
    if 'abstract' in talk:
        label = 'Résumé (en anglais)' if fr else 'Abstract'
        paragraphs = talk['abstract']
        body_lang = 'en'
    else:
        label = 'Présentation du sujet' if fr else 'Research overview'
        paragraphs = [talk['overview'][lang]]
        body_lang = lang
    bio_label = 'Biographie' if fr else 'Speaker bio'
    summary = f'{label} et biographie' if fr else f'{label} and speaker bio'
    body = ''.join(f'<p>{escape(p)}</p>' for p in paragraphs)
    links = ''.join(f'<a href="{escape(ref["url"])}">{escape(ref[lang])}</a>'
                    for ref in talk.get('references', ()))
    references = f'<div class="seminar-references">{links}</div>' if links else ''
    return f"""
      <li class="notice-row seminar-talk" id="{escape(talk['id'])}" data-start="{when[:10]}" data-time="{time}">
        <div class="notice-meta"><p><time datetime="{when}">{date_label}</time></p>{format_line}</div>
        <div class="notice-copy">
          {render_speakers(talk, prefix, fr)}
          <h4 lang="en">{escape(talk['title'])}</h4>
          <details><summary>{summary}</summary>
            <h5>{label}</h5><div lang="{body_lang}">{body}</div>
            <h5>{bio_label}</h5><p>{escape(talk['bio'][lang])}</p>{references}
          </details>
        </div>
      </li>"""


def render(fr, today, prefix=''):
    # Stable date sorting keeps consecutive talks on one day in programme order.
    by_time = sorted(SEMINARS, key=lambda talk: talk.get('time', ''))
    upcoming = sorted((t for t in by_time if t['date'] >= today), key=lambda t: t['date'])
    past = sorted((t for t in by_time if t['date'] < today), key=lambda t: t['date'], reverse=True)
    groups = (
        ('upcoming-seminars', 'Séminaires à venir' if fr else 'Upcoming seminars', upcoming),
        ('past-seminars', 'Séminaires passés' if fr else 'Past seminars', past),
    )
    sections = []
    for slug, title, talks in groups:
        rows = ''.join(render_talk(talk, fr, prefix) for talk in talks)
        sections.append(f'''<section id="{slug}" class="seminar-group" aria-labelledby="{slug}-heading"{'' if rows else ' hidden'}>
            <h3 id="{slug}-heading">{title}</h3><ul class="notice-list">{rows}</ul></section>''')
    zone = 'Les horaires sont indiqués à l’heure de Montréal.' if fr else 'All times are local to Montréal.'
    return f'''<section id="seminars" class="notice-section calendar-section" aria-labelledby="seminars-heading">
        <h2 id="seminars-heading">{'Séminaires' if fr else 'Seminars'}</h2>
        <p class="seminar-zone">{zone}</p>{''.join(sections)}</section>'''
