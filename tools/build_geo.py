"""Rebuild the map data embedded in index.html (GEO) and communes.js.

Inputs to download into tools/ first:
  metropole.geojson  https://raw.githubusercontent.com/gregoiredavid/france-geojson/master/metropole-version-simplifiee.geojson
  communes.geojson   https://raw.githubusercontent.com/gregoiredavid/france-geojson/master/communes-version-simplifiee.geojson
  communes.json      data/communes.json of the npm package @etalab/decoupage-administratif (populations, used to sort suggestions)
Run from the repository root: python3 tools/build_geo.py
Outputs: tools/geo.json (paste as `const GEO = ...;` in index.html) and communes.js.
"""
import json,math
fr=json.load(open('tools/metropole.geojson'))
bas=json.load(open('data/bassins-viticoles-france.geojson'))
def rings(g):
    if g['type']=='Polygon': return [g['coordinates']]
    return g['coordinates']
frfeat=fr['features'] if 'features' in fr else [fr]
allp=[p for f in frfeat for poly in rings(f['geometry']) for r in poly for p in r]
mnx=min(p[0] for p in allp);mxx=max(p[0] for p in allp);mny=min(p[1] for p in allp);mxy=max(p[1] for p in allp)
print(mnx,mxx,mny,mxy)
k=math.cos(math.radians((mny+mxy)/2));W=1000;sc=W/((mxx-mnx)*k);H=(mxy-mny)*sc
def proj(p): return ((p[0]-mnx)*k*sc,(mxy-p[1])*sc)
def dp(pts,eps):
    if len(pts)<3: return pts
    a,b=pts[0],pts[-1];dmax=0;idx=0
    dx,dy=b[0]-a[0],b[1]-a[1];L=math.hypot(dx,dy) or 1e-9
    for i in range(1,len(pts)-1):
        p=pts[i];dd=abs(dy*p[0]-dx*p[1]+b[0]*a[1]-b[1]*a[0])/L
        if dd>dmax:dmax,idx=dd,i
    if dmax>eps: return dp(pts[:idx+1],eps)[:-1]+dp(pts[idx:],eps)
    return [a,b]
def area(r): return abs(sum(r[i][0]*r[i-1][1]-r[i-1][0]*r[i][1] for i in range(len(r))))/2
def path(polys,minA,eps):
    segs=[];cx=cy=aw=0
    for poly in polys:
        for ri,ring in enumerate(poly):
            r=[proj(p) for p in ring];A=area(r)
            if A<minA: continue
            if ri==0: cx+=sum(p[0] for p in r)/len(r)*A;cy+=sum(p[1] for p in r)/len(r)*A;aw+=A
            m=len(r)//2;s=dp(r[:m+1],eps)[:-1]+dp(r[m:],eps)
            if len(s)<4: continue
            segs.append("M"+"L".join(f"{p[0]:.0f},{p[1]:.0f}" for p in s[:-1])+"Z")
    return "".join(segs),(cx/aw if aw else 0),(cy/aw if aw else 0)
frd="".join(path(rings(f['geometry']),20,1.0)[0] for f in frfeat)
out=[]
for f in bas['features']:
    d,cx,cy=path(rings(f['geometry']),15,1.0)
    out.append({"id":f['properties']['Bassin'],"d":d,"cx":round(cx),"cy":round(cy)})
G={"w":W,"h":round(H),"p":[round(mnx,5),round(mxy,5),round(k*sc,5),round(sc,5)],"fr":frd,"b":out}
s=json.dumps(G,ensure_ascii=False,separators=(',',':'))
open('tools/geo.json','w').write(s);print(round(H),len(s),len(frd))
# communes, largest population first so the autocomplete proposes the likeliest town first
pop={c['code']:c.get('population',0) or 0 for c in json.load(open('tools/communes.json'))}
c=json.load(open('tools/communes.geojson'))
rows=[]
for f in c['features']:
    g=f['geometry']
    if not g: continue
    r=max((p[0] for p in rings(g)),key=area)
    lon=sum(p[0] for p in r)/len(r);lat=sum(p[1] for p in r)/len(r)
    code=f['properties']['code'];dep=code[:3] if code.startswith('97') else code[:2]
    rows.append((pop.get(code,0),f"{f['properties']['nom']}|{dep}|{lon:.3f}|{lat:.3f}"))
rows.sort(key=lambda x:-x[0])
js="window.COMMUNES="+json.dumps("\n".join(r[1] for r in rows),ensure_ascii=False)+";"
open('communes.js','w').write(js);print(len(rows),len(js.encode()))
