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
    try { const url = new URL(value); return url.protocol === 'https:' && !url.username && !url.password ? url.href : null; }
    catch { return null; }
  }
  // Setups: photo of a real installation plus the list of every product it uses.
  const setupContainer = document.getElementById('setups');
  for (const setup of window.ROAD_TRIP?.setups || []) {
    const card = element('article', 'setup-card');
    const figure = element('div', 'setup-photo');
    const img = element('img', '');
    img.src = setup.image; img.alt = setup.alt || ''; img.loading = 'lazy'; img.width = 1400; img.height = 1050;
    figure.append(img);
    const body = element('div', 'setup-body');
    body.append(element('span', 'product-category', setup.category), element('h3', '', setup.title), element('p', '', setup.description));
    const list = element('ol', 'setup-items');
    for (const item of setup.items || []) {
      const li = element('li', '');
      const url = validUrl(item.url);
      const target = url ? element('a', 'setup-item') : element('div', 'setup-item pending');
      if (url) { target.href = url; target.target = '_blank'; target.rel = 'sponsored nofollow noopener'; target.referrerPolicy = 'strict-origin-when-cross-origin'; }
      // Product thumbnail: white-background packshot stored in assets/products/ (see CREDITS.md).
      if (item.image) {
        const thumb = element('img', 'setup-thumb');
        thumb.src = item.image; thumb.alt = ''; thumb.loading = 'lazy'; thumb.width = 64; thumb.height = 64;
        target.append(thumb);
      }
      const text = element('span', 'setup-text');
      text.append(element('span', 'setup-role', item.role), element('span', 'setup-name', item.name));
      const arrow = element('span', 'setup-arrow', url ? 'Amazon ↗' : 'À venir');
      target.append(text, arrow);
      li.append(target);
      list.append(li);
    }
    body.append(list, element('span', 'link-meta', 'Publicité · liens affiliés Amazon · nouvel onglet'));
    card.append(figure, body);
    setupContainer?.append(card);
  }
  const activeProducts = products.filter(product => validUrl(product.url));
  if (!activeProducts.length) return; // Keep useful static guides when no product is configured.
  container.replaceChildren();
  for (const product of activeProducts) {
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
      const host = new URL(url).hostname.toLowerCase();
      const isAmazon = host === 'amzn.to' || host === 'amazon.fr' || host.endsWith('.amazon.fr');
      const isAffiliate = isAmazon || product.affiliate;
      link.rel = isAffiliate ? 'sponsored nofollow noopener' : 'noopener';
      link.referrerPolicy = 'strict-origin-when-cross-origin';
      const label = element('span', '', isAmazon ? 'Voir sur Amazon' : (product.merchant ? `Découvrir chez ${product.merchant}` : 'Découvrir le produit'));
      label.append(element('span', 'link-meta', isAffiliate ? 'Publicité · lien affilié · nouvel onglet' : 'Nouvel onglet'));
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
