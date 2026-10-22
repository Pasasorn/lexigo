# -*- coding: utf-8 -*-
"""
สร้าง js/synonyms.js — จับคู่คำที่ "แปลไทยเหมือนกัน" แล้วชี้กลับไปคำที่เรียนไปก่อน

ทำไมต้องมี: เด็กเจอ vulnerable (Day 230) ที่แปลว่า "เปราะบาง" เหมือน fragile (Day 212)
ถ้าไม่บอก เด็กจะงงว่าเรียนซ้ำหรือเปล่า · บอกแล้วกลายเป็นโอกาสให้สังเกตความต่าง

ชี้ย้อนหลังเท่านั้น — ไม่สปอยคำที่ยังไม่ได้เรียน

รัน:  py _docs/gen_synonyms.py
"""
import csv, json, os, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
rows = list(csv.DictReader(open(os.path.join(ROOT, '_docs', 'wordlist_master.csv'),
                                encoding='utf-8-sig')))

def slug(s):
    return ''.join(c for c in s.lower() if c.isalnum())

# คำไทยพ้องรูป — แปลเหมือนกันแต่คนละความหมาย ห้ามจับคู่
# เจอตอนตรวจผลรอบแรก: "ประตู" = door/goal · "วัด" = temple/measure
# "อุปสรรค" = obstacle/prefix(ไวยากรณ์) · "เหรียญ" = coin/medal
BLOCK = {('door', 'goal'), ('temple', 'measure'),
         ('barrier', 'prefix'), ('coin', 'medal'),
         # รอบตรวจโดยครูสอนภาษา: แปลไทยตรงกันแต่ความหมาย/ชนิดคำต่างจนบอกเด็กว่า "แปลเหมือน" ไม่ได้
         ('trolley', 'wheelchair'),   # รถเข็นซื้อของ ≠ รถเข็นคนพิการ
         ('melt', 'dissolve'),        # หลอมด้วยความร้อน ≠ ละลายในของเหลว
         ('match', 'tournament'),     # 1 แมตช์ ≠ ทัวร์นาเมนต์
         ('patience', 'endurance'),   # อดทนทางใจ ≠ อึดทางกาย
         ('humble', 'lowly'),         # lowly = ต่ำต้อย
         ('sorry', 'apologize'),      # adj ≠ verb
         ('accept', 'admit'),         # admit = ยอมรับว่าทำผิด
         ('setback', 'barrier'),      # เหตุถดถอย ≠ สิ่งกีดขวาง
         ('balanced', 'equilibrium'), # adj ≠ noun
         ('intuition', 'instinct'),   # ลางสังหรณ์ ≠ สัญชาตญาณ
         ('persist', 'persevere')}    # รากศัพท์คนละคำ ไม่ใช่ตระกูลเดียวกัน


def same_root(a, b):
    """คำตระกูลเดียวกัน เช่น motivate/motivating, grey/gray — ไม่ใช่คำพ้อง"""
    a, b = a.lower(), b.lower()
    n = min(len(a), len(b))
    common = 0
    for i in range(n):
        if a[i] != b[i]:
            break
        common += 1
    if common >= 4 or (abs(len(a) - len(b)) <= 2 and common >= 3):
        return True
    # สะกดต่างเล็กน้อย เช่น grey/gray — ต่างกันไม่เกิน 2 ตัวอักษร
    if min(len(a), len(b)) >= 4 and _dist(a, b) <= 2:
        return True
    return False


def _dist(a, b):
    """ระยะห่างการแก้ไข (Levenshtein)"""
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]


by_thai = collections.defaultdict(list)
for r in rows:
    by_thai[r['thai'].strip()].append((int(r['day']), r['english'].strip()))

# word (ตัวหลัง) -> {ref: คำที่เรียนไปก่อน, day: วันของคำนั้น}
M = {}
blocked = []
for thai, items in by_thai.items():
    if len(items) < 2:
        continue
    items.sort()                       # เรียงตามวัน คำแรกคือคำที่เรียนก่อน
    for i in range(1, len(items)):
        day, word = items[i]
        pday, pword = items[i - 1]
        if pday >= day:                # กันกรณีวันเดียวกัน
            continue
        pair = (pword.lower(), word.lower())
        if pair in BLOCK or pair[::-1] in BLOCK:
            blocked.append(pair)
            continue
        M[slug(word)] = {'w': pword, 'd': pday, 'th': thai,
                         # kin = คำตระกูลเดียวกัน ใช้ข้อความต่างจากคำพ้องทั่วไป
                         'kin': 1 if same_root(pword, word) else 0}

out = os.path.join(ROOT, 'js', 'synonyms.js')
with open(out, 'w', encoding='utf-8') as f:
    f.write("/* PeekaWord — หมายเหตุคำพ้องความหมาย (สร้างด้วย _docs/gen_synonyms.py)\n"
            "   อย่าแก้ไฟล์นี้ด้วยมือ · แก้ wordlist_master.csv แล้วรันสคริปต์ใหม่ */\n")
    f.write("window.PW_SYN=" + json.dumps(M, ensure_ascii=False, separators=(',', ':')) + ";\n")

print('เขียน %s · %d คำที่มีคำพ้องเรียนมาก่อน' % (out, len(M)))
kin = sum(1 for v in M.values() if v['kin'])
print('  คำพ้องความหมาย %d · คำตระกูลเดียวกัน %d' % (len(M) - kin, kin))
print('  กันออกเพราะไทยพ้องรูป %d คู่: %s' % (len(blocked), blocked))
