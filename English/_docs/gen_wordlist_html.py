# -*- coding: utf-8 -*-
"""
สร้างหน้าเปิดดูคำศัพท์ทั้ง 3,000 คำเป็น HTML ไฟล์เดียว (เปิดออฟไลน์ได้)
ผลลัพธ์: _docs/wordlist.html

วิธีรัน:  python _docs/gen_wordlist_html.py
"""
import csv, json, os, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC  = os.path.join(ROOT, '_docs', 'wordlist_master.csv')
IMG  = os.path.join(ROOT, 'img', 'words')
OUT  = os.path.join(ROOT, '_docs', 'wordlist.html')

CEFR_ORDER = ['A1', 'A2', 'B1', 'B2']


def main():
    rows = list(csv.DictReader(open(SRC, encoding='utf-8-sig')))

    have = set()
    if os.path.isdir(IMG):
        for f in os.listdir(IMG):
            have.add(os.path.splitext(f)[0].lower())

    data, lvset = [], {}
    for r in rows:
        w = r['english']
        key = ''.join(ch for ch in w.lower() if ch.isalnum())
        data.append([int(r['day']), int(r['level']), r['cefr'], w,
                     r['thai'], r['ipa'], r['emoji'], 1 if key in have else 0])
        lvset.setdefault(int(r['level']), r['cefr'])

    data.sort(key=lambda x: (x[0], x[3].lower()))

    stats = collections.Counter(d[2] for d in data)
    pics  = sum(d[7] for d in data)
    levels = [{'n': k, 'cefr': lvset[k],
               'd0': min(x[0] for x in data if x[1] == k),
               'd1': max(x[0] for x in data if x[1] == k),
               'c': sum(1 for x in data if x[1] == k)}
              for k in sorted(lvset)]

    meta = {'total': len(data), 'pics': pics,
            'cefr': {c: stats.get(c, 0) for c in CEFR_ORDER},
            'levels': levels, 'maxDay': max(d[0] for d in data)}

    html = TPL.replace('/*DATA*/', json.dumps(data, ensure_ascii=False, separators=(',', ':'))) \
              .replace('/*META*/', json.dumps(meta, ensure_ascii=False))
    open(OUT, 'w', encoding='utf-8').write(html)
    print('เขียน %s  (%d คำ · มีภาพแล้ว %d)' % (OUT, len(data), pics))
    print('ขนาด %.0f KB' % (os.path.getsize(OUT) / 1024))


