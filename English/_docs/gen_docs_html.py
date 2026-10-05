# -*- coding: utf-8 -*-
"""
รวมเอกสาร .md ทั้งหมดใน _docs/ เป็นไฟล์ HTML เดียว เปิดได้ทุกเครื่อง

ผลลัพธ์:  _docs/คู่มือทั้งหมด.html   (ไฟล์เดียวจบ ไม่ต้องต่อเน็ต ไม่ต้องลงอะไร)

รัน:  py _docs/gen_docs_html.py
"""
import os, re, json, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC  = os.path.join(ROOT, '_docs')
OUT  = os.path.join(SRC, 'docs.html')   # ชื่ออังกฤษ กันปัญหา encoding ตอนส่งข้ามเครื่อง

# เรียงกลุ่มให้หาง่าย — ไฟล์ที่ไม่อยู่ในลิสต์จะไปอยู่กลุ่ม "อื่น ๆ"
GROUPS = [
    ('🚀 เริ่มต้น / ติดตั้ง', ['AUTO_SETUP', 'SETUP_NEW_SHEET', 'DEPLOY_NOW', 'DEPLOY_v5',
                              'SLIP_AND_LOGIN_SETUP', 'CLOUDFLARE_MIGRATION']),
    ('🔐 ความปลอดภัย / แอดมิน', ['SECURITY_FIX', 'MASTER_ADMIN', 'ADMIN_LINKS', 'ALL_LINKS',
                                 'TEACHER_PANEL', 'WATERMARK_AND_PROTECTION', 'DATA_PERSISTENCE']),
    ('🧪 ผลตรวจ / คุณภาพ', ['AUDIT_ALL_LEVELS', 'AUDIT_REPORT', 'UX_REVIEW', 'LAUNCH_READINESS']),
    ('📣 เปิดตัว / การตลาด', ['LAUNCH_PLAN', 'brand']),
    ('📚 เนื้อหา / การผลิต', ['Day_Blueprint', 'IMAGE_PIPELINE', 'Level2_Plan_Day31-60',
                              'Level4_Plan_Day91-120', 'generate-review-day-SKILL',
                              'standard-day-pattern_SKILL_updated']),
]


def main():
    docs = {}
    for p in sorted(glob.glob(os.path.join(SRC, '*.md'))):
        k = os.path.splitext(os.path.basename(p))[0]
        docs[k] = open(p, encoding='utf-8').read()

    used = set()
    groups = []
    for title, keys in GROUPS:
        items = [k for k in keys if k in docs]
        used.update(items)
        if items:
            groups.append({'t': title, 'k': items})
    rest = sorted(k for k in docs if k not in used)
    if rest:
        groups.append({'t': '📄 อื่น ๆ', 'k': rest})

    payload = json.dumps({'docs': docs, 'groups': groups}, ensure_ascii=False)
    payload = payload.replace('</script>', '<\\/script>')   # กัน script ปิดกลางคัน

    html = TPL.replace('/*DATA*/', payload).replace('__N__', str(len(docs)))
    open(OUT, 'w', encoding='utf-8').write(html)
    print('เขียน %s' % OUT)
    print('%d เอกสาร · %.0f KB' % (len(docs), os.path.getsize(OUT) / 1024))


