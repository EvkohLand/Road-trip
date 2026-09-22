from pathlib import Path
from html import escape as e
from datetime import date
import json, re
root=Path(__file__).resolve().parents[1]
dist=root/'dist'
guides=json.loads((root/'content/guides.json').read_text())
setup_data=json.loads((root/'content/setups.json').read_text())
# Absolute public URL: canonical, Open Graph and sitemap need absolute links.
SITE='https://evkohland.github.io/Road-trip/'
PUBLISHED='2026-09-22'
import subprocess
# Last real change (last commit date), not the build date: a dateModified that moves on
# every deploy is a false freshness signal. Falls back to today outside git.
try: TODAY=subprocess.run(['git','log','-1','--format=%cs'],cwd=root,capture_output=True,text=True,check=True).stdout.strip() or date.today().isoformat()
except Exception: TODAY=date.today().isoformat()

def short(text, limit=158):
    """Meta description: Google shows ~155-160 chars; cut on a word boundary."""
    if len(text)<=limit: return text
    return text[:limit].rsplit(' ',1)[0].rstrip(' ,;:.')+'…'
OG_DEFAULT='assets/og-default.jpg'  # 1200x630, built by scripts/build-images.sh

def amazon(asin): return f'https://www.amazon.fr/dp/{asin}?tag={setup_data["amazon_tag"]}'

def seo(title, description, path, image=OG_DEFAULT, image_alt=None, kind='website', jsonld=None, noindex=False):
    """Canonical + Open Graph + Twitter card + JSON-LD block for one page."""
    url=SITE+path
    description=short(description)
    image_alt=image_alt or 'Route de montagne sinueuse dans les Alpes, invitation au road trip'
    tags=[f'<link rel="canonical" href="{url}">',
          f'<meta name="robots" content="{"noindex, follow" if noindex else "index, follow, max-image-preview:large, max-snippet:-1"}">',
          '<meta property="og:site_name" content="Road Trip">','<meta property="og:locale" content="fr_FR">',
          f'<meta property="og:type" content="{kind}">',f'<meta property="og:title" content="{e(title)}">',
          f'<meta property="og:description" content="{e(description)}">',f'<meta property="og:url" content="{url}">',
          f'<meta property="og:image" content="{SITE+image}">','<meta property="og:image:width" content="1200">',
          '<meta property="og:image:height" content="630">',f'<meta property="og:image:alt" content="{e(image_alt)}">',
          '<meta name="twitter:card" content="summary_large_image">',f'<meta name="twitter:title" content="{e(title)}">',
          f'<meta name="twitter:description" content="{e(description)}">',f'<meta name="twitter:image" content="{SITE+image}">']
    if kind=='article':
        tags+= [f'<meta property="article:published_time" content="{PUBLISHED}">',f'<meta property="article:modified_time" content="{TODAY}">']
    if jsonld:
        # "</" escaped so a string can never close the script element.
        tags.append('<script type="application/ld+json">'+json.dumps(jsonld,ensure_ascii=False).replace('</','<\\/')+'</script>')
    return '<!-- seo -->\n  '+'\n  '.join(tags)+'\n  <!-- /seo -->'

PUBLISHER={'@type':'Organization','name':'Road Trip','url':SITE,'logo':{'@type':'ImageObject','url':SITE+'assets/icon-512.png','width':512,'height':512}}
def breadcrumb(*items):
    return {'@type':'BreadcrumbList','itemListElement':[{'@type':'ListItem','position':i+1,'name':n,'item':SITE+u} for i,(n,u) in enumerate(items)]}

def render_setup(st, base='./', heading='h3', link=True, lcp=False):
    """Static HTML for a setup card (readable by crawlers and link-preview bots, no JS needed)."""
    img=base+st['image']; small=img.replace('.jpg','-800.jpg')
    title=e(st['title'])
    if link: title=f'<a href="{base}installations/{st["slug"]}.html">{title}</a>'
    items=''
    for it in st['items']:
        items+=(f'<li><a class="setup-item" href="{e(amazon(it["asin"]))}" target="_blank" rel="sponsored nofollow noopener" referrerpolicy="strict-origin-when-cross-origin">'
                f'<img class="setup-thumb" src="{base}assets/products/{it["asin"]}.jpg" alt="" width="64" height="64" loading="lazy" decoding="async">'
                f'<span class="setup-text"><span class="setup-role">{e(it["role"])}</span><span class="setup-name">{e(it["name"])}</span></span>'
                '<span class="setup-arrow">Amazon ↗</span></a></li>')
    sizes='(max-width: 900px) 100vw, 56vw'
    # lcp=True when the photo is the page's main image: load it eagerly and first.
    loading='fetchpriority="high"' if lcp else 'loading="lazy"'
    webp=f'<source type="image/webp" srcset="{small[:-4]}.webp 800w, {img[:-4]}.webp 1400w" sizes="{sizes}">'
    return (f'<article class="setup-card"><div class="setup-photo"><picture>{webp}<img src="{img}" srcset="{small} 800w, {img} 1400w" sizes="{sizes}" '
            f'alt="{e(st["alt"])}" width="{st["image_width"]}" height="{st["image_height"]}" {loading} decoding="async"></picture></div>'
            f'<div class="setup-body"><span class="product-category">{e(st["category"])}</span><{heading}>{title}</{heading}><p>{e(st["description"])}</p>'
            f'<ol class="setup-items">{items}</ol><span class="link-meta">Publicité · liens affiliés Amazon · nouvel onglet</span></div></article>')
