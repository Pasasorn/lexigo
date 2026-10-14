# -*- coding: utf-8 -*-
"""
นำเข้ารูปจากโฟลเดอร์ _incoming/ แบบอัตโนมัติ

วางอะไรก็ได้ลงใน  English/_incoming/
  - ไฟล์ .zip (แตกให้เอง ไม่ต้องแตกเอง)
  - รูปเปล่า ๆ .webp .png .jpg
  - โฟลเดอร์ย่อยก็ได้

สคริปต์แยกเองว่าเป็นรูปชนิดไหน:
  ชื่อไฟล์มีเลขวัน (day12 / img_day12 / Day 12 - xxx)  →  ภาพประกอบเรื่อง  1200x675  →  img/
  ชื่อไฟล์เป็นคำศัพท์ (cat / energy)                   →  ภาพคำศัพท์      400x400   →  img/words/

รัน:  py _docs/import_incoming.py
      py _docs/import_incoming.py --dry      ตรวจอย่างเดียว
      py _docs/import_incoming.py --keep     ไม่ย้ายไฟล์ต้นทางไป done/
"""
import os, re, sys, csv, glob, shutil, zipfile, argparse, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INBOX = os.path.join(ROOT, '_incoming')
DONE  = os.path.join(INBOX, 'done')
WORK  = os.path.join(INBOX, '.unzip')
IMG   = os.path.join(ROOT, 'img')
WORDS = os.path.join(IMG, 'words')
EXT   = {'.webp', '.png', '.jpg', '.jpeg', '.bmp'}

STORY_W, STORY_H = 1200, 675
WORD_SIZE = 400


def slug(s):
    return ''.join(c for c in s.lower() if c.isalnum())


def day_of(name):
    s = os.path.splitext(os.path.basename(name))[0].lower()
    m = re.search(r'day[\s_\-]*(\d{1,3})', s)
    if not m:
        m = re.fullmatch(r'\s*(\d{1,3})\s*', s)     # ชื่อเป็นตัวเลขล้วน
    if not m:
        return None
    d = int(m.group(1))
    return d if 1 <= d <= 448 else None


