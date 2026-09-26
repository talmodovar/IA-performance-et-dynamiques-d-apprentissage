/**
 * main.js - Interactions pour la page d'accueil et le site global
 * Gestion vidéo hero, reprise de lecture, accessibilité WCAG, toast
 */

document.addEventListener('DOMContentLoaded', () => {
  initHeroVideo();
  initMobileNav();
  initResumeReading();
  initCitationCopy();
  initKeyboardNav();
});

/* ==========================================================================
   GESTION VIDÉO HERO (LANCEMENT AUTOMATIQUE EN BOUCLE)
   ========================================================================== */
function initHeroVideo() {
  const video = document.getElementById('heroVideo');
  if (!video) return;

  video.muted = true;
  video.defaultMuted = true;
  video.volume = 0;
  video.loop = true;
  video.playsInline = true;

  // Lancement automatique dès que possible
  const startVideo = () => {
    video.muted = true;
    const playPromise = video.play();
    if (playPromise !== undefined) {
      playPromise.catch(() => {
        // En cas de blocage d'autoplay strict du navigateur, lancer dès la première interaction
        const onFirstInteraction = () => {
          video.muted = true;
          video.play();
        };
        window.addEventListener('click', onFirstInteraction, { once: true, passive: true });
        window.addEventListener('touchstart', onFirstInteraction, { once: true, passive: true });
        window.addEventListener('scroll', onFirstInteraction, { once: true, passive: true });
        window.addEventListener('keydown', onFirstInteraction, { once: true, passive: true });
      });
    }
  };

  if (video.readyState >= 2) {
    startVideo();
  } else {
    video.addEventListener('canplay', startVideo, { once: true });
    video.addEventListener('loadeddata', startVideo, { once: true });
  }
  startVideo();
}

/* ==========================================================================
   NAVIGATION MOBILE
   ========================================================================== */
function initMobileNav() {
  const toggle = document.querySelector('.menu-toggle');
  const nav = document.querySelector('.main-nav');
  if (!toggle || !nav) return;

  toggle.addEventListener('click', () => {
    const isOpen = nav.classList.toggle('open');
    toggle.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
  });

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && nav.classList.contains('open')) {
      nav.classList.remove('open');
      toggle.setAttribute('aria-expanded', 'false');
      toggle.focus();
    }
  });

  document.addEventListener('click', (e) => {
    if (!toggle.contains(e.target) && !nav.contains(e.target) && nav.classList.contains('open')) {
      nav.classList.remove('open');
      toggle.setAttribute('aria-expanded', 'false');
    }
  });
}

/* ==========================================================================
   REPRISE DE LECTURE (LOCALSTORAGE SANS COMPTE)
   ========================================================================== */
function initResumeReading() {
  const banner = document.getElementById('resumeBanner');
  const link = document.getElementById('resumeBannerLink');
  const titleSpan = document.getElementById('resumeChapterTitle');
  if (!banner || !link) return;

  try {
    const raw = localStorage.getItem('memoire_last_read');
    if (raw) {
      const data = JSON.parse(raw);
      if (data && data.url && data.title) {
        if (titleSpan) titleSpan.textContent = data.title;
        link.href = data.url;
        banner.style.display = 'block';

        // Mettre à jour aussi le CTA principal du hero si disponible
        const heroPrimaryBtn = document.getElementById('btnHeroPrimary');
        if (heroPrimaryBtn) {
          heroPrimaryBtn.innerHTML = `
            <span>Reprendre ma lecture</span>
            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
          `;
          heroPrimaryBtn.href = data.url;
        }
      }
    }
  } catch (e) {
    console.warn('Accès à localStorage restreint :', e);
  }
}

/* ==========================================================================
   COPIE DE LA CITATION BIBLIOGRAPHIQUE
   ========================================================================== */
function initCitationCopy() {
  const btn = document.getElementById('btnCopyCitation');
  const citationText = document.getElementById('citationText');
  if (!btn || !citationText) return;

  btn.addEventListener('click', async () => {
    try {
      const text = citationText.innerText.trim();
      await navigator.clipboard.writeText(text);
      showToast('Citation copiée dans le presse-papier !');
    } catch (err) {
      showToast('Sélectionnez le texte manuellement pour copier.');
    }
  });
}

/* ==========================================================================
   ACCESSIBILITÉ CLAVIER GLOBALE
   ========================================================================== */
function initKeyboardNav() {
  // Focus visible pour les utilisateurs naviguant au tab
  window.addEventListener('keydown', (e) => {
    if (e.key === 'Tab') {
      document.body.classList.add('keyboard-nav');
    }
  });
}

/* ==========================================================================
   NOTIFICATIONS TOAST DISCRÈTES
   ========================================================================== */
function showToast(msg) {
  let toast = document.getElementById('siteToast');
  if (!toast) {
    toast = document.createElement('div');
    toast.id = 'siteToast';
    toast.className = 'toast-notice';
    toast.setAttribute('role', 'status');
    toast.setAttribute('aria-live', 'polite');
    document.body.appendChild(toast);
  }

  toast.textContent = msg;
  toast.classList.add('show');

  if (window.toastTimeout) clearTimeout(window.toastTimeout);
  window.toastTimeout = setTimeout(() => {
    toast.classList.remove('show');
  }, 3200);
}

// Exposer globalement pour usage dans reader.js
window.showToast = showToast;
