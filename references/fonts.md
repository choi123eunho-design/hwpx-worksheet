# 사용 가능한 글꼴 목록

**이 목록은 사용자 PC(Windows + 한글)에 실제로 설치된 글꼴이다.** 여기 없는 글꼴을
`face="..."`에 적으면 한글이 문서를 열 때 다른 글꼴로 대체 렌더링해서 레이아웃이
틀어진다. **반드시 이 목록 안에서만 고를 것.**

## 대원칙 3가지

1. **HWPX는 글꼴 파일을 품지 않는다.** `isEmbedded="0"` 상태로 이름만 참조하고,
   실제 렌더링은 문서를 여는 PC의 설치 글꼴이 담당한다. 따라서 ttf/otf 파일은
   필요 없고, **정확한 이름 문자열**만 있으면 된다.
2. **이름은 공백까지 정확히.** `나눔손글씨 펜`(공백 O)과 `나눔바른펜`(공백 X)은
   다르다. `맑은 고딕`, `한컴 고딕`, `한컴 말랑말랑`은 공백이 들어간다.
3. **Windows 글꼴 폴더에 보이는 "보통 / 중간 / 굵게"는 이름의 일부가 아니다.**
   그건 굵기(Regular/Medium/Bold) 표시다. `face`에는 `함초롬돋움`만 적고,
   굵게는 `<hh:bold/>` 태그로 준다.
4. **기준은 Windows 글꼴 폴더가 아니라 한글 프로그램의 글꼴 목록이다.** 둘은 이름이
   다를 수 있다. 특히 HY 계열은 폴더에서 `HYGothic 중간`으로 보이지만 한글에서는
   `HY중고딕`이고, **`face`에는 한글 쪽 이름을 써야 한다.** 이 문서의 목록은
   한글 표기 기준으로 정리되어 있다.

## 기본 정책: 나눔 계열

**사용자의 기본 글꼴은 나눔 계열이다.** 별도 지정이 없으면 나눔 계열로 조판한다
(skeleton 기본값이 이미 그렇게 맞춰져 있다: 본문 나눔고딕, 표 숫자 나눔바른펜).
함초롬·HY·휴먼 계열은 사용자가 명시적으로 요청할 때만 쓴다.

## 본문·학습지용 추천 조합

| 용도 | 1순위 | 대안 |
|---|---|---|
| 개념 본문 | `함초롬바탕` | `나눔명조`, `바탕` |
| 고딕 본문·문제 지문 | `나눔고딕` | `함초롬돋움`, `맑은 고딕` |
| 제목·헤드라인 | `나눔스퀘어` | `휴먼둥근헤드라인`, `한컴 고딕` |
| 숫자·표 안 좁은 칸 | `나눔바른펜` (장평 96 권장) | `나눔바른고딕` |
| 강조·주의 문구 | `나눔고딕` + bold + `#FF0000` | `나눔스퀘어` bold |
| 영문·수식 라틴 | `Times New Roman` | `Cambria`, `Calibri` |
| 손글씨 느낌 | `나눔손글씨 펜` | `한컴 말랑말랑`, `휴먼편지체` |
| 코드·고정폭 | `D2Coding` | `Consolas` |

skeleton `header.xml`의 기본 9슬롯은 다음과 같다. **id를 바꾸지 말고 `--set-face`로
이름만 갈아끼우면 기존 charPr 참조가 전부 그대로 살아난다.**

```
id=0 나눔고딕   id=1 나눔바른고딕  id=2 나눔바른펜   id=3 나눔손글씨 펜
id=4 함초롬바탕  id=5 함초롬돋움    id=6 함초롬바탕   id=7 Calibri
id=8 Times New Roman
```

> 참고: id=4는 원래 `한컴바탕`이었으나 설치 목록에 없어 `함초롬바탕`으로 교체됨.
> 9개 슬롯 전부가 설치 확인된 글꼴이며, validate가 매번 이를 대조한다.

---

## 전체 설치 목록 (173개 항목)

### 한글 — 나눔 계열
```
나눔고딕            나눔고딕 에코        나눔고딕OTF         나눔고딕OTF 에코
나눔명조            나눔명조 에코        나눔명조 옛한글      나눔명조OTF
나눔명조OTF 에코     나눔명조OTF 옛한글    나눔바른고딕        나눔바른고딕 옛한글
나눔바른고딕OTF      나눔바른고딕OTF 옛한글  나눔바른펜         나눔바른펜OTF
나눔손글씨 붓        나눔손글씨 붓 OTF     나눔손글씨 펜       나눔손글씨 펜 OTF
나눔스퀘어          나눔스퀘어 네오       나눔스퀘어 네오 OTF   나눔스퀘어 네오 variable
나눔스퀘어_ac       나눔스퀘어OTF        나눔스퀘어OTF_ac    나눔스퀘어라운드
나눔휴먼OTF         나눔휴먼TTF
```
> OTF/TTF 판이 둘 다 있을 땐 **OTF 접미사 없는 쪽**(`나눔고딕`, `나눔스퀘어`)을 쓴다.
> 한글에서 더 안정적이고 자간 계산이 예측 가능하다.

### 한글 — 함초롬·한컴 계열 (한글 기본 탑재)
```
함초롬돋움          함초롬돋움 확장       함초롬바탕         함초롬바탕 확장
함초롬바탕 확장B     한컴 고딕           한컴 말랑말랑       한컴산뜻돋움
한컴 울주 반구대 암각화체   한컴 울주 천전리 각석체
한컴 훈민정음 가로쓰기     한컴 훈민정음 세로쓰기
```

### 한글 — 휴먼 계열 (제목·장식용)
```
휴먼둥근헤드라인     휴먼매직체          휴먼모음T          휴먼아미체
휴먼엑스포          휴먼옛체            휴먼편지체
```

