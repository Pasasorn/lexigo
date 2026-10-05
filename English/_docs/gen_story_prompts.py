# -*- coding: utf-8 -*-
"""
ดึงเนื้อเรื่องของทุก Day ออกมา + สร้าง prompt สำหรับ gen ภาพประกอบ

ผลลัพธ์
  _docs/story_prompts.csv    ← เปิดด้วย Excel · เอาไป gen เป็นชุด
  _docs/story_prompts.html   ← เปิดอ่าน · กดคัดลอก prompt ทีละวันหรือทั้งหมด

รัน:  py _docs/gen_story_prompts.py
ไฟล์ภาพที่ได้ให้ตั้งชื่อ  img_day<N>.png  แล้ววางที่  English/img/
"""
import os, re, csv, json, glob, html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# สไตล์กลาง — ใช้เหมือนกันทุกวัน ภาพจะได้เป็นชุดเดียวกัน
STYLE = ("children's storybook illustration, soft warm colors, friendly rounded shapes, "
         "gentle lighting, flat vector style with light texture, wide 16:9 scene, "
         "no text, no letters, no words, no watermark")

# ตัดคำที่ทำให้ภาพออกมาเป็นนามธรรมหรือสุ่มเกินไป
DROP = re.compile(r'^(and|but|so|then|it|he|she|they|this|that|there)\b', re.I)


def clean(t):
    t = re.sub(r'<[^>]+>', ' ', t)
    t = html.unescape(t)
    return re.sub(r'\s+', ' ', t).strip()


def sentences(t):
    return [s.strip() for s in re.split(r'(?<=[.!?])\s+', t) if s.strip()]


def summarize(story, maxlen=240):
    """เลือกประโยคที่เห็นภาพได้ชัดที่สุด 2–3 ประโยคแรกที่ไม่ขึ้นต้นด้วยคำเชื่อม"""
    ss = sentences(story)
    pick = [s for s in ss if not DROP.match(s)][:3] or ss[:2]
    out = ' '.join(pick)
    if len(out) > maxlen:
        out = ' '.join(pick[:2])
    return out[:maxlen].strip()


def main():
    files = sorted(glob.glob(os.path.join(ROOT, 'Level*', 'Day*.html')),
                   key=lambda p: int(re.search(r'Day(\d+)', os.path.basename(p)).group(1)))
    rows = []
    for p in files:
        base = os.path.basename(p)
        d    = int(re.search(r'Day(\d+)', base).group(1))
        lv   = int(re.search(r'Level(\d+)', p.replace('\\', '/')).group(1))
        cefr = (re.search(r'_(A1|A2|B1|B2)\.html$', base) or [None, ''])[1]
        h    = open(p, encoding='utf-8').read()

        # เนื้อเรื่อง
        m = re.search(r'(?:const|var|let)\s+STORY\s*=\s*(["`\'])(.*?)\1\s*;', h, re.S)
        story = clean(m.group(2)) if m else ''
        if not story:
            sb = re.search(r'<div class="sbox">(.*?)</div>', h, re.S)
            story = clean(sb.group(1)) if sb else ''

        # ชื่อเรื่อง + ธีม
        t  = clean((re.search(r'<title>(.*?)</title>', h) or ['', ''])[1])
        title = re.sub(r'^Day\s*\d+\s*[—–-]\s*', '', t)
        th = re.search(r'Day\s*\d+\s*·\s*([^<—]+?)\s*(?:—|&mdash;|<)', h)
        theme = clean(th.group(1)) if th else ''

        # คำศัพท์ของวัน
        wm = re.search(r'(?:const|var|let)\s+WORDS\s*=\s*(\[.*?\])\s*;', h, re.S)
        words = re.findall(r"\be\s*:\s*['\"]([^'\"]+)['\"]", wm.group(1)) if wm else []

        is_rev = len(re.findall(r'id="p\d"', h)) == 9
        summ = summarize(story)

        wl = ', '.join(words[:9])

        if is_rev:
            prompt = ('Illustrate a cheerful review-day celebration for a children\'s English book: '
                      'two original child-friendly characters cheering together among floating '
                      'stars, balloons and simple everyday objects. '
                      'Theme: %s. ' % (theme or title) + STYLE)
        elif cefr in ('B1', 'B2'):
            # ระดับสูงเนื้อเรื่องเป็นนามธรรม ใช้หัวข้อ+คำศัพท์เป็นตัวตั้งแทน
            prompt = ('Illustrate one clear, concrete scene that explains "%s" to a child, '
                      'for a children\'s English book. Show real objects and people doing the '
                      'action — not symbols or abstract shapes. '
                      'Key ideas to show: %s. ' % (title, wl) + STYLE)
        elif story:
            prompt = ('Illustrate this short story as ONE single scene for a children\'s English '
                      'book. Story: "%s" '
                      'Show the main characters and the objects named. '
                      'Original characters, not based on any existing franchise or known cartoon. '
                      % story + STYLE)
        else:
            prompt = ('Illustrate a friendly everyday scene about "%s" for a children\'s English '
                      'book. Show: %s. ' % (theme or title, wl) + STYLE)

        rows.append(dict(day=d, level=lv, cefr=cefr, review='ทบทวน' if is_rev else '',
                         title=title, theme=theme, words=' · '.join(words),
                         summary=summ, story=story, prompt=prompt,
                         filename='img_day%d.png' % d))

    # CSV
    cp = os.path.join(ROOT, '_docs', 'story_prompts.csv')
    with open(cp, 'w', newline='', encoding='utf-8-sig') as f:
        w = csv.DictWriter(f, fieldnames=['day', 'level', 'cefr', 'review', 'filename',
                                          'title', 'theme', 'words', 'summary', 'prompt', 'story'])
        w.writeheader()
        w.writerows(rows)

    # HTML
    hp = os.path.join(ROOT, '_docs', 'story_prompts.html')
    open(hp, 'w', encoding='utf-8').write(
        TPL.replace('/*DATA*/', json.dumps(rows, ensure_ascii=False, separators=(',', ':')))
           .replace('__STYLE__', html.escape(STYLE)))

    nostory = [r['day'] for r in rows if not r['story']]
    print('เขียน %s' % cp)
    print('เขียน %s' % hp)
    print('ทั้งหมด %d วัน · ไม่มีเนื้อเรื่อง %d วัน %s'
          % (len(rows), len(nostory), nostory[:12] if nostory else ''))
    print('ความยาวเรื่องเฉลี่ย %.0f ตัวอักษร'
          % (sum(len(r['story']) for r in rows) / max(1, len(rows))))


