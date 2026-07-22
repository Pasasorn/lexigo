# -*- coding: utf-8 -*-
import re, glob, os
os.chdir('/sessions/wonderful-magical-bohr/mnt/lexigo--English')

TILES_HTML='''  <div class="step-label">Step 5 · Fill the Blank! ✏️</div>
  <p class="step-sub">See the hint → tap letters to complete the word!</p>
  <div style="text-align:center;font-size:14px;font-weight:800;color:#1565C0;margin-bottom:8px">Q <span id="g5q">1</span>/<span id="g5tot">6</span> · ⭐ <span id="g5sc">0</span></div>
  <div id="g5card" style="background:#fff;border-radius:18px;padding:18px;border:2.5px solid #90CAF9;text-align:center">
    <div id="g5hint" style="font-size:44px;margin-bottom:4px"></div>
    <div id="g5thai" style="font-size:16px;color:#546E7A;font-weight:700;margin-bottom:12px"></div>
    <div id="g5blanks" style="font-size:28px;font-weight:900;letter-spacing:6px;color:#1565C0;margin-bottom:14px;min-height:42px"></div>
    <div id="g5tiles" style="display:flex;flex-wrap:wrap;justify-content:center;gap:8px"></div>
    <div id="g5feedback" style="min-height:28px;margin-top:10px;font-size:18px;font-weight:900"></div>
  </div>
  <div id="g5done" style="display:none;text-align:center;padding:16px;background:#E3F2FD;border-radius:16px;border:2px solid #90CAF9">
    <div style="font-size:30px">✏️</div><div style="font-size:18px;font-weight:900;color:#1565C0">Spelling Star! \U0001f31f</div>
    <div style="font-size:24px;font-weight:900;margin:6px 0" id="g5result">0 pts</div>
    <button class="btn btn-p" onclick="buildG()">Play Again \U0001f504</button>
  </div>
'''
TILES_JS='''let g5deck=[],g5idx=0,g5score=0,g5blanks=[],g5answer='',g5filled=[];
function buildG(){g5idx=0;g5score=0;g5deck=[...WORDS].sort(()=>Math.random()-.5);document.getElementById('g5tot').textContent=g5deck.length;document.getElementById('g5done').style.display='none';document.getElementById('g5card').style.display='block';g5render();}
function g5render(){if(g5idx>=g5deck.length){g5end();return;}const w=g5deck[g5idx];g5answer=w.e.toLowerCase();document.getElementById('g5q').textContent=g5idx+1;document.getElementById('g5sc').textContent=g5score;document.getElementById('g5hint').textContent=w.em||'\U0001f4dd';document.getElementById('g5thai').textContent=w.t;document.getElementById('g5feedback').textContent='';const len=g5answer.length;const nb=len<=3?1:len<=5?2:3;const pos=[];while(pos.length<nb){const p=Math.floor(Math.random()*len);if(!pos.includes(p))pos.push(p);}pos.sort((a,b)=>a-b);g5blanks=pos;g5filled=new Array(len).fill(null);g5upd();const miss=pos.map(p=>g5answer[p]);const pool='abcdefghijklmnoprstuw'.split('').filter(c=>!miss.includes(c));pool.sort(()=>Math.random()-.5);const opts=[...miss,...pool.slice(0,4)].sort(()=>Math.random()-.5);const tiles=document.getElementById('g5tiles');tiles.innerHTML='';opts.forEach(c=>{const b=document.createElement('button');b.textContent=c.toUpperCase();b.style.cssText='width:48px;height:48px;border-radius:12px;border:2.5px solid #90CAF9;background:#E3F2FD;font-size:22px;font-weight:900;cursor:pointer;color:#1565C0';b.onclick=()=>g5tap(c,b);tiles.appendChild(b);});}
function g5upd(){document.getElementById('g5blanks').innerHTML=g5answer.split('').map((c,i)=>!g5blanks.includes(i)?'<span style="color:#1565C0">'+c.toUpperCase()+'</span>':g5filled[i]?'<span style="color:#388E3C;border-bottom:3px solid #388E3C">'+g5filled[i].toUpperCase()+'</span>':'<span style="color:#bbb">_</span>').join('<span style="margin:0 3px"> </span>');}
function g5tap(c,btn){const nb=g5blanks.find(p=>!g5filled[p]);if(nb===undefined)return;if(g5answer[nb]===c){g5filled[nb]=c;btn.style.opacity='0.35';btn.onclick=null;g5upd();if(g5blanks.every(p=>g5filled[p])){g5score+=5;g5idx++;document.getElementById('g5feedback').textContent='✅ Great!';document.getElementById('g5sc').textContent=g5score;updScore(g5idx,g5deck.length);setTimeout(g5render,900);}}else{btn.style.background='#FFEBEE';btn.style.borderColor='#EF9A9A';document.getElementById('g5feedback').textContent='❌ Try again!';setTimeout(()=>{btn.style.background='#E3F2FD';btn.style.borderColor='#90CAF9';document.getElementById('g5feedback').textContent='';},700);}}
function g5end(){document.getElementById('g5card').style.display='none';document.getElementById('g5done').style.display='block';document.getElementById('g5result').textContent=g5score+' pts';updScore(g5deck.length,g5deck.length);}'''

