/* PeekaWord — เติมหมายเหตุ "คำนี้คล้ายกับคำที่เรียนไปแล้ว" ลงในการ์ดคำศัพท์

   ปัญหาที่แก้: มีคำอังกฤษ 58 คำที่แปลไทยตรงกับคำที่เคยเรียนไปก่อนหน้า
   เช่น vulnerable (Day 230) แปลว่า "เปราะบาง" เหมือน fragile (Day 212)
   ถ้าไม่บอก เด็กจะคิดว่าเรียนซ้ำ · บอกแล้วกลายเป็นจุดให้สังเกตความต่าง

   ชี้ย้อนหลังอย่างเดียว ไม่เอ่ยถึงคำที่ยังไม่ได้เรียน
   ข้อความเป็นคำชวนสังเกต ไม่ได้ฟันธงกฎการใช้ เพราะความต่างของคำพ้อง
   ขึ้นกับบริบท ซึ่งเด็กจะเห็นเองจากเรื่องที่อ่าน                              */
(function () {
  'use strict';
  if (window.pwSynReady) return;
  window.pwSynReady = 1;

  function norm(s) {
    return String(s || '').toLowerCase().replace(/[^a-z0-9]/g, '');
  }

  function addStyle() {
    if (document.getElementById('pw-syn-css')) return;
    var st = document.createElement('style');
    st.id = 'pw-syn-css';
    st.textContent =
      '.pw-syn{margin-top:7px;padding:6px 8px;border-radius:9px;' +
      'background:#F1F5FF;border:1px solid #C7D5FF;' +
      'font-size:11px;font-weight:700;color:#3A4F8A;line-height:1.5}' +
      '.pw-syn b{color:#1E3A8A}';
    document.head.appendChild(st);
  }

  function decorate() {
    var map = window.PW_SYN;
    if (!map) return;
    var cards = document.querySelectorAll('.ac');
    for (var i = 0; i < cards.length; i++) {
      var card = cards[i];
      if (card.querySelector('.pw-syn')) continue;      // ใส่ไปแล้ว
      var en = card.querySelector('.ac-en');
      if (!en) continue;
      var hit = map[norm(en.textContent)];              // ตัด 🔊 และช่องว่างออกเอง
      if (!hit) continue;
      var d = document.createElement('div');
      d.className = 'pw-syn';
      // คำตระกูลเดียวกัน (motivate/motivating) ต้องบอกคนละแบบกับคำพ้อง (fragile/vulnerable)
      d.innerHTML = hit.kin
        ? '💡 มาจากคำเดียวกับ <b>' + hit.w + '</b> (Day ' + hit.d + ')'
        : '💡 แปลเหมือน <b>' + hit.w + '</b> (Day ' + hit.d + ') — ' +
          'ลองสังเกตว่าใช้ต่างกันยังไงในเรื่องวันนี้';
      card.appendChild(d);
    }
  }

  function start() {
    addStyle();
    decorate();
    // การ์ดถูกสร้างหลังปลดล็อกบทเรียน จึงต้องเฝ้าดูจนกว่าจะโผล่
    var box = document.getElementById('cvA') || document.body;
    try {
      new MutationObserver(decorate).observe(box, { childList: true, subtree: true });
    } catch (e) {}
  }

  if (document.readyState === 'loading')
    document.addEventListener('DOMContentLoaded', start);
  else start();
})();
