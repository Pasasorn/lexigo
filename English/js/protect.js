/* PeekaWord — ลายน้ำระบุตัวตน + ชั้นป้องกันการคัดลอก
   โหลดท้ายทุกหน้า:  <script src="../js/protect.js"></script>
   หมายเหตุตามจริง: เว็บไม่มี API ตรวจจับ "การแคปหน้าจอ" ได้จริง
   สิ่งที่ไฟล์นี้ทำได้คือ (1) ลายน้ำที่ติดไปกับภาพที่แคป
   (2) ดำจอตอนสลับแอป/สลับแท็บ ซึ่งครอบคลุมเครื่องมือแคปบางตัวเท่านั้น */
(function () {
  'use strict';
  if (window.__pwProtect) return;
  window.__pwProtect = true;

  /* ── 1. ใครกำลังดูอยู่ ── */
  function who() {
    var s = {};
    try { s = JSON.parse(localStorage.getItem('wla_student') || '{}') || {}; } catch (e) {}
    var em = s.email || '';
    var cd = s.code || '';
    if (localStorage.getItem('wla_admin')) return 'ADMIN';
    if (!em && !cd) {
      return localStorage.getItem('wla_last_code') === 'TRIAL' ? 'ทดลองเรียน · TRIAL' : 'ยังไม่ได้เข้าสู่ระบบ';
    }
    return (em || '') + (em && cd ? ' · ' : '') + (cd ? '#' + cd : '');
  }

  function stamp() {
    var d = new Date();
    var p = function (n) { return (n < 10 ? '0' : '') + n; };
    return d.getFullYear() + '-' + p(d.getMonth() + 1) + '-' + p(d.getDate()) +
           ' ' + p(d.getHours()) + ':' + p(d.getMinutes());
  }

  /* ── 2. สไตล์ ── */
  var css = document.createElement('style');
  css.id = 'pw-protect-css';
  css.textContent =
    '#pw-wm{position:fixed;inset:0;z-index:2147483646;pointer-events:none;overflow:hidden;' +
      'user-select:none;-webkit-user-select:none}' +
    '#pw-wm .pw-wm-row{white-space:nowrap;font:600 12px/1 system-ui,"Nunito",sans-serif;' +
      'color:rgba(15,23,42,.11);letter-spacing:.4px;transform:rotate(-24deg);transform-origin:0 0;' +
      'position:absolute}' +
    '@media (prefers-color-scheme:dark){#pw-wm .pw-wm-row{color:rgba(255,255,255,.13)}}' +
    '#pw-black{position:fixed;inset:0;z-index:2147483647;background:#000;color:#fff;display:none;' +
      'align-items:center;justify-content:center;flex-direction:column;gap:10px;text-align:center;' +
      'font:700 16px/1.7 system-ui,"Nunito",sans-serif;padding:24px}' +
    '#pw-black.on{display:flex}' +
    '#pw-black small{font-weight:600;opacity:.75;font-size:13px}' +
    '@media print{html,body{display:none!important}}';
  document.head.appendChild(css);

  /* ── 3. ลายน้ำ ── */
  function buildWM() {
    var old = document.getElementById('pw-wm');
    if (old) old.remove();
    var wrap = document.createElement('div');
    wrap.id = 'pw-wm';
    wrap.setAttribute('aria-hidden', 'true');
    var text = who() + '   ·   ' + stamp() + '   ·   PeekaWord';
    var line = (text + '     ').repeat(6);
    var vh = window.innerHeight || 800;
    var sh = (document.body && document.body.scrollHeight) || 0;
    var H = Math.max(vh, sh) + 400;
    var rows = Math.max(8, Math.ceil(H / 118) + 4);
    var html = '';
    for (var i = 0; i < rows; i++) {
      html += '<div class="pw-wm-row" style="top:' + (i * 118 - 120) + 'px;left:' +
              (i % 2 ? -140 : -40) + 'px">' + line + '</div>';
    }
    wrap.innerHTML = html;
    document.body.appendChild(wrap);
  }

  /* ── 4. จอดำ ── */
  var black;
  function buildBlack() {
    black = document.createElement('div');
    black.id = 'pw-black';
    black.innerHTML = '<div>🔒 เนื้อหานี้เปิดได้เฉพาะผู้เรียน</div>' +
      '<small>' + who() + '</small>' +
      '<small>แตะที่นี่เพื่อเรียนต่อ</small>';
    // ทางออกฉุกเฉิน: แตะแล้วหายไป จะได้ไม่มีทางค้างจอดำจนเรียนไม่ได้
    black.addEventListener('click', function () { hide(false); });
    black.addEventListener('touchstart', function () { hide(false); });
    document.body.appendChild(black);
  }
  function hide(on) { if (black) black.classList.toggle('on', !!on); }

  /* ── 4.5 ถ้ารันอยู่ในแอปที่ห่อเว็บไว้ → สั่ง OS บล็อกการแคปจริง ──
     ได้ภาพดำจริงเฉพาะตอนอยู่ในแอป (Android FLAG_SECURE / iOS secure layer)
     บนเบราว์เซอร์ปกติจะไม่มี window.WTN โค้ดนี้จะข้ามไปเงียบๆ */
  function lockNative() {
    try {
      if (window.WTN && typeof window.WTN.disableScreenshot === 'function') {
        window.WTN.disableScreenshot({ ssKey: true });
        window.__pwNativeLock = true;
        return true;
      }
    } catch (e) {}
    return false;
  }

  /* ── 5. เริ่มทำงาน ── */
  function init() {
    buildWM();
    buildBlack();

    // bridge ของแอปอาจถูกฉีดช้ากว่าหน้าเว็บ → ลองซ้ำ
    if (!lockNative()) {
      var tries = 0;
      var t = setInterval(function () {
        if (lockNative() || ++tries > 20) clearInterval(t);
      }, 500);
    }

    // ซ่อนจอตอนสลับแอป / สลับแท็บ / เรียกเครื่องมือแคปของ Windows
    document.addEventListener('visibilitychange', function () { hide(document.hidden); });
    window.addEventListener('blur', function () { hide(true); });
    window.addEventListener('focus', function () { hide(false); });
    window.addEventListener('pageshow', function () { hide(false); });

    // ปุ่ม PrintScreen (Windows) — ดำจอ 1.2 วิ แล้วล้างคลิปบอร์ด
    document.addEventListener('keyup', function (e) {
      if (e.key === 'PrintScreen' || e.keyCode === 44) {
        hide(true);
        try { navigator.clipboard && navigator.clipboard.writeText(' '); } catch (err) {}
        setTimeout(function () { hide(false); }, 1200);
      }
    });

    // กันคีย์ลัดคัดลอก/บันทึก/พิมพ์ (กันได้แค่ระดับหนึ่ง)
    document.addEventListener('keydown', function (e) {
      var k = (e.key || '').toLowerCase();
      if ((e.ctrlKey || e.metaKey) && ['p', 's', 'u'].indexOf(k) > -1) { e.preventDefault(); }
      if (e.key === 'F12') e.preventDefault();
    });
    window.addEventListener('beforeprint', function () { hide(true); });
    window.addEventListener('afterprint', function () { hide(false); });

    // กันคลิกขวา / ลากภาพ / ลากข้อความออก
    document.addEventListener('contextmenu', function (e) { e.preventDefault(); });
    document.addEventListener('dragstart', function (e) { e.preventDefault(); });
    document.addEventListener('copy', function (e) {
      if (window.getSelection && String(window.getSelection()).length > 60) e.preventDefault();
    });

    // ถ้ามีใครลบลายน้ำทิ้ง ให้สร้างใหม่
    setInterval(function () {
      var w = document.getElementById('pw-wm');
      if (!w || !w.firstChild || getComputedStyle(w).display === 'none') buildWM();
      if (!document.getElementById('pw-protect-css')) document.head.appendChild(css);
      // กันจอดำค้าง: ถ้าหน้าเห็นอยู่และมีโฟกัสจริง ต้องไม่ดำ
      if (!document.hidden && (!document.hasFocus || document.hasFocus())) hide(false);
    }, 2500);
    window.addEventListener('resize', buildWM);
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
