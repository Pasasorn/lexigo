# -*- coding: utf-8 -*-
"""
สร้างภาพประกอบคำศัพท์เป็น SVG (วาดเองทั้งหมด ไม่ลอกใคร = ไม่มีปัญหาลิขสิทธิ์)
ผลลัพธ์:
  img/words/<word>.svg        ← ไฟล์ภาพพร้อมใช้
  _docs/images/gallery.html   ← หน้ารวมดูทั้งหมด แบ่งตาม Level/Day

วิธีรัน:  python _docs/gen_svg.py
"""
import csv, os, json, html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT  = os.path.join(ROOT, 'img', 'words')
GAL  = os.path.join(ROOT, '_docs', 'images')

# ---------- จานสี (โทนเดียวกันทั้งชุด เด็กดูไม่ลายตา) ----------
P = dict(
    sky='#CFE9F7', grass='#A9DC8E', soil='#C59A6D', sun='#FFD166',
    ink='#3D4A5C', white='#FFFFFF', warm='#F4A261', red='#E76F51',
    pink='#F7A8B8', blue='#6CB4EE', deep='#2E86C1', green='#5FB06B',
    purple='#B39DDB', yellow='#F9DC5C', gray='#C9D1D9', brown='#A9744F',
)

def wrap(body, bg='sky'):
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" '
            'width="100" height="100" role="img">'
            '<rect width="100" height="100" rx="18" fill="%s"/>%s</svg>' % (P[bg], body))

# ---------- ชิ้นส่วนที่ใช้ซ้ำ ----------
def ground(c='grass', y=74):
    return '<path d="M0 %d h100 v26 H0 Z" fill="%s"/>' % (y, P[c])

def eyes(x1, x2, y, r=3.2, c='ink'):
    return ('<circle cx="%s" cy="%s" r="%s" fill="%s"/><circle cx="%s" cy="%s" r="%s" fill="%s"/>'
            '<circle cx="%s" cy="%s" r="1.1" fill="#fff"/><circle cx="%s" cy="%s" r="1.1" fill="#fff"/>'
            % (x1, y, r, P[c], x2, y, r, P[c], x1+1, y-1, x2+1, y-1))

def smile(cx, cy, w=10, c='ink'):
    return ('<path d="M%s %s q%s %s %s 0" stroke="%s" stroke-width="2.2" fill="none" '
            'stroke-linecap="round"/>' % (cx-w/2, cy, w/2, w*0.62, w, P[c]))

def figure(x, y, s, arm, leg, c='red'):
    """คนแบบเรียบง่าย: arm/leg = (x1,y1,x2,y2) ปลายแขนปลายขา"""
    g = '<circle cx="%s" cy="%s" r="%s" fill="%s"/>' % (x, y, 6*s, P['warm'])
    g += '<path d="M%s %s v%s" stroke="%s" stroke-width="%s" stroke-linecap="round"/>' % (
        x, y+6*s, 18*s, P[c], 6*s)
    for (ax, ay) in arm:
        g += '<path d="M%s %s L%s %s" stroke="%s" stroke-width="%s" stroke-linecap="round"/>' % (
            x, y+11*s, ax, ay, P['warm'], 3.6*s)
    for (lx, ly) in leg:
        g += '<path d="M%s %s L%s %s" stroke="%s" stroke-width="%s" stroke-linecap="round"/>' % (
            x, y+24*s, lx, ly, P['ink'], 4*s)
    return g

# ---------- ภาพแต่ละคำ ----------
A = {}

A['cat'] = wrap(ground() +
    '<path d="M36 44 L33 28 L47 38 Z" fill="%(warm)s"/>'
    '<path d="M64 44 L67 28 L53 38 Z" fill="%(warm)s"/>'
    '<path d="M38 41 L36.5 33 L43.5 38 Z" fill="%(pink)s"/>'
    '<path d="M62 41 L63.5 33 L56.5 38 Z" fill="%(pink)s"/>'
    '<circle cx="50" cy="56" r="20" fill="%(warm)s"/>' % P
    + eyes(43, 57, 53)
    + '<path d="M50 60 l-3 3 h6 Z" fill="%(pink)s"/>' % P
    + smile(45, 65, 5) + smile(50, 65, 5)
    + '<g stroke="%(ink)s" stroke-width="1.4" stroke-linecap="round" opacity=".55">'
      '<path d="M28 58 h8"/><path d="M28 63 h8"/><path d="M72 58 h-8"/><path d="M72 63 h-8"/></g>' % P)

A['dog'] = wrap(ground() +
    '<ellipse cx="30" cy="54" rx="8" ry="15" fill="%(brown)s"/>'
    '<ellipse cx="70" cy="54" rx="8" ry="15" fill="%(brown)s"/>'
    '<circle cx="50" cy="52" r="20" fill="%(warm)s"/>'
    '<ellipse cx="50" cy="63" rx="11" ry="9" fill="%(white)s"/>' % P
    + eyes(43, 57, 48)
    + '<ellipse cx="50" cy="59" rx="4" ry="3" fill="%(ink)s"/>' % P
    + '<path d="M50 62 v4" stroke="%(ink)s" stroke-width="1.8"/>' % P
    + smile(45, 66, 5) + smile(50, 66, 5)
    + '<path d="M50 70 q4 8 0 9 q-4 -1 0 -9" fill="%(pink)s"/>' % P)