mention='En tant que Partenaire Amazon, je réalise un bénéfice sur les achats remplissant les conditions requises.'
head=(dist/'index.html').read_text().split('<head>')[1].split('</head>')[0]
head=head[:head.index('  <script')]

def page(title, description, body, sub=False, path='', image=OG_DEFAULT, image_alt=None, kind='website', jsonld=None, back=('guides.html','← Tous les guides'), noindex=False):
    base='../' if sub else './'
    # Brand suffix only when it fits: Google cuts titles around 60 characters.
    full=title+' | Road Trip' if len(title)<=48 else title
    h=re.sub(r'<title>.*?</title>','<title>'+e(full)+'</title>',head,flags=re.S)
    h=re.sub(r'<meta name="description" content="[^"]*">','<meta name="description" content="'+e(short(description))+'">',h)
    h=h.replace('./style.css',base+'style.css').replace('./assets/',base+'assets/')
    h+='  '+seo(full,description,path,image,image_alt,kind,jsonld,noindex)+'\n'
    return f'''<!doctype html><html lang="fr"><head>{h}</head><body><a class="skip-link" href="#contenu">Aller au contenu</a><header class="header wrap"><a class="brand" href="{base}">ROAD TRIP<span class="brand-dot">.</span></a><nav aria-label="Navigation principale"><a href="{base}guides.html">Les guides</a><a class="nav-button" href="{base}a-propos.html">À propos</a></nav></header><main id="contenu" class="reading wrap"><a href="{base}{back[0]}">{back[1]}</a>{body}</main>{footer(base)}</body></html>'''

def footer(base='./'):
    return f'''<footer class="footer wrap site-footer"><div><a class="brand" href="{base}">ROAD TRIP.</a><p>{mention}</p></div><nav aria-label="Informations du site"><a href="{base}guides.html">Guides</a><a href="{base}a-propos.html">À propos et méthode</a><a href="{base}transparence.html">Affiliation</a><a href="{base}confidentialite.html">Confidentialité</a></nav></footer>'''

(dist/'guides').mkdir(exist_ok=True)
cards=[]
for g in guides:
    body=f'<p class="eyebrow">{e(g["category"])}</p><h1>{e(g["title"])}</h1><p class="article-meta">Rédaction Road Trip · Publié le 22 septembre 2026 · Guide pratique</p><p class="lead">{e(g["intro"])}</p>'
    for title,text in g['sections']: body+=f'<section><h2>{e(title)}</h2><p>{e(text)}</p></section>'
    if g.get('affiliate_links'):
        body+='<section><h2>Les références Qbrick PRO</h2><p>Voici les liens Amazon fournis pour retrouver les modules de cette installation. Vérifiez la référence, les dimensions et le contenu de l’offre sur la fiche Amazon avant de commander.</p>'
        for link in g['affiliate_links']:
            body+=(f'<p><a class="guide-read" href="{e(link["url"])}" target="_blank" rel="sponsored nofollow noopener" referrerpolicy="strict-origin-when-cross-origin">{e(link["label"])} →</a><br>'
                   '<span class="link-meta">Publicité · lien affilié Amazon · nouvel onglet</span></p>')
        body+='</section>'
    body+='<aside class="editorial-note">Ce guide présente une méthode de préparation. Il ne rapporte pas un test produit ni un voyage personnel. Les notices des fabricants et les consignes locales restent les références pour votre équipement et vos activités.</aside>'
    body+='<p><a href="../a-propos.html">Notre méthode éditoriale</a> · <a href="../transparence.html">Comprendre les liens affiliés</a></p>'
    gpath=f'guides/{g["slug"]}.html'
    ld={'@context':'https://schema.org','@graph':[{'@type':'Article','headline':g['title'],'description':g['intro'],'inLanguage':'fr-FR',
        'datePublished':PUBLISHED,'dateModified':TODAY,'image':SITE+OG_DEFAULT,'mainEntityOfPage':SITE+gpath,'articleSection':g['category'],
        'author':{'@type':'Organization','name':'Rédaction Road Trip','url':SITE+'a-propos.html'},'publisher':PUBLISHER},
        breadcrumb(('Accueil',''),('Guides','guides.html'),(g['title'],gpath))]}
    (dist/'guides'/f'{g["slug"]}.html').write_text(page(g['title'],g['intro'],body,True,gpath,kind='article',jsonld=ld))
    cards.append(f'<article class="guide-card"><p class="eyebrow">{e(g["category"])}</p><h3><a href="./guides/{g["slug"]}.html">{e(g["title"])}</a></h3><p>{e(g["intro"])}</p><a class="guide-read" href="./guides/{g["slug"]}.html">Lire le guide →</a></article>')
