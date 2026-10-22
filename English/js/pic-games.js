/* PeekaWord — เอารูปคำศัพท์ (img/words/<คำ>.webp ที่ใช้ใน Step 1) มาใช้ใน Step 4–5 ด้วย
   ไม่แก้โค้ดเกมในไฟล์ Day: เฝ้าดู DOM แล้วเสริมรูปเข้าไป ถ้าไม่มีรูปก็เหลือ emoji เดิม
   - Step 5 Fill/Scramble/Vowels : #g5hint (emoji) → รูปคำที่ตรงกับ #g5thai
   - Step 5 Memory Match         : การ์ดที่เปิดแล้วเป็น emoji → รูปคำนั้น
   - Step 4 Listen + Order       : ใส่รูปเล็กของคำศัพท์ที่อยู่ในประโยค เป็นตัวช่วยนึกความหมาย
   ต้องโหลดหลัง pic.js (ใช้ window.pwPic)                                                  */
(function () {
  'use strict';
  if (window.pwPicGames) return;
  window.pwPicGames = 1;

  function words() { try { return (typeof WORDS !== 'undefined' && WORDS) || []; } catch (e) { return []; } }
  function norm(s) { return String(s || '').toLowerCase().replace(/[^a-z0-9]/g, ''); }
  function slug(w) { return norm(w); }
  function pic(w, size, fb) {
    var s = slug(w); if (!s) return fb || '';
    return '<span class="pw-ic pw-g" style="width:' + size + 'px;margin:0 auto">' +
      '<img class="pw-pic" src="../img/words/' + s + '.webp" alt="" loading="lazy" onerror="pwPicFail(this)"' +
      ' style="max-width:' + size + 'px;margin:0 auto">' +
      '<span class="pw-fb">' + (fb || '') + '</span></span>';
  }

  var css = document.createElement('style');
  css.textContent =
    '#g5hint .pw-g img.pw-pic{border-radius:14px}' +
    '.pw-s4{display:flex;gap:6px;flex-wrap:wrap;margin:0 0 8px}' +
    '.pw-s4 img{width:46px;height:46px;object-fit:cover;border-radius:10px;background:#F1F1F4;border:1.5px solid #E3E8EE}' +
    '#g5grid .pw-g img.pw-pic{width:100%;max-width:100%;aspect-ratio:1;border-radius:9px;margin:0}' +
    '#g5grid .pw-g{display:block}';
  (document.head || document.documentElement).appendChild(css);

  /* ── Step 5: hint ── */
  var lastThai = null;
  function fixHint() {
    var h = document.getElementById('g5hint'), t = document.getElementById('g5thai');
    if (!h || !t) return;
    var th = t.textContent.trim();
    if (!th || th === lastThai && h.querySelector('.pw-g')) return;
    var w = words().find(function (x) { return String(x.t || '').trim() === th; });
    if (!w) return;
    lastThai = th;
    h.innerHTML = pic(w.e, 110, w.em || '📝');
  }

  /* ── Step 5: memory match ── */
  function fixMemory() {
    var g = document.getElementById('g5grid'); if (!g) return;
    var ws = words(); if (!ws.length) return;
    var btns = g.querySelectorAll('button');
    for (var i = 0; i < btns.length; i++) {
      var b = btns[i];
      if (b.querySelector('.pw-g')) continue;          // ใส่รูปไปแล้ว (textContent ที่เกมเซ็ตทับจะลบรูปเอง)
      var txt = b.textContent.trim();
      if (!txt || txt === '?' || /[a-z]/i.test(txt)) {
        // กลับเป็น ? หรือเป็นคำอังกฤษ → ถ้ามีรูปค้างอยู่ให้เอาออก (textContent ถูกเซ็ตทับอยู่แล้ว)
        continue;
      }
      for (var j = 0; j < ws.length; j++) {
        if (String(ws[j].em || '') === txt) { b.innerHTML = pic(ws[j].e, 80, txt); break; }
      }
    }
  }

  /* ── Step 4: รูปคำศัพท์ในประโยค ── */
  function fixS4() {
    var area = document.getElementById('s4area'); if (!area) return;
    var ws = words(); if (!ws.length) return;
    var byNorm = {};
    ws.forEach(function (w) { byNorm[norm(w.e)] = w; });
    var boxes = area.children;
    for (var i = 0; i < boxes.length; i++) {
      var box = boxes[i];
      if (box.querySelector('.pw-s4')) continue;
      var btns = box.querySelectorAll('button.s4w');
      if (!btns.length) continue;
      var seen = {}, html = '';
      for (var k = 0; k < btns.length; k++) {
        var n = norm(btns[k].getAttribute('data-word'));
        // คำในประโยคอาจเป็นรูปผัน (cats, played) → ลองตัดท้าย
        var w = byNorm[n] || byNorm[n.replace(/s$/, '')] || byNorm[n.replace(/es$/, '')] ||
                byNorm[n.replace(/ed$/, '')] || byNorm[n.replace(/ing$/, '')];
        if (!w || seen[w.e]) continue;
        seen[w.e] = 1;
        html += '<img src="../img/words/' + slug(w.e) + '.webp" alt="" title="' + String(w.e).replace(/"/g, '') +
                '" loading="lazy" onerror="pwPicFail(this)">';
      }
      if (!html) continue;
      var row = document.createElement('div');
      row.className = 'pw-s4';
      row.innerHTML = html;
      // วางใต้แถว Listen (ลูกคนแรกของกล่อง)
      var first = box.firstElementChild;
      if (first && first.nextSibling) box.insertBefore(row, first.nextSibling); else box.appendChild(row);
    }
  }

  function run() { try { fixHint(); fixMemory(); fixS4(); } catch (e) {} }
  function start() {
    run();
    try { new MutationObserver(run).observe(document.body, { childList: true, subtree: true, characterData: true }); } catch (e) {}
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start); else start();
})();
