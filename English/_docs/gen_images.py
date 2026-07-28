#!/usr/bin/env python3
"""
PeekaWord — Batch image generator (Replicate)

ใช้:
  pip install replicate
  set REPLICATE_API_TOKEN=r8_xxxxx        (Windows CMD)
  $env:REPLICATE_API_TOKEN="r8_xxxxx"     (PowerShell)

  python gen_images.py --test            # ลอง 3 รูป (Day 1,2,3) ก่อน
  python gen_images.py --days 1-20       # เจนช่วงที่ระบุ
  python gen_images.py                   # เจนทุกวันที่ยังไม่มีรูป
  python gen_images.py --force --days 2  # เจนทับรูปเดิม

ราคาโดยประมาณ (101 รูป):
  flux-schnell  ~$0.30   เร็วสุด แต่รายละเอียดหลุดบ่อย
  flux-dev      ~$2.50   << แนะนำ สำหรับงานขายจริง
  flux-1.1-pro  ~$4.00   สวยสุด
"""
import os, csv, sys, time, argparse, urllib.request

CSV = os.path.join(os.path.dirname(os.path.abspath(__file__)), "image_prompts.csv")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "img")

MODELS = {
    "schnell": "black-forest-labs/flux-schnell",
    "dev":     "black-forest-labs/flux-dev",
    "pro":     "black-forest-labs/flux-1.1-pro",
}

# กันโมเดลใส่ตัวหนังสือมั่ว + กันภาพสต็อกฝรั่ง (กฎ Brand Kit)
NEGATIVE = ("text, letters, words, numbers, signage, watermark, logo, caption, "
            "subtitles, alphabet, writing, blurry, deformed hands, extra fingers, "
            "creepy, scary, photorealistic stock photo, western classroom")


def parse_days(spec):
    out = set()
    for part in spec.split(","):
        part = part.strip()
        if "-" in part:
            a, b = part.split("-")
            out.update(range(int(a), int(b) + 1))
        elif part:
            out.add(int(part))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="dev", choices=MODELS.keys())
    ap.add_argument("--days", default="")
    ap.add_argument("--test", action="store_true", help="เจนแค่ Day 1,2,3")
    ap.add_argument("--force", action="store_true", help="เจนทับรูปที่มีแล้ว")
    ap.add_argument("--sleep", type=float, default=0.5)
    a = ap.parse_args()

    if not os.environ.get("REPLICATE_API_TOKEN"):
        sys.exit("❌ ยังไม่ได้ตั้ง REPLICATE_API_TOKEN\n"
                 "   เอา token จาก https://replicate.com/account/api-tokens")
    try:
        import replicate
    except ImportError:
        sys.exit("❌ ยังไม่ได้ติดตั้ง: pip install replicate")

    os.makedirs(OUT, exist_ok=True)
    want = parse_days("1,2,3") if a.test else (parse_days(a.days) if a.days else None)

    with open(CSV, encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))

    todo = []
    for r in rows:
        day = int(r["day"])
        if want is not None and day not in want:
            continue
        dest = os.path.join(OUT, r["filename"])
        if os.path.exists(dest) and not a.force:
            continue
        todo.append((day, r, dest))

    if not todo:
        print("✅ ไม่มีรูปที่ต้องเจน (ใช้ --force ถ้าอยากเจนทับ)")
        return

    model = MODELS[a.model]
    est = {"schnell": 0.003, "dev": 0.025, "pro": 0.04}[a.model]
    print(f"🎨 model: {model}")
    print(f"📦 จะเจน {len(todo)} รูป  ·  ประมาณ ${len(todo)*est:.2f}")
    print(f"📁 บันทึกที่: {os.path.normpath(OUT)}\n")

    ok = fail = 0
    for i, (day, r, dest) in enumerate(todo, 1):
        try:
            inp = {
                "prompt": r["prompt"],
                "aspect_ratio": "2:1",          # 800x400 banner
                "output_format": "png",
                "num_outputs": 1,
            }
            if a.model == "schnell":
                inp["num_inference_steps"] = 4
            else:
                inp["num_inference_steps"] = 28
                inp["guidance"] = 3.5
            # flux ไม่มี negative_prompt โดยตรง → ผนวกเป็นคำสั่งห้ามในตัว prompt
            inp["prompt"] += " || AVOID: " + NEGATIVE

            out = replicate.run(model, input=inp)
            item = out[0] if isinstance(out, list) else out
            url = item if isinstance(item, str) else getattr(item, "url", None)

            if url:
                urllib.request.urlretrieve(url, dest)
            else:
                with open(dest, "wb") as f:
                    f.write(item.read())

            ok += 1
            print(f"  [{i}/{len(todo)}] ✅ Day {day:>3} · {r['title'][:34]}")
        except Exception as e:
            fail += 1
            print(f"  [{i}/{len(todo)}] ❌ Day {day:>3} — {e}")
        time.sleep(a.sleep)

    print(f"\n✅ สำเร็จ {ok} · ❌ ล้มเหลว {fail}")
    print("\n📋 ตรวจก่อน push:")
    print("   - ไม่มีตัวหนังสือ/ตัวเลขในรูป (Flux ชอบแอบใส่)")
    print("   - พื้นครีม ไม่ใช่ขาวล้วน")
    print("   - เด็กเป็นเอเชีย และกำลังทำอะไรอยู่")
    print("   รูปไหนไม่ผ่าน → python gen_images.py --force --days <เลขวัน>")


if __name__ == "__main__":
    main()
