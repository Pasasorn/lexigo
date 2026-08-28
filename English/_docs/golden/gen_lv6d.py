# -*- coding: utf-8 -*-
# Level 6 · Week 28 Our World (172–178) + Day 179–180 จบ A2 · A2
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from golden_generator import build
OUT = '/sessions/wonderful-magical-bohr/mnt/English/Level6/'

def D(n, prev, title, emoji, nf, ne, game, grammar, words, story, ss, ds, tq, ta, theme='World'):
    return dict(n=n, prev=prev, level=6, cefr='A2', title=title, emoji=emoji, theme=theme,
                next_file=nf, next_emoji=ne, game=game, grammar=grammar, words=words, story=story,
                ss=ss, ds=ds, think_q=tq, think_a=ta)

W = [
D(172,171,'Our Country','🇹🇭','Day173_PlacesAndRegions_A2.html','🗺️','tiles',
  'Articles with countries: Thailand (no "the"), the Philippines (with "the").',
  [('nation','ประเทศชาติ','/ˈneɪʃn/','🏳️'),('capital','เมืองหลวง','/ˈkæpɪtl/','🏙️'),
   ('citizen','พลเมือง','/ˈsɪtɪzn/','🧑'),('border','ชายแดน','/ˈbɔːdə(r)/','🚧'),
   ('province','จังหวัด','/ˈprɒvɪns/','📍'),('heritage','มรดกวัฒนธรรม','/ˈherɪtɪdʒ/','💛'),
   ('anthem','เพลงชาติ','/ˈænθəm/','🎶')],
  "Thailand is a warm and friendly nation. Bangkok is the capital city. Every citizen learns the national anthem at school. The border in the north touches another country. Ben lives in a small province near the sea. Our heritage belongs to everyone, said the teacher. Each place has its own story.",
  ["Thailand is a warm and friendly nation.","Bangkok is the capital city.","Every citizen learns the anthem at school.","Ben lives in a small province near the sea.","Each place has its own story."],
  ["Bangkok is the capital city.","Ben lives in a small province near the sea.","Each place has its own story."],
  "Where does Ben live?","He lives in a small province near the sea."),

D(173,172,'Places and Regions','🗺️','Day174_AnimalsInDanger_A2.html','🐘','scramble',
  'Compass words: north, south, east, west.',
  [('region','ภูมิภาค','/ˈriːdʒən/','🧭'),('northern','ทางเหนือ','/ˈnɔːðən/','⬆️'),
   ('southern','ทางใต้','/ˈsʌðən/','⬇️'),('tropical','เขตร้อน','/ˈtrɒpɪkl/','🌴'),
   ('climate','ภูมิอากาศ','/ˈklaɪmət/','🌡️'),('plain','ที่ราบ','/pleɪn/','🏞️'),
   ('vast','กว้างใหญ่','/vɑːst/','🏔️')],
  "Our country has four main region. The northern hills are cool in winter. The southern islands are famous for beaches. Thailand has a tropical climate all year. Rice grows well on the wide plain. The sea looks vast from the shore. Every region has different food!",
  ["Our country has four main region.","The northern hills are cool in winter.","The southern islands are famous for beaches.","Thailand has a tropical climate.","Every region has different food."],
  ["The northern hills are cool in winter.","Thailand has a tropical climate.","Every region has different food."],
  "What is the climate of Thailand?","It has a tropical climate."),

D(174,173,'Animals in Danger','🐘','Day175_AHomeForEveryPet_A2.html','🐕','memory',
  'Present perfect with "since": Numbers have fallen since 1990.',
  [('species','สายพันธุ์','/ˈspiːʃiːz/','🦜'),('endangered','ใกล้สูญพันธุ์','/ɪnˈdeɪndʒəd/','⚠️'),
   ('habitat','ถิ่นอาศัย','/ˈhæbɪtæt/','🌳'),('hunt','ล่า','/hʌnt/','🏹'),
   ('rescue','ช่วยชีวิต','/ˈreskjuː/','🚁'),('reserve','เขตอนุรักษ์','/rɪˈzɜːv/','🛖'),
   ('survive','อยู่รอด','/səˈvaɪv/','💪')],
  "Many species are in trouble today. The wild elephant is an endangered animal. Its habitat is getting smaller every year. People must not hunt them for money. A special team works to rescue hurt animals. They live safely in a big reserve. Together we can help them survive.",
  ["Many species are in trouble today.","The wild elephant is an endangered animal.","Its habitat is getting smaller.","A special team works to rescue hurt animals.","Together we can help them survive."],
  ["The wild elephant is an endangered animal.","A special team works to rescue hurt animals.","Together we can help them survive."],
  "Why is the elephant endangered?","Because its habitat is getting smaller."),

D(175,174,'A Home for Every Pet','🐕','Day176_PeaceAndKindness_A2.html','🕊️','wordsearch',
  'Verbs + to: decide to, promise to, agree to.',
  [('adopt','รับมาเลี้ยง','/əˈdɒpt/','🏡'),('shelter','ที่พักพิงสัตว์','/ˈʃeltə(r)/','🏘️'),
   ('paw','อุ้งเท้า','/pɔː/','🐾'),('fur','ขนสัตว์','/fɜː(r)/','🧸'),
   ('stray','สัตว์จรจัด','/streɪ/','🐈'),('vet','สัตวแพทย์','/vet/','🩺'),
   ('devoted','ทุ่มเท ผูกพัน','/dɪˈvəʊtɪd/','❤️')],
  "The family decided to adopt a dog. They went to the animal shelter on Sunday. A brown puppy put one paw on Ben's hand. Its fur was very soft. He used to be a stray on the street. The vet checked him carefully. A rescued dog is the most devoted friend.",
  ["The family decided to adopt a dog.","They went to the animal shelter.","A brown puppy put one paw on Ben's hand.","He used to be a stray on the street.","A rescued dog is the most devoted friend."],
  ["They went to the animal shelter.","He used to be a stray on the street.","A rescued dog is the most devoted friend."],
  "Where did the family go on Sunday?","They went to the animal shelter."),

D(176,175,'Peace and Kindness','🕊️','Day177_OneWorld_A2.html','🌍','vowels',
  'Why / because for reasons: Why do we help? Because everyone matters.',
  [('peace','สันติภาพ','/piːs/','🕊️'),('conflict','ความขัดแย้ง','/ˈkɒnflɪkt/','⚡'),
   ('solve','แก้ปัญหา','/sɒlv/','🔑'),('unite','รวมเป็นหนึ่ง','/juˈnaɪt/','🤝'),
   ('embrace','โอบรับ','/ɪmˈbreɪs/','🫶'),('difference','ความแตกต่าง','/ˈdɪfrəns/','🎨'),
   ('calmly','อย่างใจเย็น','/ˈkɑːmli/','🧘')],
  "Peace begins in a small classroom. When a conflict starts, do not shout. Talk calmly and try to solve it. Words can unite people faster than anger. We must embrace every difference. Some children speak another language at home. That difference makes our class richer.",
  ["Peace begins in a small classroom.","When a conflict starts, do not shout.","Talk calmly and try to solve it.","We must embrace every difference.","That difference makes our class richer."],
  ["When a conflict starts, do not shout.","We must embrace every difference.","That difference makes our class richer."],
  "What should you do when a conflict starts?","Talk calmly and try to solve it."),

D(177,176,'One World','🌍','Day178_Week28Review_A2.html','⭐','tiles',
  'Everyone / everybody + singular verb: Everyone has a part to play.',
  [('global','ระดับโลก','/ˈɡləʊbl/','🌐'),('connect','เชื่อมโยง','/kəˈnekt/','🔗'),
   ('share','แบ่งปัน','/ʃeə(r)/','💡'),('worldwide','ทั่วโลก','/ˌwɜːldˈwaɪd/','🗺️'),
   ('citizenship','ความเป็นพลเมือง','/ˈsɪtɪzənʃɪp/','🎗️'),('generation','คนรุ่นต่อไป','/ˌdʒenəˈreɪʃn/','🚀'),
   ('together','ด้วยกัน','/təˈɡeðə(r)/','🫂')],
  "The internet can connect a child in Thailand with a child in Peru. Global problems need global answers. Students share ideas in an online club. Clean air is a worldwide need. Good citizenship starts with small daily choices. The world belongs to your generation. We are stronger together!",
  ["The internet can connect children everywhere.","Global problems need global answers.","Clean air is a worldwide need.","The world belongs to your generation.","We are stronger together."],
  ["Global problems need global answers.","The world belongs to your generation.","We are stronger together."],
  "What do global problems need?","They need global answers."),

D(179,178,'Look How Far','🎓','Day180_ReadyForB1_A2.html','🚀','scramble',
  'Present perfect for achievement: You have learned nine hundred words!',
  [('graduate','จบการศึกษา','/ˈɡrædʒueɪt/','🎓'),('certificate','ใบประกาศ','/səˈtɪfɪkət/','📜'),
   ('mentor','ผู้ชี้แนะ','/ˈmentɔː(r)/','🧑‍🏫'),('inspire','สร้างแรงบันดาลใจ','/ɪnˈspaɪə(r)/','✨'),
   ('potential','ศักยภาพ','/pəˈtenʃl/','🌱'),('achievement','ความสำเร็จ','/əˈtʃiːvmənt/','🏆'),
   ('onward','มุ่งไปข้างหน้า','/ˈɒnwəd/','➡️')],
  "Today the A2 students graduate together. Each child received a colourful certificate. Our teacher was a patient mentor all year. Her words inspire us every day. You have so much potential, she said. Look at this achievement: nine hundred words! Onward to the next level, everyone.",
  ["Today the A2 students graduate together.","Each child received a colourful certificate.","Our teacher was a patient mentor.","You have so much potential, she said.","Onward to the next level, everyone."],
  ["Each child received a colourful certificate.","You have so much potential, she said.","Onward to the next level, everyone."],
  "What did each child receive?","Each child received a colourful certificate.", 'Special'),

D(180,179,'Ready for B1','🚀','../dashboard.html','🏠','memory',
  'Looking ahead: At B1 you will read longer stories and give opinions.',
  [('beyond','เลยไปกว่านั้น','/bɪˈjɒnd/','🌠'),('intermediate','ระดับกลาง','/ˌɪntəˈmiːdiət/','📶'),
   ('opinion','ความคิดเห็น','/əˈpɪnjən/','💭'),('express','แสดงออก','/ɪkˈspres/','🗣️'),
   ('paragraph','ย่อหน้า','/ˈpærəɡrɑːf/','📝'),('fluency','ความคล่อง','/ˈfluːənsi/','🌊'),
   ('expedition','การเดินทางสำรวจ','/ˌekspəˈdɪʃn/','🧭')],
  "A2 is finished but the road goes beyond. Level seven begins the intermediate stage. Soon you will give your own opinion in English. You will express ideas in a full paragraph. Fluency grows a little every single day. Keep listening, keep speaking. Your expedition goes on!",
  ["A2 is finished but the road goes beyond.","Level seven begins the intermediate stage.","Soon you will give your own opinion.","Fluency grows a little every day.","Your expedition goes on."],
  ["Level seven begins the intermediate stage.","Fluency grows a little every day.","Your expedition goes on."],
  "What begins at level seven?","The intermediate stage begins.", 'Special'),
]
for d in W:
    out = build(d)
    fn = 'Day%d_%s_A2.html' % (d['n'], d['title'].replace(' ','').replace("'",''))
    open(OUT+fn,'w',encoding='utf-8').write(out)
    print('OK', fn)
