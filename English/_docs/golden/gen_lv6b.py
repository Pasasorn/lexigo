# -*- coding: utf-8 -*-
# Level 6 · Week 26 Arts & Media (158–164) · Week 27 Online World (165–171) · A2
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from golden_generator import build
OUT = '/sessions/wonderful-magical-bohr/mnt/English/Level6/'

def D(n, prev, title, emoji, nf, ne, game, grammar, words, story, ss, ds, tq, ta, theme='Media'):
    return dict(n=n, prev=prev, level=6, cefr='A2', title=title, emoji=emoji, theme=theme,
                next_file=nf, next_emoji=ne, game=game, grammar=grammar, words=words, story=story,
                ss=ss, ds=ds, think_q=tq, think_a=ta)

W = [
D(158,157,'Theatre Club','🎭','Day159_OnTelevision_A2.html','📺','tiles',
  'Past continuous: While we were rehearsing, the lights went out.',
  [('theatre','โรงละคร','/ˈθɪətə(r)/','🎭'),('script','บทละคร','/skrɪpt/','📜'),
   ('character','ตัวละคร','/ˈkærəktə(r)/','🧑‍🎤'),('scene','ฉาก','/siːn/','🖼️'),
   ('director','ผู้กำกับ','/dəˈrektə(r)/','🎬'),('applause','เสียงปรบมือ','/əˈplɔːz/','👏'),
   ('anxious','กังวล','/ˈæŋkʃəs/','😬')],
  "The school theatre was full of people. Mimi read her script one more time. Her character was a brave village girl. The first scene took place in a forest. Our director counted down from five. Mimi felt anxious before she walked out. At the end the applause was very loud!",
  ["The school theatre was full of people.","Mimi read her script one more time.","The first scene took place in a forest.","Mimi felt anxious before she walked out.","At the end the applause was very loud."],
  ["Mimi read her script one more time.","Mimi felt anxious before she walked out.","At the end the applause was very loud."],
  "Who was Mimi's character?","She was a brave village girl."),

D(159,158,'On Television','📺','Day160_ReadingTheNews_A2.html','📰','scramble',
  'Used to: I used to watch cartoons every morning.',
  [('channel','ช่อง','/ˈtʃænl/','📡'),('programme','รายการ','/ˈprəʊɡræm/','🗓️'),
   ('broadcast','ออกอากาศ','/ˈbrɔːdkɑːst/','📶'),('interview','สัมภาษณ์','/ˈɪntəvjuː/','🎙️'),
   ('advert','โฆษณา','/ˈædvɜːt/','📢'),('remote','รีโมต','/rɪˈməʊt/','🎛️'),
   ('viewer','ผู้ชมทางบ้าน','/ˈvjuːə(r)/','🛋️')],
  "Dad changed the channel with the remote. This programme is my favourite, said Ben. It is broadcast live every Saturday. A famous chef gave a short interview. Then a long advert began. I used to watch cartoons every morning, said Leo. Every viewer at home learned something new.",
  ["Dad changed the channel with the remote.","This programme is my favourite.","It is broadcast live every Saturday.","A famous chef gave a short interview.","Every viewer learned something new."],
  ["This programme is my favourite.","It is broadcast live every Saturday.","Every viewer learned something new."],
  "How often is the programme broadcast?","It is broadcast every Saturday."),

D(160,159,'Reading the News','📰','Day161_SendAMessage_A2.html','📨','memory',
  'Passive voice (simple): The story was written by a journalist.',
  [('headline','พาดหัวข่าว','/ˈhedlaɪn/','🗞️'),('article','บทความ','/ˈɑːtɪkl/','📄'),
   ('journalist','นักข่าว','/ˈdʒɜːnəlɪst/','🕵️'),('report','รายงาน','/rɪˈpɔːt/','📝'),
   ('source','แหล่งข้อมูล','/sɔːs/','🔗'),('rumour','ข่าวลือ','/ˈruːmə(r)/','🌀'),
   ('verify','ตรวจสอบให้แน่ใจ','/ˈverɪfaɪ/','🔍')],
  "Leo read the big headline on the front page. The article was written by a young journalist. She wrote a careful report about the flood. Always check the source, said the teacher. A rumour spreads faster than the truth. We must verify a story before we share it. Good readers ask questions.",
  ["Leo read the big headline.","The article was written by a journalist.","She wrote a careful report about the flood.","Always check the source, said the teacher.","We must verify a story before we share it."],
  ["Leo read the big headline.","Always check the source, said the teacher.","We must verify a story before we share it."],
  "What must we do before we share a story?","We must verify it."),

D(161,160,'Send a Message','📨','Day162_BeingSafeOnline_A2.html','🔒','wordsearch',
  'Phrasal verbs: log in, log out, sign up.',
  [('message','ข้อความ','/ˈmesɪdʒ/','💬'),('reply','ตอบกลับ','/rɪˈplaɪ/','↩️'),
   ('attach','แนบไฟล์','/əˈtætʃ/','📎'),('delete','ลบ','/dɪˈliːt/','🗑️'),
   ('download','ดาวน์โหลด','/ˌdaʊnˈləʊd/','⬇️'),('upload','อัปโหลด','/ˌʌpˈləʊd/','⬆️'),
   ('notification','การแจ้งเตือน','/ˌnəʊtɪfɪˈkeɪʃn/','🔔')],
  "Mimi sent a short message to her cousin. She waited for a reply all evening. Ben knows how to attach a photo. Please delete the old files, said Dad. Leo will download the homework sheet. Then he will upload his finished work. A small notification appeared on the screen.",
  ["Mimi sent a short message to her cousin.","She waited for a reply all evening.","Ben knows how to attach a photo.","Leo will download the homework sheet.","A small notification appeared."],
  ["She waited for a reply all evening.","Leo will download the homework sheet.","A small notification appeared."],
  "What did Mimi wait for?","She waited for a reply."),

D(162,161,'Being Safe Online','🔒','Day163_ScreenBalance_A2.html','⏳','vowels',
  'Never / always with advice: Never share your password.',
  [('profile','โปรไฟล์','/ˈprəʊfaɪl/','🪪'),('privacy','ความเป็นส่วนตัว','/ˈprɪvəsi/','🛡️'),
   ('username','ชื่อผู้ใช้','/ˈjuːzəneɪm/','🔤'),('stranger','คนแปลกหน้า','/ˈstreɪndʒə(r)/','❓'),
   ('restrict','จำกัดการเข้าถึง','/rɪˈstrɪkt/','⛔'),('alert','แจ้งเตือน','/əˈlɜːt/','🚨'),
   ('secure','ปลอดภัย','/sɪˈkjʊə(r)/','🔐')],
  "Keep your profile private, said the teacher. Privacy is very important online. Choose a username that is not your real name. Never talk to a stranger on the internet. If someone is rude, restrict that person. Then alert an adult you trust. A strong password keeps your account secure.",
  ["Keep your profile private, said the teacher.","Privacy is very important online.","Never talk to a stranger on the internet.","If someone is rude, restrict that person.","A strong password keeps your account secure."],
  ["Privacy is very important online.","If someone is rude, restrict that person.","A strong password keeps your account secure."],
  "What should you do if someone is rude?","You should restrict that person."),

D(163,162,'Screen Balance','⏳','Day164_Week26Review_A2.html','⭐','tiles',
  'Too much / not enough: too much screen time, not enough sleep.',
  [('limit','ขีดจำกัด','/ˈlɪmɪt/','🚧'),('device','อุปกรณ์','/dɪˈvaɪs/','📱'),
   ('outdoor','กลางแจ้ง','/ˌaʊtˈdɔː(r)/','🌳'),('restless','อยู่ไม่สุข','/ˈrestləs/','😑'),
   ('creative','สร้างสรรค์','/kriˈeɪtɪv/','🎨'),('offline','ออฟไลน์','/ˌɒfˈlaɪn/','🔌'),
   ('mindful','รู้ตัว','/ˈmaɪndfl/','🧘')],
  "Mum set a daily limit for every device. Too much screen time is not healthy. Go and play an outdoor game instead! At first Ben felt restless. Then he became more creative with his drawings. One offline hour every evening is our rule. Be mindful of how you spend your time.",
  ["Mum set a daily limit for every device.","Too much screen time is not healthy.","Go and play an outdoor game instead.","Then he became more creative.","Be mindful of how you spend your time."],
  ["Too much screen time is not healthy.","Then he became more creative.","Be mindful of how you spend your time."],
  "What is their evening rule?","One offline hour every evening."),
]
for d in W:
    out = build(d)
    fn = 'Day%d_%s_A2.html' % (d['n'], d['title'].replace(' ','').replace("'",''))
    open(OUT+fn,'w',encoding='utf-8').write(out)
    print('OK', fn)