def fit(im, w, h):
    """ครอบจากกลางภาพให้ได้สัดส่วน w:h แล้วย่อ"""
    W, H = im.size
    want = w / float(h)
    if W / float(H) > want:
        nw = int(H * want)
        im = im.crop(((W - nw) // 2, 0, (W - nw) // 2 + nw, H))
    else:
        nh = int(W / want)
        im = im.crop((0, (H - nh) // 2, W, (H - nh) // 2 + nh))
    return im.resize((w, h), Image.LANCZOS)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dry', action='store_true')
    ap.add_argument('--keep', action='store_true')
    ap.add_argument('--q', type=int, default=82)
    a = ap.parse_args()

    if not os.path.isdir(INBOX):
        sys.exit('ไม่พบโฟลเดอร์ %s' % INBOX)

    # ── แตก zip ──
    shutil.rmtree(WORK, ignore_errors=True)
    os.makedirs(WORK, exist_ok=True)
    zips = [p for p in glob.glob(os.path.join(INBOX, '**', '*.zip'), recursive=True)
            if DONE not in p and WORK not in p]
    def unzip_all(paths, depth=0):
        """แตก zip แล้วไล่แตก zip ที่ซ้อนอยู่ข้างในด้วย (ลึกได้ 3 ชั้น)"""
        if depth > 3:
            return
        nested = []
        for z in paths:
            try:
                base = os.path.splitext(os.path.basename(z))[0]
                dest = os.path.join(WORK, base if depth == 0 else
                                    os.path.join(os.path.dirname(z).replace(WORK, '').lstrip(os.sep), base))
                with zipfile.ZipFile(z) as zf:
                    zf.extractall(dest)
                print('%sแตก %s' % ('  ' * depth, os.path.basename(z)))
                nested += glob.glob(os.path.join(dest, '**', '*.zip'), recursive=True)
            except Exception as e:
                print('✗ แตกไม่ได้ %s : %s' % (os.path.basename(z), str(e)[:60]))
        if nested:
            unzip_all(nested, depth + 1)

    unzip_all(zips)

    # ── รวบรวมรูปทั้งหมด ──
    srcs = []
    for base in (INBOX, WORK):
        for dp, dns, fns in os.walk(base):
            if DONE in dp:
                continue
            for fn in fns:
                if os.path.splitext(fn)[1].lower() in EXT:
                    srcs.append(os.path.join(dp, fn))
    srcs = sorted(set(srcs))

    if not srcs and not zips:
        print('ไม่มีไฟล์ใหม่ใน _incoming/')
        return

    # ── คำศัพท์ที่ระบบรู้จัก ──
    rows = list(csv.DictReader(open(os.path.join(ROOT, '_docs', 'wordlist_master.csv'),
                                    encoding='utf-8-sig')))
    known = {slug(r['english']) for r in rows}

    story, word, unknown = {}, {}, []
    for p in srcs:
        d = day_of(p)
        k = slug(os.path.splitext(os.path.basename(p))[0])
        k = re.sub(r'\d+$', '', k) if k not in known and re.sub(r'\d+$', '', k) in known else k
        if d is not None:
            story[d] = p
        elif k in known:
            word[k] = p
        else:
            unknown.append(os.path.basename(p))

    print('\nเจอรูป %d ไฟล์' % len(srcs))
    print('  ภาพประกอบเรื่อง : %d  %s' % (len(story), sorted(story)[:12]))
    print('  ภาพคำศัพท์      : %d' % len(word))
    if unknown:
        print('  ⚠️ แยกไม่ออก %d ไฟล์: %s%s'
              % (len(unknown), ', '.join(unknown[:10]), ' …' if len(unknown) > 10 else ''))
        print('     → ถ้าเป็นภาพเรื่อง ตั้งชื่อให้มีเลขวัน · ถ้าเป็นคำศัพท์ ตั้งชื่อตามคำ')

    if a.dry:
        shutil.rmtree(WORK, ignore_errors=True)
        return

    global Image
    try:
        from PIL import Image, ImageFile
        ImageFile.LOAD_TRUNCATED_IMAGES = True
    except ImportError:
        sys.exit('ต้องติดตั้งก่อน:  pip install pillow')

    os.makedirs(IMG, exist_ok=True)
    os.makedirs(WORDS, exist_ok=True)
    ok = fail = 0
    tin = tout = 0

    for d, p in sorted(story.items()):
        try:
            tin += os.path.getsize(p)
            im = Image.open(p).convert('RGB')
            out = os.path.join(IMG, 'img_day%d.webp' % d)
            fit(im, STORY_W, STORY_H).save(out, 'WEBP', quality=a.q, method=6)
            # ถ้ามี .png เก่าของวันเดียวกัน ให้เอาออก (หน้าเว็บหา .png ก่อน)
            old = os.path.join(IMG, 'img_day%d.png' % d)
            if os.path.exists(old):
                os.remove(old)
                print('  ลบ img_day%d.png เก่าออก' % d)
            tout += os.path.getsize(out)
            ok += 1
        except Exception as e:
            fail += 1
            print('  ✗ Day %s : %s' % (d, str(e)[:60]))

    for k, p in sorted(word.items()):
        try:
            tin += os.path.getsize(p)
            im = Image.open(p).convert('RGB')
            out = os.path.join(WORDS, k + '.webp')
            fit(im, WORD_SIZE, WORD_SIZE).save(out, 'WEBP', quality=a.q, method=6)
            tout += os.path.getsize(out)
            ok += 1
        except Exception as e:
            fail += 1
            print('  ✗ %s : %s' % (k, str(e)[:60]))

    print('\nนำเข้าสำเร็จ %d ไฟล์%s' % (ok, (' · ล้มเหลว %d' % fail) if fail else ''))
    if tin:
        print('ขนาด %.1f MB → %.1f MB (ลด %.0f%%)'
              % (tin / 1e6, tout / 1e6, 100 - tout * 100.0 / tin))

    # ── เก็บไฟล์ต้นทาง ──
    shutil.rmtree(WORK, ignore_errors=True)
    if not a.keep:
        os.makedirs(DONE, exist_ok=True)
        moved = 0
        for p in glob.glob(os.path.join(INBOX, '*')):
            b = os.path.basename(p)
            if b in ('done', '.unzip') or b.endswith('.txt'):
                continue
            dst = os.path.join(DONE, b)
            if os.path.exists(dst):
                dst = dst + '.' + str(moved)
            shutil.move(p, dst)
            moved += 1
        if moved:
            print('ย้ายไฟล์ต้นทาง %d รายการไป _incoming/done/' % moved)

    # ── สรุปความคืบหน้า ──
    have_w = {os.path.splitext(f)[0] for f in os.listdir(WORDS)}
    have_s = {int(m.group(1)) for m in
              (re.match(r'img_day(\d+)\.', f) for f in os.listdir(IMG)) if m}
    got = sum(1 for r in rows if slug(r['english']) in have_w)
    print('\n' + '=' * 50)
    print('ภาพคำศัพท์      %d / %d  (%.0f%%)' % (got, len(rows), got * 100.0 / len(rows)))
    print('ภาพประกอบเรื่อง %d / 448' % len(have_s))

    byday = collections.defaultdict(lambda: [0, 0])
    for r in rows:
        x = byday[int(r['day'])]
        x[1] += 1
        if slug(r['english']) in have_w:
            x[0] += 1
    run = 0
    for d in range(1, max(byday) + 1):
        if d not in byday:
            continue
        if byday[d][0] == byday[d][1]:
            run = d
        else:
            break
    part = sorted(d for d, (g, t) in byday.items() if 0 < g < t)
    print('  ครบติดกันถึง Day %d' % run)
    if part:
        print('  ได้บางส่วน: %s' % ', '.join('Day %d (%d/%d)' % (d, *byday[d]) for d in part[:8]))
    print('\nขั้นต่อไป:  py _docs\\gen_wordlist_html.py  แล้ว  git push')


if __name__ == '__main__':
    main()
