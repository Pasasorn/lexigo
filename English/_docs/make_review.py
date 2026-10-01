#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""สร้างหน้าไล่ดูรูปทีละคำ — กดปุ่มทำเครื่องหมาย "ไม่ตรง" แล้ว export รายการไปค้นใหม่
   ใช้:  python make_review.py   แล้วเปิด _docs/images/review.html"""
import os, csv, json, html
HERE = os.path.dirname(os.path.abspath(__file__))
MAN  = os.path.join(HERE, 'images', 'manifest.csv')
OUTF = os.path.join(HERE, 'images', 'review.html')
if not os.path.exists(MAN):
    raise SystemExit('ยังไม่มี manifest.csv — รัน fetch_images.py ก่อน')

rows = [r for r in csv.DictReader(open(MAN, encoding='utf-8-sig')) if r['status'] == 'OK']
rows.sort(key=lambda r: (int(r['day']), r['word']))
data = [{'w': r['word'], 'd': r['day'], 'c': r['cefr'], 's': r['source']} for r in rows]

tpl = """<!DOCTYPE html><html lang="th"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>ตรวจรูปคำศัพท์</title>
<style>
body{font-family:system-ui,'Segoe UI',sans-serif;background:#FAFAFA;margin:0;padding:18px;color:#37474F}
h1{font-size:20px;margin:0 0 4px}
.bar{position:sticky;top:0;background:#FAFAFA;padding:10px 0 14px;z-index:5;border-bottom:1px solid #E0E0E0;margin-bottom:14px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:12px}
.card{background:#fff;border:2px solid #E8E8E8;border-radius:12px;padding:8px;text-align:center;cursor:pointer}
.card.bad{border-color:#E53935;background:#FFEBEE}
.card img{width:100%;aspect-ratio:1;object-fit:cover;border-radius:8px;display:block;background:#F0F0F0}
.w{font-weight:800;font-size:15px;margin-top:6px}
.m{font-size:11px;color:#90A4AE}
button{font:inherit;font-weight:700;padding:9px 16px;border-radius:9px;border:1.5px solid #CFD8DC;background:#fff;cursor:pointer}
#out{width:100%;height:110px;margin-top:10px;font-family:ui-monospace,monospace;font-size:12px;display:none}
</style></head><body>
<div class="bar">
  <h1>ตรวจรูปคำศัพท์ — __N__ รูป</h1>
  <div class="m" style="margin-bottom:8px">คลิกการ์ดที่ <b>รูปไม่ตรงความหมาย</b> ให้เป็นสีแดง แล้วกดปุ่มด้านล่าง</div>
  <button onclick="exportBad()">📋 คัดลอกรายการที่ต้องหาใหม่</button>
  <span id="cnt" class="m"></span>
  <textarea id="out"></textarea>
</div>
<div class="grid" id="g"></div>
<script>
const D=__DATA__, bad=new Set();
const g=document.getElementById('g');
g.innerHTML=D.map(x=>`<div class="card" data-w="${x.w}">
  <img src="../../img/words/${x.w}.webp" alt="${x.w}" loading="lazy">
  <div class="w">${x.w}</div><div class="m">Day ${x.d} · ${x.c} · ${x.s}</div></div>`).join('');
g.onclick=e=>{const c=e.target.closest('.card'); if(!c)return;
  const w=c.dataset.w; c.classList.toggle('bad');
  c.classList.contains('bad')?bad.add(w):bad.delete(w);
  document.getElementById('cnt').textContent=' · ทำเครื่องหมายไว้ '+bad.size+' คำ';};
function exportBad(){
  const o=document.getElementById('out');
  o.style.display='block';
  o.value='word,query\\n'+[...bad].map(w=>w+',').join('\\n');
  o.select();
  try{document.execCommand('copy')}catch(e){}
  alert(bad.size+' คำ — วางลงไฟล์ _docs/images/search_overrides.csv แล้วเติมคำค้นใหม่ในช่องหลัง จากนั้นรัน\\n\\npython fetch_images.py --days 1-7 --force');
}
</script></body></html>"""
open(OUTF, 'w', encoding='utf-8').write(
    tpl.replace('__DATA__', json.dumps(data, ensure_ascii=False)).replace('__N__', str(len(data))))
print(f'สร้างแล้ว: {OUTF}  ({len(data)} รูป)')
