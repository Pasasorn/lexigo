#!/usr/bin/env python3
"""แก้คำแปลไทยที่ผิด/แคบเกินไป (จาก audit ครูภาษา) ให้ตรงกับความหมายพื้นฐาน
และระบุความหมายในเรื่องไว้ในวงเล็บ — แก้ทั้ง _docs/wordlist_master.csv และ Day page
ใช้:  py _docs\\fix_translations.py          (แก้จริง)
      py _docs\\fix_translations.py --dry    (ดูอย่างเดียว)
"""
import csv, glob, io, re, sys, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV = os.path.join(ROOT, '_docs', 'wordlist_master.csv')
DRY = '--dry' in sys.argv

# (day, english, thai เดิม, thai ใหม่)
FIX = [
    (76,  'goal',        'ประตู',                          'ประตู (ยิงประตู); เป้าหมาย'),
    (42,  'pretty',      'น่ารัก',                         'สวย'),
    (168, 'lowly',       'ถ่อมตัว',                        'ต่ำต้อย, ถ่อมตน'),
    (184, 'measure',     'วัด',                            'วัด (ขนาด)'),
    (197, 'myth',        'เทพนิยาย',                       'ตำนาน'),
    (198, 'doubt',       'สงสัยในตัวเอง',                  'สงสัย, ไม่แน่ใจ'),
    (205, 'cause',       'จุดมุ่งหมายเพื่อสังคม',           'สาเหตุ; อุดมการณ์ที่ยึดถือ'),
    (208, 'threshold',   'จุดเริ่มต้นใหม่',                 'ธรณีประตู; จุดเริ่มต้น'),
    (219, 'effect',      'เทคนิคพิเศษ',                     'ผล, ผลกระทบ (special effect = เทคนิคพิเศษ)'),
    (222, 'interest',    'ดอกเบี้ย',                        'ความสนใจ; ดอกเบี้ย'),
    (245, 'willpower',   'กำลังใจกำลังความตั้งใจ',           'พลังใจ, ความตั้งใจแน่วแน่'),
    (255, 'resume',      'ประวัติย่อสมัครงาน',              'ประวัติย่อ (สมัครงาน); กลับมาทำต่อ'),
    (257, 'minutes',     'บันทึกการประชุม',                 'นาที; รายงานการประชุม'),
    (301, 'demand',      'อุปสงค์',                         'ความต้องการ (อุปสงค์)'),
    (315, 'fossil',      'เชื้อเพลิงฟอสซิล',                'ฟอสซิล, ซากดึกดำบรรพ์ (fossil fuel = เชื้อเพลิงฟอสซิล)'),
    (319, 'footprint',   'รอยเท้าคาร์บอน',                  'รอยเท้า (carbon footprint = รอยเท้าคาร์บอน)'),
    (320, 'circular',    'เศรษฐกิจหมุนเวียน',               'เป็นวงกลม, หมุนเวียน'),
    (343, 'moderate',    'กำกับดูแลเนื้อหา',                'ปานกลาง; กำกับดูแล (เนื้อหา)'),
    (350, 'primary',     'แหล่งข้อมูลชั้นต้น',              'หลัก, ชั้นต้น'),
    (350, 'secondary',   'แหล่งข้อมูลชั้นรอง',              'รอง, ชั้นรอง'),
    (355, 'occupation',  'การยึดครอง',                      'อาชีพ; การยึดครอง'),
    (366, 'agency',      'ความสามารถกำหนดการกระทำเอง',       'หน่วยงาน; ความสามารถตัดสินใจเอง'),
    (369, 'abundance',   'ปริมาณธาตุที่พบ',                 'ความอุดมสมบูรณ์, ปริมาณมาก'),
    (390, 'scaffolding', 'โครงช่วยเรียนรู้',                'นั่งร้าน; โครงช่วยเรียนรู้'),
    (392, 'prefix',      'อุปสรรค',                         'คำอุปสรรค (ส่วนหน้าคำ)'),
    (396, 'shadow',      'พูดตามทันทีที่ได้ยิน',             'เงา; พูดตามทันที (shadowing)'),
    (406, 'silo',        'การทำงานแยกส่วนไม่คุยกัน',         'ไซโล (ยุ้งฉาง); การทำงานแยกส่วน'),
    (408, 'anchor',      'ตัวเลขตั้งต้นที่ยึดใจ',            'สมอเรือ; ตัวเลขตั้งต้นที่ยึดใจ'),
    (420, 'register',    'ระดับภาษาที่เหมาะกับสถานการณ์',    'ลงทะเบียน; ระดับภาษา'),
    (424, 'suspension',  'สะพานแขวน',                       'การแขวน (suspension bridge = สะพานแขวน)'),
    (424, 'bore',        'การเจาะอุโมงค์',                  'เจาะ; น่าเบื่อ'),
    (443, 'reckon',      'คิดว่าประเมินว่า',                 'คิดว่า, ประเมินว่า'),
    (446, 'steep',       'แช่ตัวอยู่กับภาษา',                'ชัน; แช่, จมอยู่กับ'),
    (447, 'doorway',     'ประตูสู่สิ่งใหม่',                 'ช่องประตู'),
    (29,  'grey',        'สีเทา',                           'สีเทา (สะกดแบบอังกฤษ)'),
    (41,  'gray',        'สีเทา',                           'สีเทา (= grey สะกดแบบอเมริกัน)'),
    (409, 'arbitrator',  'อนุญาโตตุลาการ',                   'ผู้ชี้ขาดข้อพิพาท'),
    (311, 'arbitration', 'อนุญาโตตุลาการ',                   'การชี้ขาดข้อพิพาท (อนุญาโตตุลาการ)'),
]

