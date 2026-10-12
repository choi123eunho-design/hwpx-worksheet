---
name: hwpx-worksheet
description: 양식(디자인) PDF와 넣을 내용(개념 설명, 문제, 표, 수식)을 받아 한글 HWPX 파일로 조판해 주는 스킬. 사용자가 "한글파일로 만들어줘", "hwpx", "프린트/학습지/워크시트 만들어줘", "N주차 프린트"를 언급하거나, 양식 PDF + 문제/개념 텍스트를 주면서 한글 문서 산출물을 기대하는 모든 경우에 반드시 이 스킬을 사용할 것. 수학 수식(HWP 수식 스크립트), 표준정규분포표 같은 표, 페이지별 간격 규칙, 검증 루틴이 모두 여기에 정리되어 있다. 또한 사용자 PC에 설치된 글꼴 173종의 확정 목록을 갖고 있어, "제목은 나눔스퀘어 16pt 굵게로 해줘" 같은 글꼴·크기·색·굵기 지정을 그대로 반영하거나, 기존 hwpx 파일을 넣고 "이거랑 같은 서식으로 만들어줘"라고 요청할 때 서식을 분석해 재현하는 데도 이 스킬을 사용할 것.
---

# HWPX 학습지 조판 스킬

양식 PDF의 디자인을 페이지 전면 배경 이미지로 깔고, 그 위에 텍스트·수식·표를
문단 단위로 조립해서 HWPX(한글 표준 문서)를 만든다. 이 방식은 실제로 검증된
파이프라인이며, 아래 규칙을 지키면 한글에서 깨지지 않고 열린다.

## 전체 워크플로우

1. **입력 확인**: (a) 양식 PDF (디자인 페이지들), (b) 넣을 내용(텍스트/문제/표/수식),
   (c) 서식 지정이 있으면 그것도. 내용에 그래프·그림이 있는데 원본 이미지가 없으면
   `[[ 그래프 자리 — 원본 이미지 삽입 ]]` placeholder 문단으로 대체하고 사용자에게 알린다.
2. **서식 결정**: 사용자가 글꼴·크기를 지정했거나 기존 파일과 맞춰달라고 하면
   `references/fonts.md`와 `references/char-styles.md`를 읽고 처리한다. 지정이 없으면
   skeleton 기본값(본문 charPr 11 = 나눔고딕 12pt)을 그대로 쓴다.
3. **배경 이미지 생성**: 양식 PDF 각 페이지를 JPEG로 렌더링 (150dpi 권장, A4 기준):
   `pdftoppm -jpeg -r 150 양식.pdf bg/page` → `BinData/image{N}.jpeg`
   페이지 수가 늘어나면 디자인이 같은 페이지의 배경 이미지를 재사용해도 된다
   (여러 섹션이 같은 binaryItemIDRef를 참조 가능).
4. **섹션 XML 작성**: 페이지 1장 = 섹션 1개 (`Contents/section{N}.xml`).
   `references/xml-templates.md`를 반드시 먼저 읽고 그 스니펫을 그대로 변형해서 쓴다.
   `assets/skeleton/Contents/section_concept_example.xml`(개념 페이지),
   `section_problem_example.xml`(문제+표 페이지)은 실제 완성본에서 가져온
   살아있는 예제이므로 구조가 헷갈리면 이것을 연다.
5. **간격(레이아웃)**: `references/layout-rules.md`의 빈 문단 계산법을 따른다.
   임의로 빈 줄 개수를 정하지 말 것 — 계산식이 있다.
6. **수식**: 모든 수학 기호/식은 `<hp:equation>`의 HWP 수식 스크립트로 넣는다.
   문법은 `references/equation-syntax.md` 참조.
7. **등록 정보 갱신**: 새 문서의 섹션 수/이미지 수에 맞게 4곳을 **전부** 일치시킨다:
   - `Contents/header.xml`의 `secCnt`
   - `Contents/content.hpf`의 manifest(item)와 spine(itemref)
   - `META-INF/container.rdf`의 섹션/이미지 목록
   부분만 고치면 문서가 손상된다(과거 실제 사고 원인).
8. **패키징**: `python3 scripts/package_hwpx.py <소스폴더> <출력.hwpx>`
   (mimetype을 첫 항목·무압축으로 넣는 규칙이 스크립트에 구현되어 있음)
9. **검증**: `python3 scripts/validate_hwpx.py <출력.hwpx>` — 전부 통과해야 납품.
   하나라도 FAIL이면 원인을 고치고 재검증한다.

## 시작 자산 (assets/skeleton/)

검증 완료된 실제 문서에서 추출한 뼈대. **새 문서는 이 폴더를 복사해서 시작한다.**
- `mimetype`, `version.xml`, `settings.xml`, `META-INF/*`: 그대로 사용.
- `Contents/header.xml`: 스타일 정의 완비 (paraPr/charPr 표는 layout-rules.md 참조).
  표 셀 문단(paraPr 27)의 왼쪽 여백은 0으로 수정된 상태 — **되돌리지 말 것**
  (여백을 주면 좁은 셀에서 "0.52"가 "0.5/2"로 줄바꿈되는 버그 재발).
