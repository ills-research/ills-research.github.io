"""Bilingual calendar, research opportunities and laboratory news."""
from datetime import datetime
from html import escape
from zoneinfo import ZoneInfo

from . import seminars

CALENDAR_TITLE = ("Events", "Événements")
CALENDAR_INTRO = (
    "Lab seminars and workshops give researchers a place to discuss results while projects are underway.",
    "Les séminaires et les ateliers du laboratoire permettent aux équipes de discuter de leurs résultats en cours de projet.",
)
OPENINGS_TITLE = ("Openings", "Postes à pourvoir")
OPENINGS_INTRO = (
    "Research opportunities with ILLS members and their teams.",
    "Les possibilités de recherche au sein des équipes de l’ILLS.",
)
APPLICATIONS_TITLE = ("CNRS mobility", "Mobilité CNRS")
APPLICATIONS_INTRO = (
    "The International Laboratory on Learning Systems (ILLS, CNRS IRL 2020) welcomes enquiries from researchers interested in collaborating with our team in Montréal. The application route depends on your current position.",
    "Vous souhaitez mener un projet de recherche avec l’équipe de l’International Laboratory on Learning Systems (ILLS, IRL 2020 du CNRS) à Montréal ? La démarche dépend de votre statut actuel.",
)
NEWS_TITLE = ("News", "Actualités")
NEWS_INTRO = (
    "Updates from the International Laboratory on Learning Systems and its partners.",
    "Les nouvelles de l’ILLS et de ses partenaires.",
)

