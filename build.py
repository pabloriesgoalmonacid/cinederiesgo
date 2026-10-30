"""Rebuild the static site after editing content.json or dist/style.css."""
from pathlib import Path
import json, html, shutil
from press import press
from redesign import home, catalog, projects, detail
from i18n import localized_data, translate_html, UI_EN, UI_ES
ROOT=Path(__file__).parent
ORIGINAL=json.loads((ROOT/'content.json').read_text())
D=ORIGINAL
LANG='es'
def e(s):return html.escape(s)
def para(s):return '<p>'+e(s).replace('\n','<br>')+'</p>'
def img(im,alt=None,cls=''):
 return f'<img class="{cls}" src="{im["src"]}" alt="{e(alt if alt is not None else im["alt"])}" loading="lazy">'
films=['marco-polo','cvalt','mis-alignment','tiro-dominical']
titles=dict(zip(films,['Marco Polo','Cuando Volvimos A La Tierra','Mis-Alignment','Tiro Dominical']))
nav=[('peliculas','Películas'),('microdramas','MicroDramas'),('press','Prensa'),('informacion','Información'),('contacto','Contacto')]
rentals=[('cameras','Cameras'),('lenses','Lenses'),('lighting','Lighting'),('grip','Grip'),('other','Extras')]
def content(name):
 if name.startswith('microdramas/'):
  return detail(next(p for p in projects(D) if p['slug']==name.split('/')[1]))
 if name=='index':return home(D)
 if name=='microdramas':return catalog(D)
 if name=='press':return press(LANG)
 p=D[name];b=p['blocks'];ims=p['images'][1:]
 if name=='index':
  return ''.join(f'<a class="hero" href="/{key}/">'+img(ims[i],titles[key])+f'<div class="caption"><span>{e(b[i*2]["text"])}</span><h1>{titles[key]}</h1></div></a>' for i,key in enumerate(films[:2]))+'<div class="home-mark">'+img(ims[2],'Cine De Riesgo')+'</div>'
 if name=='peliculas':
  return '<div class="films-poster-gallery">'+''.join(f'<a href="/{key}/" aria-label="{e(titles[key])}">{img(ims[i],titles[key],"film-gallery-poster")}</a>' for i,key in enumerate(films))+'</div>'
 if name=='microdramas':
  cards=''
  for i in range(len(ims)):
   base=2+i*3
   cards+='<article class="drama">'+img(ims[i],b[base+1]['text'],'poster')+'<div><span class="eyebrow">'+e(b[base]['text'])+'</span><h2>'+e(b[base+1]['text'])+'</h2>'+para(b[base+2]['text'])+'</div></article>'
  return '<h1>'+e(b[0]['text'])+'</h1><div class="intro">'+para(b[1]['text'])+'</div><div class="drama-grid">'+cards+'</div>'
 if name=='informacion':
  bio='Pablo Riesgo Almonacid es guionista y director. Ha escrito y dirigido Marco Polo, Cuando Volvimos A La Tierra, Mis-Alignment y Tiro Dominical. Su trabajo en Cine De Riesgo abarca el largometraje y el cortometraje.' if LANG=='es' else 'Pablo Riesgo Almonacid is a writer and director. He wrote and directed Marco Polo, Cuando Volvimos A La Tierra, Mis-Alignment and Tiro Dominical. His work at Cine De Riesgo spans feature and short films.'
  role='Guionista y director' if LANG=='es' else 'Writer & director'
  return '<div class="split story"><aside><h1>Nuestra historia</h1></aside><div>'+''.join(para(x['text']) for x in [b[1 if LANG=='es' else 2]])+'</div></div><section class="split about-bio"><div><span class="kicker">'+role+'</span><h2>Pablo Riesgo<br>Almonacid</h2></div><div>'+para(bio)+'</div></section>'
 if name in films:
  synopsis=D['peliculas']['blocks'][3+films.index(name)*2]['text']
  back='← Todas las películas' if LANG=='es' else '← All films'
  facts=[x.strip() for x in b[0]['text'].split('|')]
  groups=[(('Guion y dirección' if LANG=='es' else 'Written & directed by'),[b[2]['text']]),(('Reparto' if LANG=='es' else 'Cast'),[x['text'] for x in b[4:7]]),(('Con el apoyo de' if LANG=='es' else 'Supported by') if name=='cvalt' else ('Distribución' if LANG=='es' else 'Distribution'),[x['text'] for x in b[8:-1]])]
  credits='<dl class="film-credits">'+''.join('<div><dt>'+e(label)+'</dt><dd>'+''.join('<span>'+e(value)+'</span>' for value in values)+'</dd></div>' for label,values in groups)+'</dl>'
  overview='<section class="film-synopsis"><h2>'+('Sinopsis' if LANG=='es' else 'Synopsis')+'</h2>'+para(synopsis)+'</section>'
  note='<section class="film-note"><h2>'+('Sobre la película' if LANG=='es' else 'About the film')+'</h2>'+para(b[-1]['text'])+'</section>'
  trailer=''
  trailer_ids={'marco-polo':'R3JV9t2qpus','mis-alignment':'fE8Beze401M'}
  if name in trailer_ids:
   video_id=trailer_ids[name]
   trailer_label='Tráiler' if LANG=='es' else 'Trailer'
   youtube_label='Ver en YouTube ↗' if LANG=='es' else 'Watch on YouTube ↗'
   trailer='<section class="film-trailer" aria-labelledby="trailer-title"><div class="trailer-heading"><h2 id="trailer-title">'+trailer_label+'</h2><a href="https://www.youtube.com/watch?v='+video_id+'" target="_blank" rel="noopener noreferrer">'+youtube_label+'</a></div><iframe src="https://www.youtube-nocookie.com/embed/'+video_id+'" title="'+e(titles[name])+' — '+trailer_label+'" width="560" height="315" loading="lazy" referrerpolicy="strict-origin-when-cross-origin" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe></section>'
  return '<a class="back" href="/peliculas/">'+back+'</a><article class="film-page"><h1 class="film-title">'+titles[name]+'</h1><ul class="film-facts">'+''.join('<li>'+e(fact)+'</li>' for fact in facts)+'</ul><div class="film-overview"><div class="film-artwork">'+img(ims[0],titles[name])+trailer+'</div><div class="film-copy">'+overview+credits+note+'</div></div></article>'+''.join(img(im,titles[name],'film-still') for im in ims[1:])

 if name=='contacto':
  return '<div class="split contact"><div><h2>Cine De Riesgo LLC</h2><h2>Cine De Riesgo SLU</h2><h2>Email</h2><a href="mailto:info@cinederiesgo.com">info@cinederiesgo.com</a>'+'</div><div><h1>Contactanos</h1><form id="contact-form"><div class="form-row"><label>Nombre<input name="nombre" autocomplete="given-name" required></label><label>Apellido<input name="apellido" autocomplete="family-name" required></label></div><label>Email<input name="email" type="email" autocomplete="email" required></label><label>Mensaje<textarea name="mensaje" rows="6" required></textarea></label><button type="submit">Preparar email ↗</button><p class="form-note">Abre tu aplicación de correo con el mensaje preparado para info@cinederiesgo.com.</p><p id="form-status" role="status"></p></form></div></div>'
 if name=='avisolegal':return '<div class="legal">'+''.join(('<h1>'+e(x['text'])+'</h1>') if i==0 else para(x['text']) for i,x in enumerate(b))+'</div>'
 return ''
