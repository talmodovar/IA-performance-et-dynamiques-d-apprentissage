import json
import re
import html

# Dictionnaire des sections officielles avec leurs sous-titres
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
        {"id": "sec-1-2", "title": "1.2 L'IA accélère : gains d'efficience sur tâches maîtrisées", "level": 2},
        {"id": "sub-1-2-a", "title": "a) L'automatisation des tâches en entreprise (Crédit Agricole)", "level": 3},
        {"id": "sub-1-2-b", "title": "b) L'accélération du travail scientifique et technique", "level": 3},
        {"id": "sec-1-3", "title": "1.3 L'IA rend possible : franchissement de seuils de capacité", "level": 2},
        {"id": "sub-1-3-a1", "title": "a.1) Le seuil d'échelle : la structure des protéines (AlphaFold)", "level": 3},
        {"id": "sub-1-3-a2", "title": "a.2) Le seuil de difficulté : le problème de Navier–Stokes", "level": 3},
        {"id": "sub-1-3-b", "title": "b) Ce que le franchissement de seuil implique", "level": 3},
        {"id": "sec-1-4", "title": "1.4 L'IA personnalise : de la moyenne au sur-mesure", "level": 2},
        {"id": "sub-1-4-a", "title": "a) Digital twin, modélisation d'un athlète numérique (Enduraw)", "level": 3},
        {"id": "sub-1-4-b", "title": "b) La personnalisation comme nouveau standard", "level": 3},
        {"id": "sub-1-4-c", "title": "c) Ce que l'IA personnalise réellement : le cas Duolingo", "level": 3},
        {"id": "sec-1-concl", "title": "Conclusion de la Partie I", "level": 2}
    ],
    "partie-2": [
        {"id": "sec-2-1", "title": "2.1 Apprendre avec l'IA : transformation de l'acte d'apprendre", "level": 2},
        {"id": "sub-2-1-a", "title": "a) Disponibilité permanente d'un interlocuteur cognitif", "level": 3},
        {"id": "sub-2-1-b", "title": "b) Déplacement de la charge cognitive (théorie de Sweller)", "level": 3},
        {"id": "sub-2-1-c", "title": "c) Retour d'expérience personnel : apprendre sur douze mois", "level": 3},
        {"id": "sec-2-2", "title": "2.2 Nouveau rôle de l’enseignement et des organisations", "level": 2},
        {"id": "sub-2-2-a", "title": "a) Les solutions de l'enseignement face à l'IA", "level": 3},
        {"id": "sub-2-2-b", "title": "b) L'apprentissage organisationnel : cas du Crédit Agricole", "level": 3},
        {"id": "sec-2-3", "title": "2.3 L’IA, future discipline à part entière", "level": 2},
        {"id": "sub-2-3-a", "title": "a) Une trajectoire comparable à celle de la digitalisation", "level": 3},
        {"id": "sub-2-3-b", "title": "b) Une compétence qui se spécialise selon les métiers", "level": 3},
        {"id": "sub-2-3-c", "title": "c) Le principe cardinal : 'Apprendre avant de déléguer'", "level": 3},
        {"id": "sec-2-concl", "title": "Conclusion de la Partie II", "level": 2}
    ],
    "partie-3": [
        {"id": "sec-3-1", "title": "3.1 Risques pour les compétences humaines", "level": 2},
        {"id": "sub-3-1-a", "title": "a) Déplacement de l'effort vs suppression de l'effort", "level": 3},
        {"id": "sub-3-1-b", "title": "b) Érosion du socle et illusion de compétence", "level": 3},
        {"id": "sub-3-1-c", "title": "c) Le risque de la boucle solitaire", "level": 3},
        {"id": "sub-3-1-d", "title": "d) Une vulnérabilité inégale entre experts et novices", "level": 3},
        {"id": "sec-3-2", "title": "3.2 Coûts de transition et impacts organisationnels", "level": 2},
        {"id": "sub-3-2-a", "title": "a) Coût réel de l'IA : investissement, ROI et incertitude", "level": 3},
        {"id": "sub-3-2-b", "title": "b) La dette de compétence : déployer plus vite que former", "level": 3},
        {"id": "sub-3-2-c", "title": "c) Coût humain et organisationnel de la transition", "level": 3},
        {"id": "sub-3-2-d", "title": "d) Homogénéisation des pratiques et responsabilité", "level": 3},
        {"id": "sub-3-2-e", "title": "e) Coût environnemental et empreinte écologique", "level": 3},
        {"id": "sec-3-3", "title": "3.3 Conditions d'une intégration réussie et nouveaux rôles", "level": 2},
        {"id": "sub-3-3-a", "title": "a) Principes directeurs d'une intégration maîtrisée", "level": 3},
        {"id": "sub-3-3-b", "title": "b) Projet personnel développé : LINA", "level": 3},
        {"id": "sec-3-concl", "title": "Conclusion de la Partie III", "level": 2}
    ],
    "conclusion": [
        {"id": "concl-bilan", "title": "Bilan personnel et perspectives", "level": 2},
        {"id": "concl-generale", "title": "Conclusion générale du mémoire", "level": 2},
        {"id": "concl-performance", "title": "Une performance réellement augmentée, sous conditions", "level": 3},
        {"id": "concl-limites", "title": "Limites, risques et conditions d'une intégration maîtrisée", "level": 3},
        {"id": "concl-reponse", "title": "Réponse finale à la problématique", "level": 3}
    ],
    "glossaire": [
        {"id": "glo-termes", "title": "Définition des termes utilisés", "level": 2},
        {"id": "glo-abrev", "title": "Description des abréviations", "level": 2}
    ],
    "bibliographie": [
        {"id": "bib-institutionnelle", "title": "Rapports institutionnels et études scientifiques", "level": 2},
        {"id": "bib-ouvrages", "title": "Ouvrages et articles académiques", "level": 2},
        {"id": "bib-webographie", "title": "Webographie et ressources en ligne", "level": 2}
    ],
    "annexes": [
        {"id": "ann-figures", "title": "Table des figures", "level": 2},
        {"id": "ann-felix", "title": "Enquête FELIX et retours terrain au Crédit Agricole", "level": 2},
        {"id": "ann-lina", "title": "Dossier de conception du projet LINA", "level": 2},
        {"id": "ann-entretiens", "title": "Retranscription des entretiens professionnels", "level": 2}
    ]
}