CALENDAR = [
    {
        "id": "workshop-nlp-2024",
        "kind": ("Workshop", "Atelier"),
        "start": "2024-10-01",
        "end": "2024-10-03",
        "date": ("1–3 October 2024", "Du 1ᵉʳ au 3 octobre 2024"),
        "details": ("Mila · Montréal", "Mila · Montréal"),
        "title": (
            "France–Québec workshop on language processing in the age of generative AI",
            "Atelier France–Québec sur le traitement du langage à l’ère de l’IA générative",
        ),
        "summary": (
            "ILLS and Mila co-organized this three-day meeting with CNRS, GDR TAL, FRQNT and IVADO. Researchers from France and Québec explored how language models handle languages with little training data, what human language development can teach us about AI, and when people rely too heavily on conversational systems.",
            "Pendant trois jours à Mila, des équipes de France et du Québec ont discuté des modèles génératifs pour le traitement du langage, des apports des sciences cognitives à l’étude de son apprentissage et des effets de ces technologies sur la société.",
        ),
        "link": ("Workshop programme at Mila", "Programme de l’atelier sur le site de Mila"),
        "url": (
            "https://mila.quebec/en/event/workshop-nlp-in-the-era-of-generative-ai-cognitive-sciences-and-societal-transformation",
            "https://mila.quebec/fr/evenement/atelier-le-traitement-du-langage-naturel-nlp-a-lere-de-lia-generative-des-sciences",
        ),
        "featured_en": {
            "organizers": "Pablo Piantanida, Frédéric Béchet and Jackie Cheung",
            "programme": [
                ("1 October", "Generative models and multilingual NLP"),
                ("2 October", "How humans and machines learn language"),
                ("3 October", "Conversational AI and its impact on society"),
            ],
        },
    },
    {
        "id": "ai4h-2026",
        "kind": ("Workshop",),
        "start": "2026-02-18", "end": "2026-02-20",
        "date": ("18–20 February 2026",),
        "details": ("ÉTS · Montréal",),
        "title": ("AI4H 2026 — Artificial Intelligence for Healthcare Applications",),
        "summary": ("ILLS, ÉTS and LAMIH co-organized this three-day workshop. Researchers and clinicians discussed how AI can guide rehabilitation, help surgeons interpret images during operations, and reveal patterns in brain scans.",),
        "link": ("View the workshop programme",),
        "url": ("https://ai4h2026.sciencesconf.org/resource/page/id/4",),
    },
    {
        "id": "medical-imaging-2023",
        "kind": ("Workshop",),
        "start": "2023-10-16",
        "date": ("16 October 2023",),
        "details": ("ÉTS · Montréal",),
        "title": ("Medical Imaging with Deep Learning",),
        "summary": ("This ILLS workshop examined how to segment medical images, how reliably a model performs on unfamiliar data, and how to evaluate its predictions in a clinical setting.",),
    },
    {
        "id": "fairness-privacy-law-2023",
        "kind": ("Workshop",),
        "start": "2023-12-01",
        "date": ("1 December 2023",),
        "details": ("ÉTS · Montréal",),
        "title": ("Fairness, Privacy, Securing AI and Law",),
        "summary": ("Researchers in machine learning and law discussed how to assess algorithmic fairness, audit privacy risks and use the findings to inform AI governance.",),
        "photos": [
            {"file": "fairness-privacy-law-2023.webp", "size": (1200, 663),
             "alt": ("Workshop banner above two photos of participants discussing AI and law around tables at ÉTS Montréal.",)},
        ],
    },
    {
        "id": "ills-workshop-2024",
        "kind": ("Workshop",),
        "start": "2024-09-09", "end": "2024-09-10",
        "date": ("9–10 September 2024",),
        "details": ("ÉTS · Montréal",),
        "title": ("ILLS Workshop 2024",),
        "summary": ("Students presented their research in short talks and poster sessions at the lab’s annual meeting. Invited talks covered explainable AI, neuroscience and scheduling.",),
        "photos": [
            {"file": "ills-workshop-2024-discussion.webp", "size": (900, 415),
             "alt": ("Workshop participants talking in small groups around tables.",)},
            {"file": "ills-workshop-2024-roundtable.webp", "size": (900, 584),
             "alt": ("A participant gestures with a pen during a workshop discussion.",)},
        ],
        "link": ("Workshop programme",),
        "url": ("https://sites.google.com/view/irl-ills-workshop2024/home",),
    },
    {
        "id": "large-scale-scheduling-2025",
        "kind": ("Workshop",),
        "start": "2025-07-08", "end": "2025-07-10",
        "date": ("8–10 July 2025",),
        "details": ("ÉTS · Montréal",),
        "title": ("18th Scheduling for Large-Scale Systems Workshop",),
        "summary": ("The workshop explored how to allocate GPUs among competing jobs, distribute the work of training a model, and account for energy use when scheduling computations.",),
        "link": ("Workshop programme and slides",),
        "url": ("https://perso.ens-lyon.fr/loris.marchal/scheduling-in-montreal/",),
    },
    {
        "id": "bellairs-workshop-2025",
        "kind": ("Workshop",),
        "start": "2025-12",
        "date": ("December 2025",),
        "details": ("Bellairs Research Institute · Holetown, Barbados",),
        "title": ("ILLS Workshop at Bellairs",),
        "summary": ("ILLS researchers met at McGill University’s Bellairs Research Institute to discuss machine learning on graphs and statistical signal processing.",),
        "photos": [
            {"file": "bellairs-workshop-2025.jpg?v=2", "size": (720, 542),
             "alt": ("Workshop participants gathered outdoors at the Bellairs Research Institute in Barbados.",)},
            {"file": "bellairs-brace-building.webp", "size": (900, 675),
             "alt": ("A garden path leads to the Brace Building at the Bellairs Research Institute.",),
             "credit": "McGill University", "source": "https://www.mcgill.ca/bellairs/media-gallery/detail/616/45"},
        ],
    },
]

