# -*- coding: utf-8 -*-
"""
สร้างหน้าไล่ดูรูปทีละคำ เพื่อหารูปที่ "ไม่ตรงความหมาย"
กดการ์ดเพื่อทำเครื่องหมาย ❌ แล้วกดปุ่มโหลดรายการออกมาเป็น CSV

รัน:   py _docs/make_review.py
เปิด:  _docs/images/review.html
"""
import os, csv, json, html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG  = os.path.join(ROOT, 'img', 'words')
OUT  = os.path.join(ROOT, '_docs', 'images', 'review.html')


def slug(s):
    return ''.join(c for c in s.lower() if c.isalnum())


rows = list(csv.DictReader(open(os.path.join(ROOT, '_docs', 'wordlist_master.csv'),
                               encoding='utf-8-sig')))
have = {os.path.splitext(f)[0] for f in os.listdir(IMG)} if os.path.isdir(IMG) else set()

data = []
for r in rows:
    k = slug(r['english'])
    if k in have:
        data.append({'k': k, 'w': r['english'], 't': r['thai'],
                     'd': int(r['day']), 'c': r['cefr']})
data.sort(key=lambda x: (x['d'], x['w'].lower()))

os.makedirs(os.path.dirname(OUT), exist_ok=True)
open(OUT, 'w', encoding='utf-8').write(r"""<!DOCTYPE html>
<html lang="th"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>ตรวจรูปคำศัพท์ · PeekaWord</title>
<style>
*{box-sizing:border-box}
body{margin:0;font-family:-apple-system,"Segoe UI",Tahoma,sans-serif;background:#f4f6f9;color:#28323e}
header{background:#1f3b57;color:#fff;padding:16px 20px}
header h1{margin:0 0 4px;font-size:19px}
header p{margin:0;font-size:12.5px;opacity:.85}
.bar{position:sticky;top:0;z-index:9;background:#fff;border-bottom:1px solid #dde3ea;
 padding:10px 20px;display:flex;gap:8px;flex-wrap:wrap;align-items:center}
.bar select,.bar button,.bar input{padding:7px 11px;border:1px solid #cbd5e1;border-radius:8px;
 background:#fff;font-size:13px;cursor:pointer}
.bar .n{margin-left:auto;font-size:13px;color:#64748b}
.bar .bad{color:#d1573a;font-weight:700}
main{padding:14px 20px 60px}
h2{margin:18px 0 8px;font-size:13.5px;color:#475569}
.g{display:grid;grid-template-columns:repeat(auto-fill,minmax(118px,1fr));gap:10px}
figure{margin:0;background:#fff;border:2px solid #dde3ea;border-radius:11px;padding:7px;
 text-align:center;cursor:pointer;user-select:none;position:relative}
figure.x{border-color:#e76f51;background:#fff3f0}
figure.x::after{content:"❌";position:absolute;top:4px;right:6px;font-size:15px}
img{width:100%;aspect-ratio:1;object-fit:cover;border-radius:8px;display:block;background:#eef1f5}
b{display:block;font-size:13px;margin-top:5px}
span{display:block;font-size:11px;color:#64748b}
</style></head><body>
<header><h1>🔍 ตรวจรูปคำศัพท์</h1>
<p>กดการ์ดที่รูป<b>ไม่ตรงความหมาย</b> → กด "โหลดรายการ" เพื่อเอาไปสร้างรูปใหม่</p></header>
<div class="bar">
 <select id="fc"><option value="">ทุกระดับ</option><option>A1</option><option>A2</option>
 <option>B1</option><option>B2</option></select>
 <select id="fd"><option value="">ทุกวัน</option><option value="1-7">Day 1–7</option>
 <option value="1-30">Day 1–30</option><option value="31-100">Day 31–100</option>
 <option value="101-250">Day 101–250</option></select>
 <button onclick="dl()">⬇ โหลดรายการที่ติดธง</button>
 <button onclick="clr()">ล้างธง</button>
 <span class="n"><span id="cnt"></span> · ติดธง <span class="bad" id="bad">0</span></span>
</div>
<main id="out"></main>
<script>
const D = __DATA__;
const KEY='pw_review_bad';
let bad = new Set(JSON.parse(localStorage.getItem(KEY)||'[]'));
function save(){ localStorage.setItem(KEY, JSON.stringify([...bad]));
  document.getElementById('bad').textContent = bad.size; }
function sel(){
  const c=document.getElementById('fc').value, dr=document.getElementById('fd').value;
  let a=0,b=9999; if(dr){const p=dr.split('-');a=+p[0];b=+p[1];}
  return D.filter(x=>(!c||x.c===c)&&x.d>=a&&x.d<=b);
}
function render(){
  const rows=sel(); document.getElementById('cnt').textContent=rows.length+' รูป';
  let h='',cur=null;
  for(const x of rows){
    if(x.d!==cur){ if(cur!==null)h+='</div>'; cur=x.d;
      h+='<h2>Day '+x.d+' · '+x.c+'</h2><div class="g">'; }
    h+='<figure data-k="'+x.k+'" class="'+(bad.has(x.k)?'x':'')+'" onclick="tog(this)">'+
       '<img src="../../img/words/'+x.k+'.webp" loading="lazy" alt="">'+
       '<b>'+x.w+'</b><span>'+x.t+'</span></figure>';
  }
  document.getElementById('out').innerHTML=h+'</div>'; save();
}
function tog(el){ const k=el.dataset.k;
  if(bad.has(k)){bad.delete(k);el.classList.remove('x');}else{bad.add(k);el.classList.add('x');}
  save(); }
function clr(){ bad.clear(); save(); render(); }
function dl(){
  const m=new Map(D.map(x=>[x.k,x]));
  let s='﻿day,cefr,english,thai,filename\n';
  [...bad].map(k=>m.get(k)).filter(Boolean).sort((a,b)=>a.d-b.d)
    .forEach(x=>s+=[x.d,x.c,'"'+x.w+'"','"'+x.t+'"',x.k+'.webp'].join(',')+'\n');
  const u=URL.createObjectURL(new Blob([s],{type:'text/csv;charset=utf-8'}));
  const a=document.createElement('a'); a.href=u; a.download='รูปที่ต้องแก้.csv'; a.click();
  URL.revokeObjectURL(u);
}
['fc','fd'].forEach(i=>document.getElementById(i).addEventListener('change',render));
render();
</script></body></html>""".replace('__DATA__', json.dumps(data, ensure_ascii=False,
                                                          separators=(',', ':'))))
print('เขียน %s  (%d รูป)' % (OUT, len(data)))
