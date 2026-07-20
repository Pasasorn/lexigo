---
name: standard-day-pattern
description: >
  Use this skill to generate a new Day HTML file for the Oxford 3000 Word Adventure system,
  following the exact Day 1 architecture. Trigger whenever the user says "สร้างไฟล์ Day",
  "ทำ HTML วันที่", "generate day HTML", "สร้าง interactive lesson", "ทำ Day [N] HTML",
  or asks to create a new day that matches the Day 1 page-based template.
  Always use this skill when the output should be a self-contained .html file with
  5 interactive steps, score bar, TTS, lock system, and completion summary.
  Use even if the user only says "Day [N]" or "ทำ Day ต่อไป" in a lesson-building context.
---

# Standard Day Pattern — Oxford 3000 Word Adventure

## What this skill produces
A single self-contained `.html` file: `Day[N]_[StoryTitle]_A1.html`  
Architecture matches **Day 1** exactly — page-based, 5 steps, score bar, lock, TTS, completion screen.

---

## ⚠️ PRE-BUILD VERIFICATION (ทำก่อนสร้างทุกครั้ง)

**Step 1 — ตรวจ game ของวันก่อนหน้า**
```bash
python3 -c "
import re, glob
f=glob.glob('Day[N-1]_*.html')[0]
html=open(f).read()
m=re.search(r'id=[\"\\x27]p5[\"\\x27].*?step-label[^>]*>([^<]{5,60})', html, re.DOTALL)
print(m.group(1) if m else 'NO P5 / Review Day')
"
```
→ **บันทึกไว้**: วันก่อนใช้ game อะไร  
→ **วันนี้ห้ามซ้ำ** — เลือก game จากตารางด้านล่างที่แตกต่างออกไป

**Step 2 — ตรวจ architecture ของ Day[N-1]**
```bash
grep -c 'class="page"' Day[N-1]_*.html   # ต้องได้ ≥ 5
```
- ≥ 5 = page-based ✅ ดำเนินการต่อได้  
- 0 = section-based ❌ → ต้อง rebuild Day[N-1] ก่อน

**Step 3 — ยืนยัน LOCK_KEY**
- `LOCK_KEY = 'wla_d[N]'` ตรงกับวันที่กำลังสร้าง
- `PREV_KEY = 'wla_d[N-1]'` ตรงกับวันก่อน

---

## Step 5 Game — Actual Assignment per Day

> **กฎสำคัญ**: Game ห้ามซ้ำกับ Day[N-1] — ตรวจก่อนสร้างทุกครั้ง

| Day | Game | Day | Game | Day | Game |
|-----|------|-----|------|-----|------|
| 1 | Word Match (WM) | 11 | True or False (TF) | 21 | Review |
| 2 | Flashcard Quiz (FC) | 12 | Word Scramble (WS) | 22 | Fill in Blank (FB) |
| 3 | Fill in Blank (FB) | 13 | Sentence Builder (SB) | 23 | Sentence Scramble (SS) |
| 4 | Flashcard Quiz (FC) | 14 | Review | 24 | Word Match (WM) |
| 5 | Word Scramble (WS) | 15 | Word Match (WM) | 25 | Memory Flip (MF) |
| 6 | Sentence Builder (SB) | 16 | Memory Flip (MF) | 26 | Fill in Blank (FB) |
| 7 | Review | 17 | Sentence Scramble (SS) | 27 | Sentence Scramble (SS) |
| 8 | Matching Game (WM) | 18 | True or False (TF) | 28 | Review |
| 9 | Flashcard Quiz (FC) | 19 | Word Match (WM) | 29 | Word Match (WM) |
| 10 | Fill in Blank (FB) | 20 | Memory Flip (MF) | 30 | Memory Flip (MF) |

> Day 7, 14, 21, 28 = Review Day — ไม่มี Step 5 game  
> Day 18 = TF (ไม่ใช่ SS เพราะ Day 17 = SS ซ้ำกัน)

