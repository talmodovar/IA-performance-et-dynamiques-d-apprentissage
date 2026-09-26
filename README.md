# Site de publication éditoriale du Mémoire de Recherche

> **Auteur** : Thomas ALMODOVAR  
> **Formation** : Mastère Dev, Data & I.A — École IPSSI - EISI (Promotion 2025-2026)  
> **Entreprise d'accueil** : Crédit Agricole Sud Méditerranée  
> **Titre** : *L’impact de l’IA sur la performance et les dynamiques d’apprentissage*  
> **Problématique** : *Dans quelle mesure l’intégration de l’intelligence artificielle permet-elle d’améliorer la performance et les dynamiques d’apprentissage ?*

---

## 1. Présentation du projet

Ce site web a été conçu comme une **publication numérique contemporaine de haut niveau académique**, inspirée par les principes ergonomiques du rapport international *Stanford HAI AI Index* :
- **Entrée visuelle immersive** avec vidéo d'ambiance en arrière-plan (lecture muette, pause accessible, respect de `prefers-reduced-motion`).
- **Deux parcours immédiats** :
  1. *Téléchargement du document original complet* (PDF de 152 pages, 2,08 Mo).
  2. *Lecture intégrale partie par partie* directement dans le navigateur.
- **Confort de lecture éditoriale** :
  - Typographie avec empattements de qualité littéraire (*Lora*) pour le corps de texte et sans empattements moderne (*Plus Jakarta Sans*) pour l'interface.
  - Trois thèmes de lecture : **Clair (Ivoire)**, **Sépia (Ambré)**, **Sombre (Onyx)**.
  - Trois réglages de taille de texte (`A-`, `A`, `A+`).
  - **Mode Zen (Concentration)** : masquage des éléments secondaires pour une lecture apaisée (raccourci clavier `Z` ou bouton).
  - Sommaire latéral dynamique synchronisé avec le défilement (*Scrollspy*).
  - Mémorisation de la progression de lecture en local (`localStorage`) et bouton de reprise automatique sur l'accueil.
  - Bouton direct « Copier le lien » pour chaque sous-section.

---

## 2. Arborescence du site

```text
Site memoire/
├── index.html                    # Page d'accueil éditoriale (Hero vidéo, Présentation, Axes clés, Sommaire, Notice)
├── lecture/                      # Pages de lecture intégrale partie par partie
│   ├── introduction.html         # Introduction & Problématique
│   ├── partie-0.html             # Partie 0 — Fondamentaux : Comprendre l'IA
│   ├── partie-1.html             # Partie I — L'IA comme levier d'augmentation de la performance
│   ├── partie-2.html             # Partie II — L'IA et les dynamiques d'apprentissage
│   ├── partie-3.html             # Partie III — Limites, risques et cohabitation humain-IA
│   ├── conclusion.html           # Bilan, perspectives et conclusion générale
│   ├── glossaire.html            # Glossaire exhaustif et abréviations
│   ├── bibliographie.html        # Bibliographie et webographie critique annotée
│   └── annexes.html              # Table des figures, enquête FELIX et entretiens retranscrits
├── assets/
│   ├── video/
│   │   ├── video_arriere_plan.mp4 # Vidéo bokeh d'accueil
│   │   └── video_poster.jpg      # Image fixe de secours (fallback)
│   ├── pdf/
│   │   └── Memoire_ALMODOVAR_Thomas.pdf # Fichier PDF original (152 pages, 2,08 Mo)
│   └── images/
│       ├── couverture_memoire.png # Capture haute définition de la page de garde originale
│       └── logos/
│           ├── logo_ipssi.png
│           └── logo_credit_agricole.png
├── css/
│   ├── main.css                  # Design system, variables CSS, typographies, layout global, responsive
│   └── reader.css                # Styles dédiés au confort de lecture, thèmes, sommaire sticky et mode Zen
├── js/
│   ├── main.js                   # Contrôle vidéo hero, navigation mobile, reprise de lecture, toast
│   └── reader.js                 # Moteur de lecture : thèmes, taille texte, scrollspy, mode Zen, copie ancres
└── generate_reader_pages.py      # Script de génération / mise à jour des pages de lecture
```

---

