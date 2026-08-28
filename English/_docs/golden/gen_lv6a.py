# -*- coding: utf-8 -*-
# Level 6 · Week 25 Family & Home (151–157) + Week 26 Hobbies & Arts (158–164) · A2
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from golden_generator import build
OUT = '/sessions/wonderful-magical-bohr/mnt/English/Level6/'

def D(n, prev, title, emoji, nf, ne, game, grammar, words, story, ss, ds, tq, ta, theme='Home'):
    return dict(n=n, prev=prev, level=6, cefr='A2', title=title, emoji=emoji, theme=theme,
                next_file=nf, next_emoji=ne, game=game, grammar=grammar, words=words, story=story,
                ss=ss, ds=ds, think_q=tq, think_a=ta)

W = [
D(151,150,'Our Big Family','👨‍👩‍👧‍👦','Day152_HouseholdChores_A2.html','🧹','tiles',
  "Possessive 's: my aunt's house, Ben's cousin.",
  [('relative','ญาติ','/ˈrelətɪv/','👪'),('cousin','ลูกพี่ลูกน้อง','/ˈkʌzn/','🧒'),
   ('aunt','ป้า/น้า','/ɑːnt/','👩'),('uncle','ลุง/อา','/ˈʌŋkl/','👨'),
   ('grandparent','ปู่ย่าตายาย','/ˈɡrænpeərənt/','👵'),('twin','ฝาแฝด','/twɪn/','👯'),
   ('nephew','หลานชาย','/ˈnefjuː/','👦')],
  "On Sunday every relative came to Grandma's house. Ben met his cousin from the north. My aunt brought sticky rice and my uncle brought fruit. Each grandparent told an old story. Mimi has a twin sister named May. Uncle Sam calls Leo his favourite nephew. A big family is a warm family!",
  ["On Sunday every relative came to Grandma's house.","Ben met his cousin from the north.","My aunt brought sticky rice.","Each grandparent told an old story.","Mimi has a twin sister named May."],
  ["Ben met his cousin from the north.","Each grandparent told an old story.","Mimi has a twin sister named May."],
  "Who did Ben meet on Sunday?","He met his cousin from the north."),

D(152,151,'Household Chores','🧹','Day153_AroundTheHouse_A2.html','🛋️','scramble',
  'Have to / has to: I have to sweep the floor.',
  [('household','ครัวเรือน','/ˈhaʊshəʊld/','🏠'),('chore','งานบ้าน','/tʃɔː(r)/','🧾'),
   ('sweep','กวาด','/swiːp/','🧹'),('dust','ปัดฝุ่น','/dʌst/','🪶'),
   ('laundry','ผ้าที่ต้องซัก','/ˈlɔːndri/','🧺'),('iron','รีดผ้า','/ˈaɪən/','♨️'),
   ('repair','ซ่อม','/rɪˈpeə(r)/','🔧')],
  "Every household needs teamwork. Mum wrote a chore list on the door. Leo has to sweep the kitchen floor. Mimi will dust the shelves. Dad puts the laundry into the machine. Later he will iron three shirts. Ben helps Grandpa repair the broken chair. Many hands make light work!",
  ["Every household needs teamwork.","Mum wrote a chore list on the door.","Leo has to sweep the kitchen floor.","Dad puts the laundry into the machine.","Ben helps Grandpa repair the chair."],
  ["Mum wrote a chore list on the door.","Dad puts the laundry into the machine.","Ben helps Grandpa repair the chair."],
  "What does Leo have to do?","He has to sweep the kitchen floor."),

D(153,152,'Around the House','🛋️','Day154_OurNeighbourhood_A2.html','🏘️','memory',
  'Prepositions of place: above, below, beside, between.',
  [('furniture','เฟอร์นิเจอร์','/ˈfɜːnɪtʃə(r)/','🛋️'),('cupboard','ตู้','/ˈkʌbəd/','🗄️'),
   ('drawer','ลิ้นชัก','/drɔː(r)/','📦'),('curtain','ผ้าม่าน','/ˈkɜːtn/','🪟'),
   ('carpet','พรม','/ˈkɑːpɪt/','🟥'),('ceiling','เพดาน','/ˈsiːlɪŋ/','⬆️'),
   ('balcony','ระเบียง','/ˈbælkəni/','🌇')],
  "Their new furniture arrived this morning. Mum put the plates inside the cupboard. Ben keeps his socks in the top drawer. A blue curtain hangs beside the window. There is a soft carpet under the table. A small lamp hangs from the ceiling. From the balcony you can see the whole street.",
  ["Their new furniture arrived this morning.","Mum put the plates inside the cupboard.","Ben keeps his socks in the top drawer.","There is a soft carpet under the table.","From the balcony you can see the street."],
  ["Mum put the plates inside the cupboard.","There is a soft carpet under the table.","From the balcony you can see the street."],
  "Where does Ben keep his socks?","He keeps them in the top drawer."),

D(154,153,'Our Neighbourhood','🏘️','Day155_MyCollection_A2.html','🎒','wordsearch',
  'There is / there are: There is a park. There are three shops.',
  [('neighbourhood','ละแวกบ้าน','/ˈneɪbəhʊd/','🏘️'),('apartment','อพาร์ตเมนต์','/əˈpɑːtmənt/','🏢'),
   ('rent','ค่าเช่า','/rent/','💴'),('landlord','เจ้าของบ้านเช่า','/ˈlændlɔːd/','🔑'),
   ('corridor','ทางเดิน','/ˈkɒrɪdɔː(r)/','🚪'),('lift','ลิฟต์','/lɪft/','🛗'),
   ('resident','ผู้อยู่อาศัย','/ˈrezɪdənt/','🌙')],
  "Ben lives in a friendly neighbourhood. His family rents an apartment on the fifth floor. They pay the rent on the first day of each month. Their landlord is a kind old man. The corridor outside is always clean. They take the lift up and down. Every resident keeps the noise down after nine.",
  ["Ben lives in a friendly neighbourhood.","His family rents an apartment.","They pay the rent each month.","Their landlord is a kind old man.","Every resident keeps the noise down after nine."],
  ["His family rents an apartment.","Their landlord is a kind old man.","Every resident keeps the noise down after nine."],
  "Who is their landlord?","He is a kind old man."),

D(155,154,'My Collection','🎒','Day156_MakingMusic_A2.html','🎵','vowels',
  'How long have you...? I have collected them for two years.',
  [('collection','คอลเลกชัน','/kəˈlekʃn/','🗃️'),('model','โมเดล','/ˈmɒdl/','🚗'),
   ('chess','หมากรุก','/tʃes/','♟️'),('sketch','ภาพร่าง','/sketʃ/','✏️'),
   ('pottery','เครื่องปั้นดินเผา','/ˈpɒtəri/','🏺'),('knit','ถัก','/nɪt/','🧶'),
   ('sew','เย็บ','/səʊ/','🪡')],
  "Ben has a big collection of stamps. Leo builds a small model car every month. On rainy days they play chess together. Mimi likes to sketch faces in her notebook. Grandma teaches pottery at the centre. She can also knit warm scarves. Mum will sew a new bag for school.",
  ["Ben has a big collection of stamps.","Leo builds a small model car.","On rainy days they play chess.","Mimi likes to sketch faces.","Grandma teaches pottery at the centre."],
  ["Leo builds a small model car.","Mimi likes to sketch faces.","Grandma teaches pottery at the centre."],
  "What does Mimi like to sketch?","She likes to sketch faces."),

D(156,155,'Making Music','🎵','Day157_Week25Review_A2.html','⭐','tiles',
  'Can / cannot for ability: She can play the flute.',
  [('melody','ทำนอง','/ˈmelədi/','🎼'),('rhythm','จังหวะ','/ˈrɪðəm/','🥁'),
   ('perform','แสดง','/pəˈfɔːm/','🎤'),('stage','เวที','/steɪdʒ/','🎭'),
   ('audience','ผู้ชม','/ˈɔːdiəns/','👏'),('rehearse','ซ้อม','/rɪˈhɜːs/','🔁'),
   ('costume','ชุดแสดง','/ˈkɒstjuːm/','👘')],
  "The school band practised a soft melody. Ben keeps the rhythm on the drum. Next Friday they will perform for the whole school. Mimi felt shy when she stood on the stage. Do not look at the audience, said Leo. They rehearse every afternoon. Mum is making a bright costume for Mimi.",
  ["The school band practised a soft melody.","Ben keeps the rhythm on the drum.","They will perform for the whole school.","Mimi stood on the stage.","They rehearse every afternoon."],
  ["Ben keeps the rhythm on the drum.","Mimi stood on the stage.","They rehearse every afternoon."],
  "When will the band perform?","They will perform next Friday."),
]
for d in W:
    out = build(d)
    fn = 'Day%d_%s_A2.html' % (d['n'], d['title'].replace(' ','').replace("'",''))
    open(OUT+fn,'w',encoding='utf-8').write(out)
    print('OK', fn)