**Game pool (Day 31+):** WM | FC | FB | TF | WS | SB | MF | SS  
เลือกโดย: ไม่ซ้ำ Day[N-1] และสลับให้หลากหลาย

---

## File Architecture

### HTML skeleton
```
<body>
  .already-done bar          ← shows "เรียนจบแล้ว" when localStorage has code
  .score-bar                 ← ⭐ Score: N / 6 + progress fill + starDisp
  .vbar                      ← voice selector + speed slider + test button
  <div class="page on fin" id="p0">  ← Cover: word cards + "Let's Start!" button
  <div class="page" id="p1">  ← Step 1: Listen First
  <div class="page" id="p2">  ← Step 2: Read + Listen (SpeechRecognition)
  <div class="page" id="p3">  ← Step 3: Read + Speak (sentence-by-sentence recording)
  <div class="page" id="p4">  ← Step 4: Listen + Arrange
  <div class="page" id="p5">  ← Step 5: Game (see table above)
  <div class="complete-screen" id="completeScreen">
  dot navigation bar (#dots)
  header label (#lbl)
</body>
```

Navigation: `go(n)` — hides current `.page.on`, shows `#p{n}`, updates dots + label.  
Triggers in `go()`: n=3 → `buildSL()`, n=4 → `buildS4()`, n=5 → game function

---

## Data Arrays (top of `<script>`)

```javascript
const WORDS = [
  {e:'cat', ph:'/kæt/', t:'แมว', em:'🐱'},
  // 6-8 words | e=English, t=Thai, ph=IPA, em=emoji optional
  // เรียง A1→A2 ตาม CEFR เสมอ ห้ามสุ่ม
];

const SS = [
  "Leo sees a big cat.",  // Step 3 speak-along — 4-6 full story sentences
];

const DS = [
  "Leo sees a big cat.",   // Step 4 — exactly 3 sentences, easy→harder
  "The dog runs fast.",
  "She has a small fish.",
];

const STORY = `Full story text...`;  // Steps 1 & 2 TTS

const STEPS = ['Cover','Step 1','Step 2','Step 3','Step 4','Step 5'];
```

---

## Score System

| Step | Points | How |
|------|--------|-----|
| Step 1 | 1 pt | `updScore(1)` เมื่อ story จบ |
| Step 2 | 0–2 pt | `updScore(sc, 6)` หลัง recording |
| Step 3 | 0–2 pt | `updScore(sc, 6)` หลัง `checkSummary3()` |
| Step 4 | 0–1 pt | `step4Score` ใน `checkS4()` |
| Step 5 | 0–1 pt | `step5Score` เมื่อ game จบ |

| Group | Days | updScore signature |
|-------|------|-------------------|
| Orange | 1–21 | `updScore(n)` |
| Blue | 22–30 | `updScore(sc, tot)` tot=6 |

---

## Theme Colors by Week

| Week | Days | BG | Primary | Accent |
|------|------|----|---------|--------|
| 1 Animals | 1–7 | `#FFF3E0` | `#E65100` | `#FFE082` |
| 2 Food | 8–14 | `#FFF3E0` | `#E65100` | `#FFE082` |
| 3 Home | 15–21 | `#FBE9E7` | `#E65100` | `#FFCC80` |
| 4 School | 22–28 | `#E3F2FD` | `#1565C0` | `#90CAF9` |
| 5+ | 29–30+ | `#E3F2FD` | `#1565C0` | `#90CAF9` |

`.s4w` border color = week's Accent color.

---

## Step 4: Listen + Arrange (ALL days)

```html
<div class="page" id="p4">
  <div class="step-label">Step 4 · Listen + Write ✏️</div>
  <p class="step-sub">กด ▶ ฟัง → กดคำเรียงประโยค!</p>
  <div id="s4area"></div>
  <div style="margin-top:10px;display:flex;gap:8px">
    <button class="btn btn-p" onclick="checkS4()">Check ✓</button>
    <button class="btn btn-o" onclick="buildS4()">Reset 🔄</button>
  </div>
  <div class="navrow">
    <button class="btn btn-o" onclick="go(3)">← Back</button>
    <button class="btn btn-p" onclick="go(5)">Play Game! 🎮</button>
  </div>
</div>
```

