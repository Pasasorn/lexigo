# -*- coding: utf-8 -*-
# Level 14 · B2 · Finale (Day 419–420)
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from golden_generator import build
OUT = '/sessions/wonderful-magical-bohr/mnt/English/Level14/'

def D(n, prev, title, emoji, nf, ne, game, grammar, words, story, ss, ds, tq, ta):
    return dict(n=n, prev=prev, level=14, cefr='B2', title=title, emoji=emoji, theme='Thinking Well',
                next_file=nf, next_emoji=ne, game=game, grammar=grammar, words=words, story=story,
                ss=ss, ds=ds, think_q=tq, think_a=ta)

W = [
D(419,418,'The Habit of Thinking','🪄','Day420_FourHundredandTwenty_B2.html','🎓','scramble',
  'Updating a view: I used to think / on reflection / the evidence has moved me.',
  [('metacognition','การรู้เท่าทันความคิดตนเอง','/ˌmetəkɒɡˈnɪʃn/','🪞'),('overconfidence','ความมั่นใจเกินจริง','/ˌəʊvəˈkɒnfɪdəns/','🎈'),
   ('calibrated','ประเมินความมั่นใจได้แม่น','/ˈkælɪbreɪtɪd/','🎚️'),('steelman','สรุปฝ่ายตรงข้ามให้แข็งที่สุด','/ˈstiːlmæn/','🛡️'),
   ('openminded','เปิดรับความคิดใหม่','/ˌəʊpənˈmaɪndɪd/','🚪'),('falsifiable','พิสูจน์ว่าผิดได้','/ˈfɔːlsɪfaɪəbl/','🧪'),
   ('parsimony','การอธิบายอย่างเรียบง่ายที่สุด','/ˈpɑːsɪməni/','✂️'),('probabilistic','เชิงความน่าจะเป็น','/ˌprɒbəbɪˈlɪstɪk/','🎲'),
   ('provisional','เป็นข้อสรุปชั่วคราว','/prəˈvɪʒənl/','📝')],
  "Metacognition is thinking about how you are thinking, and it can be practised. Overconfidence is not the same as confidence; it is confidence without evidence. A calibrated thinker is right about how often they are right. To steelman an opponent is to state their case better than they did. Being openminded is not believing everything; it is being willing to be moved. A claim that is not falsifiable cannot be tested and should not be trusted. Parsimony prefers the simplest explanation that still fits the facts. Probabilistic thinking replaces certain and impossible with more likely and less likely. Every conclusion should be held as provisional, including this one.",
  ["Overconfidence is confidence without evidence.",
   "A calibrated thinker is right about how often they are right.",
   "To steelman an opponent is to state their case better than they did.",
   "Being openminded is being willing to be moved.",
   "Every conclusion should be held as provisional."],
  ["Overconfidence is confidence without evidence.",
   "To steelman an opponent is to state their case better than they did.",
   "Every conclusion should be held as provisional."],
  "What is overconfidence?","It is confidence without evidence."),

D(420,419,'Four Hundred and Twenty','🎓','../dashboard.html','🏠','tiles',
  'Reflective summary: what has changed most is / I no longer need to.',
  [('immersion','การจมอยู่กับภาษา','/ɪˈmɜːʃn/','🌊'),('spontaneity','ความเป็นธรรมชาติทันที','/ˌspɒntəˈneɪəti/','⚡'),
   ('precision','ความแม่นยำในการใช้คำ','/prɪˈsɪʒn/','🎯'),('register','ระดับภาษาที่เหมาะกับสถานการณ์','/ˈredʒɪstə(r)/','🎼'),
   ('nuanced','ละเอียดอ่อนแยกแยะได้','/ˈnjuːɑːnst/','🔎'),('unforced','เป็นไปเองไม่ฝืน','/ˌʌnˈfɔːst/','🪶'),
   ('versatile','ใช้ได้หลากหลายสถานการณ์','/ˈvɜːsətaɪl/','🧰'),('cumulative','สะสมทบไปเรื่อย','/ˈkjuːmjələtɪv/','📚'),
   ('upkeep','การดูแลรักษาให้คงอยู่','/ˈʌpkiːp/','🌱')],
  "Immersion did most of this quietly while you were paying attention to something else. Spontaneity arrives when you stop assembling sentences in advance. Precision is choosing between two words that a beginner thinks are the same. Register is knowing that an email to a friend is not an email to a stranger. A nuanced reader hears the difference between disagree and object. English will feel unforced on some days and not on others, and both are normal. A versatile speaker can be plain, formal, funny or exact, on purpose. Everything here has been cumulative: four hundred and twenty days, one habit. Upkeep of a language means using it often enough to keep it.",
  ["Spontaneity arrives when you stop assembling sentences in advance.",
   "Precision is choosing between two words a beginner thinks are the same.",
   "Register is knowing that an email to a friend is not an email to a stranger.",
   "English will feel unforced on some days and not on others.",
   "Upkeep of a language means using it often enough to keep it."],
  ["Spontaneity arrives when you stop assembling sentences in advance.",
   "Register is knowing that an email to a friend is not an email to a stranger.",
   "Upkeep of a language means using it often enough to keep it."],
  "When does spontaneity arrive?","When you stop assembling sentences in advance."),
]
for d in W:
    out = build(d)
    fn = 'Day%d_%s_B2.html' % (d['n'], d['title'].replace(' ','').replace("'",''))
    open(OUT+fn,'w',encoding='utf-8').write(out)
    print('OK', fn, len(d['words']))
