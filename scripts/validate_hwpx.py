#!/usr/bin/env python3
"""HWPX 전수 검증. 사용법: python3 validate_hwpx.py <파일.hwpx>
전부 통과해야 사용자에게 전달 가능. 하나라도 FAIL이면 원인 수정 후 재검증.
"""
import sys, re, os, zipfile
import xml.dom.minidom as M

def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    path = sys.argv[1]
    z = zipfile.ZipFile(path)
    names = z.namelist()
    ok = True

    def check(label, cond, detail=''):
        nonlocal ok
        print(f"{'PASS' if cond else 'FAIL'}  {label}  {detail}")
        ok = ok and bool(cond)

    check('zip 무결성', z.testzip() is None)
    check('mimetype 첫 항목', names[0] == 'mimetype')
    check('mimetype 무압축', z.getinfo('mimetype').compress_type == 0)
    check('mimetype 내용', z.read('mimetype') == b'application/hwp+zip')

    # XML 유효성
    bad = []
    for n in names:
        if n.endswith(('.xml', '.hpf', '.rdf')):
            try:
                M.parseString(z.read(n))
            except Exception as e:
                bad.append(f'{n}: {e}')
    check('XML 유효성', not bad, '; '.join(bad[:3]))

    # 섹션 개수 일치 (secCnt / 파일 / manifest / spine / rdf)
    h = z.read('Contents/header.xml').decode()
    m = re.search(r'secCnt="(\d+)"', h)
    seccnt = int(m.group(1)) if m else -1
    secfiles = sorted(int(x) for n in names
                      for x in re.findall(r'^Contents/section(\d+)\.xml$', n))
    hpf = z.read('Contents/content.hpf').decode()
    man = set(re.findall(r'id="(section\d+)"', hpf))
    spine = re.findall(r'idref="(section\d+)"', hpf)
    check('secCnt == 섹션 파일 수', seccnt == len(secfiles),
          f'secCnt={seccnt}, files={len(secfiles)}')
    check('섹션 번호 연속(0..N-1)', secfiles == list(range(len(secfiles))))
    check('manifest 섹션 수 일치', len(man) == len(secfiles))
    check('spine 섹션 수 일치', len(spine) == len(secfiles))
    check('spine 순서 = 섹션 순서',
          spine == [f'section{i}' for i in range(len(secfiles))])

    # dangling 참조 (hpf / rdf → 실제 파일)
    missing = []
    for meta in ['Contents/content.hpf', 'META-INF/container.rdf']:
        d = z.read(meta).decode()
        for s in set(re.findall(r'Contents/section(\d+)\.xml', d)):
            if f'Contents/section{s}.xml' not in names:
                missing.append(f'{meta}:section{s}')
        for i in set(re.findall(r'BinData/image(\d+)\.jpe?g', d)):
            if not any(n.startswith(f'BinData/image{i}.') for n in names):
                missing.append(f'{meta}:image{i}')
    check('dangling 참조 없음', not missing, '; '.join(missing[:5]))

    # 섹션이 참조하는 이미지가 manifest에 등록되어 있는지
    declared = set(re.findall(r'id="(image\d+)"', hpf))
    used = set()
    for i in secfiles:
        used |= set(re.findall(r'binaryItemIDRef="(image\d+)"',
                               z.read(f'Contents/section{i}.xml').decode()))
    check('미등록 이미지 참조 없음', used <= declared,
          f'미등록: {sorted(used - declared)[:5]}')

    # 표 무결성: rowCnt/colCnt vs 실제 셀 수
    tblbad = []
    for i in secfiles:
        s = z.read(f'Contents/section{i}.xml').decode()
        for t in re.findall(r'<hp:tbl.*?</hp:tbl>', s, re.S):
            r = int(re.search(r'rowCnt="(\d+)"', t).group(1))
            c = int(re.search(r'colCnt="(\d+)"', t).group(1))
            cells = len(re.findall(r'<hp:tc\b', t))
            rows = len(re.findall(r'<hp:tr\b', t))
            if rows != r or cells != r * c:
                tblbad.append(f'sec{i}: {r}x{c} vs tr={rows}, tc={cells}')
    check('표 rowCnt/colCnt 일치', not tblbad, '; '.join(tblbad[:3]))

    # 글꼴/서식 무결성
    # 1) fontCnt·itemCnt가 실제 개수와 맞는지
    cntbad = []
    for fm in re.finditer(r'<hh:fontface lang="(\w+)" fontCnt="(\d+)"[^>]*>(.*?)</hh:fontface>',
                          h, re.S):
        real = len(re.findall(r'<hh:font id=', fm.group(3)))
        if int(fm.group(2)) != real:
            cntbad.append(f'{fm.group(1)}: fontCnt={fm.group(2)} vs {real}')
    for tag in ('charProperties', 'paraProperties'):
        mm = re.search(r'<hh:%s itemCnt="(\d+)"[^>]*>(.*?)</hh:%s>' % (tag, tag), h, re.S)
        if mm:
            child = 'charPr' if tag == 'charProperties' else 'paraPr'
            real = len(re.findall(r'<hh:%s id=' % child, mm.group(2)))
            if int(mm.group(1)) != real:
                cntbad.append(f'{tag}: itemCnt={mm.group(1)} vs {real}')
    check('fontCnt/itemCnt 실제 개수 일치', not cntbad, '; '.join(cntbad[:3]))

    # 2) 본문이 참조하는 charPr/paraPr가 header에 존재하는지
    charids = set(re.findall(r'<hh:charPr id="(\d+)"', h))
    paraids = set(re.findall(r'<hh:paraPr id="(\d+)"', h))
    ucha, upar = set(), set()
    for i in secfiles:
        s = z.read(f'Contents/section{i}.xml').decode()
        ucha |= set(re.findall(r'charPrIDRef="(\d+)"', s))
        upar |= set(re.findall(r'paraPrIDRef="(\d+)"', s))
    check('charPrIDRef 전부 정의됨', ucha <= charids, f'미정의: {sorted(ucha - charids)[:5]}')
    check('paraPrIDRef 전부 정의됨', upar <= paraids, f'미정의: {sorted(upar - paraids)[:5]}')

    # 3) 등록 글꼴이 사용자 PC 설치 목록에 있는지 (없으면 한글이 임의 대체 → 레이아웃 붕괴)
    flist = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                         '..', 'assets', 'installed-fonts.txt')
    if os.path.exists(flist):
        installed = {l.strip() for l in open(flist, encoding='utf-8')
                     if l.strip() and not l.startswith('#')}
        used_faces = set(re.findall(r'<hh:font id="\d+" face="([^"]*)"', h))
        unknown = sorted(f for f in used_faces if f not in installed)
        check('글꼴이 설치 목록에 존재', not unknown, f'미설치 의심: {unknown[:5]}')
    else:
        print('SKIP  글꼴 설치 목록 대조 (assets/installed-fonts.txt 없음)')

    print()
    print('전체 결과:', '통과 — 납품 가능' if ok else '실패 — 수정 필요')
    sys.exit(0 if ok else 1)

if __name__ == '__main__':
    main()