# แก้ไวยากรณ์ในเรื่อง (day, เดิม, ใหม่)
GRAMMAR = [
    (168, 'she <span class="vocab">appreciate</span> ', 'she <span class="vocab">appreciates</span> '),
    (168, 'she appreciate.', 'she appreciates.'),
    (168, 'she appreciate ', 'she appreciates '),
]

def day_file(d):
    m = glob.glob(os.path.join(ROOT, 'Level*', f'Day{d}_*.html'))
    assert len(m) == 1, (d, m)
    return m[0]

ok = bad = 0
# --- CSV ---
with io.open(CSV, encoding='utf-8-sig') as f:
    rows = list(csv.reader(f))
hdr, body = rows[0], rows[1:]
for d, en, old, new in FIX:
    hit = [r for r in body if r[0] == str(d) and r[3] == en]
    if len(hit) != 1 or hit[0][4] != old:
        print('CSV ไม่ตรง:', d, en, hit[0][4] if hit else None); bad += 1; continue
    hit[0][4] = new; ok += 1
if not DRY:
    with io.open(CSV, 'w', encoding='utf-8-sig', newline='') as f:
        w = csv.writer(f); w.writerow(hdr); w.writerows(body)
print(f'CSV: แก้ {ok} / ไม่ตรง {bad}')

# --- Day pages ---
ok = bad = 0
for d, en, old, new in FIX:
    p = day_file(d)
    s = io.open(p, encoding='utf-8').read()
    pat = f"{{e:'{en}',t:'{old}',"
    if s.count(pat) != 1:
        print('Day ไม่ตรง:', d, en, s.count(pat)); bad += 1; continue
    s = s.replace(pat, f"{{e:'{en}',t:'{new}',")
    if not DRY: io.open(p, 'w', encoding='utf-8', newline='').write(s)
    ok += 1
for d, old, new in GRAMMAR:
    p = day_file(d)
    s = io.open(p, encoding='utf-8').read()
    n = s.count(old)
    if n:
        s = s.replace(old, new)
        if not DRY: io.open(p, 'w', encoding='utf-8', newline='').write(s)
        print(f'Day{d} ไวยากรณ์: {old!r} ×{n}')
print(f'Day pages: แก้ {ok} / ไม่ตรง {bad}')