CNRS_VISIT_ARTICLES = (
    "https://ottawa.office.cnrs.fr/en/cnrs-computer-sciences-in-montreal/",
    "https://ottawa.office.cnrs.fr/visite-de-cnrs-sciences-informatiques-a-montreal-irl-ills/",
)
CNRS_VISIT_2026 = {
    "id": "cnrs-computer-sciences-visit-2026",
    "kind": ("Institutional visit", "Visite institutionnelle"),
    "start": "2026-04",
    "date": ("April 2026", "Avril 2026"),
    "details": ("ÉTS · Montréal",) * 2,
    "title": ("CNRS Computer Sciences leadership visits ILLS", "La direction de CNRS Sciences informatiques en visite à l’ILLS"),
    "summary": (
        "Adeline Nazarenko and Jérôme Durand-Lose met ILLS researchers and students to discuss how the lab makes machine learning algorithms more reliable and safer to use. The delegation also met partners at IVADO, Mila, McGill and ÉTS.",
        "Adeline Nazarenko et Jérôme Durand-Lose ont échangé avec les membres de l’ILLS sur la fiabilité et la sûreté des algorithmes d’apprentissage. La délégation a aussi rencontré des partenaires à IVADO, à Mila, à McGill et à l’ÉTS.",
    ),
    "link": ("Read the CNRS account of the visit", "Lire le compte rendu du CNRS"),
    "url": CNRS_VISIT_ARTICLES,
    "photos": [
        {"file": "cnrs-visit-ets-2026.webp", "size": (1024, 768),
         "alt": ("The CNRS delegation and its hosts stand in front of flags at ÉTS Montréal.",
                 "La délégation du CNRS et ses hôtes devant les drapeaux à l’ÉTS, à Montréal."),
         "place": "ÉTS Montréal", "credit": "Andréa Dessen", "source": CNRS_VISIT_ARTICLES[0]},
        {"file": "cnrs-visit-mila-2026.jpg", "size": (1024, 768),
         "alt": ("Three participants stand beside the purple Mila logo during the CNRS visit.",
                 "Trois personnes posent devant le logo violet de Mila lors de la visite du CNRS."),
         "place": "Mila", "source_label": "CNRS Ottawa", "source": CNRS_VISIT_ARTICLES[0]},
    ],
}
PAVILION_OPENING_ARTICLE = "https://www.etsmtl.ca/actualites/lets-inaugure-son-nouveau-pavillon-consacre-design-lia"
PAVILION_OPENING_2025 = {
    "id": "pavilion-f-inauguration-2025",
    "kind": ("Lab milestone", "Vie du laboratoire"),
    "start": "2025-12-01",
    "date": ("1 December 2025", "1ᵉʳ décembre 2025"),
    "details": ("Pavilion F, ÉTS · Montréal", "Pavillon F, ÉTS · Montréal"),
    "title": ("ÉTS inaugurates Pavilion F, home to ILLS", "L’ÉTS inaugure le pavillon F, qui accueille l’ILLS"),
    "summary": (
        "Québec minister Martine Biron attended the opening of Pavilion F. ILLS researchers and students had moved into their dedicated space in the building earlier that year.",
        "La ministre québécoise Martine Biron a assisté à l’inauguration du pavillon F. L’équipe de l’ILLS y occupait ses nouveaux locaux depuis plusieurs mois.",
    ),
    "link": ("Read the ÉTS announcement (in French)", "Lire l’annonce de l’ÉTS"),
    "url": (PAVILION_OPENING_ARTICLE,) * 2,
    "photos": [
        {"file": "ets-pavilion-f-inauguration-2025.webp", "size": (1900, 1267),
         "alt": ("Kathy Baig, Martine Biron, Nicolas Douay and Guillaume Blum at the ribbon-cutting for Pavilion F.",
                 "Kathy Baig, Martine Biron, Nicolas Douay et Guillaume Blum lors de la coupe du ruban au pavillon F."),
         "credit": "ÉTS Montréal", "source": PAVILION_OPENING_ARTICLE},
        {"file": "ets-pavilion-f-audience-2025.jpg", "size": (1024, 771),
         "alt": ("Guests sit and stand near research posters in the ILLS space during the opening of Pavilion F.",
                 "Des invités, assis et debout près d’affiches scientifiques, assistent à l’inauguration du pavillon F dans les locaux de l’ILLS.")},
    ],
}

NEWS = [CNRS_VISIT_2026, PAVILION_OPENING_2025]

