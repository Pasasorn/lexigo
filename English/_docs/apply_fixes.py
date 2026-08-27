#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PeekaWord — ชุดแก้บั๊กมาตรฐาน (idempotent: รันซ้ำได้ ไม่พัง)

ใช้กับไฟล์ Day ที่เพิ่ง generate ออกมา และกับ golden/BASE_Day61.html
เพื่อไม่ให้บั๊กที่แก้ไปแล้วกลับมาอีกในวันใหม่

  python3 apply_fixes.py ../Level4/Day105_*.html
  python3 apply_fixes.py golden/BASE_Day61.html
  python3 apply_fixes.py --all          # ทุกไฟล์ Day + BASE

บั๊กที่ครอบคลุม (จากการตรวจโดยผู้เชี่ยวชาญ 4 คน 5 รอบ — ดู AUDIT_REPORT.md)
"""
import re, sys, glob, os

SPEAKFB = '''
// ── FEEDBACK SOUND ──
function speakFb(type){
  const msgs={
    correct:['Correct!','Great job!','Well done!','Awesome!'],
    wrong:  ['Try again!','Almost!','Keep trying!'],
    perfect:['Perfect!','Amazing! All correct!','Excellent!']
  };
  const list=msgs[type]||msgs.correct;
  const txt=list[Math.floor(Math.random()*list.length)];
  try{
    const u=new SpeechSynthesisUtterance(txt);
    if(typeof curV!=='undefined'&&curV)u.voice=curV;
    u.rate=1.0;u.lang='en-US';
    window.speechSynthesis.speak(u);
  }catch(e){}
}
'''

PWPCT = ("function pwPct(){var s=window._pwScore||0,t=window._pwTot||6;"
         "return Math.max(0,Math.min(100,Math.round(s/(t||1)*100)));}\n")


def fix(h):
    # 1) speakFb ถูกเรียกแต่ไม่มีนิยาม → JS ตายตรงจุดตรวจคำตอบ Step 2
    if 'speakFb' in h and 'function speakFb' not in h:
        i = h.index('  speakFb(')
        j = h.index('\n}', i) + 2
        h = h[:j] + SPEAKFB + h[j:]

    # 2) unlock เช็กความยาวตายตัว → รหัสถูกต้องถูกปฏิเสธ (D14-XXXX ยาว 8 ไม่ใช่ 7)
    h = re.sub(r"(\w+)\.startsWith\((PREV_PFX|PREV_PREFIX)\)\s*&&\s*\1\.length\s*===\s*\d+",
               lambda m: f"new RegExp('^'+{m.group(2)}+'[A-Z0-9]{{4}}$').test({m.group(1)})", h)
    h = re.sub(r"(\w+)\.startsWith\('D'\+\((MY_)?DAY-1\)\+'-'\)",
               lambda m: f"new RegExp('^D'+({m.group(2) or ''}DAY-1)+'-[A-Z0-9]{{4}}$').test({m.group(1)})", h)

    # 3) คะแนน: บันทึกค่าสูงสุดของวัน แล้วส่งเป็นเปอร์เซ็นต์ (ทุกวันสเกลเดียวกัน)
    h = re.sub(r'function updScore\((n|n,tot)\)\{(?!window\._pwScore)',
               lambda m: 'function updScore(%s){window._pwScore=Math.max(window._pwScore||0,n);%s'
                         % (m.group(1), 'window._pwTot=tot||6;' if ',' in m.group(1) else ''), h)
    h = h.replace("function syncToCloud(day,code,score){score=score||100;",
                  "function syncToCloud(day,code,score){score=(score===undefined||score===null)?0:score;")
    if 'function pwPct(' not in h and 'function syncToCloud' in h:
        h = h.replace("function syncToCloud", PWPCT + "function syncToCloud", 1)
    h = re.sub(r'(?<!function )syncToCloud\(([^,()]+),\s*code\s*,\s*[^;]*?\)(?=;)',
               r'syncToCloud(\1,code,pwPct())', h)
    h = re.sub(r'(?<!function )syncToCloud\(([^,()]+),\s*code\)(?=;)',
               r'syncToCloud(\1,code,pwPct())', h)

    # 4) Finish เป็น latch → กดจบแล้วเล่นเพิ่ม คะแนนที่ทำได้หายหมด
    h = re.sub(r"if\(!code\)\{([^{}]*?)(syncToCloud\([^;]*?\);)\}", r"if(!code){\1}\2", h)

    # 5) แจกคะแนนฟรี — ตอบผิดหมดยังได้ 3 ข้อ / พูดมั่วยังได้ 2 คะแนน
    h = h.replace("updScore(ok+3,6)", "updScore(ok,data.length)")
    h = h.replace("updScore(Math.round(avg/100*2)+2,6)",
                  "updScore(Math.round(avg/100*SS.length),SS.length)")

    # 6) apostrophe ในประโยค → onclick="speak('Leo's ...')" เป็น SyntaxError ปุ่ม ▶ ตาย
    h = re.sub(r'onclick="speak\(\'\$\{([^}]*)\}\'\)"',
               lambda m: m.group(0) if '.replace(' in m.group(1)
               else 'onclick="speak(\'${String(%s).replace(/\'/g,"\\\\\'").replace(/"/g,\'&quot;\')}\')"' % m.group(1), h)

    # 7) รูปหาย → อย่าโชว์ข้อความสำหรับทีมงานให้ลูกค้าเห็น
    h = re.sub(r'onerror="this\.parentElement\.innerHTML=.*?"(?=\s*/?>)',
               "onerror=\"this.parentElement.style.display='none'\"", h)

    # 8) ป้ายปุ่มวันถัดไปต้องตรงกับลิงก์จริง (template เดิมค้าง "Day 62")
    h = re.sub(r'href="([^"]*Day(\d+)_[^"]*\.html)"([^>]*)>([^<]*Day\s*\d+[^<]*)</a>',
               lambda m: 'href="%s"%s>%s</a>' % (m.group(1), m.group(3),
                                                 re.sub(r'Day\s*\d+', 'Day ' + m.group(2), m.group(4))), h)
    return h


def main():
    args = sys.argv[1:]
    base = os.path.dirname(os.path.abspath(__file__))
    if '--all' in args:
        files = sorted(glob.glob(os.path.join(base, '..', 'Level*', 'Day*.html')))
        files += glob.glob(os.path.join(base, 'golden', 'BASE_*.html'))
    else:
        files = [f for a in args for f in glob.glob(a)]
    if not files:
        print('ไม่พบไฟล์'); return
    n = 0
    for f in files:
        h = open(f, encoding='utf-8', errors='ignore').read()
        h2 = fix(h)
        if h2 != h:
            open(f, 'w', encoding='utf-8').write(h2); n += 1
            print('  แก้:', os.path.basename(f))
    print(f'\nแก้ {n} / {len(files)} ไฟล์ (ที่เหลือถูกต้องอยู่แล้ว)')


if __name__ == '__main__':
    main()