SCRAM_HTML='''  <div class="step-label">Step 5 · Word Scramble! \U0001f500</div>
  <p class="step-sub">Tap letters in the right order to spell the word!</p>
  <div style="text-align:center;font-size:14px;font-weight:800;color:#1565C0;margin-bottom:8px">Q <span id="g5q">1</span>/<span id="g5tot">6</span> · ⭐ <span id="g5sc">0</span></div>
  <div id="g5card" style="background:#fff;border-radius:18px;padding:18px;border:2.5px solid #90CAF9;text-align:center">
    <div id="g5hint" style="font-size:44px;margin-bottom:4px"></div>
    <div id="g5thai" style="font-size:16px;color:#546E7A;font-weight:700;margin-bottom:10px"></div>
    <div id="g5answer" style="min-height:46px;background:#F5F5F5;border-radius:12px;padding:8px;font-size:24px;font-weight:900;letter-spacing:4px;color:#1565C0;margin-bottom:10px;display:flex;justify-content:center;align-items:center;gap:4px;flex-wrap:wrap"></div>
    <div id="g5tiles" style="display:flex;flex-wrap:wrap;justify-content:center;gap:8px"></div>
    <div id="g5feedback" style="min-height:28px;margin-top:8px;font-size:18px;font-weight:900"></div>
    <button onclick="g5clr()" style="margin-top:8px;padding:6px 18px;border-radius:10px;border:2px solid #90CAF9;background:#fff;color:#1565C0;font-weight:800;cursor:pointer;font-size:14px">Clear ↩</button>
  </div>
  <div id="g5done" style="display:none;text-align:center;padding:16px;background:#E3F2FD;border-radius:16px;border:2px solid #90CAF9">
    <div style="font-size:30px">\U0001f500</div><div style="font-size:18px;font-weight:900;color:#1565C0">Scramble Master! \U0001f389</div>
    <div style="font-size:24px;font-weight:900;margin:6px 0" id="g5result">0 pts</div>
    <button class="btn btn-p" onclick="buildG()">Play Again \U0001f504</button>
  </div>
'''
SCRAM_JS='''let g5deck=[],g5idx=0,g5score=0,g5typed=[],g5scr=[];
function buildG(){g5idx=0;g5score=0;g5deck=[...WORDS].sort(()=>Math.random()-.5);document.getElementById('g5tot').textContent=g5deck.length;document.getElementById('g5done').style.display='none';document.getElementById('g5card').style.display='block';g5render();}
function g5sc(w){const a=w.split('');let r;do{r=[...a].sort(()=>Math.random()-.5);}while(r.join('')===w&&w.length>1);return r;}
function g5render(){if(g5idx>=g5deck.length){g5end();return;}const w=g5deck[g5idx];g5typed=[];g5scr=g5sc(w.e.toLowerCase());document.getElementById('g5q').textContent=g5idx+1;document.getElementById('g5sc').textContent=g5score;document.getElementById('g5hint').textContent=w.em||'\U0001f4dd';document.getElementById('g5thai').textContent=w.t;document.getElementById('g5answer').innerHTML='<span style="color:#aaa;font-size:15px">Tap letters ↓</span>';document.getElementById('g5feedback').textContent='';const tiles=document.getElementById('g5tiles');tiles.innerHTML='';g5scr.forEach((c,i)=>{const b=document.createElement('button');b.id='t5_'+i;b.textContent=c.toUpperCase();b.style.cssText='width:48px;height:48px;border-radius:12px;border:2.5px solid #90CAF9;background:#E3F2FD;font-size:22px;font-weight:900;cursor:pointer;color:#1565C0';b.onclick=()=>g5tap(c,b);tiles.appendChild(b);});}
function g5ua(){const box=document.getElementById('g5answer');if(!g5typed.length){box.innerHTML='<span style="color:#aaa;font-size:15px">Tap letters ↓</span>';return;}box.innerHTML=g5typed.map(t=>'<span style="background:#fff;border:2px solid #42A5F5;border-radius:8px;padding:2px 8px">'+t.c.toUpperCase()+'</span>').join('');}
function g5tap(c,btn){if(btn.disabled)return;btn.disabled=true;btn.style.opacity='0.35';g5typed.push({c});g5ua();const ans=g5deck[g5idx].e.toLowerCase();if(g5typed.length===ans.length){const att=g5typed.map(t=>t.c).join('');if(att===ans){g5score+=5;document.getElementById('g5feedback').textContent='✅ Correct!';document.getElementById('g5sc').textContent=g5score;g5idx++;updScore(g5idx,g5deck.length);setTimeout(g5render,900);}else{document.getElementById('g5feedback').textContent='❌ Try again!';setTimeout(g5clr,700);}}}
function g5clr(){g5typed=[];g5ua();document.getElementById('g5feedback').textContent='';document.querySelectorAll('[id^=t5_]').forEach(b=>{b.disabled=false;b.style.opacity='1';});}
function g5end(){document.getElementById('g5card').style.display='none';document.getElementById('g5done').style.display='block';document.getElementById('g5result').textContent=g5score+' pts';updScore(g5deck.length,g5deck.length);}'''

