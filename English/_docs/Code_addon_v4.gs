// ════════════════════════════════════════════════════════════
//  PeekaWord — Add-on v4
//  (1) ตรวจสลิปอัตโนมัติผ่าน SlipOK → อนุมัติเอง ออกรหัสทันที
//  (2) Login ด้วย email + password (ตั้งเอง)
//
//  วิธีติดตั้ง: copy ทั้งไฟล์นี้ ต่อท้าย Code.gs เดิม
//               แล้วแก้ router 2 จุดตามหมายเหตุด้านล่าง
// ════════════════════════════════════════════════════════════

/* ── ⚠️ ต้องแก้ router เดิมด้วย ──────────────────────────────

ใน doPost() เพิ่ม 2 บรรทัดนี้ ก่อน return unknown:
    if (p.action === 'verifyPurchaseSlip') return actionVerifyPurchaseSlip(p, cb);
    if (p.action === 'setPassword')        return actionSetPassword(p, cb);

ใน doGet() switch เพิ่ม 4 case นี้:
    case 'setPassword':    return actionSetPassword(p, cb);
    case 'loginEmail':     return actionLoginEmail(p, cb);
    case 'hasPassword':    return actionHasPassword(p, cb);
    case 'requestReset':   return actionRequestReset(p, cb);
    case 'confirmReset':   return actionConfirmReset(p, cb);
─────────────────────────────────────────────────────────── */

const COL_PASS_HASH = 9;   // index 9  → คอลัมน์ J
const COL_PASS_SALT = 10;  // index 10 → คอลัมน์ K
const COL_RESET_TOK = 11;  // index 11 → คอลัมน์ L  (token|expiry)

// ── helper: ทำให้ Students sheet มีคอลัมน์รหัสผ่านครบ ────────
function ensurePasswordColumns_() {
  const sh = getSheet(SHEET_STUDENTS);
  const head = sh.getRange(1, 1, 1, Math.max(sh.getLastColumn(), 1)).getValues()[0];
  const want = ['pass_hash', 'pass_salt', 'reset_token'];
  want.forEach(function (name, i) {
    const col = COL_PASS_HASH + i + 1;              // 1-based
    if ((head[COL_PASS_HASH + i] || '') !== name) {
      sh.getRange(1, col).setValue(name);
    }
  });
  return sh;
}

function sha256_(str) {
  return Utilities.computeDigest(Utilities.DigestAlgorithm.SHA_256, str, Utilities.Charset.UTF_8)
    .map(function (b) { return ('0' + (b & 0xFF).toString(16)).slice(-2); }).join('');
}

function randomToken_(n) {
  const c = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789';
  let s = '';
  for (let i = 0; i < (n || 24); i++) s += c.charAt(Math.floor(Math.random() * c.length));
  return s;
}

// หา row ของนักเรียนจาก email (active เท่านั้น)
function findStudentByEmail_(sh, email) {
  const data = sh.getDataRange().getValues();
  const e = (email || '').toString().trim().toLowerCase();
  for (let i = 1; i < data.length; i++) {
    if ((data[i][2] || '').toString().trim().toLowerCase() === e) {
      return { row: i + 1, data: data[i] };
    }
  }
  return null;
}

function findStudentByCode_(sh, code) {
  const data = sh.getDataRange().getValues();
  for (let i = 1; i < data.length; i++) {
    if (data[i][0].toString().trim() === code) return { row: i + 1, data: data[i] };
  }
  return null;
}

function progressFor_(code) {
  const pSh = getSheet(SHEET_PROGRESS);
  const pData = pSh.getDataRange().getValues();
  const progress = {};
  for (let j = 1; j < pData.length; j++) {
    if (pData[j][0].toString() === code) progress['d' + pData[j][1]] = pData[j][2];
  }
  return progress;
}


// ════════════════════════════════════════════════════════════
//  PART 1 — ตรวจสลิปอัตโนมัติ (SlipOK)
// ════════════════════════════════════════════════════════════
//
//  ทำไมต้องเช็กหลายชั้น: สลิปปลอมที่เจอบ่อยมี 4 แบบ
//    1. แต่งรูปเอง        → SlipOK อ่าน QR จริงจากธนาคาร ปลอมไม่ได้
//    2. ใช้สลิปเก่าซ้ำ    → เช็ก transRef ใน UsedSlips
//    3. โอนยอดน้อยกว่า    → เช็ก amount ตรงราคาแพ็กเกจ
//    4. โอนเข้าบัญชีอื่น  → เช็กเลขบัญชีปลายทาง
//
//  POST body: { action:'verifyPurchaseSlip', order_id, pkg, price, slip:'data:image/...' }

