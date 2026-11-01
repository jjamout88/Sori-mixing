"""템플릿 + sounds.json → sori-chaeksang.html.  --rebundle 이면 clips/*.mp3 에서 sounds.json 을 먼저 다시 만든다."""
import json, base64, glob, os, re, sys
here = os.path.dirname(os.path.abspath(__file__))
if '--rebundle' in sys.argv:
    out = {}
    for p in sorted(glob.glob(os.path.join(here, 'clips', '*.mp3'))):
        name = re.sub(r'-\d+$', '', os.path.basename(p)[:-4])
        out.setdefault(name, []).append(base64.b64encode(open(p, 'rb').read()).decode())
    json.dump(out, open(os.path.join(here, 'sounds.json'), 'w'))
    print('번들 재생성:', {k: len(v) for k, v in out.items()})
t = open(os.path.join(here, 'sori-chaeksang-template.html'), encoding='utf-8').read()
assert t.count('/*__SOUNDS__*/{}') == 1, '템플릿에 /*__SOUNDS__*/{} 자리가 하나 있어야 합니다'
j = open(os.path.join(here, 'sounds.json'), encoding='utf-8').read()
open(os.path.join(here, 'sori-chaeksang.html'), 'w', encoding='utf-8').write(t.replace('/*__SOUNDS__*/{}', j))
print('빌드 완료: sori-chaeksang.html', os.path.getsize(os.path.join(here, 'sori-chaeksang.html')), 'bytes')
import shutil; shutil.copyfile(os.path.join(here, 'sori-chaeksang.html'), os.path.join(os.path.dirname(here), 'full.html'))
print('../full.html 갱신')
