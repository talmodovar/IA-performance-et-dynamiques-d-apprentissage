import json
import re
import html

# Dictionnaire des sections officielles avec leurs sous-titres et niveaux
SECTIONS_TOC = {
    "introduction": [
        {"id": "intro-problematique", "title": "Genèse et problématique de recherche", "level": 2}
    ],
    "partie-0": [
        {"id": "sec-0-1", "title": "0.1 Définition et histoire de l'intelligence artificielle", "level": 2},
        {"id": "sub-0-1-1", "title": "Qu'est-ce que l'IA ?", "level": 3},
        {"id": "sub-0-1-2", "title": "IA versus programme informatique classique", "level": 3},
        {"id": "sub-0-1-3", "title": "Histoire et chronologie de l'IA", "level": 3},
        {"id": "sub-0-1-4", "title": "Évolution récente des performances", "level": 3},
        {"id": "sec-0-2", "title": "0.2 Panorama des grandes familles de technologies IA", "level": 2},
        {"id": "sub-0-2-1", "title": "Les grands modèles de langage (LLM)", "level": 3},
        {"id": "sub-0-2-2", "title": "Les réseaux de neurones convolutifs (CNN)", "level": 3},
        {"id": "sub-0-2-3", "title": "L'IA générative au-delà du texte", "level": 3},
        {"id": "sub-0-2-4", "title": "L'IA prédictive et analytique", "level": 3},
        {"id": "sub-0-2-5", "title": "L'apprentissage par renforcement", "level": 3},
        {"id": "sub-0-2-6", "title": "Cas d'usages", "level": 3}
    ],
    "partie-1": [
        {"id": "sec-1-1", "title": "1.1 Qu'est-ce que la performance ?", "level": 2},
        {"id": "sub-1-1-a", "title": "a) Les dimensions de la performance", "level": 3},
        {"id": "sub-1-1-b", "title": "b) L'IA déplace l'attente de performance", "level": 3},
        {"id": "sec-1-2", "title": "1.2 L'IA accélère : gains d'efficience sur des tâches maîtrisées", "level": 2},
        {"id": "sub-1-2-a", "title": "a) L'automatisation des tâches en entreprise", "level": 3},
        {"id": "sub-1-2-a1", "title": "a.1) Expérience personnelle, le cas du Crédit Agricole", "level": 4},
        {"id": "sub-1-2-a2", "title": "a.2) Un changement généralisé", "level": 4},
        {"id": "sub-1-2-b", "title": "b) L'accélération du travail scientifique et technique", "level": 3},
        {"id": "sec-1-3", "title": "1.3 L'IA rend possible : le franchissement de seuils de capacité", "level": 2},
        {"id": "sub-1-3-a1", "title": "a.1) Le seuil d'échelle : la structure des protéines (AlphaFold)", "level": 4},
        {"id": "sub-1-3-a2", "title": "a.2) Le seuil de difficulté : le problème de Navier–Stokes", "level": 4},
        {"id": "sub-1-3-b", "title": "b) Ce que le franchissement de seuil implique", "level": 3},
        {"id": "sec-1-4", "title": "1.4 L'IA personnalise : de la moyenne au sur-mesure", "level": 2},
        {"id": "sub-1-4-a", "title": "a) Digital twin, modélisation d'un athlète numérique (Enduraw)", "level": 3},
        {"id": "sub-1-4-b", "title": "b) La personnalisation comme nouveau standard", "level": 3},
        {"id": "sub-1-4-c", "title": "c) Ce que l'IA personnalise réellement : le cas Duolingo", "level": 3},
        {"id": "sec-1-concl", "title": "Conclusion de la Partie I", "level": 2}
    ],
    "partie-2": [
        {"id": "sec-2-1", "title": "2.1 Apprendre avec l'IA : la transformation de l'acte d'apprendre", "level": 2},
        {"id": "sub-2-1-a", "title": "a) La disponibilité permanente d'un interlocuteur cognitif", "level": 3},
        {"id": "sub-2-1-b", "title": "b) Le déplacement de la charge cognitive", "level": 3},
        {"id": "sub-2-1-b1", "title": "b.1) La théorie de la charge cognitive (Sweller)", "level": 4},
        {"id": "sub-2-1-b2", "title": "b.2) Comparatif : apprentissage classique / apprentissage avec IA générative", "level": 4},
        {"id": "sub-2-1-c", "title": "c) Retour d'expérience : apprendre avec l'IA sur douze mois", "level": 3},
        {"id": "sec-2-2", "title": "2.2 Nouveau rôle de l'enseignement et des organisations", "level": 2},
        {"id": "sub-2-2-a", "title": "a) Les solutions de l'enseignement face à l'IA", "level": 3},
        {"id": "sub-2-2-b", "title": "b) L'apprentissage organisationnel : le cas du Crédit Agricole", "level": 3},
        {"id": "sec-2-3", "title": "2.3 L’IA, future discipline à part entière : vers une nouvelle culture générale", "level": 2},
        {"id": "sub-2-3-a", "title": "a) Une trajectoire comparable à celle de la digitalisation", "level": 3},
        {"id": "sub-2-3-b", "title": "b) Une compétence qui se spécialise selon les métiers", "level": 3},
        {"id": "sub-2-3-c", "title": "c) Apprendre avant de déléguer", "level": 3},
        {"id": "sec-2-concl", "title": "Conclusion de la Partie II", "level": 2}
    ],
    "partie-3": [
        {"id": "sec-3-1", "title": "3.1 Risques pour les compétences humaines", "level": 2},
        {"id": "sub-3-1-a", "title": "a) Quand le déplacement de l’effort devient suppression de l’effort", "level": 3},
        {"id": "sub-3-1-b", "title": "b) De l’assistance à l’érosion du socle : illusion de compétence et dépendance cognitive", "level": 3},
        {"id": "sub-3-1-c", "title": "c) Le risque de la boucle solitaire", "level": 3},
        {"id": "sub-3-1-d", "title": "d) Une vulnérabilité inégale entre experts et novices", "level": 3},
        {"id": "sec-3-2", "title": "3.2 Coûts de transition et impacts organisationnels", "level": 2},
        {"id": "sub-3-2-a", "title": "a) Le coût réel de l’IA : investissement, ROI et incertitude économique", "level": 3},
        {"id": "sub-3-2-b", "title": "b) La dette de compétence : déployer plus vite que former", "level": 3},
        {"id": "sub-3-2-c", "title": "c) Le coût humain et organisationnel de la transition", "level": 3},
        {"id": "sub-3-2-d", "title": "d) L’homogénéisation des pratiques et la question de la responsabilité", "level": 3},
        {"id": "sub-3-2-e", "title": "e) Le coût environnemental : une double exposition financière et RSE", "level": 3},
        {"id": "sec-3-3", "title": "3.3 Conditions d'une intégration réussie et nouveaux rôles", "level": 2},
        {"id": "sub-3-3-a", "title": "a) Principes directeurs d'une intégration maîtrisée et performante", "level": 3},
        {"id": "sub-3-3-a1", "title": "a.1) Les principes d’une intégration maîtrisée dans la performance", "level": 4},
        {"id": "sub-3-3-a2", "title": "a.2) Les principes d’une intégration maîtrisée dans l’apprentissage", "level": 4},
        {"id": "sub-3-3-b", "title": "b) Projet personnel développé : présentation de LINA", "level": 3},
        {"id": "sub-3-3-b1", "title": "b.1) Présentation du concept", "level": 4},
        {"id": "sub-3-3-b2", "title": "b.2) Les points d’amélioration", "level": 4},
        {"id": "sub-3-3-b3", "title": "b.3) Retour des professionnels", "level": 4},
        {"id": "sec-3-concl", "title": "Conclusion de la Partie III", "level": 2}
    ],
    "conclusion": [
        {"id": "concl-bilan", "title": "Bilan et perspectives", "level": 2},
        {"id": "concl-generale", "title": "Conclusion générale du mémoire", "level": 2},
        {"id": "concl-performance", "title": "Une performance réellement augmentée, mais sous conditions", "level": 3},
        {"id": "concl-limites", "title": "Limites, risques et conditions d’une intégration maîtrisée", "level": 3},
        {"id": "concl-reponse", "title": "Réponse à la problématique et perspectives", "level": 3}
    ],
    "glossaire": [
        {"id": "glo-termes", "title": "Définition des termes utilisés", "level": 2},
        {"id": "glo-abrev", "title": "Description des abréviations utilisées", "level": 2}
    ],
    "bibliographie": [
        {"id": "bib-webographie", "title": "Bibliographie et Webographie annotée", "level": 2}
    ],
    "annexes": [
        {"id": "ann-figures", "title": "Table des figures", "level": 2},
        {"id": "ann-retex", "title": "1) RETEX, Retour d’expérience au Crédit Agricole", "level": 2},
        {"id": "ann-retex-a", "title": "a) Contexte et méthode", "level": 3},
        {"id": "ann-retex-b", "title": "b) Ce que le terrain confirme de la thèse", "level": 3},
        {"id": "ann-retex-c", "title": "c) Ce que le terrain nuance ou complexifie", "level": 3},
        {"id": "ann-usap", "title": "2) Entretien avec le préparateur physique de l'USAP", "level": 2},
        {"id": "ann-usap-a", "title": "a) Contexte et objectif de l'entretien", "level": 3},
        {"id": "ann-usap-b", "title": "b) Résultats et enseignements", "level": 3},
        {"id": "ann-usap-c", "title": "c) Ce que ce terrain dit de la thèse générale", "level": 3},
        {"id": "ann-pedago", "title": "3) Entretien avec des professionnels de la pédagogie sur LINA", "level": 2},
        {"id": "ann-pedago-a", "title": "a) Protocole et objectif", "level": 3},
        {"id": "ann-pedago-b", "title": "b) Résultats et enseignements", "level": 3},
        {"id": "ann-pedago-c", "title": "c) Ce que ce retour dit de la thèse générale", "level": 3},
        {"id": "ann-enduraw", "title": "4) Entretien avec Anthony SALIOU, Enduraw", "level": 2},
        {"id": "ann-enduraw-a", "title": "a) Protocole et objectif", "level": 3},
        {"id": "ann-enduraw-b", "title": "b) Résultats et enseignements", "level": 3},
        {"id": "ann-enduraw-c", "title": "c) Ce que ce retour dit de la thèse générale", "level": 3},
        {"id": "ann-cam", "title": "5) Entretien avec Jean-Baptiste MERIEM, Crédit Agricole Assurances", "level": 2},
        {"id": "ann-cam-a", "title": "a) Protocole et objectif", "level": 3},
        {"id": "ann-cam-b", "title": "b) Résultats et enseignements", "level": 3},
        {"id": "ann-cam-c", "title": "c) Ce que ce retour dit de la thèse générale", "level": 3}
    ]
}

