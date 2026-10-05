# 🆕 วางระบบใหม่บน Google Sheet ใหม่

ใช้เวลารวม ~15 นาที · ทำตามลำดับ ห้ามข้าม

---

## ทำไมถึงคุ้มที่จะเริ่มใหม่

ชีตเดิม (`LexiGo`) มีแต่ข้อมูลทดสอบ — รหัส `123456` · `789454` · `182018` รวม **13 แถว ไม่มีลูกค้าจริง**
และชีตเดิมสร้างสมัยโค้ดยังเป็น v3 หัวคอลัมน์เลยไม่ครบ

**เริ่มใหม่แล้วได้เปรียบตรงนี้:** Code.gs จะ**สร้างทุกแท็บพร้อมหัวคอลัมน์ที่ถูกต้องให้เอง**
รวมถึง `sk_read` · `sk_speak` · `sk_write` ที่ชีตเก่าต้องพิมพ์เพิ่มเอง

---

## ⚠️ จุดที่ต้องรู้ก่อนเริ่ม

Sheet ใหม่ → Apps Script ใหม่ → **URL ใหม่**
ซึ่งเว็บ hardcode URL เดิมไว้ **462 จุด ใน 462 ไฟล์**

เตรียมสคริปต์เปลี่ยนให้แล้ว รันคำสั่งเดียวจบ (ขั้นที่ 5) **อย่าแก้มือ**

---

# ขั้นที่ 1 — สร้าง Sheet ใหม่

1. เปิด https://sheets.new
2. ตั้งชื่อไฟล์ เช่น **PeekaWord DB**
3. ไม่ต้องสร้างแท็บหรือพิมพ์หัวคอลัมน์อะไรทั้งนั้น — โค้ดสร้างให้เอง

# ขั้นที่ 2 — ใส่โค้ด

1. ในชีตใหม่ → **Extensions → Apps Script**
2. ลบโค้ดตัวอย่าง (`function myFunction() {}`) ให้หมด — `Ctrl+A` → `Delete`
3. เปิด `C:\Users\user\Documents\GitHub\lexigo\English\Code.gs` ด้วย Notepad
   → `Ctrl+A` → `Ctrl+C`
4. กลับมาวางใน Apps Script → `Ctrl+V` → `Ctrl+S`
5. ตั้งชื่อ project (ถ้าถาม) เช่น **PeekaWord API**

# ขั้นที่ 3 — Deploy ครั้งแรก

1. กด **Deploy** มุมขวาบน → **New deployment**
   *(รอบนี้ใช้ New deployment ได้ เพราะเป็นของใหม่)*
2. กดไอคอน **⚙️ เฟือง** ข้างคำว่า "Select type" → เลือก **Web app**
3. ตั้งค่า **สำคัญมาก ทั้ง 2 ช่อง**

   | ช่อง | ต้องเลือก |
   |---|---|
   | Execute as | **Me (pasasorn@gmail.com)** |
   | Who has access | **Anyone** ← ไม่ใช่ "Anyone with Google account" |

   > ถ้าเลือก "Anyone with Google account" เด็กที่ไม่ได้ล็อกอิน Google จะใช้ไม่ได้เลย

4. กด **Deploy**
5. Google จะขอสิทธิ์ → **Authorize access** → เลือกบัญชี →
   ถ้าขึ้น *"Google hasn't verified this app"* → กด **Advanced** → **Go to … (unsafe)** → **Allow**
   *(ปลอดภัย เพราะเป็นสคริปต์ของคุณเอง)*
6. **คัดลอก Web app URL** ที่ได้ หน้าตาแบบนี้

   ```
   https://script.google.com/macros/s/AKfycb................../exec
   ```

# ขั้นที่ 4 — ตรวจว่า deploy ติด

วาง URL ที่ได้ในเบราว์เซอร์ แล้วต่อท้ายด้วย `?action=version`

ต้องได้:

```json
{"status":"ok","version":"v6","deployed":"2026-08-29",
 "features":[..., "skill-sync", "purchase-contact-info"]}
```

- ✅ ได้ `v6` → ไปขั้นที่ 5
- ❌ ขึ้นหน้าขอ login → กลับไปแก้ **Who has access** เป็น **Anyone**

# ขั้นที่ 5 — เปลี่ยน URL ในเว็บทั้ง 462 จุด

```powershell
cd C:\Users\user\Documents\GitHub\lexigo\English

py _docs\set_api_url.py --show
```

