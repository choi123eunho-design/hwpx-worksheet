#!/usr/bin/env python3
"""HWPX 서식 인벤토리 추출기.

기존 .hwpx 파일(또는 압축 해제된 소스 폴더)에서 실제로 쓰인 글꼴/글자모양/문단모양을
사람이 읽을 수 있는 표로 뽑아낸다. "이 학습지랑 똑같은 서식으로 만들어줘" 요청이
들어왔을 때 가장 먼저 실행할 것.

사용법:
    python3 inspect_style.py <파일.hwpx | 소스폴더>
    python3 inspect_style.py <파일.hwpx> --used      # 본문에서 실제 쓰인 것만
    python3 inspect_style.py <파일.hwpx> --json      # 기계 판독용
"""
import argparse
import json
import os
import re
import sys
import zipfile
from collections import Counter, OrderedDict

HWPUNIT_MM = 283.465  # 1mm = 283.465 HWPUNIT


def load(src):
    """hwpx 또는 폴더에서 {경로: 텍스트} 반환."""
    out = {}
    if os.path.isdir(src):
        for root, _, files in os.walk(src):
            for f in files:
                if f.endswith(('.xml', '.hpf')):
                    p = os.path.join(root, f)
                    rel = os.path.relpath(p, src).replace(os.sep, '/')
                    out[rel] = open(p, encoding='utf-8').read()
    else:
        with zipfile.ZipFile(src) as z:
            for n in z.namelist():
                if n.endswith(('.xml', '.hpf')):
                    try:
                        out[n] = z.read(n).decode('utf-8')
                    except UnicodeDecodeError:
                        pass
    return out


def attrs(tag):
    return dict(re.findall(r'(\w+)="([^"]*)"', tag))


def parse_fonts(header):
    """lang -> {id: face}"""
    fonts = OrderedDict()
    for fm in re.finditer(r'<hh:fontface lang="(\w+)"[^>]*>(.*?)</hh:fontface>', header, re.S):
        lang, body = fm.group(1), fm.group(2)
        d = OrderedDict()
        for f in re.finditer(r'<hh:font\s([^>]*?)/?>', body):
            a = attrs(f.group(1))
            d[a.get('id')] = a.get('face', '?')
        fonts[lang] = d
    return fonts


def parse_charpr(header, fonts):
    hangul = fonts.get('HANGUL', {})
    latin = fonts.get('LATIN', {})
    res = OrderedDict()
    for m in re.finditer(r'<hh:charPr\s([^>]*?)>(.*?)</hh:charPr>', header, re.S):
        a = attrs(m.group(1))
        body = m.group(2)
        cid = a.get('id')
        fr = re.search(r'<hh:fontRef\s([^>]*?)/>', body)
        fa = attrs(fr.group(1)) if fr else {}
        ra = attrs(re.search(r'<hh:ratio\s([^>]*?)/>', body).group(1)) if '<hh:ratio' in body else {}
        sp = attrs(re.search(r'<hh:spacing\s([^>]*?)/>', body).group(1)) if '<hh:spacing' in body else {}
        ul = attrs(re.search(r'<hh:underline\s([^>]*?)/>', body).group(1)) if '<hh:underline' in body else {}
        res[cid] = {
            'id': cid,
            'pt': int(a.get('height', 0)) / 100,
            'color': a.get('textColor', '#000000'),
            'shade': a.get('shadeColor', 'none'),
            'hangul_font': hangul.get(fa.get('hangul'), '?'),
            'latin_font': latin.get(fa.get('latin'), '?'),
            'font_id': fa.get('hangul'),
            'bold': '<hh:bold' in body,
            'italic': '<hh:italic' in body,
            'underline': ul.get('type', 'NONE') != 'NONE',
            'ratio': int(ra.get('hangul', 100)),      # 장평 %
            'spacing': int(sp.get('hangul', 0)),      # 자간 %
        }
    return res


def parse_parapr(header):
    res = OrderedDict()
    for m in re.finditer(r'<hh:paraPr\s([^>]*?)>(.*?)</hh:paraPr>', header, re.S):
        a = attrs(m.group(1))
        body = m.group(2)
        al = attrs(re.search(r'<hh:align\s([^>]*?)/>', body).group(1)) if '<hh:align' in body else {}
        mg = re.search(r'<hh:margin>(.*?)</hh:margin>', body, re.S)
        marg = {}
        if mg:
            for k in ('left', 'right', 'prev', 'next', 'intent'):
                mm = re.search(r'<hc:%s\s([^>]*?)/>' % k, mg.group(1))
                if mm:
                    va = attrs(mm.group(1))
                    marg[k] = int(va.get('value', 0))
        ls = attrs(re.search(r'<hh:lineSpacing\s([^>]*?)/>', body).group(1)) if '<hh:lineSpacing' in body else {}
        res[a.get('id')] = {
            'id': a.get('id'),
            'align': al.get('horizontal', 'LEFT'),
            'left_mm': round(marg.get('left', 0) / HWPUNIT_MM, 2),
            'right_mm': round(marg.get('right', 0) / HWPUNIT_MM, 2),
            'indent_mm': round(marg.get('intent', 0) / HWPUNIT_MM, 2),
            'prev_mm': round(marg.get('prev', 0) / HWPUNIT_MM, 2),
            'next_mm': round(marg.get('next', 0) / HWPUNIT_MM, 2),
            'linespacing': '%s %s' % (ls.get('value', '?'), ls.get('type', '')),
        }
    return res