A['bird'] = wrap(ground() +
    '<ellipse cx="48" cy="52" rx="20" ry="16" fill="%(blue)s"/>'
    '<circle cx="64" cy="42" r="11" fill="%(blue)s"/>'
    '<path d="M74 42 l10 4 l-10 4 Z" fill="%(sun)s"/>'
    '<path d="M28 46 l-14 -8 l6 14 Z" fill="%(deep)s"/>'
    '<ellipse cx="46" cy="52" rx="10" ry="7" fill="%(deep)s" opacity=".55"/>'
    '<path d="M44 68 v6 M54 68 v6" stroke="%(sun)s" stroke-width="2.6" stroke-linecap="round"/>' % P
    + eyes(66, 66, 40, 2.4))

A['fish'] = wrap(
    '<rect width="100" height="100" rx="18" fill="%(blue)s"/>'
    '<path d="M22 50 L6 36 v28 Z" fill="%(red)s"/>'
    '<ellipse cx="54" cy="50" rx="30" ry="19" fill="%(warm)s"/>'
    '<path d="M50 31 q8 -10 14 2 Z" fill="%(red)s"/>'
    '<path d="M34 50 q10 10 0 16" stroke="%(red)s" stroke-width="2.4" fill="none"/>'
    '<circle cx="70" cy="45" r="3.4" fill="%(ink)s"/><circle cx="71" cy="44" r="1.2" fill="#fff"/>'
    '<g fill="#fff" opacity=".7"><circle cx="86" cy="28" r="3.4"/><circle cx="78" cy="19" r="2.2"/></g>' % P,
    bg='blue')

A['big'] = wrap(ground() +
    '<circle cx="36" cy="48" r="24" fill="%(deep)s"/>'
    '<circle cx="36" cy="48" r="14" fill="%(blue)s"/>'
    '<circle cx="80" cy="64" r="8" fill="%(gray)s"/>'
    '<path d="M12 84 h48" stroke="%(ink)s" stroke-width="2" stroke-linecap="round"/>'
    '<path d="M12 80 v8 M60 80 v8" stroke="%(ink)s" stroke-width="2" stroke-linecap="round"/>' % P)

A['small'] = wrap(ground() +
    '<circle cx="34" cy="56" r="16" fill="%(gray)s" opacity=".55"/>'
    '<circle cx="76" cy="60" r="11" fill="%(red)s"/>'
    '<circle cx="76" cy="60" r="5" fill="%(sun)s"/>'
    '<path d="M65 82 h22" stroke="%(ink)s" stroke-width="2" stroke-linecap="round"/>'
    '<path d="M65 78 v8 M87 78 v8" stroke="%(ink)s" stroke-width="2" stroke-linecap="round"/>' % P)

A['garden'] = wrap(ground(y=66) +
    '<g stroke="%(white)s" stroke-width="4" stroke-linecap="round">'
    '<path d="M14 66 v-14"/><path d="M30 66 v-18"/><path d="M46 66 v-14"/>'
    '<path d="M8 54 h44"/></g>'
    '<circle cx="68" cy="44" r="9" fill="%(pink)s"/><circle cx="68" cy="44" r="4" fill="%(sun)s"/>'
    '<path d="M68 53 v13" stroke="%(green)s" stroke-width="3"/>'
    '<circle cx="86" cy="52" r="7" fill="%(purple)s"/><circle cx="86" cy="52" r="3" fill="%(sun)s"/>'
    '<path d="M86 59 v7" stroke="%(green)s" stroke-width="3"/>'
    '<circle cx="24" cy="22" r="10" fill="%(sun)s"/>' % P)

A['flower'] = wrap(ground() +
    '<path d="M50 78 V46" stroke="%(green)s" stroke-width="4" stroke-linecap="round"/>'
    '<path d="M50 62 q-14 -6 -16 6 q14 4 16 -6" fill="%(green)s"/>'
    '<path d="M50 56 q14 -6 16 6 q-14 4 -16 -6" fill="%(green)s"/>'
    '<g fill="%(pink)s"><circle cx="50" cy="28" r="9"/><circle cx="38" cy="38" r="9"/>'
    '<circle cx="62" cy="38" r="9"/><circle cx="43" cy="50" r="9"/><circle cx="57" cy="50" r="9"/></g>'
    '<circle cx="50" cy="40" r="8" fill="%(sun)s"/>' % P)

A['tree'] = wrap(ground() +
    '<path d="M46 78 V48 h8 v30 Z" fill="%(brown)s"/>'
    '<circle cx="50" cy="38" r="18" fill="%(green)s"/>'
    '<circle cx="34" cy="48" r="13" fill="%(green)s"/>'
    '<circle cx="66" cy="48" r="13" fill="%(green)s"/>'
    '<circle cx="50" cy="52" r="12" fill="%(grass)s" opacity=".8"/>'
    '<circle cx="40" cy="34" r="3" fill="%(red)s"/><circle cx="62" cy="42" r="3" fill="%(red)s"/>' % P)

A['grass'] = wrap(ground(y=70) +
    '<g stroke="%(green)s" stroke-width="4" stroke-linecap="round" fill="none">'
    '<path d="M20 72 q-4 -16 2 -24"/><path d="M34 72 q2 -20 10 -26"/>'
    '<path d="M50 72 q-2 -22 -8 -28"/><path d="M64 72 q4 -18 12 -24"/>'
    '<path d="M80 72 q-3 -16 -10 -22"/></g>'
    '<circle cx="78" cy="24" r="9" fill="%(sun)s"/>' % P)

A['run'] = wrap(ground() +
    figure(52, 34, 1, [(70, 40), (36, 52)], [(70, 76), (36, 72)]) +
    '<g stroke="%(ink)s" stroke-width="2.4" stroke-linecap="round" opacity=".4">'
    '<path d="M14 40 h12"/><path d="M10 50 h16"/><path d="M14 60 h12"/></g>' % P)

