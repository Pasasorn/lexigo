# -*- coding: utf-8 -*-
"""
เปลี่ยน URL ของ Apps Script ทุกจุดในเว็บ (462 ไฟล์) ให้ชี้ไป deployment ใหม่

ใช้ตอนย้ายไปใช้ Google Sheet ใหม่ เพราะ Sheet ใหม่ = Apps Script ใหม่ = URL ใหม่

วิธีใช้
  ดูก่อน:  py _docs/set_api_url.py --show
  เปลี่ยน: py _docs/set_api_url.py "https://script.google.com/macros/s/XXXX/exec"
  ย้อนกลับ: py _docs/set_api_url.py --undo
"""
import os, re, sys, glob, json, shutil, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BK   = os.path.join(ROOT, '_docs', '.api_url_backup.json')
PAT  = re.compile(r'https://script\.google\.com/macros/s/[A-Za-z0-9_-]+/exec')


def targets():
    out = []
    for ext in ('*.html', '*.js'):
        out += glob.glob(os.path.join(ROOT, ext))
        out += glob.glob(os.path.join(ROOT, '*', ext))
        out += glob.glob(os.path.join(ROOT, '*', '*', ext))
    return sorted(set(out))


def show():
    c = collections.Counter()
    files = 0
    for p in targets():
        try:
            h = open(p, encoding='utf-8').read()
        except Exception:
            continue
        found = PAT.findall(h)
        if found:
            files += 1
            c.update(found)
    print('ไฟล์ที่มี URL : %d' % files)
    print('จำนวนจุดรวม  : %d' % sum(c.values()))
    print('\nURL ที่ใช้อยู่:')
    for u, n in c.most_common():
        print('  %4d ครั้ง  %s' % (n, u))
    return c


def apply(new):
    if not PAT.fullmatch(new):
        sys.exit('รูปแบบ URL ไม่ถูกต้อง\nต้องเป็น  https://script.google.com/macros/s/.../exec')

    backup, n_files, n_hits = {}, 0, 0
    for p in targets():
        try:
            h = open(p, encoding='utf-8').read()
        except Exception:
            continue
        hits = PAT.findall(h)
        if not hits:
            continue
        backup[os.path.relpath(p, ROOT)] = hits[0]
        h2 = PAT.sub(new, h)
        if h2 != h:
            open(p, 'w', encoding='utf-8').write(h2)
            n_files += 1
            n_hits += len(hits)

    json.dump(backup, open(BK, 'w'), ensure_ascii=False, indent=1)
    print('เปลี่ยนแล้ว %d จุด ใน %d ไฟล์' % (n_hits, n_files))
    print('สำรอง URL เดิมไว้ที่ %s (ใช้ --undo ย้อนได้)' % os.path.relpath(BK, ROOT))

    # ตรวจซ้ำ
    left = collections.Counter()
    for p in targets():
        try:
            h = open(p, encoding='utf-8').read()
        except Exception:
            continue
        for u in PAT.findall(h):
            if u != new:
                left[u] += 1
    print('\nเหลือ URL เก่าค้าง: %s' % (dict(left) if left else 'ไม่มี ✅'))


def undo():
    if not os.path.exists(BK):
        sys.exit('ไม่มีไฟล์สำรอง')
    bk = json.load(open(BK))
    n = 0
    for rel, old in bk.items():
        p = os.path.join(ROOT, rel)
        if not os.path.exists(p):
            continue
        h = open(p, encoding='utf-8').read()
        h2 = PAT.sub(old, h)
        if h2 != h:
            open(p, 'w', encoding='utf-8').write(h2)
            n += 1
    print('ย้อนกลับ %d ไฟล์' % n)


if __name__ == '__main__':
    a = sys.argv[1:]
    if not a or a[0] == '--show':
        show()
    elif a[0] == '--undo':
        undo()
    else:
        apply(a[0].strip())
