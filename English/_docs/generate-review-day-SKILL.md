---
name: generate-review-day
description: >
  Use this skill to generate a complete Week Review HTML file for the Oxford 3000 Word Adventure
  system, following the exact Day 7/14/21/28 architecture with 7 games + Speak Up! recording.
  Trigger whenever the user says "สร้าง review day", "ทำ HTML review", "generate review HTML",
  "สร้างไฟล์ Day Review", "ทำ Week Review วันที่", or asks to build a review day for any week.
  Always use when output should be a self-contained .html review file with 8 pages (Menu + 7 games),
  oval float balloons, sentence-based Speak Up!, and audio-stop-on-page-change.
  Use even if the user only says "Review Week [N]" or "ทำ Day [7/14/21/28]".
---

# Generate Review Day — Oxford 3000 Word Adventure

## What this skill produces
A single self-contained `.html` file: `Day[N]_Week[W][Theme]Review_A1.html`  
Architecture: **8 pages** (p0 Menu + p1–p7 games), score bar, TTS, lock system, completion screen.

---

## Data Arrays (define at top of `<script>`)

```javascript
const WORDS = [
  {e:'cat', day:1, icon:'🐱'},
  // ... 36 words (Days D-5 through D-1, 6 words each day)
  // NO Thai 't' field — English-only games
];

const SB_LIST = [
  {w:['The','cat','runs','fast','.']},
  {w:['She','has','a','big','cup','.']},
  // 5 sentences minimum, drawn from review words
  // used in both Sentence Builder (p6) AND Speak Up! (p7)
];
```

---

## File Architecture (8 pages)

```
body
  .already-done bar    ← "เรียนจบแล้ว" when localStorage has completion code
  .score-bar           ← ⭐ Score + #sfill progress + #starDisp
  .vbar                ← voice selector (#vsel) + speed slider (#rsl) + test button
  .mainContent
    <div class="page on" id="p0">  ← Menu: title + 3×2 grid + SP button + Results button
    <div class="page" id="p1">    ← Listen & Select (LC)
    <div class="page" id="p2">    ← Listen & Pick (LP)
    <div class="page" id="p3">    ← Speed Quiz (SQ)
    <div class="page" id="p4">    ← Balloon Pop (BP)
    <div class="page" id="p5">    ← Whack-a-Word (WA)
    <div class="page" id="p6">    ← Sentence Builder (SB)
    <div class="page" id="p7">    ← Speak Up! (SP)
  </div><!-- end mainContent -->
  .complete-screen     ← Completion overlay with code
  #dots                ← Navigation dots (8 dots: 0–7)
```

---

## p0 Menu Layout

```html
<div class="page on" id="p0">
  <div class="step-label">🌈 Week [W] Review</div>
  <p class="step-sub">เลือกเกมที่อยากเล่น!</p>
  <div style="font-size:13px;...">⭐ Score: <span id="totalSc">0</span></div>
  <div class="score-line">...</div>
  <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px">
    <button onclick="go(1);initLC()">👂 Listen & Select</button>
    <button onclick="go(2);initLP()">👂 Listen & Pick</button>
    <button onclick="go(3);initSQ()">⚡ Speed Quiz</button>
    <button onclick="go(4);initBP()">🎈 Balloon Pop</button>
    <button onclick="go(5);initWA()">🔨 Whack-a-Word</button>
    <button onclick="go(6);initSB()">🧩 Sentence Builder</button>
  </div>
  <!-- SP button: FULL WIDTH, purple gradient, below 3×2 grid -->
  <button onclick="go(7);initSP()" style="background:linear-gradient(135deg,#9C27B0,#4A148C);width:100%;...">
    🎤 Speak Up! — Read sentences aloud!
  </button>
  <button onclick="showCompletion()">🏆 See Week [W] Results!</button>
</div>
```

---

## Score System

```javascript
let lcScore=0, lpScore=0, sqScore=0, bpScore=0, waScore=0, sbScore=0, spScore=0;
let totalScore=0;

function updateScore(){
  const total = lcScore+lpScore+sqScore+bpScore+waScore+sbScore+spScore;
  totalScore = total;
  document.getElementById('totalSc').textContent = total;
  const pct = Math.min(100, Math.round(total / 7.75));    // ← 7.75 divisor
  document.getElementById('sfill').style.width = pct+'%';
  const stars = total>=550?'⭐⭐⭐':total>=375?'⭐⭐☆':'⭐☆☆';  // ← 550/375 thresholds
  document.getElementById('starDisp').textContent = stars;
}
```

Max scores per game: LC≈100, LP≈80, SQ≈75, BP≈150, WA≈120, SB≈100, SP=150 → total ~775

---

## go() Function — CRITICAL

```javascript
let curPage = 0;
function go(n){
  synth.cancel();            // ← stop ALL audio on page change
  spListening = false;       // ← stop any active speech recognition
  document.querySelectorAll('.page').forEach(p=>p.classList.remove('on'));
  const pg = document.getElementById('p'+n);
  if(pg) pg.classList.add('on');
  curPage = n;
  const dots = document.getElementById('dots');
  if(dots){
    dots.innerHTML = '';
    [0,1,2,3,4,5,6,7].forEach(i=>{   // ← 8 dots (0–7)
      const d = document.createElement('div');
      d.className = 'dot'+(i===n?' on':'');
      d.onclick = ()=>go(i);
      dots.appendChild(d);
    });
  }
}
```