---

## Step 5 Game Implementations

### WM — Word Match
```html
<div class="step-label">Step 5 · Word Match 🎮</div>
<div>⭐ <strong id="wmSc">0</strong>/6 คู่ <div id="wmFill"></div></div>
<div class="wm-grid">
  <div class="wm-col" id="wmEn"></div>
  <div class="wm-col" id="wmTh"></div>
</div>
<button onclick="buildWM()">Reset 🔄</button>
```
```javascript
// ใช้ w.e / w.t
let selE=null,selT=null,wmScore=0;
function buildWM(){wmScore=0;selE=null;selT=null;
  const sh=[...WORDS].sort(()=>Math.random()-.5);
  const thSh=[...WORDS].sort(()=>Math.random()-.5);
  document.getElementById('wmEn').innerHTML=sh.map(w=>
    `<div class="wm-btn wm-en" id="e_${w.e}" onclick="pickE('${w.e}')">${w.e}</div>`).join('');
  document.getElementById('wmTh').innerHTML=thSh.map(w=>
    `<div class="wm-btn wm-th" id="t_${w.e}" onclick="pickT('${w.e}')">${w.t}</div>`).join('');
}
function pickE(k){if(document.getElementById('e_'+k).classList.contains('correct'))return;
  document.querySelectorAll('#wmEn .wm-btn.selected').forEach(el=>el.classList.remove('selected'));
  selE=k;document.getElementById('e_'+k).classList.add('selected');if(selT)checkWM();}
function pickT(k){if(document.getElementById('t_'+k).classList.contains('correct'))return;
  document.querySelectorAll('#wmTh .wm-btn.selected').forEach(el=>el.classList.remove('selected'));
  selT=k;document.getElementById('t_'+k).classList.add('selected');if(selE)checkWM();}
function checkWM(){
  const eEl=document.getElementById('e_'+selE),tEl=document.getElementById('t_'+selT);
  if(selE===selT){eEl.classList.add('correct');tEl.classList.add('correct');wmScore++;
    document.getElementById('wmSc').textContent=wmScore;
    document.getElementById('wmFill').style.width=Math.round(wmScore/WORDS.length*100)+'%';
    if(wmScore>=WORDS.length)setTimeout(showCompletion,400);
  }else{eEl.classList.add('wrong');tEl.classList.add('wrong');
    setTimeout(()=>{eEl.classList.remove('selected','wrong');tEl.classList.remove('selected','wrong');},600);}
  selE=null;selT=null;
}
```

### FC — Flashcard Multiple Choice
```html
<div class="step-label">Step 5 · Flashcard Quiz 🃏</div>
<div id="fcCard" style="font-size:2em;text-align:center;padding:20px"></div>
<div id="fcOpts" style="display:grid;grid-template-columns:1fr 1fr;gap:8px"></div>
<div id="fcResult"></div>
```
```javascript
let fcIdx=0,fcScore=0,fcOrder=[];
function buildFC(){fcOrder=[...WORDS].sort(()=>Math.random()-.5);fcIdx=0;fcScore=0;showFC();}
function showFC(){
  if(fcIdx>=fcOrder.length){showCompletion();return;}
  const w=fcOrder[fcIdx];
  document.getElementById('fcCard').textContent=w.e;
  const opts=[w.t,...WORDS.filter(x=>x.e!==w.e).sort(()=>Math.random()-.5).slice(0,3).map(x=>x.t)]
    .sort(()=>Math.random()-.5);
  document.getElementById('fcOpts').innerHTML=opts.map((o,i)=>
    `<button class="btn" onclick="answerFC(${i},'${o}')" data-ans="${o}">${o}</button>`).join('');
}
function answerFC(i,ans){
  const w=fcOrder[fcIdx];
  document.querySelectorAll('#fcOpts .btn').forEach(b=>{b.disabled=true;
    if(b.dataset.ans===w.t)b.style.background='#C8E6C9';});
  if(ans===w.t)fcScore++;
  fcIdx++;setTimeout(showFC,700);
}
```

