#!/usr/bin/env python3
"""HWPX 패키징: mimetype을 첫 항목·무압축(STORED)으로 넣는 규격을 강제한다.
사용법: python3 package_hwpx.py <소스폴더> <출력.hwpx>
소스폴더에는 mimetype, version.xml, settings.xml, Contents/, META-INF/, BinData/ 가 있어야 함.
"""
import sys, os, zipfile

def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    src, out = sys.argv[1], sys.argv[2]
    mt = os.path.join(src, 'mimetype')
    if not os.path.exists(mt):
        sys.exit('오류: mimetype 파일이 없습니다.')
    if os.path.exists(out):
        os.remove(out)
    z = zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED)
    z.write(mt, 'mimetype', compress_type=zipfile.ZIP_STORED)
    for root, dirs, files in os.walk(src):
        dirs.sort()
        for fn in sorted(files):
            full = os.path.join(root, fn)
            arc = os.path.relpath(full, src)
            if arc == 'mimetype':
                continue
            # 스킬 예제 파일이 실수로 섞여 들어가는 것 방지
            if 'example' in arc:
                print(f'skip (example): {arc}')
                continue
            z.write(full, arc)
    z.close()
    print(f'OK: {out} ({os.path.getsize(out)/1e6:.1f} MB)')

if __name__ == '__main__':
    main()
