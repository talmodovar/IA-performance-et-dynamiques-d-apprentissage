import json
import re
import html
import os
import sys
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding='utf-8')
sys.path.append('scratch_cover')

from parse_helpers_mht import (
    URL_PATTERN, linkify_text, RE_SOURCE_SPLIT, is_source_citation,
    make_slug, match_toc_item, clean_word_paragraph_text, format_table
)
from perfect_parser import SECTIONS_TOC, FIGURE_ASSETS, FIGURE_CHAPTERS, FIGURE_CAPTIONS
from parse_helpers import EDITORIAL_SUMMARIES

# Load MHT extracted document
soup = BeautifulSoup(open('scratch_cover/memoire_extracted.html', 'r', encoding='utf-8', errors='replace'), 'html.parser')

SUPERSCRIPT_MAP = {'0': '⁰', '1': '¹', '2': '²', '3': '³', '4': '⁴', '5': '⁵', '6': '⁶', '7': '⁷', '8': '⁸', '9': '⁹'}

# Convert all <sup> tags to unicode superscripts directly in soup
for sup in soup.find_all('sup'):
    s = sup.get_text()
    converted = ''.join(SUPERSCRIPT_MAP.get(c, c) for c in s)
    sup.replace_with(converted)

h1s = soup.find_all('h1')

def format_citation_text(text):
    m = re.match(r'^([¹²³⁴⁵⁶⁷⁸⁹⁰0-9]+)\s*(.*)$', text.strip())
    if m:
        digits = m.group(1)
        rest = m.group(2)
        super_digits = ''.join(SUPERSCRIPT_MAP.get(d, d) for d in digits)
        return f'{super_digits} {rest}'
    return text

SECTIONS_CONFIG = [
    {
        "id": "introduction",
        "title": "Introduction et problématique",
        "subtitle": "Genèse de la recherche, cadre d'analyse et question centrale",
        "category": "Cadre général",
        "start_idx": 6,
        "end_idx": 7
    },
    {
        "id": "partie-0",
        "title": "Partie 0 — Fondamentaux : Comprendre l'IA",
        "subtitle": "Définitions, repères historiques et panorama des architectures",
        "category": "Partie 0",
        "start_idx": 7,
        "end_idx": 8
    },
    {
        "id": "partie-1",
        "title": "Partie I — L'IA comme levier d'augmentation de la performance",
        "subtitle": "Accélération, franchissement de seuils et personnalisation",
        "category": "Partie I",
        "start_idx": 8,
        "end_idx": 9
    },
    {
        "id": "partie-2",
        "title": "Partie II — L'IA et les dynamiques d'apprentissage",
        "subtitle": "Transformation de l'acte d'apprendre et nouveaux rôles organisationnels",
        "category": "Partie II",
        "start_idx": 9,
        "end_idx": 10
    },
    {
        "id": "partie-3",
        "title": "Partie III — Limites, risques et cohabitation humain-IA",
        "subtitle": "Compétences menacées, coûts cachés et conditions de maîtrise",
        "category": "Partie III",
        "start_idx": 10,
        "end_idx": 11
    },
    {
        "id": "conclusion",
        "title": "Bilan et Conclusion générale",
        "subtitle": "Synthèse prospective, validation de la thèse et réponses aux problématiques",
        "category": "Conclusion",
        "start_idx": 11,
        "end_idx": 13  # Includes H1[11] Bilan and H1[12] Conclusion
    },
    {
        "id": "glossaire",
        "title": "Glossaire & Abréviations",
        "subtitle": "Définitions des concepts clés et nomenclature des sigles utilisés",
        "category": "Annexes & Références",
        "start_idx": 5,  # H1[5] contains both definitions and abbreviations table
        "end_idx": 6
    },
    {
        "id": "bibliographie",
        "title": "Bibliographie & Webographie annotée",
        "subtitle": "Sources universitaires, publications scientifiques, rapports et archives en ligne",
        "category": "Annexes & Références",
        "start_idx": 14,
        "end_idx": 15
    },
    {
        "id": "annexes",
        "title": "Annexes : Terrains, Retex & Entretiens",
        "subtitle": "Table des figures, RETEX bancaire et 4 entretiens de recherche",
        "category": "Annexes & Références",
        "start_idx": 15,
        "end_idx": None
    }
]

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="fr" data-theme="light" data-text-size="standard">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{meta_title} | Mémoire de Thomas ALMODOVAR</title>
  <meta name="description" content="{meta_desc}">
  <meta name="author" content="Thomas ALMODOVAR">
  <meta name="robots" content="index, follow">

  <!-- Open Graph -->
  <meta property="og:title" content="{meta_title}">
  <meta property="og:description" content="{meta_desc}">
  <meta property="og:type" content="article">
  <meta property="og:locale" content="fr_FR">

  <!-- Styles -->
  <link rel="stylesheet" href="../css/main.css">
  <link rel="stylesheet" href="../css/reader.css">
