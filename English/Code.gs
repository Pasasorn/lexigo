// ============================================================
//  Oxford 3000 Word Adventure — Google Apps Script Backend
//  v3: Quiz Competition + Slipok payment + Speed Heroes streak
// ============================================================

const SHEET_STUDENTS  = 'Students';
const SHEET_PROGRESS  = 'Progress';
const SHEET_CONFIG    = 'Config';
const SHEET_QUIZ_ATT  = 'QuizAttempts';   // code | free_used | paid_credits | updated_at
const SHEET_QUIZ_SCR  = 'QuizScores';     // code | score | attempt_num | saved_at
const SHEET_SLIPS     = 'UsedSlips';      // trans_ref | code | amount | used_at
const SHEET_PURCHASES = 'Purchases';    // order_id | name | phone | line_id | email | pkg_name | price | type | status | slip_url | created_at | student_code
const TEACHER_PASS   = 'oxford2026';  // ← เปลี่ยนได้

// ── Helper ───────────────────────────────────────────────────
function getSheet(name) {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  let sh = ss.getSheetByName(name);
  if (!sh) {
    sh = ss.insertSheet(name);
    if (name === SHEET_STUDENTS) {
      sh.appendRow(['student_code','nickname','email','status','registered_at','added_by','type','pkg_name','expiry_date']);
      // status: pending | active | deleted
      // type: lifetime | annual | level
      // expiry_date: ISO string (เฉพาะ annual), ว่างถ้าเป็น lifetime/level
      sh.setFrozenRows(1);
    }
    if (name === SHEET_PROGRESS) {
      sh.appendRow(['student_code','day','completion_code','saved_at','score']);
      sh.setFrozenRows(1);
    }
    if (name === SHEET_CONFIG) {
      sh.appendRow(['key','value']);
      sh.appendRow(['leaderboard_open','false']);
      sh.appendRow(['competition_days','30']);
      sh.appendRow(['slipok_api_key','YOUR_SLIPOK_KEY_HERE']);
      sh.appendRow(['promptpay_number','0812345678']);  // ← ใส่เบอร์/เลขบัญชีของครู
      sh.appendRow(['early_bird_slots','6']);
      sh.appendRow(['quiz_free_attempts','3']);
      sh.appendRow(['quiz_paid_price','29']);
      sh.appendRow(['competition_start','2026-07-01']);  // ← วันเริ่ม
      sh.appendRow(['competition_end',  '2026-07-30']);  // ← วันสิ้นสุด
      sh.appendRow(['pts_attendance','10']);    // คะแนนเข้าเรียน/วัน
      sh.appendRow(['pts_per_correct','5']);    // คะแนนต่อข้อที่ถูก
      sh.appendRow(['pts_streak_7','50']);      // โบนัส streak 7 วันติด
      sh.appendRow(['pts_streak_30','200']);    // โบนัส streak 30 วันติด
      sh.setFrozenRows(1);
    }
    if (name === SHEET_QUIZ_ATT) {
      sh.appendRow(['student_code','free_used','paid_credits','updated_at']);
      sh.setFrozenRows(1);
    }
    if (name === SHEET_QUIZ_SCR) {
      sh.appendRow(['student_code','score','attempt_num','saved_at']);
      sh.setFrozenRows(1);
    }
    if (name === SHEET_SLIPS) {
      sh.appendRow(['trans_ref','student_code','amount','used_at']);
      sh.setFrozenRows(1);
    }
    if (name === SHEET_PURCHASES) {
      sh.appendRow(['order_id','name','phone','line_id','email','pkg_name','price','type','status','slip_url','created_at','student_code']);
      sh.setFrozenRows(1);
    }
  }
  return sh;
}

function getConfig(key) {
  const sh   = getSheet(SHEET_CONFIG);
  const data = sh.getDataRange().getValues();
  for (let i = 1; i < data.length; i++) {
    if (data[i][0] === key) return data[i][1].toString();
  }
  return null;
}

function getConfigAll() {
  const sh   = getSheet(SHEET_CONFIG);
  const data = sh.getDataRange().getValues();
  const cfg  = {};
  for (let i = 1; i < data.length; i++) {
    if (data[i][0]) cfg[data[i][0].toString()] = data[i][1].toString();
  }
  return cfg;
}

function setConfig(key, value) {
  const sh   = getSheet(SHEET_CONFIG);
  const data = sh.getDataRange().getValues();
  for (let i = 1; i < data.length; i++) {
    if (data[i][0] === key) { sh.getRange(i + 1, 2).setValue(value); return; }
  }
  sh.appendRow([key, value]);
}

function respond(data, cb) {
  const json = JSON.stringify(data);
  if (cb) {
    return ContentService
      .createTextOutput(cb + '(' + json + ')')
      .setMimeType(ContentService.MimeType.JAVASCRIPT);
  }
  return ContentService
    .createTextOutput(json)
    .setMimeType(ContentService.MimeType.JSON);
}

function isTeacher(p) { return p.teacher === TEACHER_PASS; }

// ── Router ───────────────────────────────────────────────────
// ── doPost: รับ JSON body (uploadSlip) หรือ verifySlip ──────
function doPost(e) {
  try {
    let p;
    try { p = JSON.parse(e.postData.contents); } catch(_) { p = e.parameter; }
    const cb = (p.callback || (e.parameter && e.parameter.callback) || null);
    if (p.action === 'verifySlip')  return actionVerifySlip(p, cb);
    if (p.action === 'uploadSlip')  return actionUploadSlip(p, cb);
    return respond({status:'error', msg:'unknown post action'}, cb);
  } catch(err) {
    return respond({status:'error', msg: err.toString()}, null);
  }
}