---

## curPage Guards (prevent audio bleed between pages)

All setTimeout callbacks that trigger after user may have navigated must check `curPage`:

```javascript
// Example in LC game:
function checkLC(){
  // ...scoring...
  setTimeout(()=>{ if(curPage===1){ lcIdx++; renderLC(); } }, 1200);
}

// Example in SB game:
function sbCheck(){
  // ...scoring...
  setTimeout(()=>{ if(curPage===6){ sbIdx++; renderSB(); } }, 1200);
}
```

Apply this guard to: checkLC (p1), checkLP (p2), checkSQ (p3), sbCheck (p6), spManual+startSP (p7)

---

## Game 4: Balloon Pop (BP) — Oval Float Style

```css
.bp-arena{position:relative;height:300px;background:linear-gradient(180deg,[SKY_TOP] 0%,[SKY_MID] 60%,[SKY_BTM] 100%);overflow:hidden;border-radius:16px;margin-bottom:10px}
.balloon{position:absolute;width:60px;height:72px;border-radius:50% 50% 50% 50% / 60% 60% 40% 40%;display:flex;align-items:center;justify-content:center;font-size:12px;font-weight:900;color:#fff;cursor:pointer;text-align:center;padding:6px;text-shadow:0 1px 2px rgba(0,0,0,.4);bottom:-110px}
.balloon::after{content:'';position:absolute;bottom:-16px;left:50%;transform:translateX(-50%);width:1px;height:16px;background:rgba(0,0,0,.25)}
@keyframes floatUp{from{bottom:-110px}to{bottom:105%}}
```

```javascript
function nextBalloon(){
  const w = bpDeck[bpRound % bpDeck.length];
  // pick 4 choices (1 correct + 3 wrong)
  const area = document.getElementById('bpArena'); // ← ID = bpArena (NOT bpArea)
  area.innerHTML = '';
  document.getElementById('bpPrompt').textContent = w.icon+' What is this?';
  speak(w.e);
  const colors = ['#FF6B9D','#FFB347','#87CEEB','#98E89A'];
  const lefts = [5,28,52,72];
  choices.forEach((c,i)=>{
    const b = document.createElement('div');
    b.className = 'balloon';
    b.textContent = c.e;
    b.style.background = colors[i];
    b.style.left = lefts[i]+'%';
    b.style.animationName = 'floatUp';
    b.style.animationDuration = (5+i*0.4)+'s';
    b.style.animationTimingFunction = 'linear';
    b.style.animationFillMode = 'forwards';
    b.onclick = ()=>popBalloon(c.e===w.e, b, area);
    area.appendChild(b);
  });
  bpTimeout = setTimeout(()=>{ if(bpActive) nextBalloon(); }, 6500);
}
```

Sky gradient colors by week theme:
| Week | SKY_TOP | SKY_MID | SKY_BTM |
|------|---------|---------|---------|
| 1 Animals (Rainbow) | `#FFF8E1` | `#FFE0B2` | `#FFCC80` |
| 2 Food (Orange) | `#FFF3E0` | `#FFCCBC` | `#FFAB91` |
| 3 Home (Green) | `#E8F5E9` | `#C8E6C9` | `#A5D6A7` |
| 4 School (Blue) | `#E8EAF6` | `#C5CAE9` | `#9FA8DA` |

---

## Game 7: Speak Up! (SP) — Sentence-Based

```javascript
let spScore=0, spIdx=0, spSentList=[], spListening=false;
const SR_API = window.SpeechRecognition || window.webkitSpeechRecognition;

function initSP(){
  spScore=0; spIdx=0; spListening=false;
  spSentList = shuffle(SB_LIST);   // ← uses same SB_LIST as Sentence Builder
  document.getElementById('spDone').style.display='none';
  document.getElementById('spSc').textContent=0;
  document.getElementById('spTotal').textContent=spSentList.length;
  if(!SR_API){ document.getElementById('spAlt').style.display='block'; }
  else{ document.getElementById('spAlt').style.display='none'; }
  renderSP();
}

function renderSP(){
  if(spIdx>=spSentList.length){ endSP(); return; }
  const s=spSentList[spIdx];
  document.getElementById('spNum').textContent=spIdx+1;
  document.getElementById('spSentence').textContent='"'+s.w.join(' ')+'"';
  document.getElementById('spFb').textContent='';
  document.getElementById('spBar').style.width='0%';
  document.getElementById('spBar').style.background='#9C27B0';
  const rb=document.getElementById('spRecord');
  if(rb){ rb.textContent='🎤 Speak!'; rb.disabled=false; }
  speak(s.w.join(' '), 0.8);
}

function startSP(){
  // ... Chrome SpeechRecognition API
  // Scoring: word-level accuracy → max 30pts per sentence
  // bestPct = best match across 5 alternatives → pts = round(bestPct/100 * 30)
  // Total max = spSentList.length × 30 (typically 5×30 = 150pts)
  // curPage===7 guard in setTimeout before advancing
}

function endSP(){
  document.getElementById('spFinalScore').textContent=spScore+'/'+spSentList.length*30+' pts';
}
```

