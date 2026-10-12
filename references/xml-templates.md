# HWPX XML 템플릿 모음 (검증 완료본에서 추출)

이 스니펫들은 실제로 한글에서 정상 동작한 문서에서 그대로 가져온 것이다.
속성값을 임의로 빼거나 추가하지 말고, 지시된 부분만 바꿔서 사용한다.

## 1. 섹션 파일 뼈대

각 section{N}.xml 은 아래 루트로 시작한다 (첫 문단 안에 secPr이 들어가는 구조는
example 섹션 파일에서 확인). 새 섹션을 만들 때는 skeleton의 example 섹션을 복사한 뒤
문단들만 교체하는 방식이 가장 안전하다.

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes" ?><hs:sec xmlns:ha="http://www.hancom.co.kr/hwpml/2011/app" xmlns:hp="http://www.hancom.co.kr/hwpml/2011/paragraph" xmlns:hp10="http://www.hancom.co.kr/hwpml/2016/paragraph" xmlns:hs="http://www.hancom.co.kr/hwpml/2011/section" xmlns:hc="http://www.hancom.co.kr/hwpml/2011/core" xmlns:hh="http://www.hancom.co.kr/hwpml/2011/head" xmlns:hhs="http://www.hancom.co.kr/hwpml/2011/history" xmlns:hm="http://www.hancom.co.kr/hwpml/2011/master-page" xmlns:hpf="http://www.hancom.co.kr/schema/2011/hpf" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:opf="http://www.idpf.org/2007/opf/" xmlns:ooxmlchart="http://www.hancom.co.kr/hwpml/2016/ooxmlchart" xmlns:hwpunitchar="http://www.hancom.co.kr/hwpml/2016/HwpUnitChar" xmlns:epub="http://www.idpf.org/2007/ops" xmlns:config="urn:oasis:names:tc:opendocument:xmlns:config:1.0">
```
(전체는 assets/skeleton/Contents/section_problem_example.xml 참조)

## 2. 문단 (paragraph)

빈 문단 (간격용):
```xml
<hp:p id="0" paraPrIDRef="24" styleIDRef="0" pageBreak="0" columnBreak="0" merged="0"><hp:run charPrIDRef="8"/></hp:p>
```
- 문제 페이지 간격: paraPrIDRef="24" (100%), 개념 페이지 간격: "21" (100%)
- id는 중복되어도 한글이 저장 시 재부여하므로 "0" 고정 사용 가능.

본문 문단 (텍스트+수식 혼합):
```xml
<hp:p id="0" paraPrIDRef="25" styleIDRef="0" pageBreak="0" columnBreak="0" merged="0">
  <hp:run charPrIDRef="14"><hp:t>확률변수 </hp:t></hp:run>
  <hp:run charPrIDRef="14">[수식 요소]</hp:run>
  <hp:run charPrIDRef="14"><hp:t>가 평균이 ...</hp:t></hp:run>
