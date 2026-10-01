#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ดึงรูป "ของจริง" มาใส่การ์ดคำศัพท์ — จาก Pexels (หลัก) และ Pixabay (สำรอง)
ทั้งสองแหล่งใช้เชิงพาณิชย์ได้ฟรี ไม่ต้องให้เครดิต

⚠️ ต้องรันบนเครื่องคุณ (sandbox ของ Claude ออกเน็ตไปสองเว็บนี้ไม่ได้)

ติดตั้ง:  pip install requests pillow

ขอ API key ฟรี (อย่างละ 1 นาที):
  Pexels  → https://www.pexels.com/api/   (200 req/ชม · 20,000 req/เดือน)
  Pixabay → https://pixabay.com/api/docs/ (~100 req/นาที)

ใช้:
  set PEXELS_KEY=xxxx
  set PIXABAY_KEY=yyyy
  python fetch_images.py --days 1-7            # ลองสัปดาห์แรกก่อน
  python fetch_images.py --cefr A1             # ทั้ง A1 (468 คำ)
  python fetch_images.py --days 1-7 --force    # ดาวน์โหลดทับของเดิม

ผลลัพธ์:
  English/img/words/<word>.webp      รูปสี่เหลี่ยมจัตุรัส 400px
  English/_docs/images/manifest.csv  บันทึกว่าแต่ละคำได้รูปจากไหน
  English/_docs/images/review.html   หน้าไว้ไล่ดูว่ารูปตรงความหมายมั้ย
