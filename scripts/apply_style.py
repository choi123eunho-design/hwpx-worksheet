#!/usr/bin/env python3
"""header.xml의 글꼴(fontfaces)과 글자모양(charPr)을 안전하게 조작한다.

itemCnt/fontCnt 갱신, lang 그룹 7개 동시 처리, XML 유효성 검사까지 자동으로 한다.
header.xml을 손으로 편집하지 말고 반드시 이 스크립트를 쓸 것.

사용법:
  # 현재 등록된 글꼴 보기
  python3 apply_style.py header.xml --list

  # 기존 글꼴 슬롯의 이름만 갈아끼우기 (charPr 참조는 그대로 유지됨)
  python3 apply_style.py header.xml --set-face 5=나눔스퀘어 --set-face 6=함초롬바탕

  # 새 글꼴 등록 (7개 lang 그룹 전부에 추가)
  python3 apply_style.py header.xml --add-font "휴먼둥근헤드라인"

  # 새 글자모양 추가 → 부여된 charPr id를 stdout으로 알려준다
  python3 apply_style.py header.xml --add-charpr \
      '{"font":"나눔스퀘어","latin":"Times New Roman","pt":16,"bold":true,"color":"#1F3864"}'
"""
import argparse
import json
import re
import shutil
import sys
import xml.dom.minidom

LANGS = ['HANGUL', 'LATIN', 'HANJA', 'JAPANESE', 'OTHER', 'SYMBOL', 'USER']

TYPEINFO = ('<hh:typeInfo familyType="FCAT_GOTHIC" weight="6" proportion="4" contrast="0" '
            'strokeVariation="0" armStyle="0" letterform="0" midline="0" xHeight="0"/>')


def read(p):
    return open(p, encoding='utf-8').read()


def write(p, s):
    xml.dom.minidom.parseString(s.encode('utf-8'))  # 유효성 검사 먼저
    shutil.copy(p, p + '.bak')
    open(p, 'w', encoding='utf-8').write(s)


def font_map(s):
    """lang -> {face: id} / {id: face}"""
    by_lang = {}
    for m in re.finditer(r'<hh:fontface lang="(\w+)"[^>]*>(.*?)</hh:fontface>', s, re.S):
        lang, body = m.group(1), m.group(2)
        d = {}
        for f in re.finditer(r'<hh:font id="(\d+)" face="([^"]*)"', body):
            d[f.group(2)] = f.group(1)
        by_lang[lang] = d
    return by_lang


def cmd_list(s):
    for m in re.finditer(r'<hh:fontface lang="(\w+)" fontCnt="(\d+)"[^>]*>(.*?)</hh:fontface>', s, re.S):
        print('[%s] fontCnt=%s' % (m.group(1), m.group(2)))
        for f in re.finditer(r'<hh:font id="(\d+)" face="([^"]*)"', m.group(3)):
            print('   id=%-3s %s' % (f.group(1), f.group(2)))
        print()


def set_face(s, fid, face):
    """모든 lang 그룹에서 id=fid인 글꼴의 face를 교체."""
    n = 0
    out = []
    pos = 0
    for m in re.finditer(r'<hh:fontface lang="\w+"[^>]*>.*?</hh:fontface>', s, re.S):
        block = m.group(0)
        new, cnt = re.subn(r'(<hh:font id="%s" face=")[^"]*(")' % fid,
                           lambda mm: mm.group(1) + face + mm.group(2), block)
        n += cnt
        out.append(s[pos:m.start()])
        out.append(new)
        pos = m.end()
    out.append(s[pos:])
    if n == 0:
        sys.exit('글꼴 슬롯 id=%s 를 찾지 못했습니다.' % fid)
    print('  set-face id=%s → %s (%d개 lang 그룹 갱신)' % (fid, face, n))
    return ''.join(out)


def add_font(s, face):
    """모든 lang 그룹 끝에 글꼴 추가. lang별로 부여된 id dict 반환."""
    ids = {}
    out = []
    pos = 0
    for m in re.finditer(r'<hh:fontface lang="(\w+)" fontCnt="(\d+)"([^>]*)>(.*?)</hh:fontface>', s, re.S):
        lang, cnt, rest, body = m.group(1), int(m.group(2)), m.group(3), m.group(4)
        exist = re.search(r'<hh:font id="(\d+)" face="%s"' % re.escape(face), body)
        if exist:
            ids[lang] = exist.group(1)
            out.append(s[pos:m.end()])
            pos = m.end()
            continue
        new_id = max(int(x) for x in re.findall(r'<hh:font id="(\d+)"', body)) + 1
        ids[lang] = str(new_id)
        body += '<hh:font id="%d" face="%s" type="TTF" isEmbedded="0">%s</hh:font>' % (
            new_id, face, TYPEINFO)
        block = '<hh:fontface lang="%s" fontCnt="%d"%s>%s</hh:fontface>' % (
            lang, cnt + 1, rest, body)
        out.append(s[pos:m.start()])
        out.append(block)
        pos = m.end()
    out.append(s[pos:])
    print('  add-font "%s" → ids %s' % (face, ids))
    return ''.join(out), ids


