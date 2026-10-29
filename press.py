"""Minimal bilingual links supplied by the site owner."""
from html import escape

ARTICLES = [
 ('Deadline', 'ReelShort y Showbox — microdramas en Corea', 'ReelShort & Showbox — microdramas in Korea', 'https://deadline.com/2026/06/reelshort-showbox-microdrama-korea-1236956135/'),
 ('Deadline', 'Premios Imagen 2024 — nominaciones', 'Imagen Awards 2024 — nominations', 'https://deadline.com/2024/07/imagen-awards-2024-nominations-list-1236021936/'),
 ('The Hollywood Reporter', 'WWE y ReelShort — colaboración en microdramas', 'WWE & ReelShort — microdrama collaboration', 'https://www.hollywoodreporter.com/business/business-news/wwe-microdramas-reelshort-collaboration-1236647005/'),
 ('Deadline', 'Futurefest — programación', 'Futurefest — lineup', 'https://deadline.com/2024/09/futurefest-lineup-unveiled-wme-1236077693/'),
 ('Variety', 'Agent of Shadows — WWE y Drew McIntyre', 'Agent of Shadows — WWE & Drew McIntyre', 'https://variety.com/2026/tv/news/wwe-microdrama-agent-of-shadows-drew-mcintyre-1236907475/'),
]

# Dates read from the publishers' datePublished metadata, not URL guesses.
DATES = ['2026-06-15', '2024-07-25', '2026-07-14', '2024-09-04', '2026-10-12']
LOGOS = {'Deadline':'deadline', 'The Hollywood Reporter':'thr', 'Variety':'variety'}

def press(lang):
 rows = ''
 months = ['ene','feb','mar','abr','may','jun','jul','ago','sep','oct','nov','dic'] if lang=='es' else ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
 for date,(publisher,es,en,url) in sorted(zip(DATES,ARTICLES),reverse=True):
  year,month,day = date.split('-')
  label = f'{int(day)} {months[int(month)-1]} {year}'
  logo = '<img class="press-logo press-logo-'+LOGOS[publisher]+'" src="/assets/press/'+LOGOS[publisher]+'.svg" alt="'+escape(publisher)+'">'
  rows += '<li><a href="'+url+'" target="_blank" rel="noopener noreferrer">'+logo+'<span class="press-label">'+escape(en if lang=='en' else es)+'</span><time datetime="'+date+'">'+label+'</time><span class="press-arrow" aria-hidden="true">↗</span></a></li>'
 return '<section class="press-page"><h1>'+('Press' if lang=='en' else 'Prensa')+'</h1><ul class="press-links">'+rows+'</ul></section>'
