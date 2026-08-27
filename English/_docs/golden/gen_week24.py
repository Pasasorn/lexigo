# -*- coding: utf-8 -*-
# Level 5 · Week 24 — Travel & The World (Day 142–148) + Day 149–150 · A2
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from golden_generator import build
OUT = '/sessions/wonderful-magical-bohr/mnt/English/Level5/'

def D(n, prev, title, emoji, nf, ne, game, grammar, words, story, ss, ds, tq, ta, theme='Travel'):
    return dict(n=n, prev=prev, level=5, cefr='A2', title=title, emoji=emoji, theme=theme,
                next_file=nf, next_emoji=ne, game=game, grammar=grammar, words=words, story=story,
                ss=ss, ds=ds, think_q=tq, think_a=ta)

W = [
D(142, 141, 'Packing to Go', '🧳', 'Day143_AtTheStation_A2.html', '🚉', 'tiles',
  'Going to + verb: We are going to visit my grandmother.',
  [('luggage','สัมภาระ','/ˈlʌɡɪdʒ/','🧳'),('passport','หนังสือเดินทาง','/ˈpɑːspɔːt/','📕'),
   ('booking','การจอง','/ˈbʊkɪŋ/','📅'),('departure','การออกเดินทาง','/dɪˈpɑːtʃə(r)/','🛫'),
   ('route','เส้นทาง','/ruːt/','🗺️'),('abroad','ต่างประเทศ','/əˈbrɔːd/','🌏'),
   ('tourist','นักท่องเที่ยว','/ˈtʊərɪst/','📸')],
  "Next week the family is going to travel abroad. Dad checked the booking on his phone. Mum found her passport in the drawer. Ben helped carry the heavy luggage. Our departure is at six in the morning. Leo studied the route on a big map. We will be a tourist family for one week!",
  ["The family is going to travel abroad.","Dad checked the booking on his phone.","Mum found her passport in the drawer.","Our departure is at six in the morning.","Leo studied the route on a map."],
  ["Dad checked the booking on his phone.","Our departure is at six in the morning.","Leo studied the route on a map."],
  "Where did Mum find her passport?","She found it in the drawer."),

D(143, 142, 'At the Station', '🚉', 'Day144_ByTheSea_A2.html', '🏖️', 'scramble',
  'Past tense: leave becomes left, wait becomes waited.',
  [('railway','ทางรถไฟ','/ˈreɪlweɪ/','🛤️'),('platform','ชานชาลา','/ˈplætfɔːm/','🚏'),
   ('carriage','ตู้โดยสาร','/ˈkærɪdʒ/','🚃'),('delay','ความล่าช้า','/dɪˈleɪ/','⏱️'),
   ('seatbelt','เข็มขัดนิรภัย','/ˈsiːtbelt/','🔗'),('aisle','ทางเดินระหว่างที่นั่ง','/aɪl/','🪟'),
   ('voyage','การเดินทางไกล','/ˈvɔɪɪdʒ/','🧭')],
  "They arrived early at the railway station. Our train leaves from platform three. There was a short delay of ten minutes. Then they found their carriage and sat down. Ben fastened his seatbelt on the bus later. Mimi walked down the aisle to find her seat. The whole voyage took four hours.",
  ["They arrived early at the railway station.","Our train leaves from platform three.","There was a short delay of ten minutes.","Mimi walked down the aisle to find her seat.","The whole voyage took four hours."],
  ["Our train leaves from platform three.","Mimi walked down the aisle to find her seat.","The whole voyage took four hours."],
  "How long was the delay?","It was ten minutes."),

D(144, 143, 'By the Sea', '🏖️', 'Day145_AmazingPlaces_A2.html', '🏛️', 'memory',
  'Superlative: the biggest, the most beautiful.',
  [('coast','ชายฝั่ง','/kəʊst/','🌊'),('island','เกาะ','/ˈaɪlənd/','🏝️'),
   ('horizon','เส้นขอบฟ้า','/həˈraɪzn/','🌅'),('shell','เปลือกหอย','/ʃel/','🐚'),
   ('tide','กระแสน้ำขึ้นลง','/taɪd/','〰️'),('sail','แล่นเรือ','/seɪl/','⛵'),
   ('seaside','ชายทะเล','/ˈsiːsaɪd/','🧂')],
  "The coast was the most beautiful place they had seen. A small island sat far away on the horizon. Mimi collected a pink shell from the sand. The tide rolled in slowly. Some boats began to sail past. Ben loved every minute at the seaside. This is the best day of the trip!",
  ["The coast was the most beautiful place.","A small island sat on the horizon.","Mimi collected a pink shell.","Some boats began to sail past.","Ben loved every minute at the seaside."],
  ["A small island sat on the horizon.","Mimi collected a pink shell.","Ben loved every minute at the seaside."],
  "What did Mimi collect from the sand?","She collected a pink shell."),

D(145, 144, 'Amazing Places', '🏛️', 'Day146_NewCultures_A2.html', '🌏', 'wordsearch',
  'Present perfect: I have visited. Have you ever seen...?',
  [('palace','พระราชวัง','/ˈpæləs/','🏰'),('landmark','สถานที่สำคัญ','/ˈlændmɑːk/','📍'),
   ('desert','ทะเลทราย','/ˈdezət/','🏜️'),('ancient','โบราณ','/ˈeɪnʃənt/','🏺'),
   ('statue','รูปปั้น','/ˈstætʃuː/','🗿'),('scenery','ทัศนียภาพ','/ˈsiːnəri/','🔭'),
   ('amazing','น่าทึ่ง','/əˈmeɪzɪŋ/','🤩')],
  "Have you ever seen an old palace? This one is the famous landmark of the city. It is more than four hundred years old and very ancient. A tall stone statue stood at the gate. From the top the scenery was amazing. One day I want to cross a desert too, said Ben.",
  ["Have you ever seen an old palace?","This is the famous landmark of the city.","It is more than four hundred years old.","A tall stone statue stood at the gate.","From the top the scenery was amazing."],
  ["This is the famous landmark of the city.","A tall stone statue stood at the gate.","From the top the scenery was amazing."],
  "How old is the palace?","It is more than four hundred years old."),

D(146, 145, 'New Cultures', '🌏', 'Day147_KeepingMemories_A2.html', '📮', 'vowels',
  'Talking about difference: In my country we... but here they...',
  [('culture','วัฒนธรรม','/ˈkʌltʃə(r)/','🎎'),('language','ภาษา','/ˈlæŋɡwɪdʒ/','💬'),
   ('custom','ธรรมเนียม','/ˈkʌstəm/','🙏'),('tradition','ประเพณี','/trəˈdɪʃn/','🏮'),
   ('greeting','การทักทาย','/ˈɡriːtɪŋ/','👋'),('admire','ชื่นชม','/ədˈmaɪə(r)/','🙇'),
   ('eager','กระตือรือร้น','/ˈiːɡə(r)/','🧐')],
  "Every country has its own culture. Ben tried to learn a few words of the local language. In Thailand the greeting is a wai. That is our custom, explained Mimi. Each tradition tells a story about the past. Always admire what makes a place special. An eager traveller learns something new every day.",
  ["Every country has its own culture.","Ben tried to learn the local language.","In Thailand the greeting is a wai.","Always admire what makes a place special.","An eager traveller learns something new."],
  ["Ben tried to learn the local language.","Always admire what makes a place special.","An eager traveller learns something new."],
  "What is the greeting in Thailand?","The greeting is a wai."),

D(147, 146, 'Keeping Memories', '📮', 'Day148_Week24Review_A2.html', '⭐', 'tiles',
  'Past tense: send becomes sent, write becomes wrote.',
  [('postcard','โปสต์การ์ด','/ˈpəʊstkɑːd/','📮'),('souvenir','ของที่ระลึก','/ˌsuːvəˈnɪə(r)/','🎁'),
   ('photograph','ภาพถ่าย','/ˈfəʊtəɡrɑːf/','📷'),('album','อัลบั้ม','/ˈælbəm/','📔'),
   ('scrapbook','สมุดติดภาพ','/ˈskræpbʊk/','✂️'),('lifetime','ชั่วชีวิต','/ˈlaɪftaɪm/','♾️'),
   ('farewell','การกล่าวลา','/ˌfeəˈwel/','👋')],
  "On the last day Mimi wrote a postcard to Grandma. Ben bought a small souvenir for his teacher. Dad took one more photograph of everyone. At home they put the pictures in an album. Mimi made a colourful scrapbook too. This trip will last a lifetime in our hearts. It was time to say farewell.",
  ["Mimi wrote a postcard to Grandma.","Ben bought a small souvenir.","Dad took one more photograph.","They put the pictures in an album.","This trip will last a lifetime."],
  ["Ben bought a small souvenir.","Dad took one more photograph.","This trip will last a lifetime."],
  "Who did Mimi write a postcard to?","She wrote to Grandma."),

D(149, 148, 'What I Can Do Now', '🌟', 'Day150_TheRoadAhead_A2.html', '🛣️', 'scramble',
  'Present perfect: I have learned five hundred words!',
  [('progress','ความก้าวหน้า','/ˈprəʊɡres/','📶'),('confidence','ความมั่นใจ','/ˈkɒnfɪdəns/','💪'),
   ('fluent','คล่องแคล่ว','/ˈfluːənt/','🗣️'),('review','ทบทวน','/rɪˈvjuː/','🔁'),
   ('mistake','ข้อผิดพลาด','/mɪˈsteɪk/','✏️'),('practice','การฝึกฝน','/ˈpræktɪs/','📈'),
   ('rejoice','ยินดีปรีดา','/rɪˈdʒɔɪs/','🎊')],
  "Look how much progress you have made! Ben can speak with real confidence now. He is not fluent yet, but his daily practice shows every week. Do you review the old words? asked the teacher. Everyone makes a mistake sometimes. That is how we learn. Today we rejoice together after one hundred and fifty days!",
  ["Look how much progress you have made.","Ben can speak with real confidence now.","His daily practice shows every week.","Everyone makes a mistake sometimes.","Today we rejoice together."],
  ["Ben can speak with real confidence now.","Everyone makes a mistake sometimes.","Today we rejoice together."],
  "Does everyone make mistakes?","Yes, and that is how we learn.", 'Special'),

D(150, 149, 'The Road Ahead', '🛣️', '../dashboard.html', '🏠', 'memory',
  'Future plans: Next month I am going to start Level 6.',
  [('challenge','ความท้าทาย','/ˈtʃælɪndʒ/','🧗'),('target','เป้าหมาย','/ˈtɑːɡɪt/','🎯'),
   ('effortless','ง่ายดาย','/ˈefətləs/','🪶'),('discipline','วินัย','/ˈdɪsəplɪn/','⏰'),
   ('persist','พากเพียร','/pəˈsɪst/','🔥'),('milestone','หมุดหมาย','/ˈmaɪlstəʊn/','🪧')],
  "Every new level is a bigger challenge. Set one clear target for next month. Nothing is effortless at the start. With daily discipline it becomes easy. Those who persist always win. Day one hundred and fifty is a happy milestone. The road ahead is long and exciting!",
  ["Every new level is a bigger challenge.","Set one clear target for next month.","Nothing is effortless at the start.","Those who persist always win.","Day 150 is a happy milestone."],
  ["Set one clear target for next month.","Those who persist always win.","Day 150 is a happy milestone."],
  "What happens with daily discipline?","It becomes easy.", 'Special'),
]
for d in W:
    d['words']=[w for w in d['words'] if w[0] and w[0].isascii()]
    out = build(d)
    fn = 'Day%d_%s_A2.html' % (d['n'], d['title'].replace(' ','').replace("'",''))
    open(OUT+fn,'w',encoding='utf-8').write(out)
    print('OK', fn, len(d['words']),'คำ')