## 3. Guide pratique de gestion et de maintenance

### A. Comment lancer le projet en local
Le site est constitué de pages HTML/CSS/JS statiques sans dépendance serveur complexe.
Vous pouvez le lancer instantanément :

**Option 1 : Avec Python (déjà installé)**
```bash
python -m http.server 3000
```
Ouvrez ensuite votre navigateur sur : `http://localhost:3000/`

**Option 2 : Avec Node / npx**
```bash
npx serve -p 3000
```

---

### B. Comment publier le site en ligne
Le site ne nécessitant aucun backend, il peut être hébergé gratuitement et instantanément sur n'importe quel hébergeur statique :
- **GitHub Pages** : Poussez le dossier sur un dépôt GitHub et activez *Pages* dans les paramètres du dépôt.
- **Vercel** : Glissez-déposez le dossier sur [vercel.com](https://vercel.com).
- **Netlify** : Glissez-déposez le dossier sur [netlify.com](https://app.netlify.com/drop).
- **Serveur universitaire / Caisse Régionale** : Déposez les fichiers dans le répertoire public de votre serveur web (Apache, Nginx).

---

### C. Où remplacer le fichier PDF
Pour mettre à jour le document PDF du mémoire :
1. Déposez votre nouveau fichier PDF dans :  
   `assets/pdf/Memoire_ALMODOVAR_Thomas.pdf`
2. Si la taille du fichier change (par exemple 2,15 Mo au lieu de 2,08 Mo), mettez à jour la mention dans `index.html` et dans le modèle du générateur.

---

### D. Où remplacer la vidéo et son image de couverture
1. Déposez votre vidéo (format MP4 H.264 recommandé) dans :  
   `assets/video/video_arriere_plan.mp4`
2. Déposez l'image d'affiche correspondante dans :  
   `assets/video/video_poster.jpg`  
   *(Cette image s'affiche pendant le chargement de la vidéo ou lorsque l'utilisateur a activé l'option d'accessibilité « Réduire les animations »).*

---

### E. Comment modifier ou corriger un chapitre
Deux approches possibles :
1. **Modification directe dans le HTML** :  
   Éditez simplement le fichier correspondant dans le dossier `lecture/` (par exemple `lecture/partie-1.html`). Le code HTML est propre, commenté et balisé sémantiquement.
2. **Re-génération automatique** :  
   Si vous modifiez le texte source dans `scratch_cover/sections_data.json`, lancez :
   ```bash
   python generate_reader_pages.py
   ```

---

### F. Comment modifier les couleurs, les thèmes et les polices
Toutes les règles graphiques sont centralisées dans `css/main.css` sous forme de variables CSS :
- **Couleur d'accent (Rubis)** :  
  Modifiez `--accent: #9E1B42;` et `--accent-hover: #7D1333;`.
- **Thème clair (Fond ivoire)** :  
  Modifiez `--bg-base: #F9F8F5;` et `--text-primary: #1A1D20;`.
- **Thème sépia** :  
  Modifiez le bloc `[data-theme="sepia"]`.
- **Thème sombre** :  
  Modifiez le bloc `[data-theme="dark"]`.
- **Polices** :  
  Modifiez `--font-serif` (par défaut `'Lora', serif`) et `--font-sans` (par défaut `'Plus Jakarta Sans', sans-serif`).

---

## 4. Respect des normes d'accessibilité (WCAG 2.2 AA)

- **Structure sémantique** : `header`, `nav`, `main`, `article`, `section`, `aside`, `footer` avec un seul `<h1>` par page.
- **Navigation au clavier** : Lien d'évitement (*Skip to content*) en tête de chaque page, fermeture des tiroirs et modes via la touche `Échap`, raccourci `Z` pour le mode Zen.
- **Contrastes de couleurs** : Ratio de contraste supérieur à 7:1 dans tous les thèmes (au-delà de l'exigence minimale de 4.5:1).
- **Contrôle des médias** : Bouton visible et accessible pour suspendre et reprendre la vidéo d'arrière-plan, neutralisation automatique si `prefers-reduced-motion` est détecté.
- **Indépendance vis-à-vis de JavaScript** : La totalité du texte et des liens de navigation fonctionne même si JavaScript est désactivé.
