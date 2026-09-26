import pypdf
import json
import re

reader = pypdf.PdfReader('Mémoire - ALMODOVAR Thomas.pdf')
total_pages = len(reader.pages)

# Page indices in 0-indexed terms
# Doc p.1 is page index 21
sections_def = [
    {
        "id": "introduction",
        "number": "00",
        "title": "Introduction et problématique",
        "subtitle": "Genèse personnelle, question de recherche et démarche d'investigation",
        "start_page": 21, # PDF page 22 (doc p.1)
        "end_page": 23,   # PDF page 23 (doc p.2)
        "category": "Cadre de recherche"
    },
    {
        "id": "partie-0",
        "number": "0.0",
        "title": "Partie 0 — Fondamentaux : Comprendre l'IA",
        "subtitle": "Histoire, rupture des transformers, familles technologiques et évolution des performances",
        "start_page": 23, # PDF page 24 (doc p.3)
        "end_page": 30,   # PDF page 30 (doc p.9)
        "category": "Socle conceptuel"
    },
    {
        "id": "partie-1",
        "number": "01",
        "title": "Partie I — L'IA comme levier d'augmentation de la performance",
        "subtitle": "Les trois régimes de performance : accélérer, rendre possible et personnaliser",
        "start_page": 30, # PDF page 31 (doc p.10)
        "end_page": 59,   # PDF page 59 (doc p.38)
        "category": "Analyse empirique & théorique"
    },
    {
        "id": "partie-2",
        "number": "02",
        "title": "Partie II — L'IA et les dynamiques d'apprentissage",
        "subtitle": "Transformation cognitive, théorie de la charge cognitive et principe 'Apprendre avant de déléguer'",
        "start_page": 59, # PDF page 60 (doc p.39)
        "end_page": 75,   # PDF page 75 (doc p.54)
        "category": "Sciences de l'apprentissage"
    },
    {
        "id": "partie-3",
        "number": "03",
        "title": "Partie III — Limites, risques et cohabitation humain-IA",
        "subtitle": "Érosion des compétences, dette organisationnelle, projet LINA et conditions d'une intégration maîtrisée",
        "start_page": 75, # PDF page 76 (doc p.55)
        "end_page": 96,   # PDF page 96 (doc p.75)
        "category": "Esprit critique & Prospective"
    },
    {
        "id": "conclusion",
        "number": "04",
        "title": "Bilan, perspectives et conclusion générale",
        "subtitle": "Synthèse de la thèse : l'augmentation sous condition d'une maîtrise humaine",
        "start_page": 96, # PDF page 97 (doc p.76)
        "end_page": 101,  # PDF page 101 (doc p.80)
        "category": "Synthèse conclusive"
    },
    {
        "id": "glossaire",
        "number": "G",
        "title": "Glossaire et définitions des termes",
        "subtitle": "Terminologie technique, concepts d'IA et abréviations du mémoire",
        "start_page": 9,  # PDF pages 10-21 & 102-107
        "end_page": 21,
        "additional_pages": [101, 107], # PDF pages 102 to 107
        "category": "Référence"
    },
    {
        "id": "bibliographie",
        "number": "B",
        "title": "Bibliographie et webographie annotée",
        "subtitle": "Rapports institutionnels, littérature scientifique, articles et documentation spécialisée",
        "start_page": 107, # PDF page 108 (doc p.87)
        "end_page": 138,   # PDF page 138 (doc p.117)
        "category": "Sources de référence"
    },
    {
        "id": "annexes",
        "number": "A",
        "title": "Annexes et entretiens de terrain",
        "subtitle": "Table des figures, enquête FELIX, retours sur LINA et entretiens professionnels intégraux",
        "start_page": 138, # PDF page 139 (doc p.118)
        "end_page": 152,   # PDF page 152
        "category": "Matériaux d'enquête"
    }
]

extracted_data = []

for sec in sections_def:
    sec_text = ""
    pages_to_extract = list(range(sec["start_page"], sec["end_page"]))
    if "additional_pages" in sec:
        pages_to_extract += list(range(sec["additional_pages"][0], sec["additional_pages"][1]))
    
    for p_idx in pages_to_extract:
        if p_idx < total_pages:
            t = reader.pages[p_idx].extract_text() or ""
            sec_text += f"\n<!-- Page {p_idx+1} -->\n" + t
    
    # Word count estimation
    words = len(sec_text.split())
    # Reading time estimation: standard 200 words per minute for academic text
    read_minutes = max(1, round(words / 200))
    
    extracted_data.append({
        "id": sec["id"],
        "number": sec["number"],
        "title": sec["title"],
        "subtitle": sec["subtitle"],
        "category": sec["category"],
        "words": words,
        "reading_time_minutes": read_minutes,
        "content_length": len(sec_text),
        "raw_text": sec_text
    })
    print(f"Extracted {sec['id']}: {words} words, ~{read_minutes} min read")

with open("scratch_cover/sections_data.json", "w", encoding="utf-8") as f:
    json.dump(extracted_data, f, ensure_ascii=False, indent=2)

print("Saved scratch_cover/sections_data.json successfully!")