### FB — Fill in the Blank
```html
<div class="step-label">Step 5 · Fill in the Blank 🔤</div>
<div id="fbArea"></div>
<button onclick="buildFB()">Reset 🔄</button>
```
```javascript
// ประโยคจาก DS มีช่องว่าง คลิกคำมาเติม
let fbScore=0,fbDone=[];
function buildFB(){fbScore=0;fbDone=DS.map(()=>false);
  document.getElementById('fbArea').innerHTML=DS.map((sent,i)=>{
    const words=WORDS[i%WORDS.length];
    const blank=sent.replace(words.e,'_____');
    return `<div>${blank}<br>`
      +WORDS.sort(()=>Math.random()-.5).map(w=>
        `<button class="g5-ss-word" onclick="fillFB(${i},'${w.e}','${words.e}')">${w.e}</button>`).join('')
      +`<span id="fbfb${i}"></span></div>`;
  }).join('<hr>');}
function fillFB(si,chosen,correct){
  if(fbDone[si])return;
  const fb=document.getElementById('fbfb'+si);
  if(chosen===correct){fb.textContent=' ✓';fb.style.color='green';fbDone[si]=true;fbScore++;
    if(fbDone.every(Boolean))setTimeout(showCompletion,400);
  }else{fb.textContent=' ✗';fb.style.color='red';}
}
```

### TF — True or False
```html
<div class="step-label">Step 5 · True or False ✅</div>
<div id="tfArea"></div>
```
```javascript
// 6 statements based on STORY (3 true, 3 false)
const TF_STMTS=[
  {s:'Leo is in the garden.',ans:true},
  {s:'Mimi has a blue bag.',ans:false},
  // ... 4 more
];
let tfScore=0;
function buildTF(){tfScore=0;
  document.getElementById('tfArea').innerHTML=TF_STMTS.map((st,i)=>
    `<div>${st.s}
      <button onclick="answerTF(${i},true)">✅ True</button>
      <button onclick="answerTF(${i},false)">❌ False</button>
      <span id="tffb${i}"></span>
    </div>`).join('');}
function answerTF(i,ans){
  const st=TF_STMTS[i];
  const fb=document.getElementById('tffb'+i);
  if(ans===st.ans){fb.textContent=' ✓';fb.style.color='green';tfScore++;
    if(tfScore>=TF_STMTS.length)setTimeout(showCompletion,400);
  }else{fb.textContent=' ✗';fb.style.color='red';}
  document.querySelectorAll(`[onclick="answerTF(${i},true)"],[onclick="answerTF(${i},false)"]`)
    .forEach(b=>b.disabled=true);
}
```

### WS — Word Scramble
```html
<div class="step-label">Step 5 · Word Scramble 🔀</div>
<div id="wsArea"></div>
<button onclick="buildWS()">Reset 🔄</button>
```
```javascript
function buildWS(){
  document.getElementById('wsArea').innerHTML=WORDS.map((w,i)=>{
    const sc=[...w.e].sort(()=>Math.random()-.5).join('');
    return `<div>📝 ${sc} → <input id="wsi${i}" style="width:80px">
      <button onclick="checkWS(${i},'${w.e}')">✓</button>
      <span id="wsfb${i}"></span></div>`;
  }).join('');}
let wsScore=0;
function checkWS(i,ans){
  const val=document.getElementById('wsi'+i).value.trim().toLowerCase();
  const fb=document.getElementById('wsfb'+i);
  if(val===ans){fb.textContent=' ✓';fb.style.color='green';wsScore++;
    if(wsScore>=WORDS.length)setTimeout(showCompletion,400);
  }else{fb.textContent=' ✗ ('+ans+')';fb.style.color='red';}
}
```