A['happy'] = wrap(
    '<rect width="100" height="100" rx="18" fill="%(sun)s"/>'
    '<circle cx="50" cy="50" r="34" fill="%(yellow)s"/>' % P
    + '<path d="M34 42 q6 -7 12 0" stroke="%(ink)s" stroke-width="3" fill="none" stroke-linecap="round"/>'
      '<path d="M54 42 q6 -7 12 0" stroke="%(ink)s" stroke-width="3" fill="none" stroke-linecap="round"/>' % P
    + '<path d="M34 58 q16 18 32 0" fill="%(ink)s"/>' % P
    + '<circle cx="28" cy="56" r="5" fill="%(pink)s" opacity=".75"/>'
      '<circle cx="72" cy="56" r="5" fill="%(pink)s" opacity=".75"/>' % P, bg='sun')

A['farm'] = wrap(ground() +
    '<path d="M18 74 V48 h40 v26 Z" fill="%(red)s"/>'
    '<path d="M14 48 L38 30 L62 48 Z" fill="%(ink)s"/>'
    '<path d="M32 74 V58 h12 v16 Z" fill="%(brown)s"/>'
    '<path d="M70 74 V44 a8 8 0 0 1 16 0 v30 Z" fill="%(gray)s"/>'
    '<circle cx="78" cy="26" r="9" fill="%(sun)s"/>' % P)

A['cow'] = wrap(ground() +
    '<path d="M30 40 q-8 -8 -2 -12 q8 2 8 10 Z" fill="%(gray)s"/>'
    '<path d="M70 40 q8 -8 2 -12 q-8 2 -8 10 Z" fill="%(gray)s"/>'
    '<ellipse cx="50" cy="52" rx="22" ry="20" fill="%(white)s"/>'
    '<ellipse cx="38" cy="44" rx="7" ry="5" fill="%(ink)s" opacity=".8"/>'
    '<ellipse cx="64" cy="46" rx="5" ry="4" fill="%(ink)s" opacity=".8"/>'
    '<ellipse cx="50" cy="64" rx="13" ry="9" fill="%(pink)s"/>'
    '<circle cx="45" cy="63" r="1.8" fill="%(ink)s"/><circle cx="55" cy="63" r="1.8" fill="%(ink)s"/>' % P
    + eyes(42, 60, 50, 2.8))

A['horse'] = wrap(ground() +
    # แผงคอ
    '<path d="M62 24 q14 6 12 24 q-2 14 -8 20 l-10 -6 q8 -16 6 -38 Z" fill="%(ink)s"/>'
    # หัว + คอ ทรงสามเหลี่ยมเอียง → อ่านออกว่าเป็นม้า
    '<path d="M58 26 q10 2 10 14 l-2 26 q-1 10 -12 10 q-10 0 -11 -10 '
    'l-2 -12 q-1 -6 -8 -10 l-14 -8 q-4 -3 0 -6 l22 -6 q9 -3 17 2 Z" fill="%(brown)s"/>'
    # หู
    '<path d="M57 26 q-2 -11 5 -11 q4 4 3 12 Z" fill="%(brown)s"/>'
    '<path d="M58 25 q0 -7 3 -8 q2 3 1 8 Z" fill="%(pink)s"/>'
    # ปาก/จมูก
    '<ellipse cx="25" cy="48" rx="9" ry="7" fill="%(warm)s"/>'
    '<ellipse cx="22" cy="47" rx="2" ry="2.6" fill="%(ink)s"/>'
    '<path d="M20 53 q6 3 11 0" stroke="%(ink)s" stroke-width="1.6" fill="none" stroke-linecap="round"/>' % P
    + eyes(49, 49, 40, 3))

A['sheep'] = wrap(ground() +
    '<path d="M40 64 v12 M56 64 v12" stroke="%(ink)s" stroke-width="4.4" stroke-linecap="round"/>'
    '<g fill="%(white)s"><circle cx="38" cy="46" r="12"/><circle cx="54" cy="42" r="13"/>'
    '<circle cx="64" cy="54" r="12"/><circle cx="42" cy="60" r="13"/>'
    '<circle cx="58" cy="62" r="12"/><circle cx="51" cy="52" r="15"/></g>'
    '<ellipse cx="28" cy="50" rx="10" ry="11" fill="%(ink)s"/>'
    '<path d="M28 39 q-3 -9 4 -8 q3 3 1 9 Z" fill="%(white)s"/>'
    '<ellipse cx="19" cy="55" rx="5" ry="6" fill="%(ink)s"/>'
    '<ellipse cx="18" cy="56" rx="1.4" ry="1.8" fill="%(gray)s"/>' % P
    + eyes(25, 32, 48, 2.2, 'white'))

A['eat'] = wrap(
    '<rect width="100" height="100" rx="18" fill="%(grass)s"/>'
    '<circle cx="50" cy="56" r="26" fill="%(white)s"/>'
    '<circle cx="50" cy="56" r="18" fill="%(gray)s" opacity=".35"/>'
    '<circle cx="46" cy="52" r="6" fill="%(red)s"/><circle cx="57" cy="58" r="5" fill="%(green)s"/>'
    '<circle cx="48" cy="63" r="4.5" fill="%(sun)s"/>'
    '<g stroke="%(ink)s" stroke-width="2.6" stroke-linecap="round">'
    '<path d="M16 34 v34"/><path d="M16 34 v10 M12 34 v10 M20 34 v10"/>'
    '<path d="M84 34 v34"/></g>'
    '<ellipse cx="84" cy="38" rx="5" ry="7" fill="%(ink)s"/>' % P, bg='grass')

