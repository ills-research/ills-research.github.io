"""Laboratory and visitor information for the Overview page."""


def render(fr: bool, prefix: str) -> str:
    if fr:
        title = 'Un laboratoire commun à Montréal'
        mission = ('Créé en 2022, l’ILLS réunit des équipes de France et du Québec à l’ÉTS. '
                   'Leurs recherches portent sur la prise de décision en temps réel et sur la façon dont les systèmes '
                   'autonomes réagissent lorsque les conditions changent. Elles associent le traitement du signal '
                   'et l’apprentissage automatique pour étudier la parole, le langage et la vision par ordinateur.')
        cnrs_url = 'https://ottawa.office.cnrs.fr/recherche/international-laboratory-on-learning-systems-2/'
        cnrs_link = 'Le laboratoire sur le site du CNRS'
        leadership = ('<a href="people/pablo-piantanida.html">Pablo Piantanida</a> est directeur de l’ILLS '
                      'et <a href="people/mark-coates.html">Mark Coates</a> en est le codirecteur.')
    else:
        title = 'A shared lab in Montréal'
        mission = ('Founded in 2022, ILLS brings researchers from France and Québec together at ÉTS. '
                   'They study how machines make decisions in real time and how autonomous systems respond '
                   'when conditions change. Their work brings signal processing and machine learning '
                   'to questions in speech, language and computer vision.')
        cnrs_url = 'https://ottawa.office.cnrs.fr/en/research/international-laboratory-on-learning-systems-2/'
        cnrs_link = 'Laboratory profile at CNRS'
        leadership = ('<a href="people/pablo-piantanida.html">Pablo Piantanida</a> is the Director of ILLS '
                      'and <a href="people/mark-coates.html">Mark Coates</a> is the Co-Director.')
    return f"""
      <section id="laboratory" class="section lab-feature" aria-labelledby="mission-heading"><div class="wrap feature-grid">
        <figure><div class="lab-photo"><img src="{prefix}assets/images/pavillon-f.jpg" width="1600" height="982"
          alt="{'Extérieur du pavillon F de l’ÉTS à Montréal' if fr else 'Exterior of ÉTS Pavilion F in Montréal'}" loading="lazy"></div>
          <figcaption class="photo-caption">{'PAVILLON F' if fr else 'PAVILION F'} · ÉTS MONTRÉAL</figcaption></figure>
        <div class="feature-copy"><p class="eyebrow">{'Le laboratoire' if fr else 'The laboratory'}</p>
          <h2 id="mission-heading">{title}</h2><p>{mission}</p>
          <div id="team" class="home-leadership"><h3 id="leadership-heading">{'Direction' if fr else 'Leadership'}</h3>
            <p>{leadership}</p></div>
          <a class="link-arrow" href="{cnrs_url}">{cnrs_link} <span aria-hidden="true">↗</span></a>
        </div></div></section>"""


def render_contact(fr: bool, prefix: str) -> str:
    heading = 'Nous joindre' if fr else 'Visit and contact'
    office = 'Bureaux de Montréal' if fr else 'Montréal office'
    floor = 'Pavillon F, 5ᵉ étage' if fr else 'Pavillon F, 5th floor'
    street = '1132, rue William' if fr else '1132 rue William'
    city = 'Montréal (Québec) H3C 1P8, Canada' if fr else 'Montréal, Québec H3C 1P8, Canada'
    email_heading = 'Secrétariat de l’ILLS' if fr else 'ILLS secretariat'
    email_copy = 'Pour organiser une visite ou prendre contact avec le laboratoire.' if fr else 'For visits and general enquiries about the laboratory.'
    alt = 'Entrée vitrée de l’ILLS au pavillon F de l’ÉTS.' if fr else 'Glass entrance to the ILLS laboratory at ÉTS Pavilion F.'
    return f"""
      <section id="contact" class="section contact-box" aria-labelledby="contact-heading"><div class="wrap feature-grid">
        <div><h2 id="contact-heading">{heading}</h2><div class="contact-grid">
          <div><h3>{office}</h3><address>École de technologie supérieure<br>{floor}<br>{street}<br>{city}</address></div>
          <div><h3>{email_heading}</h3><p>{email_copy}</p>
            <a class="text-link" href="mailto:secretariat-ills@etsmtl.ca">secretariat-ills@etsmtl.ca</a></div>
        </div></div><div class="lab-photo"><img src="{prefix}assets/images/ills-entrance.jpg" width="1600" height="1200"
          loading="lazy" alt="{alt}"></div>
      </div></section>"""
