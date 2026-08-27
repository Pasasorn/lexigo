# -*- coding: utf-8 -*-
# Level 5 · Week 22 — Health & Safety (Day 128–134) · A2
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from golden_generator import build
OUT = '/sessions/wonderful-magical-bohr/mnt/English/Level5/'

def D(n, prev, title, emoji, nf, ne, game, grammar, words, story, ss, ds, tq, ta):
    return dict(n=n, prev=prev, level=5, cefr='A2', title=title, emoji=emoji, theme='Health',
                next_file=nf, next_emoji=ne, game=game, grammar=grammar, words=words, story=story,
                ss=ss, ds=ds, think_q=tq, think_a=ta)

W = [
D(128, 127, 'Feeling Unwell', '🤒', 'Day129_AtTheClinic_A2.html', '🏥', 'tiles',
  'Talking about problems: I have a headache. My throat is sore.',
  [('unwell','ไม่สบาย','/ˌʌnˈwel/','🤒'),('fever','ไข้','/ˈfiːvə(r)/','🌡️'),
   ('cough','ไอ','/kɒf/','😷'),('sneeze','จาม','/sniːz/','🤧'),
   ('sore','เจ็บ','/sɔː(r)/','😖'),('ache','ปวด','/eɪk/','💢'),
   ('headache','ปวดหัว','/ˈhedeɪk/','🤯')],
  "This morning Ben felt unwell. His face was hot with fever. He began to cough and sneeze. My throat is sore, he said quietly. Mum touched his head. Do you have a headache too? Yes, my whole body aches. Stay in bed today, said Mum kindly.",
  ["This morning Ben felt unwell.","His face was hot with fever.","He began to cough and sneeze.","My throat is sore, he said.","Do you have a headache too?"],
  ["His face was hot with fever.","He began to cough and sneeze.","Do you have a headache too?"],
  "What did Mum tell Ben to do?","She told him to stay in bed."),

D(129, 128, 'At the Clinic', '🏥', 'Day130_MoveYourBody_A2.html', '🏃', 'scramble',
  'Past tense: take becomes took, feel becomes felt (irregular verbs).',
  [('clinic','คลินิก','/ˈklɪnɪk/','🏥'),('dentist','หมอฟัน','/ˈdentɪst/','🦷'),
   ('medicine','ยา','/ˈmedsn/','🧪'),('pill','ยาเม็ด','/pɪl/','💊'),
   ('injection','การฉีดยา','/ɪnˈdʒekʃn/','💉'),('bandage','ผ้าพันแผล','/ˈbændɪdʒ/','🩹'),
   ('recover','หายป่วย','/rɪˈkʌvə(r)/','💗')],
  "Mum took Ben to the clinic near their home. The doctor gave him some medicine. Take one pill after every meal. Ben was afraid of the injection but it did not hurt. Mimi cut her finger, so the nurse put a bandage on it. Next week they will visit the dentist. Soon Ben will recover.",
  ["Mum took Ben to the clinic.","The doctor gave him some medicine.","Take one pill after every meal.","The nurse put a bandage on it.","Soon Ben will recover."],
  ["The doctor gave him some medicine.","The nurse put a bandage on it.","Soon Ben will recover."],
  "Why did the nurse use a bandage?","Because Mimi cut her finger."),

D(130, 129, 'Move Your Body', '🏃', 'Day131_TimeToRest_A2.html', '😴', 'memory',
  'Present continuous: My heart is beating. We are running.',
  [('jog','วิ่งเหยาะ','/dʒɒɡ/','🏃'),('fitness','ความฟิต','/ˈfɪtnəs/','💪'),
   ('muscle','กล้ามเนื้อ','/ˈmʌsl/','🦾'),('breathe','หายใจ','/briːð/','🌬️'),
   ('heartbeat','การเต้นของหัวใจ','/ˈhɑːtbiːt/','❤️'),('pulse','ชีพจร','/pʌls/','📈'),
   ('stretchy','ยืดหยุ่น','/ˈstretʃi/','🤸')],
  "Every morning Leo and Dad jog around the park. Exercise is good for your fitness. Leo can feel his muscle grow stronger. Breathe slowly through your nose, said Dad. After running, his heartbeat was fast. Dad showed him how to find his pulse. Then they did some stretchy movements.",
  ["Leo and Dad jog around the park.","Exercise is good for your fitness.","Breathe slowly through your nose.","After running his heartbeat was fast.","Then they did some stretchy movements."],
  ["Exercise is good for your fitness.","Breathe slowly through your nose.","After running his heartbeat was fast."],
  "What did Dad show Leo?","He showed him how to find his pulse."),

D(131, 130, 'Time to Rest', '😴', 'Day132_SafetyFirst_A2.html', '🚧', 'wordsearch',
  'Adverbs of frequency: always, usually, sometimes, never.',
  [('nap','งีบหลับ','/næp/','🛌'),('alarm','นาฬิกาปลุก','/əˈlɑːm/','⏰'),
   ('awake','ตื่นอยู่','/əˈweɪk/','👁️'),('habit','นิสัย','/ˈhæbɪt/','🔁'),
   ('peaceful','สงบ','/ˈpiːsfl/','🤫'),('deeply','อย่างลึกซึ้ง','/ˈdiːpli/','🌙'),
   ('energy','พลังงาน','/ˈenədʒi/','⚡')],
  "A short nap after lunch is good for children. Mimi always sets her alarm for seven o'clock. Sometimes Ben stays awake too late. That is a bad habit! Keep the room peaceful and dark. Then you will sleep deeply. In the morning you will have lots of energy.",
  ["A short nap after lunch is good.","Mimi always sets her alarm for seven.","Sometimes Ben stays awake too late.","Keep the room peaceful and dark.","You will have lots of energy."],
  ["A short nap after lunch is good.","Keep the room peaceful and dark.","You will have lots of energy."],
  "What is Ben's bad habit?","He sometimes stays awake too late."),

D(132, 131, 'Safety First', '🚧', 'Day133_CleanAndHealthy_A2.html', '🧼', 'vowels',
  'Must / must not: You must wear a helmet. You must not run near the road.',
  [('safety','ความปลอดภัย','/ˈseɪfti/','🦺'),('helmet','หมวกกันน็อก','/ˈhelmɪt/','⛑️'),
   ('danger','อันตราย','/ˈdeɪndʒə(r)/','⚠️'),('warning','คำเตือน','/ˈwɔːnɪŋ/','📢'),
   ('accident','อุบัติเหตุ','/ˈæksɪdənt/','🚑'),('careful','ระมัดระวัง','/ˈkeəfl/','👀'),
   ('rule','กฎ','/ruːl/','📏')],
  "Safety is more important than speed. You must wear a helmet on a bicycle. Look for the red warning sign. It means danger! Be careful when you cross the road. Follow every rule at the swimming pool. Then you will never have an accident.",
  ["Safety is more important than speed.","You must wear a helmet on a bicycle.","Look for the red warning sign.","Be careful when you cross the road.","Follow every rule at the pool."],
  ["You must wear a helmet on a bicycle.","Be careful when you cross the road.","Follow every rule at the pool."],
  "What must you wear on a bicycle?","You must wear a helmet."),

D(133, 132, 'Clean and Healthy', '🧼', 'Day134_Week22Review_A2.html', '⭐', 'tiles',
  'Frequency: twice a day, three times a week.',
  [('hygiene','สุขอนามัย','/ˈhaɪdʒiːn/','🧴'),('germ','เชื้อโรค','/dʒɜːm/','🦠'),
   ('soap','สบู่','/səʊp/','🧼'),('towel','ผ้าเช็ดตัว','/ˈtaʊəl/','🧻'),
   ('toothbrush','แปรงสีฟัน','/ˈtuːθbrʌʃ/','🪥'),('spread','แพร่กระจาย','/spred/','↔️'),
   ('prevent','ป้องกันไม่ให้เกิด','/prɪˈvent/','🛡️')],
  "Good hygiene keeps you healthy. A germ is too small to see. Use soap and warm water for twenty seconds. Then dry your hands with a clean towel. Brush your teeth twice a day with your own toothbrush. Do not share it! Clean hands prevent germs from spreading to your family.",
  ["Good hygiene keeps you healthy.","A germ is too small to see.","Use soap and warm water.","Dry your hands with a clean towel.","Clean hands prevent germs from spreading."],
  ["A germ is too small to see.","Use soap and warm water.","Clean hands prevent germs from spreading."],
  "How long should you wash your hands?","For twenty seconds."),
]
for d in W:
    out = build(d)
    fn = 'Day%d_%s_A2.html' % (d['n'], d['title'].replace(' ','').replace("'",''))
    open(OUT+fn,'w',encoding='utf-8').write(out)
    print('OK', fn)
