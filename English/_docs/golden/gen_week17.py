# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0,os.path.dirname(__file__))
from golden_generator import build
OUT='/sessions/wonderful-magical-bohr/mnt/English/Level4/'

def D(n,prev,title,emoji,nf,ne,game,grammar,words,story,ss,ds,tq,ta):
    return dict(n=n,prev=prev,level=4,cefr='A2',title=title,emoji=emoji,theme='A Day Out',
        next_file=nf,next_emoji=ne,game=game,grammar=grammar,words=words,story=story,ss=ss,ds=ds,
        think_q=tq,think_a=ta)

W=[
D(91,90,'Getting Ready','🎒','Day92_OnTheWay_A2.html','⛴️','tiles',
  'Past tense: add -ed → pack becomes packed, look becomes looked.',
  [('suitcase','กระเป๋าเดินทาง','/ˈsuːtkeɪs/','🧳'),('backpack','เป้','/ˈbækpæk/','🎒'),('snack','ของว่าง','/snæk/','🍪'),('camera','กล้อง','/ˈkæmərə/','📷'),('torch','ไฟฉาย','/tɔːtʃ/','🔦'),('explore','สำรวจ','/ɪkˈsplɔː/','🧭'),('adventure','การผจญภัย','/ədˈventʃə/','🌄')],
  "The three friends were excited for their adventure. Leo packed his backpack with a snack and a torch. Mimi put her camera in her suitcase. What should we explore first? asked Ben. Let us find out! said Leo. They were ready to explore the big forest. It was going to be a wonderful day!",
  ["The friends were ready for their adventure.","Leo packed his backpack.","Mimi put her camera in her suitcase.","Let us explore! said Leo.","It was a wonderful day."],
  ["Leo packed his backpack.","Mimi put her camera in her suitcase.","Let us explore! said Leo."],
  "What did Leo pack in his backpack?","A snack and a torch."),
D(92,91,'On the Way','⛴️','Day93_InTheForest_A2.html','🌲','scramble',
  'Past tense: take becomes took (irregular verb).',
  [('seat','ที่นั่ง','/siːt/','💺'),('engine','เครื่องยนต์','/ˈendʒɪn/','⚙️'),('passenger','ผู้โดยสาร','/ˈpæsɪndʒə/','🧑'),('ferry','เรือข้ามฟาก','/ˈferi/','⛴️'),('sunrise','พระอาทิตย์ขึ้น','/ˈsʌnraɪz/','🌅'),('arrive','มาถึง','/əˈraɪv/','📍'),('depart','ออกเดินทาง','/dɪˈpɑːt/','🚏')],
  "The friends took a ferry across the lake. Leo found a seat by the window. Look at the big engine! said Ben. Every passenger watched the beautiful sunrise. The ferry would arrive soon. When did we depart? asked Mimi. Early in the morning! laughed Leo.",
  ["The friends took a ferry.","Leo found a seat by the window.","Every passenger watched the sunrise.","The ferry would arrive soon.","When did we depart? asked Mimi."],
  ["Leo found a seat by the window.","Every passenger watched the sunrise.","When did we depart? asked Mimi."],
  "What did the passengers watch?","The beautiful sunrise."),
D(93,92,'In the Forest','🌲','Day94_AnimalsWeSee_A2.html','🦌','memory',
  'Past tense: see becomes saw (irregular verb).',
  [('forest','ป่า','/ˈfɒrɪst/','🌲'),('trail','เส้นทางเดิน','/treɪl/','🥾'),('hill','เนินเขา','/hɪl/','⛰️'),('valley','หุบเขา','/ˈvæli/','🏞️'),('view','ทิวทัศน์','/vjuː/','🔭'),('climb','ปีน','/klaɪm/','🧗'),('wildlife','สัตว์ป่า','/ˈwaɪldlaɪf/','🦊')],
  "They walked into the green forest. A small trail went up a tall hill. From the top, they saw a wide valley. What a beautiful view! said Mimi. Leo wanted to climb a big rock. Ben looked for wildlife in the trees. The forest was full of life!",
  ["They walked into the green forest.","A trail went up a tall hill.","They saw a wide valley.","Leo wanted to climb a rock.","Ben looked for wildlife."],
  ["A trail went up a tall hill.","They saw a wide valley.","Ben looked for wildlife."],
  "What did they see from the top of the hill?","A wide valley."),
D(94,93,'Animals We See','🦌','Day95_PicnicLunch_A2.html','🧺','wordsearch',
  'Past tense: run becomes ran (irregular verb).',
  [('ranger','เจ้าหน้าที่ป่า','/ˈreɪndʒə/','👮'),('guide','ไกด์','/ɡaɪd/','🧭'),('squirrel','กระรอก','/ˈskwɪrəl/','🐿️'),('deer','กวาง','/dɪə/','🦌'),('waterfall','น้ำตก','/ˈwɔːtəfɔːl/','💦'),('splash','กระเซ็น','/splæʃ/','💧'),('wonderful','วิเศษ','/ˈwʌndəfl/','✨')],
  "In the forest, they met a park ranger. She was their guide. Look, a squirrel! said Ben. It ran up a tree. Then they saw a deer near the waterfall. The water made a big splash. What a wonderful place! said Mimi. The ranger smiled.",
  ["They met a park ranger.","She was their guide.","A squirrel ran up a tree.","They saw a deer near the waterfall.","What a wonderful place!"],
  ["She was their guide.","A squirrel ran up a tree.","What a wonderful place!"],
  "Who was their guide?","A park ranger."),
D(95,94,'Picnic Lunch','🧺','Day96_EveningAndHome_A2.html','🏕️','vowels',
  'Past tense: eat becomes ate (irregular verb).',
  [('picnic','ปิกนิก','/ˈpɪknɪk/','🧺'),('basket','ตะกร้า','/ˈbɑːskɪt/','🧺'),('sandwich','แซนด์วิช','/ˈsænwɪdʒ/','🥪'),('bottle','ขวด','/ˈbɒtl/','🍶'),('napkin','ผ้าเช็ดปาก','/ˈnæpkɪn/','🧻'),('blanket','ผ้าห่ม','/ˈblæŋkɪt/','🛌'),('delicious','อร่อย','/dɪˈlɪʃəs/','😋')],
  "It was time for a picnic! Mimi opened the basket. Leo made a sandwich for everyone. Ben poured water from a bottle. They sat on a soft blanket. Do not forget your napkin! said Mimi. The food was delicious. Everyone ate and laughed together.",
  ["It was time for a picnic!","Mimi opened the basket.","Leo made a sandwich.","They sat on a soft blanket.","The food was delicious."],
  ["Mimi opened the basket.","Leo made a sandwich.","The food was delicious."],
  "What did Leo make for everyone?","A sandwich."),
D(96,95,'Evening and Home','🏕️','Day97_Week17Review_A2.html','⭐','tiles',
  'Past tense: go becomes went (irregular verb).',
  [('campfire','กองไฟ','/ˈkæmpfaɪə/','🔥'),('tent','เต็นท์','/tent/','⛺'),('lake','ทะเลสาบ','/leɪk/','🏞️'),('sunset','พระอาทิตย์ตก','/ˈsʌnset/','🌇'),('photo','รูปถ่าย','/ˈfəʊtəʊ/','📸'),('memory','ความทรงจำ','/ˈmeməri/','💭'),('sleepy','ง่วง','/ˈsliːpi/','😴')],
  "In the evening, they made a campfire near the lake. They sat by the warm tent. The sunset was orange and pink. Mimi took a photo of the view. What a happy memory! said Leo. Ben was very sleepy. Then they all went home. What a wonderful trip!",
  ["They made a campfire near the lake.","They sat by the warm tent.","The sunset was orange and pink.","Mimi took a photo.","Ben was very sleepy."],
  ["They sat by the warm tent.","The sunset was orange and pink.","Mimi took a photo."],
  "What did Mimi take a photo of?","The view."),
]
for d in W:
    out=build(d)
    fn='Day%d_%s_A2.html'%(d['n'],d['title'].replace(' ',''))
    open(OUT+fn,'w',encoding='utf-8').write(out)
    leak=out.count('Day 61')+out.count('wla_d61')+out.count('D61-')+out.count('Happy Feelings')
    print('%s %s leak=%d'%('✅' if leak==0 else '⚠️',fn,leak))
