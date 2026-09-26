/**
 * reader.js - Moteur d'expérience de lecture éditoriale
 * Confort typographique, thèmes clair/sépia/sombre, mode concentration,
 * barre de progression, scrollspy pour sommaire actif, mémorisation de lecture
 */

document.addEventListener('DOMContentLoaded', () => {
  initPreferences();
  initReadingProgress();
  initScrollspy();
  initCopySectionLinks();
  initMobileToc();
  recordCurrentReadingPosition();
});

/* ==========================================================================
   PRÉFÉRENCES DE LECTURE (THÈMES, TAILLES, MODE CONCENTRATION)
   ========================================================================== */
function initPreferences() {
  const root = document.documentElement;

  // Restaurer thème
  let savedTheme = 'light';
  try {
    savedTheme = localStorage.getItem('reader_theme') || 'light';
  } catch (e) {}
  applyTheme(savedTheme);

  // Restaurer taille texte
  let savedSize = 'standard';
  try {
    savedSize = localStorage.getItem('reader_size') || 'standard';
  } catch (e) {}
  applyTextSize(savedSize);

  // Boutons de thème
  const themeBtns = document.querySelectorAll('[data-set-theme]');
  themeBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const theme = btn.getAttribute('data-set-theme');
      applyTheme(theme);
      try {
        localStorage.setItem('reader_theme', theme);
      } catch (e) {}
      if (window.showToast) window.showToast(`Thème : ${theme === 'dark' ? 'Sombre' : theme === 'sepia' ? 'Sépia' : 'Clair'}`);
    });
  });

  // Boutons de taille de texte
  const sizeBtns = document.querySelectorAll('[data-set-size]');
  sizeBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const size = btn.getAttribute('data-set-size');
      applyTextSize(size);
      try {
        localStorage.setItem('reader_size', size);
      } catch (e) {}
      if (window.showToast) window.showToast(`Taille du texte : ${size === 'small' ? 'Petite' : size === 'large' ? 'Grande' : 'Standard'}`);
    });
  });

  // Mode concentration (Zen mode)
  const zenBtn = document.getElementById('btnZenMode');
  if (zenBtn) {
    zenBtn.addEventListener('click', toggleZenMode);
  }

  // Raccourci clavier 'z' pour basculer le mode concentration
  document.addEventListener('keydown', (e) => {
    // Si l'utilisateur n'est pas dans un input/textarea
    if (['INPUT', 'TEXTAREA'].includes(document.activeElement.tagName)) return;
    if (e.key === 'z' || e.key === 'Z') {
      toggleZenMode();
    }
    if (e.key === 'Escape' && document.body.classList.contains('zen-mode')) {
      toggleZenMode(false);
    }
  });

  function applyTheme(theme) {
    root.setAttribute('data-theme', theme);
    document.querySelectorAll('[data-set-theme]').forEach(b => {
      const isActive = b.getAttribute('data-set-theme') === theme;
      b.classList.toggle('active', isActive);
      b.setAttribute('aria-pressed', isActive ? 'true' : 'false');
    });
  }

  function applyTextSize(size) {
    root.setAttribute('data-text-size', size);
    document.querySelectorAll('[data-set-size]').forEach(b => {
      const isActive = b.getAttribute('data-set-size') === size;
      b.classList.toggle('active', isActive);
      b.setAttribute('aria-pressed', isActive ? 'true' : 'false');
    });
  }

  function toggleZenMode(forceState) {
    const isZen = typeof forceState === 'boolean'
      ? forceState
      : !document.body.classList.contains('zen-mode');

    document.body.classList.toggle('zen-mode', isZen);
    if (zenBtn) {
      zenBtn.classList.toggle('active', isZen);
      zenBtn.setAttribute('aria-pressed', isZen ? 'true' : 'false');
      zenBtn.querySelector('.zen-label').textContent = isZen ? 'Quitter le mode Zen' : 'Mode concentration';
    }
    if (window.showToast) {
      window.showToast(isZen ? 'Mode concentration activé (Échap ou "Z" pour quitter)' : 'Mode normal rétabli');
    }
  }
}

/* ==========================================================================
   BARRE DE PROGRESSION DE LECTURE AU DÉFILEMENT
   ========================================================================== */