A['walk'] = wrap(ground() +
    figure(50, 34, 1, [(62, 54), (38, 54)], [(60, 76), (40, 76)]) +
    '<g fill="%(ink)s" opacity=".25"><ellipse cx="26" cy="84" rx="5" ry="2.4"/>'
    '<ellipse cx="40" cy="88" rx="5" ry="2.4"/></g>' % P)

A['duck'] = wrap(
    '<rect width="100" height="100" rx="18" fill="%(sky)s"/>'
    '<path d="M0 72 h100 v28 H0 Z" fill="%(blue)s"/>'
    '<ellipse cx="48" cy="62" rx="24" ry="15" fill="%(white)s"/>'
    '<circle cx="66" cy="44" r="12" fill="%(white)s"/>'
    '<path d="M76 44 q12 0 10 6 q-6 2 -10 -2 Z" fill="%(warm)s"/>'
    '<path d="M24 56 l-12 -6 l4 12 Z" fill="%(gray)s"/>'
    '<g stroke="#fff" stroke-width="2" opacity=".8" fill="none">'
    '<path d="M10 82 q6 -4 12 0 q6 4 12 0"/><path d="M62 88 q6 -4 12 0 q6 4 12 0"/></g>' % P
    + eyes(68, 68, 42, 2.4))

A['swim'] = wrap(
    '<rect width="100" height="100" rx="18" fill="%(sky)s"/>'
    '<path d="M0 60 h100 v40 H0 Z" fill="%(blue)s" opacity=".9"/>'
    '<circle cx="42" cy="50" r="8" fill="%(warm)s"/>'
    '<path d="M48 54 q18 2 26 -6" stroke="%(red)s" stroke-width="7" fill="none" stroke-linecap="round"/>'
    '<path d="M38 46 q-10 -12 -18 -4" stroke="%(warm)s" stroke-width="4.4" fill="none" stroke-linecap="round"/>'
    '<g stroke="#fff" stroke-width="2.4" opacity=".85" fill="none">'
    '<path d="M6 68 q7 -5 14 0 q7 5 14 0"/><path d="M56 74 q7 -5 14 0 q7 5 14 0"/>'
    '<path d="M20 86 q7 -5 14 0 q7 5 14 0"/></g>' % P)

A['water'] = wrap(
    '<rect width="100" height="100" rx="18" fill="%(sky)s"/>'
    '<path d="M50 16 q20 26 20 38 a20 20 0 0 1 -40 0 q0 -12 20 -38 Z" fill="%(deep)s"/>'
    '<path d="M50 26 q12 20 12 28 a12 12 0 0 1 -24 0 q0 -8 12 -28 Z" fill="%(blue)s"/>'
    '<ellipse cx="44" cy="58" rx="4" ry="6" fill="#fff" opacity=".6"/>'
    '<g stroke="%(deep)s" stroke-width="2.4" fill="none" opacity=".5">'
    '<path d="M18 86 q8 -5 16 0 q8 5 16 0 q8 -5 16 0 q8 5 16 0"/></g>' % P)

A['fly'] = wrap(
    '<rect width="100" height="100" rx="18" fill="%(sky)s"/>'
    '<g fill="#fff" opacity=".85"><circle cx="22" cy="26" r="9"/><circle cx="32" cy="26" r="11"/>'
    '<circle cx="43" cy="27" r="8"/><circle cx="74" cy="66" r="8"/><circle cx="84" cy="66" r="10"/></g>'
    '<path d="M48 56 q-30 -30 -40 -8 q18 6 40 8 Z" fill="%(white)s" stroke="%(deep)s" stroke-width="1.6"/>'
    '<path d="M48 56 q30 -30 40 -8 q-18 6 -40 8 Z" fill="%(white)s" stroke="%(deep)s" stroke-width="1.6"/>'
    '<ellipse cx="48" cy="60" rx="15" ry="11" fill="%(deep)s"/>'
    '<circle cx="60" cy="54" r="8" fill="%(deep)s"/>'
    '<path d="M67 54 l10 3 l-10 3 Z" fill="%(sun)s"/>'
    '<path d="M34 64 l-12 6 l12 2 Z" fill="%(blue)s"/>'
    '<circle cx="62" cy="52" r="2.4" fill="#fff"/><circle cx="62" cy="52" r="1.2" fill="%(ink)s"/>' % P)

A['fast'] = wrap(
    '<rect width="100" height="100" rx="18" fill="%(sun)s"/>'
    '<path d="M56 14 L28 56 h18 L38 88 L72 42 H52 Z" fill="%(white)s" stroke="%(ink)s" stroke-width="2.4"/>'
    '<g stroke="%(ink)s" stroke-width="3" stroke-linecap="round" opacity=".45">'
    '<path d="M8 30 h14"/><path d="M4 46 h18"/><path d="M8 62 h14"/>'
    '<path d="M80 34 h14"/><path d="M78 52 h18"/></g>' % P, bg='sun')

A['slow'] = wrap(ground() +
    '<ellipse cx="44" cy="70" rx="26" ry="7" fill="%(grass)s"/>'
    '<path d="M24 70 q-6 -2 -4 -10 q2 -6 8 -4" fill="none" stroke="%(green)s" stroke-width="7" stroke-linecap="round"/>'
    '<circle cx="54" cy="52" r="18" fill="%(brown)s"/>'
    '<path d="M54 52 a10 10 0 1 0 8 6" fill="none" stroke="%(sun)s" stroke-width="4"/>'
    '<path d="M54 52 a16 16 0 1 1 -14 10" fill="none" stroke="%(sun)s" stroke-width="3.4"/>'
    '<g stroke="%(green)s" stroke-width="2.6" stroke-linecap="round">'
    '<path d="M22 58 l-4 -8"/><path d="M28 56 l2 -9"/></g>'
    '<circle cx="18" cy="49" r="2" fill="%(ink)s"/><circle cx="30" cy="46" r="2" fill="%(ink)s"/>'
    '<g stroke="%(ink)s" stroke-width="2" stroke-linecap="round" opacity=".35">'
    '<path d="M80 40 h10"/><path d="M84 48 h8"/></g>' % P)