### SB — Sentence Builder
```html
<div class="step-label">Step 5 · Sentence Builder 🏗️</div>
<div id="sbArea"></div>
<button onclick="buildSB()">Reset 🔄</button>
```
```javascript
// สับคำใน DS[0] ให้เรียงใหม่
let sbPicked=[],sbDone=false;
function buildSB(){sbPicked=[];sbDone=false;
  const sent=DS[0];const words=sent.replace(/[.,!?]/g,'').split(' ');
  const sh=[...words].sort(()=>Math.random()-.5);
  document.getElementById('sbArea').innerHTML=
    '<div id="sbb" style="min-height:36px;border:1.5px dashed #ccc;padding:8px;border-radius:8px;margin-bottom:8px"></div>'
    +'<div>'+sh.map((w,i)=>`<button class="g5-ss-word" id="sbw${i}" data-w="${w}" data-tgt="${words.join(' ')}" onclick="addSBW(${i})">${w}</button>`).join('')+'</div>'
    +'<div id="sbfb"></div>';}
function addSBW(i){
  if(sbDone)return;
  const btn=document.getElementById('sbw'+i);btn.classList.add('used');
  sbPicked.push({w:btn.dataset.w,i});
  const tgt=btn.dataset.tgt.split(' ');
  document.getElementById('sbb').innerHTML=sbPicked.map(x=>x.w).join(' ');
  if(sbPicked.length===tgt.length){
    const ok=sbPicked.map(x=>x.w).join(' ')===tgt.join(' ');
    document.getElementById('sbfb').textContent=ok?'✓ Correct! 🎉':'✗ ลองใหม่';
    if(ok){sbDone=true;setTimeout(showCompletion,400);}
    else{sbPicked=[];document.querySelectorAll('.g5-ss-word.used').forEach(b=>b.classList.remove('used'));
      document.getElementById('sbb').innerHTML='';}
  }
}
```

### MF — Memory Flip (Week 3+)
CSS เพิ่ม:
```css
.g5-mfc{background:#FFF3E0;border:2px solid #FFCC80;border-radius:10px;padding:10px 6px;
  text-align:center;font-size:13px;font-weight:800;color:#E65100;cursor:pointer;
  min-height:48px;display:flex;align-items:center;justify-content:center;
  word-break:break-word;transition:background .2s}
.g5-mfc:hover{background:#FFE0B2}
```
```html
<div class="step-label">Step 5 · Memory Flip 🃏</div>
<p class="step-sub">เปิดไพ่ 2 ใบที่เป็นคู่กัน EN ↔ TH!</p>
<div>🃏 คู่: <strong id="mfsc">0</strong>/<span id="mftotal">6</span>
  <div id="mfbar" style="height:8px;background:#FFE0B2;border-radius:4px;overflow:hidden">
    <div id="mfbarfill" style="height:100%;width:0%;background:#FF7043;transition:width .4s"></div>
  </div>
  <span id="mfpct">0%</span>
</div>
<div id="mfgrid" style="display:grid;grid-template-columns:repeat(4,1fr);gap:8px"></div>
<button class="btn btn-o" onclick="buildMF()">Reset 🔄</button>
```
```javascript
let mfFlipped=[],mfMatched=0,mfLock=false;
function buildMF(){
  mfFlipped=[];mfMatched=0;mfLock=false;
  const cards=[];
  WORDS.forEach((w,i)=>{
    cards.push({txt:w.e,pair:i,type:'en'});  // ใช้ w.e / w.t เสมอ
    cards.push({txt:w.t,pair:i,type:'th'});
  });
  cards.sort(()=>Math.random()-.5);
  document.getElementById('mftotal').textContent=WORDS.length;
  document.getElementById('mfgrid').innerHTML=cards.map((c,i)=>
    `<div class="g5-mfc" id="mf${i}" data-pair="${c.pair}" data-type="${c.type}"
     data-txt="${c.txt}" onclick="flipMF(${i})">?</div>`).join('');
  document.getElementById('mfsc').textContent='0';
  document.getElementById('mfbarfill').style.width='0%';
  document.getElementById('mfpct').textContent='0%';
}
function flipMF(i){
  const el=document.getElementById('mf'+i);
  if(mfLock||el.dataset.done||mfFlipped.find(x=>x.i===i))return;
  el.textContent=el.dataset.txt;el.style.background='#FFF9C4';el.style.borderColor='#F9A825';
  mfFlipped.push({i,el,pair:+el.dataset.pair,type:el.dataset.type});
  if(mfFlipped.length===2){
    mfLock=true;
    const[a,b]=mfFlipped;
    if(a.pair===b.pair&&a.type!==b.type){
      [a.el,b.el].forEach(e=>{e.style.background='#C8E6C9';e.style.borderColor='#43A047';e.dataset.done='1';});
      mfMatched++;
      const p=Math.round(mfMatched/WORDS.length*100);
      document.getElementById('mfsc').textContent=mfMatched;
      document.getElementById('mfbarfill').style.width=p+'%';
      document.getElementById('mfpct').textContent=p+'%';
      mfFlipped=[];mfLock=false;
      if(mfMatched>=WORDS.length)setTimeout(showCompletion,400);
    }else{
      setTimeout(()=>{[a.el,b.el].forEach(e=>{e.textContent='?';e.style.background='';e.style.borderColor='';});
        mfFlipped=[];mfLock=false;},900);
    }
  }
}
```