function actionVerifyPurchaseSlip(p, cb) {
  const orderId = (p.order_id || '').toString().trim();
  const pkg     = (p.pkg || '').toString().trim();
  const price   = parseInt(p.price) || 0;
  const type    = (p.type || 'level').toString().trim();
  const name    = (p.name || '').toString().trim();
  const email   = (p.email || '').toString().trim().toLowerCase();
  const phone   = (p.phone || '').toString().trim();
  const existingCode = (p.existing_code || '').toString().trim();
  let   slip    = (p.slip || p.slip_base64 || '').toString().trim();

  if (!orderId || !slip || !price)
    return respond({ status: 'error', msg: 'ข้อมูลไม่ครบ' }, cb);

  const KEY = getConfig('slipok_api_key') || '';
  if (!KEY || KEY === 'YOUR_SLIPOK_KEY_HERE')
    return respond({ status: 'manual', msg: 'ยังไม่ได้ตั้งค่า SlipOK — ส่งให้ครูตรวจแทน' }, cb);

  slip = slip.replace(/^data:image\/\w+;base64,/, '');

  let result;
  try {
    const res = UrlFetchApp.fetch('https://api.slipok.com/api/line/apikey/' + KEY, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      payload: JSON.stringify({ data: slip, log: true }),
      muteHttpExceptions: true
    });
    result = JSON.parse(res.getContentText());
  } catch (e) {
    // เรียก API ไม่ได้ → อย่าปฏิเสธลูกค้า ให้ครูตรวจมือแทน
    return respond({ status: 'manual', msg: 'ตรวจอัตโนมัติไม่ได้ — ส่งให้ครูตรวจ' }, cb);
  }

  if (!result || !result.success || !result.data)
    return respond({
      status: 'reject',
      msg: 'อ่านสลิปไม่ได้ หรือสลิปไม่ถูกต้อง — ลองถ่ายใหม่ให้เห็น QR ชัดๆ'
    }, cb);

  const d        = result.data;
  const amount   = parseFloat(d.amount) || 0;
  const transRef = (d.transRef || d.transactionId || d.ref1 || '').toString();
  const recvAcc  = ((d.receiver && (d.receiver.account && (d.receiver.account.value ||
                     d.receiver.account.bank && d.receiver.account.bank.account))) || '').toString();
  const recvName = ((d.receiver && d.receiver.displayName) || '').toString();

  // ── ชั้น 1: ยอดเงินต้องตรง ───────────────────────────────
  if (Math.round(amount) < price)
    return respond({
      status: 'reject',
      msg: 'ยอดโอนไม่ตรง — สลิปแสดง ' + amount + ' บาท แต่แพ็กเกจนี้ ' + price + ' บาท'
    }, cb);

  // ── ชั้น 2: บัญชีปลายทางต้องเป็นของเรา ──────────────────
  // ใส่เลขบัญชี/พร้อมเพย์ 4 ตัวท้ายใน Config key = 'payee_last4'
  const last4 = (getConfig('payee_last4') || '').toString().trim();
  if (last4 && recvAcc && recvAcc.replace(/\D/g, '').indexOf(last4) === -1)
    return respond({
      status: 'reject',
      msg: 'สลิปนี้โอนเข้าบัญชีอื่น ไม่ใช่บัญชีของ PeekaWord'
    }, cb);

  // ── ชั้น 3: สลิปเก่าซ้ำ ─────────────────────────────────
  if (!transRef)
    return respond({ status: 'manual', msg: 'อ่านเลขอ้างอิงไม่ได้ — ส่งให้ครูตรวจ' }, cb);

  const slipSh = getSheet(SHEET_SLIPS);
  const slipData = slipSh.getDataRange().getValues();
  for (let i = 1; i < slipData.length; i++) {
    if (slipData[i][0].toString() === transRef)
      return respond({ status: 'reject', msg: 'สลิปนี้ถูกใช้ไปแล้ว กรุณาใช้สลิปการโอนครั้งใหม่' }, cb);
  }

  // ── ชั้น 4: สลิปต้องไม่เก่าเกิน 24 ชม. ──────────────────
  try {
    if (d.transDate) {
      const td = new Date(String(d.transDate).replace(/(\d{4})(\d{2})(\d{2})/, '$1-$2-$3'));
      if (!isNaN(td) && (Date.now() - td.getTime()) > 24 * 3600 * 1000)
        return respond({ status: 'manual', msg: 'สลิปเก่ากว่า 24 ชม. — ส่งให้ครูตรวจ' }, cb);
    }
  } catch (e) { /* ข้ามถ้า parse ไม่ได้ */ }

  // ── ผ่านทุกชั้น → บันทึก + อนุมัติอัตโนมัติ ─────────────
  slipSh.appendRow([transRef, orderId, amount, new Date().toISOString()]);

  // อัปเดตแถว Purchases
  const pSh = getSheet(SHEET_PURCHASES);
  const pAll = pSh.getDataRange().getValues();
  let pRow = 0;
  for (let i = 1; i < pAll.length; i++) {
    if (pAll[i][0].toString() === orderId) { pRow = i + 1; break; }
  }
  if (!pRow) {
    pSh.appendRow([orderId, name, phone, existingCode, email, pkg, price, type,
                   'verified', '', new Date().toISOString(), '']);
    pRow = pSh.getLastRow();
  } else {
    if (name)  pSh.getRange(pRow, 2).setValue(name);
    if (phone) pSh.getRange(pRow, 3).setValue(phone);
    if (email) pSh.getRange(pRow, 5).setValue(email);
    pSh.getRange(pRow, 9).setValue('verified');
  }

  // ออก/อัปเกรด student code — ใช้ logic เดิมของ actionVerifyPurchase
  const out = issueOrUpgradeCode_(orderId, pkg, type, name, email, existingCode);
  pSh.getRange(pRow, 12).setValue(out.code);

  return respond({
    status: 'ok',
    msg: 'ตรวจสลิปผ่านอัตโนมัติ',
    code: out.code,
    upgraded: out.upgraded,
    pkg_name: out.pkg_name,
    amount: amount,
    transRef: transRef,
    receiver: recvName
  }, cb);
}

