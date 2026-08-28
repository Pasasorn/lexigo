# -*- coding: utf-8 -*-
# Level 13 · B2 · Finale (Day 389–390)
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from golden_generator import build
OUT = '/sessions/wonderful-magical-bohr/mnt/English/Level13/'

def D(n, prev, title, emoji, nf, ne, game, grammar, words, story, ss, ds, tq, ta):
    return dict(n=n, prev=prev, level=13, cefr='B2', title=title, emoji=emoji, theme='Putting It Together',
                next_file=nf, next_emoji=ne, game=game, grammar=grammar, words=words, story=story,
                ss=ss, ds=ds, think_q=tq, think_a=ta)

W = [
D(389,388,'Putting It Together','🧠','Day390_ThreeHundredandNinety_B2.html','🎓','scramble',
  'Connecting fields: much as in / the same principle appears in.',
  [('interdisciplinary','ข้ามศาสตร์','/ˌɪntədɪsəˈplɪnəri/','🔀'),('analogy','การเปรียบเทียบอุปมา','/əˈnælədʒi/','🪞'),
   ('abstraction','การคิดเชิงนามธรรม','/æbˈstrækʃn/','☁️'),('generalise','สรุปเป็นหลักทั่วไป','/ˈdʒenrəlaɪz/','🌐'),
   ('specialise','เชี่ยวชาญเฉพาะทาง','/ˈspeʃəlaɪz/','🎯'),('transferable','นำไปใช้ข้ามงานได้','/trænsˈfɜːrəbl/','🧳'),
   ('expertise','ความเชี่ยวชาญ','/ˌekspɜːˈtiːz/','🏅'),('novice','ผู้เริ่มต้น','/ˈnɒvɪs/','🐣'),
   ('leverage','ใช้สิ่งที่มีให้เกิดผลมาก','/ˈliːvərɪdʒ/','🪜')],
  "The most interesting problems are interdisciplinary; nature never divided itself into school subjects. A good analogy carries an idea from a field you know into one you do not. Abstraction is how one solution comes to fit a thousand cases. To generalise too early is to be confidently wrong. To specialise too early is to be narrow. A transferable skill is worth more than a fact. Expertise is knowing which detail matters and which does not. A novice sees only the surface features of a problem. Leverage means using a small effort where it does the most work.",
  ["The most interesting problems are interdisciplinary.",
   "A good analogy carries an idea from a field you know into one you do not.",
   "To generalise too early is to be confidently wrong.",
   "Expertise is knowing which detail matters and which does not.",
   "A novice sees only the surface features of a problem."],
  ["To generalise too early is to be confidently wrong.",
   "Expertise is knowing which detail matters and which does not.",
   "A novice sees only the surface features of a problem."],
  "What is expertise?","Knowing which detail matters and which does not."),

D(390,389,'Three Hundred and Ninety','🎓','../dashboard.html','🏠','tiles',
  'Progress over time: has been steadily / is no longer / has come to.',
  [('compounding','การทบต้นสะสมผล','/kəmˈpaʊndɪŋ/','📈'),('incremental','ทีละเล็กละน้อย','/ˌɪŋkrəˈmentl/','🐢'),
   ('lull','ช่วงชะงักเงียบ','/lʌl/','🏔️'),('milepost','หมุดบอกระยะความก้าวหน้า','/ˈmaɪlpəʊst/','🚪'),
   ('scaffolding','โครงช่วยเรียนรู้','/ˈskæfəʊldɪŋ/','🪜'),('automaticity','ความคล่องแบบอัตโนมัติ','/ˌɔːtəməˈtɪsəti/','⚡'),
   ('consolidation','การรวบยอดความรู้','/kənˌsɒlɪˈdeɪʃn/','🧱'),('capability','ขีดความสามารถที่ทำได้จริง','/ˌkeɪpəˈbɪləti/','🏆'),
   ('doggedness','ความไม่ยอมเลิกกลางคัน','/ˈdɒɡɪdnəs/','🔥')],
  "Compounding is why ten words a day becomes three thousand and feels like nothing. Incremental progress is invisible on any single day and undeniable across a year. A lull is not a stop; it is the brain reorganising quietly. Passing a milepost in a language feels sudden and was not. Scaffolding is help you are meant to outgrow. Automaticity is the moment you stop translating in your head. Consolidation matters more at this stage than adding anything new. Capability in a language is not a certificate; it is what you can do on a tired day. Doggedness brought you three hundred and ninety days, and it is the only rare ingredient.",
  ["Compounding is why ten words a day becomes three thousand.",
   "Incremental progress is invisible on any single day.",
   "A lull is not a stop; it is the brain reorganising quietly.",
   "Scaffolding is help you are meant to outgrow.",
   "Automaticity is the moment you stop translating in your head."],
  ["A lull is not a stop; it is the brain reorganising quietly.",
   "Scaffolding is help you are meant to outgrow.",
   "Automaticity is the moment you stop translating in your head."],
  "What is a lull?","It is the brain reorganising quietly, not a stop."),
]
for d in W:
    out = build(d)
    fn = 'Day%d_%s_B2.html' % (d['n'], d['title'].replace(' ','').replace("'",''))
    open(OUT+fn,'w',encoding='utf-8').write(out)
    print('OK', fn, len(d['words']))