</head>
<body>
  <!-- Lien d'évitement WCAG -->
  <a href="#main-reading-content" class="skip-link">Passer directement au texte du chapitre</a>

  <!-- En-tête du site -->
  <header class="site-header" role="banner">
    <div class="container site-header-inner">
      <a href="../index.html" class="brand" aria-label="Retour à l'accueil du mémoire">
        <span class="brand-badge">Mémoire</span>
        <span>Thomas ALMODOVAR</span>
      </a>

      <nav class="main-nav" aria-label="Navigation principale">
        <a href="../index.html" class="nav-link">Accueil</a>
        <a href="../index.html#presentation" class="nav-link">Présentation</a>
        <a href="../index.html#sommaire" class="nav-link">Sommaire général</a>
        <a href="../index.html#a-propos" class="nav-link">À propos & Métadonnées</a>
      </nav>

      <div class="header-actions">
        <a href="../assets/pdf/Memoire_ALMODOVAR_Thomas.pdf" target="_blank" class="btn-download-header" title="Consulter le mémoire complet au format PDF dans un nouvel onglet">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/></svg>
          <span>Consulter le PDF en ligne</span>
        </a>
        <button class="menu-toggle" type="button" aria-expanded="false" aria-label="Ouvrir le menu de navigation">
          <span></span><span></span><span></span>
        </button>
      </div>
    </div>
    <!-- Progression de lecture -->
    <div class="reading-progress-track" aria-hidden="true">
      <div class="reading-progress-bar"></div>
    </div>
  </header>

  <!-- Barre d'outils de lecture (fil d'ariane & réglages) -->
  <aside class="reader-toolbar" aria-label="Commandes de confort de lecture">
    <div class="container reader-toolbar-inner">
      <div class="reader-toolbar-left">
        <nav class="breadcrumb" aria-label="Fil d'Ariane">
          <a href="../index.html">Accueil</a>
          <span class="breadcrumb-separator">/</span>
          <a href="../index.html#sommaire">Sommaire</a>
          <span class="breadcrumb-separator">/</span>
          <span class="breadcrumb-current" aria-current="page">{short_title}</span>
        </nav>
      </div>

      <div class="reader-controls">
        <button type="button" class="btn-toc-toggle" id="btnMobileToc" aria-expanded="false" aria-label="Afficher le sommaire de la partie">
          <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="18" x2="21" y2="18"/></svg>
          <span>Sommaire</span>
        </button>

        <!-- Sélecteur de Thème -->
        <div class="control-group" role="group" aria-label="Sélection du thème de lecture">
          <button type="button" class="control-btn active" data-set-theme="light" aria-pressed="true" title="Thème clair ivoire">Clair</button>
          <button type="button" class="control-btn" data-set-theme="sepia" aria-pressed="false" title="Thème sépia ambré">Sépia</button>
          <button type="button" class="control-btn" data-set-theme="dark" aria-pressed="false" title="Thème sombre onyx">Sombre</button>
        </div>

        <!-- Sélecteur de Taille de police -->
        <div class="control-group" role="group" aria-label="Taille de typographie">
          <button type="button" class="control-btn" data-set-size="small" aria-pressed="false" title="Petite taille (17px)">A-</button>
          <button type="button" class="control-btn active" data-set-size="standard" aria-pressed="true" title="Taille standard (19px)">A</button>
          <button type="button" class="control-btn" data-set-size="large" aria-pressed="false" title="Grande taille (21px)">A+</button>
        </div>

        <!-- Mode concentration -->
        <button type="button" class="btn-zen-mode" id="btnZenMode" aria-pressed="false" title="Activer le mode concentration sans distraction (Touche Z)">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="3"/><path d="M3 7V5a2 2 0 0 1 2-2h2"/><path d="M17 3h2a2 2 0 0 1 2 2v2"/><path d="M21 17v2a2 2 0 0 1-2 2h-2"/><path d="M7 21H5a2 2 0 0 1-2-2v-2"/></svg>
          <span class="zen-label">Mode Zen</span>
        </button>
      </div>
    </div>
  </aside>

  <!-- Disposition principale de lecture -->
  <div class="reader-layout">
    <!-- Sommaire latéral fixe/sticky -->
    <nav class="reader-sidebar" aria-label="Sommaire de la partie">
      <div class="reader-sidebar-title">Plan de cette partie</div>
      <ul class="chapter-toc-list">
        {sidebar_toc_html}
      </ul>
      <div style="margin-top: 32px; padding-top: 20px; border-top: 1px solid var(--border-subtle);">
        <a href="../assets/pdf/Memoire_ALMODOVAR_Thomas.pdf" target="_blank" class="btn-secondary-outline" style="width: 100%; justify-content: center; font-size: 0.825rem;">
          <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>
          <span>Ouvrir en PDF</span>
        </a>
      </div>
    </nav>

    <!-- Corps de lecture principal -->
    <main id="main-reading-content" class="reader-content" role="main">
      <header class="chapter-header">
        <div class="chapter-part-num">{part_number_label}</div>
        <h1 class="chapter-title">{part_title}</h1>
        {part_subtitle_html}

        <div class="chapter-meta-row">
          <span class="chapter-meta-pill">
            <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
            <span>~{read_minutes} min de lecture ({word_count} mots)</span>
          </span>
          <span class="chapter-meta-pill">
            <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
            <span>Thomas ALMODOVAR</span>
          </span>
          <span class="chapter-meta-pill">
            <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>
            <span>École IPSSI — 2025-2026</span>
          </span>
        </div>
      </header>

      <!-- Synthèse éditoriale identifiée -->
      <section class="editorial-chapter-summary" aria-label="Synthèse éditoriale de la partie">
        <div class="summary-heading">
          <span>Points clés du chapitre</span>
          <span class="summary-badge">Synthèse éditoriale</span>
        </div>
        <p>{editorial_summary}</p>
      </section>

      <!-- Texte intégral du mémoire -->
      <article class="chapter-body-text">
        {formatted_body_html}
      </article>

      <!-- Navigation séquentielle bas de page -->
      <footer class="chapter-nav-footer">
        <div class="chapter-nav-grid">
          {prev_card_html}
          {next_card_html}
        </div>

        <div class="chapter-nav-bottom-actions">
          <a href="../index.html#sommaire" class="btn-secondary-outline">
            <svg xmlns="http://www.w3.org/2000/svg" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="19" y1="12" x2="5" y2="12"/><polyline points="12 19 5 12 12 5"/></svg>
            <span>Retour au sommaire général</span>
          </a>

          <a href="../assets/pdf/Memoire_ALMODOVAR_Thomas.pdf" download="Memoire_ALMODOVAR_Thomas.pdf" class="btn-secondary-outline">
            <svg xmlns="http://www.w3.org/2000/svg" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
            <span>Télécharger le mémoire complet (PDF)</span>
          </a>
        </div>
      </footer>
    </main>
  </div>

  <!-- Pied de page -->
  <footer class="site-footer" role="contentinfo">
    <div class="container">
      <div class="footer-top">
        <div>
          <div class="brand">
            <span class="brand-badge">Mémoire</span>
            <span>Thomas ALMODOVAR</span>
          </div>
          <p class="footer-brand-desc">
            Publication numérique universitaire du mémoire de Mastère Dev, Data & IA (École IPSSI - EISI, promotion 2025-2026). Ce diplôme a été réalisé en alternance au sein du service Pilotage de la performance de Crédit Agricole Sud Méditerranée.
          </p>
        </div>
        <div>
          <div class="footer-heading">Navigation</div>
          <ul class="footer-links">
            <li><a href="../index.html">Accueil du site</a></li>
            <li><a href="../index.html#presentation">Présentation</a></li>
            <li><a href="../index.html#sommaire">Sommaire général</a></li>
            <li><a href="../index.html#a-propos">À propos & Métadonnées</a></li>
          </ul>
        </div>
        <div>
          <div class="footer-heading">Document</div>
          <ul class="footer-links">
            <li><a href="../assets/pdf/Memoire_ALMODOVAR_Thomas.pdf" download="Memoire_ALMODOVAR_Thomas.pdf">Télécharger le PDF original (2,08 Mo)</a></li>
            <li><a href="../assets/pdf/Memoire_ALMODOVAR_Thomas.pdf" target="_blank">Consulter le PDF en ligne</a></li>
            <li><a href="glossaire.html">Glossaire des termes</a></li>
            <li><a href="bibliographie.html">Bibliographie & Webographie</a></li>
          </ul>
        </div>
      </div>
      <div class="footer-bottom">
        <div>© 2026 Thomas ALMODOVAR — Tous droits de reproduction et de citation réservés selon les règles universitaires.</div>
        <div>Conception éditoriale respectant les critères d'accessibilité WCAG 2.2 AA.</div>
      </div>
    </div>
  </footer>

  <!-- Scripts -->
  <script src="../js/main.js"></script>
  <script src="../js/reader.js"></script>
