# -*- coding: utf-8 -*-
"""
ตรวจภาพทั้งระบบ — ช่องภาพครบไหม ชี้ไฟล์ถูกไหม ไฟล์มีจริงไหม

รัน:  py _docs/audit_images.py
      py _docs/audit_images.py --strict    (เจอปัญหา = exit 1 ใช้ใน CI)
"""
import os, re, sys, csv, glob, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG  = os.path.join(ROOT, 'img')
WORD = os.path.join(IMG, 'words')


def slug(s):
    return ''.join(c for c in s.lower() if c.isalnum())


def pages_of(h):
    """คืน dict: page id -> เนื้อหา"""
    out, cur, buf = {}, None, []
    for part in re.split(r'(<div class="page[^"]*" id="p\d">)', h):
        m = re.match(r'<div class="page[^"]*" id="(p\d)">', part)
        if m:
            if cur:
                out[cur] = ''.join(buf)
            cur, buf = m.group(1), []
        elif cur:
            buf.append(part)
    if cur:
        out[cur] = ''.join(buf)
    return out


def main():
    strict = '--strict' in sys.argv
    files = sorted(glob.glob(os.path.join(ROOT, 'Level*', 'Day*.html')),
                   key=lambda p: int(re.search(r'Day(\d+)', os.path.basename(p)).group(1)))

    have_story = {}
    for f in glob.glob(os.path.join(IMG, 'img_day*.*')):
        m = re.match(r'img_day(\d+)\.(png|webp|jpg|jpeg)$', os.path.basename(f))
        if m:
            have_story.setdefault(int(m.group(1)), []).append(m.group(2))
    have_word = {os.path.splitext(f)[0] for f in os.listdir(WORD)} if os.path.isdir(WORD) else set()

    bad = collections.defaultdict(list)
    story_days, review_days = [], []

    for p in files:
        d = int(re.search(r'Day(\d+)', os.path.basename(p)).group(1))
        h = open(p, encoding='utf-8').read()
        pg = pages_of(h)
        is_rev = len(pg) == 9
        (review_days if is_rev else story_days).append(d)

        slots = {k: len(re.findall(r'img_day(\d+)', v)) for k, v in pg.items()
                 if 'img_day' in v}

        # 1) ช่องภาพต้องอยู่ครบตามรูปแบบ
        if is_rev:
            if 'p0' not in slots:
                bad['วันทบทวนไม่มีช่องภาพหน้าปก'].append(d)
        else:
            for want in ('p1', 'p2'):
                if want not in slots:
                    bad['วันเรียนไม่มีช่องภาพใน %s' % ('Step 1' if want == 'p1' else 'Step 2')].append(d)

        # 2) ทุกช่องต้องชี้เลขวันของตัวเอง
        for n in set(re.findall(r'img_day(\d+)', h)):
            if int(n) != d:
                bad['ชี้เลขวันผิด'].append('Day %d → img_day%s' % (d, n))

        # 3) ต้องใช้ aspect-ratio ไม่ใช่ max-height (กันภาพโดนตัด)
        for tag in re.findall(r'<img [^>]*img_day\d+[^>]*>', h):
            if 'max-height' in tag:
                bad['ยังใช้ max-height (ภาพจะโดนตัด)'].append(d)
            if 'aspect-ratio:16/9' not in tag:
                bad['ไม่มี aspect-ratio:16/9'].append(d)
            if ".replace('.png','.webp')" not in tag:
                bad['ไม่มี fallback .png→.webp'].append(d)

        # 4) ไฟล์ภาพเรื่องมีจริงไหม
        if 'img_day' in h and d not in have_story:
            bad['ยังไม่มีไฟล์ภาพเรื่อง'].append(d)

        # 5) การ์ดคำศัพท์ต้องเรียกผ่าน pwPic
        if not is_rev and 'pwPic' not in h:
            bad['การ์ดคำศัพท์ไม่ได้เรียก pwPic'].append(d)

    # ── รายงาน ──
    print('ไฟล์ทั้งหมด %d  ·  วันเรียน %d  ·  วันทบทวน %d\n'
          % (len(files), len(story_days), len(review_days)))

    print('ภาพประกอบเรื่อง: %d / %d วัน' % (len(have_story), len(files)))
    dup = {d: v for d, v in have_story.items() if len(v) > 1}
    if dup:
        print('  ⚠️ มีหลายนามสกุลของวันเดียวกัน (หน้าเว็บจะใช้ .png ก่อน): %s'
              % ', '.join('Day %d (%s)' % (d, '+'.join(v)) for d, v in sorted(dup.items())[:8]))

    # คำศัพท์
    rows = list(csv.DictReader(open(os.path.join(ROOT, '_docs', 'wordlist_master.csv'),
                                    encoding='utf-8-sig')))
    byday = collections.defaultdict(lambda: [0, 0])
    for r in rows:
        x = byday[int(r['day'])]
        x[1] += 1
        if slug(r['english']) in have_word:
            x[0] += 1
    got = sum(1 for r in rows if slug(r['english']) in have_word)
    print('ภาพคำศัพท์: %d / %d คำ (%.0f%%)' % (got, len(rows), got * 100.0 / len(rows)))
    full = sorted(d for d, (g, t) in byday.items() if g == t)
    part = sorted(d for d, (g, t) in byday.items() if 0 < g < t)
    if full:
        run = 0
        for d in range(1, max(byday) + 1):
            if d not in byday:        # วันทบทวนไม่มีคำใหม่ — ข้ามไป ไม่ตัดช่วง
                continue
            if d in full:
                run = d
            else:
                break
        print('  ครบทุกคำติดกันถึง Day %d · ครบรวม %d วัน' % (run, len(full)))
    if part:
        print('  ได้บางส่วน: %s' % ', '.join('Day %d (%d/%d)' % (d, *byday[d]) for d in part[:10]))

    print('\n' + '=' * 54)
    if not bad:
        print('✅ ไม่พบปัญหา')
    for k in sorted(bad):
        v = bad[k]
        uniq = sorted(set(v), key=lambda x: (isinstance(x, str), x))
        print('❌ %s — %d จุด' % (k, len(v)))
        print('   %s%s' % (', '.join(str(x) for x in uniq[:15]), ' …' if len(uniq) > 15 else ''))

    if strict and bad:
        sys.exit(1)


if __name__ == '__main__':
    main()