A['butterfly'] = wrap(
    '<rect width="100" height="100" rx="18" fill="%(grass)s"/>'
    '<path d="M48 50 q-28 -28 -34 -6 q-4 18 34 10 Z" fill="%(purple)s"/>'
    '<path d="M52 50 q28 -28 34 -6 q4 18 -34 10 Z" fill="%(purple)s"/>'
    '<path d="M48 54 q-22 24 -28 6 q-2 -14 28 -10 Z" fill="%(pink)s"/>'
    '<path d="M52 54 q22 24 28 6 q2 -14 -28 -10 Z" fill="%(pink)s"/>'
    '<circle cx="28" cy="40" r="4" fill="%(sun)s"/><circle cx="72" cy="40" r="4" fill="%(sun)s"/>'
    '<ellipse cx="50" cy="54" rx="4" ry="20" fill="%(ink)s"/>'
    '<path d="M48 36 q-8 -10 -14 -12 M52 36 q8 -10 14 -12" stroke="%(ink)s" stroke-width="2" fill="none" stroke-linecap="round"/>'
    '<circle cx="34" cy="23" r="2.4" fill="%(ink)s"/><circle cx="66" cy="23" r="2.4" fill="%(ink)s"/>' % P, bg='grass')

A['insect'] = wrap(ground() +
    '<g stroke="%(ink)s" stroke-width="2.6" stroke-linecap="round">'
    '<path d="M32 50 l-12 -6"/><path d="M30 60 l-14 2"/><path d="M34 68 l-12 8"/>'
    '<path d="M68 50 l12 -6"/><path d="M70 60 l14 2"/><path d="M66 68 l12 8"/></g>'
    '<circle cx="50" cy="58" r="22" fill="%(red)s"/>'
    '<path d="M50 36 v44" stroke="%(ink)s" stroke-width="2.6"/>'
    '<g fill="%(ink)s"><circle cx="40" cy="52" r="4.4"/><circle cx="60" cy="52" r="4.4"/>'
    '<circle cx="42" cy="68" r="3.6"/><circle cx="58" cy="68" r="3.6"/></g>'
    '<path d="M36 40 a16 16 0 0 1 28 0 Z" fill="%(ink)s"/>'
    '<path d="M42 30 l-5 -9 M58 30 l5 -9" stroke="%(ink)s" stroke-width="2.2" stroke-linecap="round"/>'
    '<circle cx="37" cy="20" r="2.4" fill="%(ink)s"/><circle cx="63" cy="20" r="2.4" fill="%(ink)s"/>' % P)

A['color'] = wrap(
    '<rect width="100" height="100" rx="18" fill="%(white)s"/>'
    '<path d="M50 18 a32 32 0 1 0 0 64 a9 9 0 0 1 0 -18 a7 7 0 0 0 0 -14 a22 22 0 0 1 0 -32 Z" '
    'fill="%(gray)s" opacity=".3"/>'
    '<circle cx="36" cy="32" r="7" fill="%(red)s"/><circle cx="26" cy="48" r="7" fill="%(sun)s"/>'
    '<circle cx="30" cy="66" r="7" fill="%(green)s"/><circle cx="46" cy="74" r="7" fill="%(blue)s"/>'
    '<circle cx="56" cy="28" r="7" fill="%(purple)s"/>'
    '<path d="M78 76 l14 -40 l6 2 l-12 42 Z" fill="%(brown)s"/>'
    '<path d="M78 76 l8 2 l-10 6 Z" fill="%(ink)s"/>' % P, bg='white')

A['beautiful'] = wrap(
    '<rect width="100" height="100" rx="18" fill="%(purple)s"/>'
    '<g fill="%(pink)s"><circle cx="50" cy="40" r="10"/><circle cx="37" cy="52" r="10"/>'
    '<circle cx="63" cy="52" r="10"/><circle cx="43" cy="65" r="10"/><circle cx="57" cy="65" r="10"/></g>'
    '<circle cx="50" cy="54" r="9" fill="%(sun)s"/>'
    '<g fill="%(white)s"><path d="M22 20 l3 8 l8 3 l-8 3 l-3 8 l-3 -8 l-8 -3 l8 -3 Z"/>'
    '<path d="M82 30 l2.4 6 l6 2.4 l-6 2.4 l-2.4 6 l-2.4 -6 l-6 -2.4 l6 -2.4 Z"/>'
    '<path d="M76 74 l2 5 l5 2 l-5 2 l-2 5 l-2 -5 l-5 -2 l5 -2 Z"/></g>' % P, bg='purple')

A['sit'] = wrap(ground() +
    '<path d="M62 44 v34" stroke="%(brown)s" stroke-width="5" stroke-linecap="round"/>'
    '<path d="M42 62 h22" stroke="%(brown)s" stroke-width="6" stroke-linecap="round"/>'
    '<path d="M44 64 v14 M62 64 v14" stroke="%(brown)s" stroke-width="4.4" stroke-linecap="round"/>'
    '<circle cx="48" cy="38" r="7" fill="%(warm)s"/>'
    '<path d="M48 45 v14" stroke="%(red)s" stroke-width="7" stroke-linecap="round"/>'
    '<path d="M48 58 h-14 v12" stroke="%(ink)s" stroke-width="4.4" fill="none" stroke-linecap="round"/>'
    '<path d="M48 50 l-12 4" stroke="%(warm)s" stroke-width="3.6" stroke-linecap="round"/>' % P)

