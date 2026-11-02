---
widgets: [roadmap-diag]
---

# 🗺️ O'qish yo'l xaritasi

!!! abstract "Ushbu sahifadan qanday foydalanish"
    Bu — forexni endi o'rganishni boshlagan yangi boshlovchi uchun **bosqichma-bosqich yo'l**. Har bir bosqichda:

    - 🎯 **Maqsad** — bosqichdan keyin nima qila olish kerak
    - ⏱️ **Muddat** — real baholash
    - 📚 **Nimani o'qish** — loyihaning aniq sahifalari
    - ✅ **Nazorat nuqtasi** — keyingi bosqichga o'tish mezoni

    Nazorat nuqtalarini yopmaguningizcha **keyingi darajaga o'tmang**. Aks holda pulingizni behuda yo'qotasiz.

<div id="roadmap-diag"></div>

<script type="application/json" id="diag-questions">
[
  {
    "level": 0,
    "q": "EUR/USD uchun pips nima?",
    "options": [
      "0.01 — verguldan keyingi ikkinchi belgi",
      "0.0001 — verguldan keyingi to'rtinchi belgi",
      "Narxning bir sent harakati",
      "Narxning 1% i"
    ],
    "answer": 1
  },
  {
    "level": 0,
    "q": "Spred — bu…",
    "options": [
      "pul chiqarish uchun broker komissiyasi",
      "pozitsiyani ertaga o'tkazish to'lovi",
      "sotib olish (Ask) va sotish (Bid) narxi orasidagi farq",
      "depozitni ko'paytiradigan kaldıraç"
    ],
    "answer": 2
  },
  {
    "level": 0,
    "q": "Depozit $1000, kaldıraç 1:100. Broker qanday hajmli pozitsiya ochishga ruxsat beradi?",
    "options": [
      "$100 000 gacha",
      "$10 000 gacha",
      "$1100 gacha",
      "$1000 gacha"
    ],
    "answer": 0
  },
  {
    "level": 0,
    "q": "Foreksdagi standart lot — bu…",
    "options": [
      "bazaviy valyutaning 10 000 birligi",
      "bazaviy valyutaning 100 000 birligi",
      "$100",
      "1000 unsiya"
    ],
    "answer": 1
  },
  {
    "level": 1,
    "q": "Ko'tarilish trendi — bu … seriyasi",
    "options": [
      "pastroq maksimumlar va minimumlar",
      "bir xil o'lchamdagi shamlar",
      "yuqoriroq maksimumlar va minimumlar",
      "o'sib boruvchi hajmlar"
    ],
    "answer": 2
  },
  {
    "level": 1,
    "q": "Qo'llab-quvvatlash darajasi — narx ilgari … hudud",
    "options": [
      "to'xtab, yuqoriga burilgan",
      "har doim yumaloq sonda turgan",
      "tarixiy maksimum qo'ygan",
      "indikatorni kesib o'tgan"
    ],
    "answer": 0
  },
  {
    "level": 1,
    "q": "Narx o'sib borayotgan EMA 50 dan yuqorida. Bu odatda qanday o'qiladi?",
    "options": [
      "Ayiq fon — sotish izlanadi",
      "Buqа fon — sotib olish ustuvor",
      "Kafolatlangan flet",
      "Darhol sotish signali"
    ],
    "answer": 1
  },
  {
    "level": 1,
    "q": "Qo'llab-quvvatlash darajasida uzun pastki fitilli sham ko'pincha nimani bildiradi?",
    "options": [
      "sotuvchilar bozorni to'liq nazorat qiladi",
      "hajm bozordan ketgan",
      "xaridorlar pasayishni qaytarib bergan",
      "tez orada gep bo'ladi"
    ],
    "answer": 2
  },
  {
    "level": 2,
    "q": "Bitim uchun 1% xavfda ketma-ket o'n ta zarar taxminan qanchasini oladi?",
    "options": [
      "butun hisobni",
      "hisobning yarmi",
      "hisobning taxminan 10% i",
      "hisobning aynan 1% i"
    ],
    "answer": 2
  },
  {
    "level": 2,
    "q": "Ketma-ket uchta zararli bitim. Jarayon nima deydi?",
    "options": [
      "Lotni ikki baravar qilib, qaytarib olish",
      "To'xtash va bitimlarni jurnalda tahlil qilish",
      "Darhol strategiyani almashtirish",
      "«Seriya tugamagunicha» yana bitta bitim ochish"
    ],
    "answer": 1
  },
  {
    "level": 2,
    "q": "Treydingdagi FOMO — bu…",
    "options": [
      "harakatni o'tkazib yuborish qo'rquvi, signalsiz kirish",
      "kechiktirilgan order turi",
      "tungi pozitsiya to'lovi",
      "broker ochko'zligi"
    ],
    "answer": 0
  },
  {
    "level": 2,
    "q": "Savdo rejasi nima uchun kerak?",
    "options": [
      "Brokerimizni hayratda qoldirish uchun",
      "Qarorlar bitimdan oldin, hissiyotda emas, qabul qilinishi uchun",
      "Kamroq soliq to'lash uchun",
      "Yangiliklarni taxmin qilish uchun"
    ],
    "answer": 1
  },
  {
    "level": 3,
    "q": "Bektest — bu…",
    "options": [
      "demo hisobda savdo",
      "strategiya qoidalarini tarixiy ma'lumotlarda tekshirish",
      "maksimal foyda uchun parametrlarni sozlash",
      "real hisobda mikrolot bilan savdo"
    ],
    "answer": 1
  },
  {
    "level": 3,
    "q": "Nega bektestdagi «ideal» parametrlar xavfli?",
    "options": [
      "Broker ularni taqiqlaydi",
      "Ular o'tmishga moslangan va kelajakda yemirilishi mumkin",
      "Spred ularni buzadi",
      "Ular terminal xotirasini ko'p egallaydi"
    ],
    "answer": 1
  },
  {
    "level": 3,
    "q": "Real hisobdan oldin nega 50+ demo bitim kerak?",
    "options": [
      "Strategiyani besh bitim bilan emas, statistika bilan baholash uchun",
      "Terminalni «qizdirish» uchun",
      "Bu brokerlarning talabi",
      "Kaldıraçni oshirish uchun"
    ],
    "answer": 0
  },
  {
    "level": 3,
    "q": "Qanday birinchi strategiya to'g'ri?",
    "options": [
      "Ishonchlilik uchun o'n indikatorli",
      "Pullik signal chatidan olingan",
      "Martingejl — har qanday zararni qaytaradi",
      "Kirish, stop va chiqishning aniq yozma qoidalari bilan"
    ],
    "answer": 3
  },
  {
    "level": 4,
    "q": "Savdo jurnali nima uchun yuritiladi?",
    "options": [
      "Takrorlanadigan xatolarni topish uchun",
      "Faqat soliq hisoboti uchun",
      "Chiroyli skrinshotlar uchun",
      "Signallarni sotish uchun"
    ],
    "answer": 0
  },
  {
    "level": 4,
    "q": "WinRate 40%, o'rtacha RR 1:2. Bu qanday tizim?",
    "options": [
      "Zararli: g'alabalar yarmidan kam",
      "Nolga teng",
      "Hech narsa deyib bo'lmaydi",
      "Foydali: bitimiga +0.2R kutilma"
    ],
    "answer": 3
  },
  {
    "level": 4,
    "q": "Nega o'rtacha R bitta bitim natijasidan muhimroq?",
    "options": [
      "Bitta bitim — shovqin, seriya tizimni ko'rsatadi",
      "Shunga hisoblash tezroq",
      "Jurnal shart talab qiladi",
      "Stoplar qisqaradi"
    ],
    "answer": 0
  },
  {
    "level": 4,
    "q": "Xuddi shu xato jurnalda uchinchi marta takrorlandi. Nimani o'zgartirish kerak?",
    "options": [
      "Jarayon va chek-listni, «ehtiyotkorroq bo'lishga harakat» emas",
      "Qoplash uchun xavfni oshirish",
      "Valyuta juftligini almashtirish",
      "O'qishni tashlash — meniki emas"
    ],
    "answer": 0
  }
]
</script>