ดูว่าตอนนี้ใช้ URL อะไรอยู่ แล้วเปลี่ยน (ใส่ URL ใหม่ในเครื่องหมายคำพูด):

```powershell
py _docs\set_api_url.py "https://script.google.com/macros/s/วาง_URL_ใหม่_ที่นี่/exec"
```

ต้องขึ้น:

```
เปลี่ยนแล้ว 462 จุด ใน 462 ไฟล์
เหลือ URL เก่าค้าง: ไม่มี ✅
```

> **ถ้าเปลี่ยนผิด** — `py _docs\set_api_url.py --undo` ย้อนกลับได้ทันที (ทดสอบแล้ว)

# ขั้นที่ 6 — ตั้งค่าในชีต

กลับไปที่ Sheet ใหม่ แท็บต่าง ๆ จะยังไม่มี **จนกว่าจะมีคนเรียก API ครั้งแรก**
ลองเปิด `?action=version` ไปแล้วอาจยังไม่สร้าง — ให้เรียกอันนี้แทนเพื่อบังคับสร้าง:

```
<URL ใหม่>?action=checkCode&code=123456
```

จากนั้นในชีตจะมีแท็บ **Students · Progress · Config · QuizAttempts · QuizScores**

ไปที่แท็บ **Config** แล้วพิมพ์ 3 แถวนี้ (คอลัมน์ A = key, B = value):

| key | value |
|---|---|
| `payee_last4` | เลข 4 ตัวท้ายบัญชีที่รับเงิน |
| `site_url` | `https://peekaword.pages.dev/English/` |
| `pts_full_day` | `50` |

> แท็บ **Progress** ไม่ต้องทำอะไร — หัวคอลัมน์ `sk_read` `sk_speak` `sk_write` ถูกสร้างให้แล้ว

# ขั้นที่ 7 — ตรวจทั้งระบบ

เปิด `_docs\check_backend.html` (ไฟล์นี้ถูกเปลี่ยน URL ให้แล้วในขั้นที่ 5)

1. กด **▶ เริ่มตรวจ** — ต้องผ่านครบ 5 ข้อ
2. กด **▶ ตรวจการเขียน** — ต้องผ่านครบ 4 ข้อ
   ข้อสำคัญคือ *"อ่านคะแนนรายทักษะกลับมา ต้องตรงกับที่ส่งไป"* → `82 / 68 / 54`

# ขั้นที่ 8 — push ขึ้นเว็บ

```powershell
git add -A
git commit -m "chore: point API to new Google Sheet backend"
git push
```

รอ Cloudflare deploy ~1 นาที แล้วทดสอบบนเว็บจริง

---

# ✅ เช็กลิสต์

- [ ] Sheet ใหม่ + วาง Code.gs + Save
- [ ] Deploy → Web app → **Execute as: Me** + **Who has access: Anyone**
- [ ] `?action=version` ได้ `"v6"` และมี `"skill-sync"`
- [ ] `py _docs\set_api_url.py "<URL ใหม่>"` → 462 จุด เหลือเก่า 0
- [ ] เรียก `?action=checkCode&code=123456` เพื่อให้สร้างแท็บ
- [ ] Config เพิ่ม `payee_last4` · `site_url` · `pts_full_day`
- [ ] `check_backend.html` ผ่านทั้ง 2 ส่วน
- [ ] push GitHub
- [ ] **ทดสอบซื้อจริง 1 บาทให้ครบ flow** ← อย่าข้าม
- [ ] ลบข้อมูลทดสอบออกจากชีต

---

# สิ่งที่ยังต้องตั้งเพิ่ม (ถ้าจะเปิดขาย)

| เรื่อง | ทำที่ไหน |
|---|---|
| **SlipOK API key** ตรวจสลิปอัตโนมัติ | แท็บ Config — ดูชื่อ key ใน `Code.gs` ส่วน PART 1 |
| **รหัสครู** (ตอนนี้ `oxford2026`) | `Code.gs` บรรทัด 13 `TEACHER_PASS` — **ควรเปลี่ยนก่อนเปิดขาย** |
| **Analytics** | ยังไม่มีทั้งเว็บ — Cloudflare Web Analytics ติดบรรทัดเดียว |

---

# ชีตเก่ายังอยู่

`LexiGo` ไม่ถูกลบ เก็บไว้เป็นสำรองได้
https://docs.google.com/spreadsheets/d/1Bw39gtFwaFyoHKerWdxyrUecxZZgB-JFnFx8mMSlnQQ/edit

ถ้าระบบใหม่ใช้ได้ดีแล้วค่อยลบทีหลัง