A['look'] = wrap(
    '<rect width="100" height="100" rx="18" fill="%(sky)s"/>'
    '<path d="M10 50 q40 -32 80 0 q-40 32 -80 0 Z" fill="%(white)s" stroke="%(ink)s" stroke-width="2.6"/>'
    '<circle cx="50" cy="50" r="17" fill="%(blue)s"/>'
    '<circle cx="50" cy="50" r="8" fill="%(ink)s"/>'
    '<circle cx="55" cy="44" r="4" fill="#fff" opacity=".9"/>'
    '<g stroke="%(ink)s" stroke-width="2.6" stroke-linecap="round" opacity=".6">'
    '<path d="M50 24 v-8"/><path d="M24 34 l-6 -5"/><path d="M76 34 l6 -5"/></g>' % P)

A['river'] = wrap(
    '<rect width="100" height="100" rx="18" fill="%(grass)s"/>'
    '<path d="M28 0 q22 26 -2 50 q-22 24 4 50 h40 q-24 -26 -2 -50 q22 -26 0 -50 Z" fill="%(blue)s"/>'
    '<g stroke="#fff" stroke-width="2" opacity=".65" fill="none">'
    '<path d="M36 18 q8 6 14 0"/><path d="M28 48 q8 6 14 0"/><path d="M42 78 q8 6 14 0"/></g>'
    '<circle cx="12" cy="20" r="6" fill="%(green)s"/><circle cx="88" cy="36" r="7" fill="%(green)s"/>'
    '<circle cx="86" cy="80" r="6" fill="%(green)s"/><circle cx="10" cy="72" r="7" fill="%(green)s"/>' % P,
    bg='grass')

A['frog'] = wrap(
    '<rect width="100" height="100" rx="18" fill="%(sky)s"/>'
    '<ellipse cx="50" cy="80" rx="34" ry="8" fill="%(green)s" opacity=".5"/>'
    '<circle cx="34" cy="38" r="12" fill="%(green)s"/><circle cx="66" cy="38" r="12" fill="%(green)s"/>'
    '<circle cx="34" cy="38" r="7" fill="#fff"/><circle cx="66" cy="38" r="7" fill="#fff"/>'
    '<circle cx="34" cy="39" r="3.4" fill="%(ink)s"/><circle cx="66" cy="39" r="3.4" fill="%(ink)s"/>'
    '<ellipse cx="50" cy="60" rx="26" ry="20" fill="%(green)s"/>'
    '<path d="M32 60 q18 16 36 0" stroke="%(ink)s" stroke-width="2.6" fill="none" stroke-linecap="round"/>'
    '<ellipse cx="50" cy="70" rx="12" ry="7" fill="%(grass)s"/>'
    '<g fill="%(green)s"><ellipse cx="24" cy="76" rx="9" ry="5"/><ellipse cx="76" cy="76" rx="9" ry="5"/></g>' % P)

A['jump'] = wrap(ground() +
    figure(50, 26, .95, [(66, 16), (34, 16)], [(62, 60), (38, 60)]) +
    '<path d="M22 78 q28 -34 56 0" stroke="%(ink)s" stroke-width="2.2" fill="none" '
    'stroke-dasharray="4 4" opacity=".45"/>'
    '<ellipse cx="50" cy="86" rx="12" ry="3" fill="%(ink)s" opacity=".2"/>' % P)

A['catch'] = wrap(
    '<rect width="100" height="100" rx="18" fill="%(sky)s"/>'
    # ลูกบอลกำลังตกลงมา
    '<circle cx="50" cy="34" r="14" fill="%(red)s"/>'
    '<path d="M40 25 q10 9 0 18 M60 25 q-10 9 0 18" stroke="#fff" stroke-width="2" fill="none"/>'
    '<g stroke="%(ink)s" stroke-width="2.2" stroke-linecap="round" opacity=".35">'
    '<path d="M50 10 v8"/><path d="M33 15 l4 7"/><path d="M67 15 l-4 7"/></g>'
    # มือซ้าย-ขวา ประกบรับ (นิ้วทั้ง 4 เท่ากัน ไม่กำมือ)
    '<g fill="%(warm)s" stroke="%(ink)s" stroke-width="2" stroke-linejoin="round">'
    '<path d="M14 88 q-4 -22 10 -28 l4 -14 q1 -5 5 -4 q4 1 3 6 l-2 12 l4 -2 l2 -13 '
    'q1 -5 5 -4 q4 1 3 6 l-2 12 l3 -1 l1 -10 q1 -5 5 -4 q4 1 3 6 l-2 20 q-2 14 -16 18 Z"/>'
    '<path d="M86 88 q4 -22 -10 -28 l-4 -14 q-1 -5 -5 -4 q-4 1 -3 6 l2 12 l-4 -2 l-2 -13 '
    'q-1 -5 -5 -4 q-4 1 -3 6 l2 12 l-3 -1 l-1 -10 q-1 -5 -5 -4 q-4 1 -3 6 l2 20 q2 14 16 18 Z"/>'
    '</g>' % P)

A['long'] = wrap(
    '<rect width="100" height="100" rx="18" fill="%(white)s"/>'
    '<rect x="8" y="40" width="84" height="16" rx="8" fill="%(blue)s"/>'
    '<path d="M10 70 h80" stroke="%(ink)s" stroke-width="2.4" stroke-linecap="round"/>'
    '<path d="M10 64 v12 M90 64 v12" stroke="%(ink)s" stroke-width="2.4" stroke-linecap="round"/>'
    '<path d="M16 70 l6 -4 v8 Z M84 70 l-6 -4 v8 Z" fill="%(ink)s"/>'
    '<rect x="8" y="22" width="24" height="10" rx="5" fill="%(gray)s" opacity=".5"/>' % P, bg='white')