## Umumiy ko'rinish

<div class="fx-rm">

  <!-- Boshlanish -->
  <div class="fx-rm__item">
    <div class="fx-rm__badge fx-rm__badge--start">🏁</div>
    <div class="fx-rm__card">
      <div class="fx-rm__header">
        <div class="fx-rm__title">Start: forexni o'rganmoqchiman</div>
      </div>
      <p class="fx-rm__goal">Birinchi qadam — noldan demo hisobda ishonchli treydergacha bo'lgan yo'l.</p>
      <div class="fx-rm__tags">
        <span class="fx-rm__tag">Yangi boshlovchi</span>
        <a href="../" class="fx-rm__tag">Bosh sahifa →</a>
      </div>
    </div>
  </div>

  <!-- 1-faza -->
  <div class="fx-rm__phase fx-rm__phase--beginner">🌱 1-faza — Asoslar</div>

  <!-- 0-bosqich -->
  <div class="fx-rm__item" data-level="0">
    <div class="fx-rm__badge fx-rm__badge--phase1">0</div>
    <div class="fx-rm__card fx-rm__card--phase1">
      <div class="fx-rm__header">
        <div class="fx-rm__title">0-bosqich: Tayyorgarlik</div>
        <span class="fx-rm__time">~1 hafta</span>
      </div>
      <p class="fx-rm__goal">Foreks nima ekanini tushunish va u sizga to'g'ri kelishini tekshirish.</p>
      <div class="fx-rm__tags">
        <span class="fx-rm__tag">Pips · Lot · Spred · Kaldıraç</span>
        <a href="../КАК-ПОЛЬЗОВАТЬСЯ/" class="fx-rm__tag">Qanday foydalanish →</a>
      </div>
    </div>
  </div>

  <!-- 1-bosqich -->
  <div class="fx-rm__item" data-level="1">
    <div class="fx-rm__badge fx-rm__badge--phase1">1</div>
    <div class="fx-rm__card fx-rm__card--phase1">
      <div class="fx-rm__header">
        <div class="fx-rm__title">1-bosqich: Nazariya asoslari</div>
        <span class="fx-rm__time">2–4 hafta</span>
      </div>
      <p class="fx-rm__goal">Treyderning asosiy tilini o'zlashtirish: trendlar, qo'llab-quvvatlash/qarshilik, indikatorlar, shamlar.</p>
      <div class="fx-rm__tags">
        <span class="fx-rm__tag">EMA · RSI · S/R</span>
        <a href="../forex-guide/" class="fx-rm__tag">Darslik →</a>
        <a href="../docs/technical-analysis/" class="fx-rm__tag">Texnik tahlil →</a>
      </div>
    </div>
  </div>

  <!-- 2-faza -->
  <div class="fx-rm__phase fx-rm__phase--middle">⚡ 2-faza — Psixologiya va strategiya</div>

  <!-- 2-bosqich -->
  <div class="fx-rm__item" data-level="2">
    <div class="fx-rm__badge fx-rm__badge--phase2">2</div>
    <div class="fx-rm__card fx-rm__card--phase2">
      <div class="fx-rm__header">
        <div class="fx-rm__title">2-bosqich: Psixologiya va xavf-menejment</div>
        <span class="fx-rm__time">1–2 hafta</span>
      </div>
      <p class="fx-rm__goal">Asosiy raqib — o'zingiz ekanini tushunish. Pozitsiya kalkulyatori, savdo rejasi.</p>
      <div class="fx-rm__tags">
        <span class="fx-rm__tag">Anti-Tilt · Trading Plan</span>
        <a href="../extras/psychology/" class="fx-rm__tag">Psixologiya →</a>
        <a href="../tools/position-calculator/" class="fx-rm__tag">Kalkulyator →</a>
      </div>
    </div>
  </div>

  <!-- 3-bosqich -->
  <div class="fx-rm__item" data-level="3">
    <div class="fx-rm__badge fx-rm__badge--phase2">3</div>
    <div class="fx-rm__card fx-rm__card--phase2">
      <div class="fx-rm__header">
        <div class="fx-rm__title">3-bosqich: Birinchi strategiya</div>
        <span class="fx-rm__time">1–2 oy</span>
      </div>
      <p class="fx-rm__goal">Bitta strategiya tanlash, bektestni o'zlashtirish va demoda 50+ bitim qilish.</p>
      <div class="fx-rm__tags">
        <span class="fx-rm__tag">50+ demo bitim</span>
        <a href="../docs/strategy-details/" class="fx-rm__tag">Strategiya →</a>
        <a href="../tools/replay-trainer/" class="fx-rm__tag">Replay →</a>
      </div>
    </div>
  </div>

  <!-- 3-faza -->
  <div class="fx-rm__phase fx-rm__phase--advanced">🚀 3-faza — Ilg'or</div>

  <!-- 4-bosqich -->
  <div class="fx-rm__item" data-level="4">
    <div class="fx-rm__badge fx-rm__badge--phase3">4</div>
    <div class="fx-rm__card fx-rm__card--phase3">
      <div class="fx-rm__header">
        <div class="fx-rm__title">4-bosqich: Tahlil va yaxshilash</div>
        <span class="fx-rm__time">~1 oy</span>
      </div>
      <p class="fx-rm__goal">Natijalarni tahlil qilish, savdo jurnalini yuritish, xatolarni takroriy tuzatish.</p>
      <div class="fx-rm__tags">
        <span class="fx-rm__tag">Winrate > 50% · RR ≥ 1.5</span>
        <a href="../journal/web-journal/" class="fx-rm__tag">Jurnal →</a>
        <a href="../tools/winrate-rr-calculator/" class="fx-rm__tag">WinRate × RR →</a>
      </div>
    </div>
  </div>

  <!-- Carra nuqtasi -->
  <div class="fx-rm__item">
    <div class="fx-rm__badge" style="color:#ef4444;border-color:#ef4444;">?</div>
    <div class="fx-rm__card fx-rm__card--decision">
      <div class="fx-rm__header">
        <div class="fx-rm__title">5-bosqich: Real hisobga tayyormisiz?</div>
      </div>
      <p class="fx-rm__goal">Yakuniy imtihondan o'ting. Natija chegaradan past bo'lsa — 4-bosqichga qayting.</p>
      <div class="fx-rm__tags">
        <span class="fx-rm__tag">❌ Yo'q → 4-bosqich</span>
        <a href="../tools/exam/" class="fx-rm__tag">🎓 Yakuniy imtihon →</a>
        <a href="../tools/quiz/" class="fx-rm__tag">Kviz →</a>
      </div>
    </div>
  </div>

  <!-- Real hisob fazasi -->
  <div class="fx-rm__phase fx-rm__phase--real">💵 Real hisob</div>

  <!-- 5-bosqich Real -->
  <div class="fx-rm__item">
    <div class="fx-rm__badge fx-rm__badge--accent">5</div>
    <div class="fx-rm__card fx-rm__card--accent">
      <div class="fx-rm__header">
        <div class="fx-rm__title">5-bosqich: Real hisob</div>
        <span class="fx-rm__time">$100–300</span>
      </div>
      <p class="fx-rm__goal">Minimal depozit bilan real hisob ochish. Bitimga 0.5% xavf, istisnosiz.</p>
      <div class="fx-rm__tags">
        <span class="fx-rm__tag">0.5% xavf · Mini lotlar</span>
        <a href="../extras/brokers-comparison/" class="fx-rm__tag">Brokerlar →</a>
        <a href="../uz/brokers-uz/" class="fx-rm__tag">O'zbekiston uchun brokerlar →</a>
      </div>
    </div>
  </div>

  <!-- 6-bosqich -->
  <div class="fx-rm__item">
    <div class="fx-rm__badge fx-rm__badge--gold">6</div>
    <div class="fx-rm__card fx-rm__card--gold">
      <div class="fx-rm__header">
        <div class="fx-rm__title">6-bosqich: Bir yildan keyingi rivojlanish</div>
        <span class="fx-rm__time">12 oydan keyin</span>
      </div>
      <p class="fx-rm__goal">Instrumentlarni kengaytirish: Order Flow, kripto, aksiyalar, portfel tafakkuri.</p>
      <div class="fx-rm__tags">
        <span class="fx-rm__tag">Daromad > 0</span>
        <a href="../growth/order-flow-volume-profile/" class="fx-rm__tag">Order Flow →</a>
        <a href="../growth/crypto-trading-guide/" class="fx-rm__tag">Kripto →</a>
        <a href="../growth/stocks-basics/" class="fx-rm__tag">Aksiyalar →</a>
      </div>
    </div>
  </div>

