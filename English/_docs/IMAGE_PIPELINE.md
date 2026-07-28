# 🖼️ PeekaWord — Image Pipeline (ภาพประกอบ 104 วัน)

> อัปเดต: 2026-07-29 | ยึดตาม **PeekaWord Brand Kit**

---

## สถานะปัจจุบัน

| รายการ | จำนวน |
|--------|-------|
| Day ที่มีอยู่ | **104** (Day 1–104) |
| ภาพที่ต้องมี | 104 |
| ภาพที่มีแล้ว | **3** (Day 2, 3, 31) — สไตล์เก่า pastel ยังไม่ตรง Brand Kit |
| **ยังขาด** | **101 รูป** |

---

## ⚠️ บั๊กที่แก้แล้ว (สำคัญ)

เดิม Day file อ้างรูปว่า `src="img_day1.png"` → resolve เป็น `Level1/img_day1.png`
แต่ไฟล์จริงอยู่ใน `Pic English/` → **รูปไม่ขึ้นเลยแม้แต่รูปเดียว**

**แก้แล้ว:** ทั้ง 90 ไฟล์เปลี่ยนเป็น `src="../img/img_dayN.png"`
และสร้างโฟลเดอร์ `img/` ที่ root พร้อมย้ายรูปที่มีเข้าไปแล้ว

---

## 📁 วิธีเพิ่มรูป

1. gen รูปตาม prompt (ดูด้านล่าง)
2. ตั้งชื่อ **`img_dayN.png`** (N = เลขวัน เช่น `img_day15.png`)
3. วางใน `English/img/`
4. commit + push → Cloudflare deploy อัตโนมัติ

> ถ้ายังไม่มีรูป หน้าเว็บจะซ่อนกล่องรูปให้เอง (`onerror`) ไม่พัง

---

## 🎨 Prompt

ไฟล์พร้อมใช้ 2 แบบ (gen จากเนื้อเรื่องจริงของแต่ละวัน):

| ไฟล์ | ใช้กับ |
|------|--------|
| `_docs/image_prompts.txt` | copy วางทีละอัน — Canva Magic Media / ChatGPT / Midjourney |
| `_docs/image_prompts.csv` | ป้อนเข้า batch API / n8n / Make |

**Style block (ตาม Brand Kit):**

```
Children's educational storybook illustration for Thai families.
Warm cream background (#FFF8EF), never pure white.
Soft rounded shapes, no sharp corners.
Cute expressive semi-realistic characters — Thai/Southeast-Asian children,
actively doing the action (speaking, pointing, reaching, playing),
never posing for the camera.
Gentle warm lighting.
Palette: deep navy (#14204A) for outlines and dark areas,
mango yellow (#FFB020) as the single eye-catching accent,
coral (#FF6B5A) and mint green (#12B886) as small touches only.
Large pale circles (12-16% opacity) in the background instead of patterns or gradients.
ABSOLUTELY NO text, letters, words, numbers or signage anywhere in the image.
800x400 landscape banner, digital art, for ages 5-12.
SCENE: [3 ประโยคแรกของเรื่องวันนั้น]
```

**ทำไม prompt เป็นแบบนี้** — map ตรงกับกฎภาพประกอบใน Brand Kit ทุกข้อ:
พื้นครีม / มุมโค้ง / วงกลมจาง / เด็กกำลังทำอะไรอยู่ / ห้ามเด็กฝรั่ง / ห้ามข้อความ

---

## 🔧 ตัวเลือกเครื่องมือ (เรียงตามความคุ้ม)

| ทาง | ราคา 101 รูป | ข้อดี | ข้อเสีย |
|-----|-------------|-------|---------|
| **Canva Magic Media** | ฟรี (Pro quota) | ไม่เสียเพิ่ม สไตล์ใช้ได้ | ทำมือทีละรูป ~3–4 ชม. |
| **ChatGPT Plus / Gemini** | ฟรี (ใน subscription) | คุมสไตล์ดี ต่อรองได้ | ทำมือ ช้าพอกัน |
| **Replicate (Flux schnell)** ⭐ | **~$0.10–0.30** | batch script รันครั้งเดียว 101 รูป ~10 นาที | ต้องมี API key |
| **Ideogram / Recraft** | ~$10–20/เดือน | สม่ำเสมอสูง มี style reference | เสียรายเดือน |

**แนะนำ:** Replicate Flux — ถูกสุด เร็วสุด และเป็น pipeline ที่รันซ้ำได้ตอนทำ Day 105–448
(ถ้าอยากได้ตัวละคร Leo/Mimi/Sam หน้าเดิมทุกวัน ต้องใช้ตัวที่รองรับ character reference เช่น Ideogram)

---

## ✅ QA ก่อน commit

- [ ] ไม่มีตัวหนังสือ/ตัวเลขในรูป (โมเดลชอบแอบใส่)
- [ ] พื้นครีม ไม่ใช่ขาวล้วน
- [ ] เด็กเป็นเอเชีย ไม่ใช่ฝรั่งในห้องเรียนต่างประเทศ
- [ ] เด็กกำลังทำอะไรอยู่ ไม่ใช่นั่งยิ้มมองกล้อง
- [ ] ขนาด 800×400 (หน้าเว็บ crop เป็น `max-height:220px`)
- [ ] ชื่อไฟล์ `img_dayN.png` ตรงเลขวัน
