---
widgets: [exam]
---

# 🎓 Yakuniy imtihon + sertifikat

!!! abstract "Qanday ishlaydi"
    Har bir urinishda **45 talik bankdan 20 ta tasodifiy savol** tushadi va
    javob variantlari ham aralashtiriladi — tartibni yodlash ish bermaydi.
    Mavzular: risk-menejment, hajm hisobi, xarajatlar, psixologiya, bozor
    mexanikasi. O'tish bali — **80%** (20 dan 16 ta). O'tsangiz —
    **shaxsiy PNG-sertifikat** olasiz, uni yuklab olish mumkin.

    Savollarning yarmidan ko'pi ta'rifni eslashga emas, hisoblash va
    vaziyatni tahlil qilishga qaratilgan. O'ta olmasangiz — imtihon qaysi
    mavzularni qayta o'qish kerakligini ko'rsatadi. Eng yaxshi natija
    brauzerda saqlanadi.

!!! warning "O'quv materiali — moliyaviy maslahat emas"
    To'g'ri javoblar risk-menejment tamoyillarini aks ettiradi, foydani
    kafolatlamaydi. Sertifikat o'quv kursini tugatganligini tasdiqlaydi, treyder
    malakasini emas.

---

<div class="exam-widget calc-widget" id="exam-widget">

  <div id="exam-start">
    <p class="exam-best" id="exam-best"></p>
    <label class="exam-name-label">
      Sertifikat uchun ism
      <input type="text" id="exam-name" maxlength="40" placeholder="Masalan, Alisher Karimov" autocomplete="name">
    </label>
    <button class="calc-button" id="exam-start-btn">▶ Imtihonni boshlash (45 ta savoldan 20 tasi)</button>
  </div>

  <div id="exam-play" style="display:none">
    <div class="exam-progress">
      <span id="exam-counter"></span>
      <span id="exam-score"></span>
    </div>
    <div class="exam-bar-track"><div class="exam-bar-fill" id="exam-bar"></div></div>
    <h3 class="exam-question" id="exam-question"></h3>
    <div class="exam-options" id="exam-options"></div>
    <div class="exam-explain" id="exam-explain" style="display:none"></div>
    <button class="calc-button" id="exam-next" style="display:none">Keyingisi →</button>
  </div>

  <div id="exam-result" style="display:none"></div>

  <div id="exam-cert-wrap" style="display:none">
    <canvas id="exam-cert" width="1000" height="700"></canvas>
    <button class="calc-button" id="exam-download-btn">⬇ Sertifikatni yuklab olish (PNG)</button>
  </div>
</div>