### SP page HTML (p7)

```html
<div class="page" id="p7">
  <div class="step-label">🎤 Speak Up!</div>
  <p class="step-sub">Read the sentence aloud — scored on accuracy!</p>
  <div>Sentence <span id="spNum">1</span>/<span id="spTotal">5</span> · ⭐ <span id="spSc">0</span> pts</div>
  <div id="spCard" style="border:2.5px solid #AB47BC;...">
    <div id="spSentence" style="font-size:18px;font-weight:900">—</div>
    <button onclick="spHear()">🔊 Hear</button>
    <button id="spRecord" onclick="startSP()">🎤 Speak!</button>
    <div id="spBar" style="height:12px;background:#9C27B0;width:0%"></div>
    <div id="spFb"></div>
  </div>
  <!-- Non-Chrome fallback -->
  <div id="spAlt" style="display:none">
    ⚠️ Voice needs Chrome
    <button onclick="spManual()">✅ I said it! (+10)</button>
  </div>
  <!-- Completion panel -->
  <div id="spDone" style="display:none">
    <div id="spFinalScore">0/150 pts</div>
    <button onclick="go(7);initSP()">Play Again 🔄</button>
  </div>
  <div class="navrow">
    <button onclick="go(0)">← Menu</button>
    <button onclick="showCompletion()">🏆 Finish!</button>
  </div>
</div>
```

---

## SB navrow — must point to SP (not showCompletion)

```html
<!-- p6 SB navrow — bottom navigation -->
<div class="navrow">
  <button onclick="go(0)">← Menu</button>
  <button onclick="go(7);initSP()">Speak Up! →</button>  <!-- ← NOT showCompletion -->
</div>
```

---

## Lock System (same as regular days)

```javascript
const LOCK_KEY = 'wla_d[N]';          // e.g., 'wla_d7', 'wla_d14'
const PREV_KEY = 'wla_d[N-1]';        // e.g., 'wla_d6', 'wla_d13'
// Admin bypass: localStorage.getItem('wla_admin')==='1' → skip lock
// Completion code: generateCode(N) → stored in LOCK_KEY
```

---

## Theme Colors by Week

| Week | Theme | Header Gradient | Primary | Accent | Card BG |
|------|-------|----------------|---------|--------|---------|
| 1 | 🌈 Rainbow (Animals) | `#E91E63→#9C27B0→#3F51B5` | `#E91E63` | `#CE93D8` | `#F3E5F5` |
| 2 | 🍽️ Food (Orange) | `#FF8F00→#F57F17` | `#E65100` | `#FFCC02` | `#FFF3E0` |
| 3 | 🏠 Home (Green) | `#2E7D32→#558B2F` | `#2E7D32` | `#A5D6A7` | `#E8F5E9` |
| 4 | 🏫 School (Blue) | `#1A237E→#283593` | `#1565C0` | `#9FA8DA` | `#E8EAF6` |

---

## How to Generate a New Review Day

1. **Get from user**: Day N (7/14/21/28/35…), Week W, Theme name, WORDS (36 words = 6 days × 6 words), SB_LIST (5 sentences)
2. **Determine theme**: N%28 → week number → colors from table above
3. **Set LOCK_KEY/PREV_KEY**: `wla_d[N]` / `wla_d[N-1]`
4. **Build all 8 pages**: p0–p7 with correct game IDs
5. **Wire all button orders**: `go(N);initXX()` — NOT `initXX();go(N)` (causes TTS bug!)
6. **Add curPage guards** to all setTimeout callbacks in LC, LP, SQ, SB, SP

---

## Quality Checklist

- [ ] WORDS array has 36 entries with `{e, day, icon}` (no Thai `t` field)
- [ ] SB_LIST has 5+ sentences `{w:[...]}`
- [ ] `go()` has `synth.cancel()` + `spListening=false` + dots `[0,1,2,3,4,5,6,7]`
- [ ] All button calls: `go(N);initXX()` order (not reversed)
- [ ] curPage guards in: checkLC(1), checkLP(2), checkSQ(3), sbCheck(6), SP callbacks(7)
- [ ] BP uses `id="bpArena"` (not `bpArea`) and oval balloon CSS
- [ ] SP uses `SB_LIST` (not WORDS), scoring = word accuracy × 30pts/sentence
- [ ] SB navrow points to `go(7);initSP()` (not showCompletion)
- [ ] `updateScore()` includes all 7 scores, pct `/7.75`, stars `≥550/≥375`
- [ ] `LOCK_KEY='wla_d[N]'` and `PREV_KEY='wla_d[N-1]'` correct
- [ ] SR_API alias defined: `const SR_API = window.SpeechRecognition||window.webkitSpeechRecognition`
- [ ] Copyright-free content — no licensed characters or plots