INSTITUTIONAL_EVENTS = [
    CNRS_VISIT_2026,
    PAVILION_OPENING_2025,
    {
        "id": "cnrs-delegation-visit-2023",
        "kind": ("Institutional visit",),
        "start": "2023-11",
        "date": ("November 2023",),
        "details": ("ÉTS · Montréal",),
        "title": ("CNRS delegation visits ILLS at ÉTS Montréal",),
        "summary": ("Alain Schuhl and Christelle Roy met Pablo Piantanida, Mark Coates and members of the lab. Researchers and students presented their work through posters and lab tours and discussed future joint projects with the delegation.",),
        "link": ("Read the CNRS account of the visit (in French)",),
        "url": ("https://ottawa.office.cnrs.fr/visite-delegation-cnrs-quebec-sherbrooke-montreal/",),
        "photos": [
            {"file": "cnrs-visit-ets-2023.webp", "size": (743, 458),
             "alt": ("CNRS delegates sit across the table from Pablo Piantanida, Mark Coates and their colleagues at ÉTS Montréal.",),
             "credit": "ÉTS", "source": "https://ottawa.office.cnrs.fr/en/cnrs-delegation-visits-quebec-to-strengthen-strategic-collaborations/"},
            {"file": "cnrs-delegation-ets-group-2023.webp", "size": (1200, 675),
             "alt": ("The CNRS delegation and their hosts pose in front of the Direction générale sign at ÉTS Montréal.",)},
        ],
    },
    {
        "id": "sylvie-retailleau-visit-2023",
        "kind": ("Institutional visit",),
        "start": "2023-04-21",
        "date": ("21 April 2023",),
        "details": ("ÉTS · Montréal",),
        "title": ("France’s Minister of Higher Education and Research Sylvie Retailleau meets the ILLS team",),
        "summary": ("Sylvie Retailleau met ILLS researchers and students at ÉTS. Her visit to Canada coincided with the first meeting of the Canada–France Joint Committee on Science, Technology and Innovation.",),
        "link": ("View the French ministry’s visit programme (in French)",),
        "url": ("https://www.enseignementsup-recherche.gouv.fr/fr/deplacement-de-sylvie-retailleau-ministre-de-l-enseignement-superieur-et-de-la-recherche-au-canada-90491",),
        "photos": [
            {"file": "retailleau-2023-group.webp", "size": (960, 640),
             "alt": ("The visiting delegation and their hosts pose in front of flags in the ÉTS atrium.",)},
            {"file": "retailleau-2023-reception.webp", "size": (960, 640),
             "alt": ("Two participants hold a ribbon-tied folder during the reception at ÉTS.",)},
            {"file": "retailleau-2023-discussion.webp", "size": (960, 640),
             "alt": ("Three participants listen and smile during the laboratory visit.",)},
            {"file": "retailleau-2023-human-motion.webp", "size": (960, 640),
             "alt": ("A researcher shows visitors how AI can predict human motion, with a slide illustrating the movement of three figures.",)},
        ],
    },
]

OPENINGS = [
    {
        "date": ("Expected start in January 2027", "Début prévu en janvier 2027"),
        "details": ("ILLS and Mila · Montréal", "ILLS et Mila · Montréal"),
        "title": (
            "PhD in human-guided evaluation of generative AI",
            "Doctorat sur l’évaluation de l’IA générative guidée par l’expertise humaine",
        ),
        "summary": (
            "Work with Pablo Piantanida and Jackie Cheung on the REGARD project to design tests that reveal when generative AI systems fail. Applications are reviewed as they arrive until the position is filled.",
            "Sous la direction de Pablo Piantanida et de Jackie Cheung, la personne recrutée concevra, dans le cadre du projet REGARD, des tests pour repérer les défaillances des systèmes d’IA générative. Les candidatures sont étudiées au fil de leur réception jusqu’à ce que le poste soit pourvu.",
        ),
        "link": ("Position details and how to apply", "Détails du poste et modalités de candidature (en anglais)"),
        "url": ("https://pablo-piantanida.org/openings/phd-ai-evaluation/",) * 2,
    },
]