</div>

---

## 0-bosqich: Tayyorgarlik

!!! info "Maqsad"
    **Forex nima ekanligini** tushunish va u sizga mosligini tekshirish.

⏱️ **Muddat**: ~1 hafta.

### Harakatlar

| Qadam | Qayerda | Vaqt |
|---|---|---|
| 1. «Loyihadan qanday foydalanish» ni o'qish | [Bosh sahifa](index.md) | 30 daq |
| 2. Tuzilmani tushunish: qo'llanma, asboblar, strategiyalar | [README](https://github.com/MukhammadAmir-Akbarov/forex-toolkit/blob/main/README.md) | 15 daq |
| 3. 30 savolli tayyorgarlik testini topshirish | [Tayyorlik testi](tools/risk-profile.md) — brauzerda | 20 daq |
| 4. Python va bog'liqliklarni o'rnatish | Ko'rsatma | 30 daq |

### ✅ Nazorat nuqtasi

- [ ] Men **pip**, **lot**, **spred**, **leverage** nima ekanini bilaman
- [ ] **Forexda 74-89% pul yo'qotishini** tushunaman
- [ ] Tayyorgarlik testi **> 50%** ko'rsatdi
- [ ] **Python o'rnatilgan**, `pytest` o'tadi

---

## 1-bosqich: Nazariya asoslari

