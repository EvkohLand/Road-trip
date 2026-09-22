/* Modifiez ce fichier pour ajouter vos produits et vos vrais liens affiliés.
   Sans URL valide, la sélection affiche des guides utiles.
   Remplacez aussi le titre et la description par le produit réellement choisi.
   Collez les liens Amazon générés par SiteStripe, sans modifier leur identifiant.
   Amazon.fr et amzn.to sont automatiquement signalés comme liens affiliés.
   Ne pas ajouter de prix, de disponibilité, de notes ou d'avis Amazon copiés. */
/* Amazon Associates store ID (Partenaires Amazon.fr). Every Amazon link built from
   an ASIN below carries it, so commissions are credited to this account. */
const AMAZON_TAG = 'roadtriplaura-21';
const amazon = (asin) => `https://www.amazon.fr/dp/${asin}?tag=${AMAZON_TAG}`;

window.ROAD_TRIP = {
  /* Setups: one real installation photo, then every product needed to reproduce it.
     No prices here: Amazon rules forbid showing prices that are not refreshed live. */
  setups: [
    {
      category: 'CINÉMA SOUS LA TENTE',
      title: 'Une vraie soirée série, sur le toit de la voiture.',
      description: 'Écran fixé au plafond de la tente de toit, son sous l’écran, streaming dans la télécommande, le tout alimenté par une station électrique. Tout se range en quelques minutes.',
      image: './assets/setup-tv.jpg',
      alt: 'Écran fixé au plafond d’une tente de toit, avec une barre de son dessous, devant un couple allongé au coucher du soleil',
      items: [
        { role: 'L’écran', name: 'ARZOPA écran portable 144 Hz Full HD', url: amazon('B0CJCBQYDY') },
        { role: 'La fixation', name: 'CreaDream bras articulé en aluminium à pince', url: amazon('B0DHXCRRZT') },
        { role: 'Le son', name: 'ZETIY barre de son USB à clipser sur l’écran', url: amazon('B0D7ZYDDKL') },
        { role: 'Le streaming', name: 'Amazon Fire TV Stick 4K Select', url: amazon('B0CN41GMDK') },
        { role: 'L’énergie', name: 'BLUETTI AC70 station électrique 768 Wh', url: amazon('B0CCDKQ35N') }
      ]
    }
  ],
  products: [
    { category: 'ÉNERGIE', icon: 'energy', title: 'L’autonomie, où que l’on soit.', description: 'Stations électriques et solutions de recharge pour garder un peu d’énergie, même loin des prises.', url: '', merchant: '', affiliate: true },
    { category: 'CUISINE NOMADE', icon: 'cooking', title: 'Le goût du grand air.', description: 'De quoi préparer un café au réveil et un repas tout simple après une journée dehors.', url: '', merchant: '', affiliate: true },
    { category: 'CONFORT À BORD', icon: 'comfort', title: 'Un petit chez-soi, partout.', description: 'Rangement, couchage et petits essentiels pour transformer chaque arrêt en une vraie pause.', url: '', merchant: '', affiliate: true }
  ]
};
