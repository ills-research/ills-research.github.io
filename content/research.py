"""Research programme for the 2027–2031 ILLS renewal proposal.

Both languages use the same slugs and one-based PDF page numbers. The project
examples distinguish collaborations identified in the proposal (section 1.3.4)
from research questions proposed in the four scientific chapters.
"""

BREAST_CANCER_ARTICLE = "https://www.etsmtl.ca/en/news/faciliter-le-diagnostic-du-cancer-du-sein-par-lia"
REGARD_ARTICLE = "https://www.mcgill.ca/research/article/two-mcgill-professors-awarded-funding-ai-research-through-canada-france-collaboration"

AXES = [
    {
        "slug": "foundations",
        "title": "Foundations of Machine Learning",
        "short_title": "Foundations of Machine Learning",
        "teaser": "When can a model make reliable predictions on data it has never seen?",
        "description": (
            "This axis brings together statistics, optimization and information theory to determine which guarantees "
            "hold when data are scarce, noisy or collected under changing conditions. "
            "Researchers study the limits imposed by available data and computing power, and develop ways to "
            "recognize when a prediction is too uncertain to use."
        ),
        "projects": [
            {
                "title": "Knowing when to abstain",
                "description": "Selective prediction lets a model defer a decision when the evidence is weak. The programme studies how to set that threshold and check whether uncertainty estimates remain reliable as the data change.",
            },
            {
                "title": "Learning with partial feedback",
                "description": "A system that picks one action may never see what the alternatives would have yielded. Researchers study how much it can still learn, even when the outcome of its chosen action arrives late.",
            },
        ],
        "page": 16,
    },
    {
        "slug": "generative-ai",
        "title": "Safe and Trustworthy Generative AI",
        "short_title": "Trustworthy Generative AI",
        "teaser": "How can we check the evidence behind a generated answer?",
        "description": (
            "A fluent answer can contain a claim that its cited source does not support. ILLS studies how to trace "
            "claims to evidence, evaluate reasoning and detect when a model reveals sensitive training data. "
            "The work spans text, images and audio, including systems that retrieve external material before generating a response."
        ),
        "projects": [
            {
                "title": "REGARD",
                "url": REGARD_ARTICLE,
                "logos": [
                    {"label": "ANR", "url": "https://anr.fr/", "image": "funders/anr.png"},
                    {"label": "NSERC", "url": "https://nserc-crsng.canada.ca/en", "image": "funders/nserc.svg"},
                ],
                "description": (
                    "Jackie Chi Kit Cheung (McGill University) and Pablo Piantanida (CentraleSupélec) co-lead REGARD. "
                    "Together with researchers from CNRS, Aix-Marseille University, the University of Waterloo and Orange, "
                    "they study how reliably generative AI systems perform in real-world settings."
                ),
            },
            {
                "title": "Auditing information leakage",
                "description": "The proposed programme examines when a prompt can recover private information from training data or retrieved documents, and how privacy safeguards affect the usefulness of an answer.",
            },
        ],
        "page": 23,
    },
    {
        "slug": "multi-agent",
        "title": "Multi-Agent AI and World/Agent Models",
        "short_title": "Multi-Agent AI and World Models",
        "teaser": "How do agents coordinate when each sees only part of the world?",
        "description": (
            "Agents in a team rarely have the same information, and sharing observations takes time and bandwidth. "
            "ILLS studies how they decide what to communicate and learn to anticipate the effects of their actions. "
            "World models let researchers test how those plans hold up when the environment or the other agents change."
        ),
        "projects": [
            {
                "title": "Communication between learning agents",
                "logos": [
                    {"label": "IVADO", "url": "https://ivado.ca/", "image": "funders/ivado.png"},
                ],
                "description": "A collaboration involving Université Laval, McGill and CNRS studies how agents use communication to cooperate while learning through interaction.",
            },
            {
                "title": "Reinforcement learning with delayed rewards",
                "description": "A McGill–CNRS project studies decision-making when feedback is delayed or incomplete. An agent may have to choose its next action before it knows the result of the last one.",
            },
        ],
        "page": 31,
    },
    {
        "slug": "healthcare",
        "title": "Artificial Intelligence for Healthcare Systems",
        "short_title": "AI for Healthcare Systems",
        "teaser": "Will a clinical model still work at another hospital, on another scanner or for another population?",
        "description": (
            "A change in imaging equipment or in the patients a hospital serves can alter how a model performs. "
            "ILLS brings researchers and clinicians together to test systems across sites and patient groups, "
            "measure uncertainty and monitor changes over time. The programme covers medical imaging, rehabilitation and clinical decision support."
        ),
        "projects": [
            {
                "title": "Foundation models for breast cancer screening",
                "url": BREAST_CANCER_ARTICLE,
                "logos": [
                    {"label": "FRQS", "url": "https://frq.gouv.qc.ca/sante/organisation/", "image": "funders/frqs.png"},
                    {"label": "Health Data Hub", "url": "https://www.health-data-hub.fr/", "image": "funders/health-data-hub.png"},
                ],
                "description": "A joint project led by Jose Dolz at ÉTS and Maria Vakalopoulou at CentraleSupélec investigates how foundation models could support earlier detection of breast cancer.",
            },
            {
                "title": "Following disease progression",
                "description": "The programme proposes to study changes in cognition and movement in Alzheimer’s and Parkinson’s diseases using data held across several sites, then test predictions on follow-up data and previously unseen cohorts.",
            },
        ],
        "page": 40,
    },
]