# Fichiers images des figures situés dans assets/images/figures/
FIGURE_ASSETS = {
    1: "Figure1.png",
    2: "Figure2.png",
    3: "Figure3.png",
    4: "Figure4.png",
    5: "Figure5.png",
    6: "Figure6.png",
    7: "Figure7.png",
    8: "Figure8.jpg",
    9: "Figure9.jpg",
    10: "Figure10.png",
    11: "Figure11.png",
    12: "Figure12.png"
}

# Chapitres d'intégration pour chaque figure
FIGURE_CHAPTERS = {
    1: "partie-0", 2: "partie-0", 3: "partie-0",
    4: "partie-1", 5: "partie-1", 6: "partie-1", 7: "partie-1",
    8: "partie-2", 9: "partie-2",
    10: "partie-3", 11: "partie-3", 12: "partie-3"
}

# Légendes complètes canoniques issues du mémoire
FIGURE_CAPTIONS = {
    1: "Top model performance is converging, with 4 companies now clustered within 25 Elo points (inspired by chess ratings) when rated against one another by human voting in the Arena Leaderboard and benchmark. The 2026 AI Index Report",
    2: "Comment les couleurs sont transformées en couleurs",
    3: "Comment les couleurs sont transformées en couleurs part2",
    4: "Résultats de l'enquête FELIX juillet 2026 sur les testeurs de l'outils",
    5: "Qualité des prévisions météorologiques sur les deux dernières décennies en termes de corrélation des anomalies du géo-potentiel à 500hPa pour l’hémisphère nord, en été (Summer) et en hiver (Winter). Les résultats d’AIFS pour l’année 2023 sont indiqués",
    6: "University of Pittsburgh, AlphaFold Data Copyright (2022) DeepMind Technologies Limited., 3D visualization of AlphaFold structure prediction for Programmed cell death 1 ligand 1 (PDL1) protein.",
    7: "Instantané d’un mouvement local incompressible. L’orange indique une rotation angulaire plus rapide ; le bleu sarcelle, une rotation plus lente. La vitesse de circulation dépend aussi du rayon. Les trajectoires montrent une spirale vers l’intérieur et un étirement axial.",
    8: "Photo de l'auteur août 2025",
    9: "Photo de l'auteur août 2024",
    10: "Stanford University, The 2026 AI Index Report, Cumulative Public Spending on AI Contracts in European Countries",
    11: "LINA, profil d'apprentissage d'un élève",
    12: "LINA, interface professeur, gestion de la classe"
}

