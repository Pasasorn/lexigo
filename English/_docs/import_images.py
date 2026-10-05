# -*- coding: utf-8 -*-
"""
นำรูปจาก Google Drive เข้าระบบ PeekaWord
- ตั้งชื่อใหม่ให้ตรงกับคำศัพท์ (ตัวพิมพ์เล็ก ตัดอักขระพิเศษ)
- ครอบสี่เหลี่ยมจัตุรัสจากกลางภาพ + ย่อเป็น 400x400 + WebP q82
- รายงานว่าคำไหนได้ภาพแล้ว คำไหนยังขาด และไฟล์ไหนไม่ตรงกับคำศัพท์เลย

วิธีใช้
  1) เปิดโฟลเดอร์ Drive → Ctrl+A → Download  (Drive จะบีบเป็น .zip ให้)
  2) แตกไฟล์ไว้ที่ไหนก็ได้ เช่น  C:\\Users\\user\\Downloads\\words
  3) pip install pillow
  4) python _docs/import_images.py "C:\\Users\\user\\Downloads\\words"

ตัวเลือก
  --dry       ตรวจอย่างเดียว ไม่เขียนไฟล์
  --size 400  ความกว้าง/สูงปลายทาง (ค่าเริ่มต้น 400)
  --q 82      คุณภาพ WebP (ค่าเริ่มต้น 82)
  --keep      ไม่ย่อขนาด คัดลอกตรง ๆ (ไม่แนะนำ ไฟล์จะหนักมาก)
"""
import os, sys, csv, re, shutil, argparse, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEST = os.path.join(ROOT, 'img', 'words')
CSV  = os.path.join(ROOT, '_docs', 'wordlist_master.csv')
EXT  = {'.webp', '.png', '.jpg', '.jpeg', '.gif', '.bmp'}