!!! info "Maqsad"
    Treyderning **asosiy lug'atini** o'rganish: trendlar, qo'llab-quvvatlash/qarshilik, indikatorlar, sham patternlari.

⏱️ **Muddat**: 2-4 hafta (kuniga 30-60 daqiqa).

### Harakatlar

| Qadam | Qayerda | Vaqt |
|---|---|---|
| 1. **Asosiy qo'llanma** (to'liq) | [forex-guide.md](forex-guide.md) | ~5 soat |
| 2. Texnik tahlil grafiklar bilan | [docs/technical-analysis.md](docs/technical-analysis.md) | ~3 soat |
| 3. Lug'at — notanish atamalarni yozib oling | [extras/glossary.md](extras/glossary.md) | o'qish davomida |
| 4. FAQ — asosiy savollarga javob | [extras/faq.md](extras/faq.md) | 1 soat |
| 5. Tartibga solinadigan brokerda **demo-hisob** ochish | [Brokerlar (UZ)](uz/brokers-uz.md) | 30 daq |
| 6. MT5 / TradingView interfeysini o'zlashtirish | YouTube + amaliyot | 2-3 soat |

### ✅ Nazorat nuqtasi

- [ ] EMA, RSI, trend nima ekanini **boshqasiga tushuntira olaman**
- [ ] Grafikda qo'llab-quvvatlash/qarshilik darajalarini **ko'rsata olaman**
- [ ] $1000+ virtual mablag' bilan **demo-hisobim ochiq**
- [ ] Terminalda savdo **ocha va yopa olaman** (to'g'ri stop va take bilan)
- [ ] Aniq sababsiz **savdo ochmayman**

