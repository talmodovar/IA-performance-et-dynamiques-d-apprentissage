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
                # Si l'URL se termine par un tiret, un slash, ou si la continuation ressemble à un chemin
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

def linkify_text(text):
    """
    Rend cliquables tous les liens HTTP/HTTPS détectés dans le texte avec target="_blank".
    Échappe le texte environnant tout en préservant la ponctuation de fin.
    """
    pattern = re.compile(r'(https?://[^\s<>"\']+)')
    parts = []
    last_end = 0
    for m in pattern.finditer(text):
        before = text[last_end:m.start()]
        parts.append(html.escape(before))
        
        raw_url = m.group(1)
        trailing = ''
        while raw_url and raw_url[-1] in '.,;:?!)]"\'':
            trailing = raw_url[-1] + trailing
            raw_url = raw_url[:-1]
            
        href = raw_url
        parts.append(f'<a href="{html.escape(href)}" target="_blank" rel="noopener noreferrer">{html.escape(raw_url)}</a>{html.escape(trailing)}')
        last_end = m.end()
    parts.append(html.escape(text[last_end:]))
    return ''.join(parts)

def format_section_content_with_headings(sec_id, raw_text):
    """
    Formatte le texte d'une section:
    1. Détection et mise en forme des titres (h2, h3, h4) avec ID uniques
    2. Formatage des figures (notamment sur la page annexes avec retour à la ligne avant chaque Figure)
    3. Conversion de tous les liens en liens cliquables target="_blank"
    4. Formatage des listes, citations et notes
    """
    lines = [l.strip() for l in raw_text.splitlines()]
    
    # 1. Nettoyage des balises de page et numéros isolés
    filtered = []
    for l in lines:
        if l.startswith('<!-- Page') and l.endswith('-->'):
            continue
        if re.match(r'^\d{1,3}$', l):
            continue
        filtered.append(l)
        
    # 2. Réparation des URLs coupées par les retours à la ligne
    filtered = repair_urls_in_lines(filtered)
    
    # Table des titres pour sec_id
    toc_items = SECTIONS_TOC.get(sec_id, [])
    toc_by_clean = {}
    for item in toc_items:
        clean = re.sub(r'^[0-9a-z\.\-\–\s\(\)]+\s*', '', item['title']).strip().lower()
        if clean:
            toc_by_clean[clean] = item

    # Regex pour détection des titres
    RE_H2_NUM = re.compile(r'^(\d+\.\d+)\s+(.+)$')
    RE_H2_PAREN = re.compile(r'^(\d+\))\s+(.+)$')
    RE_H3_ALPHA = re.compile(r'^([a-z]\))\s+(.+)$', re.IGNORECASE)
    RE_H4_SUB = re.compile(r'^([a-z]\.\d+\)?)\s+(.+)$', re.IGNORECASE)
    RE_FIGURE = re.compile(r'^(Figure\s+\d+[\s\-\,\:])\s*(.*)$', re.IGNORECASE)
    RE_CONT = re.compile(r'\b(?:sur des|sur|de la|de|du|des|et|et des|vers une|pour|dans|au|aux|un|une|avec|–|-|:)\s*$', re.IGNORECASE)

    # Titres textuels reconnus spécifiquement
    SPECIAL_H2 = [
        "Genèse et problématique de recherche",
        "Introduction et problématique",
        "Bilan et perspectives",
        "Bilan personnel et perspectives",
        "Conclusion",
        "Conclusion générale du mémoire",
        "Conclusion de la Partie I",
        "Conclusion de la Partie II",
        "Conclusion de la Partie III",
        "Définition des termes utilisés",
        "Description des abréviations",
        "Description des abréviations utilisées",
        "Table des figures",
        "Table des matières",
        "Bibliographie / Webographie",
        "Bibliographie et Webographie annotée",
        "Rapports institutionnels et études scientifiques",
        "Ouvrages et articles académiques",
        "Webographie et ressources en ligne"
    ]
    SPECIAL_H3 = [
        "Qu'est-ce que l'IA ?",
        "IA versus programme informatique classique",
        "IA versus programme informatique classique :",
        "Histoire et chronologie de l'IA",
        "Évolution récente des performances",
        "Les grands modèles de langage (LLM)",
        "Les réseaux de neurones convolutifs (CNN)",
        "L'IA générative au-delà du texte",
        "L'IA prédictive et analytique",
        "L'apprentissage par renforcement",
        "Cas d'usages",
        "Cas d'usages :",
        "Une performance réellement augmentée, sous conditions",
        "Une performance réellement augmentée, mais sous conditions",
        "Limites, risques et conditions d'une intégration maîtrisée",
        "Limites, risques et conditions d’une intégration maîtrisée",
        "Réponse finale à la problématique",
        "Réponse à la problématique et perspectives"
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
        # 1. Correspondance exacte sur le titre complet
        for it in toc_items:
            if it['title'].lower() == title_text.lower():
                return it

        # 2. Correspondance sur le préfixe précis avec meilleur chevauchement de mots
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
                # Choisir celui qui a le plus de mots en commun
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

        # 3. Correspondance sur le texte sans préfixe
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
                if (text.startswith('«') and text.endswith('»')) or (text.startswith('"') and text.endswith('"')):
                    blocks.append(f'<blockquote><p>{linkify_text(text)}</p></blockquote>')
                elif text.startswith('•') or text.startswith('- ') or text.startswith('– '):
                    items = [it.strip() for it in re.split(r'\n?[•\-\–]\s*', text) if it.strip()]
                    li_html = ''.join(f'<li>{linkify_text(it)}</li>' for it in items)
                    blocks.append(f'<ul>{li_html}</ul>')
                else:
                    html_content = linkify_text(text)
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

        # Figure detection (annexes ou corps du texte)
        # Assure un retour à la ligne avant chaque Figure dans les annexes
        m_fig = RE_FIGURE.match(line)
        if m_fig:
            flush_p()
            prefix, caption = m_fig.groups()
            fig_text = f"{prefix} {caption}".strip()

            # Dans les annexes (Table des figures), grouper les lignes de description associées à cette figure
            if sec_id == "annexes":
                while (i + 1 < len(filtered) and 
                       filtered[i+1] and 
                       not RE_FIGURE.match(filtered[i+1]) and 
                       not RE_H2_PAREN.match(filtered[i+1]) and 
                       not RE_H2_NUM.match(filtered[i+1]) and 
                       not RE_H3_ALPHA.match(filtered[i+1])):
                    fig_text += " " + filtered[i+1]
                    i += 1

                clean_desc = re.sub(r'^Figure\s+\d+[\s\-\,\:]*\s*', '', fig_text, flags=re.IGNORECASE)
                clean_prefix = re.sub(r'[\s\-\,\:]+$', '', prefix)
                linked_desc = linkify_text(clean_desc)
                blocks.append(f'<p class="figure-item"><strong>{html.escape(clean_prefix)}</strong> — {linked_desc}</p>')
            else:
                clean_desc = re.sub(r'^Figure\s+\d+[\s\-\,\:]*\s*', '', fig_text, flags=re.IGNORECASE)
                clean_prefix = re.sub(r'[\s\-\,\:]+$', '', prefix)
                linked_desc = linkify_text(clean_desc)
                blocks.append(f'<p class="figure-callout"><strong>{html.escape(clean_prefix)}</strong> — {linked_desc}</p>')

            i += 1
            continue

        # Paragraphe normal
        current_p_lines.append(line)
        i += 1

    flush_p()
    return '\n'.join(blocks)

if __name__ == '__main__':
    print("Perfect parser module ready!")