def render_entry(entry, fr, prefix):
    attributes = ''
    kind = ''
    date_text = escape(entry['date'][fr])
    if 'kind' in entry:
        start = entry['start']
        end = entry.get('end', start)
        attributes = f' id="{entry["id"]}" data-start="{start}" data-end="{end}"'
        if not fr and 'featured_en' in entry:
            return render_featured_workshop(entry, attributes)
        kind = f'<span class="notice-kind">{escape(entry["kind"][fr])}</span>'
        date_text = f'<time datetime="{start}">{date_text}</time>'
    link = ''
    if 'url' in entry:
        link = f'<a class="link-arrow" href="{escape(entry["url"][fr])}">{escape(entry["link"][fr])} <span aria-hidden="true">↗</span></a>'
    figures = []
    for photo in entry.get('photos', ()):
        width, height = photo['size']
        src = escape(prefix + 'assets/photos/' + photo['file'])
        caption = ''
        if 'credit' in photo:
            place = escape(photo['place']) + ' · ' if 'place' in photo else ''
            caption = f'<figcaption>{place}Photo © <a href="{escape(photo["source"])}">{escape(photo["credit"])}</a></figcaption>'
        elif 'source_label' in photo:
            caption = f'<figcaption>{escape(photo["place"])} · <a href="{escape(photo["source"])}">{escape(photo["source_label"])}</a></figcaption>'
        figures.append(
            f'<figure style="--photo-ratio: {width / height:.4f}">'
            f'<img src="{src}" alt="{escape(photo["alt"][fr])}" width="{width}" height="{height}" loading="lazy" decoding="async">'
            f'{caption}</figure>'
        )
    gallery = '<div class="event-photos">' + ''.join(figures) + '</div>' if figures else ''
    return f"""
      <li class="notice-row"{attributes}>
        <div class="notice-meta">{kind}<p>{date_text}</p><p>{escape(entry["details"][fr])}</p></div>
        <div class="notice-copy"><h3>{escape(entry["title"][fr])}</h3>
          <p>{escape(entry["summary"][fr])}</p>
          {link}{gallery}
        </div>
      </li>"""


def render_openings(fr, prefix):
    rows = ''.join(render_entry(item, fr, prefix) for item in OPENINGS)
    heading = "Offres de recherche" if fr else "Research positions"
    return render_listing(OPENINGS_TITLE[fr], OPENINGS_INTRO[fr], heading, rows)


def render_news(fr, prefix):
    items = sorted(NEWS, key=lambda item: item['start'], reverse=True)
    rows = ''.join(render_entry(item, fr, prefix) for item in items)
    heading = "Nouvelles du laboratoire" if fr else "Laboratory news"
    return render_listing(NEWS_TITLE[fr], NEWS_INTRO[fr], heading, rows)


def render_listing(title, intro, heading, rows):
    return f"""
      <header class="inner-hero"><div class="wrap">
        <h1>{escape(title)}</h1><p class="lead">{escape(intro)}</p>
      </div></header>
      <section class="section wrap notice-section" aria-labelledby="list-heading">
        <h2 id="list-heading">{escape(heading)}</h2>
        <ul class="notice-list">{rows}</ul>
      </section>"""