// ── ออกรหัสใหม่ หรือเพิ่ม Level ให้บัญชีเดิม ────────────────
function issueOrUpgradeCode_(orderId, pkg, type, name, email, existingCode) {
  const sh = ensurePasswordColumns_();

  // กรณีซื้อ Level เพิ่ม
  if (existingCode) {
    const st = findStudentByCode_(sh, existingCode);
    if (st) {
      const oldPkg = (st.data[7] || '').toString();
      const oldNums = (oldPkg.match(/\d+/g) || []).map(Number);
      const newNum = levelNumFromPkg(pkg);
      const owned = Array.from(new Set(oldNums.concat([newNum]))).sort(function (a, b) { return a - b; });
      const merged = 'Level ' + owned.join(',');
      sh.getRange(st.row, 8).setValue(merged);
      return { code: existingCode, upgraded: true, pkg_name: merged };
    }
  }

  // ถ้า email นี้เคยซื้อแล้ว → อัปเกรดบัญชีเดิม ไม่ออกรหัสใหม่
  if (email) {
    const st = findStudentByEmail_(sh, email);
    if (st) {
      const oldPkg = (st.data[7] || '').toString();
      const oldNums = (oldPkg.match(/\d+/g) || []).map(Number);
      const newNum = levelNumFromPkg(pkg);
      const owned = Array.from(new Set(oldNums.concat([newNum]))).sort(function (a, b) { return a - b; });
      const merged = 'Level ' + owned.join(',');
      sh.getRange(st.row, 8).setValue(merged);
      sh.getRange(st.row, 4).setValue('active');
      return { code: st.data[0].toString(), upgraded: true, pkg_name: merged };
    }
  }

  // ออกรหัสใหม่ (ไม่ซ้ำของเดิม)
  const data = sh.getDataRange().getValues();
  const used = {};
  for (let i = 1; i < data.length; i++) used[data[i][0].toString()] = 1;
  let code = '';
  for (let t = 0; t < 200; t++) {
    const c = String(Math.floor(100000 + Math.random() * 900000));
    if (!used[c]) { code = c; break; }
  }
  if (!code) code = 'S' + Date.now().toString().slice(-6);

  sh.appendRow([code, name || '', email || '', 'active', new Date().toISOString(),
                'auto-slip', type, pkg, '']);
  return { code: code, upgraded: false, pkg_name: pkg };
}