TPL = r"""<!DOCTYPE html>
<html lang="th"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>เนื้อเรื่องรายวัน + Prompt สร้างภาพ · PeekaWord</title>
<style>
*{box-sizing:border-box}
body{margin:0;font-family:-apple-system,"Segoe UI",Tahoma,sans-serif;background:#f4f6f9;color:#28323e}
header{background:#1f3b57;color:#fff;padding:18px 20px}
header h1{margin:0 0 4px;font-size:20px}
header p{margin:0;font-size:13px;opacity:.85}
.bar{position:sticky;top:0;z-index:9;background:#fff;border-bottom:1px solid #dde3ea;
 padding:10px 20px;display:flex;gap:8px;flex-wrap:wrap;align-items:center}
.bar input,.bar select,.bar button{padding:8px 11px;border:1px solid #cbd5e1;border-radius:8px;
 background:#fff;font-size:13px;font-family:inherit}
.bar button{cursor:pointer;font-weight:700}
.bar button:hover{background:#eef2f7}
.bar .n{margin-left:auto;font-size:13px;color:#64748b}
main{max-width:980px;margin:0 auto;padding:16px 20px 60px}
.d{background:#fff;border:1px solid #dde3ea;border-radius:12px;padding:14px 16px;margin-bottom:12px}
.hd{display:flex;align-items:baseline;gap:9px;flex-wrap:wrap;margin-bottom:8px}
.hd b{font-size:16px}
.tag{font-size:10.5px;font-weight:800;color:#fff;padding:2px 8px;border-radius:20px}
.A1{background:#5FB06B}.A2{background:#3b87c9}.B1{background:#7e63c4}.B2{background:#d1573a}
.rv{background:#f0ad4e}
.hd small{color:#64748b;font-size:12px}
.w{font-size:12.5px;color:#475569;margin-bottom:8px}
.st{font-size:13.5px;line-height:1.75;background:#f7f9fc;border-radius:8px;padding:10px 12px;
 margin-bottom:8px;max-height:92px;overflow:hidden;position:relative;cursor:pointer}
.st.open{max-height:none}
.st::after{content:"";position:absolute;left:0;right:0;bottom:0;height:28px;
 background:linear-gradient(transparent,#f7f9fc)}
.st.open::after{display:none}
.pm{font-size:12.5px;line-height:1.65;background:#eef8f0;border:1px solid #c9e6ce;border-radius:8px;
 padding:10px 12px;white-space:pre-wrap}
.row{display:flex;gap:7px;margin-top:8px;align-items:center}
.row button{padding:6px 13px;font-size:12px;border:1px solid #cbd5e1;background:#fff;
 border-radius:7px;cursor:pointer;font-family:inherit}
.row code{font-size:11.5px;color:#64748b}
.more{text-align:center;margin:20px 0}
.more button{padding:10px 24px;border:1px solid #cbd5e1;background:#fff;border-radius:9px;
 cursor:pointer;font-size:14px}
.tip{background:#fff8e6;border-left:4px solid #f0ad4e;padding:11px 14px;border-radius:7px;
 font-size:13px;line-height:1.7;margin-bottom:16px}
</style></head><body>

<header>
  <h1>🖼️ เนื้อเรื่องรายวัน + Prompt สร้างภาพ</h1>
  <p>ใช้สร้างภาพประกอบเรื่อง (ภาพใหญ่หัวบทเรียน) ไม่ใช่ภาพคำศัพท์</p>
</header>

<div class="bar">
  <input type="search" id="q" placeholder="ค้นหาชื่อเรื่อง / คำศัพท์ / เนื้อเรื่อง…" style="flex:1;min-width:190px">
  <select id="fc"><option value="">ทุกระดับ</option><option>A1</option><option>A2</option>
  <option>B1</option><option>B2</option></select>
  <select id="fd"><option value="">ทุกวัน</option><option value="1-7">Day 1–7</option>
  <option value="1-30">Day 1–30</option><option value="31-100">Day 31–100</option>
  <option value="101-250">Day 101–250</option><option value="251-448">Day 251–448</option></select>
  <button onclick="copyAll()">📋 คัดลอก prompt ทั้งหมดที่กรองไว้</button>
  <span class="n" id="cnt"></span>
</div>

<main>
<div class="tip">
  <b>วิธีใช้</b> — คัดลอก prompt ไปวางใน Midjourney / DALL·E / Canva Magic Media / Gemini
  แล้วตั้งชื่อไฟล์ที่ได้เป็น <code>img_day&lt;เลขวัน&gt;.png</code> วางไว้ที่ <code>English/img/</code><br>
  <b>สัดส่วน 16:9</b> (กว้าง ~1200×675) · หน้าเว็บครอบสูงไม่เกิน 220px อยู่แล้ว<br>
  <b>สไตล์กลางที่ต่อท้ายทุก prompt:</b> <code>__STYLE__</code><br>
  ⚠️ ทุก prompt กำกับว่า <b>no text</b> และ <b>original characters</b> เพื่อกันปัญหาลิขสิทธิ์และตัวหนังสือเพี้ยนในภาพ
</div>
<div id="out"></div>
</main>

<script>
const D = /*DATA*/;
let shown = 60;

function esc(s){ return String(s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c])); }

function sel(){
  const q=document.getElementById('q').value.trim().toLowerCase(),
        c=document.getElementById('fc').value, dr=document.getElementById('fd').value;
  let a=0,b=9999; if(dr){const p=dr.split('-');a=+p[0];b=+p[1];}
  return D.filter(r=>{
    if(c && r.cefr!==c) return false;
    if(r.day<a||r.day>b) return false;
    if(q && !(r.title+' '+r.words+' '+r.story+' '+r.theme).toLowerCase().includes(q)) return false;
    return true;
  });
}

function render(){
  const rows = sel();
  document.getElementById('cnt').textContent = rows.length + ' วัน';
  const out = document.getElementById('out');
  out.innerHTML = rows.slice(0,shown).map(r=>`
    <div class="d">
      <div class="hd"><b>Day ${r.day}</b>
        <span class="tag ${r.cefr}">${r.cefr}</span>
        ${r.review?'<span class="tag rv">ทบทวน</span>':''}
        <span>${esc(r.title)}</span>
        <small>Level ${r.level}${r.theme?' · '+esc(r.theme):''}</small></div>
      ${r.words?`<div class="w">📚 ${esc(r.words)}</div>`:''}
      <div class="st" onclick="this.classList.toggle('open')">${esc(r.story)||'<i>ไม่มีเนื้อเรื่อง</i>'}</div>
      <div class="pm" id="p${r.day}">${esc(r.prompt)}</div>
      <div class="row">
        <button onclick="cp(${r.day},this)">📋 คัดลอก prompt</button>
        <code>${r.filename}</code>
      </div>
    </div>`).join('')
    + (rows.length>shown ? `<div class="more"><button onclick="shown+=60;render()">แสดงเพิ่ม (เหลือ ${rows.length-shown} วัน)</button></div>` : '');
}

function cp(day, btn){
  const t = D.find(x=>x.day===day).prompt;
  navigator.clipboard.writeText(t).then(()=>{
    const o=btn.textContent; btn.textContent='✅ คัดลอกแล้ว';
    setTimeout(()=>btn.textContent=o,1400);
  });
}
function copyAll(){
  const rows = sel();
  const t = rows.map(r=>`### ${r.filename}  (Day ${r.day} · ${r.cefr} · ${r.title})\n${r.prompt}`).join('\n\n');
  navigator.clipboard.writeText(t).then(()=>alert('คัดลอก '+rows.length+' prompt แล้ว'));
}
['q','fc','fd'].forEach(i=>document.getElementById(i).addEventListener('input',()=>{shown=60;render()}));
render();
</script>
</body></html>"""

if __name__ == '__main__':
    main()
