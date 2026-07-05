# Daily Lesson Blueprint — Oxford 3000 Word Adventure

## โครงสร้างทั้งหมด: Cover + 5 Steps

---

## 🏠 Cover Page (p0)

**จุดประสงค์:** แนะนำคำศัพท์ก่อนเรียน

**มีอะไร:**
- Emoji ประจำวัน + ชื่อเรื่อง + จำนวนคำ
- Vocab Cards 6 ใบ (grid 2×3) — แต่ละใบมี SVG icon, คำภาษาอังกฤษ, สัทอักษร, คำแปลภาษาไทย
- กดการ์ดแล้วออกเสียงคำนั้น (TTS)
- ปุ่ม "Let's Start!" → ไป Step 1

**Data ที่ต้องกำหนดในแต่ละไฟล์:**
```js
const WORDS = [
  {e:'cat', t:'แมว', ph:'/kæt/'},
  ...
]
```

---

## 🎧 Step 1 · Listen First (p1)

**จุดประสงค์:** ฝึกทักษะ Listening — ฟังเรื่องโดยไม่ดูตัวหนังสือ

**มีอะไร:**
- ปุ่ม ▶ Play Story → เล่น TTS เรื่องทั้งหมด
- ปุ่ม ■ Stop
- รูป illustration (img_dayN.png) — ซ่อนอัตโนมัติถ้าไม่มีไฟล์
- Think box — คำถาม comprehension 1 ข้อ

**Data:**
```js
const STORY = "Leo has a cat. Her name is Nala..."
```

**หมายเหตุ:** ยังไม่มี scoring — เป็น warm-up

---

## 📖 Step 2 · Read + Listen (p2)

**จุดประสงค์:** ฝึก Reading + Speaking โดยมีเสียงช่วย

**มีอะไร:**
- ปุ่ม ▶ Play Story + ■ Stop
- รูป illustration (img_dayN.png)
- เรื่องสั้น — คำศัพท์ highlight สีม่วง (`.vocab`)
- ปุ่ม 🎤 "อ่านทั้งเรื่อง" — บันทึกเสียงทั้งเรื่อง
- Progress bar แสดงคะแนน % แบบ real-time
- Auto-stop หลังเงียบ 2.5 วินาที
- Step Summary แสดงคะแนนแยกทีละประโยค

**Scoring:** เปรียบเทียบ transcript vs. ประโยคในเรื่อง (word match %)

**Data:**
```js
const SS = [  // Speak Sentences — ทุกประโยคในเรื่อง
  "Leo has a cat.",
  "Nala is small and white.",
  ...
]
```

---

## 🗣️ Step 3 · Read + Speak (p3)

**จุดประสงค์:** ฝึก Speaking ทีละประโยค — อ่านตามแล้ววัดคะแนน

**มีอะไร:**
- ประโยคละ 1 row มี: ตัวหนังสือ + ▶ ฟัง + 🎤 พูด
- กด 🎤 → บันทึก → แสดงคะแนน % + สี (เขียว/เหลือง/แดง)
- แสดงข้อความที่ได้ยิน ("ได้ยิน: ...")
- Step Summary รวมคะแนนเฉลี่ยทุกประโยค

**Scoring:** word match % เทียบกับ target sentence

**Data:** ใช้ `SS` เดิมจาก Step 2

---

## ✏️ Step 4 · Listen + Write / Dictation (p4)

**จุดประสงค์:** ฝึก Writing — ฟังแล้วพิมพ์

**มีอะไร:**
- 3 ประโยค (คัดจากเรื่อง)
- แต่ละข้อ: ปุ่ม ▶ Play + ช่องพิมพ์
- ปุ่ม "Check ✓" → ตรวจทุกข้อพร้อมกัน + เสียง feedback
  - ถูกทุกข้อ → "Perfect!" / "Amazing!"
  - ถูกบางข้อ → "Correct!" / "Great job!"
  - ผิดทุกข้อ → "Try again!" / "Keep trying!"
- ปุ่ม "Show Answers" → เฉลย

**Data:**
```js
const DS = [  // Dictation Sentences — 3 ประโยค
  "Leo has a cat.",
  "Boon is big and brown.",
  "Leo loves all his animals."
]
```

---

## 🎮 Step 5 · Word Match Game (p5)

**จุดประสงค์:** ฝึก Vocabulary — จับคู่คำ EN ↔ TH

**มีอะไร:**
- คอลัมน์ซ้าย: คำภาษาอังกฤษ (สุ่มลำดับ)
- คอลัมน์ขวา: คำแปลภาษาไทย (สุ่มลำดับ)
- กด EN → กด TH → ถ้าถูกเปลี่ยนเป็นสีเขียว + เสียง "Correct!"
- ถ้าผิด สั่นแดง + เสียง "Try again!"
- Progress bar + คะแนน / 6
- เมื่อได้ ≥ 4/6 → แสดง Completion Screen

**Completion Screen มี:**
- Day Summary (bar chart Step 2–5 %)
- Completion Code (D1-XXXX) — generate ครั้งเดียว บันทึก localStorage
- ปุ่ม Copy Code
- ลิงก์ → หน้าหลัก | Day ถัดไป

---

## ⚙️ ระบบที่ทำงานอยู่เบื้องหลัง

| ระบบ | หน้าที่ |
|------|--------|
| TTS (Web Speech API) | อ่านออกเสียง — เลือก voice + ปรับ speed ได้ |
| SpeechRecognition API | รับเสียงพูด Step 2, 3 |
| localStorage | เก็บ completion code + progress + lock ระหว่าง Day |
| Google Sheets API | sync คะแนนไปยัง cloud |
| Feedback Sound | speakFb() — สุ่ม phrase ตาม correct/wrong/perfect |

---

## 🔒 Lock System

- **Day 1:** ไม่มี lock — เปิดได้เลย
- **Day 2+:** ตรวจ `localStorage.getItem('wla_dN')` ถ้าไม่มี → แสดง lock screen
- **Admin bypass:** `localStorage.getItem('wla_admin') === '1'`
- **Code format:** `D1-ABCD` (Day + 4 ตัวอักษร random)

---

## 📁 ไฟล์ที่เกี่ยวข้อง

| ไฟล์ | หน้าที่ |
|------|--------|
| DayN_[Title]_A1.html | บทเรียนรายวัน |
| img_dayN.png | รูป illustration (ใน Pic English/) |
| admin.html | หน้าหลัก + ระบบ admin |
| leaderboard.html | อันดับนักเรียน |
| progress.html | สรุปความคืบหน้า |
| competition-quiz.html | แข่งขัน 5 ด่าน |

---

## 🎨 Color Theme ตาม Week

| Week | Theme | สี header |
|------|-------|-----------|
| 1 | Animals | Orange #FF9800 |
| 2 | Food | Green #66BB6A |
| 3 | Home/Family | Purple #AB47BC |
| 4 | School | Blue #42A5F5 |
