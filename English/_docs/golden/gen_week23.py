# -*- coding: utf-8 -*-
# Level 5 · Week 23 — Shopping & Money (Day 135–141) · A2
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from golden_generator import build
OUT = '/sessions/wonderful-magical-bohr/mnt/English/Level5/'

def D(n, prev, title, emoji, nf, ne, game, grammar, words, story, ss, ds, tq, ta):
    return dict(n=n, prev=prev, level=5, cefr='A2', title=title, emoji=emoji, theme='Money',
                next_file=nf, next_emoji=ne, game=game, grammar=grammar, words=words, story=story,
                ss=ss, ds=ds, think_q=tq, think_a=ta)

W = [
D(135, 134, 'My Own Money', '👛', 'Day136_HowMuchIsIt_A2.html', '🏷️', 'tiles',
  'How much / how many: How much does it cost? How many coins do you have?',
  [('wallet','กระเป๋าสตางค์','/ˈwɒlɪt/','👛'),('purse','กระเป๋าเงินใบเล็ก','/pɜːs/','💼'),
   ('allowance','เงินค่าขนม','/əˈlaʊəns/','🧧'),('earn','หาเงินได้','/ɜːn/','💵'),
   ('jar','โหล','/dʒɑː(r)/','🫙'),('cost','ราคา','/kɒst/','🏷️'),
   ('afford','มีเงินพอซื้อ','/əˈfɔːd/','✅')],
  "Every Sunday Ben gets a small allowance. He keeps it in a brown wallet. Mimi uses a red purse instead. Last month Leo helped a neighbour and began to earn extra money. They put their coins in a glass jar. How much does the toy cost? I cannot afford it yet, said Ben.",
  ["Every Sunday Ben gets an allowance.","He keeps it in a brown wallet.","Leo began to earn extra money.","They put their coins in a glass jar.","I cannot afford it yet, said Ben."],
  ["He keeps it in a brown wallet.","They put their coins in a glass jar.","I cannot afford it yet."],
  "Where do they keep their coins?","They keep them in a glass jar."),

D(136, 135, 'How Much Is It?', '🏷️', 'Day137_AtTheCheckout_A2.html', '🛒', 'scramble',
  'Comparing prices: cheaper than / more expensive than.',
  [('expensive','แพง','/ɪkˈspensɪv/','💸'),('discount','ส่วนลด','/ˈdɪskaʊnt/','🔻'),
   ('label','ป้ายสินค้า','/ˈleɪbl/','🏷️'),('shelf','ชั้นวางของ','/ʃelf/','🗄️'),
   ('brand','ยี่ห้อ','/brænd/','®️'),('compare','เปรียบเทียบ','/kəmˈpeə(r)/','⚖️'),
   ('size','ขนาด','/saɪz/','📐')],
  "This bag looks very expensive, said Mimi. Read the label on the shelf first. Today there is a twenty percent discount! Always compare two things before you buy. This brand is cheaper than that one. Do they have my size? A wise shopper takes time to look.",
  ["This bag looks very expensive.","Read the label on the shelf first.","Today there is a twenty percent discount.","Always compare two things before you buy.","This brand is cheaper than that one."],
  ["Read the label on the shelf first.","Always compare two things before you buy.","This brand is cheaper than that one."],
  "What should you do before you buy?","You should compare two things."),

D(137, 136, 'At the Checkout', '🛒', 'Day138_SaveOrSpend_A2.html', '🐷', 'memory',
  'Polite queue language: Excuse me, is this the end of the line?',
  [('queue','เข้าแถว','/kjuː/','🚶'),('cashier','แคชเชียร์','/kæˈʃɪə(r)/','🧑‍💼'),
   ('scan','สแกน','/skæn/','📷'),('barcode','บาร์โค้ด','/ˈbɑːkəʊd/','▓'),
   ('receipt','ใบเสร็จ','/rɪˈsiːt/','🧾'),('refund','คืนเงิน','/ˈriːfʌnd/','↩️'),
   ('exchange','แลกเปลี่ยน','/ɪksˈtʃeɪndʒ/','🔄')],
  "They stood in a long queue at the shop. The cashier smiled at every customer. She began to scan each barcode quickly. Keep your receipt safely, she said. If something is broken you can ask for a refund. Or you can exchange it for a new one within seven days.",
  ["They stood in a long queue.","The cashier smiled at every customer.","She began to scan each barcode.","Keep your receipt safely.","You can ask for a refund."],
  ["The cashier smiled at every customer.","Keep your receipt safely.","You can ask for a refund."],
  "What can you do if something is broken?","You can ask for a refund."),

D(138, 137, 'Save or Spend?', '🐷', 'Day139_LendAndBorrow_A2.html', '🤝', 'wordsearch',
  'If + present, will + verb: If you save money, you will buy it soon.',
  [('budget','งบประมาณ','/ˈbʌdʒɪt/','📊'),('decide','ตัดสินใจ','/dɪˈsaɪd/','🗒️'),
   ('overspend','ใช้เงินเกินตัว','/ˌəʊvəˈspend/','🕳️'),('patience','ความอดทน','/ˈpeɪʃns/','⏳'),
   ('bonus','โบนัส','/ˈbəʊnəs/','🎁'),('total','ยอดรวม','/ˈtəʊtl/','🧮'),
   ('half','ครึ่งหนึ่ง','/hɑːf/','➗')],
  "Mimi wrote a simple budget in her notebook. I will decide carefully before I buy anything. Do not overspend on small toys. With patience, the bonus is bigger. She counted the total in her jar. Ben decided to keep half and use half. That is a smart choice!",
  ["Mimi wrote a simple budget.","I will decide carefully before I buy anything.","Do not overspend on small toys.","With patience, the bonus is bigger.","Ben decided to keep half."],
  ["Mimi wrote a simple budget.","Do not overspend on small toys.","Ben decided to keep half."],
  "What did Ben decide to do?","He decided to keep half and use half."),

D(139, 138, 'Lend and Borrow', '🤝', 'Day140_GivingBack_A2.html', '💝', 'vowels',
  'lend = give to someone. borrow = take from someone. Do not mix them up!',
  [('borrow','ยืม','/ˈbɒrəʊ/','🙏'),('lend','ให้ยืม','/lend/','🤲'),
   ('owe','ติดหนี้','/əʊ/','📝'),('return','คืน','/rɪˈtɜːn/','↩️'),
   ('repay','จ่ายคืน','/rɪˈpeɪ/','🤞'),('reliable','พึ่งพาได้','/rɪˈlaɪəbl/','✋'),
   ('worth','มีค่า','/wɜːθ/','🫱')],
  "Ben wanted to borrow twenty baht from Leo. Leo agreed to lend it to him. Now I owe you, said Ben. He agreed to repay it on Friday. A reliable friend always returns what he takes. A good name is worth more than money. On Friday Ben kept his word!",
  ["Ben wanted to borrow twenty baht.","Leo agreed to lend it to him.","He agreed to repay it on Friday.","A reliable friend always returns it.","A good name is worth more than money."],
  ["Leo agreed to lend it to him.","A reliable friend always returns it.","A good name is worth more than money."],
  "When did Ben agree to repay the money?","He agreed to repay it on Friday."),

D(140, 139, 'Giving Back', '💝', 'Day141_Week23Review_A2.html', '⭐', 'tiles',
  'Past tense: buy becomes bought, bring becomes brought.',
  [('donate','บริจาค','/dəʊˈneɪt/','🎗️'),('charity','การกุศล','/ˈtʃærəti/','💞'),
   ('collect','เก็บรวบรวม','/kəˈlekt/','📦'),('volunteer','อาสาสมัคร','/ˌvɒlənˈtɪə(r)/','🙋'),
   ('community','ชุมชน','/kəˈmjuːnəti/','🏘️'),('thoughtful','คิดถึงผู้อื่น','/ˈθɔːtfl/','🤗'),
   ('value','คุณค่า','/ˈvæljuː/','💎')],
  "The school asked every class to donate old books. Mimi brought five and Ben brought three. They collect them for a small charity. Leo signed up as a volunteer on Saturday. Our community becomes stronger when we help, said the teacher. A thoughtful heart has real value.",
  ["The school asked every class to donate books.","Mimi brought five and Ben brought three.","They collect them for a small charity.","Leo signed up as a volunteer.","A thoughtful heart has real value."],
  ["Mimi brought five and Ben brought three.","Leo signed up as a volunteer.","A thoughtful heart has real value."],
  "What did Leo do on Saturday?","He signed up as a volunteer."),
]
for d in W:
    out = build(d)
    fn = 'Day%d_%s_A2.html' % (d['n'], d['title'].replace(' ','').replace("'",'').replace('?',''))
    open(OUT+fn,'w',encoding='utf-8').write(out)
    print('OK', fn)
