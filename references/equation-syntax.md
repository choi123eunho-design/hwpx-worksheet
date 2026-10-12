# HWP 수식 스크립트 문법 (hp:script 내용)

한글 수식은 LaTeX가 아니라 자체 스크립트다. 아래는 실제 문서에서 사용해 검증된 패턴.

## 기본
| 의미 | 스크립트 | 예 |
|---|---|---|
| 분수 | `{a} over {b}` | `{1} over {16}` |
| 위/아래 첨자 | `x^{2}`, `a_{1}` | `sigma ^{2}` |
| 근호 | `sqrt {2}` | `{sqrt {3}} over {2}` |
| 절댓값 | `vert x-1 vert` | |
| 부등호 | `le`, `ge`, `<`, `>` | `0 le x le 2` |
| 무한대/±/× | `inf`, `+-`, `times` | `- inf < x < inf` |
| 그리스 문자 | `alpha beta sigma pi` | |
| 로만체(직립) | `rm ...` | `rm P(0 le Z le z)` |
| 자간 공백 | `~` (넓음), `` ` `` (좁음) | `rm N(m,~ sigma ^{2})` |
| 점 3개 | `cdots` | `e=2.7182 cdots` |

## 자주 쓰는 조합 (확률과 통계)
```
rm P( {1} over {2} le X le {3} over {2} )
rm N(np,~npq)
Z= {X-m} over { sigma }
rm P(a le X le b)=P( {a-m} over { sigma } le Z le {b-m} over { sigma } )
f(x)= {1} over { sqrt {2 pi } sigma } e ^{- {(x-m)^{2}} over {2 sigma ^{2}}}
sum _{n=1} ^{7} rm P(X le n)
```

## 조각 함수 (cases)
```
f(x)=cases{{vert x-1 vert}``(0 le x le 2) # {0}``(x<0,~x>2)}
```
`#` 가 줄 구분, `` ` `` 두 개로 조건 앞 간격.

## 주의
- 수식 요소는 문장 중간에 넣을 때 `treatAsChar="1"` (xml-templates.md의 스니펫 사용).
- 독립 수식 줄(가운데 정렬 식)은 본문 문단 하나에 공백 들여쓰기 + 수식 run 하나로 구성.
- 스크립트 안의 `<`, `>`, `&`는 XML 이스케이프 필요: `&lt;` `&gt;` `&amp;`.
- 한글 텍스트는 수식 밖 `<hp:t>`에 두고, 기호·변수만 수식으로 (석차/첨삭 편의).