for LANG in ['es','en']:
 D=localized_data(ORIGINAL,LANG)
 for removed in ['cdrrentals']+[key for key,_ in rentals]:
  D.pop(removed,None)
  obsolete=ROOT/'dist'/('en' if LANG=='en' else '')/removed
  if obsolete.exists():shutil.rmtree(obsolete)
 D['press']={}
 for project in projects(D):
  D['microdramas/'+project['slug']]={}
  titles['microdramas/'+project['slug']]=project['title']
 for name in D:
  title=titles.get(name,dict(nav+rentals).get(name,'Cine De Riesgo' if name=='index' else 'Aviso Legal'))
  title=(UI_EN if LANG=='en' else UI_ES).get(title,title)
  header='<header><a class="brand" href="/" aria-label="Cine De Riesgo — Inicio">'+'<img src="/assets/cine-de-riesgo-red-logo.png" alt="Cine De Riesgo" width="148" height="100" fetchpriority="high">'+'</a><button class="menu" aria-expanded="false" aria-controls="navigation">Menú</button><nav id="navigation" aria-label="Principal">'+''.join(f'<a href="/{k}/"'+(' aria-current="page"' if name==k else '')+'>'+v+'</a>' for k,v in nav)+'</nav></header>'
  footer='<footer><a href="/avisolegal/">Aviso Legal</a>__LANGUAGE_SWITCH__<div>© Cine de Riesgo S.L.U.<br>Cine De Riesgo LLC</div></footer>'
  doc='<!doctype html><html lang="'+LANG+'"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>'+e(title)+(' | Cine De Riesgo' if title!='Cine De Riesgo' else '')+'</title><meta name="description" content="Cine De Riesgo. Films and microdramas. Los Angeles / Madrid."><link rel="stylesheet" href="/style.css"><link rel="stylesheet" href="/redesign.css"><script defer src="/app.js?v=carousel-2"></script></head><body><a class="skip" href="#main">Saltar al contenido</a>'+header+'<main id="main" class="'+('redesigned' if name in ['index','microdramas'] or name.startswith('microdramas/') else '')+'">'+content(name)+'</main>'+footer+'</body></html>'
  path='/' if name=='index' else '/'+name+'/'
  switch='<div class="language-switch" role="group" aria-label="'+('Idioma' if LANG=='es' else 'Language')+'"><a lang="es" hreflang="es" href="'+path+'"'+(' aria-current="true"' if LANG=='es' else '')+'>Español</a><a lang="en" hreflang="en" href="/en'+path+'"'+(' aria-current="true"' if LANG=='en' else '')+'>English</a></div>'
  doc=translate_html(doc,LANG).replace('__LANGUAGE_SWITCH__',switch)
  target=ROOT/'dist'/('en' if LANG=='en' else '')/('index.html' if name=='index' else name+'/index.html')
  target.parent.mkdir(parents=True,exist_ok=True);target.write_text(doc)
print(f'Built {len(D)*2} pages in Spanish and English')
