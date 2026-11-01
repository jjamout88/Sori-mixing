import subprocess, re, json, os, concurrent.futures as cf
os.makedirs('mp3',exist_ok=True)
meta={}
def one(name,sid):
    h=subprocess.run(['curl','-sL','-A','Mozilla/5.0',f'https://freesound.org/s/{sid}/'],capture_output=True,text=True).stdout
    mp3=re.search(r'https://cdn\.freesound\.org/previews/\d+/\d+_\d+-hq\.mp3',h) or re.search(r'https://cdn\.freesound\.org/previews/\d+/\d+_\d+-lq\.mp3',h)
    lic=re.search(r'creativecommons\.org/(licenses|publicdomain)/([a-z\-]+)/([\d.]+)',h)
    title=re.search(r'<title>([^<]*)</title>',h)
    url=re.search(r'<link rel="canonical" href="([^"]+)"',h)
    if not mp3: return sid,None
    u=mp3.group(0).replace('-lq.','-hq.')
    subprocess.run(['curl','-sL','-o',f'mp3/{sid}.mp3',u])
    return sid,dict(name=name,title=title.group(1).strip() if title else '',lic=(lic.group(2)+' '+lic.group(3)) if lic else '?',url=url.group(1) if url else f'https://freesound.org/s/{sid}/',mp3=u)
jobs=[]
with cf.ThreadPoolExecutor(8) as ex:
    for line in open('ids.txt'):
        p=line.split(); 
        for sid in p[1:]: jobs.append(ex.submit(one,p[0],sid))
    for j in jobs:
        sid,m=j.result(); meta[sid]=m; print(sid,m and (m['lic'],m['title'][:70]))
json.dump(meta,open('meta.json','w'),indent=1,ensure_ascii=False)