index='<p class="eyebrow">LE CARNET PRATIQUE</p><h1>Préparer la route.</h1><p class="lead">Des guides pour organiser le départ, comparer les équipements et garder de la place pour le voyage.</p><div class="guide-grid">'+''.join(cards)+'</div>'
gl={'@context':'https://schema.org','@graph':[{'@type':'CollectionPage','name':'Tous les guides road trip','url':SITE+'guides.html','inLanguage':'fr-FR',
    'mainEntity':{'@type':'ItemList','itemListElement':[{'@type':'ListItem','position':i+1,'url':SITE+f'guides/{g["slug"]}.html','name':g['title']} for i,g in enumerate(guides)]}},
    breadcrumb(('Accueil',''),('Guides','guides.html'))]}
(dist/'guides.html').write_text(page('Tous les guides road trip','Guides pratiques pour organiser un road trip : bagages, coffre, cuisine compacte, énergie, budget et équipements à comparer avant de partir.',index,path='guides.html',jsonld=gl,back=('','← Accueil')))
info={
'a-propos':('À propos et méthode éditoriale','''<h1>Des repères pour partir simplement.</h1><p class="lead">Road Trip est un site éditorial francophone consacré à l’organisation des escapades en voiture et aux équipements de voyage.</p><h2>Ce que vous trouverez ici</h2><p>Nos guides proposent des méthodes de préparation : partir de ses usages, vérifier les dimensions, organiser les affaires et comparer les contraintes avant un achat. Le site ne vend pas de produits et ne prend pas de réservations.</p><h2>Comment les contenus sont préparés</h2><p>Les guides de lancement ont été rédigés avec l’aide d’une intelligence artificielle. Ils présentent des conseils généraux d’organisation et ne prétendent pas restituer des essais sur le terrain. Aucun avis client, résultat de test ou expérience de voyage n’est inventé. Lorsqu’un futur article rapporte un essai personnel, il devra préciser le matériel, les conditions et les limites de cet essai.</p><h2>Nos critères de comparaison</h2><p>Nous privilégions l’usage, l’encombrement, les compatibilités documentées, les contraintes de rangement et le contenu réel de l’offre. Un lien marchand ne démontre pas qu’un produit a été testé. Les informations techniques doivent être contrôlées dans la documentation du fabricant avant l’achat.</p><h2>Signaler une erreur</h2><p>Vous pouvez signaler une erreur éditoriale dans les <a href="https://github.com/EvkohLand/Road-trip/issues">issues du projet GitHub</a> si vous disposez d’un compte. Ce canal est public : n’y déposez aucune donnée personnelle, commande ou information confidentielle.</p><h2>Crédit photographique</h2><p>Photo d’accueil : Dimitry Anikin, <a href="https://commons.wikimedia.org/wiki/File:Gro%C3%9Fglockner-Hochalpenstra%C3%9Fe_2.jpg">Großglockner-Hochalpenstraße 2</a>, Wikimedia Commons, licence CC0. Image redimensionnée.</p>'''),
'transparence':('Affiliation et transparence',f'''<h1>Des liens identifiés, un choix qui vous appartient.</h1><p class="lead">{mention}</p><h2>Reconnaître un lien rémunéré</h2><p>Les liens commerciaux rémunérés portent la mention « Publicité · lien affilié » à côté du bouton. Un achat éligible peut générer une commission pour le site, sans coût supplémentaire lié à ce lien. Vous êtes libre de consulter les guides sans acheter.</p><h2>Un site éditorial indépendant</h2><p>Road Trip n’est pas une boutique Amazon et ne représente pas Amazon. La participation au programme ne signifie pas qu’Amazon approuve nos articles. Le vendeur indiqué sur la page marchande gère la vente ; les conditions de commande, de livraison et de retour sont celles qui y sont présentées.</p><h2>Prix, disponibilité et avis</h2><p>Nous n’affichons pas de prix ni de disponibilité Amazon recopiés manuellement. Consultez la fiche marchande pour connaître l’offre au moment de votre visite. Nous ne reproduisons ni étoiles ni avis clients Amazon. Les descriptions éditoriales ne sont pas des preuves de performance.</p><h2>Lors d’un clic</h2><p>Le lien peut transmettre un identifiant d’affiliation au marchand pour attribuer les achats éligibles. La destination Amazon est indiquée avant le clic. Aucun transfert automatique vers un marchand n’est déclenché à la simple lecture du site. Consultez aussi notre <a href="./confidentialite.html">page de confidentialité</a>.</p>'''),
'confidentialite':('Confidentialité', '''<h1>Votre navigation, en clair.</h1><p class="article-meta">Version du 22 septembre 2026</p><h2>Sur Road Trip</h2><p>Cette version du site ne propose ni compte utilisateur, ni formulaire, ni newsletter, ni paiement. Le code du site n’installe aucun cookie, ne lit pas le stockage local et n’intègre aucun outil d’analyse d’audience ou pixel publicitaire. Les polices sont celles de votre appareil et les images sont servies avec le site.</p><h2>Hébergement GitHub Pages</h2><p>GitHub Pages reçoit les données techniques nécessaires à la fourniture des pages. GitHub indique notamment enregistrer l’adresse IP des visiteurs pour des raisons de sécurité, même sans connexion à un compte GitHub. Les durées et modalités de ces traitements relèvent des informations publiées par GitHub ; nous ne leur attribuons pas une durée que nous ne pouvons pas vérifier.</p><p>Consultez la <a href="https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement">déclaration de confidentialité de GitHub</a> et sa <a href="https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages">documentation Pages</a> pour connaître ces traitements et les moyens d’exercer vos droits auprès de GitHub.</p><h2>Liens vers Amazon et d’autres sites</h2><p>Un clic sur un lien externe vous conduit sur un autre site. Les liens affiliés peuvent transmettre l’identifiant du partenaire et permettre à Amazon d’attribuer un achat. Amazon peut utiliser ses propres cookies et traiter des informations relatives à votre visite selon ses paramètres et sa <a href="https://www.amazon.fr/gp/help/customer/display.html?nodeId=201909010">politique de confidentialité</a>. Ces technologies ne sont pas chargées sur Road Trip par un widget Amazon.</p><h2>Liens de signalement</h2><p>Si vous ouvrez une issue GitHub, vous utilisez le service GitHub et les informations saisies peuvent devenir publiques. Ne publiez pas de données sensibles dans ce canal. Cette page décrit les fonctions actuellement présentes ; l’ajout futur d’un formulaire, d’un outil statistique ou d’un contenu intégré devra entraîner une nouvelle évaluation et une mise à jour de cette information.</p>''')}
info_desc={'a-propos':'Qui est derrière Road Trip, comment les guides sont rédigés et selon quels critères les équipements de road trip sont comparés.',
 'transparence':'Comment Road Trip signale ses liens affiliés Amazon, ce qu’un clic transmet et pourquoi aucun prix ni avis Amazon n’est recopié.',
 'confidentialite':'Road Trip n’utilise ni cookie applicatif, ni formulaire, ni outil de mesure d’audience : ce qui se passe réellement lors de votre visite.'}
