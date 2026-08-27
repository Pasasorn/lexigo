# -*- coding: utf-8 -*-
# Level 5 · Week 21 — Food & Cooking (Day 121–127) · A2
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from golden_generator import build
OUT = '/sessions/wonderful-magical-bohr/mnt/English/Level5/'

def D(n, prev, title, emoji, nf, ne, game, grammar, words, story, ss, ds, tq, ta):
    return dict(n=n, prev=prev, level=5, cefr='A2', title=title, emoji=emoji, theme='Food',
                next_file=nf, next_emoji=ne, game=game, grammar=grammar, words=words, story=story,
                ss=ss, ds=ds, think_q=tq, think_a=ta)

W = [
D(121, 120, 'A Special Recipe', '📖', 'Day122_InTheKitchen_A2.html', '🍳', 'tiles',
  'Sequence words: first, then, next, finally. They put steps in order.',
  [('recipe','สูตรอาหาร','/ˈresəpi/','📖'),('ingredient','ส่วนผสม','/ɪnˈɡriːdiənt/','🧺'),
   ('flour','แป้ง','/ˈflaʊə(r)/','🌾'),('sugar','น้ำตาล','/ˈʃʊɡə(r)/','🧁'),
   ('mix','ผสม','/mɪks/','🥣'),('pour','เท','/pɔː(r)/','🫗'),
   ('bake','อบ','/beɪk/','🔥')],
  "Grandma opened her old recipe book. First we need every ingredient, she said. Ben measured the white flour. Mimi added two spoons of sugar. Leo began to mix them in a big bowl. Then Grandma helped them pour the batter into a tin. Finally they bake it for thirty minutes.",
  ["Grandma opened her old recipe book.","First we need every ingredient.","Ben measured the white flour.","Leo began to mix them in a bowl.","Finally they bake it for thirty minutes."],
  ["Ben measured the white flour.","Leo began to mix them in a bowl.","Finally they bake it for thirty minutes."],
  "What did Mimi add to the bowl?","She added two spoons of sugar."),

D(122, 121, 'In the Kitchen', '🍳', 'Day123_HowDoesItTaste_A2.html', '👅', 'scramble',
  'Past tense: cut becomes cut (same form!), put becomes put.',
  [('chop','สับ','/tʃɒp/','🔪'),('slice','หั่นเป็นแผ่น','/slaɪs/','🍞'),
   ('boil','ต้ม','/bɔɪl/','♨️'),('fry','ทอด','/fraɪ/','🍳'),
   ('dish','จานอาหาร','/dɪʃ/','🍽️'),('serve','เสิร์ฟ','/sɜːv/','🤵'),
   ('spoonful','หนึ่งช้อน','/ˈspuːnfʊl/','🥄')],
  "Dad let the children help in the kitchen. Mimi began to chop the carrots. Ben tried to slice the bread carefully. Dad put water in a pot to boil the eggs. Then he started to fry the rice. One spoonful of soy sauce is enough! Soon the hot dish was ready to serve.",
  ["Dad let the children help in the kitchen.","Mimi began to chop the carrots.","Ben tried to slice the bread.","Dad started to fry the rice.","The hot dish was ready to serve."],
  ["Mimi began to chop the carrots.","Dad started to fry the rice.","The hot dish was ready to serve."],
  "What did Mimi chop?","She chopped the carrots."),

D(123, 122, 'How Does It Taste?', '👅', 'Day124_AtTheRestaurant_A2.html', '🍽️', 'memory',
  'Adjectives after "taste": It tastes sweet. It tastes salty.',
  [('flavour','รสชาติ','/ˈfleɪvə(r)/','🌈'),('sweet','หวาน','/swiːt/','🍬'),
   ('sour','เปรี้ยว','/ˈsaʊə(r)/','🍋'),('salty','เค็ม','/ˈsɔːlti/','🧂'),
   ('bitter','ขม','/ˈbɪtə(r)/','☕'),('spicy','เผ็ด','/ˈspaɪsi/','🌶️'),
   ('crispy','กรอบ','/ˈkrɪspi/','🥨')],
  "Every food has its own flavour. The cake was very sweet. Ben ate a lemon and made a funny face. It is too sour! The soup was a little salty. Dark coffee tastes bitter to children. Mimi loves spicy noodles. Leo likes crispy chicken best of all.",
  ["Every food has its own flavour.","The cake was very sweet.","It is too sour, said Ben.","Mimi loves spicy noodles.","Leo likes crispy chicken best."],
  ["The cake was very sweet.","Mimi loves spicy noodles.","Leo likes crispy chicken best."],
  "Why did Ben make a funny face?","Because the lemon was too sour."),

D(124, 123, 'At the Restaurant', '🍽️', 'Day125_HealthyEating_A2.html', '🥗', 'wordsearch',
  'Polite requests: Could I have...? / May we order...?',
  [('menu','เมนู','/ˈmenjuː/','📋'),('order','สั่งอาหาร','/ˈɔːdə(r)/','✍️'),
   ('waiter','พนักงานเสิร์ฟ','/ˈweɪtə(r)/','🤵'),('customer','ลูกค้า','/ˈkʌstəmə(r)/','🧑'),
   ('bill','บิล','/bɪl/','🧾'),('tip','เงินทิป','/tɪp/','💵'),
   ('manners','มารยาท','/ˈmænəz/','🙇')],
  "The family sat down and looked at the menu. A kind waiter came to their table. May we order now? asked Dad politely. Every customer in the room looked happy. Ben said thank you and showed good manners. After the meal Dad paid the bill. He also left a small tip.",
  ["The family looked at the menu.","A kind waiter came to their table.","May we order now, asked Dad.","After the meal Dad paid the bill.","He also left a small tip."],
  ["A kind waiter came to their table.","After the meal Dad paid the bill.","He also left a small tip."],
  "Who came to their table?","A kind waiter came."),

D(125, 124, 'Healthy Eating', '🥗', 'Day126_MarketDay_A2.html', '🧺', 'vowels',
  'Should / should not: We should eat vegetables. We should not eat too much sugar.',
  [('healthy','ดีต่อสุขภาพ','/ˈhelθi/','💚'),('vitamin','วิตามิน','/ˈvɪtəmɪn/','💊'),
   ('protein','โปรตีน','/ˈprəʊtiːn/','🥚'),('portion','ปริมาณต่อมื้อ','/ˈpɔːʃn/','🍽️'),
   ('balance','ความสมดุล','/ˈbæləns/','🧘'),('avoid','หลีกเลี่ยง','/əˈvɔɪd/','🚫'),
   ('nutrition','โภชนาการ','/njuˈtrɪʃn/','🥬')],
  "A healthy body needs good food. Fruit gives us vitamin C. Eggs and beans give us protein. You should avoid too much sugar, said the nurse. A small portion of cake is fine after school. Balance is the secret! Good nutrition helps you grow tall and strong.",
  ["A healthy body needs good food.","Fruit gives us vitamin C.","You should avoid too much sugar.","A small portion of cake is fine after school.","Good nutrition helps you grow."],
  ["Fruit gives us vitamin C.","A small portion of cake is fine after school.","Good nutrition helps you grow."],
  "What gives us protein?","Eggs and beans give us protein."),

D(126, 125, 'Market Day', '🛒', 'Day127_Week21Review_A2.html', '⭐', 'tiles',
  'Countable and uncountable: three apples / some rice.',
  [('seller','คนขาย','/ˈselə(r)/','🧑‍🌾'),('stall','แผงขายของ','/stɔːl/','🎪'),
   ('weigh','ชั่งน้ำหนัก','/weɪ/','⚖️'),('kilo','กิโล','/ˈkiːləʊ/','📦'),
   ('bargain','ของถูกคุ้มค่า','/ˈbɑːɡən/','💰'),('crowded','แออัด','/ˈkraʊdɪd/','👥'),
   ('trolley','รถเข็น','/ˈtrɒli/','🛒')],
  "On Sunday they walked to the crowded street. Each stall sold something different. Mum asked the seller to weigh the fish. We need one kilo, please. These mangoes are a real bargain today! Ben helped pick the best ones. Mimi pushed the heavy trolley home.",
  ["They walked to the crowded street.","Each stall sold something different.","Mum asked the seller to weigh the fish.","These mangoes are a real bargain today.","Mimi pushed the heavy trolley home."],
  ["Each stall sold something different.","These mangoes are a real bargain today.","Mimi pushed the heavy trolley home."],
  "What did Mum ask the seller to do?","She asked him to weigh the fish."),
]
for d in W:
    out = build(d)
    fn = 'Day%d_%s_A2.html' % (d['n'], d['title'].replace(' ','').replace("'",'').replace('?',''))
    open(OUT+fn,'w',encoding='utf-8').write(out)
    print('OK', fn)