MONTHS = r'(?:janvier|f[ée]vrier|mars|avril|mai|may|juin|june|juillet|july|ao[ûu]t|august|septembre|september|octobre|october|novembre|november|d[ée]cembre|december)'

# Expression régulière pour découper plusieurs citations de sources présentes dans un même bloc de texte
RE_SOURCE_SPLIT = re.compile(
    r'(?<=\S)\s+(?='
    r'[¹²³⁴⁵⁶⁷⁸⁹⁰]+(?:\s*[A-ZÀÂÄÉÈÊËÎÏÔÖÙÛÜŸÇ«"“]|\s*https?:)'
    r'|'
    r'(?!(?:[234]D|[48]K|\d+B|\d+(?:e|ème|er|ère|nd|th|rd|st))\b)[1-9]\d?(?=[A-ZÀÂÄÉÈÊËÎÏÔÖÙÛÜŸÇ«"“]|https?:)'
    r'|'
    r'(?<=[.\?!»\)"\'’])\s*(?!(?:[234]D|[48]K|\d+B|\d+(?:e|ème|er|ère|nd|th|rd|st))\b)[1-9]\d?\s+(?!' + MONTHS + r'\b)(?:[A-ZÀÂÄÉÈÊËÎÏÔÖÙÛÜŸÇ«"“]|https?:)'
    r')'
)

