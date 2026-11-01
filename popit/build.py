"""popit-template.html + clips/*.mp3 → popit.html (단일 파일, 소리 base64 내장)"""
import json, base64, glob, os, re
here = os.path.dirname(os.path.abspath(__file__))
out = {}
for p in sorted(glob.glob(os.path.join(here, 'clips', '*.mp3')), key=lambda s: int(re.findall(r'(\d+)\.mp3$', s)[0])):
    name = re.sub(r'-\d+$', '', os.path.basename(p)[:-4])
    out.setdefault(name, []).append(base64.b64encode(open(p, 'rb').read()).decode())
t = open(os.path.join(here, 'popit-template.html'), encoding='utf-8').read()
assert t.count('/*__SOUNDS__*/{}') == 1
html = t.replace('/*__SOUNDS__*/{}', json.dumps(out))
open(os.path.join(here, 'popit.html'), 'w', encoding='utf-8').write(html)
print('빌드 완료: popit.html', len(html.encode()), 'bytes', {k: len(v) for k, v in out.items()})
# 배포 폴더 안에 있으면 루트 index.html 도 갱신
root = os.path.dirname(here)
if os.path.exists(os.path.join(root, '.nojekyll')):
    open(os.path.join(root, 'index.html'), 'w', encoding='utf-8').write(html); print('../index.html 갱신')
