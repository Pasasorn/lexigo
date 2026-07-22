# -*- coding: utf-8 -*-
"""
GOLDEN GENERATOR — สร้าง Day HTML ที่ถูกต้อง 100% ในขั้นตอนเดียว
รวม fix ทุกอย่างจาก A1: startRec2+recScores, emoji จริง, sbox=STORY,
Think Q&A ต่อวัน, แบนเนอร์ LINE, robust mic, เกม Step5 หมุน
วิธีใช้: แก้ DATA ด้านล่าง แล้วรัน  python3 golden_generator.py
"""
import re, os
from games_lib import GAMES
BASE=os.path.join(os.path.dirname(__file__),'BASE_Day61.html')
OUTDIR=os.path.dirname(__file__)

# ===== แก้เฉพาะส่วนนี้ต่อวัน =====
DATA=dict(
  n=91, prev=90, level=4, cefr='A2',
  title='Getting Ready', emoji='🎒', theme='A Day Out',
  next_file='Day92_OnTheBus_A2.html', next_emoji='🚌',
  # 7 คำ (A2) — {english, thai, phonetic, emoji}
  words=[
    ('trip','ทริป','/trɪp/','🧳'),('pack','จัดกระเป๋า','/pæk/','🎒'),
    ('start','เริ่ม','/stɑːt/','🏁'),('together','ด้วยกัน','/təˈɡeðə/','👥'),
    ('plan','วางแผน','/plæn/','📋'),('map','แผนที่','/mæp/','🗺️'),
    ('adventure','การผจญภัย','/ədˈventʃə/','🌄'),
  ],
  story="Leo, Mimi, and Ben planned a fun trip together. Early in the morning, Leo packed his bag. Mimi looked at the map. Where should we go? asked Ben. Let us start our adventure! said Leo. The three friends walked out the door together. It was going to be a wonderful day!",
  ss=[
    "Leo, Mimi, and Ben planned a trip.",
    "Leo packed his bag early.",
    "Mimi looked at the map.",
    "Let us start our adventure!",
    "The friends walked out together.",
  ],
  ds=["Leo packed his bag early.","Mimi looked at the map.","Let us start our adventure!"],
  think_q="Who planned the trip together?",
  think_a="Leo, Mimi, and Ben planned it.",
  game='tiles',   # tiles|scramble|memory|wordsearch|vowels
  grammar='Past tense: add -ed → pack becomes packed, look becomes looked.',  # A2 grammar tip
)
# =================================

def esc(s): return s.replace('"','\\"')

# base metadata (Day61 = tiles, scramble game, keys 60/61, emoji 😊, title Happy Feelings)
B=dict(N=61,P=60,NX=62,EMO='😊',TI='Happy Feelings',TH='Feelings',
       NF='Day62_BigFeelings_A1.html',NE='😠',SC='savedCode61',DAYFILE_A1='_A1')

