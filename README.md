# Road Trip

Site statique français consacré aux équipements de road trip et aux liens d’affiliation. Hébergement : GitHub Pages. Aucune base de données, aucun secret ni outil d’analyse nécessaire.

## Mettre ses liens d’affiliation

Modifier `dist/content.js` dans GitHub puis enregistrer sur `main`. Chaque entrée contient :

```js
{ category: 'ÉNERGIE', icon: 'energy', title: 'Nom du produit', description: 'Votre description honnête du produit.', url: 'https://votre-lien-affilie.example/produit', merchant: 'Nom de la boutique', affiliate: true }
```

Remplacer l’URL d’exemple par le vrai lien fourni par votre programme. Les valeurs `icon` disponibles sont `energy`, `cooking`, `comfort`. Ajouter ou retirer des entrées pour modifier la sélection. Les cartes initiales sont des catégories éditoriales, pas des avis sur des produits testés. Remplacer leurs textes lorsque les produits sont choisis.

Une URL vide ou invalide affiche « Sélection à venir ». Aucun identifiant d’affiliation n’est inventé. Les liens affiliés actifs portent `rel="sponsored nofollow noopener noreferrer"` et une mention explicite. Les textes sont insérés avec `textContent`.

## Publication

Dans **Settings → Pages → Build and deployment → Source**, sélectionner **GitHub Actions**. Le workflow `.github/workflows/pages.yml` publie seulement `dist/` à chaque push sur `main`. La première activation peut demander de relancer le workflow depuis **Actions → Deploy GitHub Pages → Run workflow**.

Adresse prévue : https://evkohland.github.io/Road-trip/

Tous les fichiers utilisent des chemins relatifs compatibles avec le sous-répertoire `/Road-trip/`.

## Personnalisation

- Contenu et liens : `dist/content.js`
- Textes de la page : `dist/index.html`
- Couleurs et mise en page responsive : `dist/style.css`
- Image : `dist/assets/road.jpg` (crédit dans `CREDITS.md`)

Polices Google Fonts : DM Sans et Manrope, avec repli sans-serif. Aucun cookie applicatif ni stockage local. Les liens marchands ouvrent un nouvel onglet. Compléter les informations d’éditeur adaptées à votre statut avant une exploitation commerciale.

## Vérification locale

```sh
node --check dist/app.js
node --check dist/content.js
python3 -m http.server 8080 --directory dist
```