A['short'] = wrap(
    '<rect width="100" height="100" rx="18" fill="%(white)s"/>'
    '<rect x="34" y="40" width="32" height="16" rx="8" fill="%(red)s"/>'
    '<path d="M36 70 h28" stroke="%(ink)s" stroke-width="2.4" stroke-linecap="round"/>'
    '<path d="M36 64 v12 M64 64 v12" stroke="%(ink)s" stroke-width="2.4" stroke-linecap="round"/>'
    '<path d="M42 70 l6 -4 v8 Z M58 70 l-6 -4 v8 Z" fill="%(ink)s"/>'
    '<rect x="8" y="22" width="84" height="10" rx="5" fill="%(gray)s" opacity=".5"/>' % P, bg='white')


# ---------- เขียนไฟล์ ----------
def main():
    os.makedirs(OUT, exist_ok=True)
    os.makedirs(GAL, exist_ok=True)
    rows = list(csv.DictReader(open(os.path.join(ROOT, '_docs', 'wordlist_master.csv'),
                                    encoding='utf-8-sig')))
    done = []
    for w, svg in A.items():
        p = os.path.join(OUT, w + '.svg')
        open(p, 'w', encoding='utf-8').write(svg)
        done.append(w)

    # จับคู่ข้อมูลคำ
    info = {}
    for r in rows:
        k = r['english'].lower()
        if k in A and k not in info:
            info[k] = r

    # จัดกลุ่มตาม CEFR → Day
    groups = {}
    for w in done:
        r = info.get(w, {})
        groups.setdefault(r.get('cefr', 'A1'), {}).setdefault(int(r.get('day', 0) or 0), []).append(w)

    cards_html = []
    for cefr in ['A1', 'A2', 'B1', 'B2']:
        if cefr not in groups:
            continue
        cards_html.append('<h2 class="lv lv-%s">%s <span>· %d คำ</span></h2>'
                          % (cefr, cefr, sum(len(v) for v in groups[cefr].values())))
        for day in sorted(groups[cefr]):
            cards_html.append('<h3 class="day">Day %d</h3><div class="grid">' % day)
            for w in groups[cefr][day]:
                r = info.get(w, {})
                cards_html.append(
                    '<figure class="c" data-w="%s">%s'
                    '<figcaption><b>%s</b><i>%s</i><span>%s</span>'
                    '<code>%s.svg</code></figcaption>'
                    '<button onclick="dl(\'%s\')">⬇ SVG</button>'
                    '<button onclick="png(\'%s\')">⬇ PNG</button></figure>'
                    % (w, A[w], html.escape(w), html.escape(r.get('ipa', '')),
                       html.escape(r.get('thai', '')), w, w, w))
            cards_html.append('</div>')

    open(os.path.join(GAL, 'gallery.html'), 'w', encoding='utf-8').write(
        TPL.replace('{{CARDS}}', '\n'.join(cards_html)).replace('{{N}}', str(len(done))))
    print('เขียน SVG %d ไฟล์ → img/words/' % len(done))
    print('หน้ารวม → _docs/images/gallery.html')


