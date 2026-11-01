import numpy as np, subprocess, os, sys, json
SR=44100
def load(sid, t0=0, t1=None):
    cmd=['ffmpeg','-loglevel','error','-ss',str(t0)]+(['-t',str(t1-t0)] if t1 else [])+['-i',f'mp3/{sid}.mp3','-ac','1','-ar',str(SR),'-f','f32le','-']
    return np.frombuffer(subprocess.run(cmd,capture_output=True).stdout,dtype=np.float32).copy()
def env_(d,win=0.004):
    n=int(SR*win); k=np.ones(n)/n; return np.sqrt(np.convolve(d*d,k,'same'))
def hp(d):  # remove DC/rumble
    a=np.exp(-2*np.pi*40/SR); y=np.zeros_like(d); px=0; py=0
    for i in range(0,len(d)):
        pass
    return d-np.convolve(d,np.ones(256)/256,'same')
def onsets(d,thr_rel,min_gap):
    env=env_(d); peak=np.percentile(env,99.9); thr=max(peak*thr_rel,0.003)
    hop=int(SR*0.002); fr=env[::hop]; look=20; gap=int(min_gap/0.002); res=[]; i=look; last=-gap
    while i<len(fr):
        prev=fr[i-look:i-2].mean()+1e-6
        if fr[i]>thr and fr[i]>2.5*prev and i-last>=gap:
            j=i
            while j>0 and fr[j-1]<fr[j] and fr[j-1]>thr*0.3: j-=1
            res.append(j*hop); last=i
        i+=1
    return res,env
def cut(d,start,end,maxlen,minlen,tail=0.05):
    s=max(0,start-int(SR*0.005)); e=min(end+int(SR*0.03),start+int(SR*maxlen),len(d))
    seg=d[s:e].copy(); env=env_(seg); pk=env.max()
    m=int(SR*minlen); below=np.where(env[m:]<pk*tail)[0]
    for b in below:
        jj=m+b
        if (env[jj:jj+int(SR*0.05)]<pk*tail).all(): seg=seg[:jj+int(SR*0.02)]; break
    return seg
def norm(seg,target_db=-16):
    env=env_(seg); act=env[env>env.max()*0.1]; rms=np.sqrt((act**2).mean())+1e-9
    g=10**(target_db/20)/rms; seg=seg*g; pk=np.abs(seg).max()
    if pk>0.89: seg*=0.89/pk
    fi=int(SR*0.003); fo=min(int(SR*0.025),len(seg)//3)
    seg[:fi]*=np.linspace(0,1,fi); seg[-fo:]*=np.linspace(1,0,fo); return seg
def export(seg,path):
    subprocess.run(['ffmpeg','-y','-loglevel','error','-f','f32le','-ar',str(SR),'-ac','1','-i','-','-ar','44100','-b:a','96k',path],input=seg.astype(np.float32).tobytes())
plan=json.load(open(sys.argv[1])); OUT=sys.argv[2]; os.makedirs(OUT,exist_ok=True)
only=sys.argv[3:]
for name,cfg in plan.items():
    if only and name not in only: continue
    for f in os.listdir(OUT):
        if f.rsplit('-',1)[0]==name: os.remove(os.path.join(OUT,f))
    segs=[]
    for src in cfg['files']:
        sid=src['id'] if isinstance(src,dict) else src
        t0=src.get('t0',0) if isinstance(src,dict) else 0; t1=src.get('t1') if isinstance(src,dict) else None
        d=hp(load(sid,t0,t1))
        if cfg.get('mode')=='loop':
            L=int(SR*cfg['len']); x=d[int(SR*cfg.get('off',0)):][:L].copy(); cf=int(SR*0.8)
            x[:cf]=x[:cf]*np.linspace(0,1,cf)+x[-cf:]*np.linspace(1,0,cf); x=x[:-cf]
            x=x/np.abs(x).max()*0.6; segs.append((1,x,sid)); continue
        on,env=onsets(d,cfg.get('thr',0.2),cfg.get('gap',0.08))
        for i,o in enumerate(on):
            nxt=on[i+1] if i+1<len(on) else len(d)
            if cfg.get('nonext'): nxt=len(d)
            seg=cut(d,o,nxt,cfg.get('max',0.5),cfg.get('min',0.03),cfg.get('tail',0.05))
            if len(seg)<SR*cfg.get('minlen',0.04): continue
            segs.append((float(env[o:o+int(SR*0.02)].max()),seg,sid))
    segs.sort(key=lambda s:-s[0])
    # skip the loudest few outliers optionally
    segs=segs[cfg.get('skip',0):cfg.get('skip',0)+cfg.get('n',8)]
    for i,(_,seg,sid) in enumerate(segs):
        if cfg.get('mode')!='loop': seg=norm(seg,cfg.get('db',-16))
        export(seg,os.path.join(OUT,f'{name}-{i}.mp3'))
    print(f"{name:9} {len(segs):2} {[round(len(s[1])/SR,2) for s in segs]} src={sorted(set(s[2] for s in segs))}")