def add_charpr(s, spec):
    """spec: {font, latin?, pt, bold?, italic?, underline?, color?, ratio?, spacing?}"""
    face = spec['font']
    latin_face = spec.get('latin', face)
    for f in (face, latin_face):
        fm = font_map(s)
        if f not in fm.get('HANGUL', {}):
            s, _ = add_font(s, f)

    fm = font_map(s)
    def fid(lang, want):
        d = fm.get(lang, {})
        return d.get(want) or d.get(face) or '0'

    hang = {l: fid(l, face) for l in LANGS}
    lat = fm.get('LATIN', {}).get(latin_face, hang['LATIN'])

    m = re.search(r'<hh:charProperties itemCnt="(\d+)"([^>]*)>(.*?)</hh:charProperties>', s, re.S)
    if not m:
        sys.exit('charProperties 블록을 찾지 못했습니다.')
    cnt, rest, body = int(m.group(1)), m.group(2), m.group(3)
    new_id = max(int(x) for x in re.findall(r'<hh:charPr id="(\d+)"', body)) + 1

    pt = int(round(float(spec['pt']) * 100))
    color = spec.get('color', '#000000')
    ratio = spec.get('ratio', 100)
    spacing = spec.get('spacing', 0)
    ul = spec.get('underline', False)

    def seven(val):
        return ' '.join('%s="%s"' % (k.lower(), val) for k in
                        ['hangul', 'latin', 'hanja', 'japanese', 'other', 'symbol', 'user'])

    charpr = (
        '<hh:charPr id="%d" height="%d" textColor="%s" shadeColor="none" useFontSpace="0" '
        'useKerning="0" symMark="NONE" borderFillIDRef="%s">'
        '<hh:fontRef hangul="%s" latin="%s" hanja="%s" japanese="%s" other="%s" symbol="%s" user="%s"/>'
        '<hh:ratio %s/><hh:spacing %s/><hh:relSz %s/><hh:offset %s/>'
        '%s%s'
        '<hh:underline type="%s" shape="SOLID" color="%s"/>'
        '<hh:strikeout shape="NONE" color="#000000"/><hh:outline type="NONE"/>'
        '<hh:shadow type="NONE" color="#C0C0C0" offsetX="10" offsetY="10"/>'
        '</hh:charPr>' % (
            new_id, pt, color, spec.get('borderFill', '2'),
            hang['HANGUL'], lat, hang['HANJA'], hang['JAPANESE'],
            hang['OTHER'], hang['SYMBOL'], hang['USER'],
            seven(ratio), seven(spacing), seven(100), seven(0),
            '<hh:bold/>' if spec.get('bold') else '',
            '<hh:italic/>' if spec.get('italic') else '',
            'SOLID' if ul else 'NONE', color,
        ))

    block = '<hh:charProperties itemCnt="%d"%s>%s%s</hh:charProperties>' % (
        cnt + 1, rest, body, charpr)
    s = s[:m.start()] + block + s[m.end():]
    print('  add-charpr → charPrIDRef="%d"  (%s %spt%s%s)' % (
        new_id, face, spec['pt'], ' bold' if spec.get('bold') else '',
        ' ' + color if color != '#000000' else ''))
    return s


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('header')
    ap.add_argument('--list', action='store_true')
    ap.add_argument('--set-face', action='append', default=[], metavar='ID=이름')
    ap.add_argument('--add-font', action='append', default=[])
    ap.add_argument('--add-charpr', action='append', default=[], metavar='JSON')
    args = ap.parse_args()

    s = read(args.header)
    if args.list:
        cmd_list(s)
        return

    changed = False
    for pair in args.set_face:
        fid, face = pair.split('=', 1)
        s = set_face(s, fid.strip(), face.strip())
        changed = True
    for face in args.add_font:
        s, _ = add_font(s, face)
        changed = True
    for js in args.add_charpr:
        s = add_charpr(s, json.loads(js))
        changed = True

    if changed:
        write(args.header, s)
        print('저장 완료 (백업: %s.bak)' % args.header)
    else:
        print('변경 사항 없음. --list / --set-face / --add-font / --add-charpr 중 하나를 쓰세요.')


if __name__ == '__main__':
    main()
