# -*- coding: utf-8 -*-
# Level 6 · Week 27 Character & Values (165–171) · Week 28 Our World (172–178) + 179–180 · A2 จบ
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from golden_generator import build
OUT = '/sessions/wonderful-magical-bohr/mnt/English/Level6/'

def D(n, prev, title, emoji, nf, ne, game, grammar, words, story, ss, ds, tq, ta, theme='Values'):
    return dict(n=n, prev=prev, level=6, cefr='A2', title=title, emoji=emoji, theme=theme,
                next_file=nf, next_emoji=ne, game=game, grammar=grammar, words=words, story=story,
                ss=ss, ds=ds, think_q=tq, think_a=ta)

W = [
D(165,164,'Be Honest','💎','Day166_BeBrave_A2.html','🦁','tiles',
  'Second conditional: If I found a wallet, I would return it.',
  [('honesty','ความซื่อสัตย์','/ˈɒnəsti/','💎'),('truth','ความจริง','/truːθ/','🕯️'),
   ('admit','ยอมรับ','/ədˈmɪt/','🙋'),('excuse','ข้ออ้าง','/ɪkˈskjuːs/','🙅'),
   ('cheat','โกง','/tʃiːt/','🚫'),('conscience','มโนธรรม','/ˈkɒnʃəns/','🫀'),
   ('genuine','จริงแท้','/ˈdʒenjuɪn/','🤍')],
  "Honesty is worth more than gold. Ben always tells the truth even when it is hard. Yesterday he broke a cup and went to admit it. He did not make an excuse. Never cheat in a test, said the teacher. Your conscience will feel heavy. A genuine apology fixes almost everything.",
  ["Honesty is worth more than gold.","Ben always tells the truth.","He went to admit it.","He did not make an excuse.","A genuine apology fixes almost everything."],
  ["Ben always tells the truth.","He did not make an excuse.","A genuine apology fixes almost everything."],
  "What did Ben do after he broke the cup?","He went to admit it."),

D(166,165,'Be Brave','🦁','Day167_BeFair_A2.html','⚖️','scramble',
  'Even though / although: Although he was afraid, he tried.',
  [('courage','ความกล้าหาญ','/ˈkʌrɪdʒ/','🦁'),('fearful','หวาดกลัว','/ˈfɪəfl/','😨'),
   ('attempt','พยายามทำ','/əˈtempt/','🎯'),('overcome','เอาชนะ','/ˌəʊvəˈkʌm/','⛰️'),
   ('bold','กล้า','/bəʊld/','⚡'),('shield','ปกป้อง','/ʃiːld/','🛡️'),
   ('hero','วีรบุรุษ','/ˈhɪərəʊ/','🦸')],
  "Courage does not mean you are never fearful. Mimi felt fearful near deep water. Although she was scared, she made one attempt. Slowly she began to overcome her fear. A bold heart grows a little every day. Real courage is to shield someone weaker. You do not need a cape to be a hero.",
  ["Courage does not mean you are never fearful.","Mimi felt fearful near deep water.","She made one attempt.","Slowly she began to overcome her fear.","You do not need a cape to be a hero."],
  ["Mimi felt fearful near deep water.","Slowly she began to overcome her fear.","You do not need a cape to be a hero."],
  "What made Mimi feel fearful?","Deep water made her feel fearful."),

D(167,166,'Be Fair','⚖️','Day168_BeGrateful_A2.html','🙏','memory',
  'Comparatives with "as ... as": as fair as, not as easy as.',
  [('fairness','ความยุติธรรม','/ˈfeənəs/','⚖️'),('equal','เท่าเทียม','/ˈiːkwəl/','🟰'),
   ('rotation','การผลัดเปลี่ยน','/rəʊˈteɪʃn/','🔁'),('unfair','ไม่ยุติธรรม','/ˌʌnˈfeə(r)/','😠'),
   ('agree','เห็นด้วย','/əˈɡriː/','🤝'),('settle','ยุติข้อขัดแย้ง','/ˈsetl/','🕊️'),
   ('referee','กรรมการ','/ˌrefəˈriː/','📕')],
  "Fairness makes every game more fun. Each player must get an equal chance. Follow the rotation, said Leo. It is unfair to jump the line. The two boys did not agree at first. Then they asked the referee together. That helped them settle the problem in one minute.",
  ["Fairness makes every game more fun.","Each player must get an equal chance.","Follow the rotation, said Leo.","It is unfair to jump the line.","They asked the referee together."],
  ["Each player must get an equal chance.","It is unfair to jump the line.","They asked the referee together."],
  "Who helped the boys settle the problem?","They asked the referee together."),

D(168,167,'Be Grateful','🙏','Day169_HelpingHands_A2.html','🤲','wordsearch',
  'Thanking: Thank you for helping me. I appreciate it.',
  [('gratitude','ความกตัญญู','/ˈɡrætɪtjuːd/','🙏'),('appreciate','ซาบซึ้ง','/əˈpriːʃieɪt/','💖'),
   ('blessing','สิ่งดีที่ได้รับ','/ˈblesɪŋ/','🍀'),('modest','ถ่อมตน','/ˈmɒdɪst/','🌾'),
   ('credit','การให้เครดิต','/ˈkredɪt/','🌟'),('lowly','ถ่อมตัว','/ˈləʊli/','🪷'),
   ('recall','นึกถึง','/rɪˈkɔːl/','🧠')],
  "Gratitude turns what we have into enough. Mimi wrote three things she appreciate each night. A warm home is a big blessing. Grandma stayed modest about her cooking prize. She likes to give credit to others instead. A lowly heart listens more than it speaks. Always recall who helped you.",
  ["Gratitude turns what we have into enough.","Mimi wrote three things she appreciate.","A warm home is a big blessing.","She likes to give credit to others instead.","Always recall who helped you."],
  ["A warm home is a big blessing.","She likes to give credit to others instead.","Always recall who helped you."],
  "What did Mimi write each night?","She wrote three things she appreciate."),

D(169,168,'Helping Hands','🤲','Day170_TeamSpirit_A2.html','🧑‍🤝‍🧑','vowels',
  'Offering help: Shall I help you? Would you like a hand?',
  [('responsible','มีความรับผิดชอบ','/rɪˈspɒnsəbl/','📋'),('duty','หน้าที่','/ˈdjuːti/','🎖️'),
   ('offer','เสนอ','/ˈɒfə(r)/','🫱'),('assist','ช่วยเหลือ','/əˈsɪst/','🤝'),
   ('elderly','ผู้สูงอายุ','/ˈeldəli/','👴'),('deliver','นำไปส่ง','/dɪˈlɪvə(r)/','🎒'),
   ('deed','การกระทำ','/diːd/','✨')],
  "Every child can be responsible at home. It is my duty to feed the cat, said Ben. On the bus Leo will offer his seat. Shall I assist you? he asked an elderly man. Mimi helped deliver two heavy bags. One small deed can change a whole day.",
  ["Every child can be responsible at home.","It is my duty to feed the cat.","On the bus Leo will offer his seat.","Mimi helped deliver two heavy bags.","One small deed can change a whole day."],
  ["It is my duty to feed the cat.","Mimi helped deliver two heavy bags.","One small deed can change a whole day."],
  "What did Leo do on the bus?","He offered his seat."),

D(170,169,'Team Spirit','🧑‍🤝‍🧑','Day171_Week27Review_A2.html','⭐','tiles',
  'Let us / shall we: Let us work together!',
  [('teamwork','การทำงานเป็นทีม','/ˈtiːmwɜːk/','🤜'),('captain','หัวหน้าทีม','/ˈkæptɪn/','🧢'),
   ('motivate','สร้างแรงจูงใจ','/ˈməʊtɪveɪt/','📣'),('cooperate','ร่วมมือ','/kəʊˈɒpəreɪt/','🔗'),
   ('victory','ชัยชนะ','/ˈvɪktəri/','🏅'),('defeat','ความพ่ายแพ้','/dɪˈfiːt/','😔'),
   ('spirit','จิตใจ','/ˈspɪrɪt/','🔥')],
  "Teamwork wins more games than talent. Leo is the captain of the small football team. He tries to motivate every player. Let us cooperate! he shouted. Their victory was very close. Last week they learned from a defeat too. Good spirit matters more than the score.",
  ["Teamwork wins more games than talent.","Leo is the captain of the team.","He tries to motivate every player.","Their victory was very close.","Good spirit matters more than the score."],
  ["Leo is the captain of the team.","Their victory was very close.","Good spirit matters more than the score."],
  "Who is the captain of the team?","Leo is the captain."),
]
for d in W:
    out = build(d)
    fn = 'Day%d_%s_A2.html' % (d['n'], d['title'].replace(' ','').replace("'",''))
    open(OUT+fn,'w',encoding='utf-8').write(out)
    print('OK', fn)
