# -*- coding: utf-8 -*-
"""
แปลงรูปจาก _incoming/.unzip ทีละชุด (กันงานค้างเพราะไฟล์เยอะ)
รันซ้ำได้เรื่อย ๆ จนกว่าจะหมด — ข้ามไฟล์ที่ทำไปแล้ว

รัน:  py _docs/convert_batch.py [จำนวนต่อรอบ]
"""
import os, re, sys, csv, collections
from PIL import Image, ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

ROOT  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK  = os.path.join(ROOT, '_incoming', '.unzip')
IMG   = os.path.join(ROOT, 'img')
WORDS = os.path.join(IMG, 'words')
EXT   = {'.webp', '.png', '.jpg', '.jpeg', '.bmp'}
LIMIT = int(sys.argv[1]) if len(sys.argv) > 1 else 60


def slug(s):
    return ''.join(c for c in s.lower() if c.isalnum())


def day_of(name):
    s = os.path.splitext(os.path.basename(name))[0].lower()
    m = re.search(r'day[\s_\-]*(\d{1,3})', s) or re.fullmatch(r'\s*(\d{1,3})\s*', s)
    if not m:
        return None
    d = int(m.group(1))
    return d if 1 <= d <= 448 else None


def fit(im, w, h):
    W, H = im.size
    want = w / float(h)
    if W / float(H) > want:
        nw = int(H * want)
        im = im.crop(((W - nw) // 2, 0, (W - nw) // 2 + nw, H))
    else:
        nh = int(W / want)
        im = im.crop((0, (H - nh) // 2, W, (H - nh) // 2 + nh))
    return im.resize((w, h), Image.LANCZOS)


rows = list(csv.DictReader(open(os.path.join(ROOT, '_docs', 'wordlist_master.csv'),
                                encoding='utf-8-sig')))
known = {slug(r['english']) for r in rows}

todo_story, todo_word = {}, {}
for dp, dn, fn in os.walk(WORK):
    for f in fn:
        if os.path.splitext(f)[1].lower() not in EXT:
            continue
        p = os.path.join(dp, f)
        d = day_of(f)
        if d is not None:
            if not os.path.exists(os.path.join(IMG, 'img_day%d.webp' % d)):
                todo_story[d] = p
            continue
        k = slug(os.path.splitext(f)[0])
        k = re.sub(r'\d+$', '', k) if k not in known and re.sub(r'\d+$', '', k) in known else k
        if k in known and not os.path.exists(os.path.join(WORDS, k + '.webp')):
            todo_word[k] = p

total = len(todo_story) + len(todo_word)
if not total:
    print('✅ แปลงครบแล้ว ไม่เหลืองาน')
    sys.exit(0)

os.makedirs(WORDS, exist_ok=True)
done = fail = 0
tin = tout = 0

for d, p in sorted(todo_story.items()):
    if done >= LIMIT:
        break
    try:
        tin += os.path.getsize(p)
        out = os.path.join(IMG, 'img_day%d.webp' % d)
        fit(Image.open(p).convert('RGB'), 1200, 675).save(out, 'WEBP', quality=82, method=6)
        old = os.path.join(IMG, 'img_day%d.png' % d)
        if os.path.exists(old):
            os.remove(old)
        tout += os.path.getsize(out)
        done += 1
    except Exception as e:
        fail += 1
        print('  ✗ Day %s : %s' % (d, str(e)[:60]))

for k, p in sorted(todo_word.items()):
    if done >= LIMIT:
        break
    try:
        tin += os.path.getsize(p)
        out = os.path.join(WORDS, k + '.webp')
        fit(Image.open(p).convert('RGB'), 400, 400).save(out, 'WEBP', quality=82, method=6)
        tout += os.path.getsize(out)
        done += 1
    except Exception as e:
        fail += 1
        print('  ✗ %s : %s' % (k, str(e)[:60]))

left = total - done
print('รอบนี้แปลง %d ไฟล์%s · เหลืออีก %d'
      % (done, (' · พลาด %d' % fail) if fail else '', left))
if tin:
    print('  %.0f MB → %.1f MB' % (tin / 1e6, tout / 1e6))

have_s = len([f for f in os.listdir(IMG) if re.match(r'img_day\d+\.webp$', f)])
have_w = len([f for f in os.listdir(WORDS) if f.endswith('.webp')])
print('รวมตอนนี้: ภาพเรื่อง %d/448 · คำศัพท์ %d/3000' % (have_s, have_w))