---

## 2-bosqich: Psixologiya va xavf-menejment

!!! info "Maqsad"
    **Asosiy raqibingiz — o'zingiz** ekanligini tushunish va buni boshqarishni o'rganish.

⏱️ **Muddat**: 1-2 hafta.

### Harakatlar

| Qadam | Qayerda | Vaqt |
|---|---|---|
| 1. **Psixologiya** bo'limi | [extras/psychology.md](extras/psychology.md) | ~2 soat |
| 2. **Anti-Tilt protokol** | [extras/anti-tilt-protocol.md](extras/anti-tilt-protocol.md) | 30 daq |
| 3. Shaxsiy **savdo rejasini** to'ldirish | [extras/trading-plan-template.md](extras/trading-plan-template.md) | 1 soat |
| 4. **Pozitsiya kalkulyatorini** o'zlashtirish | [Kalkulyator](tools/position-calculator.md) | 15 daq |
| 5. **Kunlik tartib** — treyderning kun rejimi | [extras/daily-routine.md](extras/daily-routine.md) | 30 daq |
| 6. **Ma'lumotlar manbalari** — nimani kuzatish | [extras/market-data-sources.md](extras/market-data-sources.md) | 1 soat |

### ✅ Nazorat nuqtasi

- [ ] Trading Plan **to'ldirilgan va chop etilgan**
- [ ] **3 ketma-ket yo'qotishdan keyin** nima qilishni bilaman (anti-tilt)
- [ ] Pozitsiya kalkulyatoridan **foydalana olaman**
- [ ] **Xavfni hisoblamasdan** pozitsiya ochmayman
- [ ] Kunlik tartibimni **yozganman**

