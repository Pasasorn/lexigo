# -*- coding: utf-8 -*-
# Level 12 · B2 · Finale (Day 359–360) — มองภาพยาว + สรุป Level 12
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from golden_generator import build
OUT = '/sessions/wonderful-magical-bohr/mnt/English/Level12/'

def D(n, prev, title, emoji, nf, ne, game, grammar, words, story, ss, ds, tq, ta):
    return dict(n=n, prev=prev, level=12, cefr='B2', title=title, emoji=emoji, theme='The Long View',
                next_file=nf, next_emoji=ne, game=game, grammar=grammar, words=words, story=story,
                ss=ss, ds=ds, think_q=tq, think_a=ta)

W = [
D(359,358,'The Long View','🔭','Day360_ThreeHundredandSixty_B2.html','🎓','scramble',
  'Speculating about the past: had it not been for / might well have.',
  [('continuity','ความต่อเนื่อง','/ˌkɒntɪˈnjuːəti/','🧵'),('contingency','สิ่งที่อาจเกิดโดยบังเอิญ','/kənˈtɪndʒənsi/','🎲'),
   ('inevitability','ความหลีกเลี่ยงไม่ได้','/ɪnˌevɪtəˈbɪləti/','⛰️'),('hindsight','การมองย้อนหลัง','/ˈhaɪndsaɪt/','🪞'),
   ('counterfactual','สมมติว่าไม่เกิดขึ้น','/ˌkaʊntəˈfæktʃuəl/','❓'),('causality','ความเป็นเหตุเป็นผล','/kɔːˈzæləti/','⛓️'),
   ('turningpoint','จุดเปลี่ยน','/ˈtɜːnɪŋpɔɪnt/','🔀'),('upheaval','ความปั่นป่วนครั้งใหญ่','/ʌpˈhiːvl/','🌋'),
   ('gradualism','การเปลี่ยนแปลงทีละน้อย','/ˈɡrædʒuəlɪzəm/','🐌')],
  "Continuity is easy to miss because nothing about it makes news. A single contingency, one wet morning, has decided a battle. Inevitability is something we usually discover after the event. Hindsight makes every outcome look obvious and every warning look loud. A counterfactual question asks what would have happened otherwise. Causality is harder to prove in history than in a laboratory. A turningpoint is only visible once you know what followed it. Sudden upheaval gets the attention; quiet gradualism does most of the work.",
  ["Continuity is easy to miss because nothing about it makes news.",
   "A single contingency, one wet morning, has decided a battle.",
   "Hindsight makes every outcome look obvious.",
   "A turningpoint is only visible once you know what followed it.",
   "Sudden upheaval gets the attention; quiet gradualism does most of the work."],
  ["Hindsight makes every outcome look obvious.",
   "A turningpoint is only visible once you know what followed it.",
   "Continuity is easy to miss because nothing about it makes news."],
  "When is a turningpoint visible?","Only once you know what followed it."),

D(360,359,'Three Hundred and Sixty','🎓','../dashboard.html','🏠','tiles',
  'Reflective summary: what stands out is / looking back over the year.',
  [('consolidate','ทำให้มั่นคงเป็นปึกแผ่น','/kənˈsɒlɪdeɪt/','🧱'),('entrench','ฝังรากลึก','/ɪnˈtrentʃ/','🌲'),
   ('dismantle','รื้อถอนออก','/dɪsˈmæntl/','🔧'),('transition','ช่วงเปลี่ยนผ่าน','/trænˈzɪʃn/','🚪'),
   ('longevity','การคงอยู่ยาวนาน','/lɒnˈdʒevəti/','⏳'),('watershed','เหตุการณ์แบ่งยุค','/ˈwɔːtəʃed/','⛰️'),
   ('periodisation','การแบ่งยุคสมัย','/ˌpɪəriədaɪˈzeɪʃn/','📚'),('synthesise','สังเคราะห์รวมเป็นภาพเดียว','/ˈsɪnθəsaɪz/','🧩'),
   ('panorama','ภาพรวมกว้างไกล','/ˌpænəˈrɑːmə/','🔭')],
  "Three hundred and sixty days ago these sentences would have been impossible. Consolidate what you know before reaching for what you do not. A habit that is entrenched needs no motivation at all. It is far easier to entrench a system than to dismantle one. You are in a transition between understanding English and thinking in it. The longevity of a language in your head depends on using it, not storing it. Day three hundred and sixty is a watershed in this course. Periodisation is how historians cut a long story into chapters, and you have finished one. Synthesise what you have read this level: many topics, one clear panorama.",
  ["Consolidate what you know before reaching for what you do not.",
   "A habit that is entrenched needs no motivation at all.",
   "It is far easier to entrench a system than to dismantle one.",
   "You are in a transition between understanding English and thinking in it.",
   "Day three hundred and sixty is a watershed in this course."],
  ["Consolidate what you know before reaching for what you do not.",
   "A habit that is entrenched needs no motivation at all.",
   "Day three hundred and sixty is a watershed in this course."],
  "What should you do before reaching for what you do not know?","Consolidate what you know."),
]
for d in W:
    out = build(d)
    fn = 'Day%d_%s_B2.html' % (d['n'], d['title'].replace(' ','').replace("'",''))
    open(OUT+fn,'w',encoding='utf-8').write(out)
    print('OK', fn, len(d['words']))
