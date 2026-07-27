# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0,os.path.dirname(__file__))
from golden_generator import build
OUT='/sessions/wonderful-magical-bohr/mnt/English/Level4/'
def D(n,prev,title,emoji,nf,ne,game,grammar,words,story,ss,ds,tq,ta):
    return dict(n=n,prev=prev,level=4,cefr='A2',title=title,emoji=emoji,theme='Friends',
        next_file=nf,next_emoji=ne,game=game,grammar=grammar,words=words,story=story,ss=ss,ds=ds,
        think_q=tq,think_a=ta)
W=[
D(98,97,'A New Friend','🤝','Day99_SharingIsCaring_A2.html','🎁','scramble',
  'Past tense: meet becomes met (irregular verb).',
  [('shy','ขี้อาย','/ʃaɪ/','😳'),('nervous','ประหม่า','/ˈnɜːvəs/','😰'),('greet','ทักทาย','/ɡriːt/','👋'),('polite','สุภาพ','/pəˈlaɪt/','🙇'),('invite','เชิญ','/ɪnˈvaɪt/','💌'),('include','ให้เข้าร่วม','/ɪnˈkluːd/','🫂'),('confident','มั่นใจ','/ˈkɒnfɪdənt/','💪')],
  "A new boy came to school. He looked shy and nervous. Leo walked over and greeted him with a smile. Hello! My name is Leo. The boy said hello in a polite voice. His name was Ben. Mimi invited Ben to play with them. They always include everyone. Soon Ben felt confident and happy!",
  ["A new boy came to school.","He looked shy and nervous.","Leo greeted him with a smile.","Mimi invited Ben to play.","Soon Ben felt confident."],
  ["He looked shy and nervous.","Leo greeted him with a smile.","Soon Ben felt confident."],
  "How did the new boy feel at first?","He felt shy and nervous."),
D(99,98,'Sharing is Caring','🎁','Day100_SayingSorry_A2.html','🙏','memory',
  'Past tense: give becomes gave (irregular verb).',
  [('kindness','ความเมตตา','/ˈkaɪndnəs/','💗'),('generous','ใจกว้าง','/ˈdʒenərəs/','🎁'),('selfish','เห็นแก่ตัว','/ˈselfɪʃ/','🙅'),('accept','ยอมรับ','/əkˈsept/','🤲'),('refuse','ปฏิเสธ','/rɪˈfjuːz/','🚫'),('grateful','รู้สึกขอบคุณ','/ˈɡreɪtfl/','🙏'),('praise','ชมเชย','/preɪz/','👏')],
  "Ben had only one cake. He gave half to Mimi. That was very generous! Kindness makes friends happy, said Leo. Do not be selfish, share what you have. Mimi accepted the cake and felt grateful. She did not refuse. Thank you, Ben! The teacher gave him praise for his kind heart.",
  ["Ben had only one cake.","He gave half to Mimi.","Kindness makes friends happy.","Mimi felt grateful.","The teacher gave him praise."],
  ["He gave half to Mimi.","Mimi felt grateful.","The teacher gave him praise."],
  "What did Ben do with his cake?","He gave half to Mimi."),
D(100,99,'Saying Sorry','🙏','Day101_BestFriends_A2.html','👫','wordsearch',
  'Past tense: break becomes broke (irregular verb).',
  [('argue','เถียงกัน','/ˈɑːɡjuː/','😤'),('quarrel','ทะเลาะ','/ˈkwɒrəl/','💢'),('blame','โทษ','/bleɪm/','👉'),('apologize','ขอโทษ','/əˈpɒlədʒaɪz/','🙇'),('forgive','ให้อภัย','/fəˈɡɪv/','🕊️'),('honest','ซื่อสัตย์','/ˈɒnɪst/','✋'),('comfort','ปลอบใจ','/ˈkʌmfət/','🤗')],
  "Leo and Ben began to argue about a game. It turned into a quarrel. Ben broke Leo's pencil by mistake. Do not blame him, said Mimi. It was an accident. Ben was honest and said, I am sorry. He apologized. Leo decided to forgive him. Mimi hugged them both to comfort them. Friends again!",
  ["Leo and Ben began to argue.","Ben broke Leo's pencil.","Ben apologized to Leo.","Leo decided to forgive him.","Friends again!"],
  ["Ben broke Leo's pencil.","Ben apologized to Leo.","Leo decided to forgive him."],
  "What did Ben do after the quarrel?","He apologized to Leo."),
D(101,100,'Best Friends','👫','Day102_HelpingOthers_A2.html','🫶','vowels',
  'Past tense: keep becomes kept (irregular verb).',
  [('trust','ไว้ใจ','/trʌst/','🤝'),('secret','ความลับ','/ˈsiːkrət/','🤫'),('loyal','ซื่อตรง','/ˈlɔɪəl/','🛡️'),('promise','สัญญา','/ˈprɒmɪs/','🤞'),('respect','เคารพ','/rɪˈspekt/','🙌'),('jealous','อิจฉา','/ˈdʒeləs/','😒'),('sincere','จริงใจ','/sɪnˈsɪə/','💖')],
  "Mimi told Leo a secret. She knew she could trust him. Leo kept the promise and told nobody. A loyal friend is a treasure! Sometimes Ben felt jealous when they played alone. But Leo said, We respect you too. Come and join us! Their words were sincere. True friends always include each other.",
  ["Mimi told Leo a secret.","She knew she could trust him.","Leo kept the promise.","Ben felt jealous sometimes.","True friends respect each other."],
  ["She knew she could trust him.","Leo kept the promise.","True friends respect each other."],
  "Why could Mimi tell Leo her secret?","Because she could trust him."),
D(102,101,'Helping Others','🫶','Day103_KindWords_A2.html','💬','tiles',
  'Past tense: help becomes helped (add -ed).',
  [('support','สนับสนุน','/səˈpɔːt/','🤲'),('encourage','ให้กำลังใจ','/ɪnˈkʌrɪdʒ/','📣'),('advice','คำแนะนำ','/ədˈvaɪs/','💡'),('gentle','อ่อนโยน','/ˈdʒentl/','🕊️'),('patient','อดทน','/ˈpeɪʃnt/','⏳'),('understand','เข้าใจ','/ˌʌndəˈstænd/','🧠'),('humble','ถ่อมตัว','/ˈhʌmbl/','🙇')],
  "Ben could not finish his homework. Leo helped him and gave good advice. Do not worry, we will support you! Mimi was patient and gentle. She explained it again slowly. Now I understand! said Ben happily. Leo did not brag. He stayed humble. Friends encourage each other every day.",
  ["Ben could not finish his homework.","Leo helped him with advice.","Mimi was patient and gentle.","Now I understand! said Ben.","Friends encourage each other."],
  ["Leo helped him with advice.","Mimi was patient and gentle.","Friends encourage each other."],
  "Who helped Ben with his homework?","Leo helped him."),
D(103,102,'Kind Words','💬','Day104_Week18Review_A2.html','⭐','scramble',
  'Past tense: say becomes said (irregular verb).',
  [('compliment','คำชม','/ˈkɒmplɪmənt/','🌟'),('tease','ล้อเล่น','/tiːz/','😜'),('listener','ผู้ฟังที่ดี','/ˈlɪsənə/','👂'),('apart','แยกจากกัน','/əˈpɑːt/','↔️'),('reunion','การกลับมาพบกัน','/riːˈjuːniən/','🎊'),('exclude','กีดกัน','/ɪkˈskluːd/','🚷'),('humor','อารมณ์ขัน','/ˈhjuːmə/','😄')],
  "Mimi gave Ben a nice compliment about his drawing. Never tease your friends in a mean way, she said. Leo is a good listener. He listens with care. Last year Ben moved apart from his old friends. Their reunion was full of joy! Never exclude anyone. A little humor makes everyone smile.",
  ["Mimi gave Ben a compliment.","Never tease your friends.","Leo is a good listener.","Their reunion was full of joy.","A little humor makes everyone smile."],
  ["Never tease your friends.","Leo is a good listener.","A little humor makes everyone smile."],
  "What did Mimi give Ben?","She gave him a nice compliment."),
]
for d in W:
    out=build(d)
    fn='Day%d_%s_A2.html'%(d['n'],d['title'].replace(' ','').replace("'",''))
    open(OUT+fn,'w',encoding='utf-8').write(out)
    leak=out.count('Day 61')+out.count('wla_d61')+out.count('Happy Feelings')
    print('%s %s leak=%d'%('✅' if leak==0 else '⚠️',fn,leak))