def render_applications(fr, prefix):
    if fr:
        title = "Rejoindre l’ILLS à Montréal avec le CNRS"
        directory_label = "L’ILLS dans le répertoire national des structures de recherche"
        institute_label = "L’ILLS auprès de CNRS Sciences informatiques"
        institute_url = "https://www.ins2i.cnrs.fr/fr/international-research-laboratory-irl-laboratoire-de-recherche-international"
        faculty = "Enseignantes-chercheuses et enseignants-chercheurs en France"
        delegation = "Accueil en délégation"
        eligibility = ("Si vous êtes maître ou maîtresse de conférences, professeur ou professeure des universités, "
                       "vous pouvez demander un accueil en délégation au CNRS pour mener un projet à l’ILLS. "
                       "Pendant la délégation, votre établissement continue de vous rémunérer et vous décharge de tout ou partie de votre service d’enseignement.")
        procedure = "Comment candidater"
        faculty_steps = ("Échangez en amont avec l’ILLS et votre laboratoire d’origine afin que les deux directions puissent formuler leur avis écrit. "
                         "Préparez un rapport d’activité comprenant votre CV, un projet de recherche de cinq pages maximum et une liste de dix productions scientifiques au plus. "
                         "Déposez votre dossier dans Galaxie en indiquant l’ILLS (IRL 2020) comme unité d’accueil. Votre établissement examine les dossiers et transmet au CNRS ceux qu’il soutient.")
        delegation_label = "Modalités de l’accueil en délégation au CNRS"
        galaxie_label = "Dossier de candidature et formulaires sur Galaxie"
        campaign = "Campagne 2027–2028"
        dates = ("Le dépôt des candidatures a pris fin le 16 octobre 2026. Si vous avez déposé un dossier, vous pourrez consulter la proposition "
                 "du CNRS et y répondre sur Galaxie du 8 au 22 avril 2027.")
        calendar_label = "Calendrier officiel 2027–2028 (PDF)"
        researchers = "Chercheuses et chercheurs titulaires du CNRS"
        reassignment = "Changement d’affectation"
        mobility = ("Si vous êtes titulaire au CNRS et souhaitez travailler à l’ILLS à Montréal, vous pouvez demander une affectation au laboratoire. "
                    "Discutez de votre projet scientifique et des dates envisagées avec la direction de l’ILLS et celle de votre unité d’origine. "
                    "Prenez contact en amont avec la direction scientifique de votre institut pour préciser le calendrier et les modalités d’une affectation à l’étranger.")
        mobility_steps = ("Recueillez les avis écrits des directions de votre unité d’origine et de l’ILLS, puis transmettez votre projet scientifique "
                          "et votre demande à la direction scientifique du ou des instituts concernés. La décision revient aux directions de ces instituts.")
        mobility_label = "Lignes directrices du CNRS sur la mobilité, section II.A (PDF)"
        contact = "Discuter de votre projet avec l’ILLS"
        contact_copy = ("Que vous envisagiez une délégation ou un changement d’affectation, contactez <strong>Pablo Piantanida, directeur de l’ILLS</strong>. "
                        "Dans votre message, présentez brièvement votre projet, les personnes avec qui vous aimeriez collaborer et vos dates de séjour souhaitées à Montréal.")
        email_label = "Écrire à Pablo Piantanida"
        letter_heading = "Lettre d’entente"
        letter_copy = ("Cette lettre présente les attentes communes envers les chercheuses et chercheurs basés en France accueillis à l’ILLS entre 2027 et 2031, "
                       "notamment en matière de collaboration, d’animation scientifique et de formation.")
        letter_label = "Télécharger la lettre d’admission et d’entente (PDF)"
    else:
        title = "Join ILLS in Montréal through CNRS"
        directory_label = "ILLS in the French research directory"
        institute_label = "ILLS at CNRS Sciences informatiques"
        institute_url = "https://www.ins2i.cnrs.fr/en/international-research-laboratory-irl"
        faculty = "For university faculty in France"
        delegation = "Accueil en délégation"
        eligibility = ("If you are a <i lang='fr'>maître de conférences</i> or <i lang='fr'>professeur des universités</i>, "
                       "you can apply for a CNRS delegation to carry out a research project at ILLS. During an approved delegation, "
                       "your home institution continues to pay your salary and releases you from all or part of your teaching duties.")
        procedure = "How to apply"
        faculty_steps = ("Discuss the project with ILLS and your home laboratory early enough for both directors to provide their written opinions. "
                         "Prepare an activity report including your CV, a research proposal of up to five pages, and up to ten selected research outputs. "
                         "Submit your application through Galaxie, identifying ILLS (IRL 2020) as the proposed host. Your institution reviews the application and forwards supported dossiers to CNRS.")
        delegation_label = "CNRS delegation guidance"
        galaxie_label = "Galaxie application instructions and forms"
        campaign = "2027–2028 campaign"
        dates = ("The deadline for applicants was 16 October 2026. Applicants who submitted a dossier can consult and respond to CNRS proposals "
                 "in Galaxie from 8 to 22 April 2027.")
        calendar_label = "Official 2027–2028 campaign calendar (PDF)"
        researchers = "For permanent CNRS researchers"
        reassignment = "Changement d’affectation"
        mobility = ("If you are a permanent CNRS researcher and would like to work at ILLS in Montréal, you can request an assignment to the laboratory. "
                    "Begin by discussing your research plan and proposed dates with the ILLS directors and your current unit director. "
                    "Contact the scientific leadership of your CNRS institute early to confirm the timetable and arrangements for an assignment abroad.")
        mobility_steps = ("Obtain the written opinions of your current and prospective unit directors, then send your research project and reassignment request "
                          "to the scientific leadership of the CNRS institute or institutes concerned. The institute directors make the decision.")
        mobility_label = "CNRS researcher mobility guidelines, section II.A (PDF)"
        contact = "Discuss your project with ILLS"
        contact_copy = ("Whether you are considering a CNRS delegation or a reassignment, please contact <strong>Pablo Piantanida, Director of ILLS</strong>, "
                        "to discuss your project. In your message, briefly describe your research idea, whom you would like to work with, and your preferred dates in Montréal.")
        email_label = "Email Pablo Piantanida"
        letter_heading = "Letter of Understanding"
        letter_copy = ("This letter sets out the shared expectations for France-based researchers hosted at ILLS during 2027–2031, "
                       "including collaboration, scientific engagement, and training.")
        letter_label = "Download the admission letter of understanding (PDF)"

    return f"""
      <header class="inner-hero"><div class="wrap">
        <h1>{title}</h1><p class="lead">{APPLICATIONS_INTRO[fr]}</p>
        <p class="section-jumps"><a href="https://appliweb.dgri.education.fr/rnsr/PresenteStruct.jsp?PUBLIC=OK&amp;numNatStruct=202224169E">{directory_label}</a>
        <a href="{institute_url}">{institute_label}</a></p>
      </div></header>
      <div class="section wrap">
        <section class="notice-row" id="delegation" aria-labelledby="delegation-heading">
          <div><p class="notice-kind">{faculty}</p><h2 lang="fr" id="delegation-heading">{delegation}</h2></div>
          <div class="notice-copy"><p>{eligibility}</p>
            <a class="link-arrow" href="https://carrieres.cnrs.fr/accueil-en-delegation/">{delegation_label}</a>
            <p><strong>{procedure}.</strong> {faculty_steps}</p>
            <a class="link-arrow" href="https://www.galaxie.enseignementsup-recherche.gouv.fr/ensup/cand_acc_delegation_CNRS.htm">{galaxie_label}</a>
            <p><strong>{campaign}.</strong> {dates}</p>
            <a class="link-arrow" href="https://www.galaxie.enseignementsup-recherche.gouv.fr/ensup/SIRAH/CALENDRIER_SIRAH_2027.pdf">{calendar_label}</a>
          </div>
        </section>
        <section class="notice-row" id="reassignment" aria-labelledby="reassignment-heading">
          <div><p class="notice-kind">{researchers}</p><h2 lang="fr" id="reassignment-heading">{reassignment}</h2></div>
          <div class="notice-copy"><p>{mobility}</p><p><strong>{procedure}.</strong> {mobility_steps}</p>
            <a class="link-arrow" href="https://www.cnrs.fr/sites/default/files/pdf/DRH2020-11_LDG-mobilite.pdf">{mobility_label}</a>
          </div>
        </section>
        <section class="notice-row" id="letter-of-understanding" aria-labelledby="letter-of-understanding-heading">
          <div><p class="notice-kind">{'Période 2027–2031' if fr else '2027–2031 period'}</p><h2 id="letter-of-understanding-heading">{letter_heading}</h2></div>
          <div class="notice-copy"><p>{letter_copy}</p>
            <a class="link-arrow" href="{escape(prefix)}assets/documents/ILLS_Letter_of_Understanding_2027-2031.pdf" download="ILLS_Letter_of_Understanding_2027-2031.pdf">{letter_label}</a>
          </div>
        </section>
        <section class="notice-row" id="discuss-your-project" aria-labelledby="project-heading">
          <h2 id="project-heading">{contact}</h2><div class="notice-copy"><p>{contact_copy}</p>
            <a class="link-arrow" href="mailto:pablo.piantanida@cnrs.fr">{email_label} <span aria-hidden="true">→</span></a>
          </div>
        </section>
      </div>"""


