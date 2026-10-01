/* PeekaWord — ภาพประกอบบนการ์ดคำศัพท์
   ลำดับการหา:  img/words/<คำ>.webp  →  img/words/<คำ>.svg  →  emoji เดิม
   ไม่ต้องแก้ไฟล์ Day ซ้ำเมื่อเพิ่มรูปใหม่ — แค่วางไฟล์รูปลงโฟลเดอร์ก็ขึ้นเอง */
(function () {
  'use strict';
  if (window.pwPic) return;

  var css = document.createElement('style');
  css.textContent =
    '.pw-ic{display:block;line-height:1}' +
    '.pw-ic img.pw-pic{width:100%;max-width:92px;aspect-ratio:1;object-fit:cover;' +
      'border-radius:12px;display:block;margin:0 auto 4px;background:#F1F1F4}' +
    '.pw-ic:has(img.pw-pic) .pw-fb{display:none}' +
    '@media(max-width:380px){.pw-ic img.pw-pic{max-width:76px}}';
  (document.head || document.documentElement).appendChild(css);

  /* .webp ไม่เจอ → ลอง .svg · .svg ไม่เจอ → ลบ img ทิ้ง เหลือ emoji */
  window.pwPicFail = function (img) {
    if (img.getAttribute('data-try') === 'svg') { img.remove(); return; }
    img.setAttribute('data-try', 'svg');
    img.src = img.src.replace(/\.webp(\?.*)?$/, '.svg');
  };

  /* word = คำศัพท์ · fallback = HTML เดิม (emoji หรือ inline svg) */
  window.pwPic = function (word, fallback) {
    var w = String(word || '').toLowerCase().replace(/[^a-z0-9]/g, '');
    if (!w) return fallback || '';
    return '<span class="pw-ic">' +
             '<img class="pw-pic" src="../img/words/' + w + '.webp" alt="" ' +
                  'loading="lazy" onerror="pwPicFail(this)">' +
             '<span class="pw-fb">' + (fallback || '') + '</span>' +
           '</span>';
  };
})();