---

## 3-bosqich: Birinchi strategiya

!!! info "Maqsad"
    **Bitta strategiyani chuqur** o'zlashtirish, demoda 30+ savdo qilish, **jurnal yuritish**.

⏱️ **Muddat**: 1-2 oy. **Shoshilmang.**

### Harakatlar

| Qadam | Qayerda | Vaqt |
|---|---|---|
| 1. **EMA50 Pullback** strategiyasini batafsil o'rganish | [docs/strategy-details.md](docs/strategy-details.md) | 1 soat |
| 2. Sintetikada **bektesterni** ishga tushirish | `python bot/backtest.py` | 30 daq |
| 3. EUR/USD uchun **real ma'lumotlarni** yuklab olish | `python advanced/data_downloader.py` | 10 daq |
| 4. **Real spred** bilan bektest | `python bot/backtest.py --csv data/EURUSD_1h.csv --spread-pips 2 --max-consecutive-losses 3` | 30 daq |
| 5. **Savdo jurnalini** ochish | `python tools/journal_cli.py --help` | 5 daq |
| 6. EMA50 strategiyasi bo'yicha **demoda 30+ savdo** | Broker terminali | 1-2 oy |
| 7. **Har bir savdo** jurnalda, kirish sababi va his-tuyg'ular bilan | `journal_cli.py add` | 5 daq/savdo |

### ✅ Nazorat nuqtasi

- [ ] Jurnalda kirish tasvirlari bilan **30+ yozuv**
- [ ] `journal_dashboard.py` ni ishga tushirib o'z statistikamni **o'qiy olaman**
- [ ] Demoda win rate va Profit Factor **barqaror**
- [ ] So'nggi 10 ta savdoda Trading Plan ni **buzmadim**

---

## 4-bosqich: Tahlil va yaxshilash

!!! info "Maqsad"
    **O'z xatolarini** topish, nima ishlayotganini tushunish va strategiyani tuzatish.

⏱️ **Muddat**: ~1 oy.

### Harakatlar

| Qadam | Qayerda | Vaqt |
|---|---|---|
| 1. **Jurnal analizatori** — AI insaytlar | `python tools/journal_analyzer.py` | 30 daq |
| 2. **Xatolar jurnali** — takrorlanadiganlarini yozish | [journal/mistakes-log.md](journal/mistakes-log.md) | 1 soat |
| 3. **Strategiyalar taqqoslash** | `python strategies/compare.py` | 1 soat |
| 4. **Walk-forward optimizatsiya** | `python advanced/walk_forward.py` | 30 daq |
| 5. **Monte Carlo** — vayron bo'lish xavfi | `python tools/monte_carlo.py` | 15 daq |
| 6. Tuzatishlar bilan **yana 30 demo savdo** | Terminal | 1 oy |

### ✅ Nazorat nuqtasi

