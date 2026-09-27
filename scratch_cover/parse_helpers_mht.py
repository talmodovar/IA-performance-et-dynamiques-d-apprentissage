import re
import html
import sys
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding='utf-8')

from perfect_parser import SECTIONS_TOC, FIGURE_ASSETS, FIGURE_CHAPTERS, FIGURE_CAPTIONS, MONTHS

# Enhanced URL Pattern catching any domain with a path (like digital.hec.ca/blog/..., research.netflix.com/...)
URL_PATTERN = re.compile(
    r'('
    r'https?://[^\s<>"\'\)]+[^\s<>"\'\),;:?!.\)\]]'
    r'|'
    r'www\.[a-zA-Z0-9_\-\.]+\.[a-zA-Z]{2,6}[^\s<>"\'\),;:?!.\)\]]*'
    r'|'
    r'(?:[a-zA-Z0-9_\-]+\.)+[a-zA-Z]{2,6}/[^\s<>"\'\)]+[^\s<>"\'\),;:?!.\)\]]'
    r')'
)

def linkify_text(text):
    """
    Rend cliquables tous les liens HTTP/HTTPS ou noms de domaine (ex: digital.hec.ca) avec target="_blank".
    """
    parts = []
    last_end = 0
    for m in URL_PATTERN.finditer(text):
        parts.append(html.escape(text[last_end:m.start()]))
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

RE_SOURCE_SPLIT = re.compile(
    r'(?<=\S)\s+(?='
    r'[¹²³⁴⁵⁶⁷⁸⁹⁰]+(?:\s*[A-ZÀÂÄÉÈÊËÎÏÔÖÙÛÜŸÇ«"“]|\s*https?:)'
    r'|'
    r'(?!(?:[234]D|[48]K|\d+B|\d+(?:e|ème|er|ère|nd|th|rd|st))\b)[1-9]\d?(?=[A-ZÀÂÄÉÈÊËÎÏÔÖÙÛÜŸÇ«"“]|https?:)'
    r'|'
    r'(?<=[.\?!»\)"\'’])\s*(?!(?:[234]D|[48]K|\d+B|\d+(?:e|ème|er|ère|nd|th|rd|st))\b)[1-9]\d?\s+(?!' + MONTHS + r'\b)(?:[A-ZÀÂÄÉÈÊËÎÏÔÖÙÛÜŸÇ«"“]|https?:)'
    r')'
)

SUPERSCRIPT_MAP = {'0': '⁰', '1': '¹', '2': '²', '3': '³', '4': '⁴', '5': '⁵', '6': '⁶', '7': '⁷', '8': '⁸', '9': '⁹'}

def is_source_citation(text):
    t = text.strip()
    if re.match(r'^(?:[234]D|[48]K|\d+B|\d+(?:e|ème|er|ère|nd|th|rd|st))\b', t, re.IGNORECASE):
        return False
        
    m_num = re.match(r'^[¹²³⁴⁵⁶⁷⁸⁹⁰0-9]+', t)
    if not m_num:
        return False
        
    # Check for citation indicators
    if re.search(r'https?://|www\.|arxiv\.org|youtube\.com|digital\.hec\.ca|hal\.science', t):
        return True
    if re.search(r'\b(?:et al\.|Database|Report|Press|éd\.|vol\.|pp?\.|arXiv|interview|entretien|conférence|webinaire|audition)\b', t, re.IGNORECASE):
        return True
    if re.match(r'^[¹²³⁴⁵⁶⁷⁸⁹⁰0-9]+\s*(?:[«"“]|Wikipédia|Wikipedia|YouTube|ECMWF|NASA|OpenAI|AlphaFold|Stanford|Union|Université|University|Le Monde|Le Quotidien|Académie|Cnam|École|Classement|Prévisions|Insee|Joseph MESTRALLET|Maureen|LearnLM|George|Weixu|Evan|Hamsa|Bozena|Parker|Sejoon|Thibault|Zied|Sylvestre|Quentin|Arthur|David|Fabrice|Brandon|Le MAG|European|S\. Knerr)', t, re.IGNORECASE):
        if re.search(r'^[¹²³⁴⁵⁶⁷⁸⁹⁰0-9]+\s*(?:Autor y voit|Fabrice Popineau documente)', t):
            return False
        return True
    if re.search(r'[«"“]', t) and re.search(r'\b(?:19\d\d|20\d\d)\b', t):
        return True
        
    return False

