#!/usr/bin/env python3
"""แก้คำที่ไม่ใช่คำจริง (เขียนติดกัน เช่น sealevel) ให้เป็นวลีที่ถูกต้อง (sea level)
ทั้งใน Day page (WORDS, story, ประโยค) และ _docs/wordlist_master.csv
ชื่อไฟล์ภาพไม่เปลี่ยน เพราะ pic.js ตัดช่องว่าง/ขีดออกก่อนหาไฟล์
และเพิ่มการ์ดกันเกมเติมตัวอักษร (g5) สุ่มช่องว่างมาเป็นช่องเติม
ใช้:  py _docs\\fix_nonwords.py [--dry]
"""
import csv, glob, io, re, sys, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV = os.path.join(ROOT, '_docs', 'wordlist_master.csv')
DRY = '--dry' in sys.argv

# (day, เดิม, ใหม่, thai ใหม่ หรือ None = คงเดิม)
FIX = [
    (266, 'screentime',    'screen time',     None),
    (315, 'sealevel',      'sea level',       None),
    (325, 'selftalk',      'self-talk',       None),
    (330, 'peerreview',    'peer review',     None),
    (346, 'factcheck',     'fact-check',      None),
    (366, 'freewill',      'free will',       None),
    (366, 'headstart',     'head start',      None),
    (368, 'lightyear',     'light-year',      None),
    (369, 'bigbang',       'Big Bang',        None),
    (370, 'blackhole',     'black hole',      None),
    (370, 'neutronstar',   'neutron star',    None),
    (370, 'solarwind',     'solar wind',      None),
    (378, 'sideeffect',    'side effect',     None),
    (380, 'primarycare',   'primary care',    None),
    (384, 'floorplan',     'floor plan',      None),
    (384, 'highrise',      'high-rise',       None),
    (403, 'closeread',     'close reading',   None),
    (408, 'walkaway',      'walk-away',       None),
    (408, 'winwin',        'win-win',         None),
    (410, 'longterm',      'long-term',       None),
    (410, 'shortterm',     'short-term',      None),
    (412, 'supplychain',   'supply chain',    None),
    (412, 'freetrade',     'free trade',      None),
    (416, 'selfrestraint', 'self-restraint',  None),
    (421, 'upforce',       'lift',            'แรงยก (ปีกเครื่องบิน)'),
    (428, 'fossilrecord',  'fossil record',   None),
    (432, 'foodweb',       'food web',        None),
    (433, 'linkway',       'corridor',        'ทางเชื่อม (ผืนป่า)'),
    (435, 'carbonfibre',   'carbon fibre',    None),
]

G5_OLD = "while(pos.length<nb){const p=Math.floor(Math.random()*len);if(!pos.includes(p))pos.push(p);}"
G5_NEW = "while(pos.length<nb){const p=Math.floor(Math.random()*len);if(!pos.includes(p)&&/[a-z]/.test(g5answer[p]))pos.push(p);}"

def day_file(d):
    m = glob.glob(os.path.join(ROOT, 'Level*', f'Day{d}_*.html'))
    assert len(m) == 1, (d, m)
    return m[0]

def swap_case(old, new, m):
    s = m.group(0)
    if s.isupper(): return new.upper()
    if s[0].isupper(): return new[0].upper() + new[1:]
    return new

# --- CSV ---
rows = list(csv.reader(io.open(CSV, encoding='utf-8-sig')))
hdr, body = rows[0], rows[1:]
n = 0
for d, old, new, th in FIX:
    hit = [r for r in body if r[0] == str(d) and r[3] == old]
    if len(hit) != 1: print('CSV ไม่เจอ', d, old); continue
    hit[0][3] = new
    if th: hit[0][4] = th
    n += 1
if not DRY:
    with io.open(CSV, 'w', encoding='utf-8-sig', newline='') as f:
        w = csv.writer(f); w.writerow(hdr); w.writerows(body)
print('CSV แก้', n)

# --- Day pages ---
for d, old, new, th in FIX:
    p = day_file(d)
    s = io.open(p, encoding='utf-8').read()
    pat = re.compile(r'\b' + re.escape(old) + r'\b', re.I)
    cnt = len(pat.findall(s))
    s2 = pat.sub(lambda m: swap_case(old, new, m), s)
    if th:
        s2 = re.sub(r"(\{e:'" + re.escape(new) + r"',t:')[^']*'", lambda m: m.group(1) + th + "'", s2)
    print(f'Day{d} {old} → {new}: {cnt} ที่')
    if not DRY: io.open(p, 'w', encoding='utf-8', newline='').write(s2)

# --- g5 guard ทุกไฟล์ ---
g = 0
for p in glob.glob(os.path.join(ROOT, 'Level*', 'Day*.html')):
    s = io.open(p, encoding='utf-8').read()
    if G5_OLD in s:
        g += 1
        if not DRY: io.open(p, 'w', encoding='utf-8', newline='').write(s.replace(G5_OLD, G5_NEW))
print('g5 guard:', g, 'ไฟล์')
