# 🚀 Deploy Code.gs v5 — ทำตามนี้ (~5 นาที)

> รอบนี้แก้เรื่องเดียว: **เก็บชื่อ/อีเมล/เบอร์ ตอนลูกค้าจ่ายเงิน**
> ถ้าไม่ deploy ระบบยังใช้ได้ แต่ชีต Purchases จะยังว่าง 3 คอลัมน์เหมือนเดิม

---

## ขั้นที่ 1 — วางโค้ดใหม่

1. Google Sheet → **Extensions → Apps Script**
2. **Ctrl+A → Delete** (ลบของเดิมทั้งหมด)
3. เปิด `English/Code.gs` → **Ctrl+A → Ctrl+C** → กลับมาวาง (**1,639 บรรทัด**)
4. **Ctrl+S**

## ขั้นที่ 2 — Deploy

**Deploy → Manage deployments** *(ไม่ใช่ New deployment)*
→ กด ✏️ **ดินสอ** ที่ deployment เดิม
→ ช่อง **Version** เลือก **New version**
→ **Deploy**

> ❌ **ห้ามกด "New deployment"** — URL จะเปลี่ยน แล้วทั้งเว็บเรียก API ไม่ได้

---

## ขั้นที่ 3 — ตรวจว่า deploy ติดจริง ⭐

วางใน browser:

```
https://script.google.com/macros/s/AKfycbz8SuCV8PsUkIElDN3rFm9eE1TKm0UOFS5M_u6TrHmxkslAOQuopYmv3IFM0JBoRYq-/exec?action=version
```

**ต้องได้:**
```json
{"status":"ok","version":"v5","deployed":"2026-08-29",
 "features":[...,"purchase-contact-info","trial-lead-capture"]}
```

- ✅ ได้ `"version":"v5"` → deploy สำเร็จ ไปขั้นที่ 4
- ❌ ยังได้ `"version":"v4"` → **ยังไม่ได้เลือก New version** กลับไปทำขั้นที่ 2 ใหม่

*(นี่คือจุดที่พลาดบ่อยที่สุด — ครั้งก่อนกด Deploy 3 รอบแล้วยังเป็นโค้ดเก่า เพราะลืมสลับ Version dropdown)*

---

## ขั้นที่ 4 — ทดสอบว่าเก็บข้อมูลติดต่อได้จริง

วางใน browser (แทน URL ยาวข้างบนด้วย `...` เพื่อความสั้น):

```
.../exec?action=newPurchase&order_id=TEST-001&pkg=ทดสอบ&price=1&type=trial&name=ทดสอบ ระบบ&email=Test@Mail.com&phone=0812345678
```

**ต้องได้:** `{"status":"ok","order_id":"TEST-001"}`

จากนั้นเปิดชีต **Purchases** → แถวล่างสุดต้องเป็น:

| order_id | name | phone | line_id | email | pkg_name |
|---|---|---|---|---|---|
| TEST-001 | ทดสอบ ระบบ | 0812345678 | *(ว่าง)* | test@mail.com | ทดสอบ |

- ✅ ชื่อ/เบอร์/อีเมลขึ้นครบ + อีเมลเป็นตัวพิมพ์เล็ก → **เสร็จ**
- ❌ ยังว่าง → โค้ดเก่ายังทำงานอยู่ กลับไปขั้นที่ 2

**ลบแถว TEST-001 ทิ้งเมื่อทดสอบเสร็จ**

---

## ขั้นที่ 5 — push เว็บขึ้น GitHub

ไฟล์ฝั่งเว็บที่แก้รอบนี้:

```
English/register.html      ← เพิ่มช่องชื่อ/อีเมล/เบอร์ ตอนจ่ายเงิน
English/trial.html         ← ส่ง lead ไปเก็บที่ backend
English/login.html         ← เก็บอีเมลเข้า session (ให้ลายน้ำแสดงได้)
English/js/protect.js      ← ลายน้ำ + ป้องกันการคัดลอก (ไฟล์ใหม่)
English/Level*/Day*.html   ← ฝัง protect.js 448 ไฟล์
English/dashboard.html
English/Code.gs
```

Cloudflare Pages จะ deploy ให้เองหลัง push

---

## ✅ เช็กลิสต์

- [ ] `?action=version` → `v5`
- [ ] ทดสอบ `newPurchase` → ชีต Purchases มีชื่อ/เบอร์/อีเมลครบ
- [ ] ลบแถว TEST-001
- [ ] push GitHub → รอ Cloudflare deploy (~1 นาที)
- [ ] เปิด `register.html` จริง → เห็นกล่องเขียว "📇 ข้อมูลติดต่อกลับ" ก่อนช่องแนบสลิป
- [ ] เปิด Day ไหนก็ได้ → เห็นลายน้ำจางๆ ทั้งหน้า
- [ ] **ซื้อจริง 1 บาท ให้ครบ flow** ← สำคัญที่สุด อย่าข้าม