MEM_HTML='''  <div class="step-label">Step 5 · Memory Match! \U0001f9e0</div>
  <p class="step-sub">Flip cards → match each word with its picture!</p>
  <div style="text-align:center;font-size:14px;font-weight:800;color:#1565C0;margin-bottom:8px">Pairs <span id="g5pairs">0</span>/6 · Tries <span id="g5tries">0</span></div>
  <div id="g5grid" style="display:grid;grid-template-columns:repeat(4,1fr);gap:8px"></div>
  <div id="g5done" style="display:none;text-align:center;padding:16px;background:#E3F2FD;border-radius:16px;border:2px solid #90CAF9;margin-top:10px">
    <div style="font-size:30px">\U0001f9e0</div><div style="font-size:18px;font-weight:900;color:#1565C0">Memory Master! \U0001f389</div>
    <div style="font-size:24px;font-weight:900;margin:6px 0" id="g5result">0</div>
    <button class="btn btn-p" onclick="buildG()">Play Again \U0001f504</button>
  </div>
'''
MEM_JS='''let g5cards=[],g5flip=[],g5pairs=0,g5tries=0,g5lock=false;
function buildG(){g5pairs=0;g5tries=0;g5flip=[];g5lock=false;document.getElementById('g5done').style.display='none';const deck=[];WORDS.forEach((w,i)=>{deck.push({id:i,label:w.e});deck.push({id:i,label:w.em});});g5cards=deck.sort(()=>Math.random()-.5);document.getElementById('g5pairs').textContent=0;document.getElementById('g5tries').textContent=0;const g=document.getElementById('g5grid');g.innerHTML='';g5cards.forEach((c,idx)=>{const b=document.createElement('button');b.id='mc'+idx;b.style.cssText='aspect-ratio:1;border-radius:12px;border:2.5px solid #90CAF9;background:#42A5F5;font-size:16px;cursor:pointer;color:#fff;font-weight:900;padding:2px;word-break:break-word';b.textContent='?';b.onclick=()=>g5tap(idx);g.appendChild(b);});}
function g5tap(i){if(g5lock)return;const c=g5cards[i],b=document.getElementById('mc'+i);if(b.dataset.done||g5flip.find(f=>f.i===i))return;b.textContent=c.label;b.style.background='#fff';b.style.color='#1565C0';g5flip.push({i,c});if(g5flip.length===2){g5tries++;document.getElementById('g5tries').textContent=g5tries;g5lock=true;const a=g5flip[0],d=g5flip[1];if(a.c.id===d.c.id){setTimeout(()=>{['mc'+a.i,'mc'+d.i].forEach(id=>{const e=document.getElementById(id);e.style.background='#E8F5E9';e.style.borderColor='#7CB342';e.dataset.done=1;});g5pairs++;document.getElementById('g5pairs').textContent=g5pairs;updScore(g5pairs,6);g5flip=[];g5lock=false;if(g5pairs===6)g5end();},450);}else{setTimeout(()=>{['mc'+a.i,'mc'+d.i].forEach(id=>{const e=document.getElementById(id);e.textContent='?';e.style.background='#42A5F5';e.style.color='#fff';});g5flip=[];g5lock=false;},850);}}}
function g5end(){document.getElementById('g5done').style.display='block';document.getElementById('g5result').textContent=g5tries+' tries';updScore(6,6);}'''

