import json
import re
import html

# Charger les données extraites
with open('scratch_cover/sections_data.json', 'r', encoding='utf-8') as f:
    sections = json.load(f)

# Descriptions éditoriales pour chaque section (identifiées comme telles)
EDITORIAL_SUMMARIES = {
    "introduction": "Genèse d'une recherche née d'une expérience personnelle de transformation physique de 50 kg et de préparation sportive couplée à l'analyse professionnelle au Crédit Agricole. Formulation de la problématique centrale : dans quelle mesure l'intégration de l'IA permet-elle d'améliorer la performance et les dynamiques d'apprentissage ?",
    "partie-0": "Socle conceptuel traçant l'histoire de l'IA depuis les systèmes experts jusqu'aux architectures Transformers et à la multimodalité actuelle. Analyse comparative entre programmation classique déterministe et modèles statistiques d'apprentissage.",
    "partie-1": "Démonstration des trois régimes d'impact de l'IA : accélérer les tâches maîtrisées (retours chiffrés d'entreprise et outil FELIX), rendre possibles des ruptures d'échelle et de complexité (AlphaFold, Navier-Stokes), et personnaliser l'action humaine (athlète numérique, Duolingo).",
    "partie-2": "Analyse cognitive de l'acte d'apprendre assisté par l'IA. Application de la théorie de la charge cognitive de Sweller, formalisation du principe cardinal 'Apprendre avant de déléguer' et examen de l'évolution du rôle des formateurs et des organisations.",
    "partie-3": "Examen critique des vulnérabilités humaines et organisationnelles : risque de déqualification et d'illusion de compétence, coût réel et dette de compétence, présentation détaillée du projet LINA et formulation des principes directeurs d'une intégration maîtrisée.",
    "conclusion": "Synthèse générale des apports de la thèse : l'IA ne génère de surperformance durable que comme amplificateur d'une expertise humaine solide, responsable et critique, et non comme un substitut cognitif.",
    "glossaire": "Répertoire exhaustif de plus de 60 définitions et abréviations techniques et conceptuelles mobilisées tout au long du mémoire.",
    "bibliographie": "Recensement critique et annoté des sources scientifiques, institutionnelles (dont le rapport Stanford AI Index 2026), économiques et techniques appuyant l'argumentation.",
    "annexes": "Matériaux d'enquête de terrain : table des figures, données de l'enquête FELIX au Crédit Agricole Sud Méditerranée, documentation du prototype LINA et retranscription des 4 entretiens semi-directifs : Échanges avec Anthony SALIOU (Enduraw), Jean-Baptiste MERIEM (Crédit Agricole Assurance), Alexandre FERRER (USAP) et Celian BONNOT (USAP)."
}

def clean_pdf_text_to_html(raw_text):
    """
    Nettoie le texte extrait du PDF et le structure en HTML riche :
    - Détecte les en-têtes (h2, h3, h4)
    - Supprime les numéros de page isolés
    - Fusionne les coupures de ligne de paragraphe
    - Identifie les citations et les listes à puces
    """
    lines = raw_text.split('\n')
    cleaned_lines = []
    
    # Supprimer les commentaires de page
    for line in lines:
        stripped = line.strip()
        if stripped.startswith('<!-- Page') and stripped.endswith('-->'):
            continue
        # Ignorer les lignes ne contenant qu'un numéro de page
        if re.match(r'^\d{1,3}\s*$', stripped):
            continue
        cleaned_lines.append(stripped)
    
    paragraphs = []
    current_p = []
    
    for line in cleaned_lines:
        if not line:
            if current_p:
                paragraphs.append(' '.join(current_p))
                current_p = []
        else:
            current_p.append(line)
    if current_p:
        paragraphs.append(' '.join(current_p))
        
    html_output = []
    toc_items = []
    
    h2_counter = 0
    h3_counter = 0
    
    for p in paragraphs:
        # Détection d'un grand titre h2 (ex: "1.1 Qu'est-ce que...", "0.1 Définition...", "3.2 Coûts...", "Conclusion...")
        if re.match(r'^(0\.[1-9]|1\.[1-9]|2\.[1-9]|3\.[1-9]|[A-Z0-9\.\s—]+:)\s+[A-ZÀ-Ÿ]', p) or \
           re.match(r'^(Qu’est-ce que|L’IA accélère|L’IA rend possible|L’IA personnalise|Apprendre avec|Nouveau rôle|Risques pour|Coûts de transition|Conditions d’une|Bilan|Conclusion)', p, re.IGNORECASE) and len(p) < 100:
            h2_counter += 1
            sec_id = f"sec-{h2_counter}"
            title_text = html.escape(p)
            toc_items.append({"id": sec_id, "title": p, "level": 2})
            html_output.append(f'<h2 id="{sec_id}">{title_text}</h2>')
            
        # Détection d'un sous-titre h3 (ex: "a) Les dimensions...", "b) L'IA déplace...", "b.1) ...")
        elif re.match(r'^([a-d]\)|[a-d]\.[1-9]\))\s+', p) and len(p) < 140:
            h3_counter += 1
            sec_id = f"sub-{h2_counter}-{h3_counter}"
            title_text = html.escape(p)
            toc_items.append({"id": sec_id, "title": p, "level": 3})
            html_output.append(f'<h3 id="{sec_id}">{title_text}</h3>')
            
        # Détection d'un titre h4 ou intitulé court isolé
        elif (len(p) < 70 and not p.endswith('.') and not p.endswith(':') and not p.endswith(',')) and \
             any(p.startswith(w) for w in ["Ce qui devient", "Vers quoi", "La thèse", "Deux conséquences", "Articulation", "Une progression", "Pourquoi former", "Un outil"]):
            html_output.append(f'<h4>{html.escape(p)}</h4>')
            
        # Détection d'une citation (commence et termine par des guillemets)
        elif (p.startswith('«') and p.endswith('»')) or (p.startswith('"') and p.endswith('"')):
            html_output.append(f'<blockquote><p>{html.escape(p)}</p></blockquote>')
            
        # Détection d'une liste à puces
        elif p.startswith('•') or p.startswith('- ') or p.startswith('– '):
            item_text = re.sub(r'^[•\-\–]\s*', '', p)
            html_output.append(f'<ul><li>{html.escape(item_text)}</li></ul>')
            
        # Paragraphe normal
        else:
            # Traiter les appels de notes de type [1] ou (1)
            escaped = html.escape(p)
            # Remplacement des appels de notes éventuels
            escaped = re.sub(r'\[(\d+)\]', r'<sup><a href="#note-\1" class="footnote-ref">[\1]</a></sup>', escaped)
            html_output.append(f'<p>{escaped}</p>')
            
    return '\n'.join(html_output), toc_items

print("Cleaner function ready!")
