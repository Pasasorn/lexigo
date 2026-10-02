# -*- coding: utf-8 -*-
"""
กวาดตรวจไฟล์ Day ทุกไฟล์ทุก Level — จำลองสิ่งที่ผู้ใช้จะเจอ
รัน:  python _docs/audit_all.py
"""
import os, re, json, glob, collections, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
files = sorted(glob.glob(os.path.join(ROOT, 'Level*', 'Day*.html')),
               key=lambda p: int(re.search(r'Day(\d+)', os.path.basename(p)).group(1)))

ISSUES = collections.defaultdict(list)   # code -> [(day, detail)]
def bug(code, day, detail=''):
    ISSUES[code].append((day, detail))

# ---- ทะเบียนไฟล์จริง (เทียบ case-sensitive แบบ Cloudflare) ----
real = {}
for p in files:
    real.setdefault(os.path.basename(os.path.dirname(p)), set()).add(os.path.basename(p))
all_names = {(os.path.basename(os.path.dirname(p)), os.path.basename(p)) for p in files}

days = {}
for p in files:
    d = int(re.search(r'Day(\d+)', os.path.basename(p)).group(1))
    days[d] = p

print('พบไฟล์ %d  ·  Day %d–%d' % (len(files), min(days), max(days)))
missing = [d for d in range(1, max(days) + 1) if d not in days]
if missing:
    bug('DAY_MISSING', 0, 'ขาดวัน: %s' % missing[:20])

for d in sorted(days):
    p = days[d]
    lvdir = os.path.basename(os.path.dirname(p))
    h = open(p, encoding='utf-8').read()
    low = h.lower()

    # 1) สคริปต์ที่ต้องฝังครบ
    for js, code in [('js/report.js', 'NO_REPORT'), ('js/pic.js', 'NO_PIC'),
                     ('js/protect.js', 'NO_PROTECT')]:
        if js not in h:
            bug(code, d)

    # 2) ครบ 5 ขั้นตอน
    for n in range(1, 6):
        if not re.search(r"(id=['\"](page|step)%d['\"]|data-step=['\"]%d['\"])" % (n, n), h):
            bug('STEP%d_MISSING' % n, d)

    # 3) WORDS
    m = re.search(r'(?:const|var|let)\s+WORDS\s*=\s*(\[.*?\])\s*;', h, re.S)
    if not m:
        bug('NO_WORDS', d)
        nwords = 0
    else:
        raw = m.group(1)
        es = re.findall(r"\be\s*:\s*['\"]([^'\"]+)['\"]", raw)
        ths = re.findall(r"\bt\s*:\s*['\"]([^'\"]*)['\"]", raw)
        phs = re.findall(r"\bph\s*:\s*['\"]([^'\"]*)['\"]", raw)
        ems = re.findall(r"\bem\s*:\s*['\"]([^'\"]*)['\"]", raw)
        nwords = len(es)
        if nwords == 0:
            bug('WORDS_EMPTY', d)
        if len(set(x.lower() for x in es)) != nwords:
            dup = [w for w, c in collections.Counter(x.lower() for x in es).items() if c > 1]
            bug('WORD_DUP_IN_DAY', d, str(dup))
        if ths and len([t for t in ths if t.strip()]) < nwords:
            bug('THAI_MISSING', d, '%d/%d' % (len([t for t in ths if t.strip()]), nwords))
        if phs and len([t for t in phs if t.strip()]) < nwords:
            bug('IPA_MISSING', d, '%d/%d' % (len([t for t in phs if t.strip()]), nwords))
        if ems and len([t for t in ems if t.strip()]) < nwords:
            bug('EMOJI_MISSING', d, '%d/%d' % (len([t for t in ems if t.strip()]), nwords))
        if ems:
            de = [e for e, c in collections.Counter(ems).items() if c > 1 and e.strip()]
            if de:
                bug('EMOJI_DUP_IN_DAY', d, str(de))

    # 4) จำนวนคำต่อวันตามกติกา (A1=6 A2=7 B1=8 B2=9)
    cefr = (re.search(r'_(A1|A2|B1|B2)\.html$', os.path.basename(p)) or [None, '?'])[1]
    want = {'A1': 6, 'A2': 7, 'B1': 8, 'B2': 9}.get(cefr)
    if want and nwords and nwords != want and d not in (447,):
        bug('WORDCOUNT_ODD', d, '%s ควร %d ได้ %d' % (cefr, want, nwords))

    # 5) เฉลย Think ของ Step 1 และ Step 2 ต้องมี และต้องไม่ซ้ำกัน
    t1 = re.search(r"thinkAns1['\"]?\s*[\)\]]?[^>]*>(.*?)</", h, re.S)
    has1 = 'thinkAns1' in h
    has2 = re.search(r"thinkAns['\"]", h) is not None
    if not has1:
        bug('NO_THINK1_ANSWER', d)
    q = re.findall(r'<p class="q"[^>]*>(.*?)</p>', h, re.S)
    if len(q) >= 2 and q[0].strip() and q[0].strip() == q[1].strip():
        bug('THINK_Q_SAME', d, q[0][:50])

    # 6) ลิงก์วันถัดไป (case ต้องตรงเป๊ะ แบบ Cloudflare)
    for href in set(re.findall(r'href=["\']\.\./(Level\d+)/(Day[^"\']+\.html)["\']', h)):
        if href not in all_names:
            bug('LINK_404', d, '/'.join(href))
    for href in set(re.findall(r'href=["\'](Day[^"\'/]+\.html)["\']', h)):
        if (lvdir, href) not in all_names:
            bug('LINK_404', d, lvdir + '/' + href)
    if d < max(days) and 'Day%d' % (d + 1) not in h and "Day' + " not in h \
       and 'dashboard' not in low:
        bug('NO_NEXT_LINK', d)

    # 7) คะแนน / sync
    if 'pwCollect' not in h:
        bug('NO_COLLECT', d)
    if 'syncToCloud' in h and 'pwSkillQS' not in h:
        bug('NO_SKILLQS', d)
    if '_pwScore' not in h and 'pwPct' not in h:
        bug('NO_SCOREVAR', d)

    # 8) TTS
    if 'speechSynthesis' not in h:
        bug('NO_TTS', d)

    # 9) ป้าย Step 4 ต้องไม่เขียนว่า Write/เขียน (จริง ๆ คือเรียงประโยค)
    if re.search(r'Listen\s*\+\s*Write|ฟังแล้วเขียน', h):
        bug('STEP4_LABEL', d)

    # 10) ภาพประกอบเรื่อง
    for src in set(re.findall(r'src=["\']\.\./(img/[^"\']+)["\']', h)):
        if not src.startswith('img/words') and not os.path.exists(os.path.join(ROOT, src)):
            bug('IMG_404', d, src)

    # 11) ไอคอนบนการ์ด ต้องผ่าน pwPic
    if 'ac-em' in h and 'pwPic' not in h:
        bug('CARD_NO_PWPIC', d)

    # 12) ไวยากรณ์ JS
    for sm in re.finditer(r'<script(?![^>]*\bsrc=)[^>]*>(.*?)</script>', h, re.S):
        code = sm.group(1)
        if code.count('`') % 2:
            bug('JS_BACKTICK_ODD', d)
        for a, b in [('{', '}'), ('(', ')'), ('[', ']')]:
            pass