def format_section_content_with_headings(sec_id, raw_text):
    """
    Formatte le texte brut d'une section en insérant les en-têtes prévus
    et en séparant les paragraphes, citations, listes, encadrés.
    """
    # Liste des patterns à remplacer par un titre HTML
    toc_list = SECTIONS_TOC.get(sec_id, [])
    
    # Nettoyage initial : sauts de page pypdf
    lines = raw_text.split('\n')
    filtered_lines = []
    for l in lines:
        s = l.strip()
        if s.startswith('<!-- Page') and s.endswith('-->'):
            continue
        if re.match(r'^\d{1,3}\s*$', s): # Numéro de page seul
            continue
        filtered_lines.append(s)
        
    full_text = '\n'.join(filtered_lines)
    
    # Remplacer les titres connus par des balises avec ID
    # Pour chaque item dans SECTIONS_TOC, on cherche un mot clé fort
    for item in toc_list:
        title = item["title"]
        tag = f"h{item['level']}"
        # Construire un motif de recherche souple
        # Ex: "1.1 Qu'est-ce que la performance"
        clean_key = re.sub(r'^[0-9a-z\.\-\–\s\(\)]+\s*', '', title)
        clean_key = clean_key.split('(')[0].strip()
        if len(clean_key) > 5:
            pattern = re.compile(r'(' + re.escape(clean_key) + r'[:\s\?]*\b)', re.IGNORECASE)
            # Remplacement avec délimiteur unique
            # On ne fait le remplacement qu'une seule fois
            full_text = pattern.sub(f'\n\n[[HEADING:{item["id"]}:{item["level"]}:{title}]]\n\n', full_text, count=1)
            
    # Découper en paragraphes
    paragraphs = re.split(r'\n\s*\n', full_text)
    html_parts = []
    
    for p in paragraphs:
        p = p.strip()
        if not p:
            continue
            
        # Vérifier si c'est notre balise heading
        m_head = re.match(r'^\[\[HEADING:([^:]+):(\d):(.*?)\]\]$', p)
        if m_head:
            hid = m_head.group(1)
            hlevel = m_head.group(2)
            htitle = m_head.group(3)
            html_parts.append(f'<h{hlevel} id="{hid}">{html.escape(htitle)}</h{hlevel}>')
            continue
            
        # Citations
        if (p.startswith('«') and p.endswith('»')) or (p.startswith('"') and p.endswith('"')):
            html_parts.append(f'<blockquote><p>{html.escape(p)}</p></blockquote>')
        # Puces
        elif p.startswith('•') or p.startswith('- ') or p.startswith('– '):
            items = [item.strip() for item in re.split(r'\n?[•\-\–]\s*', p) if item.strip()]
            list_items = ''.join(f'<li>{html.escape(it)}</li>' for it in items)
            html_parts.append(f'<ul>{list_items}</ul>')
        else:
            # Traiter les retours à la ligne internes
            inline = p.replace('\n', ' ')
            # Échapper HTML
            inline = html.escape(inline)
            # Traiter les notes de bas de page type [1], [2], etc.
            inline = re.sub(r'\[(\d+)\]', r'<sup><a href="#note-\1" class="footnote-ref">[\1]</a></sup>', inline)
            html_parts.append(f'<p>{inline}</p>')
            
    return '\n'.join(html_parts)

print("Perfect parser ready!")
