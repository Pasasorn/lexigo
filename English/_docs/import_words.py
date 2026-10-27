#!/usr/bin/env python3
"""นำเข้ารูปคำศัพท์จาก _incoming/ (zip หรือ .webp หลวม ๆ) → img/words/<คำ>.webp
- รับเฉพาะ .webp ที่ชื่อตรงคำใน wordlist_master.csv (ตัดช่องว่าง/ขีด) · ข้าม backup/ และไฟล์ที่มีอยู่แล้ว
- สรุปรายวัน + อัปเดต _docs/missing_word_images.csv และ wordlist.html
ใช้:  py _docs\\import_words.py
"""
import zipfile, glob, os, io, re, csv, shutil, collections, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
slug = lambda w: re.sub(r'[^a-z0-9]', '', w.lower())
rows = list(csv.reader(io.open('_docs/wordlist_master.csv', encoding='utf-8-sig')))[1:]
valid = {slug(r[3]): r for r in rows}
have = set(os.listdir('img/words'))

added, dup, unknown, bad, zips = [], 0, [], [], 0
def put(name, data):
    global dup
    s = slug(name[:-5])
    if s not in valid: unknown.append(name); return
    if s + '.webp' in have: dup += 1; return
    if not data.startswith(b'RIFF'): bad.append((name, 'not webp')); return
    io.open('img/words/' + s + '.webp', 'wb').write(data); have.add(s + '.webp'); added.append(s)

for z in sorted(glob.glob('_incoming/*.zip')):
    try: zf = zipfile.ZipFile(z)
    except Exception as e: bad.append((z, str(e))); continue
    zips += 1
    for n in zf.namelist():
        if n.endswith('/') or '/backup/' in n.lower(): continue
        b = os.path.basename(n).lower()
        if b.endswith('.webp'): put(b, zf.read(n))
for p in glob.glob('_incoming/*.webp'):
    put(os.path.basename(p).lower(), io.open(p, 'rb').read())

print(f'zip {zips} · เพิ่มใหม่ {len(added)} · ซ้ำข้าม {dup} · ชื่อไม่ตรงคำ {len(unknown)} {unknown[:8]} · เสีย {bad[:3]}')
byday = collections.Counter(int(valid[s][0]) for s in added)
for d in sorted(byday):
    tot = sum(1 for r in rows if int(r[0]) == d)
    print(f'  Day {d}: +{byday[d]}  ({sum(1 for r in rows if int(r[0]) == d and slug(r[3]) + ".webp" in have)}/{tot})')

miss = [r for r in rows if slug(r[3]) + '.webp' not in have]
print(f'รวมมีรูป {3000 - len(miss)} / 3000 · ยังขาด {len(miss)}')
bd = collections.Counter(int(r[0]) for r in miss); days = sorted(bd); rng = []; s = p = None
for d in days:
    if s is None: s = p = d
    elif d == p + 1: p = d
    else: rng.append((s, p)); s = p = d
if s is not None: rng.append((s, p))
print('ยังขาดช่วง:', ' · '.join(f'{a}–{b} ({sum(bd[x] for x in range(a, b + 1))})' if a != b else f'{a} ({bd[a]})' for a, b in rng))
with io.open('_docs/missing_word_images.csv', 'w', encoding='utf-8-sig', newline='') as f:
    w = csv.writer(f); w.writerow(['day', 'level', 'cefr', 'english', 'thai', 'filename_needed'])
    for r in miss: w.writerow([r[0], r[1], r[2], r[3], r[4], slug(r[3]) + '.webp'])
subprocess.run([sys.executable, '-I', '_docs/gen_wordlist_html.py'], capture_output=True)
