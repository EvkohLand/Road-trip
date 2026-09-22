# Road Trip

Site statique français consacré aux équipements de road trip et aux liens d’affiliation. Hébergement : GitHub Pages. Aucune base de données, aucun secret ni outil d’analyse nécessaire.

## Mettre ses liens d’affiliation

Modifier `dist/content.js` dans GitHub puis enregistrer sur `main`. Chaque entrée contient :

```js
{ category: 'ÉNERGIE', icon: 'energy', title: 'Nom du produit', description: 'Votre description honnête du produit.', url: 'https://votre-lien-affilie.example/produit', merchant: 'Nom de la boutique', affiliate: true }
```

Remplacer l’URL d’exemple par le vrai lien fourni par votre programme. Les valeurs `icon` disponibles sont `energy`, `cooking`, `comfort`. Ajouter ou retirer des entrées pour modifier la sélection. Les cartes initiales sont des catégories éditoriales, pas des avis sur des produits testés. Remplacer leurs textes lorsque les produits sont choisis.

Sans produit avec URL valide, la page présente des guides pratiques. Aucun identifiant d’affiliation n’est inventé. Les liens affiliés actifs portent `rel="sponsored nofollow noopener"` et une mention explicite. Les textes sont insérés avec `textContent`.

## Installations (setups)

Une installation = une photo réelle + la liste de tous les produits nécessaires pour la reproduire. Dans `dist/content.js`, tableau `setups` :

```js
{ category: 'CINÉMA SOUS LA TENTE', title: '…', description: '…', image: './assets/setup-tv.jpg', alt: '…',
  items: [ { role: 'L’écran', name: 'ARZOPA écran portable', url: amazon('B0CJCBQYDY') } ] }
```

`amazon('ASIN')` construit le lien avec l’identifiant Partenaires `roadtriplaura-21`. L’ASIN est le code de 10 caractères après `/dp/` dans l’adresse du produit Amazon. Pas de prix affichés : le règlement Amazon interdit les prix non actualisés en direct. La mention obligatoire « En tant que Partenaire Amazon… » est dans `dist/index.html`.

## Publication

Dans **Settings → Pages → Build and deployment → Source**, sélectionner **GitHub Actions**. Le workflow `.github/workflows/pages.yml` publie seulement `dist/` à chaque push sur `main`. La première activation peut demander de relancer le workflow depuis **Actions → Deploy GitHub Pages → Run workflow**.

Adresse prévue : https://evkohland.github.io/Road-trip/

Tous les fichiers utilisent des chemins relatifs compatibles avec le sous-répertoire `/Road-trip/`.

## Personnalisation

- Contenu et liens : `dist/content.js`
- Textes de la page : `dist/index.html`
- Couleurs et mise en page responsive : `dist/style.css`
- Image : `dist/assets/road.jpg` (crédit dans `CREDITS.md`)

Polices système, sans requête Google Fonts. Aucun cookie applicatif ni stockage local. Les liens marchands ouvrent un nouvel onglet. Compléter les informations d’éditeur adaptées à votre statut avant une exploitation commerciale.

## Vérification locale

```sh
node --check dist/app.js
node --check dist/content.js
python3 -m http.server 8080 --directory dist
```


## Contenu éditorial et conformité

Les articles sont dans `content/guides.json`. Exécuter `python3 scripts/build-pages.py` après modification et versionner les pages HTML générées. Le workflow valide les liens locaux avec `python3 scripts/check-site.py` avant publication. Les articles restent lisibles sans JavaScript.

Lire `docs/amazon-compliance.md` pour les règles de maintenance et les points restant à compléter. Ne pas présenter ce dépôt comme une certification Amazon ou juridique.
