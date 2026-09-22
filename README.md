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

Une installation = une photo réelle + la liste de tous les produits nécessaires pour la reproduire. Source unique : `content/setups.json` (`asin` = code de 10 caractères après `/dp/` dans l’adresse Amazon). `scripts/build-pages.py` la rend en HTML statique sur l’accueil et sur une page dédiée `installations/<slug>.html`, avec le lien `https://www.amazon.fr/dp/<ASIN>?tag=roadtriplaura-21`. Pas de JavaScript : robots et aperçus de partage voient le contenu.

Vignette produit : `dist/assets/products/<ASIN>.jpg`, 128×128, fond blanc. Pas de prix affichés : le règlement Amazon interdit les prix non actualisés en direct.

## Référencement et partage

Généré par `scripts/build-pages.py` pour chaque page : balise canonical, Open Graph + Twitter card (image 1200×630), données structurées JSON-LD (WebSite, Article, BreadcrumbList, ItemList), `sitemap.xml`, page `404.html` non indexée. Les descriptions sont coupées à 158 caractères ; le suffixe « | Road Trip » n’est ajouté que si le titre reste court. `scripts/check-site.py` bloque la publication si une page perd l’un de ces éléments.

Images dérivées (aperçus 1200×630, WebP, versions mobiles, icônes) : `scripts/build-images.sh`, à relancer après changement d’une photo source.

Pas de `robots.txt` : sur un site de projet GitHub Pages, les robots ne le lisent qu’à la racine du domaine (`evkohland.github.io/robots.txt`), hors de ce dépôt. Déclarer le sitemap dans Google Search Console.

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