</hp:p>
```
- 개념 본문: paraPr 22 또는 23 / 문제 본문: paraPr 25
- XML 이스케이프 필수: & → &amp;, < → &lt;, > → &gt;

## 3. 수식 (hp:equation, treatAsChar=1로 문장 안에 흐름)

```xml
<hp:equation id="0" zOrder="1" numberingType="EQUATION" textWrap="TOP_AND_BOTTOM" textFlow="BOTH_SIDES" lock="0" dropcapstyle="None" version="Equation Version 60" baseLine="60" textColor="#000000" baseUnit="850" lineMode="CHAR" font="HancomEQN"><hp:sz width="651" widthRelTo="ABSOLUTE" height="850" heightRelTo="ABSOLUTE" protect="0"/><hp:pos treatAsChar="1" affectLSpacing="0" flowWithText="1" allowOverlap="0" holdAnchorAndSO="0" vertRelTo="PARA" horzRelTo="PARA" vertAlign="TOP" horzAlign="LEFT" vertOffset="0" horzOffset="0"/><hp:outMargin left="56" right="56" top="0" bottom="0"/><hp:shapeComment>수식입니다.</hp:shapeComment><hp:script>z</hp:script></hp:equation>
```
- `<hp:script>` 안에 HWP 수식 스크립트를 넣는다 (문법: equation-syntax.md).
- sz width/height는 대략값이어도 한글이 열 때 재계산하지만,
  height는 baseUnit(=850, 8.5pt)과 같게, width는 글자당 ~430 hwpunit로 어림.

## 4. 페이지 전면 배경 이미지 (디자인 레이어)

섹션의 **첫 문단** 안 run에 넣는다. textWrap="BEHIND_TEXT", 종이 기준 배치:
```xml
<hp:pic id="1134640015" zOrder="25" numberingType="NONE" textWrap="BEHIND_TEXT" textFlow="BOTH_SIDES" lock="0" dropcapstyle="None" href="" groupLevel="0" instid="60900015" reverse="0"><hp:offset x="0" y="0"/><hp:orgSz width="59476" height="84008"/><hp:curSz width="0" height="0"/><hp:flip horizontal="0" vertical="0"/><hp:rotationInfo angle="0" centerX="29738" centerY="42004" rotateimage="1"/><hp:renderingInfo><hc:transMatrix e1="1" e2="0" e3="0" e4="0" e5="1" e6="0"/><hc:scaMatrix e1="1" e2="0" e3="0" e4="0" e5="1" e6="0"/><hc:rotMatrix e1="1" e2="0" e3="0" e4="0" e5="1" e6="0"/></hp:renderingInfo><hc:img binaryItemIDRef="image15" bright="0" contrast="0" effect="REAL_PIC" alpha="0"/><hp:imgRect><hc:pt0 x="0" y="0"/><hc:pt1 x="59476" y="0"/><hc:pt2 x="59476" y="84008"/><hc:pt3 x="0" y="84008"/></hp:imgRect><hp:imgClip left="0" right="93075" top="0" bottom="131625"/><hp:inMargin left="0" right="0" top="0" bottom="0"/><hp:imgDim dimwidth="93075" dimheight="131625"/><hp:effects/><hp:sz width="59476" widthRelTo="ABSOLUTE" height="84008" heightRelTo="ABSOLUTE" protect="0"/><hp:pos treatAsChar="0" affectLSpacing="0" flowWithText="1" allowOverlap="1" holdAnchorAndSO="0" vertRelTo="PAPER" horzRelTo="PAPER" vertAlign="TOP" horzAlign="LEFT" vertOffset="86" horzOffset="23"/><hp:outMargin left="0" right="0" top="0" bottom="0"/><hp:shapeComment>그림입니다.
원본 그림의 이름: image15.jpeg
원본 그림의 크기: 가로 1241pixel, 세로 1755pixel</hp:shapeComment></hp:pic>
```
- binaryItemIDRef="image{N}" 만 페이지에 맞게 교체.
- orgSz/pt2/pt3 의 59476×84008 은 A4 전체 (hwpunit=1/7200 inch, 1mm≈283.46).
- vertOffset/horzOffset은 86/23 수준의 미세값 유지.

## 5. 표 (hp:tbl)

전체 구조는 section_problem_example.xml 의 <hp:tbl> 을 복사해 변형한다. 핵심:
- `rowCnt`/`colCnt` 와 실제 `<hp:tr>`/`<hp:tc>` 수 일치.
- 각 셀: `<hp:tc ...><hp:subList ...><hp:p paraPrIDRef="27">…</hp:p></hp:subList>
  <hp:cellAddr colAddr r rowAddr/><hp:cellSpan/><hp:cellSz width height/><hp:cellMargin/></hp:tc>`
- **열 폭 = 해당 열 모든 셀의 cellSz width 동일**, 표의 `<hp:sz width>` = 열 폭 합.
- z-표 권장 폭: z열 4406 (15.5mm), 값열 9593 (33.8mm), 행 높이 2200.
- 셀 문단은 paraPr 27 (가운데 정렬, 왼쪽 여백 0). **여백 있는 paraPr을 쓰면
  좁은 셀에서 줄바꿈 발생** — 이 스킬의 skeleton header.xml은 이미 0으로 고정됨.
- 표 anchor: 본문 문단 안에 run으로 넣고 pos treatAsChar="1".

## 6. 등록 정보 4곳 (섹션/이미지 개수 변경 시 필수 동기화)

1. header.xml: `<hh:beginNum ...>` 근처의 `secCnt="N"`
2. content.hpf manifest: `<opf:item id="sectionK" href="Contents/sectionK.xml" .../>`
   와 이미지 `<opf:item id="imageK" href="BinData/imageK.jpeg" media-type="image/jpeg"/>`
3. content.hpf spine: `<opf:itemref idref="sectionK" .../>` (순서 = 페이지 순서)
4. META-INF/container.rdf: 섹션·이미지 파일 경로 목록

skeleton의 content.hpf / container.rdf 에서 기존 항목 형식을 그대로 복제해 늘린다.