"""
import os, sys, csv, io, time, json, argparse, urllib.parse

try:
    import requests
    from PIL import Image
except ImportError:
    sys.exit("ต้องติดตั้งก่อน:  pip install requests pillow")

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT  = os.path.join(ROOT, 'img', 'words')
MAN  = os.path.join(HERE, 'images', 'manifest.csv')
WORDS= os.path.join(HERE, 'wordlist_master.csv')
OVER = os.path.join(HERE, 'images', 'search_overrides.csv')

PEXELS  = os.environ.get('PEXELS_KEY', '').strip()
PIXABAY = os.environ.get('PIXABAY_KEY', '').strip()

# คำที่ค้นตรง ๆ แล้วได้รูปมั่ว — แปลงเป็นคำค้นที่เห็นภาพชัด
# เติมเพิ่มได้ใน _docs/images/search_overrides.csv (word,query)
DEFAULT_OVERRIDES = {
    'run':'child running','walk':'child walking','jump':'child jumping','swim':'child swimming',
    'eat':'child eating','drink':'child drinking','sit':'child sitting','look':'child looking',
    'fly':'bird flying','catch':'catching ball','sleep':'child sleeping','read':'child reading',
    'big':'big elephant small mouse','small':'tiny mouse','long':'long giraffe neck','short':'short pencil',
    'hot':'steaming hot soup','cold':'ice cubes','fast':'running cheetah','slow':'slow turtle',
    'happy':'happy child smiling','sad':'sad child','angry':'angry child face','scared':'scared child face',
    'tired':'tired sleepy child','excited':'excited happy kid','shy':'shy child','proud':'proud child',
    'beautiful':'beautiful flower','sweet':'honey dessert','color':'colorful paint',
}

def load_overrides():
    ov = dict(DEFAULT_OVERRIDES)
    if os.path.exists(OVER):
        with open(OVER, encoding='utf-8-sig') as f:
            for r in csv.DictReader(f):
                w = (r.get('word') or '').strip().lower()
                q = (r.get('query') or '').strip()
                if w and q: ov[w] = q
    return ov

def search_pexels(q):
    if not PEXELS: return None
    try:
        r = requests.get('https://api.pexels.com/v1/search',
                         headers={'Authorization': PEXELS},
                         params={'query': q, 'per_page': 3, 'orientation': 'square'},
                         timeout=20)
        if r.status_code != 200: return None
        ph = r.json().get('photos') or []
        if not ph: return None
        p = ph[0]
        return {'url': p['src']['large'], 'src': 'pexels',
                'page': p.get('url',''), 'author': (p.get('photographer') or '')}
    except Exception:
        return None

def search_pixabay(q):
    if not PIXABAY: return None
    try:
        r = requests.get('https://pixabay.com/api/',
                         params={'key': PIXABAY, 'q': q, 'image_type': 'photo',
                                 'safesearch': 'true', 'per_page': 3},
                         timeout=20)
        if r.status_code != 200: return None
        hits = r.json().get('hits') or []
        if not hits: return None
        h = hits[0]
        return {'url': h.get('largeImageURL') or h.get('webformatURL'), 'src': 'pixabay',
                'page': h.get('pageURL',''), 'author': h.get('user','')}
    except Exception:
        return None

def fetch_square(url, dest, size=400):
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    im = Image.open(io.BytesIO(r.content)).convert('RGB')
    w, h = im.size
    s = min(w, h)                                  # ครอบตรงกลางเป็นจัตุรัส
    im = im.crop(((w-s)//2, (h-s)//2, (w-s)//2+s, (h-s)//2+s))
    im = im.resize((size, size), Image.LANCZOS)
    im.save(dest, 'WEBP', quality=82, method=5)    # ~25–40 KB ต่อรูป

def pick_words(args):
    rows = list(csv.DictReader(open(WORDS, encoding='utf-8-sig')))
    if args.days:
        a, _, b = args.days.partition('-')
        lo, hi = int(a), int(b or a)
        rows = [r for r in rows if lo <= int(r['day']) <= hi]
    if args.cefr:
        want = {x.strip().upper() for x in args.cefr.split(',')}
        rows = [r for r in rows if r['cefr'].upper() in want]
    seen, out = set(), []
    for r in rows:
        w = r['english'].lower()
        if w in seen: continue
        seen.add(w); out.append(r)
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--days', help='ช่วงวัน เช่น 1-7')
    ap.add_argument('--cefr', help='ระดับ เช่น A1 หรือ A1,A2')
    ap.add_argument('--force', action='store_true', help='ดาวน์โหลดทับรูปเดิม')
    ap.add_argument('--limit', type=int, default=0)
    args = ap.parse_args()

    if not PEXELS and not PIXABAY:
        sys.exit('ยังไม่ได้ตั้ง PEXELS_KEY หรือ PIXABAY_KEY — ดูวิธีขอ key ที่หัวไฟล์')

    os.makedirs(OUT, exist_ok=True)
    os.makedirs(os.path.dirname(MAN), exist_ok=True)
    ov = load_overrides()
    words = pick_words(args)
    if args.limit: words = words[:args.limit]
    if not words: sys.exit('ไม่พบคำตามเงื่อนไขที่ให้มา')

    print(f'จะดึงรูป {len(words)} คำ  (Pexels={"มี key" if PEXELS else "-"} · Pixabay={"มี key" if PIXABAY else "-"})\n')

    man, ok, skip, fail = [], 0, 0, 0
    for i, r in enumerate(words, 1):
        w = r['english'].lower()
        dest = os.path.join(OUT, w + '.webp')
        if os.path.exists(dest) and not args.force:
            skip += 1
            print(f'  [{i:4}/{len(words)}] {w:<18} ข้าม (มีรูปแล้ว)')
            continue
        q = ov.get(w, w)
        hit = search_pexels(q) or search_pixabay(q)
        if not hit and q != w:                     # ลองคำตรง ๆ อีกรอบ
            hit = search_pexels(w) or search_pixabay(w)
        if not hit:
            fail += 1
            print(f'  [{i:4}/{len(words)}] {w:<18} ❌ ไม่เจอรูป  (query: {q})')
            man.append([w, r['cefr'], r['day'], q, '', '', '', 'NOT_FOUND'])
            continue
        try:
            fetch_square(hit['url'], dest)
            ok += 1
            print(f'  [{i:4}/{len(words)}] {w:<18} ✅ {hit["src"]}')
            man.append([w, r['cefr'], r['day'], q, hit['src'], hit['author'], hit['page'], 'OK'])
        except Exception as e:
            fail += 1
            print(f'  [{i:4}/{len(words)}] {w:<18} ❌ โหลดรูปไม่สำเร็จ: {e}')
            man.append([w, r['cefr'], r['day'], q, hit['src'], '', hit['page'], 'DOWNLOAD_FAIL'])
        time.sleep(0.4)                            # กัน rate limit

    head = ['word','cefr','day','query','source','author','page','status']
    old = []
    if os.path.exists(MAN):
        with open(MAN, encoding='utf-8-sig') as f:
            old = [row for row in csv.reader(f)][1:]
    done = {m[0] for m in man}
    merged = man + [o for o in old if o and o[0] not in done]
    with open(MAN, 'w', newline='', encoding='utf-8-sig') as f:
        cw = csv.writer(f); cw.writerow(head); cw.writerows(sorted(merged, key=lambda x: x[0]))

    print(f'\nสำเร็จ {ok} · ข้าม {skip} · ไม่สำเร็จ {fail}')
    print(f'รูปอยู่ที่      {OUT}')
    print(f'บันทึกแหล่งที่มา {MAN}')
    print('\nขั้นต่อไป: python make_review.py   แล้วเปิด _docs/images/review.html ไล่ดูทีละรูป')

if __name__ == '__main__':
    main()
