# -*- coding: utf-8 -*-
# Level 10 · B1 · Finale (Day 299–300) — ปิด B1 เตรียมขึ้น B2
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from golden_generator import build
OUT = '/sessions/wonderful-magical-bohr/mnt/English/Level10/'

def D(n, prev, title, emoji, nf, ne, game, grammar, words, story, ss, ds, tq, ta):
    return dict(n=n, prev=prev, level=10, cefr='B1', title=title, emoji=emoji, theme='Milestone',
                next_file=nf, next_emoji=ne, game=game, grammar=grammar, words=words, story=story,
                ss=ss, ds=ds, think_q=tq, think_a=ta)

W = [
D(299,298,'The Whole Journey','🛤️','Day300_ThreeHundredDays_B1.html','🎓','scramble',
  'Present perfect continuous: You have been learning for three hundred days.',
  [('competence','ความสามารถที่ทำได้จริง','/ˈkɒmpɪtəns/','🎯'),('gist','ใจความสำคัญ','/dʒɪst/','🔍'),
   ('infer','อนุมานจากบริบท','/ɪnˈfɜː(r)/','🕵️'),('inference','การอนุมาน','/ˈɪnfərəns/','🧠'),
   ('summarise','สรุปความ','/ˈsʌməraɪz/','📝'),('deduce','สรุปจากเหตุผล','/dɪˈdjuːs/','🔗'),
   ('critique','วิจารณ์อย่างมีเหตุผล','/krɪˈtiːk/','⚖️'),('formality','ระดับความเป็นทางการ','/fɔːˈmæləti/','🎩')],
  "Competence is quieter than confidence and lasts longer. You can now catch the gist of a talk you have never heard. You infer the meaning of a new word without stopping. That single skill, inference, will carry you for years. Try to summarise a page in two sentences. From two facts you can often deduce the third. A fair critique names what worked first. Choose the right formality for the person in front of you.",
  ["Competence is quieter than confidence and lasts longer.",
   "You can now catch the gist of a talk you have never heard.",
   "You infer the meaning of a new word without stopping.",
   "Try to summarise a page in two sentences.",
   "A fair critique names what worked first."],
  ["Competence is quieter than confidence and lasts longer.",
   "Try to summarise a page in two sentences.",
   "A fair critique names what worked first."],
  "What does a fair critique name first?","It names what worked first."),

D(300,299,'Three Hundred Days','🎓','../dashboard.html','🏠','tiles',
  'Looking back and forward: this time last year / by this time next year.',
  [('proficient','ชำนาญ','/prəˈfɪʃnt/','🏅'),('idiomatic','เป็นสำนวนเจ้าของภาษา','/ˌɪdiəˈmætɪk/','🗨️'),
   ('colloquial','ภาษาพูดในชีวิตประจำวัน','/kəˈləʊkwiəl/','☕'),('outset','จุดเริ่มต้น','/ˈaʊtset/','🚪'),
   ('accomplishment','ความสำเร็จที่ทำได้','/əˈkʌmplɪʃmənt/','🪧'),('tenacity','ความไม่ยอมแพ้','/təˈnæsəti/','🔥'),
   ('steadfast','มั่นคงไม่ไหวเอน','/ˈstedfɑːst/','🔭'),('brink','ขอบของสิ่งใหม่','/brɪŋk/','➡️')],
  "Three hundred days ago you knew a few hundred words. You are proficient now in a way that felt impossible then. Idiomatic English is the next hill, and it is a friendly one. Colloquial speech is learned by listening, not by studying. You are standing at the outset of something, not a finish line. Day three hundred is an accomplishment worth stopping to notice. Your tenacity was not because it was easy. Stay steadfast and curious — you are on the brink of B2.",
  ["Three hundred days ago you knew a few hundred words.",
   "Idiomatic English is the next hill.",
   "Colloquial speech is learned by listening.",
   "You are standing at the outset of something, not a finish line.",
   "Stay steadfast and curious — you are on the brink of B2."],
  ["Idiomatic English is the next hill.",
   "You are standing at the outset of something, not a finish line.",
   "Stay steadfast and curious — you are on the brink of B2."],
  "Is day three hundred a finish line?","No, it is the outset of something new."),
]
for d in W:
    out = build(d)
    fn = 'Day%d_%s_B1.html' % (d['n'], d['title'].replace(' ','').replace("'",''))
    open(OUT+fn,'w',encoding='utf-8').write(out)
    print('OK', fn)
