#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Master Wordlist Checker — เช็คว่าคำที่จะใช้ในวันใหม่ ซ้ำกับที่ใช้ไปแล้วมั้ย
วิธีใช้:
  python3 check_new_words.py trip ready pack early wait start together
  หรือ:  python3 check_new_words.py --file candidate.txt
ผลลัพธ์: บอกคำที่ซ้ำ (พร้อมวันที่เคยใช้) และคำที่ปลอดภัย (ใช้ได้)
"""
import sys, csv, os, re
BASE=os.path.dirname(os.path.abspath(__file__))
CSV=os.path.join(BASE,'wordlist_master.csv')

def load():
    """อ่านจากไฟล์ HTML จริงทุกครั้ง — ไม่พึ่ง CSV ที่อาจเก่า
    (เคยพลาดมาแล้ว: CSV ไม่มี Day 241-245 ทำให้เช็กซ้ำไม่เจอ 7 คำ)"""
    import glob
    used = {}
    root = os.path.join(BASE, '..')
    for f in sorted(glob.glob(os.path.join(root, 'Level*', 'Day*.html'))):
        if 'Review' in os.path.basename(f):
            continue
        n = int(re.search(r'Day(\d+)', os.path.basename(f)).group(1))
        h = open(f, encoding='utf-8', errors='ignore').read()
        m = re.search(r'const WORDS\s*=\s*\[(.*?)\n\s*\];', h, re.S)
        if not m:
            continue
        for w in re.findall(r"\{e:'([^']+)'", m.group(1)):
            used.setdefault(w.lower(), []).append('Day%d' % n)
    return used


def main():
    args=sys.argv[1:]
    if not args:
        print(__doc__); return
    if args[0]=='--file':
        words=open(args[1],encoding='utf-8').read().split()
    else:
        words=args
    used=load()
    dup=[]; ok=[]
    for w in words:
        wl=w.lower().strip()
        if not wl: continue
        if wl in used: dup.append((wl,used[wl]))
        else: ok.append(wl)
    print("="*50)
    if dup:
        print("❌ คำที่ซ้ำ (ต้องเปลี่ยน) — %d คำ:"%len(dup))
        for w,days in dup: print("   %-14s เคยใช้: %s"%(w,', '.join(days)))
    else:
        print("✅ ไม่มีคำซ้ำเลย!")
    print("-"*50)
    print("✅ คำที่ใช้ได้ (%d): %s"%(len(ok),', '.join(ok) if ok else '-'))
    print("="*50)
    print("รวมคำในระบบตอนนี้: %d คำไม่ซ้ำ"%len(used))

if __name__=='__main__': main()
