"""Marco Polo coverage. Dates verified against publisher metadata."""
from html import escape

REVIEWS = [
 ('2024-11-14','Murcia Plaza','murcia-plaza.png','Marco Polo en Prime Video','Marco Polo on Prime Video','https://murciaplaza.com/murciaplaza/marco-polo'),
 ('2023-08-31','Cinemanía','cinemania.svg','Esperanza y resiliencia en La Manga','Hope and resilience in La Manga','https://www.20minutos.es/cinemania/noticias/marco-polo-pelicula-pablo-riesgo-5168338/'),
 ('2023-08-29','La Verdad','la-verdad.svg','Una película con la luz de La Manga del Mar Menor','A film with the light of La Manga del Mar Menor','https://www.laverdad.es/culturas/marco-polo-pelicula-luz-manga-mar-menor-20230828003727-nt.html'),
]

def reviews(lang):
 months = ['ene','feb','mar','abr','may','jun','jul','ago','sep','oct','nov','dic'] if lang=='es' else ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
 rows = ''
 for date,publisher,logo,es,en,url in sorted(REVIEWS,reverse=True):
  y,m,d=date.split('-')
  rows += f'<li><a href="{escape(url)}" target="_blank" rel="noopener noreferrer"><img class="press-logo" src="/assets/press/{logo}" alt="{escape(publisher)}" loading="lazy"><span class="press-label">{escape(es if lang=="es" else en)}</span><time datetime="{date}">{int(d)} {months[int(m)-1]} {y}</time></a></li>'
 return '<section class="film-reviews" aria-labelledby="reviews-title"><h2 id="reviews-title">'+('Reseñas' if lang=='es' else 'Reviews')+'</h2><ul class="press-links">'+rows+'</ul></section>'

def watch(lang):
 label='Ver en Amazon Prime Video' if lang=='es' else 'Watch on Amazon Prime Video'
 return '<div class="film-streaming"><span>'+('Ya disponible en' if lang=='es' else 'Now streaming on')+'</span><a href="https://www.primevideo.com/detail/0PHN3WV3WIY80UU7KOUG84TL55/ref=atv_sso_std" target="_blank" rel="noopener noreferrer" aria-label="'+label+'"><img src="/assets/prime-video.svg" alt="Amazon Prime Video" width="120" height="38"></a></div>'
