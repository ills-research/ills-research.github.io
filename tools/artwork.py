"""Optional: regenerate original illustrations. Requires Pillow and NumPy."""
from pathlib import Path
from math import sin,cos,pi,exp,sqrt
import numpy as np
from PIL import Image,ImageDraw,ImageFilter
OUT=Path(__file__).resolve().parents[1]/'site/assets/art'
OUT.mkdir(parents=True, exist_ok=True)
# A sampled ribbon folded around a trefoil. Depth sorting gives the surface volume.
S=2
W,H=1000,810
def surface(u,v):
    c,s=np.cos,np.sin
    def curve(t):
        return np.stack(((1.05+.55*c(3*t))*c(2*t),(1.05+.55*c(3*t))*s(2*t),.67*s(3*t)),-1)
    d=curve(u+.001)-curve(u-.001)
    d/=np.linalg.norm(d,axis=-1,keepdims=True)
    n=np.cross(d,np.array([0,0,1]))
    n/=np.linalg.norm(n,axis=-1,keepdims=True)
    b=np.cross(d,n)
    a=curve(u)+(.26+.035*c(3*u))[...,None]*c(v)[...,None]*n+.26*s(v)[...,None]*b
    x,y,z=a[...,0],a[...,1],a[...,2]
    y,z=y*c(.65)-z*s(.65),y*s(.65)+z*c(.65)
    x,y=x*c(-.22)-y*s(-.22),x*s(-.22)+y*c(-.22)
    return x,y,z
u,v=np.meshgrid(np.linspace(0,2*pi,680,endpoint=False),np.linspace(0,2*pi,70,endpoint=False))
x,y,z=surface(u,v)
scale=min(934/(x.max()-x.min()),738/(y.max()-y.min()))
xx=((x-(x.min()+x.max())/2)*scale+W/2)*S
yy=(-(y-(y.min()+y.max())/2)*scale+H/2)*S
zz=(z-z.min())/(z.max()-z.min())
# Cyan sweep and blue-violet shadows track the geometry, not the screen.
t=np.clip((np.cos(u-.8)+.45*np.sin(v+u)+.9)/2.0,0,1)
intensity=(.51+.47*zz)*(.81+.19*np.cos(v-1.1))
im=Image.new('RGBA',(W*S,H*S))
d=ImageDraw.Draw(im)
for i,j in zip(*np.unravel_index(np.argsort(z,axis=None),z.shape)):
    dep=zz[i,j]; a=t[i,j]; lum=intensity[i,j]
    col=tuple(int(n*lum) for n in (69+66*a+28*dep,102+146*a,252-34*a))+(int(190+55*dep),)
    px,py=xx[i,j],yy[i,j]
    # hairline filaments connect the samples on alternating paths
    k=(j+1)%u.shape[1]
    if i%3==0:
        d.line((px,py,xx[i,k],yy[i,k]),fill=(*col[:3],int(80+78*dep)),width=1)
    if j%9==0:
        k2=(i+1)%u.shape[0]
        d.line((px,py,xx[k2,j],yy[k2,j]),fill=(*col[:3],int(62+66*dep)),width=1)
    rad=(.64+.35*dep)*S
    d.ellipse((px-rad,py-rad,px+rad,py+rad),fill=col)
im.resize((1200,972),Image.Resampling.LANCZOS).save(OUT/'learning-surface.webp',quality=93,method=6)
# Four original diagrams, each with its own visual vocabulary.
def line(p,c,w=1,op=1):
    return '<polyline points="'+' '.join(f'{a:.2f},{b:.2f}' for a,b in p)+f'" fill="none" stroke="{c}" stroke-width="{w}" opacity="{op}"/>'
def circle(x,y,r,c,op=1):
    return f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{r}" fill="{c}" opacity="{op}"/>'
for ax,(fg,bg) in enumerate([('#5e6ccc','#edf0fc'),('#267e77','#e2f3f0'),('#465c9f','#e9eef9'),('#8b61aa','#f1eaf5')],1):
    paths=[]
    if ax==1:
        for fixed in range(-18,19):
            for mode in [0,1]:
                pts=[]
                for k in range(100):
                    a,b=fixed/8,(k-49.5)/22
                    if mode:a,b=b,a
                    z=exp(-((a+.5)**2+(b-.3)**2)*.7)-.6*exp(-((a-.7)**2+(b+.8)**2)*1.15)
                    pts.append((180+36*a+27*b,92+12*a-12*b-65*z))
                paths.append(line(pts,fg,.8,.82))
    elif ax==2:
        for j in range(33):
            pts=[]
            for k in range(160):
                a=2*pi*k/159
                r=1+.15*sin(3*a+.1*j)+.06*cos(5*a-.03*j)
                pts.append((177+cos(a)*r*(64+j*1.25)+j*.6,82+sin(a)*r*(18+j*1.15)-j*.28))
            paths.append(line(pts,fg,1,.78))
    elif ax==3:
        pts=[(76,100),(110,48),(131,107),(162,70),(179,32),(194,103),(222,82),(233,129),(264,49),(290,103),(216,33),(95,136)]
        for i,p in enumerate(pts):
            for j,q in enumerate(pts[:i]):
                if (p[0]-q[0])**2+(p[1]-q[1])**2<78**2:paths.append(line([p,q],fg,1,.65))
        for i,p in enumerate(pts):
            paths.append(circle(*p,8 if i in [2,3,6] else 4,fg,.23));paths.append(circle(*p,3,fg))
    else:
        for i in range(105):
            x0=180+(i-52)*2.45; amp=45*exp(-((i-53)/32)**2)
            y=sin(i/12)*15
            paths.append(line([(x0,77+y-amp*(.6+.4*cos(i/6))),(x0,77+y+amp*(.6+.4*sin(i/6)))],fg,1.55,.88))
        for n in range(7):
            paths.append(line([(50+k*1.3,83+sin((k+n*4)/24)*(3+27*exp(-((k-102)/45)**2))+n*2) for k in range(201)],fg,.7,.38))
    (OUT/f'axis-{ax}.svg').write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 360 160"><rect width="360" height="160" fill="{bg}"/>'+''.join(paths)+'</svg>')
