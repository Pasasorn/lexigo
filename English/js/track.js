/* PeekaWord — ติดตาม funnel แบบไม่เก็บข้อมูลส่วนตัว
   ใช้คู่กับ Cloudflare Web Analytics (เปิดจาก dashboard ไม่ต้องแก้โค้ด)

   วิธีทำงาน: เปลี่ยน path ชั่วคราวด้วย history.pushState เมื่อถึงจุดสำคัญ
   → Cloudflare นับเป็น page view แยก ทำให้เห็นว่าคนหลุดตรงไหน

   ไม่เก็บชื่อ อีเมล รหัสนักเรียน หรืออะไรที่ระบุตัวตนได้
   ไม่ส่งข้อมูลออกนอก Cloudflare */
(function () {
  'use strict';
  if (window.pwTrack) return;

  var sent = {};                      // กันนับซ้ำในหน้าเดียว
  var base = location.pathname;

  function hit(name) {
    if (!name || sent[name]) return;
    sent[name] = 1;
    try {
      history.pushState(null, '', base + '?e=' + encodeURIComponent(name));
      history.replaceState(null, '', base);   // คืน URL เดิมทันที ผู้ใช้ไม่เห็นอะไรเปลี่ยน
    } catch (e) {}
  }
  window.pwTrack = hit;

  /* ── จุดที่นับอัตโนมัติ ── */
  document.addEventListener('DOMContentLoaded', function () {
    var p = location.pathname;

    // หน้าแรก — ดูราคา / กดทดลอง
    if (/\/English\/(index\.html)?$/.test(p)) {
      hit('home');
      document.addEventListener('click', function (ev) {
        var a = ev.target.closest && ev.target.closest('a[href]');
        if (!a) return;
        var h = a.getAttribute('href') || '';
        if (/trial/.test(h))    hit('click_trial');
        if (/register/.test(h)) hit('click_package');
        if (/login/.test(h))    hit('click_login');
      }, true);

      // เลื่อนถึงส่วนราคา
      var price = document.querySelector('.prices, .seats');
      if (price && 'IntersectionObserver' in window) {
        new IntersectionObserver(function (es, o) {
          if (es[0].isIntersecting) { hit('see_price'); o.disconnect(); }
        }, { threshold: 0.3 }).observe(price);
      }
    }

    if (/trial/.test(p))    hit('trial_page');
    if (/register/.test(p)) hit('register_page');
    if (/report/.test(p))   hit('report_page');
    if (/login/.test(p))    hit('login_page');

    // หน้าบทเรียน — นับเมื่อเริ่มและเมื่อถึงแต่ละขั้น
    var m = p.match(/Day(\d+)/);
    if (m) {
      var day = parseInt(m[1], 10);
      hit('day' + day + '_open');
      var seen = {};
      setInterval(function () {
        var on = document.querySelector('.page.on, .page:not([style*="display: none"])');
        if (!on || !on.id) return;
        var s = on.id.replace('p', '');
        if (s === '0' || seen[s]) return;
        seen[s] = 1;
        hit('step' + s);
        if (s === '5') hit('day' + day + '_done');
      }, 1500);
    }
  });
})();