- `Contents/content.hpf`: 매니페스트/스파인 템플릿. 섹션·이미지 목록만 교체.
- `installed-fonts.txt`: 사용자 PC 설치 글꼴 확정 목록. validate가 자동 대조한다.
- 예제 섹션 2개: 구조 참고용이며 최종 패키지에 넣지 않는다.

## 페이지 유형별 조립 요약

- **표지/구분지**: 배경 이미지 문단 1개만 있는 섹션.
- **개념 페이지**: 배경(제목 디자인 포함) + 빈 문단 (제목 높이만큼, 계산식 사용)
  + 본문 문단들 + 성질 박스(1×1 표) + placeholder.
- **문제 페이지**: 배경(예제N 헤더) + 빈 문단 → 문제1 (지문/수식/표/선택지)
  → 빈 문단 (문제2가 페이지 상단에서 152mm 지점에 오도록 계산) → 문제2.
  단독 문제 페이지는 문제1만. 선택지는 `  ① ...    ② ...` 형태의 한 문단.

## 글꼴·서식 (신규)

**사용자의 기본 글꼴은 나눔 계열이다.** 별도 지정이 없으면 나눔 계열로 조판한다
(skeleton 기본값이 이미 그렇게 되어 있다). 함초롬·HY·휴먼 계열은 명시적 요청 시에만.

설치 글꼴 목록은 확정되어 있다. 목록에 없는 이름을 쓰면 한글이 임의의 다른 글꼴로
대체 렌더링해서 줄 수가 바뀌고 레이아웃이 무너진다. **글꼴 이름은 추측하지 말고
반드시 목록에서 고른다.**

목록의 기준은 Windows 글꼴 폴더가 아니라 **한글 프로그램의 글꼴 목록 표기**다.
둘은 다를 수 있다 (폴더의 `HYGothic 중간` = 한글의 `HY중고딕`). HY 계열의 끝
`B/M/L`은 굵기가 아니라 이름의 일부이므로 반드시 붙여 쓴다.

- 사람이 읽는 목록·용도별 추천: `references/fonts.md`
- 기계 대조용 목록: `assets/installed-fonts.txt` (validate가 자동으로 읽음)
- charPr/paraPr 인벤토리와 서식 지정법: `references/char-styles.md`

세 가지 상황별 대응:

**(a) 사용자가 서식을 지정한 경우** ("제목은 나눔스퀘어 16pt 굵게 남색")
```bash
python3 scripts/apply_style.py Contents/header.xml --add-charpr \
  '{"font":"나눔스퀘어","pt":16,"bold":true,"color":"#1F3864"}'
# → charPrIDRef="33" 을 반환. 이 id를 section XML의 <hp:run>에 쓴다.
```
글꼴 등록·`itemCnt` 갱신·lang 그룹 7개 동기화·XML 검증을 스크립트가 다 한다.
**header.xml을 손으로 편집하지 말 것.**

**(b) 기존 파일과 똑같이 맞춰달라는 경우**
```bash
python3 scripts/inspect_style.py 기존파일.hwpx --used
```
글꼴, charPr별 크기·색·굵기·장평·자간, 사용 횟수와 **샘플 텍스트**, paraPr별
정렬·여백·줄간격이 표로 나온다. 샘플을 보면 각 서식의 역할을 바로 알 수 있다.
결과를 사용자에게 표로 보고한 뒤 그 서식을 새 문서에 적용한다.

**(c) 지정이 없는 경우** — skeleton 기본값 유지. 본문 `charPrIDRef="11"`
(나눔고딕 12pt), 표 안 숫자 `14`(나눔바른펜 장평 96), 강조 `15`(빨강 굵게).

기존 글꼴 슬롯의 이름만 바꾸는 것이 가장 안전하다 (charPr 참조가 전부 살아있음):
```bash
python3 scripts/apply_style.py Contents/header.xml --set-face "5=나눔스퀘어"
```

> 참고: skeleton의 글꼴 슬롯 id=4는 원래 `한컴바탕`이었으나 사용자 설치 목록에
> 없어 `함초롬바탕`으로 교체해 두었다. 되돌리지 말 것.

**본문 글자 크기를 바꿨으면 `layout-rules.md`의 빈 문단 계산을 다시 할 것.**
줄 높이가 달라져 아래 요소가 전부 밀린다.

## 절대 규칙

- XML을 수정하면 반드시 `xml.dom.minidom.parse`로 유효성 확인.
- 섹션/이미지를 추가·삭제하면 등록 정보 4곳을 동시에 갱신.
- 글꼴 이름은 `assets/installed-fonts.txt`에 있는 것만 사용. 사용자가 목록에 없는
  글꼴을 요청하면 **임의로 비슷한 걸 넣지 말고** 가장 가까운 대안을 제시해 확인받는다.
- 글꼴·글자모양 변경은 `apply_style.py`로만. header.xml 직접 편집 금지.
- 숫자 답·수식이 포함된 문제는 납품 전에 SymPy로 계산 검증 (사용자의 기존 워크플로우).
- 최종 산출물은 validate_hwpx.py 전체 통과 후에만 사용자에게 전달.
- 한글(HWP) 렌더링을 이 환경에서 직접 확인할 수 없으므로, 사용자가 인쇄/내보내기한
  PDF를 주면 layout-rules.md의 측정법으로 위치를 픽셀 측정해 보정한다.