def is_source_citation(text):
    """
    Détermine si une ligne ou un fragment de texte correspond à une citation de source ou note de bas de page.
    """
    t = text.strip()
    if re.match(r'^[¹²³⁴⁵⁶⁷⁸⁹⁰]+', t):
        return True
    
    # Exclusion des nombres ordinaux (10ème, 1er), tailles de modèles (8B, 70B), dimensions (3D, 4K)
    if re.match(r'^(?:[234]D|[48]K|\d+B|\d+(?:e|ème|er|ère|nd|th|rd|st))\b', t, re.IGNORECASE):
        return False

    # Exclusion des phrases narratives commençant par un auteur suivi d'un verbe (ex: 1Autor y voit..., 2Fabrice Popineau documente...)
    if re.match(r'^[1-9]\d?\s*[A-ZÀÂÄÉÈÊËÎÏÔÖÙÛÜŸÇa-z\.\-]+(?:\s+[A-ZÀÂÄÉÈÊËÎÏÔÖÙÛÜŸÇa-z\.\-]+)?\s+[a-z]{1,10}\b', t):
        if not re.search(r'\b(?:et al\.|Database|Report|Press|arXiv|interview|entretien|conférence)\b', t[:40], re.IGNORECASE) and not re.search(r'[«"“]', t[:40]):
            return False
        
    m = re.match(r'^[1-9]\d?\s*(?:[A-ZÀÂÄÉÈÊËÎÏÔÖÙÛÜŸÇ«"“]|https?:)', t)
    if m:
        # 1. Contient une URL ou archive
        if re.search(r'https?://|www\.|arxiv\.org|youtube\.com', t):
            return True
        # 2. Citations institutionnelles ou titres directs
        if re.match(r'^[1-9]\d?\s*(?:[«"“]|Wikipédia|Wikipedia|YouTube|ECMWF|NASA|OpenAI|AlphaFold|Stanford|Union|Université|University|Le Monde|Le Quotidien|Académie|Cnam|École|Classement|Prévisions)', t, re.IGNORECASE):
            return True
        # 3. Auteur avec titre entre guillemets ou date de publication
        if re.search(r'[«"“]', t) and re.search(r'\b(?:19\d\d|20\d\d)\b', t):
            return True
        # 4. Termes académiques de citation
        if re.search(r'\b(?:et al\.|Database|Report|Press|éd\.|vol\.|pp?\.|arXiv|interview|entretien|conférence|webinaire)\b', t, re.IGNORECASE):
            return True
            
    return False

