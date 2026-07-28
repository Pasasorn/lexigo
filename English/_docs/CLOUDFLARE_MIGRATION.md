# ☁️ ย้าย PeekaWord ไป Cloudflare Pages

> ใช้เวลา ~15 นาที | ฟรี | **ไม่ต้องแก้ไฟล์ใดๆ** | GitHub Pages เดิมยังใช้ได้ต่อ (ไม่ต้องปิด)

---

## ทำไมต้องย้าย

| | GitHub Pages | Cloudflare Pages |
|---|---|---|
| ความเร็วในไทย | ปานกลาง (server US) | 🚀 เร็วกว่า (CDN มี PoP กรุงเทพ) |
| Bandwidth | จำกัด soft 100GB/เดือน | ไม่จำกัด |
| Build/deploy | ~1-2 นาที | ~30 วินาที |
| Custom domain + SSL | ได้ | ได้ (ฟรี) |
| Workers (API/paywall) | ❌ | ✅ ต่อยอดได้ |

---

## 📝 ขั้นตอน (ทำครั้งเดียว)

### 1. สมัคร Cloudflare (ถ้ายังไม่มี)
- ไปที่ https://dash.cloudflare.com/sign-up
- สมัครด้วย email → ยืนยัน email

### 2. สร้าง Pages project
1. เข้า Dashboard → เมนูซ้าย **Workers & Pages**
2. กด **Create** → แท็บ **Pages** → **Connect to Git**
3. กด **Connect GitHub** → อนุญาต (authorize) Cloudflare
4. เลือก repository: **`peekaword`**
5. กด **Begin setup**

### 3. ตั้งค่า Build (สำคัญ — ใส่ให้ตรง)

| ช่อง | ใส่อะไร |
|------|---------|
| **Project name** | `peekaword` (จะได้ URL `peekaword.pages.dev`) |
| **Production branch** | `main` |
| **Framework preset** | **None** |
| **Build command** | *(เว้นว่าง)* |
| **Build output directory** | *(เว้นว่าง หรือใส่ `/`)* |

> ⚠️ เว็บเราเป็น static HTML ล้วน **ห้ามใส่ build command** ไม่งั้น build fail

6. กด **Save and Deploy** → รอ ~30 วินาที

### 4. ได้ URL ใหม่
```
https://peekaword.pages.dev/English/dashboard.html
https://peekaword.pages.dev/English/register.html
https://peekaword.pages.dev/English/login.html
```

> โครงสร้างโฟลเดอร์เหมือนเดิมทุกอย่าง แค่เปลี่ยน domain

---

## ✅ ทดสอบหลัง deploy

- [ ] เปิด `peekaword.pages.dev/English/login.html` → หน้าโหลดขึ้น
- [ ] login → เข้า dashboard ได้
- [ ] เปิด Day ใดวันหนึ่ง → **ทดสอบไมค์ (Chrome)** ต้องทำงาน
- [ ] register → QR แสดง → อัปสลิปได้
- [ ] teacher.html → อนุมัติได้

> **ไมค์ต้องทำงาน** เพราะ Cloudflare ให้ HTTPS อัตโนมัติ (เงื่อนไขเดียวของ SpeechRecognition)

---

## 🔄 หลังจากนี้ deploy อัตโนมัติ

```
แก้ไฟล์ → GitHub Desktop → Commit → Push
   ↓ (อัตโนมัติ ~30 วินาที)
Cloudflare build & deploy → เว็บอัปเดตเอง
```

ไม่ต้องทำอะไรเพิ่ม เหมือน GitHub Pages แต่เร็วกว่า

---

## 🌐 (ทางเลือก) ใช้ domain ตัวเอง เช่น peekaword.com

1. ซื้อ domain (Namecheap / Cloudflare Registrar / GoDaddy)
2. Cloudflare Pages → project → **Custom domains** → **Set up a domain**
3. ใส่ชื่อ domain → ทำตามที่ระบบบอก (ชี้ nameserver หรือ CNAME)
4. รอ ~5–30 นาที → SSL ออกให้อัตโนมัติ

**ผลลัพธ์:** `https://peekaword.com/English/login.html` (ดูมืออาชีพกว่า `.pages.dev`)

> 💡 ถ้าซื้อ domain ที่ Cloudflare Registrar จะตั้งค่าง่ายสุด (ไม่ต้องย้าย nameserver)

---

## 📌 หลังย้ายเสร็จ ต้องอัปเดตอะไรบ้าง

**ต้องแก้:**
- [ ] `_docs/MASTER_ADMIN.md` + `ALL_LINKS.md` → เปลี่ยน base URL
- [ ] ลิงก์ที่ส่งลูกค้าใน LINE / โฆษณา

**ไม่ต้องแก้:**
- ✅ ไฟล์ HTML ทั้งหมด (ใช้ relative path อยู่แล้ว)
- ✅ Code.gs / Google Apps Script (API URL เดิม)
- ✅ ลิงก์ระหว่างหน้า (Day → Day, dashboard → Level)

---

## ⚠️ ข้อควรรู้

1. **GitHub Pages เดิมยังทำงานอยู่** — ไม่ต้องปิด ใช้เป็น backup ได้
   (ถ้าอยากปิด: repo → Settings → Pages → Unpublish)

2. **นักเรียนเก่าที่ bookmark URL เดิม** ยังเข้าได้ (GitHub Pages ยังอยู่)
   แต่ progress แยกกันคนละ domain! (localStorage ผูกกับ domain)
   → **ควรแจ้งนักเรียนให้ใช้ URL ใหม่อย่างเดียว** หรือปิด GitHub Pages ไปเลยเพื่อกันสับสน

3. **Cloudflare ฟรี** จนกว่าจะเกิน limit ที่สูงมาก (500 builds/เดือน, bandwidth ไม่จำกัด)

---

## 🚀 ต่อยอดในอนาคต (Cloudflare Workers)

เมื่อย้ายมาแล้ว ทำเพิ่มได้:
- **Paywall จริง** — ตรวจสิทธิ์ก่อนส่งไฟล์ Day (แก้ปัญหาเดา URL เข้าฟรี)
- **API ของตัวเอง** — แทน Google Apps Script (เร็วกว่า, ไม่จำกัด quota)
- **Auth ระบบใหม่** — email + password + reset (ถ้าอยากเปลี่ยนภายหลัง)

ทั้งหมดฟรีใน free tier
