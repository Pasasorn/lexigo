# -*- coding: utf-8 -*-
"""
สแกนหาความลับที่หลุดอยู่ในโปรเจกต์ — รันก่อน push ทุกครั้ง

รัน:  py _docs/scan_secrets.py
      py _docs/scan_secrets.py --strict   (เจออะไรก็ตอบ exit code 1 ใช้ใน CI ได้)

ทุกอย่างในโฟลเดอร์นี้ถูก deploy ขึ้น Cloudflare รวม _docs/ ด้วย
อะไรที่เขียนลงไฟล์ = เปิดอ่านได้จากอินเทอร์เน็ต
"""
import os, re, sys, glob, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP_DIR = {'.git', 'node_modules', 'img', '__pycache__'}
SKIP_FILE = {'wordlist_master.csv', 'scan_secrets.py'}
EXT = {'.html', '.js', '.gs', '.md', '.json', '.css', '.txt', '.csv', '.py'}

# ── สิ่งที่ถือว่าเป็นความลับ ──
RULES = [
    ('🔴 รหัสผ่าน/คีย์ เขียนตรง ๆ ในโค้ด',
     re.compile(r"""(?:const|let|var)\s+\w*(?:PASS|PASSWORD|PWD|SECRET|APIKEY|API_KEY|TOKEN|AUTH)\w*\s*=\s*['"]([^'"]{4,})['"]""", re.I)),

    ('🔴 รหัสผ่านใน key-value ของ object/JSON',
     re.compile(r"""['"]?(?:password|passwd|secret|api_?key|token|teacher|admin_?pass)['"]?\s*[:=]\s*['"]([^'"]{6,})['"]""", re.I)),

    ('🔴 คีย์ของผู้ให้บริการ',
     re.compile(r"\b(sk_live_[A-Za-z0-9]{10,}|sk-[A-Za-z0-9]{20,}|AIza[0-9A-Za-z_\-]{30,}|ghp_[A-Za-z0-9]{30,}|xox[baprs]-[A-Za-z0-9-]{10,})\b")),

    # รหัสที่เคยหลุดสู่สาธารณะ — เติมรหัสเก่าทุกตัวไว้ที่นี่ จะได้ไม่ถูกนำกลับมาใช้
    ('🟠 รหัสที่เคยรั่ว — ห้ามใช้ซ้ำ',
     re.compile('\\b(' + '|'.join(['Gift' + '0142', 'oxford' + '2026']) + ')\\b')),

    ('🟠 เลขบัญชี / พร้อมเพย์ เขียนตรง ๆ',
     re.compile(r"""(?:promptpay|bank_?acc\w*|account_?no)\w*\s*[:=]\s*['"]?(\d{9,15})['"]?""", re.I)),

    ('🟡 เบอร์โทรส่วนตัว',
     re.compile(r"(?<![\d.])0(?:6|8|9)\d[- ]?\d{3}[- ]?\d{4}(?![\d.])")),
]

# ── ยกเว้นที่ไม่ใช่ความลับจริง ──
ALLOW = re.compile(
    r"YOUR_[A-Z_]+_HERE|<[^>]*ของคุณ>|example|placeholder|xxx+|อาทิ|ตัวอย่าง"
    r"|0812345678|123456|password'\s*\)|ADMIN_HASH|'pw_|\"pw_|wla_|pw_skills"
    r"|getElementById|querySelector|localStorage|sessionStorage", re.I)


def files():
    out = []
    for dp, dns, fns in os.walk(ROOT):
        dns[:] = [d for d in dns if d not in SKIP_DIR]
        for fn in fns:
            if fn in SKIP_FILE:
                continue
            if os.path.splitext(fn)[1].lower() in EXT:
                out.append(os.path.join(dp, fn))
    return sorted(out)


def main():
    strict = '--strict' in sys.argv
    hits = collections.defaultdict(list)
    n_files = 0

    for p in files():
        n_files += 1
        rel = os.path.relpath(p, ROOT).replace('\\', '/')
        try:
            lines = open(p, encoding='utf-8', errors='replace').read().split('\n')
        except Exception:
            continue
        for i, line in enumerate(lines, 1):
            if len(line) > 4000:
                continue
            for label, rx in RULES:
                for m in rx.finditer(line):
                    frag = (m.group(1) if m.groups() else m.group(0))
                    ctx = line.strip()[:120]
                    # คีย์ของผู้ให้บริการไม่ยกเว้นให้เด็ดขาด แม้จะดูเหมือนตัวอย่าง
                    if 'ผู้ให้บริการ' not in label and ALLOW.search(ctx):
                        continue
                    hits[label].append((rel, i, frag[:40], ctx))

    print('สแกน %d ไฟล์\n' % n_files)
    if not hits:
        print('✅ ไม่พบความลับหลุดในโปรเจกต์')
    total = 0
    for label, _ in RULES:
        if label not in hits:
            continue
        lst = hits[label]
        total += len(lst)
        print('%s — %d จุด' % (label, len(lst)))
        for rel, i, frag, ctx in lst[:12]:
            print('   %s:%d' % (rel, i))
            print('      %s' % ctx)
        if len(lst) > 12:
            print('   … อีก %d จุด' % (len(lst) - 12))
        print()

    # ── เตือนเรื่องไฟล์ที่ไม่ควร deploy ──
    print('─' * 54)
    print('ไฟล์ใน _docs/ ที่เปิดจากอินเทอร์เน็ตได้ (deploy ไปด้วย)')
    pub = [os.path.relpath(p, ROOT).replace('\\', '/')
           for p in glob.glob(os.path.join(ROOT, '_docs', '*.html'))]
    for p in pub:
        print('   https://peekaword.pages.dev/English/%s' % p)
    print('   → ไม่ควรมีรหัสผ่าน ข้อมูลลูกค้า หรือลิงก์ลับอยู่ในนี้')

    print('\n' + '─' * 54)
    if total:
        print('สรุป: พบ %d จุดที่ต้องดู' % total)
    else:
        print('สรุป: ผ่าน ✅')
    if strict and total:
        sys.exit(1)


if __name__ == '__main__':
    main()
