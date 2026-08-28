# -*- coding: utf-8 -*-
# Level 9 · B1 · Finale (Day 269–270)
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from golden_generator import build
OUT = '/sessions/wonderful-magical-bohr/mnt/English/Level9/'

def D(n, prev, title, emoji, nf, ne, game, grammar, words, story, ss, ds, tq, ta):
    return dict(n=n, prev=prev, level=9, cefr='B1', title=title, emoji=emoji, theme='Learning',
                next_file=nf, next_emoji=ne, game=game, grammar=grammar, words=words, story=story,
                ss=ss, ds=ds, think_q=tq, think_a=ta)

W = [
D(269,268,'How I Learn Best','🧠','Day270_ReadyfortheNextLevel_B1.html','🚀','scramble',
  'Talking about method: by + -ing (I remember words by using them).',
  [('mnemonic','เทคนิคช่วยจำ','/nɪˈmɒnɪk/','🪄'),('glossary','อภิธานศัพท์','/ˈɡlɒsəri/','📔'),
   ('syllable','พยางค์','/ˈsɪləbl/','🔤'),('thesaurus','พจนานุกรมคำเหมือน','/θɪˈsɔːrəs/','📚'),
   ('retention','การจดจำได้นาน','/rɪˈtenʃn/','🧲'),('consistency','ความสม่ำเสมอ','/kənˈsɪstənsi/','📅'),
   ('drill','แบบฝึกซ้ำ','/drɪl/','🔁'),('shadowing','พูดตามทันที','/ˈʃædəʊɪŋ/','🗣️')],
  "A mnemonic works because it gives the word a hook. Build your own glossary as you read. Clap each syllable and the long word becomes easy. A thesaurus shows you five ways to say one thing. Retention comes from meeting a word again next week. Consistency beats a long weekend of study. A short daily drill is enough. Shadowing a speaker trains your mouth, not only your ear.",
  ["A mnemonic gives the word a hook.",
   "Build your own glossary as you read.",
   "Clap each syllable and the long word becomes easy.",
   "Consistency beats a long weekend of study.",
   "A short daily drill is enough."],
  ["Build your own glossary as you read.",
   "Consistency beats a long weekend of study.",
   "A short daily drill is enough."],
  "What does consistency beat?","It beats a long weekend of study."),

D(270,269,'Ready for the Next Level','🚀','../dashboard.html','🏠','tiles',
  'Looking ahead: by this time next year, I will have learned...',
  [('pronunciation','การออกเสียง','/prəˌnʌnsiˈeɪʃn/','👄'),('intonation','ทำนองเสียง','/ˌɪntəˈneɪʃn/','🎵'),
   ('hesitate','ลังเล','/ˈhezɪteɪt/','⏸️'),('immerse','ดำดิ่งอยู่กับภาษา','/ɪˈmɜːs/','🌊'),
   ('subtitle','คำบรรยายใต้ภาพ','/ˈsʌbtaɪtl/','🎬'),('collocation','คำที่มักใช้คู่กัน','/ˌkɒləˈkeɪʃn/','🔗'),
   ('dedication','ความทุ่มเท','/ˌdedɪˈkeɪʃn/','🔥'),('lifelong','ตลอดชีวิต','/ˈlaɪflɒŋ/','♾️')],
  "Your pronunciation has changed more than you notice. Intonation carries meaning that words alone cannot. Do not hesitate for the perfect sentence. Immerse yourself for twenty minutes a day. Watch with an English subtitle, then with none. Learn a collocation, not a lonely word. Dedication brought you here across two hundred and seventy days. A language is a lifelong friend, and yours has only started talking.",
  ["Your pronunciation has changed more than you notice.",
   "Do not hesitate for the perfect sentence.",
   "Immerse yourself for twenty minutes a day.",
   "Learn a collocation, not a lonely word.",
   "A language is a lifelong friend."],
  ["Do not hesitate for the perfect sentence.",
   "Learn a collocation, not a lonely word.",
   "A language is a lifelong friend."],
  "How long should you immerse yourself each day?","Twenty minutes a day."),
]
for d in W:
    out = build(d)
    fn = 'Day%d_%s_B1.html' % (d['n'], d['title'].replace(' ','').replace("'",''))
    open(OUT+fn,'w',encoding='utf-8').write(out)
    print('OK', fn)
