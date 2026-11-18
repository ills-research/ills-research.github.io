"""Research programme for the 2027–2031 ILLS renewal proposal.

Both languages use the same slugs and one-based PDF page numbers. The project
examples distinguish collaborations identified in the proposal (section 1.3.4)
from research questions proposed in the four scientific chapters.
"""

BREAST_CANCER_ARTICLE = "https://www.etsmtl.ca/en/news/faciliter-le-diagnostic-du-cancer-du-sein-par-lia"
REGARD_ARTICLE = "https://www.mcgill.ca/research/article/two-mcgill-professors-awarded-funding-ai-research-through-canada-france-collaboration"

# Selected papers for the Foundations of Machine Learning carousel. The figures
# are reused from the open-access articles under the licenses shown in each
# figure credit; the files are kept with the site for stable rendering.
FOUNDATIONS_PAPERS = [
    {
        "year": "2022",
        "venue": "ICML · PMLR",
        "title": "A Differential Entropy Estimator for Training Neural Networks",
        "url": "https://proceedings.mlr.press/v162/pichler22a.html",
        "figure": "research/papers/entropy-estimation.svg",
        "figure_alt": [
            "Figure from the article illustrating differential-entropy estimation as Gaussian variance changes.",
            "Figure de l’article illustrant l’estimation de l’entropie différentielle lorsque la variance gaussienne varie.",
        ],
        "credit": "Figure 1 · Pichler et al., 2022",
        "license": "CC BY 4.0",
        "license_url": "https://creativecommons.org/licenses/by/4.0/",
        "summary": [
            "Introduces KNIFE, a differentiable estimator of entropy and mutual information that can be used to train neural networks.",
            "Présente KNIFE, un estimateur différentiable de l’entropie et de l’information mutuelle utilisable pour entraîner des réseaux de neurones.",
        ],
        "ills_authors": [{"name": "Pablo Piantanida", "path": "people/pablo-piantanida.html"}],
    },
    {
        "year": "2023",
        "venue": "ICML · PMLR",
        "title": "Graph Inductive Biases in Transformers without Message Passing",
        "url": "https://proceedings.mlr.press/v202/ma23c.html",
        "figure": "research/papers/graph-transformer.png",
        "figure_alt": [
            "The GRIT graph transformer architecture, from the article.",
            "Architecture du Transformer pour graphes GRIT, reproduite de l’article.",
        ],
        "credit": "GRIT architecture · Ma et al., 2023",
        "license": "CC BY 4.0",
        "license_url": "https://creativecommons.org/licenses/by/4.0/",
        "summary": [
            "Shows how graph structure can strengthen transformers without message passing, with theoretical guarantees and benchmark results.",
            "Montre comment intégrer la structure des graphes aux Transformers sans transmission de messages, avec des garanties théoriques et des résultats expérimentaux.",
        ],
        "ills_authors": [{"name": "Mark Coates", "path": "people/mark-coates.html"}],
    },
    {
        "year": "2024",
        "venue": "NeurIPS",
        "title": "When is an Embedding Model More Promising than Another?",
        "url": "https://papers.nips.cc/paper_files/paper/2024/hash/7e6f445a74cdb71931aac64f1e3f49c9-Abstract-Conference.html",
        "figure": "research/papers/embedding-comparison.png",
        "figure_alt": [
            "Article diagram comparing two embedding models as information channels.",
            "Schéma de l’article comparant deux modèles d’embeddings comme canaux d’information.",
        ],
        "credit": "Figure 1 · Darrin et al., 2024",
        "license": "CC BY-SA 4.0",
        "license_url": "https://creativecommons.org/licenses/by-sa/4.0/",
        "summary": [
            "Develops an information-theoretic way to compare embedding models, with experiments in language and molecular modelling.",
            "Développe une méthode fondée sur la théorie de l’information pour comparer des modèles d’embeddings, évaluée en traitement du langage et en modélisation moléculaire.",
        ],
        "ills_authors": [
            {"name": "Maxime Darrin", "path": "people/students/maxime-darrin.html"},
            {"name": "Philippe Formont", "path": "people/students/philippe-formont.html"},
            {"name": "Ismail Ben Ayed", "path": "people/ismail-ben-ayed.html"},
            {"name": "Jackie Chi Kit Cheung", "path": "people/jackie-chi-kit-cheung.html"},
            {"name": "Pablo Piantanida", "path": "people/pablo-piantanida.html"},
        ],
    },
    {
        "year": "2025",
        "venue": "ICML · PMLR",
        "title": "When to retrain a machine learning model",
        "url": "https://proceedings.mlr.press/v267/regol25a.html",
        "figure": "research/papers/retraining-problem.svg",
        "figure_alt": [
            "Article diagram showing model performance decreasing under distribution shift and the timing of retraining.",
            "Schéma de l’article montrant la baisse de performance d’un modèle face à un décalage de distribution et le choix du moment de son réentraînement.",
        ],
        "credit": "Figure 1 · Regol et al., 2025",
        "license": "CC BY 4.0",
        "license_url": "https://creativecommons.org/licenses/by/4.0/",
        "summary": [
            "Frames retraining as a decision under distribution shift and uses uncertainty-aware forecasts to balance performance against retraining costs.",
            "Formule le réentraînement comme une décision face au décalage de distribution et s’appuie sur des prévisions tenant compte de l’incertitude pour arbitrer entre performance et coût.",
        ],
        "ills_authors": [{"name": "Mark Coates", "path": "people/mark-coates.html"}],
    },
    {
        "year": "2022",
        "venue": "NeurIPS",
        "title": "On Learning Fairness and Accuracy on Multiple Subgroups",
        "url": "https://proceedings.neurips.cc/paper_files/paper/2022/hash/dc96134e169de5aea1ba1fc34dfb8419-Abstract-Conference.html",
        "figure_url": "https://arxiv.org/html/2210.10837v2/bi_demo.svg",
        "figure_alt": [
            "Paper diagram illustrating the relationship between subgroup sufficiency and a fairness–accuracy objective.",
            "Schéma de l’article illustrant le lien entre la suffisance des sous-groupes et un objectif d’équité et de précision.",
        ],
        "credit": "Figure 1 · Shui et al., 2022",
        "license": "CC BY-NC-SA 4.0",
        "license_url": "https://creativecommons.org/licenses/by-nc-sa/4.0/",
        "summary": [
            "Studies how to balance predictive accuracy with fairness across multiple subgroups, including the limits imposed by small samples.",
            "Étudie comment concilier précision prédictive et équité entre plusieurs sous-groupes, notamment lorsque les échantillons sont limités.",
        ],
        "ills_authors": [{"name": "Tal Arbel", "url": "https://www.mcgill.ca/ece/tal-arbel"}],
    },
    {
        "year": "2022",
        "venue": "NeurIPS",
        "title": "Attention-based Neural Cellular Automata",
        "url": "https://papers.nips.cc/paper_files/paper/2022/hash/361e5112d2eca09513bbd266e4b2d2be-Abstract-Conference.html",
        "figure_url": "https://arxiv.org/html/2211.01233v1/assets/teaser.png",
        "figure_alt": [
            "Article teaser showing patterns and images produced by an attention-based neural cellular automaton.",
            "Illustration de l’article montrant des motifs et des images produits par un automate cellulaire neuronal fondé sur l’attention.",
        ],
        "credit": "Figure 1 · Tesfaldet et al., 2022",
        "license": "CC BY 4.0",
        "license_url": "https://creativecommons.org/licenses/by/4.0/",
        "summary": [
            "Introduces a cellular automaton that uses spatially localised self-attention, then evaluates its learned representations and image-denoising performance.",
            "Présente un automate cellulaire qui utilise l’attention auto-régressive localisée dans l’espace, puis évalue ses représentations et ses performances de débruitage d’images.",
        ],
        "ills_authors": [{"name": "Derek Nowrouzezahrai", "url": "https://www.mcgill.ca/ece/derek-nowrouzezahrai"}],
    },
    {
        "year": "2023",
        "venue": "AutoML · PMLR",
        "title": "Balanced Mixture of SuperNets for Learning the CNN Pooling Architecture",
        "url": "https://proceedings.mlr.press/v224/roshtkhari23a.html",
        "figure_url": "https://arxiv.org/html/2306.11982v1/scheme.svg",
        "figure_alt": [
            "Diagram of the balanced mixture of supernets used to search for CNN pooling configurations.",
            "Schéma du mélange équilibré de super-réseaux utilisé pour rechercher des configurations de pooling de CNN.",
        ],
        "credit": "Figure 2 · Javan et al., 2023",
        "license": "CC BY 4.0",
        "license_url": "https://creativecommons.org/licenses/by/4.0/",
        "summary": [
            "Proposes a balanced mixture of supernets to search for CNN pooling configurations while reducing interference between candidate architectures.",
            "Propose un mélange équilibré de super-réseaux pour rechercher des configurations de pooling de CNN tout en réduisant l’interférence entre architectures candidates.",
        ],
        "ills_authors": [{"name": "Marco Pedersoli", "path": "people/marco-pedersoli.html"}],
    },
    {
        "year": "2023",
        "venue": "CVPR",
        "title": "A Strong Baseline for Generalized Few-Shot Semantic Segmentation",
        "url": "https://openaccess.thecvf.com/content/CVPR2023/html/Hajimiri_A_Strong_Baseline_for_Generalized_Few-Shot_Semantic_Segmentation_CVPR_2023_paper.html",
        "figure_url": "https://arxiv.org/html/2211.14126v2/visual.png",
        "figure_alt": [
            "Unmodified qualitative segmentation results from the article, showing predictions for novel classes.",
            "Résultats qualitatifs de segmentation reproduits sans modification, montrant des prédictions pour de nouvelles classes.",
        ],
        "credit": "Figure 2 · Hajimiri et al., 2023",
        "license": "CC BY-NC-ND 4.0",
        "license_url": "https://creativecommons.org/licenses/by-nc-nd/4.0/",
        "summary": [
            "Presents an information-theoretic method for semantic segmentation with only a few labelled examples of new classes, while retaining knowledge of known classes.",
            "Présente une méthode fondée sur la théorie de l’information pour segmenter de nouvelles classes à partir de quelques exemples annotés, tout en conservant les connaissances acquises sur les classes connues.",
        ],
        "ills_authors": [{"name": "José Dolz", "path": "people/jose-dolz.html"}],
    },
    {
        "year": "2024",
        "venue": "NeurIPS",
        "title": "Supra-Laplacian Encoding for Transformer on Dynamic Graphs",
        "url": "https://proceedings.neurips.cc/paper_files/paper/2024/hash/1ed4723f12853cbd02aecb8160f5e0c9-Abstract-Conference.html",
        "figure_url": "https://arxiv.org/html/2409.17986v2/figures/slate.png",
        "figure_alt": [
            "SLATE architecture diagram combining the time slices of a dynamic graph in a transformer.",
            "Schéma de l’architecture SLATE, qui combine dans un Transformer les différentes tranches temporelles d’un graphe dynamique.",
        ],
        "credit": "Figure 2 · Karmim et al., 2024",
        "license": "CC BY 4.0",
        "license_url": "https://creativecommons.org/licenses/by/4.0/",
        "summary": [
            "Introduces a spectral encoding that helps graph transformers preserve both structural and temporal information when predicting links in dynamic graphs.",
            "Introduit un encodage spectral qui aide les Transformers pour graphes à préserver les informations structurelles et temporelles lors de la prédiction de liens dans des graphes dynamiques.",
        ],
        "ills_authors": [{"name": "Nicolas Thome", "path": "people/nicolas-thome.html"}],
    },
    {
        "year": "2025",
        "venue": "ICML · PMLR",
        "title": "A Theoretical Justification for Asymmetric Actor-Critic Algorithms",
        "url": "https://proceedings.mlr.press/v267/lambrechts25a.html",
        "figure": "research/papers/asymmetric-actor-critic.svg",
        "figure_alt": [
            "Diagram adapted from the article to show how the actor uses observations while the critic can also use state information during training.",
            "Schéma adapté de l’article montrant que l’acteur utilise les observations, tandis que le critique peut aussi utiliser l’état pendant l’entraînement.",
        ],
        "credit": "Diagram adapted from Figure 1 · Lambrechts et al., 2025",
        "license": "CC BY 4.0",
        "license_url": "https://creativecommons.org/licenses/by/4.0/",
        "summary": [
            "Provides a finite-time theoretical analysis of asymmetric actor–critic methods and shows how a privileged training-time critic can reduce errors caused by partial observability.",
            "Fournit une analyse théorique en temps fini des méthodes acteur–critique asymétriques et montre comment un critique disposant d’informations supplémentaires pendant l’entraînement peut réduire les erreurs dues à l’observabilité partielle.",
        ],
        "ills_authors": [{"name": "Aditya Mahajan", "path": "people/aditya-mahajan.html"}],
    },
    {
        "year": "2025",
        "venue": "ICML · PMLR",
        "title": "Pareto-Optimality, Smoothness, and Stochasticity in Learning-Augmented One-Max-Search",
        "url": "https://proceedings.mlr.press/v267/benomar25a.html",
        "figure_url": "https://arxiv.org/html/2502.05720v1/thresh_rho.svg",
        "figure_alt": [
            "Article figure comparing threshold functions for learning-augmented one-max search.",
            "Figure de l’article comparant les fonctions seuils pour la recherche du maximum avec prédictions.",
        ],
        "credit": "Figure 2 · Benomar et al., 2025",
        "license": "CC BY 4.0",
        "license_url": "https://creativecommons.org/licenses/by/4.0/",
        "summary": [
            "Studies online search with predictions and develops an algorithm that balances strong performance when predictions are accurate with robustness when they are not.",
            "Étudie la recherche en ligne avec prédictions et développe un algorithme qui concilie de bonnes performances lorsque les prédictions sont précises et la robustesse lorsqu’elles ne le sont pas.",
        ],
        "ills_authors": [{"name": "Spyros Angelopoulos", "path": "people/spyros-angelopoulos.html"}],
    },
    {
        "year": "2025",
        "venue": "NeurIPS",
        "title": "Learning Task-Agnostic Representations through Multi-Teacher Distillation",
        "url": "https://papers.nips.cc/paper_files/paper/2025/hash/9e11d680214e92c1683aaf80ae30febe-Abstract-Conference.html",
        "figure_url": "https://arxiv.org/html/2510.18680v1/figures/method.png",
        "figure_alt": [
            "Overview figure of the multi-teacher distillation method for learning task-agnostic representations.",
            "Schéma général de la méthode de distillation multi-enseignants pour apprendre des représentations indépendantes des tâches.",
        ],
        "credit": "Figure 1 · Shateri et al., 2025",
        "license": "CC BY 4.0",
        "license_url": "https://creativecommons.org/licenses/by/4.0/",
        "summary": [
            "Combines knowledge from multiple teacher models to learn general-purpose representations without requiring labels for each downstream task.",
            "Combine les connaissances de plusieurs modèles enseignants pour apprendre des représentations polyvalentes sans exiger des annotations pour chaque tâche ultérieure.",
        ],
        "ills_authors": [{"name": "Mohammadhadi Shateri", "path": "people/mohammadhadi-shateri.html"}],
    },
]

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