def build(d):
    t=open(BASE,encoding='utf-8').read()
    nn=d['n']; pv=d['prev']; suf='_'+d['cefr']
    # WORDS
    t=re.sub(r"const WORDS=\[.*?\];","const WORDS=[\n"+",\n".join("  {e:'%s',t:'%s',ph:'%s',em:'%s'}"%w for w in d['words'])+"\n];",t,flags=re.DOTALL)
    # SS / DS / STORY
    t=re.sub(r"const SS=\[.*?\];","const SS=[\n"+",\n".join('  "%s"'%esc(s) for s in d['ss'])+"\n];",t,flags=re.DOTALL)
    t=re.sub(r"const DS=\[.*?\];","const DS=[\n"+",\n".join('  "%s"'%esc(s) for s in d['ds'])+"\n];",t,flags=re.DOTALL)
    t=re.sub(r'const STORY="[^"]*";','const STORY="%s";'%esc(d['story']),t)
    # keys
    t=t.replace("PREV_KEY='wla_d%d',MY_KEY='wla_d%d',PREV_PFX='D%d-',MY_DAY=%d"%(B['P'],B['N'],B['P'],B['N']),
                "PREV_KEY='wla_d%d',MY_KEY='wla_d%d',PREV_PFX='D%d-',MY_DAY=%d"%(pv,nn,pv,nn))
    # title/header
    t=t.replace("<title>Day %d — %s</title>"%(B['N'],B['TI']),"<title>Day %d — %s</title>"%(nn,d['title']))
    t=t.replace("%s Day %d · %s"%(B['EMO'],B['N'],B['TI']),"%s Day %d · %s"%(d['emoji'],nn,d['title']))
    t=t.replace("'%s Day %d · '+STEPS[n]"%(B['EMO'],B['N']),"'%s Day %d · '+STEPS[n]"%(d['emoji'],nn))
    t=t.replace("%s!"%B['TI'],"%s!"%d['title'])
    t=t.replace("Day %d · %s — <strong"%(B['N'],B['TH']),"Day %d · %s — <strong"%(nn,d['theme']))
    # counts: 6 → 7 new words
    t=t.replace("6 new words","%d new words"%len(d['words']))
    # alreadyDone / savedCode / lock / complete
    t=t.replace("เรียน Day %d จบแล้ว"%B['N'],"เรียน Day %d จบแล้ว"%nn)
    t=t.replace("Day %d ปลดล็อกแล้ว"%B['NX'],"Day %d ปลดล็อกแล้ว"%(nn+1))
    t=t.replace('id="%s"'%B['SC'],'id="savedCode%d"'%nn).replace("getElementById('%s')"%B['SC'],"getElementById('savedCode%d')"%nn)
    t=t.replace("Day %d ยังล็อกอยู่"%B['N'],"Day %d ยังล็อกอยู่"%nn).replace("Unlock Day %d"%B['N'],"Unlock Day %d"%nn)
    t=t.replace('placeholder="D%d-????"'%B['P'],'placeholder="D%d-????"'%pv)
    t=t.replace("Day %d Complete!"%B['N'],"Day %d Complete!"%nn)
    t=t.replace("Completion Code — Day %d"%B['N'],"Completion Code — Day %d"%nn)
    t=t.replace('id="codeDisplay">D%d-????'%B['N'],'id="codeDisplay">D%d-????'%nn)
    t=t.replace("Day %d ปลดล็อกอัตโนมัติแล้ว"%B['NX'],"Day %d ปลดล็อกอัตโนมัติแล้ว"%(nn+1))
    # nav
    t=t.replace('href="%s"'%B['NF'],'href="%s"'%d['next_file'])
    t=t.replace("%s Day %d →"%(B['NE'],B['NX']),"%s Day %d →"%(d['next_emoji'],nn+1))
    # sbox (visible story) = STORY with vocab highlighted
    words=[w[0] for w in d['words']]; html=d['story']
    for w in sorted(set(words),key=len,reverse=True):
        html=re.sub(r'\b(%s)\b'%re.escape(w),lambda m:'<span class="vocab">%s</span>'%m.group(1),html,flags=re.IGNORECASE)
    t=re.sub(r'(<div class="sbox">).*?(</div>)',lambda m:m.group(1)+html+m.group(2),t,count=1,flags=re.DOTALL)
    # Think Q&A
    t=re.sub(r'💬 Think: [^<]*','💬 Think: '+d['think_q'],t,count=1)
    t=re.sub(r'(<div id="thinkAns"[^>]*>)✅[^<]*(</div>)',lambda m:m.group(1)+'✅ '+d['think_a']+m.group(2),t,count=1)
    # image
    t=re.sub(r'img_day\d+\.png','img_day%d.png'%nn,t)

    # ---- SWAP Step 5 game (5-game rotation) ----
    if d.get('game') and d['game'] in GAMES:
        ghtml,gjs=GAMES[d['game']]
        NAV='<div class="navrow"><button class="btn btn-o" onclick="go(4)">← Back</button><button class="btn btn-p" onclick="showCompletion()">🏆 Finish!</button></div>'
        t=re.sub(r'(<div class="page" id="p5">\s*\n).*?('+re.escape(NAV)+r')',
                 lambda m:m.group(1)+ghtml+'  '+m.group(2),t,count=1,flags=re.DOTALL)
        t=re.sub(r'let g5[\s\S]*?function g5end\([^)]*\)\{[\s\S]*?\}',lambda m:gjs,t,count=1)
    # ---- Grammar Spotlight box (A2) ----
    if d.get('grammar'):
        gbox=('\n  <div style="margin-top:10px;background:#EDE7F6;border:2px solid #B39DDB;border-radius:14px;padding:11px 14px">'
              '<div style="font-size:13px;font-weight:900;color:#5E35B1">📝 Grammar: '+d['grammar']+'</div></div>')
        # ใส่ต่อจากกล่อง thinkAns ใน Step 2
        t=re.sub(r'(<div id="thinkAns"[^>]*>✅[^<]*</div></div>)',lambda m:m.group(1)+gbox,t,count=1)
    return t

out=build(DATA)
fn='Day%d_%s_%s.html'%(DATA['n'],DATA['title'].replace(' ',''),DATA['cefr'])
open(os.path.join(OUTDIR,fn),'w',encoding='utf-8').write(out)
leak=out.count('Day 61')+out.count('wla_d61')+out.count('D61-')+out.count('Happy Feelings')
print("✅ สร้าง %s | leftover=%d (ควร 0)"%(fn,leak))