### SS — Sentence Scramble (Week 3+)
CSS เพิ่ม:
```css
.g5-ss-word{background:#fff;border:2px solid #FFCC80;border-radius:8px;padding:6px 12px;
  font-size:13px;font-weight:800;color:#E65100;cursor:pointer;transition:all .2s}
.g5-ss-word:hover{background:#FFF3E0}
.g5-ss-word.used{opacity:.35;pointer-events:none}
.g5-ss-bw{background:#FFF3E0;border:1.5px solid #FFCC80;border-radius:6px;padding:4px 10px;
  font-size:13px;font-weight:800;color:#E65100;cursor:pointer;margin:2px}
```
```html
<div class="step-label">Step 5 · Sentence Scramble 🔀</div>
<p class="step-sub">กดคำตามลำดับที่ถูกต้อง!</p>
<div id="ssarea" style="display:flex;flex-direction:column;gap:10px"></div>
<button class="btn btn-o" onclick="buildSS()">Reset 🔄</button>
```
```javascript
const SS_SENTS=DS.slice(0,3);  // ใช้ DS (3 ประโยค)
let ssBuilt=[],ssDone=[];
function buildSS(){
  ssBuilt=SS_SENTS.map(()=>[]);ssDone=SS_SENTS.map(()=>false);
  document.getElementById('ssarea').innerHTML=SS_SENTS.map((sent,i)=>{
    const cl=sent.replace(/[.,!?:]/g,'');
    const ws=cl.split(/\s+/).filter(Boolean);
    const sh=[...ws].sort(()=>Math.random()-.5);
    return '<div style="background:#FFF3E0;border-radius:10px;padding:10px 12px;border:1.5px solid #FFCC80">'
      +'<div style="font-size:12px;color:#888;margin-bottom:6px">ประโยค '+(i+1)+':</div>'
      +'<div id="ssb'+i+'" style="min-height:36px;background:#fff;border-radius:8px;padding:8px;'
      +'border:1.5px dashed #FFCC80;display:flex;flex-wrap:wrap;gap:6px;margin-bottom:8px"></div>'
      +'<div id="ssk'+i+'" style="display:flex;flex-wrap:wrap;gap:6px">'
      +sh.map((w,j)=>'<button class="g5-ss-word" id="ssw'+i+'_'+j+'" data-w="'+w
        +'" data-tgt="'+ws.join(' ')+'" onclick="addSSW('+i+','+j+')">'+w+'</button>').join('')
      +'</div><div class="fb" id="ssfb'+i+'"></div></div>';
  }).join('');
}
function addSSW(si,wi){
  if(ssDone[si])return;
  const btn=document.getElementById('ssw'+si+'_'+wi);
  const w=btn.dataset.w;btn.classList.add('used');ssBuilt[si].push({w,wi});
  const bEl=document.getElementById('ssb'+si);
  const sp=document.createElement('button');sp.className='g5-ss-bw';sp.textContent=w;
  sp.onclick=()=>remSSW(si,wi,sp);bEl.appendChild(sp);
  const tgt=btn.dataset.tgt.split(' ');
  if(ssBuilt[si].length===tgt.length){
    const ok=ssBuilt[si].map(x=>x.w).join(' ').toLowerCase()===tgt.join(' ').toLowerCase();
    const fbEl=document.getElementById('ssfb'+si);
    if(ok){fbEl.textContent='✓ Correct! 🎉';fbEl.className='fb ok';ssDone[si]=true;
      if(ssDone.every(Boolean))setTimeout(showCompletion,400);
    }else{fbEl.textContent='✗ ลองใหม่ — กดคำเพื่อเอาออก';fbEl.className='fb err';}
  }
}
function remSSW(si,wi,sp){
  if(ssDone[si])return;
  ssBuilt[si]=ssBuilt[si].filter(x=>x.wi!==wi);sp.remove();
  document.getElementById('ssw'+si+'_'+wi)?.classList.remove('used');
  document.getElementById('ssfb'+si).textContent='';
  document.getElementById('ssfb'+si).className='fb';
}
```