function initReadingProgress() {
  const bar = document.querySelector('.reading-progress-bar');
  if (!bar) return;

  function updateBar() {
    const totalHeight = document.documentElement.scrollHeight - window.innerHeight;
    if (totalHeight <= 0) {
      bar.style.width = '0%';
      return;
    }
    const currentProgress = (window.scrollY / totalHeight) * 100;
    bar.style.width = `${Math.min(100, Math.max(0, currentProgress))}%`;
  }

  window.addEventListener('scroll', updateBar, { passive: true });
  updateBar();
}

/* ==========================================================================
   SCROLLSPY (SOMMAIRE ACTIF SYNCHRONISÉ)
   ========================================================================== */
function initScrollspy() {
  const tocLinks = document.querySelectorAll('.chapter-toc-link');
  if (tocLinks.length === 0) return;

  const headings = Array.from(document.querySelectorAll('.reader-content h2[id], .reader-content h3[id]'));
  if (headings.length === 0) return;

  const observerOptions = {
    root: null,
    rootMargin: '-80px 0px -65% 0px',
    threshold: 0
  };

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const id = entry.target.getAttribute('id');
        setActiveTocLink(id);
      }
    });
  }, observerOptions);

  headings.forEach(h => observer.observe(h));

  function setActiveTocLink(id) {
    tocLinks.forEach(link => {
      const href = link.getAttribute('href');
      const matches = href === `#${id}`;
      link.classList.toggle('active', matches);
      if (matches) {
        // Faire défiler doucement le lien dans la sidebar si nécessaire
        link.scrollIntoView({ block: 'nearest', inline: 'nearest', behavior: 'smooth' });
      }
    });
  }
}

/* ==========================================================================
   BOUTON COPIER LE LIEN DIRECT D'UNE SECTION
   ========================================================================== */
function initCopySectionLinks() {
  const headings = document.querySelectorAll('.reader-content h2[id], .reader-content h3[id]');
  headings.forEach(heading => {
    const btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'copy-section-btn';
    btn.setAttribute('aria-label', `Copier le lien direct vers : ${heading.textContent.trim()}`);
    btn.innerHTML = `
      <svg xmlns="http://www.w3.org/2000/svg" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/></svg>
      <span>Copier le lien</span>
    `;

    btn.addEventListener('click', async (e) => {
      e.stopPropagation();
      const id = heading.getAttribute('id');
      const url = `${window.location.origin}${window.location.pathname}#${id}`;
      try {
        await navigator.clipboard.writeText(url);
        if (window.showToast) window.showToast('Lien direct copié dans le presse-papier !');
      } catch (err) {
        if (window.showToast) window.showToast(url);
      }
    });

    heading.appendChild(btn);
  });
}

/* ==========================================================================
   SOMMAIRE MOBILE REPLIABLE
   ========================================================================== */
function initMobileToc() {
  const toggleBtn = document.getElementById('btnMobileToc');
  const sidebar = document.querySelector('.reader-sidebar');
  if (!toggleBtn || !sidebar) return;

  toggleBtn.addEventListener('click', () => {
    const isOpen = sidebar.classList.toggle('open');
    toggleBtn.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
  });

  // Fermer quand un lien du sommaire est cliqué sur mobile
  const links = sidebar.querySelectorAll('a');
  links.forEach(link => {
    link.addEventListener('click', () => {
      if (window.innerWidth <= 1024) {
        sidebar.classList.remove('open');
        toggleBtn.setAttribute('aria-expanded', 'false');
      }
    });
  });

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && sidebar.classList.contains('open')) {
      sidebar.classList.remove('open');
      toggleBtn.setAttribute('aria-expanded', 'false');
      toggleBtn.focus();
    }
  });
}

/* ==========================================================================
   MÉMORISATION DE LA LECTURE (LOCAL STORAGE)
   ========================================================================== */
function recordCurrentReadingPosition() {
  try {
    const titleEl = document.querySelector('.chapter-title');
    const partEl = document.querySelector('.chapter-part-num');
    const chapterName = titleEl ? titleEl.textContent.trim() : document.title;
    const partName = partEl ? partEl.textContent.trim() : '';

    const payload = {
      title: `${partName ? partName + ' — ' : ''}${chapterName}`,
      url: window.location.pathname,
      timestamp: Date.now()
    };

    localStorage.setItem('memoire_last_read', JSON.stringify(payload));
  } catch (e) {
    console.warn('Impossible de mémoriser la lecture :', e);
  }
}