<script type="application/json" id="exam-questions">
[
  {
    "q": "Yangi boshlovchi uchun bitta savdodagi maksimal risk qancha bo'lishi oqilona?",
    "options": [
      "Depozitning 5–10% — aks holda hisob juda sekin o'sadi",
      "Depozitning 1–2%",
      "Signalga qanchalik ishonganingga bog'liq",
      "Oldingi zararni qoplaydigan darajada"
    ],
    "answer": 1,
    "explain": "Bitta savdoga 1–2%. 1% riskda ketma-ket 10 ta zarar ham hisobning atigi ~10% ini oladi va hisob seriyadan omon qoladi. «Ishonchga qarab» — bu risk-menejment emas: ishonchni o'lchab bo'lmaydi va u aynan eng yomon savdolar oldidan kuchayadi."
  },
  {
    "q": "Depozit $1000, risk 2%, EUR/USD bo'yicha stop 50 punkt. Hajm qancha?",
    "options": [
      "0.04 lot",
      "0.4 lot",
      "1.0 lot",
      "0.02 lot"
    ],
    "answer": 0,
    "explain": "$20 risk ÷ (50 punkt × lotiga $10) = 0.04 lot. Hajm riskdan va stop masofasidan kelib chiqadi, «ko'z bilan» tanlanmaydi."
  },
  {
    "q": "Depozit $2000, risk 1.5%, USD/JPY bo'yicha stop 30 punkt, kurs 150.00. Hajm qancha?",
    "options": [
      "0.10 lot",
      "0.20 lot",
      "0.15 lot",
      "0.015 lot"
    ],
    "answer": 2,
    "explain": "USD/JPY da punkt $10 EMAS: 0.01 × 100 000 = 1000 ¥ ÷ 150 = lotiga $6.67. $30 risk ÷ (30 × 6.67) = 0.15 lot. Odat bo'yicha $10 qo'ygan kishi 0.10 oladi va rejadagi $30 o'rniga atigi $20 risk qiladi."
  },
  {
    "q": "Depozit $500, yelka 1:100. EUR/USD bo'yicha 1.1000 da 0.5 lot ochmoqchisan. Qancha marja kerak?",
    "options": [
      "$55 — zaxirasi bilan yetadi",
      "$550 — depozit yetmaydi, savdo ochilmaydi",
      "$110",
      "$5.50"
    ],
    "answer": 1,
    "explain": "0.5 lot = 50 000 EUR ≈ $55 000. Marja = $55 000 ÷ 100 = $550, bu depozitdan ko'p. Yelka «pul bermaydi» — u pozitsiyaning qancha qismini muzlatish kerakligini belgilaydi."
  },
  {
    "q": "Stop 1.0950 da turgan edi, lekin pozitsiya 1.0938 da yopildi. Bu…",
    "options": [
      "Terminal xatosi — qayta o'rnatish kerak",
      "Brokerning aldashi, shikoyat yozish kerak",
      "Sirg'anish (slippage): stop — bu ishga tushirish narxi, ijro kafolati emas",
      "Imkonsiz, stop aynan darajada ijro etiladi"
    ],
    "answer": 2,
    "explain": "Oddiy stop darajaga tegishi bilan bozor orderiga aylanadi. Tez bozorda eng yaqin mavjud narx yomonroq bo'ladi. Shuning uchun haqiqiy zarar rejadagidan katta chiqishi mumkin — kafolatni faqat alohida «kafolatlangan stop» mahsuloti beradi."
  },
  {
    "q": "Ikkita $1000 lik hisob: birinchisida yelka 1:30, ikkinchisida 1:500. Ikkalasi ham 20 punktlik stop bilan 0.1 lot EUR/USD ochadi. Kimning puldagi riski katta?",
    "options": [
      "Bir xil — ikkalasida $20: riskni hajm va stop belgilaydi, yelka emas",
      "Ikkinchisiniki taxminan 16 barobar katta",
      "Ikkinchisiniki marja tufayli sal kattaroq",
      "Birinchisiniki — u ko'proq pul muzlatadi"
    ],
    "answer": 0,
    "explain": "0.1 lot × 20 punkt × $1 = ikkalasida ham $20. Yelka faqat garov hajmiga ta'sir qiladi ($367 va $22). Xavfli narsa — yelkaning o'zi emas, u ochishga imkon beradigan hajm."
  },
  {
    "q": "G'alaba ulushi 50%, o'rtacha yutuq 1.5R, o'rtacha zarar 1R, spred va komissiya har savdoda ≈0.1R oladi. Kutilma (EV) qancha?",
    "options": [
      "+0.25R",
      "+0.15R",
      "−0.10R",
      "+0.65R"
    ],
    "answer": 1,
    "explain": "0.5 × 1.5 − 0.5 × 1 − 0.1 = +0.15R. +0.25R faqat xarajatlarni unutgandagina chiqadi — «qog'ozda foydali» strategiya amalda aynan shu tarzda zararli bo'lib qoladi."
  },
  {
    "q": "Strategiya: g'alaba ulushi 90%, o'rtacha yutuq 0.1R, o'rtacha zarar 1R. Uzoq masofada u…",
    "options": [
      "Foydali — 10 tadan 9 tasi g'alaba",
      "Zararsiz (nol)",
      "Zararli: EV = har savdoda −0.01R",
      "Hajmni oshirsa foydali"
    ],
    "answer": 2,
    "explain": "0.9 × 0.1 − 0.1 × 1 = −0.01R. Kichkina teykli va katta stopli yuqori g'alaba ulushi — eng keng tarqalgan tuzoq: to'qqizta g'alaba bitta zararni qoplamaydi."
  },
  {
    "q": "R:R = 1:3. Zarar ko'rmaslik uchun minimal g'alaba ulushi qancha (xarajatlarsiz)?",
    "options": [
      "33%",
      "50%",
      "25%",
      "75%"
    ],
    "answer": 2,
    "explain": "Nolga chiqish ulushi = 1 ÷ (1 + 3) = 25%. 33% — bu 1:2 uchun javob, tez-tez chalkashtiriladi. R:R qanchalik yuqori bo'lsa, haq bo'lish shunchalik kam kerak."
  },
  {
    "q": "Spred 1.5 punkt, oyiga EUR/USD bo'yicha 0.1 lotdan 40 ta savdo. Oyiga spredga qancha ketadi?",
    "options": [
      "$6",
      "$1.50",
      "$600",
      "$60 — bu $1000 depozitning 6% i"
    ],
    "answer": 3,
    "explain": "1.5 × punktiga $1 (0.1 lot) × 40 = $60. $1000 lik hisobda bu oyiga faqat xarajatlarga 6% — strategiya senga ishlashdan oldin avval shuni qaytarishi kerak."
  },
  {
    "q": "Stop 10 punkt, spred 2 punkt. Spred riskning qancha ulushini yeydi?",
    "options": [
      "20%",
      "2%",
      "10%",
      "0.2%"
    ],
    "answer": 0,
    "explain": "2 ÷ 10 = riskning 20% i narx qimirlashidan oldin brokerga ketadi. Shuning uchun qisqa stoplar va skalping yangi boshlovchiga ko'ringanidan qimmatroq: stop qanchalik yaqin bo'lsa, undagi xarajat ulushi shunchalik katta."
  },
  {
    "q": "Odatda qaysi kuni uch karra svop hisoblanadi?",
    "options": [
      "Jumada",
      "Dushanbada",
      "Chorshanbada — dam olish kunlari hisob-kitobi unga o'tkaziladi",
      "Uch karra svop bo'lmaydi"
    ],
    "answer": 2,
    "explain": "Hisob-kitob T+2 sxemasi bo'yicha ketadi, shuning uchun hafta o'rtasidan o'tkazilgan pozitsiya svopni birdaniga uch kunga oladi. Chorshanbadan o'tkazsang — uch barobar to'laysan (yoki olasan)."
  },
  {
    "q": "1% riskdan uchta pozitsiya ochiq: long EUR/USD, long GBP/USD, short USD/CHF. Portfelning haqiqiy riski qancha?",
    "options": [
      "1% — risklar o'rtachalanadi",
      "≈1.7% — qisman diversifikatsiya",
      "≈3% — uchalasi ham dollarga qarshi bitta stavka",
      "Har biriga 0.33% dan"
    ],
    "answer": 2,
    "explain": "Uchta tiket, lekin stavka bitta: dollar pastga. Bitta kuchli dollar harakati uchala stopni birvarakayiga uradi. Riskni savdolar soni bilan emas, bitta bozor harakati nima qilishi bilan o'lcha."
  },
  {
    "q": "Hisob 30% yo'qotdi, keyin 30% ishladi. Boshlanishga nisbatan qayerda?",
    "options": [
      "Aynan boshlang'ich holatga qaytdi",
      "−9%",
      "−0.9%",
      "+9%"
    ],
    "answer": 1,
    "explain": "0.7 × 1.3 = 0.91, ya'ni −9%. Prosadka va tiklanish nosimmetrik: −50% dan keyin +100% kerak. Shuning uchun kapitalni himoya qilish daromad ortidan quvishdan muhimroq."
  },
  {
    "q": "50% g'alaba ulushida ketma-ket 5 ta zarar chiqdi. Matematika nima deydi?",
    "options": [
      "Strategiya buzilgan, uni almashtirish kerak",
      "Bozor o'zgargan",
      "Bu deyarli imkonsiz",
      "Bu normal: bunday seriya taxminan har 32 urinishda bir marta chiqadi"
    ],
    "answer": 3,
    "explain": "0.5⁵ = 3.1%, ya'ni taxminan 32 tadan 1 ta. Zarar seriyasining o'zi hech narsani isbotlamaydi — strategiyani besh savdo tufayli almashtirish uni shovqinga qarab almashtirish demakdir."
  },
  {
    "q": "20 ta savdo jami +6R berdi. Bu natija haqida nima deyish to'g'ri?",
    "options": [
      "Strategiya ustunligini isbotladi",
      "Riskni bemalol ikki barobar oshirsa bo'ladi",
      "Tanlanma kichik: tasodif ham shunday natijani taxminan 13% seriyada beradi",
      "G'alaba ulushi endi kafolatlangan holda saqlanadi"
    ],
    "answer": 2,
    "explain": "20 ta savdoda mahorat va omadni ajratib bo'lmaydi. O'z natijangni «Mahorat yoki omad» bo'limida tekshir — u tasodifiy seriyalarning qancha ulushi sennikidan yomon emasligini hisoblaydi."
  },
  {
    "q": "Kirish 1.1000, stop 1.0950, chiqish 1.1120 da. Bu necha R?",
    "options": [
      "+1.2R",
      "+2.4R",
      "+0.4R",
      "+120R"
    ],
    "answer": 1,
    "explain": "Risk = 50 punkt = 1R. Natija = 120 punkt = 120 ÷ 50 = +2.4R. Savdolarni dollarda emas, R da sanash — hajm har xil bo'lganda ularni solishtirishning yagona yo'li."
  },
  {
    "q": "Strategiya 1% riskda har savdoda +0.2R beradi, oyiga 8 ta savdo. Oyiga kutilayotgan daromad qancha?",
    "options": [
      "≈16%",
      "≈1.6%",
      "≈8%",
      "≈0.2%"
    ],
    "answer": 1,
    "explain": "0.2R × 1% × 8 = oyiga 1.6% — bu ishlaydigan strategiyada. Haqiqiy raqamlar zerikarli ko'rinadi; oyiga 30% va'da qilgan narsa daromadni emas, hisobni nolga tushirish riskini va'da qiladi."
  },
  {
    "q": "Kirishdan keyin darhol stopni zararsiz (breakeven) darajaga ko'chirish…",
    "options": [
      "Har doim to'g'ri qadam — savdo bepul bo'lib qoladi",
      "Riskni kamaytiradi, lekin bozor shovqinida ko'proq uchirib yuboradi: qoida oldindan yozilgan bo'lishi kerak",
      "Hech narsaga ta'sir qilmaydi",
      "O'rtacha yutuqni oshiradi"
    ],
    "answer": 1,
    "explain": "Bepul yaxshilanish bo'lmaydi: riskni olib tashlab, buning evaziga plyusga chiqishi mumkin bo'lgan savdolar ulushini to'laysan. Bu joiz qaror, lekin u qoidalarning bir qismi bo'lishi va tarixda tekshirilishi kerak — qo'rquvdan savdo o'rtasida qabul qilinmasligi kerak."
  },
  {
    "q": "Kunlik zarar limiti −2R tushlikkacha tugadi. Intizomli treyder nima qiladi?",
    "options": [
      "Limitni bitta katta savdo bilan qaytaradi",
      "Yarim hajmda savdoni davom ettiradi",
      "Ertagacha terminalni yopadi — limit shuning uchun qo'yilgan",
      "Limitni ertaga ko'chiradi va −4R gacha savdo qiladi"
    ],
    "answer": 2,
    "explain": "Surib qo'ysa bo'ladigan limit — limit emas, xohish. Yarim hajm oqilona eshitiladi, lekin bu ham o'sha qoidani aylanib o'tish — aynan limit tugagandan keyin qarorlar eng yomon bo'ladi."
  },
  {
    "q": "Stop Out Margin Call dan nimasi bilan farq qiladi?",
    "options": [
      "Margin Call pozitsiyalarni yopadi, Stop Out esa faqat ogohlantirish",
      "Bu bir xil narsa",
      "Margin Call — marja yetishmayotgani haqida ogohlantirish, Stop Out — broker tomonidan majburiy yopish",
      "Stop Out ni treyder qo'yadi, Margin Call ni broker"
    ],
    "answer": 2,
    "explain": "Avval Margin Call darajasi erkin marja kamayganini bildiradi. Zarar o'sishda davom etsa — Stop Out ishga tushadi va broker pozitsiyalarni o'zi, bozor narxida, sendan so'ramasdan yopadi."
  },
  {
    "q": "Yil bo'yicha: $3000 foyda, $1200 zarar. JShDS 12% — qancha to'lanadi (O'zbekiston rezidenti)?",
    "options": [
      "$360",
      "$216",
      "$144",
      "$0 — foreks soliqqa tortilmaydi"
    ],
    "answer": 1,
    "explain": "Yillik sof natija deklaratsiya qilinadi: ($3000 − $1200) × 12% = $216. $360 esa zararni ayirishni unutib, faqat foydadan hisoblaganda chiqadi. soliq.uz bilan solishtir — qoidalar o'zgaradi."
  },
  {
    "q": "0.01 lot EUR/USD — bu qancha valyuta va punkt qancha turadi?",
    "options": [
      "100 birlik, punkt ≈ $1",
      "10 000 birlik, punkt ≈ $1",
      "1 000 birlik, punkt ≈ $0.10",
      "1 000 birlik, punkt ≈ $1"
    ],
    "answer": 2,
    "explain": "Standart lot = 100 000 birlik, demak 0.01 lot = 1000 EUR, punkt esa $0.10 turadi. Mikrolot — birinchi real hisob uchun to'g'ri hajm."
  },
  {
    "q": "Stop 20 punkt, bir daqiqadan keyin NFP chiqadi. Aynan shu stop bilan nima noto'g'ri ketishi mumkin?",
    "options": [
      "Hech narsa — stop aynan 20 punkt zararni kafolatlaydi",
      "Narx sakrashi stopni darajadan yomonroqda ijro etadi va zarar rejadan katta bo'ladi",
      "Stop avtomatik bekor bo'ladi",
      "Broker stopni sen uchun kengaytiradi"
    ],
    "answer": 1,
    "explain": "Yangilik chiqishida kotirovka darajalar ustidan sakraydi va spred kengayadi. Stop birinchi mavjud narxda ishlaydi — ba'zan darajadan ancha uzoqda. Yangi boshlovchiga chiqishni kutib turish bunday ijroga to'lashdan arzonroq."
  },
  {
    "q": "Ikki treyder EV +0.2R bo'lgan bitta strategiyada ishlaydi. Birinchisi har savdoda 1%, ikkinchisi 10% risk qiladi. 200 ta savdodan keyin…",
    "options": [
      "Ikkinchisi aynan 10 barobar ko'p ishlaydi",
      "Natijalar foizda bir xil bo'ladi",
      "Ikkinchisining riski pastroq — u tezroq plyusga chiqadi",
      "Bir xil EV ga qaramay, ikkinchisining hisobni nolga tushirish ehtimoli ancha yuqori"
    ],
    "answer": 3,
    "explain": "Musbat EV faqat masofagacha yetib borgan odam uchun ishlaydi. 10% riskda 7 ta zarar hisobning yarmidan ko'pini oladi va tiklanish matematik jihatdan deyarli imkonsiz bo'ladi. Risk hajmi o'z ustunligingni umuman ko'rasanmi-yo'qmi, shuni hal qiladi."
  },
  {
    "q": "Demoda uch oy foydali savdo. Bu nimani isbotlaMAYDI?",
    "options": [
      "Pul haqiqiy bo'lganda ham o'sha prosadkaga chidashingni",
      "Terminalni o'zlashtirganingni",
      "Strategiya qoidalarini mexanik bajarish mumkinligini",
      "Pozitsiya hajmini hisoblay olishingni"
    ],
    "answer": 0,
    "explain": "Demo mexanikani va qoidalarni tekshiradi, psixologiyani emas. Haqiqiy zarar paytida o'zingni qanday tutishingni bilishning yagona yo'li — minimal hajmdagi real hisob."
  },
  {
    "q": "Quyidagilardan qaysi biri O'Z-O'ZIDAN firibgarlik belgisi emas?",
    "options": [
      "Oyiga 30% foyda kafolati",
      "Foydani yechish uchun qo'shimcha pul kiritishni talab qilish",
      "1:500 yelka",
      "Litsenziya va yuridik shaxsning yo'qligi"
    ],
    "answer": 2,
    "explain": "Katta yelkani YeI dan tashqaridagi qonuniy brokerlar ham taklif qiladi — xavfli narsa uni ro'yxatda ko'rish emas, undan foydalanish. Daromad kafolati va «yechish uchun to'la» esa — puli qaytmaydigan sxemaning belgilari."
  },
  {
    "q": "Kundalikdagi yozuvni tahlilga yaroqli qiladigan narsa nima?",
    "options": [
      "Izohsiz grafik skrinshoti",
      "Kirish sababi va qoidalarga rioya qilingani, natija ma'lum bo'lishidan OLDIN yozilgani",
      "Oylik jami P/L",
      "Hafta oxirida esdan yozilgan qayd"
    ],
    "answer": 1,
    "explain": "Savdo yopilgach xotira sababni natijaga moslab qayta yozadi: yutuq hisob-kitobdek, zarar esa omadsizlikdek ko'rinadi. Faqat oldindan qayd etilgan narsa ma'lumot beradi."
  },
  {
    "q": "Nega London va Nyu-York kesishuvi EUR/USD bo'yicha yangi boshlovchiga qulayroq?",
    "options": [
      "Bu vaqtda narx trend bo'ylab yuradi",
      "Hajm ko'proq va spred torroq",
      "Bu vaqtda zarar ko'rish riski pastroq",
      "Broker komissiyani kamaytiradi"
    ],
    "answer": 1,
    "explain": "Maksimal likvidlik — tor spred va kamroq sirg'anish, ya'ni arzonroq kirish va halolroq stop ijrosi. Likvidlik harakat yo'nalishini va'da qilmaydi."
  },
  {
    "q": "Uzoq masofada yangi boshlovchining hisob taqdirini qaysi ko'nikma hal qiladi?",
    "options": [
      "Yo'nalishni bashorat qilish aniqligi",
      "Yangiliklarga tez munosabat",
      "To'g'ri sozlangan indikator",
      "Riskni boshqarish va intizom"
    ],
    "answer": 3,
    "explain": "Yo'nalishni barqaror topa oladigan odam yo'q. Zararni cheklaydigan va o'z qoidalarini bajaradiganlar omon qoladi — bu butun imtihon aynan shuni tekshirdi."
  },
  {
    "q": "USD/JPY = 150 bo'lsa, EUR/JPY bo'yicha bitta lotda punkt qancha turadi?",
    "options": [
      "$10 — barcha majorlardagidek",
      "≈$6.67",
      "≈$66.70",
      "EUR/USD kursiga bog'liq"
    ],
    "answer": 1,
    "explain": "Punkt narxini kotirovka valyutasi belgilaydi, bazaviy emas. Iyenali har qanday juftlikda punkt = 0.01 × 100 000 = 1000 ¥, dollarda esa 1000 ÷ 150 = $6.67. Shuning uchun EUR/JPY va USD/JPY da punkt bir xil turadi."
  },
  {
    "q": "Depozit $1000, band marja $500, ochiq pozitsiyalarda joriy zarar $300. Marja darajasi qancha?",
    "options": [
      "200%",
      "140%",
      "70%",
      "40%"
    ],
    "answer": 1,
    "explain": "Marja darajasi = mablag' ÷ marja × 100% = (1000 − 300) ÷ 500 × 100% = 140%. Brokerlarda Stop Out odatda 20–50% da: majburiy yopilishgacha zaxira bor, lekin u zarar bilan birga kamayadi."
  },
  {
    "q": "Komissiya lotiga $7 round-turn (kirish + chiqish). 0.5 lotlik savdo qancha turadi?",
    "options": [
      "$7.00",
      "$3.50",
      "$14.00",
      "$0.70"
    ],
    "answer": 1,
    "explain": "0.5 × $7 = $3.50, va bu hali spredsiz. Qisqa stoplarda komissiya riskning sezilarli ulushiga aylanadi — uni spred bilan birga sanang, alohida emas."
  },
  {
    "q": "Depozit $1000, barqaror oyiga +2%. Bir yildan keyin butun foydani yechganda va yechmaganda:",
    "options": [
      "Bir xil — $1240",
      "Yechmasa $1268; hammasini yechsa hisob $1000 bo'lib qoladi va $240 qo'lda",
      "Yechmasa $1240; yechsa $1268",
      "Farq bir dollardan kam"
    ],
    "answer": 1,
    "explain": "1000 × 1.02¹² = $1268, ikkinchi holatda $1000 plyus qo'lda $240. Bir yilda farq kichik, mohiyati ham shunda: murakkab foiz yillar davomida ishlaydi, oylar emas. «Bir oyda ikki barobar» va'dasining bunga aloqasi yo'q."
  },
  {
    "q": "Yillik foyda $500, uni SWIFT orqali $52 ga yechasiz. Yechish foydaning qancha qismini yeydi?",
    "options": [
      "10.4%",
      "1.04%",
      "5.2%",
      "52%"
    ],
    "answer": 0,
    "explain": "52 ÷ 500 = 10.4%. Qat'iy komissiya kichik summalarga eng qattiq uradi: $5000 da xuddi shu o'tkazma 1% bo'lardi. Qancha ishlaganingizni hal qilishdan oldin yechish narxini hisoblang."
  },
  {
    "q": "Pozitsiyaning yarmini +1R da yopdingiz, qolganini zararsizga ko'chirdingiz va u yerda uchdi. Savdo natijasi qanday?",
    "options": [
      "+1R",
      "+0.5R",
      "0R",
      "+2R"
    ],
    "answer": 1,
    "explain": "Yarmi +1R berdi, qolgani nol: jami +0.5R. Qisman yopish natijalar tarqoqligini kamaytiradi, lekin yuqori chegarani ham kesadi: xotirjamlik uchun o'rtacha R bilan to'lanadi. Bu tanlov, bepul yaxshilanish emas."
  },
  {
    "q": "Pozitsiya minusda, siz «kirishni o'rtachalash» uchun xuddi shuncha hajm qo'shasiz. Risk bilan nima bo'ldi?",
    "options": [
      "Risk ikki barobar oshdi, dastlabki stop endi rejani himoya qilmaydi",
      "Risk o'zgarmadi — kirish narxi yaxshilandi",
      "Risk kamaydi: o'rtacha narx bozorga yaqinroq",
      "Risk uchdan biriga oshdi"
    ],
    "answer": 0,
    "explain": "Hajm ikkilandi, demak sizga qarshi har bir punkt ikki barobar qimmat. O'rtacha narx haqiqatan yaxshilandi — tuzoq ham shunda: rejadan chetga chiqqan savdo endi rejadan ikki barobar katta."
  },
  {
    "q": "Stop-loss qo'yilgan edi, lekin dushanba bozor undan ancha uzoqda gep bilan ochildi. Nima bo'ldi?",
    "options": [
      "Stop gepdan keyingi birinchi narxda ishladi — zarar rejadagidan katta",
      "Broker stopni ko'rsatilgan narxda bajarishi shart",
      "Stop keyingi haftaga o'tadi",
      "Pozitsiya zararsizda yopildi"
    ],
    "answer": 0,
    "explain": "Dam olish kunlari bozor savdo qilmaydi, yangiliklar esa chiqadi. Gep stop darajasidan sakrab o'tadi va u birinchi mavjud narxda bajariladi. Pozitsiyani dam olishdan o'tkazish — alohida riskli alohida qaror."
  },
  {
    "q": "Demo-hisob savdolarni realdan yaxshiroq bajaradi. Nega?",
    "options": [
      "Demo sirg'anish, rekvot va spred kengayishini takrorlamaydi",
      "Demoda komissiya pastroq",
      "Demoda boshqa kotirovka provayderi",
      "Farq yo'q, shunday tuyuladi xolos"
    ],
    "answer": 0,
    "explain": "Demo kotirovka bo'yicha bir zumda bajaradi, real bozor esa mavjud likvidlik bo'yicha. Shuning uchun qisqa stopli va tez-tez savdo qiladigan strategiya demoda realda bo'lgandan yaxshiroq ko'rinadi."
  },
  {
    "q": "Sakkizta sozlanadigan parametrli strategiya tarixda +300% ko'rsatdi. Ehtimoli ko'proq nima?",
    "options": [
      "Parametrlar o'tmishga moslangan va yangi ma'lumotlarda natija tarqaladi",
      "Strategiya haqiqatan juda yaxshi",
      "Realda yanada yaxshi bo'ladi — tarix kamaytirib ko'rsatadi",
      "Shunchaki hajmni oshirish kerak"
    ],
    "answer": 0,
    "explain": "Sozlagich qancha ko'p bo'lsa, egri chiziqni allaqachon bo'lgan narsaga moslash shunchalik oson. Yagona tekshiruv: strategiya sozlash paytida ko'rmagan ma'lumotlarda ishga tushirish. «Robotlar» aynan chiroyli bektestlar ustiga sotiladi."
  },
  {
    "q": "Savdo uchinchi kun joyida turibdi — na stopga, na maqsadga. Nima oqilona?",
    "options": [
      "Vaqt qoidasi bo'yicha yopish, agar u rejada bo'lgan bo'lsa",
      "Qancha kerak bo'lsa kutish — stop baribir himoya qiladi",
      "Qo'shish, narx qarshi ketmayapti-ku",
      "Maqsadni yaqinlashtirish"
    ],
    "answer": 0,
    "explain": "To'xtab qolgan savdodagi pul band va ishlamaydi, risk esa osilib turadi. Vaqt cheklovi rejaning normal qismi, lekin u kirishdan OLDIN yozilgan bo'lishi kerak, aks holda bu shunchaki sabrsizlik."
  },
  {
    "q": "30 punktlik stopda 2R olish uchun bozor…",
    "options": [
      "Yo'lda stopga tegmasdan siz tomonga 60 punkt yurishi kerak",
      "30 punkt yurishi kerak",
      "Istalgan tartibda 60 punkt yurishi kerak",
      "Kirishdan yuqorida yopilishi kerak"
    ],
    "answer": 0,
    "explain": "2R maqsadi — bu 60 punkt, va masofa qancha muhim bo'lsa, yo'l ham shuncha muhim: agar narx avval 30 punkt qarshi ketsa, savdo tugadi. Shuning uchun keng maqsadlar nafaqat harakatni, balki uning shaklini ham talab qiladi."
  },
  {
    "q": "Svopsiz hisobda broker svop olmaydi. U o'zinikini qayerdan qaytaradi?",
    "options": [
      "Kengroq spred, oshirilgan komissiya yoki holat uchun to'lovdan",
      "Hech qayerdan — bu xayriya",
      "Boshqa mijozlar hajmidan",
      "Depozit foizlaridan"
    ],
    "answer": 0,
    "explain": "«Svopsiz» — xarajatni yo'q qilish emas, qayta taqsimlash. O'z stsenariyingizning to'liq narxini ikkala hisob turida solishtiring: tez-tez qisqa savdolarda svop deyarli yig'ilmaydi, kengaytirilgan spred esa har bir savdoda to'lanadi."
  },
  {
    "q": "Hisob so'mda to'ldirilgan, brokerda esa dollarda. Qanday risk qo'shildi?",
    "options": [
      "Kurs riski: so'mdagi natija ham savdoga, ham USD/UZS kursiga bog'liq",
      "Hech qanday, broker kursni qat'iylashtiradi",
      "Faqat konvertatsiya komissiyasi",
      "Soliq riski — summa ikki marta sanaladi"
    ],
    "answer": 0,
    "explain": "Dollardagi foyda so'm mustahkamlanganda qadrsizlanishi mumkin va aksincha. Bu «savdo qilma» degani emas; bu natijani siz sarflaydigan valyutada sanash kerak degani — jurnal ikkalasini ham ko'rsata oladi."
  },
  {
    "q": "Svopsiz hisobda spred 0.5 punktga kengroq. Oyiga 0.1 lotdan 40 ta savdoda bu…",
    "options": [
      "Oyiga $20 qo'shimcha xarajat",
      "Oyiga $2",
      "Oyiga $200",
      "Hech narsa, yarim punkt sezilmaydi"
    ],
    "answer": 0,
    "explain": "0.5 × punktiga $1 (0.1 lot) × 40 = $20. «Yarim punkt» arzimasdek eshitiladi, lekin har bir savdoga ko'payadi. Hisob turlarini bitta savdoda emas, o'z savdolaringiz soni bo'yicha solishtirish kerak."
  }
]
</script>

---

## Keyingi qadam

Imtihondan o'tdingizmi? Tabriklaymiz — siz asoslarni o'zlashtirgansiz. Lekin haqiqiy
imtihon — **bozor**. [Demo](README.md) dan boshlang, [jurnal](../journal/trading-journal-template.md)
yuritib boring, xavfni [pozitsiya kalkulyatori](position-calculator.md) bilan hisoblang
va realga **kichik** hajm bilan o'ting.

O'ta olmadingizmi? Muammo yo'q — [asosiy qo'llanmaga](../index.md) va
[savdo oldidan chek-listga](../extras/pre-trade-check.md) qaytib, keyin qaytadan urinib ko'ring.

---

!!! danger "Moliyaviy maslahat emas"
    Sertifikat — bu o'quv yutug'i, litsenziya yoki foyda kafolati emas. Forexda
    savdo kapital yo'qotishning yuqori xavfi bilan bog'liq.
