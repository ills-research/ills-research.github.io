"""Partner directory in English and French."""

from html import escape


# Mark, English and French names, and the institution's localized homepages.
CORE_PARTNERS = {
    "Québec, Canada": (
        ("mcgill", "McGill University", "Université McGill",
         "https://www.mcgill.ca/", "https://www.mcgill.ca/fr"),
        ("ets", "École de technologie supérieure", "École de technologie supérieure",
         "https://www.etsmtl.ca/en", "https://www.etsmtl.ca/"),
    ),
    "France": (
        ("cnrs", "French National Centre for Scientific Research",
         "Centre national de la recherche scientifique",
         "https://www.cnrs.fr/en", "https://www.cnrs.fr/fr"),
        ("paris-saclay", "Université Paris-Saclay", "Université Paris-Saclay",
         "https://www.universite-paris-saclay.fr/en", "https://www.universite-paris-saclay.fr/"),
        ("centralesupelec", "CentraleSupélec", "CentraleSupélec",
         "https://www.centralesupelec.fr/en", "https://www.centralesupelec.fr/"),
    ),
}

ASSOCIATED_PARTNERS = {
    "Québec, Canada": (
        ("mila", "Mila – Quebec AI Institute", "Mila – Institut québécois d’intelligence artificielle",
         "https://mila.quebec/en", "https://mila.quebec/fr"),
    ),
}

SUPPORT_PARTNERS = {
    "Québec, Canada": (
        ("frq", "Fonds de recherche du Québec (FRQ)", "Fonds de recherche du Québec (FRQ)",
         "https://frq.gouv.qc.ca/en/", "https://frq.gouv.qc.ca/"),
    ),
    "France": (
        ("dataia", "Institut DATAIA Paris-Saclay", "Institut DATAIA Paris-Saclay",
         "https://www.dataia.eu/en", "https://www.dataia.eu/"),
    ),
}


def render_groups(partners_by_region, fr: bool, prefix: str) -> str:
    groups = []
    for region, partners in partners_by_region.items():
        rows = []
        for mark, english_name, french_name, english_url, french_url in partners:
            name = french_name if fr else english_name
            url = french_url if fr else english_url
            rows.append(f"""
              <li><a class="network-partner" href="{escape(url)}">
                <span class="network-mark"><img src="{prefix}assets/partners/{mark}.png"
                  alt="" loading="lazy" decoding="async"></span>
                <span class="network-name">{escape(name)}</span>
                <span class="network-arrow" aria-hidden="true">↗</span>
              </a></li>""")
        groups.append(f"""
          <section class="network-group"><h3>{escape(region)}</h3>
            <ul>{''.join(rows)}</ul>
          </section>""")

    return ''.join(groups)


def render(fr: bool, prefix: str) -> str:
    core = 'Établissements partenaires principaux' if fr else 'Core Partner Institutions'
    associated = 'Établissements partenaires associés' if fr else 'Associated Partner Institutions'
    support = 'Établissements partenaires de soutien' if fr else 'Support Partners Institutions'
    return f"""
      <div id="partners" class="section network-directory"><div class="wrap">
        <section id="core-partners" aria-labelledby="partners-heading">
          <h2 id="partners-heading">{core}</h2>
          <div class="network-groups">{render_groups(CORE_PARTNERS, fr, prefix)}</div>
        </section>
        <section id="associated-partners" aria-labelledby="associated-partners-heading">
          <h2 id="associated-partners-heading">{associated}</h2>
          <div class="network-groups">{render_groups(ASSOCIATED_PARTNERS, fr, prefix)}</div>
        </section>
        <section id="support-partners" aria-labelledby="support-partners-heading">
          <h2 id="support-partners-heading">{support}</h2>
          <div class="network-groups">{render_groups(SUPPORT_PARTNERS, fr, prefix)}</div>
        </section>
      </div></div>"""
