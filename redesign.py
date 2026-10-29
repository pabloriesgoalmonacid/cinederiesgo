from html import escape as e
import re, json
from pathlib import Path
ADDITIONS=json.loads((Path(__file__).parent/"microdrama-additions.json").read_text())

def picture(im,alt,cls='',eager=False):
 return f'<img class="{cls}" src="{im["src"]}" alt="{e(alt)}" loading="{"eager" if eager else "lazy"}"'+(' fetchpriority="high"' if eager else '')+'>'
def projects(D):
 p=D['microdramas'];items=[]
 for i,im in enumerate(p['images'][1:]):
  b=2+i*3;title=p['blocks'][b+1]['text'];title='King of Montana' if title=='Project Name' else title
  items.append(dict(title=title,platform=p['blocks'][b]['text'].replace('Reel Shorts','ReelShort'),synopsis=p['blocks'][b+2]['text'],image=im,slug=re.sub('[^a-z0-9]+','-',title.lower()).strip('-')))
 added=[dict(title=r["title"],platform=r["platform"],synopsis=r["description"],image=r["image"],slug=r["slug"]) for r in ADDITIONS]
 slugs={p["slug"] for p in added}
 return added+[p for p in items if p["slug"] not in slugs]

AWARDS={'queen-of-the-court':'Winner · Best Sports Vertical','queen-never-cry':'Winner · Best Drama'}
def award(p):
 if p['slug'] not in AWARDS:return ''
 return '<span class="project-award"><strong>'+AWARDS[p['slug']]+'</strong><span>Vertical Drama Love Awards</span></span>'

def card(p):
 return '<a href="/microdramas/'+p['slug']+'/" aria-label="'+e(p['title'])+'">'+picture(p['image'],p['title'],'film-gallery-poster')+award(p)+'</a>'

def contact():
 return ''

def home(D):
 banners=''.join('<div class="home-slide" role="group" aria-label="'+title+'"><a class="home-film" href="/'+key+'/" aria-label="'+title+'">'+picture(im,title)+'</a></div>' for key,title,im in [('marco-polo','Marco Polo',D['index']['images'][1]),('cvalt','Cuando Volvimos A La Tierra',D['index']['images'][2])])
 agent=next(p for p in projects(D) if p['slug']=='agent-of-shadows')
 spotlight='<div class="home-agent-feature"><a class="home-agent-poster" href="/microdramas/agent-of-shadows/" aria-label="Agent of Shadows">'+picture(agent['image'],agent['title'],eager=True)+'</a><a class="home-agent-press" href="https://variety.com/2026/tv/news/wwe-microdrama-agent-of-shadows-drew-mcintyre-1236907475/" target="_blank" rel="noopener noreferrer"><img src="/assets/press/variety.svg" alt="Variety" width="150" height="42" loading="lazy"><h2>Agent of Shadows</h2><p>WWE · Drew McIntyre</p><span class="text-link">Leer en Variety ↗</span></a></div>'
 return '<section class="home-carousel" aria-label="Proyectos destacados"><div class="home-track" id="home-track" tabindex="0"><div class="home-slide" role="group" aria-label="Agent of Shadows">'+spotlight+'</div>'+banners+'</div><div class="carousel-controls"><div class="carousel-dots">'+''.join('<button type="button" data-slide="'+str(i)+'" aria-label="'+title+'"'+(' aria-current="true"' if i==0 else '')+'></button>' for i,title in enumerate(['Agent of Shadows','Marco Polo','Cuando Volvimos A La Tierra']))+'</div></div></section>'

def catalog(D):
 return '<div class="films-poster-gallery microdrama-posters">'+''.join(card(p) for p in projects(D))+'</div>'

def detail(p):
 return '<a class="back" href="/microdramas/">← Todos los microdramas</a><article class="micro-detail"><div>'+picture(p['image'],p['title'],eager=True)+'</div><div><span class="kicker">MICRODRAMA · '+e(p['platform'])+'</span><h1>'+e(p['title'])+'</h1>'+award(p)+'<h2>Sinopsis</h2><p lang="en">'+e(p['synopsis'])+'</p><dl><div><dt>Formato</dt><dd>Serie vertical</dd></div><div><dt>Plataforma / colaboración</dt><dd>'+e(p['platform'])+'</dd></div></dl><a class="text-link" href="/contacto/">Hablemos de un proyecto ↗</a></div></article>'+contact()
