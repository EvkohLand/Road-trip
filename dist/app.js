(() => {
  'use strict';
  const icons = {
    energy: '<rect x="3" y="6" width="16" height="12" rx="2"/><path d="M21 10v4m-10-6-3 5h5l-3 4"/>',
    cooking: '<path d="M5 10h13v6a4 4 0 0 1-4 4H9a4 4 0 0 1-4-4Zm13 1h1a3 3 0 0 1 0 6h-1M8 3v3m4-3v3m4-3v3"/>',
    comfort: '<rect x="3" y="9" width="18" height="12" rx="2"/><path d="M8 9V5a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v4M3 14h18M9 13v3m6-3v3"/>'
  };
  const container = document.getElementById('products');
  const products = window.ROAD_TRIP?.products || [];
  const element = (tag, className, text) => {
    const node = document.createElement(tag);
    node.className = className;
    if (text) node.textContent = text;
    return node;
  };
  function validUrl(value) {
    try { const url = new URL(value); return ['https:', 'http:'].includes(url.protocol) ? url.href : null; }
    catch { return null; }
  }
  for (const product of products) {
    const card = element('article', 'product-card');
    const top = element('div', 'product-top');
    const icon = element('div', 'product-icon');
    icon.setAttribute('aria-hidden', 'true');
    icon.innerHTML = `<svg viewBox="0 0 24 24">${icons[product.icon] || icons.comfort}</svg>`;
    top.append(icon, element('span', 'product-category', product.category));
    const body = element('div', 'product-body');
    body.append(element('h3', '', product.title), element('p', '', product.description));
    const url = validUrl(product.url);
    if (url) {
      const link = element('a', 'product-link');
      link.href = url;
      link.target = '_blank';
      link.rel = product.affiliate ? 'sponsored nofollow noopener noreferrer' : 'noopener noreferrer';
      const label = element('span', '', product.merchant ? `Découvrir chez ${product.merchant}` : 'Découvrir le produit');
      label.append(element('span', 'link-meta', product.affiliate ? 'Lien affilié · nouvel onglet' : 'Nouvel onglet'));
      const arrow = element('span', '', '↗'); arrow.setAttribute('aria-hidden', 'true');
      link.append(label, arrow);
      body.append(link);
    } else {
      body.append(element('span', 'product-link pending', 'Sélection à venir'));
    }
    card.append(top, body);
    container.append(card);
  }
  if (!products.length) container.append(element('p', '', 'Notre sélection arrive bientôt.'));
})();