function doGet(e) {
  const p  = e.parameter;
  const cb = p.callback || null;
  try {
    switch (p.action) {
      // นักเรียน
      case 'register':     return actionRegister(p, cb);
      case 'login':        return actionLogin(p, cb);
      case 'save':         return actionSave(p, cb);
      case 'recover':      return actionRecover(p, cb);
      // ครู
      case 'getLeaderboard':    return actionGetLeaderboard(p, cb);
      case 'toggleLeaderboard': return actionToggleLeaderboard(p, cb);
      case 'getAttempts':       return actionGetAttempts(p, cb);
      case 'useAttempt':        return actionUseAttempt(p, cb);
      case 'saveQuizScore':     return actionSaveQuizScore(p, cb);
      case 'getQuizLeaderboard':return actionGetQuizLeaderboard(p, cb);
      case 'addAttempts':       return actionAddAttempts(p, cb);  // ครู manual
      case 'updateEmail':  return actionUpdateEmail(p, cb);
      case 'addStudent':   return actionAddStudent(p, cb);
      case 'deleteStudent':   return actionDeleteStudent(p, cb);
      case 'activateStudent': return actionActivateStudent(p, cb);
      case 'stats':           return actionStats(p, cb);
      case 'myStats':         return actionMyStats(p, cb);
      // Purchase flow
      case 'newPurchase':     return actionNewPurchase(p, cb);
      case 'getStats':        return actionGetStats(p, cb);
      case 'getPurchases':    return actionGetPurchases(p, cb);
      case 'verifyPurchase':  return actionVerifyPurchase(p, cb);
      case 'rejectPurchase':  return actionRejectPurchase(p, cb);
      case 'checkOrder':      return actionCheckOrder(p, cb);
      case 'checkCode':       return actionCheckCode(p, cb);
      case 'selfRegister':    return actionSelfRegister(p, cb);
      case 'checkApproval':   return actionCheckApproval(p, cb);
      default:                return respond({status:'error', msg:'unknown action'}, cb);
    }
  } catch(err) {
    return respond({status:'error', msg: err.toString()}, cb);
  }
}

// ── 1. Register (นักเรียนยืนยันตัวตน) ────────────────────────
// เด็กต้องกรอก code ที่ครูกำหนดให้ + nickname + email
// ?action=register&code=123456&name=ชื่อ&email=x@x.com
function actionRegister(p, cb) {
  const code  = (p.code  || '').toString().trim();
  const name  = (p.name  || '').toString().trim();
  const email = (p.email || '').toString().trim().toLowerCase();

  if (!code || code.length !== 6) return respond({status:'error', msg:'รหัสต้องเป็นตัวเลข 6 หลัก'}, cb);
  if (!name)  return respond({status:'error', msg:'กรุณาใส่ชื่อเล่น'}, cb);
  if (!email || !email.includes('@')) return respond({status:'error', msg:'กรุณาใส่ email ที่ถูกต้อง'}, cb);

  const sh   = getSheet(SHEET_STUDENTS);
  const data = sh.getDataRange().getValues();

  for (let i = 1; i < data.length; i++) {
    const row = data[i];
    if (row[0].toString() !== code) continue;

    if (row[3] === 'deleted') return respond({status:'error', msg:'รหัสนี้ถูกยกเลิกแล้ว ติดต่อครู'}, cb);

    if (row[3] === 'active') {
      const savedEmail = (row[2]||'').toString().toLowerCase();
      if (!savedEmail) {
        // ยังไม่มี email → อัปเดตให้เลย
        sh.getRange(i + 1, 3).setValue(email);
        return respond({status:'ok', name: row[1], updated_email: true}, cb);
      }
      if (savedEmail === email) {
        return respond({status:'already_active', name: row[1]}, cb);
      }
      return respond({status:'error', msg:'รหัสนี้ถูกใช้แล้ว หรือ email ไม่ตรง'}, cb);
    }

    if (row[3] === 'pending') {
      // ครูเพิ่มรหัสรอไว้ → เด็กมายืนยัน
      sh.getRange(i + 1, 2).setValue(name);
      sh.getRange(i + 1, 3).setValue(email);
      sh.getRange(i + 1, 4).setValue('active');
      sh.getRange(i + 1, 5).setValue(new Date().toISOString());
      return respond({status:'ok', name: name}, cb);
    }
  }

  return respond({status:'error', msg:'ไม่พบรหัสนี้ในระบบ — ขอรหัสจากครูก่อนนะ 😊'}, cb);
}

// ── 2. Login ─────────────────────────────────────────────────
function actionLogin(p, cb) {
  const code = (p.code || '').toString().trim();
  if (!code) return respond({status:'error', msg:'ไม่มี code'}, cb);

  const sh   = getSheet(SHEET_STUDENTS);
  const data = sh.getDataRange().getValues();
  for (let i = 1; i < data.length; i++) {
    if (data[i][0].toString() !== code) continue;
    if (data[i][3] !== 'active') return respond({status:'error', msg:'รหัสนี้ยังไม่ได้ activate ติดต่อครู'}, cb);

    const pSh   = getSheet(SHEET_PROGRESS);
    const pData = pSh.getDataRange().getValues();
    const progress = {};
    for (let j = 1; j < pData.length; j++) {
      if (pData[j][0].toString() === code) {
        progress['d' + pData[j][1]] = pData[j][2];
      }
    }
    return respond({status:'ok', name: data[i][1], progress}, cb);
  }
  return respond({status:'not_found'}, cb);
}

// ── 3. Save Progress ─────────────────────────────────────────
function actionSave(p, cb) {
  const code = (p.code || '').toString().trim();
  const day  = parseInt(p.day);
  const comp = (p.completion || '').toString().trim().toUpperCase();

  const score = Math.min(100, Math.max(0, parseInt(p.score) || 100)); // 0–100, default 100
  if (!code || !day || !comp) return respond({status:'error', msg:'ข้อมูลไม่ครบ'}, cb);
  if (!comp.startsWith('D'+day+'-') || comp.length !== 7)
    return respond({status:'error', msg:'completion code ผิด format'}, cb);

  const sh   = getSheet(SHEET_STUDENTS);
  const data = sh.getDataRange().getValues();
  let found  = false;
  for (let i = 1; i < data.length; i++) {
    if (data[i][0].toString() === code && data[i][3] === 'active') { found = true; break; }
  }
  if (!found) return respond({status:'error', msg:'ไม่พบ student หรือยังไม่ได้ activate'}, cb);

  const pSh   = getSheet(SHEET_PROGRESS);
  const pData = pSh.getDataRange().getValues();
  for (let i = 1; i < pData.length; i++) {
    if (pData[i][0].toString() === code && parseInt(pData[i][1]) === day) {
      return respond({status:'already_saved', completion: pData[i][2]}, cb);
    }
  }

  // คำนวณ day_points = เข้าเรียน(10) + quiz(correct × 5)
  const PTS_ATT     = parseInt(getConfig('pts_attendance')   || '10');
  const PTS_CORRECT = parseInt(getConfig('pts_per_correct')  || '5');
  // score field = จำนวนข้อที่ถูก (0–N) ส่งมาจาก HTML
  const correctAns  = Math.min(100, Math.max(0, score));  // reuse score field as correct count
  const dayPoints   = PTS_ATT + (correctAns * PTS_CORRECT);

  pSh.appendRow([code, day, comp, new Date().toISOString(), correctAns, dayPoints]);
  return respond({status:'ok', day_points: dayPoints}, cb);
}

