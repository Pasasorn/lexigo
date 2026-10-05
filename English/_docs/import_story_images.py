# -*- coding: utf-8 -*-
"""
นำภาพประกอบเรื่อง (ภาพใหญ่หัวบทเรียน) เข้าระบบ
- จับเลขวันจากชื่อไฟล์แบบไหนก็ได้  เช่น "Day 12.png" · "day12_v2.png" · "12.png"
- ครอบเป็น 16:9 + ย่อ 1200x675 + บันทึกเป็น WebP (เบากว่า PNG 5-10 เท่า)
- รายงานว่าวันไหนได้แล้ว วันไหนยังขาด

ใช้:
  py _docs/import_story_images.py "C:\\Users\\user\\Downloads\\story"
  py _docs/import_story_images.py "...\\story" --dry        ตรวจอย่างเดียว
  py _docs/import_story_images.py "...\\story" --png        เก็บเป็น .png ด้วย (ไม่แนะนำ ไฟล์ใหญ่)
"""
import os, re, sys, csv, argparse, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEST = os.path.join(ROOT, 'img')
EXT  = {'.png', '.jpg', '.jpeg', '.webp', '.bmp'}
W, H = 1200, 675          # 16:9


def day_of(name):
    """ดึงเลขวันจากชื่อไฟล์ — รองรับหลายแบบ"""
    s = os.path.splitext(os.path.basename(name))[0].lower()
    m = (re.search(r'day[\s_\-]*(\d{1,3})', s) or
         re.search(r'(?:^|[^0-9])(\d{1,3})(?:[^0-9]|$)', s))
    if not m:
        return None
    d = int(m.group(1))
    return d if 1 <= d <= 448 else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('src')
    ap.add_argument('--dry', action='store_true')
    ap.add_argument('--png', action='store_true')
    ap.add_argument('--q', type=int, default=80)
    a = ap.parse_args()

    if not os.path.isdir(a.src):
        sys.exit('ไม่พบโฟลเดอร์: %s' % a.src)

    found, unknown = {}, []
    for dp, _, fns in os.walk(a.src):
        for fn in fns:
            if os.path.splitext(fn)[1].lower() not in EXT:
                continue
            d = day_of(fn)
            if d:
                found[d] = os.path.join(dp, fn)      # ไฟล์หลังทับไฟล์ก่อน
            else:
                unknown.append(fn)

    print('ไฟล์ภาพที่เจอ : %d' % (len(found) + len(unknown)))
    print('จับคู่วันได้  : %d วัน' % len(found))
    if unknown:
        print('⚠️  อ่านเลขวันจากชื่อไฟล์ไม่ได้ %d ไฟล์: %s%s'
              % (len(unknown), ', '.join(unknown[:10]), ' …' if len(unknown) > 10 else ''))
        print('    → ตั้งชื่อให้มีเลขวัน เช่น  day12.png  หรือ  Day 12 - ชื่อเรื่อง.png')

    if not a.dry and found:
        try:
            from PIL import Image
        except ImportError:
            sys.exit('ต้องติดตั้งก่อน:  pip install pillow')
        os.makedirs(DEST, exist_ok=True)
        ok = fail = 0
        tin = tout = 0
        for i, (d, p) in enumerate(sorted(found.items()), 1):
            try:
                tin += os.path.getsize(p)
                im = Image.open(p).convert('RGB')
                # ครอบกลางภาพให้เป็น 16:9 ก่อนย่อ
                w, h = im.size
                want = W / float(H)
                if w / float(h) > want:                 # กว้างเกิน → ตัดข้าง
                    nw = int(h * want)
                    im = im.crop(((w - nw) // 2, 0, (w - nw) // 2 + nw, h))
                else:                                   # สูงเกิน → ตัดบนล่าง
                    nh = int(w / want)
                    im = im.crop((0, (h - nh) // 2, w, (h - nh) // 2 + nh))
                im = im.resize((W, H), Image.LANCZOS)
                out = os.path.join(DEST, 'img_day%d.webp' % d)
                im.save(out, 'WEBP', quality=a.q, method=6)
                tout += os.path.getsize(out)
                if a.png:
                    im.save(os.path.join(DEST, 'img_day%d.png' % d), 'PNG', optimize=True)
                ok += 1
            except Exception as e:
                fail += 1
                print('  ✗ Day %s : %s' % (d, str(e)[:70]))
            if i % 50 == 0:
                print('  … %d/%d' % (i, len(found)))
        print('\nเขียนสำเร็จ %d ไฟล์%s' % (ok, (' · ล้มเหลว %d' % fail) if fail else ''))
        if tin:
            print('ขนาดรวม %.1f MB → %.1f MB (ลด %.0f%%)'
                  % (tin / 1e6, tout / 1e6, 100 - tout * 100.0 / tin))

    # ── เตือนไฟล์ชนกัน: .png เก่า จะถูกใช้ก่อน .webp ใหม่ ──
    clash = []
    if os.path.isdir(DEST):
        for f in os.listdir(DEST):
            m = re.match(r'img_day(\d+)\.png$', f)
            if m and os.path.exists(os.path.join(DEST, 'img_day%s.webp' % m.group(1))):
                clash.append(m.group(1))
    if clash:
        print('\n⚠️  มีทั้ง .png และ .webp ของวัน: %s' % ', '.join(sorted(clash, key=int)))
        print('    หน้าเว็บหา .png ก่อน → จะได้ภาพเก่า ให้ย้าย .png พวกนี้ออก')

    # ── ความครอบคลุม ──
    have = set()
    if os.path.isdir(DEST):
        for f in os.listdir(DEST):
            m = re.match(r'img_day(\d+)\.(webp|png|jpg)$', f)
            if m:
                have.add(int(m.group(1)))
    if a.dry:
        have |= set(found)

    print('\n' + '=' * 50)
    print('ภาพประกอบเรื่อง: %d / 448 วัน (%.0f%%)' % (len(have), len(have) * 100.0 / 448))
    miss = [d for d in range(1, 449) if d not in have]
    print('ยังขาด %d วัน' % len(miss))
    if miss:
        print('  7 วันทดลอง (สำคัญสุด): %s' % ([d for d in miss if d <= 7] or 'ครบแล้ว ✅'))
        print('  30 วันแรก: %s' % ([d for d in miss if d <= 30][:20] or 'ครบแล้ว ✅'))
        mp = os.path.join(ROOT, '_docs', 'missing_story_images.csv')
        with open(mp, 'w', newline='', encoding='utf-8-sig') as f:
            w = csv.writer(f)
            w.writerow(['day', 'filename_ควรตั้ง'])
            for d in miss:
                w.writerow([d, 'img_day%d.png' % d])
        print('\nรายชื่อวันที่ขาด → _docs/missing_story_images.csv')


if __name__ == '__main__':
    main()