def repair_urls_in_lines(lines):
    """
    Répare les URLs coupées sur deux lignes par l'extraction pypdf.
    Exemple: 'https://storage.googleapis.com/deepmind-' suivi de 'media/LearnLM/...'
    """
    new_lines = []
    i = 0
    while i < len(lines):
        line = lines[i]
        m = re.search(r'(https?://[^\s<>"]+)$', line)
        if m and i + 1 < len(lines):
            url_part = m.group(1)
            next_l = lines[i+1].strip()
            m_next = re.match(r'^([a-zA-Z0-9_\-\./\?&=%#]+)(\s+.*)?$', next_l)
            if m_next:
                cont = m_next.group(1)
                rest = m_next.group(2) or ""
                if url_part.endswith('-') or url_part.endswith('/') or '/' not in url_part[8:] or '.' in cont or '/' in cont:
                    repaired_url = url_part + cont
                    line = line[:m.start(1)] + repaired_url
                    if rest.strip():
                        new_lines.append(line)
                        lines[i+1] = rest.strip()
                        i += 1
                        continue
                    else:
                        i += 1
        new_lines.append(line)
        i += 1
    return new_lines

URL_PATTERN = re.compile(r'((?:https?://|www\.|(?:[a-zA-Z0-9_\-]+\.)+(?:com|org|fr|edu|io|ai|net)/)[^\s<>"\']+[^\s<>"\',;:?!.\)\]])')

def linkify_text(text):
    """
    Rend cliquables tous les liens HTTP/HTTPS ou noms de domaine détectés (ex: youtube.com) avec target="_blank".
    Échappe le texte environnant tout en préservant la ponctuation de fin.
    """
    parts = []
    last_end = 0
    for m in URL_PATTERN.finditer(text):
        before = text[last_end:m.start()]
        parts.append(html.escape(before))
        
        raw_url = m.group(1)
        trailing = ''
        while raw_url and raw_url[-1] in '.,;:?!)]"\'':
            trailing = raw_url[-1] + trailing
            raw_url = raw_url[:-1]
            
        href = raw_url if raw_url.startswith(('http://', 'https://')) else f'https://{raw_url}'
        parts.append(f'<a href="{html.escape(href)}" target="_blank" rel="noopener noreferrer">{html.escape(raw_url)}</a>{html.escape(trailing)}')
        last_end = m.end()
    parts.append(html.escape(text[last_end:]))
    return ''.join(parts)