for slug,(title,body) in info.items(): (dist/f'{slug}.html').write_text(page(title,info_desc[slug],body,path=f'{slug}.html',back=('','← Accueil')))

# Setup pages: one indexable page per installation (photo + full product list).
(dist/'installations').mkdir(exist_ok=True)
for st in setup_data['setups']:
    spath=f'installations/{st["slug"]}.html'
    og=f'assets/og-{st["slug"]}.jpg'
    body=(f'<p class="eyebrow">{e(st["category"])}</p><h1>{e(st["seo_title"])}</h1><p class="lead">{e(st["seo_description"])}</p>'
          '<div class="setups">'+render_setup(st,'../','h2',False,lcp=True)+'</div>'
          '<p><a href="../guides.html">Nos guides pour préparer la route</a> · <a href="../transparence.html">Comprendre les liens affiliés</a></p>')
    ld={'@context':'https://schema.org','@graph':[{'@type':'WebPage','name':st['seo_title'],'description':st['seo_description'],'url':SITE+spath,'inLanguage':'fr-FR',
        'primaryImageOfPage':{'@type':'ImageObject','url':SITE+st['image']},'datePublished':PUBLISHED,'dateModified':TODAY,'publisher':PUBLISHER,
        'mainEntity':{'@type':'ItemList','name':'Matériel de l’installation','itemListElement':[{'@type':'ListItem','position':i+1,'name':it['name'],'url':amazon(it['asin'])} for i,it in enumerate(st['items'])]}},
        breadcrumb(('Accueil',''),(st['seo_title'],spath))]}
    (dist/spath).write_text(page(st['seo_title'],st['seo_description'],body,True,spath,og,st['alt'],'article',ld,('#selection','← La sélection')))

