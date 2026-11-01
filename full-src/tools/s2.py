import sys; from search import search
for q in sys.argv[1:]:
    r=search(q,cc0=False); print('##',q,len(r))
    for x in r[:8]: print(f"  {x['id']:>7} {x['dur']:6.1f}s dl={x['dl']:<6} {x['user']:<18} {x['title'][:60]}")