// ── 4. Recover code จาก email ────────────────────────────────
// ?action=recover&email=x@x.com
function actionRecover(p, cb) {
  const email = (p.email || '').toString().trim().toLowerCase();
  if (!email || !email.includes('@')) return respond({status:'error', msg:'email ไม่ถูกต้อง'}, cb);

  const sh   = getSheet(SHEET_STUDENTS);
  const data = sh.getDataRange().getValues();
  for (let i = 1; i < data.length; i++) {
    const savedEmail = (data[i][2] || '').toString().toLowerCase();
    if (savedEmail === email && data[i][3] === 'active') {
      return respond({status:'ok', code: data[i][0], name: data[i][1]}, cb);
    }
  }
  return respond({status:'not_found', msg:'ไม่พบ email นี้ในระบบ'}, cb);
}

// ── 5. Leaderboard (สาธารณะ) ─────────────────────────────────
// ?action=getLeaderboard
function actionGetLeaderboard(p, cb) {
  const isOpen = getConfig('leaderboard_open') === 'true';
  const compDays = parseInt(getConfig('competition_days') || '30');

  const sh   = getSheet(SHEET_STUDENTS);
  const data = sh.getDataRange().getValues();
  const pSh   = getSheet(SHEET_PROGRESS);
  const pData = pSh.getDataRange().getValues();

  const progMap = {};
  for (let i = 1; i < pData.length; i++) {
    const c = pData[i][0].toString();
    if (!progMap[c]) progMap[c] = { days: [], total_score: 0, day30_date: null, savedAts: [] };
    const dayNum  = parseInt(pData[i][1]);
    const score   = parseFloat(pData[i][4]) || 100;
    const savedAt = pData[i][3] ? pData[i][3].toString() : '';
    progMap[c].days.push(dayNum);
    progMap[c].total_score += score;
    if (savedAt) progMap[c].savedAts.push(savedAt);
    if (dayNum === 30 && savedAt) progMap[c].day30_date = savedAt;
  }

  const students = [];
  for (let i = 1; i < data.length; i++) {
    if (data[i][3] !== 'active') continue;
    const c   = data[i][0].toString();
    const pm  = progMap[c] || { days: [], total_score: 0, day30_date: null };
    const streak = calcStreak(pm.savedAts);
    students.push({
      name:           data[i][1] || 'ไม่ระบุชื่อ',
      code:           c,
      days_done:      pm.days.length,
      last_day:       pm.days.length ? Math.max(...pm.days) : 0,
      total_score:    Math.round(pm.total_score),
      day30_date:     pm.day30_date,
      finished:       pm.days.length >= compDays,
      current_streak: streak.current,
      max_streak:     streak.max,
    });
  }

  // Main leaderboard: sort by days_done then total_score
  students.sort((a, b) => b.days_done - a.days_done || b.total_score - a.total_score);

  // Speed Heroes: Day 30+ completers, rank by max_streak DESC then total_score DESC
  const speedHeroes = students
    .filter(s => s.days_done >= 30)
    .sort((a, b) => b.max_streak - a.max_streak || b.total_score - a.total_score)
    .slice(0, 3)
    .map((s, i) => ({ ...s, sh_rank: i + 1 }));

  // Quiz Champions: from QuizScores sheet — best score per student (top 3)
  const qSh   = getSheet(SHEET_QUIZ_SCR);
  const qData = qSh.getDataRange().getValues();
  // qBest: best score per student, tiebreaker = ใช้เวลาน้อยกว่าชนะ
  const qBest = {};  // code -> {score, time_seconds}
  for (let i = 1; i < qData.length; i++) {
    const c    = qData[i][0].toString();
    const s    = parseInt(qData[i][1]) || 0;
    const t    = parseInt(qData[i][4]) || 999999;  // col E = time_seconds
    const prev = qBest[c];
    if (!prev || s > prev.score || (s === prev.score && t < prev.time_seconds)) {
      qBest[c] = {score: s, time_seconds: t};
    }
  }
  const nameMap = {};
  for (let i = 1; i < data.length; i++) nameMap[data[i][0].toString()] = data[i][1] || data[i][0];

  // สร้าง map days_done per student
  const daysDoneMap = {};
  for (const s of students) daysDoneMap[s.code] = s.days_done;

  const quizChampions = Object.entries(qBest)
    .filter(([code]) => (daysDoneMap[code] || 0) >= compDays)  // ต้องเรียนครบ 30 วันก่อน
    .map(([code, b]) => ({
      code,
      nickname: nameMap[code] || code,
      quiz_score:   b.score,
      time_seconds: b.time_seconds,
      days_done:    daysDoneMap[code] || 0,
    }))
    .sort((a, b) => b.quiz_score - a.quiz_score || a.time_seconds - b.time_seconds) // tiebreaker: เวลาน้อยชนะ
    .slice(0, 10)
    .map((s, i) => ({ ...s, qc_rank: i + 1 }));

  const cfg = getConfigAll();
  return respond({ status:'ok', open: isOpen, students, speed_heroes: speedHeroes, quiz_champions: quizChampions, competition_days: compDays, config: cfg }, cb);
}

// ?action=toggleLeaderboard&teacher=xxx&open=true|false
function actionToggleLeaderboard(p, cb) {
  if (!isTeacher(p)) return respond({status:'error', msg:'รหัสครูไม่ถูกต้อง'}, cb);
  const val = p.open === 'true' ? 'true' : 'false';
  setConfig('leaderboard_open', val);
  return respond({status:'ok', open: val === 'true'}, cb);
}