TPL = """<!DOCTYPE html>
<html lang="th"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>PeekaWord · คลังภาพประกอบคำศัพท์</title>
<style>
*{box-sizing:border-box}
body{margin:0;font-family:-apple-system,"Segoe UI",Tahoma,sans-serif;background:#f4f6f9;color:#2b3440}
header{background:#1f3b57;color:#fff;padding:22px 20px}
header h1{margin:0 0 6px;font-size:21px}
header p{margin:0;opacity:.85;font-size:13px}
main{max-width:1100px;margin:0 auto;padding:20px}
.spec{background:#fff;border:1px solid #dde3ea;border-radius:12px;padding:18px 20px;margin-bottom:26px}
.spec h2{margin:0 0 12px;font-size:17px}
.spec table{width:100%;border-collapse:collapse;font-size:13.5px}
.spec td,.spec th{padding:7px 9px;border-bottom:1px solid #eef1f5;text-align:left;vertical-align:top}
.spec th{background:#f7f9fc;width:150px;font-weight:600}
.spec code{background:#eef3f8;padding:2px 6px;border-radius:4px;font-size:12.5px}
.note{background:#fff8e6;border-left:4px solid #f0ad4e;padding:11px 14px;border-radius:7px;
  font-size:13px;margin-top:14px;line-height:1.65}
.lv{margin:30px 0 4px;font-size:19px;padding-left:12px;border-left:6px solid #888}
.lv span{font-size:13px;font-weight:400;opacity:.6}
.lv-A1{border-color:#5FB06B}.lv-A2{border-color:#6CB4EE}
.lv-B1{border-color:#B39DDB}.lv-B2{border-color:#E76F51}
.day{margin:16px 0 8px;font-size:14px;color:#64748b;font-weight:600}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(146px,1fr));gap:13px}
.c{margin:0;background:#fff;border:1px solid #dde3ea;border-radius:12px;padding:11px;text-align:center}
.c svg{width:100%;height:auto;max-width:112px;display:block;margin:0 auto 8px}
.c figcaption{font-size:12.5px;line-height:1.55}
.c b{display:block;font-size:14.5px}
.c i{display:block;color:#6b7a8d;font-size:11.5px;font-style:normal}
.c figcaption span{display:block;color:#2b3440}
.c code{display:block;margin-top:5px;font-size:10.5px;color:#8b97a7;word-break:break-all}
.c button{margin:7px 2px 0;font-size:11px;padding:4px 8px;border:1px solid #cbd5e1;
  background:#f8fafc;border-radius:6px;cursor:pointer}
.c button:hover{background:#eef2f7}
footer{text-align:center;padding:30px 20px;color:#8b97a7;font-size:12px}
</style></head><body>

<header>
  <h1>🎨 คลังภาพประกอบคำศัพท์ · PeekaWord</h1>
  <p>วาดเองทั้งหมดเป็น SVG — ไม่ได้ลอกใคร ใช้เชิงพาณิชย์ได้ 100% · ตอนนี้มี {{N}} คำ</p>
</header>

<main>
<section class="spec">
  <h2>📐 ถ้าจะหารูปมาใส่เอง ต้องวางแบบไหน</h2>
  <table>
    <tr><th>วางที่ไหน</th><td><code>English/img/words/</code> &nbsp;(โฟลเดอร์เดียว ไม่ต้องแยก Level)</td></tr>
    <tr><th>ตั้งชื่อไฟล์</th><td><code>&lt;คำศัพท์&gt;.webp</code> ตัวพิมพ์เล็กทั้งหมด ตัดอักขระพิเศษออก<br>
      <code>cat</code> → <code>cat.webp</code> · <code>Leo's</code> → <code>leos.webp</code> · <code>ice cream</code> → <code>icecream.webp</code></td></tr>
    <tr><th>นามสกุล</th><td><code>.webp</code> ← ระบบหาตัวนี้ก่อน<br>
      <code>.svg</code> ← ถ้าไม่เจอ .webp จะหาตัวนี้ (ไฟล์ในหน้านี้ทั้งหมด)<br>
      ไม่เจอทั้งคู่ → แสดง emoji เดิมอัตโนมัติ ไม่มีไอคอนรูปแตก</td></tr>
    <tr><th>ขนาด</th><td><b>400 × 400 px สี่เหลี่ยมจัตุรัส</b> — การ์ดแสดงที่ ~112px จึงคมพอบนจอ Retina</td></tr>
    <tr><th>น้ำหนักไฟล์</th><td>ไม่เกิน <b>40 KB</b>/ไฟล์ (WebP quality 82) — ทั้งวันมี 6–9 รูป ต้องโหลดไวบนมือถือ</td></tr>
    <tr><th>องค์ประกอบภาพ</th><td>วัตถุหลัก<b>อยู่กลางภาพ</b> กินพื้นที่ 60–80% · พื้นหลังเรียบหรือเบลอ ·
      ไม่มีตัวหนังสือในรูป (เด็กต้องอ่านคำจากการ์ด ไม่ใช่จากภาพ)</td></tr>
    <tr><th>ไม่ต้องแก้โค้ด</th><td>วางไฟล์แล้ว<b>ขึ้นเองทันที</b> — <code>js/pic.js</code> ฝังครบ 448 วันแล้ว</td></tr>
  </table>
  <div class="note">
    <b>⚠️ ลิขสิทธิ์ — ต้องผ่านทุกไฟล์</b><br>
    • Pexels / Pixabay / Unsplash = ใช้เชิงพาณิชย์ได้ ไม่ต้องให้เครดิต <b>แต่ห้ามใช้ภาพคนที่ระบุตัวตนได้ในบริบทเชิงลบ</b>
      → คำอย่าง <code>angry</code> <code>sad</code> <code>scared</code> อย่าใช้หน้าคนจริง<br>
    • ห้ามใช้ภาพที่มีโลโก้ แบรนด์ ตัวการ์ตูนมีเจ้าของ หรือตัวละครที่จำได้<br>
    • เก็บบันทึกที่มาทุกไฟล์ไว้ใน <code>_docs/images/manifest.csv</code> (source + license + URL)
  </div>
  <div class="note" style="background:#eaf6ee;border-color:#5FB06B">
    <b>✅ ขอบเขตที่แนะนำ</b> — ทำเฉพาะ <b>A1 + A2 (1,013 คำ)</b> ที่เป็นรูปธรรม
    ส่วน B1/B2 อีก 1,987 คำเป็นนามธรรม (<code>governance</code> <code>conjecture</code>) ภาพช่วยไม่ได้ คง emoji ไว้ดีกว่า<br>
    เริ่มจาก <b>Day 1–7</b> ก่อน เพราะเป็นช่วงทดลองที่ตัดสินว่าพ่อแม่จะจ่ายไหม
  </div>
</section>

{{CARDS}}
</main>
<footer>ภาพทั้งหมดในหน้านี้วาดขึ้นใหม่เป็น SVG · สร้างโดย <code>_docs/gen_svg.py</code></footer>

<script>
function svgOf(w){return document.querySelector('.c[data-w="'+w+'"] svg').outerHTML;}
function dl(w){
  var b=new Blob([svgOf(w)],{type:'image/svg+xml'}),u=URL.createObjectURL(b),a=document.createElement('a');
  a.href=u;a.download=w+'.svg';a.click();URL.revokeObjectURL(u);
}
function png(w){
  var img=new Image(),S=400;
  img.onload=function(){
    var c=document.createElement('canvas');c.width=c.height=S;
    c.getContext('2d').drawImage(img,0,0,S,S);
    c.toBlob(function(b){
      var u=URL.createObjectURL(b),a=document.createElement('a');
      a.href=u;a.download=w+'.png';a.click();URL.revokeObjectURL(u);
    },'image/png');
  };
  img.src='data:image/svg+xml;charset=utf-8,'+encodeURIComponent(svgOf(w));
}
</script>
</body></html>"""

if __name__ == '__main__':
    main()
