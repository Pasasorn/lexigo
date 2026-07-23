# 🔐 LexiGo — Master Admin (ลิงก์ + รหัสทั้งหมด)

> อัปเดต: 2026-07-23 | **เก็บไฟล์นี้เป็นความลับ อย่าแชร์ลูกค้า**
> Base URL: `https://pasasorn.github.io/lexigo/English/`

---

## 🔑 รหัสสำคัญ 3 ชุด (จำให้ได้)

| รหัส | ค่า | ใช้ที่ไหน |
|------|-----|----------|
| **Teacher (อนุมัติสลิป)** | `oxford2026` | teacher.html — ตั้งใน Code.gs บรรทัด 13 |
| **Admin (ดู dashboard ทุก Level)** | `Gift0142` | dashboard.html?admin= / gate |
| **Token ชื่อไฟล์ admin** | `k7m3x9q2p5` | panel/gate filenames |

---

## 🛠️ หน้า Admin (สำหรับคุณ — อย่าส่งใคร)

| หน้า | ลิงก์ | รหัส |
|------|-------|------|
| 🔓 **อนุมัติสลิป/คำสั่งซื้อ** | `.../teacher.html` | `oxford2026` |
| 🛠️ Admin Panel (กดเปิดทุก Day) | `.../panel-k7m3x9q2p5.html` | — |
| 🔒 Admin Gate (ใส่รหัสเข้า dashboard) | `.../gate-k7m3x9q2p5.html` | `Gift0142` |
| ⚡ Dashboard admin (URL ตรง) | `.../dashboard.html?admin=Gift0142` | — |
| ❌ ปิด admin mode | `.../dashboard.html?admin=off` | — |

---

## 🌐 หน้าสำหรับลูกค้า/นักเรียน (ส่งได้)

| หน้า | ลิงก์ | ใคร |
|------|-------|-----|
| 🛒 **สมัคร + จ่ายเงิน** | `.../register.html` | ลูกค้าใหม่ |
| ➕ ซื้อ Level เพิ่ม | `.../register.html?buymore=1` | ลูกค้าเก่า (มีปุ่มใน dashboard) |
| 🔑 **Login** | `.../login.html` | นักเรียนที่ซื้อแล้ว |
| 🏠 Dashboard | `.../dashboard.html` | นักเรียน (หลัง login) |
| 📊 Progress | `.../progress.html` | นักเรียน |
| 🎯 Placement Test | `.../placement-test.html` | ทดสอบระดับ |
| 🏆 Leaderboard | `.../leaderboard.html` | นักเรียน |
| ⚡ Competition Quiz | `.../competition-quiz.html` | นักเรียน |
| 🥇 Competition Dashboard | `.../competition-dashboard.html` | นักเรียน |

> **⚠️ ตอนส่งลิงก์ใน LINE:** เขียนกำกับ *"เปิดใน Chrome นะคะ (ไมค์ใช้ในไลน์ไม่ได้)"*

---

## ⚙️ Backend (Google Apps Script)

| รายการ | ค่า |
|--------|-----|
| **API endpoint (/exec)** | `https://script.google.com/macros/s/AKfycbz8SuCV8PsUkIElDN3rFm9eE1TKm0UOFS5M_u6TrHmxkslAOQuopYmv3IFM0JBoRYq-/exec` |
| **เปิด Apps Script editor** | Google Sheet → Extensions → Apps Script หรือ https://script.google.com/home |
| **Teacher pass** | `oxford2026` (Code.gs บรรทัด 13) |

> **Deploy Code.gs:** วางทับ → Save → Deploy → **Manage deployments → edit → New version** (อย่าสร้าง deployment ใหม่ URL จะเปลี่ยน)

---

## 📚 บทเรียน (สำหรับตรวจ/ทดสอบ)

| Level | Day | โฟลเดอร์ | CEFR |
|-------|-----|----------|------|
| 1 | 1–30 | `Level1/` | A1 |
| 2 | 31–60 | `Level2/` | A1 |
| 3 | 61–90 | `Level3/` | A1 |
| 4 | 91–120 | `Level4/` | A2 (Day 91–97 เสร็จ) |

ตัวอย่าง: `.../Level1/Day1_LeosBigDay_A1.html`
ลิงก์ Day รายวันครบ: ดูใน `_docs/ALL_LINKS.md`

---

## 💰 ราคา

| แบบ | ราคา |
|-----|------|
| ราย Level (30 วัน) | **฿599** |
| Lifetime (15 Level) | ฿2,590 / 2,990 / 3,990 / 4,590 |

QR PromptPay: `qr_promptpay.JPG` (ในโฟลเดอร์ root)

---

## 🔧 Flow ระบบขาย

```
1. ลูกค้า → register.html → เลือก Level → จ่าย QR → อัปสลิป
2. คุณ → teacher.html (oxford2026) → Orders → ดูสลิป → อนุมัติ
3. ระบบออก student code (หรือ upgrade บัญชีเดิมถ้าซื้อเพิ่ม)
4. ลูกค้า → login.html → ใส่ code → เข้าเรียน (เห็นเฉพาะ Level ที่ซื้อ)
```

---

## 📌 เครื่องมือช่วย (ใน _docs/)

| ไฟล์ | ใช้ทำอะไร |
|------|-----------|
| `wordlist_master.csv` | คำศัพท์ทั้งหมด 468 คำ + level/week |
| `check_new_words.py` | เช็คคำซ้ำก่อนสร้าง Day ใหม่ |
| `golden/golden_generator.py` | สร้าง Day ใหม่ (ถูกทุกจุด) |
| `Level4_Plan_Day91-120.md` | แผน Level 4 (A2) |
| `ALL_LINKS.md` | ลิงก์ Day รายวันครบ |