// ── 6. Update Email (ครูแก้ email นักเรียน) ──────────────────
// ?action=updateEmail&teacher=xxx&code=123456&email=new@email.com
function actionUpdateEmail(p, cb) {
  if (!isTeacher(p)) return respond({status:'error', msg:'รหัสครูไม่ถูกต้อง'}, cb);
  const code  = (p.code  || '').toString().trim();
  const email = (p.email || '').toString().trim().toLowerCase();
  if (!code)  return respond({status:'error', msg:'ระบุ code ด้วย'}, cb);
  if (!email || !email.includes('@')) return respond({status:'error', msg:'email ไม่ถูกต้อง'}, cb);

  const sh   = getSheet(SHEET_STUDENTS);
  const data = sh.getDataRange().getValues();
  for (let i = 1; i < data.length; i++) {
    if (data[i][0].toString() !== code) continue;
    sh.getRange(i + 1, 3).setValue(email);
    return respond({status:'ok', code, email}, cb);
  }
  return respond({status:'not_found'}, cb);
}

// ── 6. Add Student (ครูเพิ่มเด็ก) ────────────────────────────
// ?action=addStudent&teacher=xxx&code=123456
// หรือไม่ใส่ code → ระบบสร้างให้อัตโนมัติ
function actionAddStudent(p, cb) {
  if (!isTeacher(p)) return respond({status:'error', msg:'รหัสครูไม่ถูกต้อง'}, cb);

  let code = (p.code || '').toString().trim();
  const note = (p.note || '').toString().trim(); // หมายเหตุ เช่นชื่อจริง

  // สร้าง code อัตโนมัติถ้าไม่ระบุ
  if (!code || code.length !== 6) {
    code = String(Math.floor(100000 + Math.random() * 900000));
  }

  const sh   = getSheet(SHEET_STUDENTS);
  const data = sh.getDataRange().getValues();

  // ตรวจซ้ำ
  for (let i = 1; i < data.length; i++) {
    if (data[i][0].toString() === code && data[i][3] !== 'deleted') {
      return respond({status:'exists', code, name: data[i][1]}, cb);
    }
  }

  // เพิ่มแถวใหม่ — status=pending รอเด็กมายืนยัน
  sh.appendRow([code, note||'', '', 'pending', '', 'teacher']);
  return respond({status:'ok', code}, cb);
}

// ── 6. Delete Student (ครูลบเด็ก) ────────────────────────────
// ?action=deleteStudent&teacher=xxx&code=123456
function actionDeleteStudent(p, cb) {
  if (!isTeacher(p)) return respond({status:'error', msg:'รหัสครูไม่ถูกต้อง'}, cb);

  const code = (p.code || '').toString().trim();
  if (!code) return respond({status:'error', msg:'ระบุ code ด้วย'}, cb);

  const sh   = getSheet(SHEET_STUDENTS);
  const data = sh.getDataRange().getValues();
  for (let i = 1; i < data.length; i++) {
    if (data[i][0].toString() === code) {
      sh.getRange(i + 1, 4).setValue('deleted');
      return respond({status:'ok', code}, cb);
    }
  }
  return respond({status:'not_found'}, cb);
}

// ── 6b. Activate Student (ครู approve pending → active) ──────
// ?action=activateStudent&teacher=xxx&code=123456
function actionActivateStudent(p, cb) {
  if (!isTeacher(p)) return respond({status:'error', msg:'รหัสครูไม่ถูกต้อง'}, cb);
  const code = (p.code || '').toString().trim();
  if (!code) return respond({status:'error', msg:'ระบุ code ด้วย'}, cb);
  const sh   = getSheet(SHEET_STUDENTS);
  const data = sh.getDataRange().getValues();
  for (let i = 1; i < data.length; i++) {
    if (data[i][0].toString() === code) {
      sh.getRange(i + 1, 4).setValue('active');
      return respond({status:'ok', code}, cb);
    }
  }
  return respond({status:'not_found'}, cb);
}

// ── Streak helper ────────────────────────────────────────────
function calcStreak(savedAtList) {
  if (!savedAtList.length) return { current: 0, max: 0 };
  const dates = [...new Set(savedAtList.map(d => d.toString().split('T')[0]))].sort();
  let max = 1, cur = 1;
  for (let i = 1; i < dates.length; i++) {
    const diff = (new Date(dates[i]) - new Date(dates[i-1])) / 86400000;
    cur  = diff === 1 ? cur + 1 : 1;
    max  = Math.max(max, cur);
  }
  const today       = new Date().toISOString().split('T')[0];
  const last        = dates[dates.length - 1];
  const daysSince   = (new Date(today) - new Date(last)) / 86400000;
  return { current: daysSince <= 1 ? cur : 0, max };
}

// ── Quiz Attempt helpers ─────────────────────────────────────
function getAttemptRow(sh, code) {
  const data = sh.getDataRange().getValues();
  for (let i = 1; i < data.length; i++) {
    if (data[i][0].toString() === code) return { row: i + 1, data: data[i] };
  }
  return null;
}

// ── 8a. Get Attempts ─────────────────────────────────────────
// ?action=getAttempts&code=123456
function actionGetAttempts(p, cb) {
  const code = (p.code || '').toString().trim();
  if (!code) return respond({status:'error', msg:'ไม่มี code'}, cb);

  const FREE_TOTAL = parseInt(getConfig('quiz_free_attempts') || '3');
  const sh   = getSheet(SHEET_QUIZ_ATT);
  const row  = getAttemptRow(sh, code);

  if (!row) {
    return respond({status:'ok', free_remaining: FREE_TOTAL, paid_credits: 0, total_remaining: FREE_TOTAL, attempt_num: 0}, cb);
  }
  const freeUsed     = parseInt(row.data[1]) || 0;
  const paidCredits  = parseInt(row.data[2]) || 0;
  const freeRemaining = Math.max(0, FREE_TOTAL - freeUsed);
  const totalRemaining = freeRemaining + paidCredits;

  // Best quiz score
  const sSh  = getSheet(SHEET_QUIZ_SCR);
  const sData = sSh.getDataRange().getValues();
  let bestScore = 0, attemptNum = 0;
  for (let i = 1; i < sData.length; i++) {
    if (sData[i][0].toString() === code) {
      bestScore  = Math.max(bestScore, parseInt(sData[i][1]) || 0);
      attemptNum = Math.max(attemptNum, parseInt(sData[i][2]) || 0);
    }
  }
  return respond({status:'ok', free_remaining: freeRemaining, paid_credits: paidCredits, total_remaining: totalRemaining, attempt_num: attemptNum, best_score: bestScore}, cb);
}

