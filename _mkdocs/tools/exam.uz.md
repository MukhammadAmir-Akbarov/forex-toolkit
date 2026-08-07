# 🎓 Yakuniy imtihon + sertifikat

!!! abstract "Qanday ishlaydi"
    Butun kurs bo'yicha 18 ta savol: risk-menejment, psixologiya, xarajatlar va
    bozor mexanikasi. O'tish bali — **80%** (18 dan 15 ta). O'tsangiz —
    **shaxsiy PNG-sertifikat** olasiz, uni yuklab olishingiz va ko'rsatishingiz mumkin.

    Bu «dahoning» emas, balki omon qolgan yangi boshlovchilarni yo'qolgan
    depozitdan ajratib turuvchi tamoyillarni o'zlashtirganligingizni tekshiradi.
    Eng yaxshi natija brauzerda saqlanadi.

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
    <button class="calc-button" id="exam-start-btn">▶ Imtihonni boshlash (18 ta savol)</button>
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
    "q": "Yangi boshlovchi uchun bir savdoda tavsiya etiladigan maksimal xavf qancha?",
    "options": ["Depozitning 10%", "Depozitning 1–2%", "Depozitning 50%", "Qancha bo'lsa ham farq qilmaydi"],
    "answer": 1,
    "explain": "Savdoga 1–2% — hatto ketma-ket 10 ta yo'qotish ham hisobni yo'q qilmaydi. Bu omon qolishning asosiy qoidasi."
  },
  {
    "q": "Depozit $1000, xavf 2%, stop EUR/USD bo'yicha 50 pips. Pozitsiya hajmi qancha?",
    "options": ["0.04 lot", "0.4 lot", "1.0 lot", "0.004 lot"],
    "answer": 0,
    "explain": "$20 xavf / (50 pips × lotga $10/pip) = 0.04 lot. Pozitsiya hajmi xavfdan HISOBLANADI, taxmin bilan emas."
  },
  {
    "q": "Stop-loss nima?",
    "options": ["Foyda fiksatsiya darajasi", "Zararli savdoni yopishning oldindan belgilangan darajasi", "Richag hajmi", "Broker komissiyasi"],
    "answer": 1,
    "explain": "Stop-loss zararni oldindan cheklaydi. Stopsiz savdo — depozitni yo'qotishning eng tez yo'li."
  },
  {
    "q": "1:500 richag — bu…",
    "options": ["500 baravar foyda kafolati", "Depozitdan 500 baravar katta pozitsiyani boshqarish imkoniyati (va xavf ham ×)", "Brokerdan chegirma", "Hisobga bonus"],
    "answer": 1,
    "explain": "Richag ham foydani, ham zararni kuchaytiradi. Katta richag = katta xavf O'Z-O'ZICHA emas — xavfni pozitsiya hajmi va stop boshqaradi."
  },
  {
    "q": "Strategiyaning matematik kutilmasi (EV) nimani ko'rsatadi?",
    "options": ["Qancha pul topishingiz aniq", "Uzoq muddatda bir savdoning o'rtacha natijasi", "Komissiya hajmi", "Yutuq foizi"],
    "answer": 1,
    "explain": "EV = (yutuq foizi × o'rtacha yutuq) − (yutqazishlar). Agar EV ≤ 0 bo'lsa — hatto million savdo ham saqlab qolmaydi."
  },
  {
    "q": "Yutuq foizi 40%, R:R = 1:2. Strategiya…",
    "options": ["Zararli", "Uzoq muddatda foydali", "Brokerga bog'liq", "Mumkin emas"],
    "answer": 1,
    "explain": "R:R 1:2 da zararsizblik yutuq foizi ≈ 33%. 40% > 33% → musbat EV. Yuqori yutuq foizi shart emas."
  },
  {
    "q": "Spred — bu…",
    "options": ["Davlat solig'i", "Sotib olish va sotish narxi o'rtasidagi farq", "Stop hajmi", "Richag"],
    "answer": 1,
    "explain": "Spred (Ask − Bid) — savdo ochilganda darhol to'lanadigan xarajat."
  },
  {
    "q": "Svop — bu…",
    "options": ["Pozitsiyani tunda o'tkazish uchun to'lov", "Hajm uchun bonus", "Order turi", "Chiqarish komissiyasi"],
    "answer": 0,
    "explain": "Svop pozitsiyani tunda ushlab turganlik uchun hisoblanadi va valyutalar foiz stavkalarining farqiga bog'liq."
  },
  {
    "q": "Oyiga 40 ta kichik savdo, spredlar depozitning katta qismini yeydi — bu misol…",
    "options": ["Savodli treydingning", "Overtreydingning (xarajatlar hisobni o'ldiradi)", "Xejirovkaning", "Xavsiz skalpingning"],
    "answer": 1,
    "explain": "Yuzlab savdolardagi xarajatlar — «depozitning jim qotili». Kamroq va ongliroq savdo qiling."
  },
  {
    "q": "Ketma-ket 5 ta yutqazishdan keyin eng to'g'ri yo'l…",
    "options": ["Qaytarib olish uchun hajmni ikki baravar oshirish", "Tanaffus olib, intizomni tekshirish", "Brokerni almashtirish", "RichaGni oshirish"],
    "answer": 1,
    "explain": "Qaytarib olishga urinish (martingayl, tilt) hisoblarni yo'q qiladi. Yutqazishlar seriyasi — xavfni oshirish emas, balki tanaffus va tahlilga signal."
  },
  {
    "q": "Savdo jurnali nima uchun kerak?",
    "options": ["Faqat soliq uchun", "O'z xato patternlarini topib, rivojlanish uchun", "Bu ixtiyoriy", "Maqtanish uchun"],
    "answer": 1,
    "explain": "Jurnal tajribani ma'lumotga aylantiradi: qachon va nimada yutqazib, yutayotganingizni ko'rsatadi. Usiz taraqqiyot tasodifiy bo'ladi."
  },
  {
    "q": "Demo-hisob nima uchun kerak?",
    "options": ["Real pul ishlash uchun", "Xavfsiz terminal o'rganish va strategiyani sinash uchun", "Bonus olish uchun", "Soliqdan qochish uchun"],
    "answer": 1,
    "explain": "Demo — mexanika va strategiyani sinash uchun. Lekin demo real pulning psixologiyasini bermaydi — kichik hajm bilan realga o'ting."
  },
  {
    "q": "Boshqaruvchi «oyiga 30% kafolatlangan foyda» va'da qilmoqda — bu…",
    "options": ["Ajoyib imkoniyat", "Skam / piramida belgisi", "Forex uchun norma", "Bank xizmati"],
    "answer": 1,
    "explain": "Kafolatlangan yuqori daromad mavjud emas. Bu klassik firibgarlik belgisi."
  },
  {
    "q": "Savdo solig'i (O'z rezidenti) bo'yicha nima deklaratsiya qilinadi?",
    "options": ["Har bir savdo alohida", "Yillik natija: foydalar minus zararlar", "Faqat chiqarishlar", "Hech narsa"],
    "answer": 1,
    "explain": "Yillik sof natija deklaratsiya qilinadi, JSHSHT 12%. soliq.uz saytini tekshiring."
  },
  {
    "q": "Margin Call darajasi nimani anglatadi…",
    "options": ["Broker sizga qo'shimcha to'laydi", "Erkin margin kam — majburiy yopilish xavfi bor", "Savdo foydada yopildi", "Bonus"],
    "answer": 1,
    "explain": "Margin Call — pozitsiya uchun mablag' yetarli emasligidan ogohlantirish. Keyingisi — Stop Out (majburiy yopilish)."
  },
  {
    "q": "Majör juftliklar uchun eng yaxshi volatillik oynasi — bu…",
    "options": ["Toshkent bo'yicha tun", "London + Nyu-York sessiyalarining qoplanishi", "Sidney ochilishi", "Dam olish kunlari"],
    "answer": 1,
    "explain": "London/Nyu-York qoplanishi — EUR/USD, GBP/USD bo'yicha maksimal hajm va tor spredlar."
  },
  {
    "q": "Barbod bo'lish xavfi (risk of ruin) qachon oshadi…",
    "options": ["Savdodagi xavf kichik bo'lsa", "Savdodagi xavf katta va/yoki EV manfiy bo'lsa", "Stop-loss mavjud bo'lsa", "Jurnal yuritilsa"],
    "answer": 1,
    "explain": "Savdodagi katta xavf ishlaydigan strategiyada ham hisobni nolga tushirish ehtimolini keskin oshiradi. Xavf hajmini nazorat qiling."
  },
  {
    "q": "Yangi boshlovchining asosiy omon qolish ko'nikmasi — bu…",
    "options": ["Yo'nalishni taxmin qilish", "Risk-menejment va intizom", "Katta richag", "Ko'p savdo"],
    "answer": 1,
    "explain": "Bozorni barqaror ravishda taxmin qilib bo'lmaydi. Omon qolish kirish aniqligi emas, balki risk-menejment va intizom orqali ta'minlanadi."
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