def render_featured_workshop(entry, attributes):
    feature = entry['featured_en']
    days = ''.join(f'<dt>{escape(day)}</dt><dd>{escape(topic)}</dd>' for day, topic in feature['programme'])
    return f"""
      <li class="featured-workshop"{attributes}>
        <div>
          <p class="eyebrow">Featured workshop</p>
          <h3 class="workshop-title">{escape(entry['title'][0])}</h3>
          <p class="workshop-meta">{escape(entry['date'][0])} · {escape(entry['details'][0])}</p>
          <p class="workshop-summary">{escape(entry['summary'][0])}</p>
          <a class="btn btn-aqua" href="{escape(entry['url'][0])}">Explore the programme at Mila <span aria-hidden="true">↗</span></a>
        </div>
        <div class="workshop-programme">
          <h4>Programme at a glance</h4><dl>{days}</dl>
          <p><strong>Organizing committee</strong><br>{escape(feature['organizers'])}</p>
        </div>
      </li>"""


def render_calendar(fr, prefix):
    today = datetime.now(ZoneInfo('America/Toronto')).date().isoformat()
    upcoming = []
    past = []
    for item in sorted(CALENDAR, key=lambda item: item['start']):
        if fr and len(item['title']) == 1:
            continue
        if item.get('end', item['start']) >= today:
            upcoming.append(item)
        else:
            past.append(item)
    groups = [
        ('upcoming', 'Événements à venir' if fr else 'Upcoming events', upcoming,
         'Aucun événement à venir n’a encore été annoncé.' if fr else 'No upcoming events have been announced.'),
        ('seminars', 'Séminaires' if fr else 'Seminars', (), ''),
        ('archive', 'Événements passés' if fr else 'Past events', reversed(past),
         'Aucun événement passé à afficher.' if fr else 'There are no past events to display.'),
    ]
    if not fr:
        groups.append(('institutional-visits', 'Institutional visits',
                       sorted(INSTITUTIONAL_EVENTS, key=lambda item: item['start'], reverse=True),
                       'No institutional visits have been listed.'))
    jumps = ''.join(f'<a href="#{slug}">{escape(heading)}</a>' for slug, heading, _, _ in groups)
    parts = [f"""
      <header class="inner-hero"><div class="wrap">
        <h1>{escape(CALENDAR_TITLE[fr])}</h1><p class="lead">{CALENDAR_INTRO[fr]}</p>
        <nav class="section-jumps" aria-label="{'Sur cette page' if fr else 'On this page'}">
          {jumps}
        </nav>
      </div></header>
      <div class="wrap calendar" data-calendar-date="{today}">"""]
    for slug, heading, entries, message in groups:
        if slug == 'seminars':
            parts.append(seminars.render(fr, today, prefix))
            continue
        rows = ''.join(render_entry(item, fr, prefix) for item in entries)
        parts.append(f"""
          <section id="{slug}" class="notice-section calendar-section" aria-labelledby="{slug}-heading">
            <h2 id="{slug}-heading">{escape(heading)}</h2>
            <p class="calendar-empty"{' hidden' if rows else ''}>{message}</p>
            <ul class="notice-list">{rows}</ul>
          </section>""")
    return ''.join(parts) + '</div>'