// ── 8b. Use Attempt ──────────────────────────────────────────
// ?action=useAttempt&code=123456
function actionUseAttempt(p, cb) {
  const code = (p.code || '').toString().trim();
  if (!code) return respond({status:'error', msg:'ไม่มี code'}, cb);

  const FREE_TOTAL = parseInt(getConfig('quiz_free_attempts') || '3');
  const sh   = getSheet(SHEET_QUIZ_ATT);
  const row  = getAttemptRow(sh, code);

  let freeUsed = 0, paidCredits = 0;
  if (row) { freeUsed = parseInt(row.data[1]) || 0; paidCredits = parseInt(row.data[2]) || 0; }

  const freeRemaining = Math.max(0, FREE_TOTAL - freeUsed);
  if (freeRemaining === 0 && paidCredits === 0) {
    return respond({status:'error', msg:'หมด attempt แล้ว — ซื้อเพิ่มได้ 29 บาท'}, cb);
  }

  if (freeRemaining > 0) {
    freeUsed++;
  } else {
    paidCredits--;
  }

  const now = new Date().toISOString();
  if (row) {
    sh.getRange(row.row, 2).setValue(freeUsed);
    sh.getRange(row.row, 3).setValue(paidCredits);
    sh.getRange(row.row, 4).setValue(now);
  } else {
    sh.appendRow([code, freeUsed, paidCredits, now]);
  }

  const remaining = Math.max(0, FREE_TOTAL - freeUsed) + paidCredits;
  return respond({status:'ok', remaining, used_free: freeUsed, paid_credits: paidCredits}, cb);
}

// ── 8c. Save Quiz Score ──────────────────────────────────────
// ?action=saveQuizScore&code=123456&score=25&attempt=1
function actionSaveQuizScore(p, cb) {
  const code         = (p.code  || '').toString().trim();
  const score        = parseInt(p.score)        || 0;
  const time_seconds = parseInt(p.time_seconds) || 0;  // เวลาที่ใช้ทั้งหมด (วินาที)
  if (!code) return respond({status:'error', msg:'ไม่มี code'}, cb);

  const sh   = getSheet(SHEET_QUIZ_SCR);
  const data = sh.getDataRange().getValues();

  // นับจำนวน attempt ของ student คนนี้ (auto-increment)
  let attemptNum = 1;
  for (let i = 1; i < data.length; i++) {
    if (data[i][0].toString() === code) attemptNum++;
  }

  // [code, score, attempt_num, saved_at, time_seconds]
  sh.appendRow([code, score, attemptNum, new Date().toISOString(), time_seconds]);
  return respond({status:'ok', score, attempt_num: attemptNum, time_seconds}, cb);
}

// ── 8d. Get Quiz Leaderboard ─────────────────────────────────
function actionGetQuizLeaderboard(p, cb) {
  const sh   = getSheet(SHEET_QUIZ_SCR);
  const data = sh.getDataRange().getValues();

  const bestMap = {};
  for (let i = 1; i < data.length; i++) {
    const c = data[i][0].toString();
    const s = parseInt(data[i][1]) || 0;
    if (!bestMap[c] || s > bestMap[c]) bestMap[c] = s;
  }

  // Get student names
  const stSh   = getSheet(SHEET_STUDENTS);
  const stData = stSh.getDataRange().getValues();
  const nameMap = {};
  for (let i = 1; i < stData.length; i++) nameMap[stData[i][0].toString()] = stData[i][1];

  const results = Object.entries(bestMap)
    .map(([code, score]) => ({ code, name: nameMap[code] || code, score }))
    .sort((a, b) => b.score - a.score);

  return respond({status:'ok', results}, cb);
}

// ── 8e. Add Attempts (ครู manual / backup) ───────────────────
// ?action=addAttempts&teacher=xxx&code=123456&n=1
function actionAddAttempts(p, cb) {
  if (!isTeacher(p)) return respond({status:'error', msg:'รหัสครูไม่ถูกต้อง'}, cb);
  const code = (p.code || '').toString().trim();
  const n    = Math.max(1, parseInt(p.n) || 1);
  if (!code) return respond({status:'error', msg:'ระบุ code'}, cb);

  const sh   = getSheet(SHEET_QUIZ_ATT);
  const row  = getAttemptRow(sh, code);
  const now  = new Date().toISOString();

  if (row) {
    const paid = (parseInt(row.data[2]) || 0) + n;
    sh.getRange(row.row, 3).setValue(paid);
    sh.getRange(row.row, 4).setValue(now);
    return respond({status:'ok', paid_credits: paid}, cb);
  }
  sh.appendRow([code, 0, n, now]);
  return respond({status:'ok', paid_credits: n}, cb);
}