def make_slug(title_text):
    slug = re.sub(r'[^a-zA-Z0-9]+', '-', title_text.lower()).strip('-')
    return slug[:40]

def match_toc_item(title_text, toc_items):
    clean_t = ' '.join(title_text.split()).strip()
    clean_t_lower = clean_t.lower()
    
    # 1. Exact match
    for it in toc_items:
        if it['title'].lower() == clean_t_lower:
            return it
            
    # 2. Prefix match (e.g. "1.1", "a)", "a.1)", "b.2)", "1)", "0.1")
    m_p = re.match(r'^([0-9a-z\.\-\–\(\)]+)\s*', clean_t, re.IGNORECASE)
    pref = m_p.group(1).lower().rstrip('.)-') if m_p else ''
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
            # disambiguate with clean text
            clean_sans_pref = re.sub(r'^[0-9a-z\.\-\–\s\(\)]+\s*', '', clean_t).strip().lower()
            for it in candidates:
                it_clean = re.sub(r'^[0-9a-z\.\-\–\s\(\)]+\s*', '', it['title']).strip().lower()
                if clean_sans_pref and (clean_sans_pref in it_clean or it_clean in clean_sans_pref):
                    return it
            return candidates[0]

    # 3. Substring match
    for it in toc_items:
        it_clean = re.sub(r'^[0-9a-z\.\-\–\s\(\)]+\s*', '', it['title']).strip().lower()
        if len(it_clean) > 8 and (it_clean in clean_t_lower or clean_t_lower in it_clean):
            return it

    return None

