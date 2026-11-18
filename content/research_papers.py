"""Figure-led selections for the three remaining research-axis carousels.

Figures are shown without modification and link back to their paper source and
license. Article links prefer the published version when one is available.
"""

AXIS_PAPERS = {
    "generative-ai": [
        {
            "year": "2025",
            "venue": "ECCV",
            "title": "Robust Calibration of Large Vision-Language Adapters",
            "url": "https://link.springer.com/10.1007/978-3-031-72691-0_9",
            "figure_url": "https://arxiv.org/html/2407.13588v1/clipa_rp.png",
            "figure_alt": [
                "Comparison of confidence calibration for CLIP adaptation methods on out-of-distribution images.",
                "Comparaison du calibrage de confiance de méthodes d’adaptation de CLIP sur des images hors distribution.",
            ],
            "credit": "Figure 1 · Murugesan et al., 2025",
            "license": "CC BY 4.0",
            "license_url": "https://creativecommons.org/licenses/by/4.0/",
            "summary": [
                "Shows that common ways of adapting CLIP can become overconfident on out-of-distribution images, and studies methods to improve calibration.",
                "Montre que des méthodes courantes d’adaptation de CLIP peuvent devenir trop confiantes sur des images hors distribution, puis étudie des façons d’améliorer leur calibrage.",
            ],
            "ills_authors": [
                {"name": "Ismail Ben Ayed", "path": "people/ismail-ben-ayed.html"},
                {"name": "José Dolz", "path": "people/jose-dolz.html"},
            ],
        },
        {
            "year": "2025",
            "venue": "ICCV Workshops",
            "title": "Prompt4Trust: A Reinforcement Learning Prompt Augmentation Framework for Clinically-Aligned Confidence Calibration in Multimodal Large Language Models",
            "url": "https://ieeexplore.ieee.org/document/11374512/",
            "figure_url": "https://arxiv.org/html/2507.09279v4/fig1.png",
            "figure_alt": [
                "Overview of Prompt4Trust, which uses reinforcement learning to improve confidence calibration in medical visual question answering.",
                "Vue d’ensemble de Prompt4Trust, qui utilise l’apprentissage par renforcement pour améliorer le calibrage de confiance en question-réponse médicale sur images.",
            ],
            "credit": "Figure 1 · Kriz et al., 2025",
            "license": "CC BY-NC-ND 4.0",
            "license_url": "https://creativecommons.org/licenses/by-nc-nd/4.0/",
            "summary": [
                "Uses reinforcement learning to augment prompts for medical visual question answering, addressing prompt sensitivity and overconfident incorrect answers.",
                "Utilise l’apprentissage par renforcement pour enrichir les invites en question-réponse médicale sur images, afin de réduire la sensibilité aux invites et les réponses erronées trop confiantes.",
            ],
            "ills_authors": [
                {"name": "Tal Arbel", "url": "https://www.mcgill.ca/ece/tal-arbel"},
            ],
        },
        {
            "year": "2026",
            "venue": "PVLDB",
            "title": "Understanding Disclosure Risk in Differential Privacy with Applications to Noise Calibration and Auditing",
            "url": "https://www.vldb.org/pvldb/vol19/p1558-guerra-balboa.pdf",
            "figure_url": "https://arxiv.org/html/2603.12142v1/figures/Laplace_accu_m10.png",
            "figure_alt": [
                "Plot comparing the utility of two differential-privacy noise-calibration methods at a fixed estimated disclosure risk.",
                "Graphique comparant l’utilité de deux méthodes de calibrage du bruit différentiel privé pour un risque de divulgation estimé donné.",
            ],
            "credit": "Figure 2 · Guerra-Balboa et al., 2026",
            "license": "CC BY-NC-ND 4.0",
            "license_url": "https://creativecommons.org/licenses/by-nc-nd/4.0/",
            "summary": [
                "Connects differential-privacy noise choices to disclosure risk and the useful information that can still be released, using attack-based auditing.",
                "Relie le choix du bruit en confidentialité différentielle au risque de divulgation et à l’information qui peut rester utile, à l’aide d’audits fondés sur des attaques.",
            ],
            "ills_authors": [
                {"name": "Héber H. Arcolezi", "path": "people/heber-h-arcolezi.html"},
            ],
        },
        {
            "year": "2026",
            "venue": "AAAI",
            "title": "Beyond Patches: Mining Interpretable Part-Prototypes for Explainable AI",
            "url": "https://ojs.aaai.org/index.php/AAAI/article/view/41052",
            "figure_url": "https://arxiv.org/html/2504.12197v3/imgs/model-c.png",
            "figure_alt": [
                "Architecture of a model that extracts semantic part prototypes to explain image predictions.",
                "Architecture d’un modèle qui extrait des prototypes de parties sémantiques pour expliquer ses prédictions sur les images.",
            ],
            "credit": "Figure 2 · Alehdaghi et al., 2026",
            "license": "CC BY 4.0",
            "license_url": "https://creativecommons.org/licenses/by/4.0/",
            "summary": [
                "Introduces semantic part prototypes as an explanation of image-model decisions, addressing limits of heatmaps and rigid patch selection.",
                "Introduit des prototypes de parties sémantiques pour expliquer les décisions d’un modèle d’image, en réponse aux limites des cartes de chaleur et du choix rigide de fenêtres.",
            ],
            "ills_authors": [
                {"name": "Éric Granger", "path": "people/eric-granger.html"},
            ],
        },
        {
            "year": "2026",
            "venue": "TMLR",
            "title": "Extracting and Following Paths for Robust Relational Reasoning with Large Language Models",
            "url": "https://openreview.net/forum?id=EbELaNKmZK",
            "figure_url": "https://arxiv.org/html/2412.17963v2/PoT_figure_v5.png",
            "figure_alt": [
                "Path-of-Thoughts diagram: an LLM extracts a graph, selects a relation path and reasons over it, including an example with an extraction error.",
                "Schéma Path-of-Thoughts : un grand modèle de langue extrait un graphe, choisit un chemin relationnel et raisonne à partir de celui-ci, y compris avec une erreur d’extraction.",
            ],
            "credit": "Figure 1 · Zhang et al., 2026",
            "license": "CC BY 4.0",
            "license_url": "https://creativecommons.org/licenses/by/4.0/",
            "summary": [
                "Breaks relational reasoning into graph extraction, path finding and reasoning, then evaluates how the process handles errors in extracted relations.",
                "Décompose le raisonnement relationnel en extraction de graphe, recherche de chemin et raisonnement, puis évalue la robustesse aux erreurs d’extraction des relations.",
            ],
            "ills_authors": [
                {"name": "Mark Coates", "path": "people/mark-coates.html"},
            ],
        },
        {
            "year": "2026",
            "venue": "Preprint · arXiv",
            "title": "Training Fair Tabular Foundation Models",
            "url": "https://arxiv.org/abs/2608.14211",
            "figure_url": "https://arxiv.org/html/2608.14211v1/figure_step_1.png",
            "figure_alt": [
                "Diagram of fairness-aware task sampling used to train a tabular foundation model.",
                "Schéma de l’échantillonnage de tâches tenant compte de l’équité pour entraîner un modèle de fondation tabulaire.",
            ],
            "credit": "Figure 1 · Kenfack et al., 2026",
            "license": "CC BY 4.0",
            "license_url": "https://creativecommons.org/licenses/by/4.0/",
            "summary": [
                "Builds fairness constraints into tabular foundation-model training so predictions can be made with a single forward pass on new tasks.",
                "Intègre des contraintes d’équité à l’entraînement de modèles de fondation tabulaires afin de produire des prédictions en une seule passe sur de nouvelles tâches.",
            ],
            "ills_authors": [
                {"name": "Ulrich Aïvodji", "path": "people/ulrich-aivodji.html"},
            ],
        },
        {
            "year": "2023",
            "venue": "AIES",
            "title": "Beyond the ML Model: Applying Safety Engineering Frameworks to Text-to-Image Development",
            "url": "https://dl.acm.org/doi/10.1145/3600211.3604685",
            "figure_url": "https://arxiv.org/html/2307.10312v1/figures/STPAfigure1.png",
            "figure_alt": [
                "Steps in the STPA safety-analysis process applied to text-to-image system development.",
                "Étapes de l’analyse de sécurité STPA appliquée au développement de systèmes de génération texte-image.",
            ],
            "credit": "Figure 2 · Rismani et al., 2023",
            "license": "CC BY 4.0",
            "license_url": "https://creativecommons.org/licenses/by/4.0/",
            "summary": [
                "Applies FMEA and STPA safety-engineering methods to text-to-image development, identifying risks across data processing, system integration and use.",
                "Applique les méthodes d’ingénierie de sécurité FMEA et STPA au développement texte-image, et identifie les risques liés aux données, à l’intégration et à l’usage.",
            ],
            "ills_authors": [
                {"name": "AJung Moon", "path": "people/ajung-moon.html"},
            ],
        },
        {
            "year": "2024",
            "venue": "TMLR",
            "title": "Do not trust what you trust: Miscalibration in Semi-supervised Learning",
            "url": "https://openreview.net/forum?id=1WqLLYgBNt",
            "figure_url": "https://arxiv.org/html/2403.15567v1/images/RadarPlots.png",
            "figure_alt": [
                "Radar plots comparing uncertainty estimates from semi-supervised learning methods across several datasets.",
                "Graphiques radar comparant les estimations d’incertitude de méthodes d’apprentissage semi-supervisé sur plusieurs jeux de données.",
            ],
            "credit": "Figure 2 · Mishra et al., 2024",
            "license": "CC BY 4.0",
            "license_url": "https://creativecommons.org/licenses/by/4.0/",
            "summary": [
                "Shows how confident pseudo-labels can still be wrong in semi-supervised learning, and examines how uncertainty estimates can be improved.",
                "Montre que les pseudo-étiquettes confiantes peuvent rester erronées en apprentissage semi-supervisé, et étudie comment améliorer les estimations d’incertitude.",
            ],
            "ills_authors": [
                {"name": "Marco Pedersoli", "path": "people/marco-pedersoli.html"},
                {"name": "Ismail Ben Ayed", "path": "people/ismail-ben-ayed.html"},
                {"name": "José Dolz", "path": "people/jose-dolz.html"},
            ],
        },
    ],
    "multi-agent": [
        {
            "year": "2023",
            "venue": "CoLLAs · PMLR",
            "title": "Dealing With Non-stationarity in Decentralized Cooperative Multi-Agent Deep Reinforcement Learning via Multi-Timescale Learning",
            "url": "https://proceedings.mlr.press/v232/nekoei23a.html",
            "figure_url": "https://arxiv.org/html/2302.02792v2/MTL_unified.png",
            "figure_alt": [
                "Diagram relating independent, sequential and multi-timescale learning schedules for cooperative agents.",
                "Schéma comparant les calendriers d’apprentissage indépendant, séquentiel et à plusieurs échelles de temps pour des agents coopératifs.",
            ],
            "credit": "Figure 2 · Nekoei et al., 2023",
            "license": "CC0",
            "license_url": "https://creativecommons.org/publicdomain/zero/1.0/",
            "summary": [
                "Uses different learning timescales to address non-stationarity as cooperative agents update their policies at the same time.",
                "Utilise différentes échelles de temps d’apprentissage pour traiter la non-stationnarité lorsque des agents coopératifs mettent simultanément à jour leurs politiques.",
            ],
            "ills_authors": [
                {"name": "Aditya Mahajan", "path": "people/aditya-mahajan.html"},
            ],
        },
        {
            "year": "2025",
            "venue": "IEEE Robotics and Automation Letters",
            "title": "STAMP: Differentiable Task and Motion Planning via Stein Variational Gradient Descent",
            "url": "https://ieeexplore.ieee.org/document/10966056/",
            "figure_url": "https://arxiv.org/html/2310.01775v4/Figures/real_pusher.jpg",
            "figure_alt": [
                "Three robot plans for pushing a block from different directions, found by the STAMP task-and-motion planner.",
                "Trois plans de robot pour pousser un bloc depuis différentes directions, calculés par le planificateur de tâches et de mouvements STAMP.",
            ],
            "credit": "Figure 1 · Lee et al., 2025",
            "license": "CC BY 4.0",
            "license_url": "https://creativecommons.org/licenses/by/4.0/",
            "summary": [
                "Combines task-level search with geometric motion planning so candidate robot plans account for whether the motions are physically feasible.",
                "Combine la recherche de tâches à la planification géométrique des mouvements afin que les plans envisagés tiennent compte de leur faisabilité physique.",
            ],
            "ills_authors": [
                {"name": "Derek Nowrouzezahrai", "url": "https://www.mcgill.ca/ece/derek-nowrouzezahrai"},
            ],
        },
        {
            "year": "2023",
            "venue": "Preprint · arXiv",
            "title": "Improving Reinforcement Learning Training Regimes for Social Robot Navigation",
            "url": "https://arxiv.org/abs/2308.14947",
            "figure_url": "https://arxiv.org/html/2308.14947v2/img/envs/bl-sq-demo-10-agents.png",
            "figure_alt": [
                "Social-robot navigation scenario with ten agents moving through a crossing environment.",
                "Scénario de navigation sociale montrant dix agents se déplaçant dans un environnement de croisement.",
            ],
            "credit": "Figure 1b · Sigal et al., 2023",
            "license": "CC BY 4.0",
            "license_url": "https://creativecommons.org/licenses/by/4.0/",
            "summary": [
                "Studies whether robot-navigation policies trained with reinforcement learning generalize to richer social environments and human norms.",
                "Étudie si des politiques de navigation robotique apprises par renforcement se généralisent à des environnements sociaux plus riches et aux normes humaines.",
            ],
            "ills_authors": [
                {"name": "AJung Moon", "path": "people/ajung-moon.html"},
            ],
        },
        {
            "year": "2026",
            "venue": "Preprint · arXiv",
            "title": "H-WM: Robotic Task and Motion Planning Guided by Hierarchical World Model",
            "url": "https://arxiv.org/abs/2602.11291",
            "figure_url": "https://arxiv.org/html/2602.11291v3/fig1.png",
            "figure_alt": [
                "H-WM architecture: a hierarchical world model predicts robot subtask transitions and guides a vision-language-action controller.",
                "Architecture H-WM : un modèle du monde hiérarchique prédit les transitions entre sous-tâches robotiques et guide un contrôleur vision-langage-action.",
            ],
            "credit": "Figure 1 · Chen et al., 2026",
            "license": "CC BY-NC-SA 4.0",
            "license_url": "https://creativecommons.org/licenses/by-nc-sa/4.0/",
            "summary": [
                "Combines a hierarchical model of logical and visual state changes with low-level robot control to support longer-horizon task planning.",
                "Combine un modèle hiérarchique des changements d’état logiques et visuels avec le contrôle robotique de bas niveau pour planifier des tâches à plus long horizon.",
            ],
            "ills_authors": [
                {"name": "Mark Coates", "path": "people/mark-coates.html"},
            ],
        },
        {
            "year": "2026",
            "venue": "Preprint · arXiv",
            "title": "Latent Goal Prediction from Language for Model-Based Planning",
            "url": "https://arxiv.org/abs/2606.20627",
            "figure_url": "https://arxiv.org/html/2606.20627v4/lago_high_level.png",
            "figure_alt": [
                "LAGO predicts language-conditioned subgoals and action-conditioned state rollouts in a shared latent space.",
                "LAGO prédit des sous-objectifs conditionnés par le langage et des trajectoires d’états conditionnées par les actions dans un espace latent partagé.",
            ],
            "credit": "Figure 1 · Barbeau et al., 2026",
            "license": "CC BY 4.0",
            "license_url": "https://creativecommons.org/licenses/by/4.0/",
            "summary": [
                "Learns a latent predictive model that combines language goals with action-conditioned rollouts to help an agent plan without a separate generative model.",
                "Apprend un modèle prédictif latent qui combine des objectifs en langage et des trajectoires conditionnées par les actions, afin d’aider un agent à planifier sans modèle génératif séparé.",
            ],
            "ills_authors": [
                {"name": "Christian Desrosiers", "path": "people/christian-desrosiers.html"},
                {"name": "Nicolas Thome", "path": "people/nicolas-thome.html"},
            ],
        },
        {
            "year": "2026",
            "venue": "EACL System Demonstrations",
            "title": "SDialog: A Python Toolkit for End-to-End Agent Building, User Simulation, Dialog Generation, and Evaluation",
            "url": "https://aclanthology.org/2026.eacl-demo.23/",
            "figure_url": "https://arxiv.org/html/2506.10622v3/modules-shadow.png",
            "figure_alt": [
                "SDialog toolkit architecture, with eight modules grouped into auxiliary, core and output components.",
                "Architecture de la boîte à outils SDialog, avec huit modules organisés en composantes auxiliaires, centrales et de sortie.",
            ],
            "credit": "Figure 1 · Burdisso et al., 2026",
            "license": "CC BY 4.0",
            "license_url": "https://creativecommons.org/licenses/by/4.0/",
            "summary": [
                "An open-source toolkit for building and studying conversational agents, including multi-agent dialog simulation, generation and evaluation.",
                "Une boîte à outils libre pour créer et étudier des agents conversationnels, avec simulation multi-agents, génération et évaluation de dialogues.",
            ],
            "ills_authors": [
                {"name": "Ricard Marxer", "path": "people/ricard-marxer.html"},
            ],
        },
        {
            "year": "2026",
            "venue": "Preprint · arXiv",
            "title": "Continual Enterprise World Model Discovery in Dynamic Systems",
            "url": "https://arxiv.org/abs/2609.19551",
            "figure_url": "https://arxiv.org/html/2609.19551v1/CEWM_final.drawio.svg",
            "figure_alt": [
                "EnterpriseWorldShift diagram showing versions of an enterprise environment changing as business rules are added or modified.",
                "Schéma EnterpriseWorldShift montrant différentes versions d’un environnement d’entreprise lorsque des règles métier sont ajoutées ou modifiées.",
            ],
            "credit": "Figure 1 · Mishra et al., 2026",
            "license": "CC BY 4.0",
            "license_url": "https://creativecommons.org/licenses/by/4.0/",
            "summary": [
                "Studies how an agent can infer changing business rules in enterprise software and predict the effects of its actions as the system evolves.",
                "Étudie comment un agent peut inférer l’évolution des règles métier d’un logiciel d’entreprise et prévoir les effets de ses actions au fil des changements.",
            ],
            "ills_authors": [
                {"name": "Marco Pedersoli", "path": "people/marco-pedersoli.html"},
                {"name": "José Dolz", "path": "people/jose-dolz.html"},
            ],
        },
        {
            "year": "2026",
            "venue": "Preprint · arXiv",
            "title": "PrivacySkills: How Privacy Guidance Shapes Source Selection in LLM Agents",
            "url": "https://arxiv.org/abs/2609.35937",
            "figure_url": "https://arxiv.org/html/2609.35937v1/figures/overview4.png",
            "figure_alt": [
                "PrivacySkills scenario in which an agent can request information from a user or choose between public and confidential sources.",
                "Scénario PrivacySkills où un agent peut demander une information à la personne ou choisir entre des sources publiques et confidentielles.",
            ],
            "credit": "Figure 1 · Biechy et al., 2026",
            "license": "CC BY 4.0",
            "license_url": "https://creativecommons.org/licenses/by/4.0/",
            "summary": [
                "Tests how privacy instructions affect whether language-model agents choose public or confidential information sources to complete a task.",
                "Évalue comment les consignes de confidentialité influencent le choix d’agents fondés sur des modèles de langue entre sources publiques et confidentielles.",
            ],
            "ills_authors": [
                {"name": "Héber H. Arcolezi", "path": "people/heber-h-arcolezi.html"},
            ],
        },
    ],
    "healthcare": [
        {
            "year": "2025",
            "venue": "ICCV Workshops",
            "title": "Building a General SimCLR Self-Supervised Foundation Model Across Neurological Diseases to Advance 3D Brain MRI Diagnoses",
            "url": "https://ieeexplore.ieee.org/document/11375618/",
            "figure_url": "https://arxiv.org/html/2509.10620v1/brains.png",
            "figure_alt": [
                "Brain MRI slices from people with Alzheimer’s disease, Parkinson’s disease and a healthy control.",
                "Coupes d’IRM cérébrale de personnes atteintes de la maladie d’Alzheimer, de la maladie de Parkinson et d’un témoin en bonne santé.",
            ],
            "credit": "Figure 1 · Kaczmarek et al., 2025",
            "license": "CC BY 4.0",
            "license_url": "https://creativecommons.org/licenses/by/4.0/",
            "summary": [
                "Studies self-supervised foundation-model training across neurological conditions, with the goal of improving transfer to 3D brain-MRI diagnosis tasks.",
                "Étudie l’entraînement auto-supervisé d’un modèle de fondation sur plusieurs maladies neurologiques afin d’améliorer son transfert aux tâches diagnostiques sur IRM cérébrale 3D.",
            ],
            "ills_authors": [
                {"name": "Tal Arbel", "url": "https://www.mcgill.ca/ece/tal-arbel"},
            ],
        },
        {
            "year": "2024",
            "venue": "Medical Image Analysis",
            "title": "Boundary-aware information maximization for self-supervised medical image segmentation",
            "url": "https://linkinghub.elsevier.com/retrieve/pii/S1361841524000756",
            "figure_url": "https://arxiv.org/html/2202.02371v2/boundary-aware-figure/uncertanty/Fig1.png",
            "figure_alt": [
                "Boundary-aware clustering diagram showing how the method estimates cluster assignments and their uncertainty during self-supervised training.",
                "Schéma de regroupement sensible aux contours montrant comment la méthode estime les affectations aux groupes et leur incertitude pendant l’entraînement auto-supervisé.",
            ],
            "credit": "Figure 1 · Peng et al., 2024",
            "license": "CC BY 4.0",
            "license_url": "https://creativecommons.org/licenses/by/4.0/",
            "summary": [
                "Introduces boundary-aware information maximization for self-supervised medical segmentation when labelled images are limited.",
                "Introduit une maximisation de l’information sensible aux contours pour segmenter des images médicales sans annotations nombreuses.",
            ],
            "ills_authors": [
                {"name": "Christian Desrosiers", "path": "people/christian-desrosiers.html"},
                {"name": "Marco Pedersoli", "path": "people/marco-pedersoli.html"},
            ],
        },
        {
            "year": "2026",
            "venue": "IPMI",
            "title": "MAD-AD: Masked Diffusion for Unsupervised Brain Anomaly Detection",
            "url": "https://link.springer.com/10.1007/978-3-031-96625-5_10",
            "figure_url": "https://arxiv.org/html/2502.16943v3/masked-ddim-reverse.png",
            "figure_alt": [
                "Brain-image example of the reverse diffusion process, showing predicted anomaly masks and reconstructed image representations over several steps.",
                "Exemple cérébral du processus de diffusion inverse, avec les masques d’anomalie prédits et les représentations reconstruites à plusieurs étapes.",
            ],
            "credit": "Figure 2 · Beizaee et al., 2026",
            "license": "CC BY-NC-SA 4.0",
            "license_url": "https://creativecommons.org/licenses/by-nc-sa/4.0/",
            "summary": [
                "Uses masked diffusion to detect and localize brain anomalies without requiring labelled abnormal scans for training.",
                "Utilise la diffusion masquée pour détecter et localiser des anomalies cérébrales sans exiger d’IRM anormales annotées pour l’entraînement.",
            ],
            "ills_authors": [
                {"name": "José Dolz", "path": "people/jose-dolz.html"},
                {"name": "Christian Desrosiers", "path": "people/christian-desrosiers.html"},
            ],
        },
        {
            "year": "2024",
            "venue": "MICCAI",
            "title": "Few-Shot Adaptation of Medical Vision-Language Models",
            "url": "https://link.springer.com/10.1007/978-3-031-72390-2_52",
            "figure_url": "https://arxiv.org/html/2409.03868v1/fs_medical.png",
            "figure_alt": [
                "Benchmark comparison of few-shot adaptation methods for medical vision-language models across nine tasks.",
                "Comparaison sur neuf tâches de méthodes d’adaptation en few-shot de modèles vision-langage médicaux.",
            ],
            "credit": "Figure 1 · Shakeri et al., 2024",
            "license": "CC BY-NC-ND 4.0",
            "license_url": "https://creativecommons.org/licenses/by-nc-nd/4.0/",
            "summary": [
                "Studies how medical vision-language models can adapt to new tasks from a small number of labelled examples, across multiple modalities.",
                "Étudie comment des modèles vision-langage médicaux peuvent s’adapter à de nouvelles tâches à partir de peu d’exemples annotés et de plusieurs modalités.",
            ],
            "ills_authors": [
                {"name": "Ismail Ben Ayed", "path": "people/ismail-ben-ayed.html"},
                {"name": "José Dolz", "path": "people/jose-dolz.html"},
            ],
        },
        {
            "year": "2025",
            "venue": "Preprint · arXiv",
            "title": "DAFTED: Decoupled Asymmetric Fusion of Tabular and Echocardiographic Data for Cardiac Hypertension Diagnosis",
            "url": "https://arxiv.org/abs/2509.15990",
            "figure_url": "https://arxiv.org/html/2509.15990v1/figures/MuFDI_pipeline_prez.jpg",
            "figure_alt": [
                "DAFTED model pipeline for combining tabular patient information with echocardiographic data to predict cardiac hypertension.",
                "Pipeline du modèle DAFTED combinant des données tabulaires sur les patients et des données échocardiographiques pour prédire l’hypertension cardiaque.",
            ],
            "credit": "Figure 1 · Stym-Popper et al., 2025",
            "license": "CC BY 4.0",
            "license_url": "https://creativecommons.org/licenses/by/4.0/",
            "summary": [
                "Combines echocardiographic and tabular data asymmetrically, treating them as complementary sources for cardiac-hypertension diagnosis.",
                "Combine de façon asymétrique des données échocardiographiques et tabulaires, considérées comme complémentaires pour diagnostiquer l’hypertension cardiaque.",
            ],
            "ills_authors": [
                {"name": "Nicolas Thome", "path": "people/nicolas-thome.html"},
            ],
        },
        {
            "year": "2026",
            "venue": "WACV",
            "title": "CLIP-IT: CLIP-based Pairing of Histology Images with Privileged Textual Information",
            "url": "https://ieeexplore.ieee.org/document/11491958/",
            "figure_url": "https://arxiv.org/html/2504.16181v5/Fig/drawing.png",
            "figure_alt": [
                "CLIP-IT pairs each histology image with a semantically similar report from an unpaired text collection.",
                "CLIP-IT associe chaque image histologique à un compte rendu sémantiquement proche provenant d’une collection de textes non appariés.",
            ],
            "credit": "Figure 2 · Karimian et al., 2026",
            "license": "CC BY 4.0",
            "license_url": "https://creativecommons.org/licenses/by/4.0/",
            "summary": [
                "Uses unpaired pathology reports as privileged text to improve vision-language training for histology without requiring large paired datasets.",
                "Utilise des comptes rendus anatomopathologiques non appariés comme information textuelle auxiliaire pour améliorer l’apprentissage vision-langage en histologie.",
            ],
            "ills_authors": [
                {"name": "Éric Granger", "path": "people/eric-granger.html"},
                {"name": "Mohammadhadi Shateri", "path": "people/mohammadhadi-shateri.html"},
            ],
        },
        {
            "year": "2025",
            "venue": "NeurIPS · Datasets and Benchmarks",
            "title": "THUNDER: Tile-level Histopathology image UNDERstanding benchmark",
            "url": "https://papers.nips.cc/paper_files/paper/2025/hash/e3a2bd22ef74970b2fff74a16f806237-Abstract-Datasets_and_Benchmarks_Track.html",
            "figure_url": "https://arxiv.org/html/2507.07860v3/teaser.png",
            "figure_alt": [
                "THUNDER benchmark overview comparing pathology foundation models on downstream tasks, feature spaces and uncertainty.",
                "Vue d’ensemble de THUNDER, un banc d’essai comparant des modèles de fondation en pathologie selon les tâches, les espaces de caractéristiques et l’incertitude.",
            ],
            "credit": "Figure 1 · Marza et al., 2025",
            "license": "CC BY 4.0",
            "license_url": "https://creativecommons.org/licenses/by/4.0/",
            "summary": [
                "Introduces a tile-level histopathology benchmark for comparing foundation models on task performance, feature representations and uncertainty.",
                "Présente un banc d’essai d’images histopathologiques en tuiles pour comparer les modèles de fondation selon les tâches, les représentations et l’incertitude.",
            ],
            "ills_authors": [
                {"name": "Pablo Piantanida", "path": "people/pablo-piantanida.html"},
                {"name": "Christian Desrosiers", "path": "people/christian-desrosiers.html"},
                {"name": "José Dolz", "path": "people/jose-dolz.html"},
            ],
        },
        {
            "year": "2026",
            "venue": "Preprint · arXiv",
            "title": "Single-Exam Mammography Risk Prediction with Privileged History Distillation",
            "url": "https://arxiv.org/abs/2603.15814",
            "figure_url": "https://arxiv.org/html/2603.15814v2/Fig/t.png",
            "figure_alt": [
                "SEM-HD framework: a student model learns from longitudinal mammograms during training and uses one current exam at deployment.",
                "Cadre SEM-HD : un modèle étudiant apprend à partir de mammographies longitudinales à l’entraînement et utilise un seul examen lors du déploiement.",
            ],
            "credit": "Figure 2 · Karimian et al., 2026",
            "license": "CC BY 4.0",
            "license_url": "https://creativecommons.org/licenses/by/4.0/",
            "summary": [
                "Trains with longitudinal mammography history, then predicts future risk from one current screening exam when earlier images are unavailable at deployment.",
                "Entraîne le modèle avec l’historique mammographique, puis prédit le risque futur à partir d’un seul examen lorsque les images antérieures ne sont pas disponibles.",
            ],
            "ills_authors": [
                {"name": "Mohammadhadi Shateri", "path": "people/mohammadhadi-shateri.html"},
                {"name": "Éric Granger", "path": "people/eric-granger.html"},
            ],
        },
    ],
}