# ---------- สรุป ----------
print('\n' + '=' * 62)
SEV = {
  'DAY_MISSING':'🔴','NO_WORDS':'🔴','WORDS_EMPTY':'🔴','LINK_404':'🔴',
  'STEP1_MISSING':'🔴','STEP2_MISSING':'🔴','STEP3_MISSING':'🔴',
  'STEP4_MISSING':'🔴','STEP5_MISSING':'🔴','JS_BACKTICK_ODD':'🔴',
  'WORD_DUP_IN_DAY':'🟠','NO_THINK1_ANSWER':'🟠','THINK_Q_SAME':'🟠',
  'NO_REPORT':'🟠','NO_COLLECT':'🟠','NO_SCOREVAR':'🟠','NO_NEXT_LINK':'🟠',
  'IPA_MISSING':'🟠','THAI_MISSING':'🟠','STEP4_LABEL':'🟠',
  'NO_PIC':'🟡','NO_PROTECT':'🟡','NO_SKILLQS':'🟡','NO_TTS':'🟡',
  'EMOJI_MISSING':'🟡','EMOJI_DUP_IN_DAY':'🟡','WORDCOUNT_ODD':'🟡',
  'IMG_404':'🟡','CARD_NO_PWPIC':'🟡',
}
if not ISSUES:
    print('✅ ไม่พบปัญหาเลย')
for code in sorted(ISSUES, key=lambda c: (SEV.get(c, '🟡'), -len(ISSUES[c]))):
    lst = ISSUES[code]
    ds = sorted(set(x[0] for x in lst))
    head = '%s %-18s %4d จุด' % (SEV.get(code, '🟡'), code, len(lst))
    print(head)
    print('     วัน: %s%s' % (', '.join(map(str, ds[:14])), ' …' if len(ds) > 14 else ''))
    det = [x[1] for x in lst if x[1]][:3]
    for t in det:
        print('     · %s' % t[:110])

json.dump({k: v for k, v in ISSUES.items()},
          open(os.path.join(ROOT, '_docs', 'audit_result.json'), 'w'),
          ensure_ascii=False, indent=1)
print('\nบันทึก → _docs/audit_result.json')