VOW_HTML='''  <div class="step-label">Step 5 · Missing Vowels! \U0001f170️</div>
  <p class="step-sub">Tap the correct vowels (a e i o u) to complete the word!</p>
  <div style="text-align:center;font-size:14px;font-weight:800;color:#1565C0;margin-bottom:8px">Q <span id="g5q">1</span>/<span id="g5tot">6</span> · ⭐ <span id="g5sc">0</span></div>
  <div id="g5card" style="background:#fff;border-radius:18px;padding:18px;border:2.5px solid #90CAF9;text-align:center">
    <div id="g5hint" style="font-size:44px;margin-bottom:4px"></div>
    <div id="g5thai" style="font-size:16px;color:#546E7A;font-weight:700;margin-bottom:12px"></div>
    <div id="g5blanks" style="font-size:28px;font-weight:900;letter-spacing:6px;color:#1565C0;margin-bottom:14px;min-height:42px"></div>
    <div id="g5tiles" style="display:flex;flex-wrap:wrap;justify-content:center;gap:8px"></div>
    <div id="g5feedback" style="min-height:28px;margin-top:10px;font-size:18px;font-weight:900"></div>
  </div>
  <div id="g5done" style="display:none;text-align:center;padding:16px;background:#E3F2FD;border-radius:16px;border:2px solid #90CAF9">
    <div style="font-size:30px">\U0001f170️</div><div style="font-size:18px;font-weight:900;color:#1565C0">Vowel Hero! \U0001f31f</div>
    <div style="font-size:24px;font-weight:900;margin:6px 0" id="g5result">0 pts</div>
    <button class="btn btn-p" onclick="buildG()">Play Again \U0001f504</button>
  </div>
'''
VOW_JS='''let g5deck=[],g5idx=0,g5score=0,g5ans='',g5pos=[],g5fill=[];
function buildG(){g5idx=0;g5score=0;g5deck=[...WORDS].sort(()=>Math.random()-.5);document.getElementById('g5tot').textContent=g5deck.length;document.getElementById('g5done').style.display='none';document.getElementById('g5card').style.display='block';g5render();}
function g5render(){if(g5idx>=g5deck.length){g5end();return;}const w=g5deck[g5idx];g5ans=w.e.toLowerCase();document.getElementById('g5q').textContent=g5idx+1;document.getElementById('g5sc').textContent=g5score;document.getElementById('g5hint').textContent=w.em||'\U0001f4dd';document.getElementById('g5thai').textContent=w.t;document.getElementById('g5feedback').textContent='';g5pos=[];for(let i=0;i<g5ans.length;i++)if('aeiou'.includes(g5ans[i]))g5pos.push(i);if(!g5pos.length)g5pos.push(0);g5fill=new Array(g5ans.length).fill(null);g5upd();const tiles=document.getElementById('g5tiles');tiles.innerHTML='';'aeiou'.split('').forEach(c=>{const b=document.createElement('button');b.textContent=c.toUpperCase();b.style.cssText='width:50px;height:50px;border-radius:12px;border:2.5px solid #90CAF9;background:#E3F2FD;font-size:22px;font-weight:900;cursor:pointer;color:#1565C0';b.onclick=()=>g5tap(c,b);tiles.appendChild(b);});}
function g5upd(){document.getElementById('g5blanks').innerHTML=g5ans.split('').map((c,i)=>!g5pos.includes(i)?'<span style="color:#1565C0">'+c.toUpperCase()+'</span>':g5fill[i]?'<span style="color:#388E3C;border-bottom:3px solid #388E3C">'+g5fill[i].toUpperCase()+'</span>':'<span style="color:#bbb">_</span>').join('<span style="margin:0 3px"> </span>');}
function g5tap(c,btn){const nb=g5pos.find(p=>!g5fill[p]);if(nb===undefined)return;if(g5ans[nb]===c){g5fill[nb]=c;g5upd();if(g5pos.every(p=>g5fill[p])){g5score+=5;g5idx++;document.getElementById('g5feedback').textContent='✅ Great!';document.getElementById('g5sc').textContent=g5score;updScore(g5idx,g5deck.length);setTimeout(g5render,900);}}else{btn.style.background='#FFEBEE';btn.style.borderColor='#EF9A9A';document.getElementById('g5feedback').textContent='❌ Try again!';setTimeout(()=>{btn.style.background='#E3F2FD';btn.style.borderColor='#90CAF9';document.getElementById('g5feedback').textContent='';},600);}}
function g5end(){document.getElementById('g5card').style.display='none';document.getElementById('g5done').style.display='block';document.getElementById('g5result').textContent=g5score+' pts';updScore(g5deck.length,g5deck.length);}'''