TPL = r"""<!DOCTYPE html>
<html lang="th"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>คู่มือ PeekaWord</title>
<style>
*{box-sizing:border-box}
body{margin:0;font-family:-apple-system,"Segoe UI",Tahoma,sans-serif;background:#f4f6f9;color:#28323e;
  display:flex;min-height:100vh}
#side{width:272px;flex:none;background:#1f3b57;color:#fff;overflow:auto;position:sticky;top:0;height:100vh}
#side h1{margin:0;padding:16px 18px 6px;font-size:17px}
#side p{margin:0;padding:0 18px 12px;font-size:12px;opacity:.75}
#side input{width:calc(100% - 24px);margin:0 12px 10px;padding:8px 11px;border:0;border-radius:8px;font-size:13px}
#side .g{font-size:11px;text-transform:uppercase;letter-spacing:.6px;opacity:.6;
  padding:12px 18px 5px;font-weight:700}
#side a{display:block;padding:7px 18px;color:#dce6f2;text-decoration:none;font-size:13.2px;line-height:1.45;
  border-left:3px solid transparent}
#side a:hover{background:rgba(255,255,255,.08)}
#side a.on{background:rgba(255,255,255,.15);border-left-color:#7fd1ff;color:#fff;font-weight:700}
#main{flex:1;min-width:0;overflow:auto}
#bar{display:none}
article{max-width:860px;margin:0 auto;padding:26px 30px 70px;line-height:1.8}
article h1{font-size:25px;margin:0 0 14px;padding-bottom:9px;border-bottom:2px solid #dde3ea}
article h2{font-size:20px;margin:30px 0 11px;padding-bottom:6px;border-bottom:1px solid #e6eaf0}
article h3{font-size:16.5px;margin:22px 0 8px}
article p{margin:0 0 12px}
article ul,article ol{margin:0 0 13px;padding-left:24px}
article li{margin-bottom:5px}
article code{background:#eef3f8;padding:2px 6px;border-radius:5px;font-size:13px;
  font-family:Consolas,Monaco,monospace;word-break:break-word}
article pre{background:#1f2a37;color:#e6edf3;padding:13px 16px;border-radius:10px;overflow:auto;
  font-size:13px;line-height:1.65;margin:0 0 14px}
article pre code{background:none;color:inherit;padding:0;font-size:13px}
article table{border-collapse:collapse;width:100%;margin:0 0 15px;font-size:14px;
  background:#fff;border:1px solid #dde3ea;border-radius:9px;overflow:hidden}
article th,article td{padding:8px 11px;border-bottom:1px solid #eef1f5;text-align:left;vertical-align:top}
article th{background:#f7f9fc;font-weight:700;font-size:12.5px}
article tr:last-child td{border-bottom:0}
article blockquote{margin:0 0 14px;padding:10px 15px;background:#fff8e6;border-left:4px solid #f0ad4e;
  border-radius:0 8px 8px 0}
article blockquote p:last-child{margin:0}
article hr{border:0;border-top:1px solid #dde3ea;margin:26px 0}
article a{color:#1f6feb}
article strong{color:#14204a}
mark{background:#fde68a}
@media print{#side{display:none}body{display:block}article{max-width:none}}
@media(max-width:820px){
  body{display:block}
  #side{position:static;width:auto;height:auto;max-height:46vh}
  article{padding:18px 16px 60px}
}
</style></head><body>

<nav id="side">
  <h1>📘 คู่มือ PeekaWord</h1>
  <p>__N__ เอกสาร · เปิดได้ทุกเครื่อง ไม่ต้องต่อเน็ต</p>
  <input type="search" id="q" placeholder="ค้นหาในทุกเอกสาร…" autocomplete="off">
  <div class="g">🔧 เครื่องมือ (ไฟล์แยก)</div>
  <a href="wordlist.html" target="_blank">คำศัพท์ทั้ง 3,000 คำ</a>
  <a href="story_prompts.html" target="_blank">เนื้อเรื่อง + prompt 448 วัน</a>
  <a href="images/review.html" target="_blank">ตรวจรูปคำศัพท์</a>
  <a href="check_backend.html" target="_blank">ตรวจ Backend</a>
  <div id="nav"></div>
</nav>

<main id="main"><article id="doc"></article></main>

<script>
const D = /*DATA*/;

/* ── ตัวแปลง Markdown เล็ก ๆ (ไม่ต้องโหลดไลบรารีจากเน็ต) ── */
function esc(s){ return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;'); }

function inline(s){
  return esc(s)
    .replace(/`([^`]+)`/g, (m,a)=>'<code>'+a+'</code>')
    .replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')
    .replace(/(^|[^*])\*([^*\n]+)\*/g, '$1<em>$2</em>')
    .replace(/~~([^~]+)~~/g, '<del>$1</del>')
    .replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank" rel="noopener">$1</a>')
    .replace(/(^|\s)(https?:\/\/[^\s<)]+)/g, '$1<a href="$2" target="_blank" rel="noopener">$2</a>');
}

function md(src){
  const L = src.replace(/\r/g,'').split('\n');
  let out = [], i = 0;
  while (i < L.length){
    let l = L[i];

    if (/^```/.test(l)){                       // โค้ดบล็อก
      let buf = []; i++;
      while (i < L.length && !/^```/.test(L[i])) buf.push(L[i++]);
      i++;
      out.push('<pre><code>' + esc(buf.join('\n')) + '</code></pre>');
      continue;
    }
    if (/^\s*\|.*\|\s*$/.test(l) && /^\s*\|[\s:|-]+\|\s*$/.test(L[i+1]||'')){   // ตาราง
      const cells = r => r.trim().replace(/^\||\|$/g,'').split('|').map(c=>c.trim());
      const head = cells(l); i += 2;
      let rows = [];
      while (i < L.length && /^\s*\|.*\|\s*$/.test(L[i])) rows.push(cells(L[i++]));
      out.push('<table><thead><tr>' + head.map(c=>'<th>'+inline(c)+'</th>').join('') +
        '</tr></thead><tbody>' +
        rows.map(r=>'<tr>'+r.map(c=>'<td>'+inline(c)+'</td>').join('')+'</tr>').join('') +
        '</tbody></table>');
      continue;
    }
    if (/^#{1,6}\s/.test(l)){                  // หัวข้อ
      const n = l.match(/^#+/)[0].length;
      out.push('<h'+n+'>' + inline(l.replace(/^#+\s*/,'')) + '</h'+n+'>'); i++; continue;
    }
    if (/^(-{3,}|\*{3,}|_{3,})\s*$/.test(l)){ out.push('<hr>'); i++; continue; }
    if (/^>\s?/.test(l)){                      // อ้างอิง
      let buf = [];
      while (i < L.length && /^>\s?/.test(L[i])) buf.push(L[i++].replace(/^>\s?/,''));
      out.push('<blockquote>' + md(buf.join('\n')) + '</blockquote>'); continue;
    }
    if (/^\s*([-*+]|\d+\.)\s/.test(l)){        // รายการ
      const ord = /^\s*\d+\./.test(l);
      let buf = [];
      while (i < L.length && /^\s*([-*+]|\d+\.)\s/.test(L[i]))
        buf.push(L[i++].replace(/^\s*([-*+]|\d+\.)\s/,''));
      out.push('<'+(ord?'ol':'ul')+'>' + buf.map(x=>'<li>'+inline(x)+'</li>').join('') +
               '</'+(ord?'ol':'ul')+'>');
      continue;
    }
    if (!l.trim()){ i++; continue; }
    let buf = [];                              // ย่อหน้า
    while (i < L.length && L[i].trim() && !/^(#{1,6}\s|```|>|\s*([-*+]|\d+\.)\s|\s*\|)/.test(L[i]))
      buf.push(L[i++]);
    out.push('<p>' + inline(buf.join(' ')) + '</p>');
  }
  return out.join('\n');
}

/* ── เมนู ── */
const nav = document.getElementById('nav');
function buildNav(filter){
  let h = '';
  for (const g of D.groups){
    const items = g.k.filter(k => !filter ||
      k.toLowerCase().includes(filter) || D.docs[k].toLowerCase().includes(filter));
    if (!items.length) continue;
    h += '<div class="g">' + g.t + '</div>';
    for (const k of items)
      h += '<a href="#'+encodeURIComponent(k)+'" data-k="'+k+'">'+k.replace(/_/g,' ')+'</a>';
  }
  nav.innerHTML = h || '<div class="g">ไม่พบเอกสารที่ค้นหา</div>';
}

function show(k){
  if (!D.docs[k]) return;
  document.getElementById('doc').innerHTML = md(D.docs[k]);
  document.querySelectorAll('#side a').forEach(a =>
    a.classList.toggle('on', a.dataset.k === k));
  document.getElementById('main').scrollTop = 0;
  window.scrollTo(0,0);
}

addEventListener('hashchange', () => show(decodeURIComponent(location.hash.slice(1))));
document.getElementById('q').addEventListener('input', e => buildNav(e.target.value.trim().toLowerCase()));

buildNav('');
const first = location.hash ? decodeURIComponent(location.hash.slice(1)) : D.groups[0].k[0];
show(D.docs[first] ? first : D.groups[0].k[0]);
</script>
</body></html>"""

if __name__ == '__main__':
    main()