// ════════════════════════════════════════════════════════════
//  PART 2 — Login ด้วย email + password
// ════════════════════════════════════════════════════════════
//
//  ความปลอดภัย:
//   • หน้าเว็บ hash รหัสผ่านด้วย SHA-256 ก่อนส่ง → รหัสจริงไม่เคยวิ่งผ่านเน็ต
//     และไม่ถูกบันทึกใน log ของ Google (สำคัญ เพราะ JSONP ส่งผ่าน URL)
//   • ฝั่ง server hash ซ้ำอีกชั้นพร้อม salt เฉพาะคน → ต่อให้ Sheet หลุด
//     ก็เอาไป login ไม่ได้ และเทียบข้ามบัญชีไม่ได้
//
//  ?action=setPassword&code=123456&ph=<sha256 ฝั่ง client>&email=x@x.com

function actionSetPassword(p, cb) {
  const code  = (p.code || '').toString().trim();
  const ph    = (p.ph || '').toString().trim().toLowerCase();
  const email = (p.email || '').toString().trim().toLowerCase();

  if (!code || !ph) return respond({ status: 'error', msg: 'ข้อมูลไม่ครบ' }, cb);
  if (!/^[a-f0-9]{64}$/.test(ph))
    return respond({ status: 'error', msg: 'รูปแบบรหัสผ่านไม่ถูกต้อง' }, cb);

  const sh = ensurePasswordColumns_();
  const st = findStudentByCode_(sh, code);
  if (!st) return respond({ status: 'not_found', msg: 'ไม่พบรหัสนักเรียนนี้' }, cb);
  if (st.data[3] !== 'active')
    return respond({ status: 'error', msg: 'บัญชียังไม่ถูกเปิดใช้งาน' }, cb);

  // email ต้องไม่ชนกับบัญชีอื่น
  if (email) {
    const other = findStudentByEmail_(sh, email);
    if (other && other.data[0].toString() !== code)
      return respond({ status: 'error', msg: 'อีเมลนี้ถูกใช้กับอีกบัญชีแล้ว' }, cb);
    sh.getRange(st.row, 3).setValue(email);
  }

  const salt = randomToken_(16);
  sh.getRange(st.row, COL_PASS_SALT + 1).setValue(salt);
  sh.getRange(st.row, COL_PASS_HASH + 1).setValue(sha256_(ph + '|' + salt));
  sh.getRange(st.row, COL_RESET_TOK + 1).setValue('');

  return respond({ status: 'ok', msg: 'ตั้งรหัสผ่านเรียบร้อย', code: code }, cb);
}

// ?action=loginEmail&email=x@x.com&ph=<sha256>
function actionLoginEmail(p, cb) {
  const email = (p.email || '').toString().trim().toLowerCase();
  const ph    = (p.ph || '').toString().trim().toLowerCase();
  if (!email || !ph) return respond({ status: 'error', msg: 'ข้อมูลไม่ครบ' }, cb);

  const sh = ensurePasswordColumns_();
  const st = findStudentByEmail_(sh, email);

  // ข้อความเดียวกันทั้งกรณีไม่มี email และรหัสผิด — กันคนไล่เดาว่ามีใครสมัครบ้าง
  const WRONG = { status: 'error', msg: 'อีเมลหรือรหัสผ่านไม่ถูกต้อง' };
  if (!st) return respond(WRONG, cb);
  if (st.data[3] !== 'active')
    return respond({ status: 'error', msg: 'บัญชียังไม่ถูกเปิดใช้งาน ติดต่อครู' }, cb);

  const salt = (st.data[COL_PASS_SALT] || '').toString();
  const hash = (st.data[COL_PASS_HASH] || '').toString();
  if (!salt || !hash)
    return respond({ status: 'no_password', msg: 'บัญชีนี้ยังไม่ได้ตั้งรหัสผ่าน' }, cb);
  if (sha256_(ph + '|' + salt) !== hash) return respond(WRONG, cb);

  const code = st.data[0].toString();
  return respond({
    status: 'ok',
    code: code,
    name: st.data[1],
    email: st.data[2],
    type: st.data[6],
    pkg_name: st.data[7],
    level: st.data[7],
    progress: progressFor_(code)
  }, cb);
}