def slug(s):
    return re.sub(r'[^a-z0-9]', '', s.lower())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('src', help='โฟลเดอร์ที่แตกไฟล์จาก Drive ไว้')
    ap.add_argument('--dry', action='store_true')
    ap.add_argument('--size', type=int, default=400)
    ap.add_argument('--q', type=int, default=82)
    ap.add_argument('--keep', action='store_true')
    a = ap.parse_args()

    if not os.path.isdir(a.src):
        sys.exit('ไม่พบโฟลเดอร์: %s' % a.src)

    # --- คำศัพท์ทั้งหมด ---
    rows = list(csv.DictReader(open(CSV, encoding='utf-8-sig')))
    bySlug = {}
    for r in rows:
        bySlug.setdefault(slug(r['english']), r)
    print('คำศัพท์ในระบบ: %d คำ' % len(bySlug))

    # --- ไฟล์ต้นทาง (ไล่โฟลเดอร์ย่อยด้วย) ---
    srcs = []
    for dp, _, fns in os.walk(a.src):
        for fn in fns:
            if os.path.splitext(fn)[1].lower() in EXT:
                srcs.append(os.path.join(dp, fn))
    print('ไฟล์รูปที่เจอ: %d ไฟล์' % len(srcs))
    if not srcs:
        sys.exit('ไม่เจอไฟล์รูปเลย — ตรวจ path อีกที')

    # --- จับคู่ ---
    match, unknown, dup = {}, [], collections.defaultdict(list)
    for p in srcs:
        k = slug(os.path.splitext(os.path.basename(p))[0])
        # ตัดท้ายแบบ "cat (1)" / "cat-2" ที่ Drive ชอบเติม
        k = re.sub(r'\d+$', '', k) if k not in bySlug and re.sub(r'\d+$', '', k) in bySlug else k
        if k in bySlug:
            dup[k].append(p)
            match[k] = p
        else:
            unknown.append(os.path.basename(p))

    dups = {k: v for k, v in dup.items() if len(v) > 1}
    print('จับคู่กับคำศัพท์ได้: %d คำ' % len(match))
    if dups:
        print('⚠️  มีไฟล์ซ้ำชื่อ %d คำ (ใช้ไฟล์ล่าสุด): %s'
              % (len(dups), ', '.join(list(dups)[:8])))
    if unknown:
        print('⚠️  ไม่ตรงกับคำศัพท์ใด ๆ %d ไฟล์: %s%s'
              % (len(unknown), ', '.join(unknown[:12]), ' …' if len(unknown) > 12 else ''))

    # --- แปลง + เขียน ---
    if not a.dry:
        os.makedirs(DEST, exist_ok=True)
        try:
            from PIL import Image
        except ImportError:
            sys.exit('ต้องติดตั้งก่อน:  pip install pillow')

        ok = fail = 0
        tot_in = tot_out = 0
        for i, (k, p) in enumerate(sorted(match.items()), 1):
            out = os.path.join(DEST, k + '.webp')
            try:
                tot_in += os.path.getsize(p)
                if a.keep:
                    shutil.copyfile(p, out)
                else:
                    im = Image.open(p).convert('RGB')
                    w, h = im.size
                    s = min(w, h)
                    im = im.crop(((w - s) // 2, (h - s) // 2,
                                  (w - s) // 2 + s, (h - s) // 2 + s))
                    im = im.resize((a.size, a.size), Image.LANCZOS)
                    im.save(out, 'WEBP', quality=a.q, method=6)
                tot_out += os.path.getsize(out)
                ok += 1
            except Exception as e:
                fail += 1
                print('  ✗ %s : %s' % (k, str(e)[:70]))
            if i % 100 == 0:
                print('  … %d/%d' % (i, len(match)))

        print('\nเขียนสำเร็จ %d ไฟล์%s' % (ok, (' · ล้มเหลว %d' % fail) if fail else ''))
        print('ขนาดรวม %.1f MB → %.1f MB  (ลด %.0f%%)'
              % (tot_in / 1e6, tot_out / 1e6,
                 100 - tot_out * 100.0 / tot_in if tot_in else 0))

    # --- ความครอบคลุม ---
    have = {os.path.splitext(f)[0] for f in os.listdir(DEST)} if os.path.isdir(DEST) else set()
    if a.dry:
        have |= set(match)

    print('\n' + '=' * 52)
    print('ความครอบคลุมภาพประกอบ')
    byc = collections.defaultdict(lambda: [0, 0])
    for r in rows:
        c = byc[r['cefr']]
        c[1] += 1
        if slug(r['english']) in have:
            c[0] += 1
    for c in ['A1', 'A2', 'B1', 'B2']:
        if c in byc:
            g, t = byc[c]
            print('  %-3s %4d/%-4d  %3.0f%%  %s' % (c, g, t, g * 100.0 / t,
                  '█' * int(g * 20.0 / t) + '░' * (20 - int(g * 20.0 / t))))
    g = sum(1 for r in rows if slug(r['english']) in have)
    print('  รวม %d/%d  (%.0f%%)' % (g, len(rows), g * 100.0 / len(rows)))

    # วันที่ภาพครบแล้ว
    byday = collections.defaultdict(lambda: [0, 0])
    for r in rows:
        d = byday[int(r['day'])]
        d[1] += 1
        if slug(r['english']) in have:
            d[0] += 1
    full = sorted(d for d, (g2, t) in byday.items() if g2 == t)
    part = sorted(d for d, (g2, t) in byday.items() if 0 < g2 < t)
    print('\nวันที่ภาพครบทุกคำ: %d วัน' % len(full))
    if full:
        print('  %s%s' % (', '.join(map(str, full[:30])), ' …' if len(full) > 30 else ''))
    print('วันที่ได้บางส่วน: %d วัน' % len(part))

    # คำที่ยังขาด เขียนเป็นไฟล์ไว้ไปสร้างรูปต่อ
    missing = [r for r in rows if slug(r['english']) not in have]
    mp = os.path.join(ROOT, '_docs', 'images', 'missing_words.csv')
    os.makedirs(os.path.dirname(mp), exist_ok=True)
    with open(mp, 'w', newline='', encoding='utf-8-sig') as f:
        w = csv.writer(f)
        w.writerow(['day', 'cefr', 'english', 'thai', 'filename_ควรตั้ง'])
        for r in missing:
            w.writerow([r['day'], r['cefr'], r['english'], r['thai'],
                        slug(r['english']) + '.webp'])
    print('\nคำที่ยังไม่มีภาพ %d คำ → _docs/images/missing_words.csv' % len(missing))
    print('(เรียงตามวัน — ใช้ไฟล์นี้ไปสร้างรูปรอบต่อไปได้เลย)')


if __name__ == '__main__':
    main()