- [ ] **3 ta asosiy xatomni** bilaman va yozganman
- [ ] Yangi savdolarda kamida bittasini **tuzatdim**
- [ ] Win rate **barqaror** (80% → 20% → 70% sakrash yo'q)
- [ ] Demoda **3 oydan ortiq** o'tdi
- [ ] Real yo'qotishlarga **psixologik tayyorman**

---

## 5-bosqich: Real hisobga o'tish

!!! info "Maqsad"
    **Minimal depozit** bilan real pulga o'tish, xavf qoidalarini buzmasdan.

⏱️ **Muddat**: individual.

### Harakatlar

| Qadam | Qayerda | Vaqt |
|---|---|---|
| 1. **Demo vs Real** ni o'qish | [journal/demo-vs-real-comparison.md](journal/demo-vs-real-comparison.md) | 30 daq |
| 2. $100-300 ga **real hisob** ochish | Demo bilan bir xil brokerda | 1-2 kun (KYC) |
| 3. Faqat **mikro-lot** (0.01) | Terminal | — |
| 4. Savdoga **0.5% xavf** — istisnosiz | Pozitsiya kalkulyatori | har savdo |
| 5. **Birinchi real savdo** alohida yoziladi | `journal_cli.py add` | — |
| 6. Jurnal bilan **30 real savdo** | 1-2 oy | 5 daq/savdo |

!!! danger "Real pulning asosiy qoidasi"
    **Yashashga, ijaraga, ovqatga kerakli pul bilan savdo qilmang.**

    Real yo'qotishlar demodagidan **kuchliroq ta'sir qiladi**. Bu normal. Buni qabul qiling.

### ✅ Nazorat nuqtasi

- [ ] Jurnalda **30+ real savdo**
- [ ] Hech bir savdoda **0.5% xavfdan oshmadim**
- [ ] Balans **15% dan ortiq tushmadi**
- [ ] His-tuyg'usiz qarorlar bilan **prosadkani chiday olaman**

---

## 6-bosqich: Rivojlanish (1 yildan keyin)

!!! info "Maqsad"
    Chuqurroq o'rganish, asboblarni kengaytirish, ehtimol avtomatlashtirish.

⏱️ **Muddat**: cheksiz.

### Mumkin bo'lgan yo'nalishlar

```mermaid
graph LR
    A[📈 Real savdo ≥ 1 yil] --> B[📊 Volume Profile / Order Flow]
    A --> C[💱 Crypto / Stocks]
    A --> D[🤖 Avtomatlashtirish]
    A --> E[👥 Mentorlik / kontent]
```

### Bu bosqichda NIMA QILMASLIK kerak

- ❌ Xavfni keskin **5-10% gacha oshirish**
- ❌ **Pulli signallarga** obuna bo'lish
- ❌ Jurnalni tashlab qo'yish — u **yanada muhimroq** bo'ladi
- ❌ Boshqalarga o'rgatish, **o'zingiz 2+ yil barqaror** daromad ko'rsatmaguningizcha

---

## ⚠️ Asosiy qoidalar (har bosqichda)

!!! warning "O'tkazib yubormang"
    1. **Kerakli pul bilan savdo qilmang**
    2. Reaga o'tishdan oldin **kamida 3 oy demo**
    3. **Doim stop-loss qo'ying**
    4. Savdoga **xavf ≤ 1%** (yangi boshlovchi 0.5%)
    5. Har savdoda **jurnal yuriting**
    6. Oson pul va'dalariga **ishonmang**
    7. Faqat g'alabalarni emas, **yo'qotishlarni ham tahlil qiling**
    8. «Gurular» dan **uzoq turing** — pulli signallar yo'q

## 📍 Hozir qaerdasiz?

| Hozir sizda... | Bu yerga boring |
|---|---|
| 0 bilim | [0-bosqich: Tayyorgarlik](#0-bosqich-tayyorgarlik) |
| Demo bor, indikatorlar tushunarsiz | [1-bosqich: Nazariya](#1-bosqich-nazariya-asoslari) |
| Nazariya bor, demoda yo'qotyapsiz | [2-bosqich: Psixologiya](#2-bosqich-psixologiya-va-xavf-menejment) |
| Jurnalsiz 10+ demo savdo | [3-bosqich: Birinchi strategiya](#3-bosqich-birinchi-strategiya) |
| 30+ savdo, win rate beqaror | [4-bosqich: Tahlil](#4-bosqich-tahlil-va-yaxshilash) |
| Demoda 3+ oy barqaror | [5-bosqich: Real](#5-bosqich-real-hisobga-otish) |
| Realda 1+ yil | [6-bosqich: Rivojlanish](#6-bosqich-rivojlanish-1-yildan-keyin) |

---

## ⚠️ Mas'uliyatdan ozod qilish

Bu — **o'quv** marshrut. Muddatlar — taxminiy. Har kim o'z tezligida o'rganadi. Tayyor emasligingizni his qilsangiz — **shoshilmang**. Depozit yo'qotgandan ko'ra qo'shimcha bir oy demo'da qolish yaxshi.

**Hech qanday «yo'l xaritasi» foydani kafolatlamaydi.** Yakuniy natija faqat sizga bog'liq — intizom, xavf-menejment va psixologiya.