### 한글 — Windows 기본
```
굴림    굴림체   궁서   궁서체   돋움   돋움체   바탕   바탕체
맑은 고딕        새굴림           Noto Sans KR      Noto Serif KR
```

### 한글 — HY 계열 (사용자가 잘 쓰지 않음. 요청 시에만)
한글 프로그램 화면에 뜨는 이름 그대로 확인된 목록. **끝의 B/M/L은 굵기가 아니라
이름의 일부이므로 반드시 붙여 쓴다** (`HY헤드라인M`이 정확, `HY헤드라인` 아님).
```
HY강B      HY강M      HY견고딕    HY견명조    HY궁서      HY궁서B
HY그래픽    HY그래픽M   HY나무B     HY나무L     HY나무M     HY동녘B
HY동녘M     HY목각파임B  HY목판L     HY바다L     HY바다M     HY백송B
HY산B      HY센스L     HY수평선B    HY수평선M   HY신명조     HY얕은샘물M
HY엽서L     HY엽서M     HY울릉도B    HY울릉도M   HY중고딕     HY크리스탈M
HY태백B     HY헤드라인M
```
> Windows 글꼴 폴더의 영문 이름(`HYGothic`, `HYSinMyeongJo`, `HYPost` 등)은
> **`face`에 쓰면 안 된다.** 한글이 인식하지 못해 다른 글꼴로 대체된다.
> 대략의 대응: HYGothic→`HY중고딕`, HYSinMyeongJo→`HY신명조`,
> HYHeadLine→`HY헤드라인M`, HYGraphic→`HY그래픽M`, HYGungSo→`HY궁서B`,
> HYPost→`HY엽서L`/`HY엽서M`, HYShortSamul→`HY얕은샘물M`, HYPMokGak→`HY목각파임B`.

### 수식 전용
```
HancomEQN     HyhwpEQ     Cambria Math     MT Extra     Symbol
```
> `<hp:equation>` 안의 글꼴은 보통 건드리지 않는다. 수식 글꼴을 바꿔달라는 요청이
> 오면 `HancomEQN`을 기본으로 쓴다.

### 영문 — 본문·제목용
```
Arial          Bahnschrift    Book Antiqua   Bookman Old Style   Calibri
Cambria        Candara        Century        Century Gothic      Comic Sans MS
Constantia     Corbel         Dubai          Ebrima              Franklin Gothic
Gabriola       Gadugi         Garamond       Georgia             Impact
Ink Free       Leelawadee     Leelawadee UI  Lucida Sans Unicode Microsoft Sans Serif
Monotype Corsiva   MS Reference Sans Serif   MS Sans Serif      MS Serif
Palatino Linotype  Roman       Sans Serif Collection   Script
Segoe Print    Segoe Script   Segoe UI       Segoe UI Historic   Segoe UI Variable
Sitka          Small Fonts    Sylfaen        Tahoma              Times New Roman
Trebuchet MS   Verdana
```

### 고정폭 / 코딩
```
Consolas    Courier New    Courier    D2Coding    D2Coding ligature
Fixedsys    Lucida Console    Modern    System    Terminal
```

### CJK·다국어 (한중일·기타 문자 대응용)
```
Javanese Text   Microsoft Himalaya   Microsoft JhengHei   Microsoft JhengHei UI
Microsoft New Tai Lue   Microsoft PhagsPa   Microsoft Tai Le   Microsoft Uighur
Microsoft YaHei   Microsoft YaHei UI   Microsoft Yi Baiti   MingLiU-ExtB
MingLiU_HKSCS-ExtB   MingLiU_MSCS-ExtB   Mongolian Baiti   MS Gothic
MS PGothic   MS UI Gothic   Myanmar Text   NewJumja   Nirmala Text
Nirmala UI   NSimSun   PMingLiU-ExtB   SimSun   SimSun-ExtB   SimSun-ExtG
Yu Gothic   Yu Gothic UI
```

### 기호·아이콘 (본문 금지 — 글자가 그림으로 바뀐다)
```
Bookshelf Symbol 7   Haan Wing2   MS Outlook   MS Reference Specialty
Segoe Fluent Icons   Segoe MDL2 Assets   Segoe UI Emoji   Segoe UI Symbol
Webdings   Wingdings   Wingdings 2   Wingdings 3
```
> ①②③ 같은 원문자는 이 글꼴들이 아니라 **유니코드 문자를 그대로** 넣는다.
> 본문 글꼴이 알아서 그린다.

---

## 글꼴 등록/교체 방법

header.xml을 손으로 편집하지 말 것. `fontCnt`, `itemCnt`, lang 그룹 7개를
동시에 맞춰야 해서 실수하면 문서가 깨진다. 반드시 스크립트를 쓴다.

```bash
# 현재 등록 상태 확인
python3 scripts/apply_style.py Contents/header.xml --list

# 기존 슬롯 이름만 교체 (charPr 참조 전부 유지됨 — 가장 안전)
python3 scripts/apply_style.py Contents/header.xml --set-face "5=나눔스퀘어"

# 새 글꼴 등록 (lang 그룹 7개에 동시 추가, fontCnt 자동 갱신)
python3 scripts/apply_style.py Contents/header.xml --add-font "휴먼둥근헤드라인"
```

> 이름에 공백이 있으면 셸에서 **반드시 따옴표로 감쌀 것**: `--set-face "4=한컴 고딕"`

lang 그룹마다 부여되는 id가 다를 수 있다(HANJA/OTHER 그룹은 글꼴 수가 하나 적어서
id가 1씩 밀린다). 스크립트가 그룹별 id를 각각 추적해 charPr에 정확히 꽂아주므로
직접 계산하지 말 것.