# 404 page: served by GitHub Pages for unknown URLs; never indexed.
(dist/'404.html').write_text(page('Page introuvable','Cette page n’existe pas ou plus. Retrouvez la sélection et les guides Road Trip.',
    '<h1>Cette route ne mène nulle part.</h1><p class="lead">La page demandée n’existe pas ou a été déplacée.</p><p><a href="https://evkohland.github.io/Road-trip/">Retour à l’accueil</a> · <a href="https://evkohland.github.io/Road-trip/guides.html">Tous les guides</a></p>',
    path='404.html',noindex=True,back=('','← Accueil')).replace('href="./','href="'+SITE).replace('src="./','src="'+SITE))
p=dist/'index.html'; s=p.read_text()
start=s.index('<footer'); end=s.index('</footer>',start)+len('</footer>'); s=s[:start]+footer()+s[end:]
if 'id="guides"' not in s:
    s=s.replace('    <section id="esprit"','    <section id="guides" class="wrap guide-section"><div class="section-heading"><div><p class="eyebrow">LE CARNET PRATIQUE</p><h2>Préparer, choisir, partir.</h2></div><a href="./guides.html">Voir les dix guides →</a></div><div class="guide-grid">'+''.join(cards[:3])+'</div></section>\n    <section id="esprit"')
s=s.replace('<a href="#esprit">L’esprit road trip</a>','<a href="./guides.html">Les guides</a>')
s=s.replace('Transparence : lorsqu’un lien est indiqué « lien affilié », un achat peut nous rapporter une commission, sans surcoût pour vous.',mention+' Les liens commerciaux sont signalés à côté des boutons.')
s=s.replace('<div id="products" class="product-grid"></div><noscript><p>Activez JavaScript pour consulter les équipements et leurs liens.</p></noscript>','<div id="products" class="product-grid">'+''.join(cards[i] for i in [3,4,1])+'</div>')
s=s.replace('<div id="setups" class="setups"></div>','<div id="setups" class="setups"><!-- setups --><!-- /setups --></div>')
s=re.sub(r'<!-- setups -->.*?<!-- /setups -->',lambda m:'<!-- setups -->'+''.join(render_setup(st) for st in setup_data['setups'])+'<!-- /setups -->',s,flags=re.S)
home_title=re.search(r'<title>(.*?)</title>',s).group(1)
home_desc=re.search(r'<meta name="description" content="([^"]*)">',s).group(1)
home_ld={'@context':'https://schema.org','@graph':[
    {'@type':'WebSite','@id':SITE+'#website','name':'Road Trip','url':SITE,'inLanguage':'fr-FR','description':home_desc,'publisher':PUBLISHER},
    dict(PUBLISHER,**{'@id':SITE+'#organization'}),
    {'@type':'ItemList','name':'Installations Road Trip','itemListElement':[{'@type':'ListItem','position':i+1,'url':SITE+f'installations/{st["slug"]}.html','name':st['seo_title']} for i,st in enumerate(setup_data['setups'])]}]}
first=setup_data['setups'][0]
s=re.sub(r'\n  <!-- seo -->.*?<!-- /seo -->','',s,flags=re.S)
s=s.replace('</head>','  '+seo(home_title,home_desc,'',f'assets/og-{first["slug"]}.jpg',first['alt'],'website',home_ld)+'\n</head>',1)
p.write_text(s)

urls=['','guides.html']+[f'guides/{g["slug"]}.html' for g in guides]+[f'installations/{st["slug"]}.html' for st in setup_data['setups']]+['a-propos.html','transparence.html','confidentialite.html']
(dist/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    +''.join(f'  <url><loc>{SITE+u}</loc><lastmod>{TODAY}</lastmod></url>\n' for u in urls)+'</urlset>\n')
print(f'Generated {len(guides)} guides and {len(info)+1} information/index pages.')
