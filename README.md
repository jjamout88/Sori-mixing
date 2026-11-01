# 소리 믹싱 책상 (소리 책상 v2)

책상 위 물건을 1분 동안 마구 눌러 녹음하면, 그 소리가 똑같은 타이밍으로 무한 반복되는 ASMR 믹싱 장난감.

## 실행
- `sori-chaeksang.html` 을 브라우저로 그냥 열면 됨 (서버 필요 없음, 소리는 파일 안에 base64로 내장).
- 폰: 이 HTML 파일을 폰에 옮겨 열거나, PC에서 `python3 -m http.server` 후 같은 와이파이로 접속.
- 인터넷은 픽셀 폰트(Google Fonts)에만 씀. 없어도 동작.

## 사용법
1. 시작 → 자유롭게 눌러보기
2. ● 녹음 → 첫 소리를 내는 순간부터 60초 카운트다운
3. 60초가 끝나거나 ■ 녹음 끝 → 바로 무한 루프 재생 (누른 물건이 반짝임)
4. ■ 정지 / ▶ 무한 재생 / ● 다시 녹음 / ⤓ WAV(루프 한 바퀴를 이음새 없이 저장)
- 마지막 믹스는 브라우저(localStorage)에 저장돼 다음에 열어도 ▶로 다시 들을 수 있음.
- 빗소리·모닥불은 배경음(녹음 안 됨). 재생 중에도 위에 덧연주 가능(녹음 안 됨).

## 개발
- 소스: `sori-chaeksang-template.html` → `python3 build.py --rebundle` (clips/*.mp3 → sounds.json → 최종 HTML)
- 새 소리: `tools/` 파이프라인 (Freesound 검색 `search.py`/`s2.py`, 다운로드 `dl.py`(ids.txt), 자르기 `slice2.py plan2.json clips`)
- 녹음 원리: 모든 소리는 `play()` 한 함수로 나며, 녹음 중이면 (시각·버퍼 번호·음높이·음량·좌우·물건 id)를 기록.
  재생은 25ms 간격 lookahead 스케줄러가 `AudioBufferSourceNode.start(정확한 시각)`으로 예약 → 샘플 단위로 같은 타이밍.
- 왁뿌볼 소리: YouTube "왁뿌 왕창 많이 하고 싶어서 만들어 본 왁뿌볼 ASMR" (rappeler하쁠리, https://www.youtube.com/watch?v=nwPvPG-1UCw) 2:00–5:00 구간 발췌
- 출처: 페이지 하단 "소리 출처" 및 tools/credits.json
