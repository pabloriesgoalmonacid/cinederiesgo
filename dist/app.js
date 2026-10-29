const menu=document.querySelector('.menu');
menu?.addEventListener('click',()=>{const open=menu.getAttribute('aria-expanded')!=='true';menu.setAttribute('aria-expanded',String(open));document.querySelector('nav').classList.toggle('open',open)});
document.querySelector('#contact-form')?.addEventListener('submit',event=>{event.preventDefault();const data=new FormData(event.currentTarget);const name=`${data.get('nombre')} ${data.get('apellido')}`;const body=`${data.get('mensaje')}\n\n${name}\n${data.get('email')}`;window.location.href=`mailto:info@cinederiesgo.com?subject=${encodeURIComponent((document.documentElement.lang==='en'?'Contact — ':'Contacto — ')+name)}&body=${encodeURIComponent(body)}`;document.querySelector('#form-status').textContent=document.documentElement.lang==='en'?'Message prepared. Send it from your email application; it has not been sent automatically.':'Mensaje preparado. Envíalo desde tu aplicación de correo; no se ha enviado automáticamente.'});
// The custom cursor is purely decorative; native keyboard focus stays visible.
const cursorMedia=window.matchMedia('(hover: hover) and (pointer: fine) and (forced-colors: none)');
const cursor=document.createElement('div');
cursor.className='risk-cursor';cursor.setAttribute('aria-hidden','true');document.body.append(cursor);
let cursorFrame=0,cursorX=0,cursorY=0;
function hideCursor(){document.documentElement.classList.remove('risk-cursor-active');cursor.classList.remove('over-link');if(cursorFrame){cancelAnimationFrame(cursorFrame);cursorFrame=0;}}
function drawCursor(){cursor.style.transform=`translate3d(${cursorX}px,${cursorY}px,0)`;cursorFrame=0;}
document.addEventListener('pointermove',event=>{
 if(!cursorMedia.matches||event.pointerType==='touch'){hideCursor();return;}
 cursorX=event.clientX;cursorY=event.clientY;
 if(!document.documentElement.classList.contains('risk-cursor-active'))drawCursor();
 document.documentElement.classList.add('risk-cursor-active');
 cursor.classList.toggle('over-link',Boolean(event.target.closest('a,button,input,textarea,select,summary,[role="button"]')));
 if(!cursorFrame)cursorFrame=requestAnimationFrame(drawCursor);
},{passive:true});
document.documentElement.addEventListener('pointerleave',hideCursor);
window.addEventListener('blur',hideCursor);
document.addEventListener('visibilitychange',()=>{if(document.hidden)hideCursor();});
document.addEventListener('keydown',event=>{if(event.key==='Tab')hideCursor();});
cursorMedia.addEventListener('change',hideCursor);

// Native swiping, dot navigation, and automatic advance after six idle seconds.
const carousel=document.querySelector('.home-carousel');
if(carousel){
 const track=carousel.querySelector('.home-track');
 const slides=[...track.children],dots=[...carousel.querySelectorAll('[data-slide]')];
 const reduced=window.matchMedia('(prefers-reduced-motion: reduce)');
 let index=0,frame=0,timer=0,dragging=false;
 const keyboardFocus=()=>carousel.contains(document.activeElement)&&document.activeElement.matches(':focus-visible');
 function stop(){clearTimeout(timer);timer=0;}
 function schedule(){
  stop();
  if(document.hidden||reduced.matches||dragging||keyboardFocus())return;
  timer=setTimeout(()=>{go(index+1);schedule();},6000);
 }
 function update(){
  index=Math.max(0,Math.min(slides.length-1,Math.round(track.scrollLeft/track.clientWidth)));
  dots.forEach((dot,i)=>{if(i===index)dot.setAttribute('aria-current','true');else dot.removeAttribute('aria-current');});
  slides.forEach((slide,i)=>{slide.inert=i!==index;});
  frame=0;
 }
 function go(i){track.scrollTo({left:((i+slides.length)%slides.length)*track.clientWidth,behavior:reduced.matches?'instant':'smooth'});}
 dots.forEach((dot,i)=>dot.addEventListener('click',()=>{go(i);schedule();}));
 track.addEventListener('scroll',()=>{if(!frame)frame=requestAnimationFrame(update);schedule();},{passive:true});
 track.addEventListener('keydown',event=>{if(event.key==='ArrowRight'||event.key==='ArrowLeft'){event.preventDefault();go(index+(event.key==='ArrowRight'?1:-1));}schedule();});
 carousel.addEventListener('pointerdown',()=>{dragging=true;stop();});
 window.addEventListener('pointerup',()=>{dragging=false;schedule();});
 window.addEventListener('pointercancel',()=>{dragging=false;schedule();});
 carousel.addEventListener('click',schedule);
 carousel.addEventListener('focusin',schedule);
 carousel.addEventListener('focusout',()=>setTimeout(schedule,0));
 document.addEventListener('visibilitychange',schedule);
 reduced.addEventListener('change',schedule);
 new ResizeObserver(()=>{track.scrollTo({left:index*track.clientWidth,behavior:'instant'});}).observe(track);
 update();schedule();
}
