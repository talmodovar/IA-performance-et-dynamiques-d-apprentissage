import json
import re
import html
import os
import sys
sys.path.append('scratch_cover')
from perfect_parser import SECTIONS_TOC, format_section_content_with_headings
from parse_helpers import EDITORIAL_SUMMARIES

with open('scratch_cover/sections_data.json', 'r', encoding='utf-8') as f:
    sections = json.load(f)

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
          <span class="summary-badge">Synthèse éditoriale à valider</span>
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

os.makedirs('lecture', exist_ok=True)

for i, sec in enumerate(sections):
    sec_id = sec['id']
    formatted_html = format_section_content_with_headings(sec_id, sec['raw_text'])
    
    # Construction du sommaire latéral à partir de SECTIONS_TOC
    toc_items = SECTIONS_TOC.get(sec_id, [])
    sidebar_items = []
    if not toc_items:
        sidebar_items.append(f'<li class="chapter-toc-item"><a href="#main-reading-content" class="chapter-toc-link active">{html.escape(sec["title"])}</a></li>')
    else:
        for t in toc_items:
            cls = "chapter-toc-link"
            if t["level"] == 3:
                sidebar_items.append(f'<li class="chapter-toc-item" style="padding-left: 12px;"><a href="#{t["id"]}" class="{cls}">{html.escape(t["title"])}</a></li>')
            else:
                sidebar_items.append(f'<li class="chapter-toc-item"><a href="#{t["id"]}" class="{cls}">{html.escape(t["title"])}</a></li>')
    sidebar_toc_html = '\n'.join(sidebar_items)
    
    # Navigation précédent / suivant
    prev_card_html = ''
    if i > 0:
        prev_sec = sections[i-1]
        prev_card_html = f"""
        <a href="{prev_sec['id']}.html" class="chapter-nav-card prev">
          <span class="chapter-nav-direction">
            <svg xmlns="http://www.w3.org/2000/svg" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="15 18 9 12 15 6"/></svg>
            <span>Partie précédente</span>
          </span>
          <span class="chapter-nav-title">{html.escape(prev_sec['title'])}</span>
          <span class="chapter-nav-time">~{prev_sec['reading_time_minutes']} min de lecture</span>
        </a>
        """
    else:
        prev_card_html = '<div></div>'
        
    next_card_html = ''
    if i < len(sections) - 1:
        next_sec = sections[i+1]
        next_card_html = f"""
        <a href="{next_sec['id']}.html" class="chapter-nav-card next">
          <span class="chapter-nav-direction">
            <span>Partie suivante</span>
            <svg xmlns="http://www.w3.org/2000/svg" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="9 18 15 12 9 6"/></svg>
          </span>
          <span class="chapter-nav-title">{html.escape(next_sec['title'])}</span>
          <span class="chapter-nav-time">~{next_sec['reading_time_minutes']} min de lecture</span>
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
        read_minutes=sec['reading_time_minutes'],
        word_count=f"{sec['words']:,}".replace(',', ' '),
        editorial_summary=html.escape(EDITORIAL_SUMMARIES.get(sec_id, "Synthèse en cours de validation.")),
        sidebar_toc_html=sidebar_toc_html,
        formatted_body_html=formatted_html,
        prev_card_html=prev_card_html,
        next_card_html=next_card_html
    )
    
    file_path = f"lecture/{sec_id}.html"
    with open(file_path, "w", encoding="utf-8") as out:
        out.write(page_html)
    print(f"Generated {file_path}")

print("All reader pages regenerated with perfect TOC headings!")
