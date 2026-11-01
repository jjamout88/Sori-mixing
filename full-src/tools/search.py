import re, sys, subprocess, json, urllib.parse, html
def search(q, cc0=True):
    url = "https://freesound.org/search/?q="+urllib.parse.quote_plus(q)
    if cc0: url += "&f=license:%22Creative+Commons+0%22"
    url += "&s=Downloads+%28most+first%29"
    h = subprocess.run(['curl','-sL','-A','Mozilla/5.0',url],capture_output=True,text=True).stdout
    res=[]
    for m in re.finditer(r'data-sound-id="(\d+)"\s+data-username="([^"]*)".*?data-mp3="([^"]*)".*?data-title="([^"]*)"\s+data-duration="([^"]*)".*?data-num-downloads="(\d+)"', h, re.S):
        sid,u,mp3,t,d,n=m.groups()
        res.append(dict(id=sid,user=u,mp3=mp3.replace('-lq.','-hq.'),title=html.unescape(t),dur=float(d),dl=int(n)))
    return res
if __name__=='__main__':
    for q in sys.argv[1:]:
        r=search(q)
        print('##',q,len(r))
        for x in r[:10]: print(f"  {x['id']:>7} {x['dur']:6.1f}s dl={x['dl']:<6} {x['user']:<18} {x['title'][:60]}")