def scan_sections(docs):
    """본문에서 charPr/paraPr 사용 빈도 + 샘플 텍스트 수집."""
    char_use, para_use = Counter(), Counter()
    samples = {}
    for name, txt in docs.items():
        if 'section' not in name.lower():
            continue
        for m in re.finditer(r'<hp:p\s([^>]*?)>(.*?)</hp:p>', txt, re.S):
            pa = attrs(m.group(1))
            body = m.group(2)
            if pa.get('paraPrIDRef'):
                para_use[pa['paraPrIDRef']] += 1
            for rm in re.finditer(r'<hp:run\s([^>]*?)>(.*?)</hp:run>', body, re.S):
                ra = attrs(rm.group(1))
                cid = ra.get('charPrIDRef')
                if not cid:
                    continue
                char_use[cid] += 1
                tm = re.search(r'<hp:t>([^<]{2,60})</hp:t>', rm.group(2))
                if tm and cid not in samples:
                    samples[cid] = tm.group(1).strip()
    return char_use, para_use, samples


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('src')
    ap.add_argument('--used', action='store_true', help='본문에서 실제 쓰인 항목만 출력')
    ap.add_argument('--json', action='store_true')
    args = ap.parse_args()

    docs = load(args.src)
    hk = next((k for k in docs if k.endswith('header.xml')), None)
    if not hk:
        sys.exit('header.xml을 찾을 수 없습니다: %s' % args.src)
    header = docs[hk]

    fonts = parse_fonts(header)
    chars = parse_charpr(header, fonts)
    paras = parse_parapr(header)
    cuse, puse, samples = scan_sections(docs)

    if args.json:
        print(json.dumps({'fonts': fonts, 'charPr': chars, 'paraPr': paras,
                          'charUse': cuse, 'paraUse': puse, 'samples': samples},
                         ensure_ascii=False, indent=2))
        return

    print('=' * 78)
    print('글꼴 (fontfaces) — HANGUL 그룹 기준')
    print('=' * 78)
    for fid, face in fonts.get('HANGUL', {}).items():
        lat = fonts.get('LATIN', {}).get(fid, '')
        print('  id=%-3s %-22s (LATIN: %s)' % (fid, face, lat))

    print()
    print('=' * 78)
    print('글자 모양 (charPr)   ※ 사용횟수 0은 정의만 되어 있고 안 쓰인 것')
    print('=' * 78)
    print('%-4s %-6s %-18s %-9s %-6s %-5s %-5s %s' %
          ('id', 'pt', '글꼴', '색', '굵게', '장평', '자간', '사용/샘플'))
    print('-' * 78)
    for cid, c in chars.items():
        n = cuse.get(cid, 0)
        if args.used and n == 0:
            continue
        deco = 'B' if c['bold'] else ' '
        deco += 'I' if c['italic'] else ' '
        deco += 'U' if c['underline'] else ' '
        s = samples.get(cid, '')
        if len(s) > 20:
            s = s[:20] + '…'
        print('%-4s %-6s %-18s %-9s %-6s %-5s %-5s %sx %s' %
              (cid, c['pt'], c['hangul_font'][:18], c['color'], deco,
               c['ratio'], c['spacing'], n, s))

    print()
    print('=' * 78)
    print('문단 모양 (paraPr)')
    print('=' * 78)
    print('%-4s %-10s %-8s %-8s %-8s %-10s %s' %
          ('id', '정렬', '왼여백mm', '들여쓰기', '문단뒤mm', '줄간격', '사용'))
    print('-' * 78)
    for pid, p in paras.items():
        n = puse.get(pid, 0)
        if args.used and n == 0:
            continue
        print('%-4s %-10s %-8s %-8s %-8s %-10s %sx' %
              (pid, p['align'], p['left_mm'], p['indent_mm'], p['next_mm'],
               p['linespacing'], n))

    print()
    print('요약: 글꼴 %d개 / charPr %d개(사용 %d) / paraPr %d개(사용 %d)' %
          (len(fonts.get('HANGUL', {})), len(chars), len(cuse), len(paras), len(puse)))


if __name__ == '__main__':
    main()