// ── 8f. Verify Slip via Slipok ───────────────────────────────
// POST: action=verifySlip&code=123456&slip_base64=...
function actionVerifySlip(p, cb) {
  const code      = (p.code || '').toString().trim();
  const slipB64   = (p.slip_base64 || '').toString().trim();
  const SLIPOK_KEY = getConfig('slipok_api_key') || '';
  const EXPECTED  = parseInt(getConfig('quiz_paid_price') || '29');

  if (!code || !slipB64) return respond({status:'error', msg:'ข้อมูลไม่ครบ'}, cb);
  if (!SLIPOK_KEY || SLIPOK_KEY === 'YOUR_SLIPOK_KEY_HERE')
    return respond({status:'error', msg:'ครูยังไม่ได้ตั้งค่า Slipok API key'}, cb);

  try {
    const res = UrlFetchApp.fetch(`https://api.slipok.com/api/line/apikey/${SLIPOK_KEY}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      payload: JSON.stringify({ data: slipB64 }),
      muteHttpExceptions: true
    });
    const result = JSON.parse(res.getContentText());

    if (!result.success) return respond({status:'error', msg:'ตรวจ slip ไม่ผ่าน: ' + (result.message||'')}, cb);

    const amount   = parseFloat(result.data.amount) || 0;
    const transRef = (result.data.transRef || result.data.ref1 || '').toString();

    if (Math.round(amount) !== EXPECTED)
      return respond({status:'error', msg:`ยอดเงินไม่ตรง — พบ ${amount} บาท (ต้องการ ${EXPECTED} บาท)`}, cb);

    // ตรวจซ้ำ
    const slipSh   = getSheet(SHEET_SLIPS);
    const slipData = slipSh.getDataRange().getValues();
    for (let i = 1; i < slipData.length; i++) {
      if (slipData[i][0].toString() === transRef)
        return respond({status:'error', msg:'slip นี้ถูกใช้แล้ว'}, cb);
    }

    // บันทึก slip + เพิ่ม credit
    slipSh.appendRow([transRef, code, amount, new Date().toISOString()]);
    const attSh = getSheet(SHEET_QUIZ_ATT);
    const row   = getAttemptRow(attSh, code);
    const now   = new Date().toISOString();
    if (row) {
      const paid = (parseInt(row.data[2]) || 0) + 1;
      attSh.getRange(row.row, 3).setValue(paid);
      attSh.getRange(row.row, 4).setValue(now);
    } else {
      attSh.appendRow([code, 0, 1, now]);
    }
    return respond({status:'ok', msg:'ชำระเงินสำเร็จ! ได้รับ 1 attempt', amount, transRef}, cb);

  } catch(e) {
    return respond({status:'error', msg:'เรียก Slipok ไม่ได้: ' + e.toString()}, cb);
  }
}

// ── 7b. My Stats (student self-view) ─────────────────────────
function actionMyStats(p, cb) {
  const code = (p.code || '').toString().trim().toUpperCase();
  if (!code) return respond({status:'error', msg:'กรุณากรอก code'}, cb);

  // ตรวจว่า student มีอยู่จริง
  const stSh   = getSheet(SHEET_STUDENTS);
  const stData = stSh.getDataRange().getValues();
  let studentRow = null;
  for (let i = 1; i < stData.length; i++) {
    if (stData[i][0].toString().toUpperCase() === code && stData[i][3] !== 'deleted') {
      studentRow = stData[i]; break;
    }
  }
  if (!studentRow) return respond({status:'error', msg:'ไม่พบ code นี้'}, cb);

  const pSh   = getSheet(SHEET_PROGRESS);
  const pData = pSh.getDataRange().getValues();

  // รวบรวม row ของ student นี้
  const myRows = [];
  for (let i = 1; i < pData.length; i++) {
    if (pData[i][0].toString().toUpperCase() === code) {
      myRows.push({
        day:           parseInt(pData[i][1])   || 0,
        saved_at:      pData[i][3]             || '',
        correct_count: parseInt(pData[i][4])   || 0,
        day_points:    parseInt(pData[i][5])   || 0,
      });
    }
  }

  // เรียงตามวันที่บันทึก
  myRows.sort((a,b) => new Date(a.saved_at) - new Date(b.saved_at));

  // คำนวณ streak per row
  const dates = myRows.map(r => r.saved_at ? r.saved_at.toString().split('T')[0] : '');
  let streak = 1;
  const streakPerRow = [1];
  for (let i = 1; i < dates.length; i++) {
    const diff = dates[i] && dates[i-1]
      ? (new Date(dates[i]) - new Date(dates[i-1])) / 86400000
      : 999;
    streak = diff === 1 ? streak + 1 : 1;
    streakPerRow.push(streak);
  }

  const daily_log = myRows.map((r, i) => ({...r, streak_at_day: streakPerRow[i]}));

  // streak stat
  const s = calcStreak(myRows.map(r => r.saved_at));
  const total_score = myRows.reduce((acc, r) => acc + (r.day_points||0), 0);

  // โบนัส streak ที่ถึง milestone
  const PTS_S7  = parseInt(getConfig('pts_streak_7')  || '50');
  const PTS_S30 = parseInt(getConfig('pts_streak_30') || '200');
  let bonus = 0;
  if (s.max >= 30) bonus += PTS_S30;
  else if (s.max >= 7) bonus += PTS_S7;

  const cfg = getConfigAll();

  return respond({
    status: 'ok',
    nickname:       studentRow[1] || '',
    days_completed: myRows.length,
    current_streak: s.current,
    max_streak:     s.max,
    total_score:    total_score + bonus,
    streak_bonus:   bonus,
    daily_log,
    config: cfg,
  }, cb);
}

// ── 7. Stats (teacher dashboard) ─────────────────────────────
function actionStats(p, cb) {
  if (!isTeacher(p)) return respond({status:'error', msg:'รหัสครูไม่ถูกต้อง'}, cb);

  const sh   = getSheet(SHEET_STUDENTS);
  const data = sh.getDataRange().getValues();

  const pSh   = getSheet(SHEET_PROGRESS);
  const pData = pSh.getDataRange().getValues();

  const progMap = {};
  for (let i = 1; i < pData.length; i++) {
    const c = pData[i][0].toString();
    if (!progMap[c]) progMap[c] = [];
    progMap[c].push(parseInt(pData[i][1]));
  }

  const students = [];
  for (let i = 1; i < data.length; i++) {
    const status = data[i][3];
    if (status === 'deleted') continue;
    const c    = data[i][0].toString();
    const days = progMap[c] || [];
    students.push({
      code:         c,
      name:         data[i][1] || '(รอเด็กยืนยัน)',
      email:        data[i][2] || '',
      status:       status,
      days_done:    days.length,
      last_day:     days.length ? Math.max(...days) : 0,
      type:         (data[i][6] || 'lifetime').toString(),
      pkg_name:     (data[i][7] || '').toString(),
      expiry_date:  (data[i][8] || '').toString(),
    });
  }

  students.sort((a, b) => b.days_done - a.days_done);
  return respond({status:'ok', students, total: students.length}, cb);
}

// ════════════════════════════════════════════════════════════
//  PURCHASE SYSTEM — สำหรับ register.html
// ════════════════════════════════════════════════════════════

// ── getStats: จำนวนที่ขายได้ (ใช้คำนวณ tier ราคา) ───────────
// ?action=getStats&callback=cb
function actionGetStats(p, cb) {
  const sh   = getSheet(SHEET_PURCHASES);
  const data = sh.getDataRange().getValues();
  let sold = 0;
  for (let i = 1; i < data.length; i++) {
    if (data[i][8] !== 'rejected') sold++;  // นับทุก order ที่ไม่ถูก reject
  }
  return respond({status:'ok', lifetimeSold: sold}, cb);
}

// ── newPurchase: บันทึก order ใหม่ ─────────────────────────
// ?action=newPurchase&name=...&phone=...&email=...&pkg=...&price=...&type=lifetime
function actionNewPurchase(p, cb) {
  const orderId = (p.order_id || ('ORD-' + Date.now())).toString().trim();
  const pkg     = (p.pkg   || '').toString().trim();
  const price   = parseInt(p.price) || 0;
  const type    = (p.type  || 'lifetime').toString().trim();

  if (!pkg) return respond({status:'error', msg:'ไม่พบ pkg'}, cb);

  const sh = getSheet(SHEET_PURCHASES);
  sh.appendRow([orderId, '', '', '', '', pkg, price, type, 'pending', '', new Date().toISOString(), '']);

  return respond({status:'ok', order_id: orderId}, cb);
}

// ── uploadSlip: รับสลิป base64 → บันทึกไฟล์ใน Google Drive ─
// POST body: { action:'uploadSlip', order_id:'ORD-...', slip:'data:image/jpeg;base64,...' }
function actionUploadSlip(p, cb) {
  const orderId = (p.order_id || p.phone || '').toString().trim();
  const slip    = (p.slip  || '').toString().trim();

  if (!orderId || !slip) return respond({status:'error', msg:'ข้อมูลไม่ครบ'}, cb);

  try {
    const base64Data = slip.replace(/^data:image\/\w+;base64,/, '');
    const blob = Utilities.newBlob(
      Utilities.base64Decode(base64Data),
      'image/jpeg',
      'slip_' + orderId + '_' + Date.now() + '.jpg'
    );

    // สร้าง/หาโฟลเดอร์ "LexiGo Slips" ใน Drive
    const folderIter = DriveApp.getFoldersByName('LexiGo Slips');
    const folder = folderIter.hasNext() ? folderIter.next() : DriveApp.createFolder('LexiGo Slips');
    const file = folder.createFile(blob);
    file.setSharing(DriveApp.Access.ANYONE_WITH_LINK, DriveApp.Permission.VIEW);
    const url = file.getUrl();

    // อัปเดต slip_url ใน Purchases (หา row จาก orderId)
    const sh   = getSheet(SHEET_PURCHASES);
    const data = sh.getDataRange().getValues();
    for (let i = data.length - 1; i >= 1; i--) {
      if (data[i][0].toString() === orderId) {
        sh.getRange(i + 1, 10).setValue(url);
        break;
      }
    }

    return respond({status:'ok', slip_url: url}, cb);
  } catch(err) {
    return respond({status:'error', msg: err.toString()}, cb);
  }
}

// ── getPurchases: ครูดูรายการ order ทั้งหมด ─────────────────
// ?action=getPurchases&teacher=xxx
function actionGetPurchases(p, cb) {
  if (!isTeacher(p)) return respond({status:'error', msg:'รหัสครูไม่ถูกต้อง'}, cb);

  const sh   = getSheet(SHEET_PURCHASES);
  const data = sh.getDataRange().getValues();
  const purchases = [];
  for (let i = 1; i < data.length; i++) {
    purchases.push({
      order_id:     data[i][0],
      name:         data[i][1],
      phone:        data[i][2],
      line_id:      data[i][3],
      email:        data[i][4],
      pkg_name:     data[i][5],
      price:        data[i][6],
      type:         data[i][7],
      status:       data[i][8],
      slip_url:     data[i][9],
      created_at:   data[i][10],
      student_code: data[i][11],
    });
  }
  purchases.sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
  return respond({status:'ok', purchases, total: purchases.length}, cb);
}

// ── verifyPurchase: ครู approve → สร้าง student code อัตโนมัติ
// ?action=verifyPurchase&teacher=xxx&order_id=ORD-...
function actionVerifyPurchase(p, cb) {
  if (!isTeacher(p)) return respond({status:'error', msg:'รหัสครูไม่ถูกต้อง'}, cb);
  const orderId = (p.order_id || '').toString().trim();
  if (!orderId) return respond({status:'error', msg:'ระบุ order_id'}, cb);

  const sh   = getSheet(SHEET_PURCHASES);
  const data = sh.getDataRange().getValues();
  for (let i = 1; i < data.length; i++) {
    if (data[i][0].toString() !== orderId) continue;

    // ถ้า verify แล้ว → คืน code เดิม
    if (data[i][8] === 'verified')
      return respond({status:'ok', msg:'verified แล้ว', student_code: data[i][11]}, cb);

    // สร้าง student code 6 หลัก
    const code    = String(Math.floor(100000 + Math.random() * 900000));
    const name    = data[i][1];
    const email   = data[i][4];
    const type    = (data[i][7] || 'lifetime').toString().trim(); // lifetime | annual | level
    const pkgName = (data[i][5] || '').toString().trim();

    // คำนวณวันหมดอายุ (รายปี = วันนี้ + 365 วัน)
    let expiryDate = '';
    if (type === 'annual') {
      const exp = new Date();
      exp.setDate(exp.getDate() + 365);
      expiryDate = exp.toISOString();
    }

    // เพิ่มใน Students sheet (status=pending รอเด็กกรอกโปรไฟล์)
    const stSh = getSheet(SHEET_STUDENTS);
    stSh.appendRow([code, name, email, 'pending', new Date().toISOString(), 'purchase:' + orderId, type, pkgName, expiryDate]);

    // อัปเดต Purchases row
    sh.getRange(i + 1, 9).setValue('verified');
    sh.getRange(i + 1, 12).setValue(code);

    return respond({status:'ok', student_code: code, name, email, type, expiry_date: expiryDate}, cb);
  }
  return respond({status:'not_found'}, cb);
}

// ── checkOrder: นักเรียนเช็คสถานะ order ของตัวเอง ───────────
// ?action=checkOrder&phone=0812345678
function actionCheckOrder(p, cb) {
  const phone = (p.phone || '').toString().trim();
  if (!phone) return respond({status:'error', msg:'ระบุเบอร์โทร'}, cb);

  const sh   = getSheet(SHEET_PURCHASES);
  const data = sh.getDataRange().getValues();
  for (let i = data.length - 1; i >= 1; i--) {
    if (data[i][2].toString() === phone) {
      return respond({
        status:       'ok',
        order_status: data[i][8],      // pending | verified | rejected
        student_code: data[i][11] || '',
        pkg_name:     data[i][5]  || '',
      }, cb);
    }
  }
  return respond({status:'not_found'}, cb);
}

// ── rejectPurchase: ครูปฏิเสธ order ────────────────────────
// ?action=rejectPurchase&teacher=xxx&order_id=ORD-...
function actionRejectPurchase(p, cb) {
  if (!isTeacher(p)) return respond({status:'error', msg:'รหัสครูไม่ถูกต้อง'}, cb);
  const orderId = (p.order_id || '').toString().trim();
  if (!orderId) return respond({status:'error', msg:'ระบุ order_id'}, cb);

  const sh   = getSheet(SHEET_PURCHASES);
  const data = sh.getDataRange().getValues();
  for (let i = 1; i < data.length; i++) {
    if (data[i][0].toString() === orderId) {
      sh.getRange(i + 1, 9).setValue('rejected');
      // อัปเดต student record ด้วย (ถ้ามี)
      const studentCode = (data[i][11] || '').toString().trim();
      if (studentCode) {
        const stSh = getSheet(SHEET_STUDENTS);
        const stData = stSh.getDataRange().getValues();
        for (let j = 1; j < stData.length; j++) {
          if (stData[j][0].toString() === studentCode) {
            stSh.getRange(j + 1, 4).setValue('rejected');
            break;
          }
        }
      }
      return respond({status:'ok'}, cb);
    }
  }
  return respond({status:'not_found'}, cb);
}

// ── checkCode: ตรวจสอบว่ารหัส 6 หลักว่างอยู่หรือไม่ ─────────
// ?action=checkCode&code=123456
function actionCheckCode(p, cb) {
  const code = (p.code || '').toString().trim();
  if (!/^\d{6}$/.test(code)) return respond({status:'ok', available:false, msg:'รหัสต้องเป็นตัวเลข 6 หลัก'}, cb);
  const sh   = getSheet(SHEET_STUDENTS);
  const data = sh.getDataRange().getValues();
  for (let i = 1; i < data.length; i++) {
    if (data[i][0].toString() === code) return respond({status:'ok', available:false}, cb);
  }
  return respond({status:'ok', available:true}, cb);
}

// ── selfRegister: นักเรียนลงทะเบียนและตั้งรหัสเอง ────────────
// ?action=selfRegister&code=123456&nick=xxx&first=xxx&last=xxx&phone=xxx&line=xxx&email=xxx&orderId=ORD-...
function actionSelfRegister(p, cb) {
  const code    = (p.code    || '').toString().trim();
  const nick    = (p.nick    || '').toString().trim();
  const first   = (p.first   || '').toString().trim();
  const last    = (p.last    || '').toString().trim();
  const phone   = (p.phone   || '').toString().trim();
  const line    = (p.line    || '').toString().trim();
  const email   = (p.email   || '').toString().trim();
  const ref     = (p.ref     || '').toString().trim();
  const course  = (p.course  || '').toString().trim();
  const orderId = (p.orderId || '').toString().trim();

  if (!/^\d{6}$/.test(code))    return respond({status:'error', msg:'รหัสต้องเป็นตัวเลข 6 หลัก'}, cb);
  if (!nick || !first || !last) return respond({status:'error', msg:'ข้อมูลไม่ครบ'}, cb);
  if (!phone || !email)         return respond({status:'error', msg:'ข้อมูลไม่ครบ'}, cb);

  // ตรวจซ้ำ
  const stSh   = getSheet(SHEET_STUDENTS);
  const stData = stSh.getDataRange().getValues();
  for (let i = 1; i < stData.length; i++) {
    if (stData[i][0].toString() === code) return respond({status:'code_taken', msg:'รหัส '+code+' ถูกใช้แล้ว'}, cb);
  }

  // หาข้อมูล purchase จาก orderId
  const purSh   = getSheet(SHEET_PURCHASES);
  const purData = purSh.getDataRange().getValues();
  let purRow = -1, purType = 'lifetime', pkgName = course;
  for (let i = purData.length - 1; i >= 1; i--) {
    if (purData[i][0].toString() === orderId) {
      purRow  = i;
      purType = (purData[i][7] || 'lifetime').toString().trim();
      pkgName = (purData[i][5] || course).toString().trim();
      break;
    }
  }

  // คำนวณ expiry
  let expiryDate = '';
  if (purType === 'annual') {
    const exp = new Date();
    exp.setDate(exp.getDate() + 365);
    expiryDate = exp.toISOString();
  }

  // สร้าง student record (pending_approval)
  const fullName = first + ' ' + last;
  stSh.appendRow([code, nick, email, 'pending_approval', new Date().toISOString(),
                  'purchase:' + orderId, purType, pkgName, expiryDate]);

  // อัปเดต Purchases row ด้วย contact info + student_code
  if (purRow >= 0) {
    purSh.getRange(purRow + 1, 2).setValue(fullName);  // name
    purSh.getRange(purRow + 1, 3).setValue(phone);     // phone
    purSh.getRange(purRow + 1, 4).setValue(line);      // line_id
    purSh.getRange(purRow + 1, 5).setValue(email);     // email
    purSh.getRange(purRow + 1, 9).setValue('pending_approval');
    purSh.getRange(purRow + 1, 12).setValue(code);
  }

  return respond({status:'ok', code: code, pkg_name: pkgName}, cb);
}

// ── checkApproval: นักเรียนเช็คสถานะการอนุมัติ ───────────────
// ?action=checkApproval&code=123456
function actionCheckApproval(p, cb) {
  const code = (p.code || '').toString().trim();
  if (!code) return respond({status:'error', msg:'ระบุรหัส'}, cb);
  const sh   = getSheet(SHEET_STUDENTS);
  const data = sh.getDataRange().getValues();
  for (let i = 1; i < data.length; i++) {
    if (data[i][0].toString() === code) {
      return respond({status:'ok', approval_status: data[i][3], nick: data[i][1]}, cb);
    }
  }
  return respond({status:'not_found'}, cb);
}