TPL = r"""<!DOCTYPE html>
<html lang="th"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>PeekaWord · คำศัพท์ทั้งหมด 3,000 คำ</title>
<style>
*{box-sizing:border-box}
body{margin:0;font-family:-apple-system,"Segoe UI",Tahoma,sans-serif;background:#f4f6f9;color:#28323e}
header{background:#1f3b57;color:#fff;padding:18px 20px 0}
header h1{margin:0 0 4px;font-size:20px}
header p{margin:0 0 14px;font-size:13px;opacity:.85}
.kpi{display:flex;gap:9px;flex-wrap:wrap;padding-bottom:16px}
.kpi div{background:rgba(255,255,255,.13);border-radius:9px;padding:7px 13px;font-size:12.5px}
.kpi b{display:block;font-size:17px;line-height:1.3}
.bar{position:sticky;top:0;z-index:9;background:#fff;border-bottom:1px solid #dde3ea;
  padding:11px 20px;display:flex;gap:9px;flex-wrap:wrap;align-items:center}
.bar input[type=search]{flex:1;min-width:190px;padding:8px 12px;border:1px solid #cbd5e1;
  border-radius:8px;font-size:14px}
.bar select,.bar button{padding:8px 11px;border:1px solid #cbd5e1;border-radius:8px;
  background:#fff;font-size:13px;cursor:pointer}
.bar button:hover{background:#f1f5f9}
.bar .cnt{font-size:12.5px;color:#64748b;margin-left:auto}
main{max-width:1180px;margin:0 auto;padding:16px 20px 60px}
h2.day{margin:22px 0 9px;font-size:14px;color:#475569;display:flex;align-items:center;gap:9px}
h2.day .tag{font-size:10.5px;font-weight:700;color:#fff;padding:2px 7px;border-radius:20px}
.A1{background:#5FB06B}.A2{background:#3b87c9}.B1{background:#7e63c4}.B2{background:#d1573a}
h2.day .lv{font-size:11.5px;color:#94a3b8;font-weight:400}
table{width:100%;border-collapse:collapse;background:#fff;border:1px solid #dde3ea;
  border-radius:11px;overflow:hidden}
th,td{padding:8px 11px;text-align:left;font-size:13.5px;border-bottom:1px solid #eef1f5}
th{background:#f7f9fc;font-size:11.5px;color:#64748b;font-weight:600;text-transform:uppercase;
  letter-spacing:.4px}
tr:last-child td{border-bottom:0}
td.ic{width:46px;text-align:center;font-size:21px;padding:4px}
td.ic img{width:38px;height:38px;border-radius:8px;display:block;margin:0 auto;object-fit:cover}
td.en{font-weight:600;width:24%}
td.ipa{color:#64748b;font-size:12.5px;width:21%;font-family:"Segoe UI",sans-serif}
td.th{width:30%}
td.pic{width:34px;text-align:center;font-size:11px}
mark{background:#fde68a;padding:0 1px;border-radius:2px}
.empty{text-align:center;padding:50px 20px;color:#94a3b8}
.more{text-align:center;margin:22px 0}
.more button{padding:10px 24px;border:1px solid #cbd5e1;background:#fff;border-radius:9px;
  cursor:pointer;font-size:14px}
@media(max-width:560px){
  td.ipa{display:none}th:nth-child(3){display:none}
  td.en{width:40%}td.th{width:46%}
}
@media print{.bar,header,.more{display:none}body{background:#fff}}
</style></head><body>

<header>
  <h1>📚 คำศัพท์ทั้งหมด · PeekaWord</h1>
  <p>Oxford 3000 · เรียงตาม CEFR ง่าย → ยาก · ไม่มีคำซ้ำ</p>
  <div class="kpi" id="kpi"></div>
</header>

<div class="bar">
  <input type="search" id="q" placeholder="ค้นหาคำอังกฤษ หรือคำแปลไทย…" autocomplete="off">
  <select id="fc"><option value="">ทุกระดับ CEFR</option></select>
  <select id="fl"><option value="">ทุก Level</option></select>
  <select id="fd">
    <option value="">ทุกวัน</option>
    <option value="1-7">Day 1–7 (ทดลองฟรี)</option>
    <option value="1-30">Day 1–30</option>
    <option value="1-100">Day 1–100</option>
    <option value="101-250">Day 101–250</option>
    <option value="251-447">Day 251–447</option>
  </select>
  <select id="fp"><option value="">ภาพ: ทั้งหมด</option>
    <option value="1">มีภาพแล้ว</option><option value="0">ยังไม่มีภาพ</option></select>
  <button onclick="reset()">ล้าง</button>
  <button onclick="csv()">⬇ CSV</button>
  <span class="cnt" id="cnt"></span>
</div>

<main id="out"></main>

<script>
var D = /*DATA*/;
var M = /*META*/;
var PAGE = 400, shown = PAGE;

/* [0]day [1]level [2]cefr [3]english [4]thai [5]ipa [6]emoji [7]hasPic */

document.getElementById('kpi').innerHTML =
  '<div><b>' + M.total.toLocaleString() + '</b>คำทั้งหมด</div>' +
  '<div><b>' + M.maxDay + '</b>วันเรียน</div>' +
  '<div><b>' + M.levels.length + '</b>Level</div>' +
  ['A1','A2','B1','B2'].map(function(c){
    return '<div><b>' + M.cefr[c].toLocaleString() + '</b>' + c + '</div>'; }).join('') +
  '<div><b>' + M.pics + '</b>มีภาพแล้ว</div>';

var fc = document.getElementById('fc'), fl = document.getElementById('fl');
['A1','A2','B1','B2'].forEach(function(c){
  fc.insertAdjacentHTML('beforeend','<option value="'+c+'">'+c+' ('+M.cefr[c]+')</option>'); });
M.levels.forEach(function(l){
  fl.insertAdjacentHTML('beforeend','<option value="'+l.n+'">Level '+l.n+' · '+l.cefr+
    ' · Day '+l.d0+'–'+l.d1+'</option>'); });

function esc(s){ return String(s).replace(/[&<>"]/g, function(c){
  return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]; }); }

function hl(s, q){
  if(!q) return esc(s);
  var i = s.toLowerCase().indexOf(q);
  if(i < 0) return esc(s);
  return esc(s.slice(0,i)) + '<mark>' + esc(s.slice(i,i+q.length)) + '</mark>' + esc(s.slice(i+q.length));
}

function slug(w){ return w.toLowerCase().replace(/[^a-z0-9]/g,''); }

function filtered(){
  var q = document.getElementById('q').value.trim().toLowerCase(),
      c = fc.value, l = fl.value, p = document.getElementById('fp').value,
      dr = document.getElementById('fd').value, d0 = 0, d1 = 9999;
  if(dr){ var a = dr.split('-'); d0 = +a[0]; d1 = +a[1]; }
  return D.filter(function(r){
    if(c && r[2] !== c) return false;
    if(l && r[1] !== +l) return false;
    if(p !== '' && r[7] !== +p) return false;
    if(r[0] < d0 || r[0] > d1) return false;
    if(q && r[3].toLowerCase().indexOf(q) < 0 && r[4].indexOf(q) < 0) return false;
    return true;
  });
}

function render(){
  var q = document.getElementById('q').value.trim().toLowerCase();
  var rows = filtered();
  document.getElementById('cnt').textContent = rows.length.toLocaleString() + ' คำ';
  var out = document.getElementById('out');
  if(!rows.length){ out.innerHTML = '<div class="empty">ไม่พบคำที่ค้นหา</div>'; return; }

  var slice = rows.slice(0, shown), h = [], curDay = null;
  slice.forEach(function(r){
    if(r[0] !== curDay){
      if(curDay !== null) h.push('</tbody></table>');
      curDay = r[0];
      h.push('<h2 class="day"><span class="tag ' + r[2] + '">' + r[2] + '</span>Day ' + r[0] +
             '<span class="lv">Level ' + r[1] + '</span></h2>' +
             '<table><thead><tr><th></th><th>คำศัพท์</th><th>คำอ่าน</th><th>ความหมาย</th><th></th>' +
             '</tr></thead><tbody>');
    }
    h.push('<tr><td class="ic">' +
      (r[7] ? '<img src="../img/words/' + slug(r[3]) + '.svg" alt="" loading="lazy" ' +
              'onerror="this.replaceWith(document.createTextNode(\'' + r[6] + '\'))">'
            : esc(r[6])) +
      '</td><td class="en">' + hl(r[3], q) + '</td>' +
      '<td class="ipa">' + esc(r[5]) + '</td>' +
      '<td class="th">' + hl(r[4], q) + '</td>' +
      '<td class="pic">' + (r[7] ? '🖼️' : '') + '</td></tr>');
  });
  h.push('</tbody></table>');
  if(rows.length > shown)
    h.push('<div class="more"><button onclick="shown+=' + PAGE + ';render()">' +
           'แสดงเพิ่ม (เหลืออีก ' + (rows.length - shown).toLocaleString() + ' คำ)</button></div>');
  out.innerHTML = h.join('');
}

function reset(){
  document.getElementById('q').value = '';
  fc.value = fl.value = document.getElementById('fd').value =
    document.getElementById('fp').value = '';
  shown = PAGE; render();
}

function csv(){
  var rows = filtered();
  var s = '﻿day,level,cefr,english,thai,ipa,emoji,has_image\n' +
    rows.map(function(r){
      return [r[0], r[1], r[2], '"'+r[3]+'"', '"'+r[4]+'"', '"'+r[5]+'"', r[6], r[7]].join(',');
    }).join('\n');
  var b = new Blob([s], {type:'text/csv;charset=utf-8'}), u = URL.createObjectURL(b),
      a = document.createElement('a');
  a.href = u; a.download = 'peekaword-words-' + rows.length + '.csv'; a.click();
  URL.revokeObjectURL(u);
}

['q','fc','fl','fd','fp'].forEach(function(id){
  document.getElementById(id).addEventListener('input', function(){ shown = PAGE; render(); });
});
render();
</script>
</body></html>"""

if __name__ == '__main__':
    main()