---

## Lock System

```javascript
const LOCK_KEY = 'wla_d[N]';   // e.g. 'wla_d16'
const PREV_KEY = 'wla_d[N-1]'; // e.g. 'wla_d15'

function checkLock(){
  if(localStorage.getItem('wla_admin')==='1'){unlockContent();return;}
  const done=localStorage.getItem(LOCK_KEY);
  if(done){
    document.getElementById('alreadyDone').classList.add('show');
    document.getElementById('savedCode').textContent=done;
  }
  if(localStorage.getItem(PREV_KEY)){unlockContent();}
  else{showLocked();}
}
// Input field: id="codeInput" (ห้ามใช้ "lockInput")
```

---

## DOMContentLoaded — required call order

```javascript
window.addEventListener('DOMContentLoaded', () => {
  checkLock();
  buildDots();          // navigation dots
  loadV();              // TTS voices
  buildCards('cvA');    // word cards Cover — id="cvA" เสมอ (ห้ามใช้ 'acgrid')
  buildS4();            // Step 4
  buildMF();            // ← แทนด้วย game function ที่ใช้จริง (buildWM/buildFC/buildFB/buildTF/buildWS/buildSS)
  buildSL();            // Step 3 mic — เรียกสุดท้ายเสมอ
});
```

---

## ⚠️ Known Bugs — ตรวจก่อน save ทุกครั้ง

| # | อาการ | สาเหตุ | วิธีแก้ |
|---|-------|---------|---------|
| 1 | Step 3 ไม่มีปุ่ม mic | `buildSL()` ไม่ถูกเรียก | เพิ่มใน DOMContentLoaded |
| 2 | Step 4 ว่างเปล่า | `buildS4()` ไม่ถูกเรียก | เพิ่มใน DOMContentLoaded |
| 3 | Step 5 ไม่มีเกม | game function ไม่ถูกเรียก | ตรวจชื่อให้ตรงกับ game จริง |
| 4 | Cover cards ไม่ขึ้น | `buildCards('acgrid')` ผิด | แก้เป็น `buildCards('cvA')` |
| 5 | Lock form error | `getElementById('lockInput')` | แก้เป็น `getElementById('codeInput')` |
| 6 | JS crash ทั้งหน้า | เรียก `buildDL()` แต่ไม่ได้ define | ลบออกจาก DOMContentLoaded |
| 7 | `syncToCloud` error | `wmScore` ไม่ได้ define (เปลี่ยน game แล้ว) | แทนด้วย score variable ที่ตรงกับ game |
| 8 | Step 5 ซ้ำกับ Day[N-1] | ไม่ได้ตรวจ | ดู Pre-Build Verification ด้านบน |
| 9 | Memory Flip ไม่แสดงคำ | ใช้ `w.en`/`w.th` แทน `w.e`/`w.t` | WORDS ทุก Day ใช้ `{e, t, ph}` format |
| 10 | Step 4 DS ว่าง | `DS` array ไม่ได้ define | ตรวจว่า DS มีครบ 3 ประโยค |

