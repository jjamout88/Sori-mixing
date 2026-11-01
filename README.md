# 팡팡 팝잇 (+ 소리 믹싱 책상)

- `index.html` — 팡팡 팝잇: 화면 가득 도트 팝잇. 누르거나 쓸어서 터뜨리고, 다 누르면 판이 뒤집혀요. 단일 HTML(소리 내장).
- `full.html` — 이전 버전 「소리 믹싱 책상」(1분 녹음 → 무한 루프).

## 빌드
- 팝잇: `python3 popit/build.py` → `popit/popit.html` + 루트 `index.html` 갱신 (소리: `popit/clips/popit-N.mp3`)
- 믹싱 책상: `cd full-src && python3 build.py --rebundle` → 루트 `full.html` 갱신

## 소리 출처
- 팝잇: Freesound — Sadiquecat #868928 (CC0), haus.the.child #839343 (CC0), dyingSatyr #857285 (CC0), designerschoice #811021 (CC BY 4.0). 페이지의 "출처" 버튼에도 표시.
- 믹싱 책상: full.html 하단 "소리 출처" 참고 (Freesound CC0/CC BY/CC BY-NC, 왁뿌볼은 YouTube rappeler하쁠리 영상 발췌).
