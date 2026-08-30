/* PeekaWord — เก็บผลรายทักษะ + สรุปผลการเรียน
   โหลดในทุกหน้า Day (เก็บข้อมูล) และใน report.html (อ่านข้อมูล)

   เก็บอะไร: เฉพาะคะแนนที่ระบบวัดได้จริงเท่านั้น
     read  = Step 2 อ่านออกเสียงทั้งเรื่อง   (step2Score)
     speak = Step 3 พูดตามทีละประโยค        (recScores เฉลี่ย)
     write = Step 4 ฟังแล้วเขียนตามคำบอก    (step4Score)
   Step 1 (ฟังอย่างเดียว) กับ Step 5 (เกม) ไม่ได้ให้คะแนนเป็น % จึงไม่นำมาสรุป
   ถ้าเด็กข้ามขั้นไหน จะบันทึกเป็น null — รายงานจะบอกว่า "ยังไม่มีข้อมูล" ไม่เดาแทน */
(function () {
  'use strict';
  var KEY = 'pw_skills';

  function clamp(v) {
    v = parseInt(v, 10);
    return isNaN(v) ? null : Math.max(0, Math.min(100, v));
  }
  function gv(n) { try { return window[n]; } catch (e) { return undefined; } }

  function load() {
    try { return JSON.parse(localStorage.getItem(KEY) || '{}') || {}; }
    catch (e) { return {}; }
  }
  function save(o) {
    try { localStorage.setItem(KEY, JSON.stringify(o)); } catch (e) {}
  }

  /* เรียกตอนกดจบวัน — เก็บคะแนนรายทักษะของวันนั้น */
  window.pwCollect = function (day) {
    day = parseInt(day, 10);
    if (!day) return;

    var speak = null;
    var rs = gv('recScores');
    if (Object.prototype.toString.call(rs) === '[object Array]') {
      var done = [];
      for (var i = 0; i < rs.length; i++) {
        if (typeof rs[i] === 'number' && !isNaN(rs[i])) done.push(rs[i]);
      }
      if (done.length) {
        var sum = 0;
        for (var j = 0; j < done.length; j++) sum += done[j];
        speak = clamp(Math.round(sum / done.length));
      }
    }

    var rec = {
      read:  clamp(gv('step2Score')),
      speak: speak,
      write: clamp(gv('step4Score')),
      at:    new Date().toISOString().slice(0, 10)
    };

    // คะแนนรวมของวัน: ใช้ของระบบถ้ามี ไม่มีก็เฉลี่ยจากทักษะที่ทำจริง
    var tot = gv('_pwTot'), sc = gv('_pwScore');
    if (typeof tot === 'number' && tot > 0 && typeof sc === 'number') {
      rec.total = clamp(Math.round(sc / tot * 100));
    } else {
      var vals = [];
      if (rec.read  !== null) vals.push(rec.read);
      if (rec.speak !== null) vals.push(rec.speak);
      if (rec.write !== null) vals.push(rec.write);
      if (vals.length) {
        var s2 = 0;
        for (var k = 0; k < vals.length; k++) s2 += vals[k];
        rec.total = clamp(Math.round(s2 / vals.length));
        // 5 วันแรก ๆ ที่ระบบเดิมไม่ได้ตั้ง _pwScore → เติมให้ pwPct() ใช้ได้ถูกต้อง
        window._pwScore = rec.total;
        window._pwTot = 100;
      } else {
        rec.total = null;
      }
    }

    var all = load();
    var old = all[day];
    // เล่นซ้ำ: เก็บผลที่ดีที่สุดของแต่ละทักษะ ไม่ลงโทษการฝึกซ้ำ
    if (old) {
      ['read', 'speak', 'write', 'total'].forEach(function (f) {
        if (old[f] !== null && old[f] !== undefined &&
            (rec[f] === null || old[f] > rec[f])) rec[f] = old[f];
      });
    }
    all[day] = rec;
    save(all);
  };

  /* สรุปผล — ใช้ในหน้ารายงาน */
  window.pwSummary = function (fromDay, toDay) {
    var all = load(), days = [];
    for (var d = (fromDay || 1); d <= (toDay || 448); d++) if (all[d]) days.push(d);

    function stat(field) {
      var v = [];
      for (var i = 0; i < days.length; i++) {
        var x = all[days[i]][field];
        if (typeof x === 'number') v.push(x);
      }
      if (!v.length) return { n: 0, avg: null, first: null, last: null, trend: null };
      var sum = 0;
      for (var j = 0; j < v.length; j++) sum += v[j];
      var avg = Math.round(sum / v.length);
      var trend = null;
      if (v.length >= 4) {
        var h = Math.floor(v.length / 2), a = 0, b = 0;
        for (var p = 0; p < h; p++) a += v[p];
        for (var q = v.length - h; q < v.length; q++) b += v[q];
        trend = Math.round(b / h) - Math.round(a / h);
      }
      return { n: v.length, avg: avg, first: v[0], last: v[v.length - 1], trend: trend };
    }

    return {
      daysDone: days.length,
      days: days,
      read:  stat('read'),
      speak: stat('speak'),
      write: stat('write'),
      total: stat('total')
    };
  };

  /* ต่อท้าย URL ตอน syncToCloud เพื่อเก็บคะแนนรายทักษะไว้บนคลาวด์ด้วย */
  window.pwSkillQS = function (day) {
    var r = load()[parseInt(day, 10)];
    if (!r) return '';
    var q = '';
    if (r.read  !== null && r.read  !== undefined) q += '&sk_r=' + r.read;
    if (r.speak !== null && r.speak !== undefined) q += '&sk_s=' + r.speak;
    if (r.write !== null && r.write !== undefined) q += '&sk_w=' + r.write;
    return q;
  };

  /* รับข้อมูลที่ดึงกลับมาจากคลาวด์ (ตอน login) มารวมกับของในเครื่อง */
  window.pwMergeCloud = function (obj) {
    if (!obj || typeof obj !== 'object') return;
    var all = load(), changed = false;
    Object.keys(obj).forEach(function (k) {
      var d = parseInt(String(k).replace(/^d/, ''), 10);
      if (!d) return;
      var c = obj[k] || {};
      var cur = all[d] || { read: null, speak: null, write: null, total: null, at: '' };
      ['read', 'speak', 'write', 'total'].forEach(function (f) {
        var v = parseInt(c[f], 10);
        if (!isNaN(v) && (cur[f] === null || cur[f] === undefined || v > cur[f])) {
          cur[f] = v; changed = true;
        }
      });
      all[d] = cur;
    });
    if (changed) save(all);
  };

  /* ขอให้เบราว์เซอร์ไม่ล้างข้อมูลนี้ทิ้งอัตโนมัติ (Chrome/Edge/Android อนุมัติถ้าใช้งานสม่ำเสมอ) */
  try {
    if (navigator.storage && navigator.storage.persist && navigator.storage.persisted) {
      navigator.storage.persisted().then(function (already) {
        if (!already) navigator.storage.persist();
      });
    }
  } catch (e) {}

  window.pwSkillsRaw = load;
})();
