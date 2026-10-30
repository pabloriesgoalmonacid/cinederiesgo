"""Generate the recording-dot favicons with Python's standard library."""
from pathlib import Path
import math, struct, zlib
ROOT=Path(__file__).parent/'dist'
def png(size, opaque=False):
 rows=[]
 for y in range(size):
  row=bytearray([0])
  for x in range(size):
   d=math.hypot(x+.5-size/2,y+.5-size/2)
   radius=size*.22
   core=max(0,min(1,radius+.5-d))
   glow=.32*math.exp(-max(0,d-radius)**2/(2*(size*.115)**2))
   alpha=core+(1-core)*glow
   if opaque:row.extend((255,round(255*(1-alpha)),round(255*(1-alpha)+36*alpha),255))
   else:row.extend((255,0,36,round(255*alpha)))
  rows.append(bytes(row))
 def chunk(kind,data):return struct.pack('!I',len(data))+kind+data+struct.pack('!I',zlib.crc32(kind+data)&0xffffffff)
 return b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR',struct.pack('!2I5B',size,size,8,6,0,0,0))+chunk(b'IDAT',zlib.compress(b''.join(rows)))+chunk(b'IEND',b'')
folder=ROOT/'assets/icons';folder.mkdir(parents=True,exist_ok=True)
(folder/'rec-96.png').write_bytes(png(96))
(folder/'apple-touch-icon.png').write_bytes(png(180,True))
sizes=[16,32,48];images=[png(n) for n in sizes];offset=6+16*len(sizes);entries=[]
for size,data in zip(sizes,images):
 entries.append(struct.pack('<4B2H2I',size,size,0,0,1,32,len(data),offset));offset+=len(data)
(ROOT/'favicon.ico').write_bytes(struct.pack('<3H',0,1,len(sizes))+b''.join(entries)+b''.join(images))
