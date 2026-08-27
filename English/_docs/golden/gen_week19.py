# -*- coding: utf-8 -*-
# Week 19 — Nature & Seasons (Day 105–111) · Level 4 · A2
# คำทั้ง 42 ตรวจแล้วไม่ซ้ำกับ 495 คำเดิม (check_new_words.py)
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from golden_generator import build

OUT = '/sessions/wonderful-magical-bohr/mnt/English/Level4/'


def D(n, prev, title, emoji, nf, ne, game, grammar, words, story, ss, ds, tq, ta):
    return dict(n=n, prev=prev, level=4, cefr='A2', title=title, emoji=emoji, theme='Nature',
                next_file=nf, next_emoji=ne, game=game, grammar=grammar, words=words, story=story,
                ss=ss, ds=ds, think_q=tq, think_a=ta)


W = [
D(105, 104, 'Deep in the Woods', '🌳', 'Day106_GrowingPlants_A2.html', '🌱', 'tiles',
  'Past tense: walk becomes walked, look becomes looked (add -ed).',
  [('wood', 'ป่าไม้', '/wʊd/', '🌲'), ('branch', 'กิ่งไม้', '/brɑːntʃ/', '🌿'),
   ('root', 'ราก', '/ruːt/', '🪵'), ('bark', 'เปลือกไม้', '/bɑːk/', '🟤'),
   ('shade', 'ร่มเงา', '/ʃeɪd/', '🌥️'), ('still', 'นิ่ง', '/stɪl/', '🤫'),
   ('discover', 'ค้นพบ', '/dɪˈskʌvə(r)/', '🔎')],
  "Leo, Mimi and Ben walked into the quiet wood. A big branch hung above their heads. Ben touched the rough bark of an old tree. Look at this root! It is bigger than my arm. They sat in the cool shade and stayed very still. Then Mimi began to discover something small moving near her foot.",
  ["They walked into the quiet wood.",
   "A big branch hung above their heads.",
   "Ben touched the rough bark.",
   "They sat in the cool shade.",
   "Mimi began to discover something small."],
  ["A big branch hung above their heads.",
   "Ben touched the rough bark.",
   "They sat in the cool shade."],
  "Where did the three friends sit?", "They sat in the cool shade."),

D(106, 105, 'Growing Plants', '🌱', 'Day107_LittleCreatures_A2.html', '🐞', 'scramble',
  'Past tense: plant becomes planted, water becomes watered (add -ed).',
  [('plant', 'ต้นไม้ / ปลูก', '/plɑːnt/', '🪴'), ('seed', 'เมล็ด', '/siːd/', '🌰'),
   ('soil', 'ดิน', '/sɔɪl/', '🟫'), ('sprout', 'แตกหน่อ', '/spraʊt/', '🌱'),
   ('sunlight', 'แสงแดด', '/ˈsʌnlaɪt/', '☀️'), ('bloom', 'ผลิบาน', '/bluːm/', '🌺'),
   ('gardener', 'คนสวน', '/ˈɡɑːdnə(r)/', '👨‍🌾')],
  "Grandpa is a careful gardener. He gave each child one small seed. Ben pushed his seed into the soft soil. Mimi watered her plant every morning. Warm sunlight helped them grow. After one week the first seed began to sprout! In spring the flowers will bloom, said Grandpa with a smile.",
  ["Grandpa is a careful gardener.",
   "He gave each child one small seed.",
   "Ben pushed his seed into the soil.",
   "Warm sunlight helped them grow.",
   "The first seed began to sprout."],
  ["He gave each child one small seed.",
   "Warm sunlight helped them grow.",
   "The first seed began to sprout."],
  "What did Grandpa give each child?", "He gave each child one small seed."),

D(107, 106, 'Little Creatures', '🐞', 'Day108_ByTheWater_A2.html', '💧', 'memory',
  'Past tense: find becomes found (irregular verb).',
  [('beetle', 'ด้วง', '/ˈbiːtl/', '🪲'), ('spider', 'แมงมุม', '/ˈspaɪdə(r)/', '🕷️'),
   ('web', 'ใยแมงมุม', '/web/', '🕸️'), ('nest', 'รัง', '/nest/', '🪹'),
   ('wing', 'ปีก', '/wɪŋ/', '🪽'), ('feather', 'ขนนก', '/ˈfeðə(r)/', '🪶'),
   ('crawl', 'คลาน', '/krɔːl/', '🐛')],
  "A shiny beetle began to crawl across Ben's shoe. Above them a spider sat in the centre of its web. Mimi found a soft feather on the ground. Look up! There is a bird nest in the branch. A small bird opened one wing and flew away. Nature is full of tiny wonders.",
  ["A shiny beetle began to crawl.",
   "A spider sat in its web.",
   "Mimi found a soft feather.",
   "There is a bird nest in the branch.",
   "A small bird opened one wing."],
  ["A spider sat in its web.",
   "Mimi found a soft feather.",
   "A small bird opened one wing."],
  "What did Mimi find on the ground?", "She found a soft feather."),

D(108, 107, 'By the Water', '💧', 'Day109_WeatherChanges_A2.html', '⛈️', 'wordsearch',
  'Past tense: throw becomes threw, swim becomes swam (irregular verbs).',
  [('stream', 'ลำธาร', '/striːm/', '🏞️'), ('pond', 'สระน้ำ', '/pɒnd/', '🦆'),
   ('stone', 'ก้อนหิน', '/stəʊn/', '🪨'), ('pebble', 'กรวด', '/ˈpebl/', '⚪'),
   ('deep', 'ลึก', '/diːp/', '🌊'), ('float', 'ลอย', '/fləʊt/', '🛟'),
   ('flow', 'ไหล', '/fləʊ/', '➡️')],
  "A small stream ran beside the path. The water was clear but not deep. Ben threw a flat stone and it jumped three times! Mimi collected a smooth pebble for her pocket. A dry leaf began to float on the water. Watch how it moves, said Leo. The stream will flow all the way to the pond.",
  ["A small stream ran beside the path.",
   "The water was clear but not deep.",
   "Ben threw a flat stone.",
   "A dry leaf began to float.",
   "The stream will flow to the pond."],
  ["The water was clear but not deep.",
   "Ben threw a flat stone.",
   "A dry leaf began to float."],
  "What did Ben throw into the stream?", "He threw a flat stone."),

D(109, 108, 'Weather Changes', '⛈️', 'Day110_TakeCareOfEarth_A2.html', '🌍', 'vowels',
  'Past tense: begin becomes began, run becomes ran (irregular verbs).',
  [('thunder', 'ฟ้าร้อง', '/ˈθʌndə(r)/', '🌩️'), ('lightning', 'ฟ้าแลบ', '/ˈlaɪtnɪŋ/', '⚡'),
   ('breeze', 'ลมอ่อน', '/briːz/', '🍃'), ('fog', 'หมอก', '/fɒɡ/', '🌫️'),
   ('freeze', 'แข็งตัว', '/friːz/', '🧊'), ('melt', 'ละลาย', '/melt/', '💧'),
   ('forecast', 'พยากรณ์อากาศ', '/ˈfɔːkɑːst/', '📺')],
  "In the morning a cool breeze moved the leaves. Thick fog covered the hill. Later the sky turned grey and they heard thunder. Bright lightning flashed above the wood! The forecast said rain, so they ran home. In winter this water will freeze into ice. In spring the ice will melt again.",
  ["A cool breeze moved the leaves.",
   "Thick fog covered the hill.",
   "They heard thunder in the sky.",
   "Bright lightning flashed above the wood.",
   "In spring the ice will melt again."],
  ["Thick fog covered the hill.",
   "They heard thunder in the sky.",
   "In spring the ice will melt again."],
  "Why did the children run home?", "Because the forecast said rain."),

D(110, 109, 'Take Care of Earth', '🌍', 'Day111_Week19Review_A2.html', '⭐', 'tiles',
  'Past tense: put becomes put (same form!), keep becomes kept.',
  [('planet', 'ดาวเคราะห์', '/ˈplænɪt/', '🌏'), ('litter', 'ขยะเกลื่อน', '/ˈlɪtə(r)/', '🗑️'),
   ('waste', 'ของเสีย', '/weɪst/', '♻️'), ('pollution', 'มลพิษ', '/pəˈluːʃn/', '🏭'),
   ('recycle', 'รีไซเคิล', '/ˌriːˈsaɪkl/', '🔄'), ('protect', 'ปกป้อง', '/prəˈtekt/', '🛡️'),
   ('save', 'รักษาไว้', '/seɪv/', '💚')],
  "On the way home they saw litter beside the path. Ben put every plastic bottle into his bag. We must protect our planet, he said. Cars and factories make pollution. Do not throw waste on the ground! At school they recycle paper every week. Small actions save the Earth for the future.",
  ["They saw litter beside the path.",
   "Ben put the bottles into his bag.",
   "We must protect our planet.",
   "At school they recycle paper.",
   "Small actions save the Earth."],
  ["Ben put the bottles into his bag.",
   "We must protect our planet.",
   "At school they recycle paper."],
  "What did Ben do with the plastic bottles?", "He put them into his bag."),
]

for d in W:
    out = build(d)
    fn = 'Day%d_%s_A2.html' % (d['n'], d['title'].replace(' ', '').replace("'", ''))
    open(OUT + fn, 'w', encoding='utf-8').write(out)
    leak = out.count('Day 61') + out.count('wla_d61') + out.count('Happy Feelings')
    print('%s %s leak=%d' % ('OK' if leak == 0 else 'WARN', fn, leak))