---

## Completion Screen

```html
<div class="complete-screen" id="completeScreen">
  <div class="complete-content">
    <div style="font-size:2.5em">🎉</div>
    <h2>Day [N] Complete!</h2>
    <p>Your code: <strong id="codeDisplay"></strong></p>
    <div id="daySummary"></div>
    <button onclick="copyCode()">📋 Copy Code</button>
    <a href="Day[N+1]_[Title].html">
      <button class="btn btn-p">Next Day →</button>
    </a>
  </div>
</div>
```

`showCompletion()` → `generateCode(DAY)` → `buildDaySummary()` → save localStorage  
**ทุก game ต้อง call `showCompletion()` โดยตรง** — ไม่จำเป็นต้อง define `checkGameComplete()`

---

## TTS (required)

```javascript
let allV=[],curV=null;
function loadV(){/* filter en-US voices */}
function speak(t,cb){/* SpeechSynthesisUtterance with curV + rate from #rsl */}
function stopAll(){window.speechSynthesis.cancel();}
window.speechSynthesis.onvoiceschanged=loadV;
setTimeout(loadV,300);setTimeout(loadV,800);setTimeout(loadV,2000);
```

---

## How to generate a new Day file

1. **รับจาก user**: Day N, story title, WORDS (6–8), STORY, SS (4–6), DS (3 easy→hard)
2. **Pre-Build**: ตรวจ game Day[N-1] + architecture (≥5 pages) + LOCK_KEY
3. **เลือก game**: ดูตาราง per-day → ต้องไม่ซ้ำ Day[N-1]
4. **group**: N ≤ 21 = orange → `updScore(n)` | N ≥ 22 = blue → `updScore(sc,6)`
5. **template**: Day 15 (orange) หรือ Day 22 (blue) เป็นต้นแบบ
6. **แทนค่า**: WORDS, SS, DS, STORY, LOCK_KEY, PREV_KEY, DAY, title, emoji, next file link
7. **แทน Step 5**: ลบ game เดิม ใส่ implementation ใหม่จากด้านบน
8. **ตรวจ DOMContentLoaded**: `buildCards('cvA')`, `buildS4()`, game fn, `buildSL()` ครบ
9. **Filename**: `Day[N]_[StoryTitle]_A1.html`

---

## Quality Checklist (ก่อน save ทุกครั้ง)

- [ ] **Pre-build**: ตรวจ game Day[N-1] → วันนี้ใช้ game ที่ต่างออกไป ✓
- [ ] `WORDS` เรียง A1→A2, ทุก item มี `{e, t, ph}` ✓
- [ ] `DS` มีครบ 3 ประโยค, เรียง easy→harder ✓
- [ ] `LOCK_KEY='wla_d[N]'`, `PREV_KEY='wla_d[N-1]'` ถูกต้อง ✓
- [ ] Pages p0–p5 + `.complete-screen` ครบ (Review day: p0–p4 เท่านั้น) ✓
- [ ] Score bar: `#totalSc`, `#sfill`, `#starDisp` มีใน HTML ✓
- [ ] DOMContentLoaded: `buildCards('cvA')`, `buildS4()`, game fn, `buildSL()` ครบ ✓
- [ ] `id="codeInput"` (ไม่ใช่ `lockInput`) ในล็อกฟอร์ม ✓
- [ ] `syncToCloud()` ใช้ score variable ที่ตรงกับ game ปัจจุบัน ✓
- [ ] Step 5 game label + HTML + JS ตรงกัน, `showCompletion()` ถูกเรียกเมื่อจบ ✓
- [ ] Font: `Nunito` load จาก Google Fonts ✓
- [ ] Story ไม่ละเมิดลิขสิทธิ์ (original characters only) ✓