def clean_word_paragraph_text(p_node):
    """
    Extrait le texte d'un paragraphe Word en nettoyant les espaces multiples,
    les retours charriot internes, tout en préservant le texte des balises <span>.
    Garantit la préservation des exposants (ex: INSEE¹) et la correction des mots coupés.
    """
    # Remplacer les <br> par des espaces
    for br in p_node.find_all('br'):
        br.replace_with(' ')
        
    # Remplacer les <sup> par leur équivalent unicode en exposant
    for sup in p_node.find_all('sup'):
        s = sup.get_text()
        converted = ''.join(SUPERSCRIPT_MAP.get(c, c) for c in s)
        sup.replace_with(converted)
        
    text = p_node.get_text()
    # Nettoyage des espaces insécables et espaces multiples
    text = text.replace('\xa0', ' ').replace('\u202f', ' ')
    
    # Correction des affiliations auteurs dans la prévision météo
    text = text.replace('Bouallègue1', 'Bouallègue¹').replace('Clare2', 'Clare²').replace('Chevallier1', 'Chevallier¹')
    
    # Nettoyage des références non exposant signalées comme "INSEE 1" ou "INSEE1" -> "INSEE¹"
    text = re.sub(r'\bINSEE\s*1\b', 'INSEE¹', text)
    text = re.sub(r'\bEurope\s*2\b', 'Europe²', text)
    
    # Nettoyage des espaces avant les chiffres en exposant (ex: "INSEE ¹" -> "INSEE¹", "Europe ²" -> "Europe²")
    text = re.sub(r'([^\s\(\[\{«"“])\s+([⁰¹²³⁴⁵⁶⁷⁸⁹]+)', r'\1\2', text)
    # Préserver l'espace après les conjonctions "et" ou "ou" (ex: "recensées³ et ⁴")
    text = re.sub(r'\b(et|ou)\s*([⁰¹²³⁴⁵⁶⁷⁸⁹]+)', r'\1 \2', text)
    
    # Nettoyage des apostrophes avec espaces (ex: "l '", "l' ")
    text = re.sub(r'\b([cldjsmtnCLDJSMTN])\s+[\'’]\s*', r"\1'", text)
    text = re.sub(r'\b([cldjsmtnCLDJSMTN][\'’])\s+', r"\1", text)
    text = re.sub(r'\b(qu|Qu)\s+[\'’]\s*', r"\1'", text)
    text = re.sub(r'\b(qu|Qu)[\'’]\s+', r"\1'", text)
    
    # Nettoyage des mots coupés et tirets avec espaces
    cut_cleanups = [
        (r'\be\s+-\s*mail\b', 'e-mail'),
        (r'\blui\s+-\s*même\b', 'lui-même'),
        (r'\belle\s+-\s*même\b', 'elle-même'),
        (r'\bmacro\s+-\s*stratégique\b', 'macro-stratégique'),
        (r'\bauto\s+-\s*amplifie\b', 'auto-amplifie'),
        (r'\bc\'est\s+-\s*à\s*-\s*dire\b', "c'est-à-dire"),
        (r'\ba\s+-\s*t\s*-\s*elle\b', 'a-t-elle'),
        (r'\ba\s+-\s*t\s*-\s*il\b', 'a-t-il'),
        (r'\bdonnent\s+-\s*elles\b', 'donnent-elles'),
        (r'\bpeut\s+-\s*elle\b', 'peut-elle'),
        (r'\bquarante\s+-\s*sept\b', 'quarante-sept'),
        (r'\bClaude\s+-\s*Louis\b', 'Claude-Louis'),
        (r'\bXIX\s+ème\b', 'XIXème'),
        (r'\bac\s+tivité\b', 'activité'),
        (r'\bnotab\s+le\b', 'notable'),
        (r'\bcontent\s+e\b', 'contente'),
        (r'\bch\s+ange\b', 'change'),
        (r'\bartifici\s+elle\b', 'artificielle'),
        (r'\bsa\s+tisfaction\b', 'satisfaction'),
        (r'\bconditi\s+onné\b', 'conditionné'),
        (r'\btr\s+avail\b', 'travail'),
        (r'\béqui\s+pés\b', 'équipés'),
        (r'\batt\s+ente\b', 'attente'),
        (r'\bindépendant\s+e\b', 'indépendante'),
        (r'\bpré\s+caution\b', 'précaution'),
        (r'\bse\s+s\s+travaux\b', 'ses travaux'),
        (r'\bpreu\s+ve\b', 'preuve'),
        (r'\bci\s+bler\b', 'cibler'),
        (r'\bentr\s+aînement\b', 'entraînement'),
        (r'\bquan\s+tifier\b', 'quantifier'),
    ]
    for pattern, repl in cut_cleanups:
        text = re.sub(pattern, repl, text, flags=re.IGNORECASE)

    text = ' '.join(text.split())
    return text

def format_table(table_node):
    """
    Convertit un tableau Word <table> en tableau propre responsive avec <thead> et <tbody>.
    """
    rows = table_node.find_all('tr')
    if not rows:
        return ''
    
    html_lines = ['<div class="table-container">', '  <table class="reader-table">']
    
    # Header row
    first_row = rows[0]
    th_cells = first_row.find_all(['td', 'th'])
    html_lines.append('    <thead>')
    html_lines.append('      <tr>')
    for cell in th_cells:
        cell_text = ' '.join(cell.get_text().replace('\xa0', ' ').split())
        html_lines.append(f'        <th>{html.escape(cell_text)}</th>')
    html_lines.append('      </tr>')
    html_lines.append('    </thead>')
    
    # Body rows
    if len(rows) > 1:
        html_lines.append('    <tbody>')
        for r in rows[1:]:
            td_cells = r.find_all(['td', 'th'])
            # Vérifier si la ligne n'est pas complètement vide
            row_text = ''.join(c.get_text() for c in td_cells).strip()
            if not row_text:
                continue
            html_lines.append('      <tr>')
            for cell in td_cells:
                cell_text = ' '.join(cell.get_text().replace('\xa0', ' ').split())
                linked_cell = linkify_text(cell_text)
                html_lines.append(f'        <td>{linked_cell}</td>')
            html_lines.append('      </tr>')
        html_lines.append('    </tbody>')
        
    html_lines.append('  </table>')
    html_lines.append('</div>')
    return '\n'.join(html_lines)