def format_section_content_with_headings(sec_id, raw_text):
    """
    Formatte le texte d'une section:
    1. Détection et mise en forme des titres (h2, h3, h4) avec ID uniques
    2. Intégration des figures avec images réelles et légendes canoniques
    3. Séparation de chaque source citée sur sa propre ligne avec mise en page dédiée
    4. Conversion de tous les liens en liens cliquables target="_blank"
    """
    lines = [l.strip() for l in raw_text.splitlines()]
    
    # Nettoyage des balises de page et numéros isolés
    filtered = []
    for l in lines:
        if l.startswith('<!-- Page') and l.endswith('-->'):
            continue
        if re.match(r'^\d{1,3}$', l):
            continue
        filtered.append(l)
        
    filtered = repair_urls_in_lines(filtered)
    
    toc_items = SECTIONS_TOC.get(sec_id, [])

    # Regex pour détection des titres
    RE_H2_NUM = re.compile(r'^(\d+\.\d+)\s+(.+)$')
    RE_H2_PAREN = re.compile(r'^(\d+\))\s+(.+)$')
    RE_H3_ALPHA = re.compile(r'^([a-z]\))\s+(.+)$', re.IGNORECASE)
    RE_H4_SUB = re.compile(r'^([a-z]\.\d+\)?)\s+(.+)$', re.IGNORECASE)
    RE_FIGURE = re.compile(r'^(Figure\s+\d+[\s\-\,\:]*)\s*(.*)$', re.IGNORECASE)
    RE_CONT = re.compile(r'\b(?:sur des|sur|de la|de|du|des|et|et des|vers une|pour|dans|au|aux|un|une|avec|–|-|:)\s*$', re.IGNORECASE)

    SPECIAL_H2 = [
        "Genèse et problématique de recherche", "Introduction et problématique",
        "Bilan et perspectives", "Bilan personnel et perspectives", "Conclusion",
        "Conclusion générale du mémoire", "Conclusion de la Partie I", "Conclusion de la Partie II",
        "Conclusion de la Partie III", "Définition des termes utilisés", "Description des abréviations",
        "Description des abréviations utilisées", "Table des figures", "Table des matières",
        "Bibliographie / Webographie", "Bibliographie et Webographie annotée",
        "Rapports institutionnels et études scientifiques", "Ouvrages et articles académiques",
        "Webographie et ressources en ligne"
    ]
    SPECIAL_H3 = [
        "Qu'est-ce que l'IA ?", "IA versus programme informatique classique",
        "IA versus programme informatique classique :", "Histoire et chronologie de l'IA",
        "Évolution récente des performances", "Les grands modèles de langage (LLM)",
        "Les réseaux de neurones convolutifs (CNN)", "L'IA générative au-delà du texte",
        "L'IA prédictive et analytique", "L'apprentissage par renforcement", "Cas d'usages",
        "Cas d'usages :", "Une performance réellement augmentée, sous conditions",
        "Une performance réellement augmentée, mais sous conditions",
        "Limites, risques et conditions d'une intégration maîtrisée",
        "Limites, risques et conditions d’une intégration maîtrisée",
        "Réponse finale à la problématique", "Réponse à la problématique et perspectives"
    ]

    used_ids = set()

    def get_unique_id(base_id):
        cand = base_id
        count = 2
        while cand in used_ids:
            cand = f"{base_id}-{count}"
            count += 1
        used_ids.add(cand)
        return cand

    def find_toc_item(title_text):
        for it in toc_items:
            if it['title'].lower() == title_text.lower():
                return it

        m_p = re.match(r'^([0-9a-z\.\-\–\(\)]+)\s*', title_text, re.IGNORECASE)
        pref = m_p.group(1).lower().rstrip('.)-') if m_p else ''
        clean_text = re.sub(r'^[0-9a-z\.\-\–\s\(\)]+\s*', '', title_text).strip().lower()
        if pref:
            candidates = []
            for it in toc_items:
                m_it = re.match(r'^([0-9a-z\.\-\–\(\)]+)\s*', it['title'], re.IGNORECASE)
                it_pref = m_it.group(1).lower().rstrip('.)-') if m_it else ''
                if pref == it_pref:
                    candidates.append(it)
            if len(candidates) == 1:
                return candidates[0]
            elif len(candidates) > 1:
                words = set(w for w in clean_text.split() if len(w) > 2)
                best_it = candidates[0]
                best_overlap = -1
                for it in candidates:
                    it_clean = re.sub(r'^[0-9a-z\.\-\–\s\(\)]+\s*', '', it['title']).strip().lower()
                    it_words = set(w for w in it_clean.split() if len(w) > 2)
                    overlap = len(words & it_words)
                    if overlap > best_overlap:
                        best_overlap = overlap
                        best_it = it
                return best_it

        for it in toc_items:
            it_clean = re.sub(r'^[0-9a-z\.\-\–\s\(\)]+\s*', '', it['title']).strip().lower()
            if clean_text == it_clean or (len(clean_text) > 8 and clean_text in it_clean) or (len(it_clean) > 8 and it_clean in clean_text):
                return it
        return None

    def make_slug(title_text):
        slug = re.sub(r'[^a-zA-Z0-9]+', '-', title_text.lower()).strip('-')
        return slug[:40]

    blocks = []
    current_p_lines = []

    def flush_p():
        nonlocal current_p_lines
        if current_p_lines:
            text = ' '.join(current_p_lines).strip()
            if text:
                # Découpage si une ou plusieurs sources sont présentes dans le texte
                parts = RE_SOURCE_SPLIT.split(text)
                for part in parts:
                    p_clean = part.strip()
                    if not p_clean:
                        continue
                    if is_source_citation(p_clean):
                        html_content = linkify_text(p_clean)
                        blocks.append(f'<p class="source-citation">{html_content}</p>')
                    elif (p_clean.startswith('«') and p_clean.endswith('»')) or (p_clean.startswith('"') and p_clean.endswith('"')):
                        blocks.append(f'<blockquote><p>{linkify_text(p_clean)}</p></blockquote>')
                    elif p_clean.startswith('•') or p_clean.startswith('- ') or p_clean.startswith('– '):
                        items = [it.strip() for it in re.split(r'\n?[•\-\–]\s*', p_clean) if it.strip()]
                        li_html = ''.join(f'<li>{linkify_text(it)}</li>' for it in items)
                        blocks.append(f'<ul>{li_html}</ul>')
                    else:
                        html_content = linkify_text(p_clean)
                        html_content = re.sub(r'\[(\d+)\]', r'<sup><a href="#note-\1" class="footnote-ref">[\1]</a></sup>', html_content)
                        blocks.append(f'<p>{html_content}</p>')
            current_p_lines = []

    i = 0
    while i < len(filtered):
        line = filtered[i]
        if not line:
            flush_p()
            i += 1
            continue

        # Ignore la répétition brute du titre de la partie en tout début de texte
        if line.startswith("PARTIE ") and ("Comprendre l'IA" in line or "L'IA comme" in line):
            i += 1
            continue

        # Titres H4: a.1), b.2), b.3), etc.
        m_h4 = RE_H4_SUB.match(line)
        if m_h4:
            flush_p()
            prefix, rest_title = m_h4.groups()
            full_title = f"{prefix} {rest_title}".strip()
            if i + 1 < len(filtered) and RE_CONT.search(rest_title):
                full_title += " " + filtered[i+1]
                i += 1
            
            toc_match = find_toc_item(full_title)
            base_id = toc_match['id'] if toc_match else f"sub-{make_slug(full_title)}"
            hid = get_unique_id(base_id)
            disp_title = toc_match['title'] if toc_match else full_title
            blocks.append(f'<h4 id="{hid}">{html.escape(disp_title)}</h4>')
            i += 1
            continue

        # Titres H3: a), b), c), etc.
        m_h3 = RE_H3_ALPHA.match(line)
        if m_h3:
            flush_p()
            prefix, rest_title = m_h3.groups()
            full_title = f"{prefix} {rest_title}".strip()
            if i + 1 < len(filtered) and RE_CONT.search(rest_title):
                full_title += " " + filtered[i+1]
                i += 1
                
            toc_match = find_toc_item(full_title)
            base_id = toc_match['id'] if toc_match else f"sub-{make_slug(full_title)}"
            hid = get_unique_id(base_id)
            disp_title = toc_match['title'] if toc_match else full_title
            blocks.append(f'<h3 id="{hid}">{html.escape(disp_title)}</h3>')
            i += 1
            continue

        # Titres H2: 1), 2), 3), etc.
        m_h2_p = RE_H2_PAREN.match(line)
        if m_h2_p:
            flush_p()
            prefix, rest_title = m_h2_p.groups()
            full_title = f"{prefix} {rest_title}".strip()
            if i + 1 < len(filtered) and RE_CONT.search(rest_title):
                full_title += " " + filtered[i+1]
                i += 1
                
            toc_match = find_toc_item(full_title)
            base_id = toc_match['id'] if toc_match else f"sec-{make_slug(full_title)}"
            hid = get_unique_id(base_id)
            disp_title = toc_match['title'] if toc_match else full_title
            blocks.append(f'<h2 id="{hid}">{html.escape(disp_title)}</h2>')
            i += 1
            continue

        # Titres H2: 1.1, 1.2, 0.1, etc.
        m_h2_n = RE_H2_NUM.match(line)
        if m_h2_n:
            flush_p()
            prefix, rest_title = m_h2_n.groups()
            full_title = f"{prefix} {rest_title}".strip()
            if i + 1 < len(filtered) and RE_CONT.search(rest_title):
                full_title += " " + filtered[i+1]
                i += 1
                
            toc_match = find_toc_item(full_title)
            base_id = toc_match['id'] if toc_match else f"sec-{make_slug(full_title)}"
            hid = get_unique_id(base_id)
            disp_title = toc_match['title'] if toc_match else full_title
            blocks.append(f'<h2 id="{hid}">{html.escape(disp_title)}</h2>')
            i += 1
            continue

        # Titres H2 textuels spéciaux
        is_special_h2 = False
        for sp in SPECIAL_H2:
            if line.lower() == sp.lower() or line.lower().startswith(sp.lower()):
                flush_p()
                toc_match = find_toc_item(sp)
                base_id = toc_match['id'] if toc_match else f"sec-{make_slug(sp)}"
                hid = get_unique_id(base_id)
                blocks.append(f'<h2 id="{hid}">{html.escape(sp)}</h2>')
                is_special_h2 = True
                break
        if is_special_h2:
            i += 1
            continue

        # Titres H3 textuels spéciaux
        is_special_h3 = False
        for sp in SPECIAL_H3:
            if line.lower() == sp.lower() or line.lower().startswith(sp.lower().rstrip(':')):
                flush_p()
                toc_match = find_toc_item(sp)
                base_id = toc_match['id'] if toc_match else f"sub-{make_slug(sp)}"
                hid = get_unique_id(base_id)
                blocks.append(f'<h3 id="{hid}">{html.escape(sp.rstrip(" :"))}</h3>')
                is_special_h3 = True
                break
        if is_special_h3:
            i += 1
            continue

        # Détection des Figures (annexes ou corps du texte)
        m_fig = RE_FIGURE.match(line)
        if m_fig:
            flush_p()
            prefix, caption = m_fig.groups()
            m_num = re.search(r'\d+', prefix)
            fig_num = int(m_num.group(0)) if m_num else None

            # Dans les annexes (Table des figures)
            if sec_id == "annexes":
                fig_text = f"{prefix} {caption}".strip()
                while (i + 1 < len(filtered) and 
                       filtered[i+1] and 
                       not RE_FIGURE.match(filtered[i+1]) and 
                       not RE_H2_PAREN.match(filtered[i+1]) and 
                       not RE_H2_NUM.match(filtered[i+1]) and 
                       not RE_H3_ALPHA.match(filtered[i+1])):
                    fig_text += " " + filtered[i+1]
                    i += 1

                clean_desc = re.sub(r'^Figure\s+\d+[\s\-\,\:]*\s*', '', fig_text, flags=re.IGNORECASE)
                clean_desc = re.sub(r'\s*\.{3,}\s*\d+\s*$', '', clean_desc)
                clean_prefix = f"Figure {fig_num}" if fig_num else prefix.strip(' -:,')
                canonical = FIGURE_CAPTIONS.get(fig_num, clean_desc)
                linked_desc = linkify_text(canonical)
                target_chap = FIGURE_CHAPTERS.get(fig_num, "annexes")
                link_target = f"{target_chap}.html#fig-{fig_num}" if fig_num else "#"
                blocks.append(f'<p class="figure-item"><a href="{link_target}"><strong>{html.escape(clean_prefix)}</strong></a> — {linked_desc}</p>')
            else:
                # Dans les chapitres de lecture (partie-0, partie-1, partie-2, partie-3)
                canonical = FIGURE_CAPTIONS.get(fig_num, caption)
                words = set(re.findall(r'\w+', canonical.lower()))
                while i + 1 < len(filtered):
                    next_l = filtered[i+1].strip()
                    if not next_l:
                        break
                    if re.match(r'^(?:Figure\s+\d+|[a-z]\)|[a-z]\.\d+|\d+\.|\d+\))', next_l, re.IGNORECASE):
                        break
                    if any(next_l.lower().startswith(sp.lower().rstrip(':')) for sp in SPECIAL_H2 + SPECIAL_H3):
                        break
                    next_words = set(re.findall(r'\w+', next_l.lower()))
                    overlap = len(words & next_words)
                    if overlap >= min(3, len(next_words)) and (overlap / max(1, len(next_words)) > 0.4 or next_l.lower() in canonical.lower()):
                        i += 1
                    else:
                        break

                img_file = FIGURE_ASSETS.get(fig_num)
                clean_prefix = f"Figure {fig_num}" if fig_num else prefix.strip(' -:,')
                linked_desc = linkify_text(canonical)
                if img_file:
                    blocks.append(f'''<figure class="reader-figure-card" id="fig-{fig_num}">
  <div class="figure-img-container">
    <img src="../assets/images/figures/{img_file}" alt="{html.escape(clean_prefix)} — {html.escape(canonical)}" class="figure-img" loading="lazy">
  </div>
  <figcaption class="figure-caption">
    <strong>{html.escape(clean_prefix)}</strong> — {linked_desc}
  </figcaption>
</figure>''')
                else:
                    blocks.append(f'<p class="figure-callout"><strong>{html.escape(clean_prefix)}</strong> — {linked_desc}</p>')

            i += 1
            continue

        # Citation de source / note isolée
        if is_source_citation(line):
            flush_p()
            current_p_lines.append(line)
            i += 1
            continue

        # Paragraphe normal
        current_p_lines.append(line)
        i += 1

    flush_p()
    return '\n'.join(blocks)

if __name__ == '__main__':
    print("Perfect parser module ready!")