FR_AXES = [
    {
        "slug": "foundations",
        "title": "Fondements de l’apprentissage automatique",
        "short_title": "Fondements de l’apprentissage automatique",
        "teaser": "À quelles conditions un modèle peut-il faire des prédictions fiables sur de nouvelles données ?",
        "description": (
            "Cet axe réunit statistique, optimisation et théorie de l’information pour déterminer quelles garanties "
            "restent valables lorsque les données sont rares, bruitées ou recueillies dans des conditions changeantes. "
            "Les équipes étudient les limites qu’imposent la quantité de données et la puissance de calcul, ainsi que "
            "les moyens de reconnaître une prédiction trop incertaine pour guider une décision."
        ),
        "projects": [
            {
                "title": "Savoir quand s’abstenir",
                "description": "La prédiction sélective permet à un modèle de s’abstenir lorsque les éléments disponibles sont insuffisants. Les équipes étudient comment fixer ce seuil et vérifier que les estimations d’incertitude restent fiables lorsque les données évoluent.",
            },
            {
                "title": "Apprendre avec une information partielle",
                "description": "Un système qui choisit une action ignore souvent ce qu’auraient donné les autres options. Les équipes étudient ce qu’il peut apprendre malgré cette limite, même lorsque le résultat de l’action choisie se fait attendre.",
            },
        ],
        "page": 16,
    },
    {
        "slug": "generative-ai",
        "title": "IA générative sûre et digne de confiance",
        "short_title": "IA générative de confiance",
        "teaser": "Comment vérifier les sources sur lesquelles repose une réponse générée ?",
        "description": (
            "Une réponse bien formulée peut contenir une affirmation que la source citée ne confirme pas. L’ILLS "
            "étudie comment rattacher chaque affirmation à des éléments vérifiables, évaluer le raisonnement d’un modèle "
            "et repérer la divulgation de données sensibles. Les travaux portent sur le texte, l’image et le son, "
            "y compris dans les systèmes qui consultent des documents externes avant de produire une réponse."
        ),
        "projects": [
            {
                "title": "REGARD",
                "url": REGARD_ARTICLE,
                "logos": [
                    {"label": "ANR", "url": "https://anr.fr/", "image": "funders/anr.png"},
                    {"label": "NSERC", "url": "https://nserc-crsng.canada.ca/en", "image": "funders/nserc.svg"},
                ],
                "description": (
                    "Jackie Chi Kit Cheung (Université McGill) et Pablo Piantanida (CentraleSupélec) codirigent REGARD. "
                    "Avec des équipes du CNRS, d’Aix-Marseille Université, de l’Université de Waterloo et d’Orange, "
                    "ils étudient la fiabilité des systèmes d’IA générative en conditions réelles d’utilisation."
                ),
            },
            {
                "title": "Détecter les fuites d’information",
                "description": "Le programme étudie dans quelles conditions une requête peut révéler des renseignements privés issus des données d’entraînement ou des documents consultés, et comment les mesures de protection influent sur l’utilité des réponses.",
            },
        ],
        "page": 23,
    },
    {
        "slug": "multi-agent",
        "title": "IA multi-agents et modèles du monde et des agents",
        "short_title": "IA multi-agents et modèles du monde",
        "teaser": "Comment des agents se coordonnent-ils quand chacun n’observe qu’une partie de son environnement ?",
        "description": (
            "Les agents d’une équipe disposent rarement des mêmes informations. Échanger leurs observations prend du "
            "temps et mobilise de la bande passante. L’ILLS étudie comment ils choisissent les informations à partager "
            "et apprennent à anticiper les effets de leurs actions. Les modèles du monde servent à tester leurs stratégies "
            "lorsque l’environnement ou le comportement des autres agents change."
        ),
        "projects": [
            {
                "title": "La communication entre agents apprenants",
                "logos": [
                    {"label": "IVADO", "url": "https://ivado.ca/", "image": "funders/ivado.png"},
                ],
                "description": "Une collaboration entre l’Université Laval, McGill et le CNRS étudie la manière dont des agents communiquent pour coopérer tout en apprenant de leurs interactions.",
            },
            {
                "title": "Apprentissage par renforcement avec récompense différée",
                "description": "Un projet mené par McGill et le CNRS porte sur la prise de décision lorsque le retour d’information est tardif ou incomplet. Un agent doit parfois choisir sa prochaine action avant de connaître le résultat de la précédente.",
            },
        ],
        "page": 31,
    },
    {
        "slug": "healthcare",
        "title": "Intelligence artificielle pour les systèmes de santé",
        "short_title": "IA pour les systèmes de santé",
        "teaser": "Un modèle clinique reste-t-il fiable dans un autre hôpital, sur un autre appareil ou auprès d’une autre population ?",
        "description": (
            "Les performances d’un modèle peuvent varier lorsque le matériel d’imagerie change ou que le profil des "
            "patients évolue. L’ILLS associe des équipes de recherche et des cliniciens pour évaluer ces systèmes dans "
            "plusieurs établissements et groupes de patients, mesurer l’incertitude et suivre son évolution. Les travaux "
            "portent sur l’imagerie médicale, la réadaptation et l’aide à la décision clinique."
        ),
        "projects": [
            {
                "title": "Des modèles de fondation pour le dépistage du cancer du sein",
                "url": BREAST_CANCER_ARTICLE,
                "logos": [
                    {"label": "FRQS", "url": "https://frq.gouv.qc.ca/sante/organisation/", "image": "funders/frqs.png"},
                    {"label": "Health Data Hub", "url": "https://www.health-data-hub.fr/", "image": "funders/health-data-hub.png"},
                ],
                "description": "Un projet conjoint dirigé par Jose Dolz à l’ÉTS et Maria Vakalopoulou à CentraleSupélec étudie la contribution que pourraient apporter les modèles de fondation à la détection précoce du cancer du sein.",
            },
            {
                "title": "Suivre la progression des maladies",
                "description": "Le programme propose d’étudier l’évolution des fonctions cognitives et motrices dans les maladies d’Alzheimer et de Parkinson à partir de données réparties entre plusieurs établissements. Les prédictions seraient ensuite évaluées sur des données de suivi et auprès de nouvelles cohortes.",
            },
        ],
        "page": 40,
    },
]