// ?action=hasPassword&email=... → ให้หน้าเว็บรู้ว่าต้องพาไปตั้งรหัสมั้ย
function actionHasPassword(p, cb) {
  const email = (p.email || '').toString().trim().toLowerCase();
  const sh = ensurePasswordColumns_();
  const st = email ? findStudentByEmail_(sh, email) : null;
  return respond({
    status: 'ok',
    exists: !!st,
    has_password: !!(st && st.data[COL_PASS_HASH])
  }, cb);
}

// ?action=requestReset&email=... → ส่งลิงก์ตั้งรหัสใหม่ทางอีเมล
function actionRequestReset(p, cb) {
  const email = (p.email || '').toString().trim().toLowerCase();
  const sh = ensurePasswordColumns_();
  const st = email ? findStudentByEmail_(sh, email) : null;

  // ตอบเหมือนกันเสมอ ไม่บอกว่ามี email นี้ในระบบมั้ย
  const SAME = { status: 'ok', msg: 'ถ้ามีบัญชีนี้อยู่ เราส่งลิงก์ตั้งรหัสใหม่ไปที่อีเมลแล้ว' };
  if (!st) return respond(SAME, cb);

  const tok = randomToken_(24);
  const exp = Date.now() + 30 * 60 * 1000;   // 30 นาที
  sh.getRange(st.row, COL_RESET_TOK + 1).setValue(tok + '|' + exp);

  try {
    const base = getConfig('site_url') || 'https://peekaword.pages.dev/English/';
    MailApp.sendEmail({
      to: email,
      subject: 'PeekaWord — ตั้งรหัสผ่านใหม่',
      htmlBody:
        '<div style="font-family:sans-serif;color:#14204A;line-height:1.8">' +
        '<h2 style="color:#14204A">ตั้งรหัสผ่านใหม่</h2>' +
        '<p>กดลิงก์ด้านล่างเพื่อตั้งรหัสผ่านใหม่ (ใช้ได้ 30 นาที)</p>' +
        '<p><a href="' + base + 'reset.html?t=' + tok + '&e=' + encodeURIComponent(email) + '" ' +
        'style="background:#FFB020;color:#14204A;padding:12px 26px;border-radius:24px;' +
        'text-decoration:none;font-weight:bold">ตั้งรหัสผ่านใหม่</a></p>' +
        '<p style="color:#4A5578;font-size:13px">ถ้าไม่ได้เป็นคนขอ ไม่ต้องทำอะไร รหัสเดิมยังใช้ได้ตามปกติ</p>' +
        '</div>'
    });
  } catch (e) { /* โควตาเมลเต็ม — ยังตอบ ok เพื่อไม่เปิดเผยข้อมูล */ }

  return respond(SAME, cb);
}

// ?action=confirmReset&email=...&t=<token>&ph=<sha256 ใหม่>
function actionConfirmReset(p, cb) {
  const email = (p.email || '').toString().trim().toLowerCase();
  const tok   = (p.t || '').toString().trim();
  const ph    = (p.ph || '').toString().trim().toLowerCase();

  if (!email || !tok || !/^[a-f0-9]{64}$/.test(ph))
    return respond({ status: 'error', msg: 'ข้อมูลไม่ครบ' }, cb);

  const sh = ensurePasswordColumns_();
  const st = findStudentByEmail_(sh, email);
  if (!st) return respond({ status: 'error', msg: 'ลิงก์ไม่ถูกต้อง' }, cb);

  const saved = (st.data[COL_RESET_TOK] || '').toString().split('|');
  if (saved[0] !== tok || !saved[1] || Date.now() > parseInt(saved[1]))
    return respond({ status: 'error', msg: 'ลิงก์หมดอายุแล้ว กรุณาขอใหม่' }, cb);

  const salt = randomToken_(16);
  sh.getRange(st.row, COL_PASS_SALT + 1).setValue(salt);
  sh.getRange(st.row, COL_PASS_HASH + 1).setValue(sha256_(ph + '|' + salt));
  sh.getRange(st.row, COL_RESET_TOK + 1).setValue('');

  return respond({ status: 'ok', msg: 'ตั้งรหัสผ่านใหม่เรียบร้อย', code: st.data[0].toString() }, cb);
}