</body>
</html>
"""

def render_figure(fig_num, caption=None):
    clean_prefix = f"Figure {fig_num}"
    canonical = FIGURE_CAPTIONS.get(fig_num, caption or "")
    linked_desc = linkify_text(canonical)
    img_file = FIGURE_ASSETS.get(fig_num)
    if img_file:
        return f'''<figure class="reader-figure-card" id="fig-{fig_num}">
  <div class="figure-img-container">
    <img src="../assets/images/figures/{img_file}" alt="{clean_prefix} — {canonical}" class="figure-img" loading="lazy">
  </div>
  <figcaption class="figure-caption">
    <strong>{clean_prefix}</strong> — {linked_desc}
  </figcaption>
</figure>'''
    else:
        return f'<p class="figure-callout"><strong>{clean_prefix}</strong> — {linked_desc}</p>'

def parse_section(sec_id, start_h1, end_h1=None):
    toc_items = SECTIONS_TOC.get(sec_id, [])
    blocks = []
    
    used_ids = set()
    def get_unique_id(base_id):
        cand = base_id
        count = 2
        while cand in used_ids:
            cand = f"{base_id}-{count}"
            count += 1
        used_ids.add(cand)
        return cand

    # Handle Introduction special top heading
    if sec_id == "introduction":
        blocks.append('<h2 id="intro-problematique">Genèse et problématique de recherche</h2>')

    curr = start_h1.find_next_sibling()
    
    current_list_type = None
    current_list_items = []
    
    def flush_list():
        nonlocal current_list_type, current_list_items
        if current_list_items:
            tag = current_list_type or 'ul'
            li_html = '\n'.join(f'  <li>{it}</li>' for it in current_list_items)
            blocks.append(f'<{tag}>\n{li_html}\n</{tag}>')
            current_list_items = []
            current_list_type = None

    rendered_figs = set()

    while curr and curr != end_h1:
        # Check if inside conclusion and encounter second H1
        if sec_id == "conclusion" and curr.name == 'h1':
            flush_list()
            h_text = clean_word_paragraph_text(curr)
            if 'Bilan' in h_text:
                blocks.append('<h2 id="concl-bilan">Bilan et perspectives</h2>')
            elif 'Conclusion' in h_text:
                blocks.append('<h2 id="concl-generale">Conclusion générale du mémoire</h2>')
            curr = curr.find_next_sibling()
            continue

        # Skip raw repetitions of section titles
        if curr.name == 'p':
            t_raw = clean_word_paragraph_text(curr)
            if t_raw.startswith("PARTIE ") and ("Comprendre l'IA" in t_raw or "L'IA comme" in t_raw or "L'IA et les" in t_raw or "Limites, risques" in t_raw):
                curr = curr.find_next_sibling()
                continue

        # Handle Tables
        if curr.name == 'table':
            flush_list()
            tbl_html = format_table(curr)
            if tbl_html:
                blocks.append(tbl_html)
            curr = curr.find_next_sibling()
            continue

        # Handle Headings (h2, h3, h4, h5)
        if curr.name in ['h2', 'h3', 'h4', 'h5', 'h6']:
            flush_list()
            h_text = clean_word_paragraph_text(curr)
            if not h_text:
                curr = curr.find_next_sibling()
                continue
                
            toc_match = match_toc_item(h_text, toc_items)
            tag = curr.name
            
            if toc_match:
                lvl = toc_match.get('level', 2)
                tag = f"h{lvl}"
                base_id = toc_match['id']
                disp_title = toc_match['title']
            else:
                base_id = f"sec-{make_slug(h_text)}"
                disp_title = h_text
                
            hid = get_unique_id(base_id)
            blocks.append(f'<{tag} id="{hid}">{html.escape(disp_title)}</{tag}>')
            curr = curr.find_next_sibling()
            continue

        # Check for VML or special figure paragraphs (e.g. Figure 8 in partie-2)
        if sec_id == "partie-2" and ('Figure 8' in str(curr) or 'Zone_x0020_de_x0020_texte' in str(curr)):
            flush_list()
            if 8 not in rendered_figs:
                blocks.append(render_figure(8))
                rendered_figs.add(8)

        # Handle Paragraphs (<p>)
        if curr.name == 'p':
            t = clean_word_paragraph_text(curr)
            if not t:
                curr = curr.find_next_sibling()
                continue

            # Check if this is a Figure
            m_fig = re.match(r'^(Figure\s+(\d+))[\s\-\,\:]*(.*)$', t, re.IGNORECASE)
            if m_fig:
                flush_list()
                prefix = m_fig.group(1)
                fig_num = int(m_fig.group(2))
                caption = m_fig.group(3).strip()
                
                # If in Annexes (Table des figures)
                if sec_id == "annexes":
                    canonical = FIGURE_CAPTIONS.get(fig_num, caption)
                    target_chap = FIGURE_CHAPTERS.get(fig_num, "annexes")
                    linked_caption = linkify_text(canonical)
                    blocks.append(f'<p class="figure-item"><a href="{target_chap}.html#fig-{fig_num}"><strong>Figure {fig_num}</strong></a> — {linked_caption}</p>')
                else:
                    # In body chapter
                    if fig_num == 9 and 8 not in rendered_figs and sec_id == "partie-2":
                        blocks.append(render_figure(8))
                        rendered_figs.add(8)
                    if fig_num not in rendered_figs:
                        blocks.append(render_figure(fig_num, caption))
                        rendered_figs.add(fig_num)
                curr = curr.find_next_sibling()
                continue

            # Check for Glossaire defined term with <b>
            if sec_id == "glossaire":
                b_tag = curr.find('b')
                if b_tag and not is_source_citation(t):
                    term = ' '.join(b_tag.get_text().split()).strip()
                    # Definition is text after term
                    full_p_text = clean_word_paragraph_text(curr)
                    if full_p_text.startswith(term):
                        definition = full_p_text[len(term):].strip().lstrip(' :—-')
                        linked_def = linkify_text(definition)
                        blocks.append(f'<p class="glossary-entry"><strong>{html.escape(term)}</strong> — {linked_def}</p>')
                        curr = curr.find_next_sibling()
                        continue

            # Check for MsoListParagraph or bullet
            is_list = ('List' in ' '.join(curr.get('class', []))) or t.startswith(('· ', 'o ', '- ', '• '))
            is_numbered_list = bool(re.match(r'^\d+[\.\)]\s+', t)) and len(t) < 400 and not is_source_citation(t)
            
            if is_list or (is_numbered_list and 'MsoList' in ' '.join(curr.get('class', []))):
                list_type = 'ol' if is_numbered_list else 'ul'
                if current_list_type != list_type:
                    flush_list()
                    current_list_type = list_type
                
                clean_li = re.sub(r'^(?:[·o\-•]|\d+[\.\)])\s*', '', t).strip()
                current_list_items.append(linkify_text(clean_li))
                curr = curr.find_next_sibling()
                continue
            else:
                flush_list()

            # Check if this is a footnote / source citation
            if is_source_citation(t):
                parts = RE_SOURCE_SPLIT.split(t)
                for part in parts:
                    p_c = part.strip()
                    if p_c:
                        if is_source_citation(p_c):
                            formatted_c = format_citation_text(p_c)
                            blocks.append(f'<p class="source-citation">{linkify_text(formatted_c)}</p>')
                        else:
                            blocks.append(f'<p>{linkify_text(p_c)}</p>')
                curr = curr.find_next_sibling()
                continue

            # Check for multi-citation merged in paragraph
            parts = RE_SOURCE_SPLIT.split(t)
            if len(parts) > 1 and any(is_source_citation(p) for p in parts):
                for part in parts:
                    p_c = part.strip()
                    if p_c:
                        if is_source_citation(p_c):
                            formatted_c = format_citation_text(p_c)
                            blocks.append(f'<p class="source-citation">{linkify_text(formatted_c)}</p>')
                        else:
                            blocks.append(f'<p>{linkify_text(p_c)}</p>')
                curr = curr.find_next_sibling()
                continue

            # Bibliographie card formatting
            if sec_id == "bibliographie":
                blocks.append(f'<p>{linkify_text(t)}</p>')
                curr = curr.find_next_sibling()
                continue

            # Standard paragraph
            blocks.append(f'<p>{linkify_text(t)}</p>')

        curr = curr.find_next_sibling()

    flush_list()
    return '\n'.join(blocks)

os.makedirs('lecture', exist_ok=True)

for i, sec in enumerate(SECTIONS_CONFIG):
    sec_id = sec['id']
    start_node = h1s[sec['start_idx']]
    end_node = h1s[sec['end_idx']] if sec['end_idx'] is not None else None
    
    formatted_html = parse_section(sec_id, start_node, end_node)
    
    # Calculate words and read time
    text_only = re.sub(r'<[^>]+>', ' ', formatted_html)
    words = len(text_only.split())
    read_minutes = max(1, round(words / 230))
    
    # Construction du sommaire latéral à partir de SECTIONS_TOC
    toc_items = SECTIONS_TOC.get(sec_id, [])
    sidebar_items = []
    if not toc_items:
        sidebar_items.append(f'<li class="chapter-toc-item"><a href="#main-reading-content" class="chapter-toc-link active">{html.escape(sec["title"])}</a></li>')
    else:
        for t in toc_items:
            cls = "chapter-toc-link"
            if t.get("level") == 4:
                sidebar_items.append(f'<li class="chapter-toc-item" style="padding-left: 20px; font-size: 0.8rem;"><a href="#{t["id"]}" class="{cls}">{html.escape(t["title"])}</a></li>')
            elif t.get("level") == 3:
                sidebar_items.append(f'<li class="chapter-toc-item" style="padding-left: 10px;"><a href="#{t["id"]}" class="{cls}">{html.escape(t["title"])}</a></li>')
            else:
                sidebar_items.append(f'<li class="chapter-toc-item"><a href="#{t["id"]}" class="{cls}">{html.escape(t["title"])}</a></li>')
    sidebar_toc_html = '\n'.join(sidebar_items)
    
    # Navigation précédent / suivant
    prev_card_html = ''
    if i > 0:
        prev_sec = SECTIONS_CONFIG[i-1]
        prev_card_html = f"""
        <a href="{prev_sec['id']}.html" class="chapter-nav-card prev">
          <span class="chapter-nav-direction">
            <svg xmlns="http://www.w3.org/2000/svg" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="15 18 9 12 15 6"/></svg>
            <span>Partie précédente</span>
          </span>
          <span class="chapter-nav-title">{html.escape(prev_sec['title'])}</span>
        </a>
        """
    else:
        prev_card_html = '<div></div>'
        
    next_card_html = ''
    if i < len(SECTIONS_CONFIG) - 1:
        next_sec = SECTIONS_CONFIG[i+1]
        next_card_html = f"""
        <a href="{next_sec['id']}.html" class="chapter-nav-card next">
          <span class="chapter-nav-direction">
            <span>Partie suivante</span>
            <svg xmlns="http://www.w3.org/2000/svg" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="9 18 15 12 9 6"/></svg>
          </span>
          <span class="chapter-nav-title">{html.escape(next_sec['title'])}</span>
        </a>
        """
    else:
        next_card_html = '<div></div>'
        
    part_subtitle_html = f'<p class="chapter-subtitle">{html.escape(sec["subtitle"])}</p>' if sec.get('subtitle') else ''
    
    page_html = HTML_TEMPLATE.format(
        meta_title=html.escape(sec['title']),
        meta_desc=html.escape(EDITORIAL_SUMMARIES.get(sec_id, sec['subtitle'])[:160]),
        short_title=html.escape(sec['title'].split('—')[-1].strip() if '—' in sec['title'] else sec['title']),
        part_number_label=html.escape(sec['category']),
        part_title=html.escape(sec['title']),
        part_subtitle_html=part_subtitle_html,
        read_minutes=read_minutes,
        word_count=f"{words:,}".replace(',', ' '),
        editorial_summary=html.escape(EDITORIAL_SUMMARIES.get(sec_id, "Synthèse en cours de validation.")),
        sidebar_toc_html=sidebar_toc_html,
        formatted_body_html=formatted_html,
        prev_card_html=prev_card_html,
        next_card_html=next_card_html
    )
    
    file_path = f"lecture/{sec_id}.html"
    with open(file_path, "w", encoding="utf-8") as out:
        out.write(page_html)
    print(f"Generated {file_path} ({words} words, ~{read_minutes} min)")

print("\nSUCCESS: All reader pages regenerated directly from MHT source of truth!")
