import re

with open("scratch_cover/all_text_raw.txt", "r", encoding="utf-8") as f:
    content = f.read()

pages = content.split("<<< PAGE ")

print(f"Total page chunks: {len(pages) - 1}")

headings_to_find = [
    "Remerciements",
    "Résumé",
    "Abstract",
    "Sommaire",
    "Liste des abréviations",
    "Introduction et problématique",
    "PARTIE 0, FONDAMENTAUX",
    "0.1 Définition et histoire",
    "0.2 Panorama des grandes familles",
    "PARTIE I, L'IA comme levier",
    "1.1 Qu'est-ce que la performance",
    "1.2 L'IA accélère",
    "1.3 L'IA rend possible",
    "1.4 L'IA personnalise",
    "Conclusion de partie I",
    "PARTIE II, L'IA et les dynamiques",
    "2.1 Apprendre avec l'IA",
    "2.2 Nouveau rôle de l'enseignement",
    "2.3 L’IA, future discipline",
    "Conclusion de partie II",
    "PARTIE III, Limites, risques",
    "3.1 Risques pour les compétences",
    "3.2 Coûts de transition",
    "3.3 Conditions d'une intégration",
    "Conclusion de partie III",
    "Bilan et perspectives",
    "Conclusion",
    "Glossaire",
    "Bibliographie",
    "Annexes"
]

for h in headings_to_find:
    pattern = re.compile(re.escape(h), re.IGNORECASE)
    matches = []
    for idx, p in enumerate(pages[1:], start=1):
        if pattern.search(p):
            matches.append(idx)
    print(f"{h[:35]:<35} -> Pages: {matches}")
