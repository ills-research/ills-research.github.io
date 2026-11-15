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
    {
        "id": "ills-evaluation-2026",
        "kind": ("Milestone", "Étape marquante"),
        "start": "2026-04-27", "end": "2026-04-29",
        "date": ("27–29 April 2026", "Du 27 au 29 avril 2026"),
        "details": ("ÉTS · Montréal", "ÉTS · Montréal"),
        "title": ("ILLS evaluation in Montréal", "Évaluation de l’ILLS à Montréal"),
        "summary": (
            "From 27 to 29 April, the ILLS community gathered in Montréal for the laboratory’s evaluation, presenting its work and discussing the scientific programme ahead.",
            "Du 27 au 29 avril, la communauté de l’ILLS s’est réunie à Montréal pour l’évaluation du laboratoire, afin de présenter ses travaux et d’échanger sur son programme scientifique.",
        ),
        "photos": [
            {"file": "ills-evaluation-2026-group.jpg", "size": (3900, 1365),
             "alt": ("ILLS researchers and students gather for the laboratory evaluation in Montréal.",
                    "Des chercheurs et étudiants de l’ILLS réunis à Montréal pour l’évaluation du laboratoire.")},
            {"file": "ills-evaluation-2026-auditorium.jpg", "size": (4080, 3072),
             "alt": ("Researchers attend a presentation during the ILLS evaluation in Montréal.",
                    "Des chercheurs assistent à une présentation pendant l’évaluation de l’ILLS à Montréal.")},
            {"file": "ills-evaluation-2026-seminar-room.jpg", "size": (4080, 3072),
             "alt": ("ILLS researchers and students gather for a presentation in Montréal.",
                    "Des chercheurs et étudiants de l’ILLS assistent à une présentation à Montréal.")},
        ],
        "photo_layout": "lead",
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
        "Adeline Nazarenko, Director of CNRS Computer Sciences, and Jérôme Durand-Lose, Deputy Scientific Director for Europe and International Affairs, met ILLS researchers and students to discuss how the lab makes machine learning algorithms more reliable and safer to use. The delegation also met partners at IVADO, Mila, McGill and ÉTS.",
        "Adeline Nazarenko, directrice de CNRS Sciences informatiques, et Jérôme Durand-Lose, directeur adjoint scientifique chargé de l’Europe et de l’international, ont échangé avec les membres de l’ILLS sur la fiabilité et la sûreté des algorithmes d’apprentissage. La délégation a aussi rencontré des partenaires à IVADO, à Mila, à McGill et à l’ÉTS.",
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

NEWS = [
    CNRS_VISIT_2026,
    {
        "id": "diag-nos-chair-2026",
        "kind": ("Research chair", "Chaire de recherche"),
        "start": "2026-06-15",
        "date": ("15 June 2026", "15 juin 2026"),
        "details": ("ÉTS · Montréal", "ÉTS · Montréal"),
        "title": (
            "ÉTS and DIAGNOS launch a new industrial chair in AI for medical imaging",
            "L’ÉTS et DIAGNOS lancent une nouvelle chaire industrielle en intelligence artificielle pour l’imagerie médicale",
        ),
        "summary": (
            "Led by ILLS member Ismail Ben Ayed, the new chair will develop reliable AI methods to analyse retinal images and support earlier detection of disease.",
            "Dirigée par Ismail Ben Ayed, membre de l’ILLS, la nouvelle chaire développera des méthodes d’IA fiables pour analyser les images rétiniennes et favoriser le dépistage précoce de maladies.",
        ),
        "link": ("Discover the DIAGNOS Research Chair", "Découvrir la chaire de recherche DIAGNOS"),
        "url": (
            "https://www.etsmtl.ca/actualites/analyse-retine-pourrait-permettre-depister-centaine-maladies",
            "https://www.etsmtl.ca/actualites/analyse-retine-pourrait-permettre-depister-centaine-maladies",
        ),
    },
    {
        "id": "cvpr-compute-transparency-2026",
        "kind": ("Award", "Prix"),
        "start": "2026-06",
        "date": ("June 2026", "Juin 2026"),
        "details": ("ÉTS · Montréal", "ÉTS · Montréal"),
        "title": (
            "Mohammadhadi Shateri and Éric Granger share a CVPR 2026 transparency award",
            "Mohammadhadi Shateri et Éric Granger reçoivent un prix de transparence à CVPR 2026",
        ),
        "summary": (
            "The paper Uni-DAD, co-authored with LIVIA researchers Yara Bahram and Mélodie Desbos, received CVPR’s Compute Transparency Champion award for its reporting of computational resources and experiments.",
            "L’article Uni-DAD, cosigné avec les chercheuses de LIVIA Yara Bahram et Mélodie Desbos, a reçu le prix Compute Transparency Champion de CVPR pour la transparence de sa documentation des ressources de calcul et des expériences.",
        ),
        "links": [
            {"label": ("CVPR compute reporting initiative", "Initiative de transparence de CVPR"),
             "url": ("https://cvpr.thecvf.com/Conferences/2026/ComputeReporting",) * 2},
            {"label": ("Uni-DAD paper", "Article Uni-DAD"),
             "url": ("https://arxiv.org/abs/2511.18281",) * 2},
        ],
    },
    {
        "id": "georges-kaddoum-awards-2022-2025",
        "kind": ("Awards and distinctions", "Prix et distinctions"),
        "start": "2025-11-06",
        "date": ("2022–2025", "2022–2025"),
        "details": ("ÉTS · Montréal", "ÉTS · Montréal"),
        "title": (
            "Georges Kaddoum receives major research and engineering honours",
            "Georges Kaddoum reçoit plusieurs distinctions en recherche et en génie",
        ),
        "summary": (
            "Since 2022, ILLS member Georges Kaddoum has received the IEEE TCSC Award for Excellence in Scalable Computing (2022), the Mitacs Award for Exceptional Leadership (2023), election to the Royal Society of Canada (2024), and four 2025 honours: the ÉTS Board of Directors Research Excellence Award, the Université du Québec Partnership Excellence Award, the NSERC Synergy Award for Innovation and Engineers Canada’s Gold Medal.",
            "Depuis 2022, Georges Kaddoum, membre de l’ILLS, a reçu le prix d’excellence en informatique évolutive du comité TCSC de l’IEEE (2022), le prix Mitacs pour leadership exceptionnel (2023), son élection à la Société royale du Canada (2024), puis quatre distinctions en 2025 : le Prix d’excellence du C.A. en recherche de l’ÉTS, le Prix d’excellence du partenariat de l’Université du Québec, le prix Synergie du CRSNG pour l’innovation et la Médaille d’or d’Ingénieurs Canada.",
        ),
        "links": [
            {"label": ("ÉTS profile and honours", "Profil et distinctions à l’ÉTS"),
             "url": ("https://www.etsmtl.ca/etudier-a-lets/corps-professoral/gkaddoum?lang=en-CA",) * 2},
            {"label": ("NSERC Synergy Award", "Prix Synergie du CRSNG"),
             "url": ("https://www.etsmtl.ca/actualites/georges-kaddoum-remporte-prix-innovation-synergie-crsng",) * 2},
            {"label": ("Engineers Canada Gold Medal", "Médaille d’or d’Ingénieurs Canada"),
             "url": ("https://engineerscanada.ca/news-and-events/news/engineers-canada-honours-six-exceptional-members-of-the-engineering-community",) * 2},
            {"label": ("UQ Partnership Excellence Award", "Prix d’excellence du partenariat de l’UQ"),
             "url": ("https://reseau.uquebec.ca/fr/a-propos/salle-de-presse/communiques-de-presse/universite-du-quebec-souligne-excellence-des-membres-de-sa-communaute-universitaire",) * 2},
        ],
    },
    {
        "id": "dasc-best-session-jeremy-2025",
        "kind": ("Award", "Prix"),
        "start": "2025",
        "date": ("2025", "2025"),
        "details": ("McGill University · Montréal", "Université McGill · Montréal"),
        "title": ("Jeremy R. Cooperstock’s WILCO paper earns a DASC Best of Session award", "L’article WILCO de Jeremy R. Cooperstock reçoit un prix Best of Session au DASC"),
        "summary": (
            "The WILCO paper by ILLS member Jeremy R. Cooperstock and collaborators received a Best of Session award at the 2025 Digital Avionics Systems Conference.",
            "L’article WILCO de Jeremy R. Cooperstock, membre de l’ILLS, et de ses collaborateurs a reçu un prix Best of Session à la conférence Digital Avionics Systems Conference 2025.",
        ),
        "link": ("DASC 2025 paper awards", "Prix des articles du DASC 2025"),
        "url": ("https://2025.dasconline.org/awards/best-paper-awards/",) * 2,
    },
    {
        "id": "impact-health-ets-2024",
        "kind": ("Award", "Prix"),
        "start": "2024-04-11",
        "date": ("11 April 2024", "11 avril 2024"),
        "details": ("ÉTS · Montréal", "ÉTS · Montréal"),
        "title": ("Éric Granger and Marco Pedersoli receive the ÉTS Impact Award for Health and Well-being", "Éric Granger et Marco Pedersoli reçoivent le prix Impact de l’ÉTS – Santé et mieux-être"),
        "summary": (
            "The award recognized a collaborative project exploring how AI can support lasting behaviour change. The ÉTS team included ILLS members Éric Granger and Marco Pedersoli.",
            "Le prix récompense un projet collaboratif qui étudie comment l’IA peut soutenir des changements durables de comportement. L’équipe de l’ÉTS comprenait Éric Granger et Marco Pedersoli, membres de l’ILLS.",
        ),
        "link": ("ÉTS 2024 awards announcement", "Annonce des prix 2024 de l’ÉTS"),
        "url": ("https://www.etsmtl.ca/actualites/gala-dexcellence-recherche-et-enseignement-2024",) * 2,
    },
    {
        "id": "aditya-mahajan-fellowships-2023-2024",
        "kind": ("Fellowships", "Bourses"),
        "start": "2024",
        "date": ("2023–2024", "2023–2024"),
        "details": ("McGill University · Montréal", "Université McGill · Montréal"),
        "title": ("Aditya Mahajan receives DATAIA and Jean d’Alembert fellowships", "Aditya Mahajan reçoit les bourses DATAIA et Jean d’Alembert"),
        "summary": (
            "Current ILLS member Aditya Mahajan received a DATAIA Fellowship in 2023 and a Jean d’Alembert Fellowship from Université Paris-Saclay in 2024.",
            "Aditya Mahajan, membre actuel de l’ILLS, a reçu une bourse DATAIA en 2023, puis une bourse Jean d’Alembert de l’Université Paris-Saclay en 2024.",
        ),
        "link": ("GERAD profile and awards", "Profil et distinctions sur le site du GERAD"),
        "url": ("https://www.gerad.ca/en/people/aditya-mahajan",) * 2,
    },
    {
        "id": "ajung-moon-adler-scholar-award-2025",
        "kind": ("Distinction", "Distinction"),
        "start": "2025",
        "date": ("2025–2028", "2025–2028"),
        "details": ("McGill University · Montréal", "Université McGill · Montréal"),
        "title": ("AJung Moon named an Eric L. Adler Faculty Scholar", "AJung Moon nommée Eric L. Adler Faculty Scholar"),
        "summary": (
            "ILLS member AJung Moon received the Eric L. Adler Faculty Scholar Award for a three-year term running from 2025 to 2028.",
            "AJung Moon, membre de l’ILLS, a reçu l’Eric L. Adler Faculty Scholar Award pour un mandat de trois ans, de 2025 à 2028.",
        ),
    },
    {
        "id": "stephane-coulombe-ieee-election-2024",
        "kind": ("Distinction", "Distinction"),
        "start": "2024",
        "date": ("2024–2028", "2024–2028"),
        "details": ("ÉTS · Montréal", "ÉTS · Montréal"),
        "title": ("Stéphane Coulombe elected to IEEE CASS technical committee", "Stéphane Coulombe élu au comité technique IEEE CASS"),
        "summary": (
            "ILLS member Stéphane Coulombe was elected to the IEEE Circuits and Systems Society Multimedia Systems and Applications Technical Committee for the 2024–2028 term.",
            "Stéphane Coulombe, membre de l’ILLS, a été élu au comité technique Multimedia Systems and Applications de l’IEEE Circuits and Systems Society pour le mandat 2024–2028.",
        ),
        "link": ("IEEE committee profile", "Profil du comité IEEE"),
        "url": ("https://ieee-cas.org/contact/stephane-coulombe",) * 2,
    },
    {
        "id": "ulrich-aivodji-frqnt-2024",
        "kind": ("Award", "Prix"),
        "start": "2024-04-30",
        "date": ("30 April 2024", "30 avril 2024"),
        "details": ("ÉTS · Montréal", "ÉTS · Montréal"),
        "title": ("Ulrich Aïvodji receives an FRQNT award for new academics", "Ulrich Aïvodji reçoit un prix du FRQNT pour la relève professorale"),
        "summary": (
            "ILLS member Ulrich Aïvodji received the FRQNT Research Support for New Academics Award.",
            "Ulrich Aïvodji, membre de l’ILLS, a reçu le prix Soutien à la recherche pour la relève professorale du FRQNT.",
        ),
        "link": ("TISL Lab announcement", "Annonce du laboratoire TISL"),
        "url": ("https://tisl-lab.github.io/",) * 2,
    },
    {
        "id": "amazon-research-award-pablo-2023",
        "kind": ("Award", "Prix"),
        "start": "2023",
        "date": ("2023", "2023"),
        "details": ("CentraleSupélec · France", "CentraleSupélec · France"),
        "title": ("Pablo Piantanida receives an Amazon Research Award", "Pablo Piantanida reçoit un Amazon Research Award"),
        "summary": (
            "The award supported research into efficient adaptation of generative language models through unsupervised calibration, a project involving ILLS co-director Pablo Piantanida.",
            "Le prix a soutenu des travaux sur l’adaptation efficace des modèles génératifs de langue par calibration non supervisée, un projet auquel participe Pablo Piantanida, codirecteur de l’ILLS.",
        ),
        "link": ("Award recipient profile", "Profil du lauréat"),
        "url": ("https://www.amazon.science/research-awards/recipients/pablo-piantanida",) * 2,
    },
    {
        "id": "jeremy-cooperstock-chi-2022",
        "kind": ("Distinction", "Distinction"),
        "start": "2022",
        "date": ("2022", "2022"),
        "details": ("McGill University · Montréal", "Université McGill · Montréal"),
        "title": ("Jeremy R. Cooperstock co-authors a CHI 2022 Honorable Mention paper", "Jeremy R. Cooperstock cosigne un article récompensé d’une mention honorable à CHI 2022"),
        "summary": (
            "“The Sound of Hallucinations: Toward a More Convincing Emulation of Internalized Voices” received an Honorable Mention at the ACM CHI Conference on Human Factors in Computing Systems.",
            "« The Sound of Hallucinations: Toward a More Convincing Emulation of Internalized Voices » a reçu une mention honorable à la conférence ACM CHI sur les facteurs humains en informatique.",
        ),
        "link": ("Sound Recording and Interaction Lab publications", "Publications du Sound Recording and Interaction Lab"),
        "url": ("https://srl.mcgill.ca/publications/",) * 2,
    },
    PAVILION_OPENING_2025,
]

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
        "date": ("2027", "2027"),
        "details": ("ILLS · Montréal", "ILLS · Montréal"),
        "title": (
            "Research internships in Montréal (4–6 months, 2027)",
            "Stages de recherche à Montréal (4 à 6 mois, 2027)",
        ),
        "summary": (
            "ILLS invites students to apply for a 4–6-month research internship in Montréal during 2027. Projects span trustworthy generative AI, multi-agent AI and world models, AI for healthcare and critical engineering systems, and foundations of machine learning. To discuss project fit and application details, email the ILLS secretariat with a CV, academic transcript, a short statement of research interests, and your preferred dates.",
            "L’ILLS invite les étudiantes et étudiants à présenter leur candidature pour un stage de recherche de 4 à 6 mois à Montréal en 2027. Les projets portent sur l’IA générative de confiance, l’IA multi-agent et les modèles du monde, l’IA pour la santé et les systèmes d’ingénierie critiques, ainsi que les fondements de l’apprentissage automatique. Pour discuter d’un projet et des modalités de candidature, écrivez au secrétariat de l’ILLS en joignant un CV, un relevé de notes, une courte présentation de vos intérêts de recherche et vos dates de disponibilité.",
        ),
        "link": ("Contact the ILLS secretariat", "Écrire au secrétariat de l’ILLS"),
        "url": ("mailto:secretariat-ills@etsmtl.ca",) * 2,
    },
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
        kind_label = escape(entry['kind'][fr])
        english_kind = entry['kind'][0].lower()
        award_icon = ''
        if any(term in english_kind for term in ('award', 'distinction', 'prize')):
            award_icon = (
                '<svg class="notice-award-icon" viewBox="0 0 24 24" fill="none" '
                'aria-hidden="true"><path d="M8 4h8v3.5a4 4 0 0 1-8 0V4ZM8 6H4.5v1.5a3 3 0 0 0 3 3M16 6h3.5v1.5a3 3 0 0 1-3 3M12 11.5V16m-3 0h6m-7 4h8m-7-4-1 4m7-4 1 4" '
                'stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/></svg>'
            )
        kind = f'<span class="notice-kind">{award_icon}{kind_label}</span>'
        date_text = f'<time datetime="{start}">{date_text}</time>'
    link = ''
    if 'links' in entry:
        link = ''.join(
            f'<a class="link-arrow" href="{escape(item["url"][fr])}">'
            f'{escape(item["label"][fr])} <span aria-hidden="true">↗</span></a> '
            for item in entry['links']
        )
    elif 'url' in entry:
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
    gallery_class = 'event-photos event-photos--lead' if entry.get('photo_layout') == 'lead' else 'event-photos'
    gallery = f'<div class="{gallery_class}">' + ''.join(figures) + '</div>' if figures else ''
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
        exchange_heading = "Programmes d’échanges France–Québec"
        exchange_intro = "Des programmes récurrents peuvent aider à financer des séjours de recherche, des stages et de nouveaux projets conjoints. Les appels, les critères et les montants évoluent : vérifiez les modalités en vigueur auprès de chaque organisme et du bureau de la recherche de votre université."
        exchange_programmes = [
            ("Fonds France-Canada pour la Recherche (FFCR)", "Appel annuel de l’Ambassade de France au Canada et d’universités canadiennes pour amorcer de nouvelles collaborations franco-canadiennes. Les projets soutiennent notamment la mobilité des équipes et des étudiants. Le chercheur principal canadien doit être rattaché à une université membre du consortium, dont McGill. Le programme est réservé aux nouvelles collaborations : des travaux antérieurs entre les deux responsables peuvent rendre l’équipe inadmissible.", "https://www.institutfrancais.ca/fr/ffcr"),
            ("Programme Samuel-De Champlain", "Appels récurrents pour des projets interuniversitaires franco-québécois en recherche ou en formation, qui peuvent structurer une collaboration et soutenir la mobilité des équipes. L’intelligence artificielle figure parmi les thèmes prioritaires des derniers appels.", "https://cfqcu.org/fr/conseil-franco-quebecois-cooperation-universitaire/appels-a-projets"),
            ("Bourse de mobilité Québec–France Sophie Germain", "Le FRQ et le Consulat général de France à Québec soutiennent les doctorantes, doctorants et stagiaires postdoctoraux du Québec qui effectuent un séjour de recherche en France d’au moins un mois. Consultez le concours en cours pour connaître les conditions et le financement disponibles.", "https://frq.gouv.qc.ca/programme/bourses-de-mobilite-quebec-france-sophie-germain/"),
            ("Bourse de recherche Globalink de Mitacs (BRG)", "Finance des stages de recherche de 12 à 24 semaines, sous codirection, pour les étudiantes et étudiants de premier cycle avancé, des cycles supérieurs et les stagiaires postdoctoraux. L’appel Adoption de l’IA du G7 inclut la France; les places dépendent de l’allocation de l’université canadienne.", "https://www.mitacs.ca/fr-ca/nos-programmes/bourse-de-recherche-globalink/"),
        ]
        exchange_link_label = "Consulter le programme et les modalités"
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
        exchange_heading = "France–Québec exchange programmes"
        exchange_intro = "Recurring programmes can help fund research visits, internships and new joint projects. Calls, eligibility and award amounts change, so check each programme’s current rules and your university research office before applying."
        exchange_programmes = [
            ("France–Canada Research Fund (FCRF)", "An annual programme supported by the Embassy of France in Canada and a consortium of Canadian universities to launch new France–Canada research collaborations. Grants support project development and mobility for research teams and students. The Canadian lead must be at a consortium member university, including McGill. It is intended for new collaborations; prior joint work may affect eligibility.", "https://www.institutfrancais.ca/en/fcrf"),
            ("Samuel-De Champlain Programme", "Recurring calls support France–Québec university partnerships in research and training, helping teams structure collaborations and mobility. Artificial intelligence has been among the priority themes in recent calls.", "https://cfqcu.org/fr/conseil-franco-quebecois-cooperation-universitaire/appels-a-projets"),
            ("Sophie Germain Québec–France Mobility Grant", "The Fonds de recherche du Québec and the Consulate General of France in Québec support Québec-based doctoral students and postdoctoral fellows undertaking research stays of at least one month in France. Check the current competition for eligibility and funding details.", "https://frq.gouv.qc.ca/programme/bourses-de-mobilite-quebec-france-sophie-germain/"),
            ("Mitacs Globalink Research Award (GRA)", "Funds 12–24-week jointly supervised research internships for senior undergraduates, graduate students and postdoctoral fellows. The G7 AI Adoption call includes France; available awards depend on the Canadian university’s allocation.", "https://www.mitacs.ca/our-programs/globalink-research-award/"),
        ]
        exchange_link_label = "Programme details and current call"
        contact = "Discuss your project with ILLS"
        contact_copy = ("Whether you are considering a CNRS delegation or a reassignment, please contact <strong>Pablo Piantanida, Director of ILLS</strong>, "
                        "to discuss your project. In your message, briefly describe your research idea, whom you would like to work with, and your preferred dates in Montréal.")
        email_label = "Email Pablo Piantanida"
        letter_heading = "Letter of Understanding"
        letter_copy = ("This letter sets out the shared expectations for France-based researchers hosted at ILLS during 2027–2031, "
                       "including collaboration, scientific engagement, and training.")
        letter_label = "Download the admission letter of understanding (PDF)"

    exchange_items = ''.join(
        f'<li><h3><a href="{url}">{name}</a></h3><p>{description}</p>'
        f'<a class="link-arrow" href="{url}">{exchange_link_label} <span aria-hidden="true">↗</span></a></li>'
        for name, description, url in exchange_programmes
    )

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
        <section class="notice-row" id="exchange-programmes" aria-labelledby="exchange-programmes-heading">
          <div><p class="notice-kind">{'Mobilité internationale' if fr else 'International mobility'}</p><h2 id="exchange-programmes-heading">{exchange_heading}</h2></div>
          <div class="notice-copy"><p>{exchange_intro}</p><ul class="mobility-programme-list">{exchange_items}</ul></div>
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