WS_HTML='''  <div class="step-label">Step 5 · Word Search! \U0001f50d</div>
  <p class="step-sub">Tap the first and last letter of each word to find it!</p>
  <div style="text-align:center;font-size:14px;font-weight:800;color:#1565C0;margin-bottom:8px">Found <span id="g5found">0</span>/6</div>
  <div id="g5grid" style="display:grid;gap:3px;justify-content:center;margin-bottom:10px"></div>
  <div id="g5words" style="display:flex;flex-wrap:wrap;gap:6px;justify-content:center"></div>
  <div id="g5done" style="display:none;text-align:center;padding:16px;background:#E3F2FD;border-radius:16px;border:2px solid #90CAF9;margin-top:10px">
    <div style="font-size:30px">\U0001f50d</div><div style="font-size:18px;font-weight:900;color:#1565C0">Word Finder! \U0001f389</div>
    <div style="font-size:24px;font-weight:900;margin:6px 0" id="g5result">6/6</div>
    <button class="btn btn-p" onclick="buildG()">Play Again \U0001f504</button>
  </div>
'''
WS_JS='''let g5N=8,g5g=[],g5place=[],g5found=0,g5sel=null;
function buildG(){g5found=0;g5sel=null;document.getElementById('g5done').style.display='none';document.getElementById('g5found').textContent=0;const words=WORDS.map(w=>w.e.toUpperCase().replace(/[^A-Z]/g,'')).filter(w=>w.length<=g5N).slice(0,6);let ok=false,tr=0;while(!ok&&tr<40){tr++;g5g=Array.from({length:g5N},()=>Array(g5N).fill(''));g5place=[];ok=true;for(const w of words){let placed=false;for(let a=0;a<30&&!placed;a++){const dir=Math.floor(Math.random()*2),r=Math.floor(Math.random()*g5N),c=Math.floor(Math.random()*g5N),dr=dir===0?0:1,dc=dir===0?1:0;if(r+dr*(w.length-1)>=g5N||c+dc*(w.length-1)>=g5N)continue;let fit=true;for(let k=0;k<w.length;k++){const cell=g5g[r+dr*k][c+dc*k];if(cell&&cell!==w[k]){fit=false;break;}}if(!fit)continue;for(let k=0;k<w.length;k++)g5g[r+dr*k][c+dc*k]=w[k];g5place.push({w,cells:Array.from({length:w.length},(_,k)=>[r+dr*k,c+dc*k]),found:false});placed=true;}if(!placed){ok=false;break;}}}for(let r=0;r<g5N;r++)for(let c=0;c<g5N;c++)if(!g5g[r][c])g5g[r][c]='ABCDEFGHIJKLMNOPRSTUW'[Math.floor(Math.random()*21)];const g=document.getElementById('g5grid');g.style.gridTemplateColumns='repeat('+g5N+',1fr)';g.innerHTML='';for(let r=0;r<g5N;r++)for(let c=0;c<g5N;c++){const b=document.createElement('button');b.id='ws'+r+'_'+c;b.textContent=g5g[r][c];b.style.cssText='width:34px;height:34px;border-radius:7px;border:2px solid #BBDEFB;background:#fff;font-size:15px;font-weight:900;cursor:pointer;color:#1565C0;padding:0';b.onclick=()=>g5cell(r,c);g.appendChild(b);}const wl=document.getElementById('g5words');wl.innerHTML='';g5place.forEach((p,i)=>{const s=document.createElement('span');s.id='wl'+i;s.textContent=p.w;s.style.cssText='background:#E3F2FD;border:1.5px solid #90CAF9;border-radius:8px;padding:4px 10px;font-size:13px;font-weight:800;color:#1565C0';wl.appendChild(s);});}
function g5cell(r,c){const b=document.getElementById('ws'+r+'_'+c);if(!g5sel){g5sel=[r,c];b.style.background='#FFF59D';return;}const r0=g5sel[0],c0=g5sel[1];document.getElementById('ws'+r0+'_'+c0).style.background='#fff';g5sel=null;for(let i=0;i<g5place.length;i++){const p=g5place[i];if(p.found)continue;const f=p.cells[0],l=p.cells[p.cells.length-1];if((f[0]===r0&&f[1]===c0&&l[0]===r&&l[1]===c)||(f[0]===r&&f[1]===c&&l[0]===r0&&l[1]===c0)){p.found=true;g5found++;document.getElementById('g5found').textContent=g5found;document.getElementById('wl'+i).style.cssText='background:#C8E6C9;border:1.5px solid #7CB342;border-radius:8px;padding:4px 10px;font-size:13px;font-weight:800;color:#2E7D32;text-decoration:line-through';p.cells.forEach(x=>{document.getElementById('ws'+x[0]+'_'+x[1]).style.background='#C8E6C9';});updScore(g5found,6);if(g5found>=g5place.length)g5end();return;}}}
function g5end(){document.getElementById('g5done').style.display='block';document.getElementById('g5result').textContent=g5found+'/'+g5place.length;updScore(6,6);}'''

GAMES={'tiles':(TILES_HTML,TILES_JS),'scramble':(SCRAM_HTML,SCRAM_JS),'memory':(MEM_HTML,MEM_JS),'wordsearch':(WS_HTML,WS_JS),'vowels':(VOW_HTML,VOW_JS)}
