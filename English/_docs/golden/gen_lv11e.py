# -*- coding: utf-8 -*-
# Level 11 · B2 · Finale (Day 329–330) — อ่านให้ลึกและตรวจสอบข้อมูล
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from golden_generator import build
OUT = '/sessions/wonderful-magical-bohr/mnt/English/Level11/'

def D(n, prev, title, emoji, nf, ne, game, grammar, words, story, ss, ds, tq, ta):
    return dict(n=n, prev=prev, level=11, cefr='B2', title=title, emoji=emoji, theme='Critical Reading',
                next_file=nf, next_emoji=ne, game=game, grammar=grammar, words=words, story=story,
                ss=ss, ds=ds, think_q=tq, think_a=ta)

W = [
D(329,328,'Reading Between the Lines','📖','Day330_ThreeHundredandThirty_B2.html','🎓','scramble',
  'Inferred meaning: implies rather than states / stops short of saying.',
  [('implication','นัยที่แฝงอยู่','/ˌɪmplɪˈkeɪʃn/','🫥'),('connotation','ความหมายแฝง','/ˌkɒnəˈteɪʃn/','🎨'),
   ('undertone','น้ำเสียงแฝง','/ˈʌndətəʊn/','🎚️'),('irony','การประชด','/ˈaɪərəni/','🙃'),
   ('understatement','การพูดน้อยกว่าความจริง','/ˌʌndəˈsteɪtmənt/','🤏'),('euphemism','การใช้คำอ้อม','/ˈjuːfəmɪzəm/','🎀'),
   ('rhetoric','วาทศิลป์','/ˈretərɪk/','🗯️'),('anecdote','เรื่องเล่าประกอบ','/ˈænɪkdəʊt/','📔'),
   ('credibility','ความน่าเชื่อถือ','/ˌkredəˈbɪləti/','🏅')],
  "The implication of a sentence is often larger than the sentence. Two words can share a meaning and have a very different connotation. There was a warning in the polite undertone of her reply. Irony says one thing and means the opposite, and not everyone hears it. Calling a storm unhelpful is a British understatement. A euphemism softens a hard fact and sometimes hides it. Rhetoric is not a lie; it is language arranged to persuade. One vivid anecdote can outweigh a hundred careful numbers in a reader's mind. Credibility is built slowly and spent in a single careless sentence.",
  ["The implication of a sentence is often larger than the sentence.",
   "Two words can share a meaning and have a very different connotation.",
   "Irony says one thing and means the opposite.",
   "Rhetoric is not a lie; it is language arranged to persuade.",
   "Credibility is built slowly and spent in a single careless sentence."],
  ["Two words can share a meaning and have a very different connotation.",
   "Rhetoric is not a lie; it is language arranged to persuade.",
   "Credibility is built slowly and spent in a single careless sentence."],
  "What is rhetoric?","It is language arranged to persuade, not a lie."),

D(330,329,'Three Hundred and Thirty','🎓','../dashboard.html','🏠','tiles',
  'Academic caution: the data suggest / this does not establish that.',
  [('citation','การอ้างอิงแหล่งที่มา','/saɪˈteɪʃn/','🔖'),('plagiarism','การลอกงานผู้อื่น','/ˈpleɪdʒərɪzəm/','🚫'),
   ('correlation','ความสัมพันธ์ร่วม','/ˌkɒrəˈleɪʃn/','📈'),('causation','ความเป็นเหตุเป็นผล','/kɔːˈzeɪʃn/','➡️'),
   ('methodology','ระเบียบวิธีวิจัย','/ˌmeθəˈdɒlədʒi/','🧪'),('peerreview','การตรวจโดยผู้รู้เท่ากัน','/ˈpɪərɪvjuː/','👓'),
   ('replicate','ทำซ้ำเพื่อยืนยันผล','/ˈreplɪkeɪt/','🔁'),('anomaly','สิ่งผิดปกติจากรูปแบบ','/əˈnɒməli/','❗'),
   ('synthesis','การสังเคราะห์ข้อมูล','/ˈsɪnθəsɪs/','🧩')],
  "A citation is a promise that the reader can check you. Plagiarism is not only unfair; it hides where an idea actually came from. Correlation means two things move together. Causation means one of them moves the other. Ask about the methodology before you argue about the conclusion. Peerreview is imperfect and still better than no review at all. A result nobody can replicate is a story, not a finding. One anomaly is noise. A repeated anomaly is a discovery waiting. Real understanding is a synthesis: many sources, one clear picture in your own words.",
  ["A citation is a promise that the reader can check you.",
   "Correlation means two things move together.",
   "Ask about the methodology before you argue about the conclusion.",
   "A result nobody can replicate is a story, not a finding.",
   "One anomaly is noise. A repeated anomaly is a discovery waiting."],
  ["A citation is a promise that the reader can check you.",
   "Ask about the methodology before you argue about the conclusion.",
   "A result nobody can replicate is a story, not a finding."],
  "What should you ask about before arguing about the conclusion?","Ask about the methodology."),
]
for d in W:
    out = build(d)
    fn = 'Day%d_%s_B2.html' % (d['n'], d['title'].replace(' ','').replace("'",''))
    open(OUT+fn,'w',encoding='utf-8').write(out)
    print('OK', fn, len(d['words']))
