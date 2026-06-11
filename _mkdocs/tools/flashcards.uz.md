# 🎴 Kartochkalar trenajyori (forex atamalari)

!!! abstract "Trenajyor qanday ishlaydi"
    Oldingizda foreks bo'yicha 105 ta kartochka bor: atamalar, patternlar, psixologiya.
    **«Javobni ko'rsatish»** tugmasini bosing, keyin halol baholang — «Bildim» yoki «Bilmadim».
    Dastur brauzeringizda progressingizni saqlab, qiyin kartochkalarni ko'proq ko'rsatadi.

    **Maqsad:** 105/105 o'rganilgan kartochkaga yetish (ketma-ket ≥3 to'g'ri javob).

!!! warning "O'quv materiali — moliyaviy maslahat emas"
    Barcha atamalar faqat o'quv maqsadida taqdim etilgan. Foreksda savdo qilish yuqori xavf bilan bog'liq.

---

<style>
/* Flashcard widget — самодостаточные стили */
.ftk-widget {
  background: var(--md-code-bg-color);
  border: 1px solid var(--md-default-fg-color--lightest);
  border-radius: 12px;
  padding: 1.5rem;
  margin: 1.5rem 0;
}

/* Progress bar */
.ftk-progress-wrap {
  margin-bottom: 1.2rem;
}
.ftk-progress-label {
  display: flex;
  justify-content: space-between;
  font-size: 0.88rem;
  font-weight: 600;
  margin-bottom: 0.35rem;
  color: var(--md-default-fg-color--light);
}
.ftk-progress-track {
  width: 100%;
  height: 10px;
  background: var(--md-default-fg-color--lightest);
  border-radius: 99px;
  overflow: hidden;
}
.ftk-progress-bar {
  height: 100%;
  background: #22c55e;
  border-radius: 99px;
  transition: width 0.4s ease;
}

/* Stats row */
.ftk-stats {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
  margin-bottom: 1.2rem;
}
.ftk-stat {
  flex: 1 1 120px;
  background: var(--md-default-bg-color);
  border-radius: 8px;
  padding: 0.6rem 0.9rem;
  text-align: center;
  border: 1px solid var(--md-default-fg-color--lightest);
}
.ftk-stat-num {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--md-primary-fg-color);
  font-family: var(--md-code-font-family);
}
.ftk-stat-lbl {
  font-size: 0.75rem;
  color: var(--md-default-fg-color--light);
  margin-top: 0.15rem;
}

/* Filter row */
.ftk-filter-row {
  display: flex;
  align-items: center;
  gap: 0.7rem;
  margin-bottom: 1.2rem;
  flex-wrap: wrap;
}
.ftk-filter-row label {
  font-size: 0.88rem;
  font-weight: 600;
}
.ftk-filter-row select {
  padding: 0.4rem 0.7rem;
  font-size: 0.9rem;
  border: 1px solid var(--md-default-fg-color--lighter);
  border-radius: 6px;
  background: var(--md-default-bg-color);
  color: var(--md-default-fg-color);
  font-family: inherit;
  cursor: pointer;
}
.ftk-filter-row select:focus {
  outline: 2px solid var(--md-primary-fg-color);
}

/* Card */
.ftk-card-area {
  perspective: 800px;
  margin-bottom: 1.2rem;
  min-height: 180px;
}
.ftk-card {
  position: relative;
  width: 100%;
  min-height: 180px;
  transform-style: preserve-3d;
  transition: transform 0.45s cubic-bezier(.4,0,.2,1);
  cursor: default;
}
.ftk-card.flipped {
  transform: rotateY(180deg);
}
.ftk-card-face {
  position: absolute;
  top: 0; left: 0; right: 0; bottom: 0;
  background: var(--md-default-bg-color);
  border-radius: 10px;
  border: 2px solid var(--md-primary-fg-color);
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  backface-visibility: hidden;
  -webkit-backface-visibility: hidden;
}
.ftk-card-face.ftk-back {
  transform: rotateY(180deg);
  border-color: #22c55e;
}
.ftk-card-tag {
  font-size: 0.72rem;
  color: var(--md-default-fg-color--light);
  background: var(--md-code-bg-color);
  padding: 0.15rem 0.5rem;
  border-radius: 99px;
  margin-bottom: 0.7rem;
  font-family: var(--md-code-font-family);
}
.ftk-card-term {
  font-size: 1.6rem;
  font-weight: 700;
  color: var(--md-default-fg-color);
  line-height: 1.2;
}
.ftk-card-hint {
  margin-top: 0.6rem;
  font-size: 0.8rem;
  color: var(--md-default-fg-color--light);
}
.ftk-card-def {
  font-size: 1.05rem;
  line-height: 1.55;
  color: var(--md-default-fg-color);
}
.ftk-card-repeats {
  margin-top: 0.6rem;
  font-size: 0.78rem;
  color: var(--md-default-fg-color--light);
}

/* Buttons */
.ftk-btn-row {
  display: flex;
  gap: 0.7rem;
  flex-wrap: wrap;
  margin-bottom: 0.8rem;
}
.ftk-btn {
  flex: 1 1 130px;
  padding: 0.7rem 1.2rem;
  font-size: 0.95rem;
  font-weight: 600;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: filter 0.15s;
  font-family: inherit;
}
.ftk-btn:hover { filter: brightness(1.1); }
.ftk-btn:disabled { opacity: 0.4; cursor: default; filter: none; }
.ftk-btn-show {
  background: var(--md-primary-fg-color);
  color: var(--md-primary-bg-color);
}
.ftk-btn-knew {
  background: #22c55e;
  color: #fff;
}
.ftk-btn-didnt {
  background: #ef4444;
  color: #fff;
}
.ftk-btn-reset {
  flex: none;
  padding: 0.5rem 1rem;
  font-size: 0.8rem;
  font-weight: 600;
  background: transparent;
  color: var(--md-default-fg-color--light);
  border: 1px solid var(--md-default-fg-color--lighter);
  border-radius: 6px;
  cursor: pointer;
  font-family: inherit;
}
.ftk-btn-reset:hover { color: #ef4444; border-color: #ef4444; }

/* No cards message */
.ftk-empty {
  text-align: center;
  padding: 2rem;
  color: var(--md-default-fg-color--light);
  font-size: 1rem;
}
</style>

<div class="ftk-widget" id="ftk-widget">

  <!-- Progress -->
  <div class="ftk-progress-wrap">
    <div class="ftk-progress-label">
      <span>Progress: <span id="ftk-learned-count">0</span> / <span id="ftk-total-count">105</span> o'rganildi</span>
      <span id="ftk-pct">0%</span>
    </div>
    <div class="ftk-progress-track">
      <div class="ftk-progress-bar" id="ftk-progress-bar" style="width:0%"></div>
    </div>
  </div>

  <!-- Stats -->
  <div class="ftk-stats">
    <div class="ftk-stat">
      <div class="ftk-stat-num" id="ftk-streak">0</div>
      <div class="ftk-stat-lbl">ketma-ket kun</div>
    </div>
    <div class="ftk-stat">
      <div class="ftk-stat-num" id="ftk-session-ok">0</div>
      <div class="ftk-stat-lbl">«Bildim» sessiyada</div>
    </div>
    <div class="ftk-stat">
      <div class="ftk-stat-num" id="ftk-session-fail">0</div>
      <div class="ftk-stat-lbl">«Bilmadim» sessiyada</div>
    </div>
    <div class="ftk-stat">
      <div class="ftk-stat-num" id="ftk-remaining">105</div>
      <div class="ftk-stat-lbl">hali o'rganilmagan</div>
    </div>
  </div>

  <!-- Filter -->
  <div class="ftk-filter-row">
    <label for="ftk-tag-select">Mavzu bo'yicha filtr:</label>
    <select id="ftk-tag-select">
      <option value="all">Barcha kartochkalar (105)</option>
    </select>
    <button class="ftk-btn-reset" id="ftk-reset-btn" title="Barcha kartochkalar bo'yicha progressni tiklash">Progressni tiklash</button>
  </div>

  <!-- Card area -->
  <div class="ftk-card-area" id="ftk-card-area">
    <div class="ftk-card" id="ftk-card">
      <div class="ftk-card-face ftk-front" id="ftk-front">
        <div class="ftk-card-tag" id="ftk-card-tag">...</div>
        <div class="ftk-card-term" id="ftk-card-term">Yuklanmoqda...</div>
        <div class="ftk-card-hint">«Javobni ko'rsatish» tugmasini bosing</div>
      </div>
      <div class="ftk-card-face ftk-back" id="ftk-back">
        <div class="ftk-card-tag" id="ftk-card-tag-back">...</div>
        <div class="ftk-card-def" id="ftk-card-def">...</div>
        <div class="ftk-card-repeats" id="ftk-card-repeats"></div>
      </div>
    </div>
  </div>

  <!-- Buttons -->
  <div class="ftk-btn-row" id="ftk-btn-row">
    <button class="ftk-btn ftk-btn-show" id="ftk-show-btn">Javobni ko'rsatish</button>
    <button class="ftk-btn ftk-btn-knew" id="ftk-knew-btn" disabled>Bildim ✓</button>
    <button class="ftk-btn ftk-btn-didnt" id="ftk-didnt-btn" disabled>Bilmadim ✗</button>
  </div>

  <div class="ftk-empty" id="ftk-empty" style="display:none">
    Bu mavzudagi barcha kartochkalar o'rganildi! Boshqa mavzuni tanlang yoki progressni tiklang.
  </div>

</div>

<script>
(function () {
  /* ─────────── данные карточек ─────────── */
  var CARDS = [
    {front:"Pip",back:"Narx o'zgarishining standart birligi. Odatda verguldan keyin 4-chi raqam. JPY juftliklari uchun — 2-chi raqam.",tags:["forex","basic"]},
    {front:"Lot",back:"Pozitsiya hajmining birligi. 1 standart lot = 100 000 asosiy valyuta. Mikrolot = 0.01.",tags:["forex","basic"]},
    {front:"Spread",back:"Ask va Bid o'rtasidagi farq. Har bir savdo uchun brokerga to'lov.",tags:["forex","basic"]},
    {front:"Bid",back:"Broker sizdan valyuta SOTIB OLADIGAN narx (siz sotadigan narx). Ask dan past.",tags:["forex","basic"]},
    {front:"Ask",back:"Broker sizga valyuta SOTADIGAN narx (siz sotib oladigan narx). Bid dan yuqori.",tags:["forex","basic"]},
    {front:"Leverage",back:"Kredit richagi. 1:30 → $100 depozit $3 000 pozitsiya ochishga imkon beradi. Foyda ham, zarar ham oshadi.",tags:["forex","basic"]},
    {front:"Margin",back:"Ochiq pozitsiya ostida muzlatilgan summa (garov sifatida).",tags:["forex","basic"]},
    {front:"Long",back:"Xarid. Narx oshishiga tikish.",tags:["forex","basic"]},
    {front:"Short",back:"Sotuv. Narx tushishiga tikish.",tags:["forex","basic"]},
    {front:"Stop Loss (SL)",back:"Belgilangan zarar bo'lganda pozitsiyani avtomatik yopadigan order. Har bir savdoda MAJBURIY.",tags:["forex","risk"]},
    {front:"Take Profit (TP)",back:"Belgilangan foyda bo'lganda pozitsiyani avtomatik yopadigan order.",tags:["forex","risk"]},
    {front:"Margin Call",back:"Brokerning erkin margin kam qolayotgani haqidagi ogohlantirishi. Tez orada majburiy yopish bo'ladi.",tags:["forex","risk"]},
    {front:"Stop Out",back:"Margin kritik darajaga tushganda broker tomonidan pozitsiyalarning majburiy yopilishi (odatda 20-50%).",tags:["forex","risk"]},
    {front:"Major",back:"USD bilan eng likvid valyuta juftliklari: EUR/USD, GBP/USD, USD/JPY, USD/CHF, AUD/USD, USD/CAD, NZD/USD.",tags:["forex","basic"]},
    {front:"Cross",back:"USDsiz valyuta jufti: EUR/GBP, EUR/JPY, GBP/JPY.",tags:["forex","basic"]},
    {front:"Exotic",back:"Rivojlanayotgan mamlakat valyutasi bilan juftlik: USD/TRY, USD/ZAR. Yangi boshlovchilar uchun XAVFLI.",tags:["forex","basic"]},
    {front:"Swap",back:"Pozitsiyani kechasi o'tkazish uchun komissiya. Musbat ham, manfiy ham bo'lishi mumkin.",tags:["forex","basic"]},
    {front:"Base currency",back:"Juftlikdagi birinchi valyuta. EUR/USD da asosiy = EUR.",tags:["forex","basic"]},
    {front:"Quote currency",back:"Juftlikdagi ikkinchi (kotirovka) valyuta. EUR/USD da kotirovka = USD.",tags:["forex","basic"]},
    {front:"OHLC",back:"Open, High, Low, Close — sham hosil qiluvchi to'rtta narx.",tags:["technical","candles"]},
    {front:"Bullish candle",back:"Ko'taruvchi sham: Close > Open. Yashil yoki oq.",tags:["technical","candles"]},
    {front:"Bearish candle",back:"Tushiruvchi sham: Close < Open. Qizil yoki qora.",tags:["technical","candles"]},
    {front:"Body",back:"Sham tanasi — Open va Close o'rtasidagi to'rtburchak.",tags:["technical","candles"]},
    {front:"Wick / Shadow",back:"Sham soyasi — tanadan yuqori va pastga, High va Low gacha cho'zilgan chiziqlar.",tags:["technical","candles"]},
    {front:"Hammer",back:"Bolg'a. Yuqorida kichik tana, uzun pastki soya. Pasayish oxirida ko'taruvchi burilish patterni.",tags:["technical","patterns"]},
    {front:"Shooting Star",back:"Uchuvchi yulduz. Pastda kichik tana, uzun yuqori soya. Tushiruvchi burilish patterni.",tags:["technical","patterns"]},
    {front:"Bullish Engulfing",back:"Ko'taruvchi qamrab olish. Katta yashil sham oldingi qizil shamning tanasini qoplab oladi. Yuqoriga burilish signali.",tags:["technical","patterns"]},
    {front:"Bearish Engulfing",back:"Tushiruvchi qamrab olish. Katta qizil sham oldingi yashil shamning tanasini qoplab oladi. Pastga burilish signali.",tags:["technical","patterns"]},
    {front:"Doji",back:"Open ≈ Close bo'lgan sham (kichik tana). Noaniqlik, ko'taruvchi/tushiruvchi kuchlar muvozanatda.",tags:["technical","patterns"]},
    {front:"Pin Bar",back:"Uzun soyali va kichik tanali sham. Soyaga qarama-qarshi yo'nalishda burilish signali.",tags:["technical","patterns"]},
    {front:"Uptrend",back:"Ko'tariluvchi trend. Ketma-ket yuqori maksimumlar (HH) va yuqori minimumlar (HL).",tags:["technical","trends"]},
    {front:"Downtrend",back:"Tushuvchi trend. Ketma-ket past maksimumlar (LH) va past minimumlar (LL).",tags:["technical","trends"]},
    {front:"Range / Flat",back:"Yonak / flat. Narx gorizontal koridorda harakat qiladi.",tags:["technical","trends"]},
    {front:"Support",back:"Qo'llab-quvvatlash. Narx undan yuqoriga sakrab chiqqan daraja.",tags:["technical","levels"]},
    {front:"Resistance",back:"Qarshilik. Narx undan pastga sakrab tushgan daraja.",tags:["technical","levels"]},
    {front:"Breakout",back:"Qo'llab-quvvatlash yoki qarshilik darajasini yorib o'tish.",tags:["technical","levels"]},
    {front:"Retest",back:"Narxning yorib o'tilgan darajaga qaytib tasdiqlashi.",tags:["technical","levels"]},
    {front:"Pullback / Retracement",back:"Orqaga chekinish. Asosiy trendga qarshi vaqtinchalik harakat.",tags:["technical","trends"]},
    {front:"EMA",back:"Exponential Moving Average. Eksponensial skользящее o'rtacha. So'nggi shamlar eski shamlardan ko'proq og'irlikka ega.",tags:["technical","indicators"]},
    {front:"SMA",back:"Simple Moving Average. N davr uchun yopilish narxlarining oddiy o'rtachasi.",tags:["technical","indicators"]},
    {front:"EMA 200",back:"Asosiy yo'nalish filtri: narx EMA200 dan yuqorida = faqat long, pastda = faqat short.",tags:["technical","indicators"]},
    {front:"RSI",back:"Relative Strength Index. 0-100 oscillyatori. >70 = ortiqcha sotib olingan, <30 = ortiqcha sotilgan.",tags:["technical","indicators"]},
    {front:"MACD",back:"Trend + momentum indikatori. MACD = EMA(12) − EMA(26). Signallar: kesishishlar, divergensiya.",tags:["technical","indicators"]},
    {front:"Bollinger Bands",back:"Bollinger tasmalari. O'rtacha + 2 standart og'ish. Narx vaqtning 95% da tasma orasida bo'ladi.",tags:["technical","indicators"]},
    {front:"ATR",back:"Average True Range. O'rtacha sham hajmi. Stop-losslarni o'rnatishga yordam beradi.",tags:["technical","indicators"]},
    {front:"Divergence",back:"Narx va indikator o'rtasidagi tafovut: narx yangi ekstremal nuqtaga yetadi, indikator esa yo'q. Zaiflashuv signali.",tags:["technical","patterns"]},
    {front:"Head and Shoulders",back:"Bosh va yelkalar. Tepa burilish patterni: chap yelka → bosh (yuqoriroq) → o'ng yelka.",tags:["technical","patterns"]},
    {front:"Double Top",back:"Ikki marta tepa. Narx darajani ikki marta yorib o'tolmaydi, keyin pastga buriladi.",tags:["technical","patterns"]},
    {front:"Triangle",back:"Uchburchak. Ko'tariluvchi = ko'pincha yuqoriga yorilib chiqadi. Tushuvchi = ko'pincha pastga. Simmetrik = oldindan aytib bo'lmaydi.",tags:["technical","patterns"]},
    {front:"Flag",back:"Bayroq. Trend davomi patterni: kuchli impuls + qisqa konsolidatsiya.",tags:["technical","patterns"]},
    {front:"Fibonacci",back:"Orqaga chekinish darajalari: 23.6%, 38.2%, 50%, 61.8%, 78.6%. Orqaga chekinishda kirish zonalari sifatida ishlatiladi.",tags:["technical","levels"]},
    {front:"Risk Reward (R:R)",back:"Xavf va foyda nisbati. R:R 1:2 = $1 xavf uchun $2 foydaga mo'ljallash. Yangi boshlovchi uchun minimum: 1:2.",tags:["risk","basic"]},
    {front:"Win Rate",back:"Foydali savdolar ulushi. R:R 1:2 da ≥ 40% yaxshi.",tags:["risk","metrics"]},
    {front:"Profit Factor",back:"Jami foydalar / Jami zararlar. ≥ 1.5 yaxshi.",tags:["risk","metrics"]},
    {front:"Expectancy",back:"Bir savdoning kutilgan natijasi: (WR × O'rtacha foyda) − (LR × O'rtacha zarar). > 0 bo'lishi kerak.",tags:["risk","metrics"]},
    {front:"Drawdown",back:"Cho'kish. Balansning maksimumdan og'ishi.",tags:["risk","metrics"]},
    {front:"Max Drawdown",back:"Davr uchun maksimal cho'kish. Depozitning < 15% = yaxshi.",tags:["risk","metrics"]},
    {front:"R (Risk Unit)",back:"Bir savdodagi xavf birligi. Agar $5 xavf qo'ysangiz — bu 1R. +2R = +$10.",tags:["risk","metrics"]},
    {front:"Equity",back:"Joriy hisob balansi + ochiq savdolarning suzuvchi natijasi.",tags:["risk","metrics"]},
    {front:"Equity Curve",back:"Vaqt bo'yicha equity o'zgarishi grafigi. Strategiyaning asosiy vizual ko'rsatkichi.",tags:["risk","metrics"]},
    {front:"1% Rule",back:"Qoida: bir savdodagi xavf ≤ depozitning 1%. Yangi boshlovchi uchun 0.5% yaxshiroq.",tags:["risk","management"]},
    {front:"Tilt",back:"Tilt. Zarar bo'lgandan keyingi psixologik holat: g'azab, o'ch olishga intilish. Depozitlarning asosiy qotili.",tags:["psychology","basic"]},
    {front:"FOMO",back:"Fear of Missing Out. Harakatni o'tkazib yuborish qo'rquvi. Signal bo'lmasdan kirish imkonini beradi.",tags:["psychology","basic"]},
    {front:"Averaging Down",back:"Zarar pozitsiyani burilishga umid qilib o'rtalashtirish. XAVFLI usul, yangi boshlovchilarga taqiqlangan.",tags:["psychology","management"]},
    {front:"Demo Account",back:"Haqiqiy kotirovkalardagi virtual pullik hisob. O'qitishning majburiy bosqichi — 2-3 oy.",tags:["basic","broker"]},
    {front:"Live Account",back:"Haqiqiy pullik hisob. Faqat demoda barqaror musbat natijadan keyin o'tish kerak.",tags:["basic","broker"]},
    {front:"Cent Account",back:"Balans sentlarda bo'lgan hisob. $10 = 1000 sent. Mikro-mashq uchun mos.",tags:["basic","broker"]},
    {front:"ECN Account",back:"Orderlarni to'g'ridan-to'g'ri bozorga chiqarish. Tor spread + komissiya. Tajribalillar uchun.",tags:["basic","broker"]},
    {front:"Market Order",back:"Joriy bozor narxida bajarilish uchun order.",tags:["basic","orders"]},
    {front:"Limit Order",back:"Joriy narxdan past sotib olish / yuqori sotish uchun kechiktirilgan order.",tags:["basic","orders"]},
    {front:"Stop Order",back:"Joriy narxdan yuqori sotib olish / past sotish uchun kechiktirilgan order (yorib chiqish uchun).",tags:["basic","orders"]},
    {front:"Slippage",back:"Sirpanish. Haqiqiy bajarilish narxi kutilganidan farq qiladi. Ayniqsa yangiliklar paytida.",tags:["basic","orders"]},
    {front:"Liquidity",back:"Likvidlik. Narxni sezilarli o'zgartirmay sotib olish/sotish qanchalik oson.",tags:["basic","market"]},
    {front:"Volatility",back:"Volatillik. Davr uchun narx tebranishlarining amplitudasi.",tags:["basic","market"]},
    {front:"NFP",back:"Non-Farm Payrolls. AQSHda bandlik. Oyning birinchi juma kuni. Oyning eng muhim yangiligi.",tags:["fundamental","news"]},
    {front:"FOMC",back:"Federal Open Market Committee. FRS stavkalar bo'yicha majlisi. Yiliga 8 marta.",tags:["fundamental","news"]},
    {front:"CPI",back:"Consumer Price Index. Iste'mol narxlari indeksi (inflyatsiya).",tags:["fundamental","news"]},
    {front:"GDP",back:"Gross Domestic Product. Yalpi ichki mahsulot.",tags:["fundamental","news"]},
    {front:"Interest Rate",back:"Markaziy bank foiz stavkasi. Stavka qanchalik yuqori — valyuta shunchalik kuchli (soddalashtirilgan).",tags:["fundamental","news"]},
    {front:"Carry Trade",back:"Strategiya: yuqori stavkali valyutani past stavkali valyutaga qarshi sotib olish. Swaplardan daromad.",tags:["fundamental","strategy"]},
    {front:"Hedging",back:"Xejjing. Xavfdan himoya uchun qarama-qarshi pozitsiya ochish.",tags:["risk","management"]},
    {front:"Diversification",back:"Diversifikatsiya. Xavfni turli aktivlar bo'yicha taqsimlash.",tags:["risk","management"]},
    {front:"Money Management (MM)",back:"Kapital boshqaruvi: pozitsiya hajmi, xavf, diversifikatsiya.",tags:["risk","management"]},
    {front:"Trailing Stop",back:"Foydali tomonga narx bilan harakatlanadigan, lekin orqaga qaytmaydigan stop.",tags:["risk","orders"]},
    {front:"Break-even",back:"Zararsizlik. Savdoni nolga yopish yoki stopni kirish narxiga ko'chirish.",tags:["risk","orders"]},
    {front:"Scalping",back:"Skalping. Kichik foydalar bilan M1-M5 da savdo. Stressli, yangi boshlovchilar uchun emas.",tags:["style","trading"]},
    {front:"Day Trading",back:"Kunlik savdo. Savdolar savdo kuni davomida yopiladi.",tags:["style","trading"]},
    {front:"Swing Trading",back:"Sving-treyding. Bir necha soatdan bir necha kungacha savdolar.",tags:["style","trading"]},
    {front:"Position Trading",back:"Pozitsion savdo. Savdolar haftalar-oylar davomida ushlab turiladi.",tags:["style","trading"]},
    {front:"Backtest",back:"Bektest. Strategiyani tarixiy ma'lumotlarda tekshirish.",tags:["strategy","testing"]},
    {front:"Forward Test",back:"Forward-test. Strategiyani real vaqtda demoda tekshirish.",tags:["strategy","testing"]},
    {front:"Walk-Forward",back:"Walk-forward optimallashtirish. Parametrlarni tarixning bir qismida tanlash, keyingisida tekshirish.",tags:["strategy","testing"]},
    {front:"Overfitting",back:"Ortiqcha moslashtirish. Strategiya tarixga haddan tashqari moslanib, yangi ma'lumotlarda ishlamaydi.",tags:["strategy","testing"]},
    {front:"Expert Advisor (EA)",back:"MT4/MT5 uchun savdo maslahatchi. Avtomatik bot.",tags:["technology","bots"]},
    {front:"MQL5",back:"MetaTrader 5 da EA yozish uchun dasturlash tili.",tags:["technology","bots"]},
    {front:"API",back:"Brokerga ulanish uchun dasturiy interfeys (masalan, MetaTrader 5 Python API).",tags:["technology","bots"]},
    {front:"Spread Cost",back:"Spread qiymati. EUR/USD da 1 piplik spread = har bir standart lot uchun $1.",tags:["risk","costs"]},
    {front:"Pip Value",back:"1 pipning qiymati. EUR/USD da 1 standart lot uchun ≈ $10. 0.01 lot uchun ≈ $0.10.",tags:["basic","costs"]},
    {front:"Lot Size",back:"Pozitsiya hajmi. Formula bo'yicha hisoblanadi: (Depozit × Xavf%) / (Stop pipsda × Pip qiymati).",tags:["risk","management"]},
    {front:"Trading Session",back:"Savdo sessiyasi. London (10:00-19:00 UTC+3), Amerika (14:00-23:00 UTC+3).",tags:["basic","time"]},
    {front:"Asian Session",back:"Osiyo sessiyasi (02:00-11:00 UTC+3). Past likvidlik. Yangi boshlovchilar o'tkazib yuborishi yaxshi.",tags:["basic","time"]},
    {front:"Sniper Entry",back:"Snayper kirish. Qoidalarga ko'ra ideal kirish nuqtasini sabr bilan kutish.",tags:["psychology","patience"]},
    {front:"Trading Plan",back:"Savdo rejasi. Yozilgan qoidalar: nima, qachon, qanday savdo qilish.",tags:["psychology","discipline"]},
    {front:"Trading Journal",back:"Savdolar jurnali. Har bir savdoni yozib borish. O'sishning asosiy vositasi.",tags:["psychology","discipline"]}
  ];

  /* ─────────── константы ─────────── */
  var LEARNED_THRESHOLD = 3; // сколько раз подряд нужно ответить «Знал»

  /* ─────────── localStorage helpers ─────────── */
  function getState(idx) {
    /* returns {streak: number} — количество успешных повторов подряд */
    try {
      var raw = localStorage.getItem('ftk-flash-' + idx);
      if (raw) return JSON.parse(raw);
    } catch(e) {}
    return {streak: 0};
  }

  function setState(idx, obj) {
    try { localStorage.setItem('ftk-flash-' + idx, JSON.stringify(obj)); } catch(e) {}
  }

  function getSessionStats() {
    try {
      var raw = localStorage.getItem('ftk-flash-session');
      if (raw) return JSON.parse(raw);
    } catch(e) {}
    return {ok: 0, fail: 0};
  }

  function setSessionStats(obj) {
    try { localStorage.setItem('ftk-flash-session', JSON.stringify(obj)); } catch(e) {}
  }

  function getStreak() {
    var streak = 0;
    var lastDay = '';
    try {
      streak = parseInt(localStorage.getItem('ftk-flash-streak') || '0', 10);
      lastDay = localStorage.getItem('ftk-flash-lastday') || '';
    } catch(e) {}
    return {streak: streak, lastDay: lastDay};
  }

  function touchStreak() {
    var today = new Date().toISOString().slice(0, 10);
    var s = getStreak();
    if (s.lastDay === today) return; // уже отметились сегодня
    var yesterday = new Date(Date.now() - 86400000).toISOString().slice(0, 10);
    var newStreak = (s.lastDay === yesterday) ? s.streak + 1 : 1;
    try {
      localStorage.setItem('ftk-flash-streak', String(newStreak));
      localStorage.setItem('ftk-flash-lastday', today);
    } catch(e) {}
  }

  /* ─────────── SM-2-подобный приоритет ─────────── */
  /*
    Алгоритм: каждой карточке сопоставляем «приоритет»:
      - streak=0 → самый высокий приоритет (не начато)
      - 1 ≤ streak < LEARNED_THRESHOLD → средний (в процессе)
      - streak ≥ LEARNED_THRESHOLD → низкий (выучено), но изредка повторяем
    Среди карточек одного уровня — случайный порядок.
    Отбираем карточки, соответствующие выбранному тегу/фильтру.
  */
  function pickNext(activeIndices, lastIdx) {
    if (activeIndices.length === 0) return -1;

    var buckets = [[], [], []]; // [не начато/сброшено, в процессе, выучено]
    activeIndices.forEach(function(i) {
      if (i === lastIdx) return; // не повторяем ту же карточку подряд
      var s = getState(i).streak;
      if (s <= 0) buckets[0].push(i);
      else if (s < LEARNED_THRESHOLD) buckets[1].push(i);
      else buckets[2].push(i);
    });

    // если есть хоть одна карточка в первых двух бакетах — берём оттуда
    var pool = buckets[0].length > 0 ? buckets[0]
             : buckets[1].length > 0 ? buckets[1]
             : buckets[2];

    // если все исключены из-за lastIdx — включаем lastIdx обратно
    if (pool.length === 0) pool = activeIndices;

    return pool[Math.floor(Math.random() * pool.length)];
  }

  /* ─────────── фильтр по тегам ─────────── */
  // Собираем уникальные теги
  var tagSet = {};
  var tagLabelMap = {
    'forex':        'Forex: asoslar',
    'technical':    'Texnik tahlil',
    'risk':         'Risk-menejment',
    'psychology':   'Psixologiya',
    'fundamental':  'Fundamental tahlil',
    'basic':        'Asosiy tushunchalar',
    'strategy':     'Strategiya va testlash',
    'style':        'Savdo uslubi',
    'technology':   'Texnologiyalar (EA, API)',
    'candles':      'Sham tahlili',
    'patterns':     'Patternlar',
    'trends':       'Trendlar',
    'levels':       'Darajalar',
    'indicators':   'Indikatorlar',
    'management':   'Kapital boshqaruvi',
    'metrics':      'Metrikalar',
    'orders':       'Orderlar',
    'news':         'Yangiliklar (Fundamental)',
    'broker':       'Hisob turlari',
    'bots':         'Botlar va avtomatizatsiya',
    'costs':        'Xarajatlar',
    'time':         'Savdo sessiyalari',
    'testing':      'Strategiyalarni testlash',
    'discipline':   'Intizom',
    'patience':     'Sabr va kirish'
  };

  CARDS.forEach(function(c) {
    c.tags.forEach(function(t) { tagSet[t] = true; });
  });

  var tagSelect = document.getElementById('ftk-tag-select');
  Object.keys(tagSet).sort().forEach(function(t) {
    var count = CARDS.filter(function(c){ return c.tags.indexOf(t) !== -1; }).length;
    var opt = document.createElement('option');
    opt.value = t;
    opt.textContent = (tagLabelMap[t] || t) + ' (' + count + ')';
    tagSelect.appendChild(opt);
  });

  /* ─────────── состояние виджета ─────────── */
  var currentFilter = 'all';
  var activeIndices = [];
  var currentIdx = -1;
  var isFlipped = false;
  var sessionOk = 0;
  var sessionFail = 0;

  /* ─────────── DOM-ссылки ─────────── */
  var elCard        = document.getElementById('ftk-card');
  var elFront       = document.getElementById('ftk-front');
  var elBack        = document.getElementById('ftk-back');
  var elCardTag     = document.getElementById('ftk-card-tag');
  var elCardTagBack = document.getElementById('ftk-card-tag-back');
  var elCardTerm    = document.getElementById('ftk-card-term');
  var elCardDef     = document.getElementById('ftk-card-def');
  var elCardRep     = document.getElementById('ftk-card-repeats');
  var elShowBtn     = document.getElementById('ftk-show-btn');
  var elKnewBtn     = document.getElementById('ftk-knew-btn');
  var elDidntBtn    = document.getElementById('ftk-didnt-btn');
  var elEmpty       = document.getElementById('ftk-empty');
  var elCardArea    = document.getElementById('ftk-card-area');
  var elLearnedCount= document.getElementById('ftk-learned-count');
  var elTotalCount  = document.getElementById('ftk-total-count');
  var elPct         = document.getElementById('ftk-pct');
  var elProgressBar = document.getElementById('ftk-progress-bar');
  var elStreakNum    = document.getElementById('ftk-streak');
  var elSessionOk   = document.getElementById('ftk-session-ok');
  var elSessionFail = document.getElementById('ftk-session-fail');
  var elRemaining   = document.getElementById('ftk-remaining');

  /* ─────────── вычислить активные индексы по фильтру ─────────── */
  function rebuildActive() {
    if (currentFilter === 'all') {
      activeIndices = CARDS.map(function(_, i){ return i; });
    } else {
      activeIndices = CARDS.reduce(function(acc, c, i){
        if (c.tags.indexOf(currentFilter) !== -1) acc.push(i);
        return acc;
      }, []);
    }
  }

  /* ─────────── обновить счётчики и прогресс ─────────── */
  function updateStats() {
    var learned = CARDS.filter(function(_, i){
      return getState(i).streak >= LEARNED_THRESHOLD;
    }).length;
    var total = CARDS.length;
    var pct = Math.round(learned / total * 100);

    elLearnedCount.textContent = learned;
    elTotalCount.textContent   = total;
    elPct.textContent          = pct + '%';
    elProgressBar.style.width  = pct + '%';

    var activeLearnedCount = activeIndices.filter(function(i){
      return getState(i).streak >= LEARNED_THRESHOLD;
    }).length;
    elRemaining.textContent = activeIndices.length - activeLearnedCount;

    var s = getStreak();
    elStreakNum.textContent = s.streak;
    elSessionOk.textContent   = sessionOk;
    elSessionFail.textContent = sessionFail;
  }

  /* ─────────── показать карточку ─────────── */
  function showCard(idx) {
    if (idx < 0) {
      // пустой результат (все выучены в этой теме)
      elCardArea.style.display = 'none';
      document.getElementById('ftk-btn-row').style.display = 'none';
      elEmpty.style.display = 'block';
      return;
    }
    elCardArea.style.display = '';
    document.getElementById('ftk-btn-row').style.display = '';
    elEmpty.style.display = 'none';

    var card = CARDS[idx];
    var tagLabel = card.tags.map(function(t){ return tagLabelMap[t] || t; }).join(' · ');
    var s = getState(idx);

    elCardTag.textContent     = tagLabel;
    elCardTagBack.textContent = tagLabel;
    elCardTerm.textContent    = card.front;
    elCardDef.textContent     = card.back;

    var streakTxt = s.streak >= LEARNED_THRESHOLD
      ? '✅ O\'rganildi (' + s.streak + ' marta ketma-ket)'
      : s.streak > 0
        ? '🔄 Ketma-ket takrorlash: ' + s.streak + ' / ' + LEARNED_THRESHOLD
        : '🆕 Yangi kartochka';
    elCardRep.textContent = streakTxt;

    // убираем флип без анимации
    elCard.style.transition = 'none';
    elCard.classList.remove('flipped');
    void elCard.offsetWidth; // reflow
    elCard.style.transition = '';

    isFlipped = false;
    elShowBtn.disabled  = false;
    elKnewBtn.disabled  = true;
    elDidntBtn.disabled = true;
  }

  /* ─────────── события кнопок ─────────── */
  elShowBtn.addEventListener('click', function() {
    if (isFlipped) return;
    elCard.classList.add('flipped');
    isFlipped = true;
    elShowBtn.disabled  = true;
    elKnewBtn.disabled  = false;
    elDidntBtn.disabled = false;
    touchStreak(); // отметим день как активный
    updateStats();
  });

  elKnewBtn.addEventListener('click', function() {
    if (!isFlipped || currentIdx < 0) return;
    var s = getState(currentIdx);
    s.streak = (s.streak || 0) + 1;
    setState(currentIdx, s);
    sessionOk++;
    advance();
  });

  elDidntBtn.addEventListener('click', function() {
    if (!isFlipped || currentIdx < 0) return;
    setState(currentIdx, {streak: 0});
    sessionFail++;
    advance();
  });

  function advance() {
    updateStats();
    var next = pickNext(activeIndices, currentIdx);
    currentIdx = next;
    showCard(next);
  }

  /* ─────────── фильтр ─────────── */
  tagSelect.addEventListener('change', function() {
    currentFilter = tagSelect.value;
    rebuildActive();
    currentIdx = -1;
    advance();
  });

  /* ─────────── сброс прогресса ─────────── */
  document.getElementById('ftk-reset-btn').addEventListener('click', function() {
    if (!confirm('Barcha kartochkalar progressini tiklashni xohlaysizmi? Bu brauzerdan barcha natijalarni o\'chiradi.')) return;
    for (var i = 0; i < CARDS.length; i++) {
      try { localStorage.removeItem('ftk-flash-' + i); } catch(e) {}
    }
    try {
      localStorage.removeItem('ftk-flash-streak');
      localStorage.removeItem('ftk-flash-lastday');
      localStorage.removeItem('ftk-flash-session');
    } catch(e) {}
    sessionOk   = 0;
    sessionFail = 0;
    currentIdx  = -1;
    rebuildActive();
    advance();
  });

  /* ─────────── инициализация ─────────── */
  rebuildActive();
  currentIdx = pickNext(activeIndices, -1);
  showCard(currentIdx);
  updateStats();

}());
</script>

---

## To'g'ri mashq qilish usuli

1. **Har kuni 10-15 daqiqa** — haftada bir marta bir soatdan yaxshiroq.
2. **Halol bo'ling**: «Bildim» tugmasini faqat kartochkani ag'darishdan oldin ta'rifni rostdan eslagan bo'lsangiz bosing.
3. **Algoritm o'zi ustuvorliklarni belgilaydi**: nol strikli kartochkalar eng ko'p ko'rsatiladi.
4. **Maqsad**: 105/105 kartochka ketma-ket 3+ to'g'ri javob bilan.

!!! tip "Kartochkalardan keyingi qadam"
    Barcha atamalarni bilgach — strategiya matematikasini tushunish uchun [WinRate × RR kalkulyatoriga](winrate-rr-calculator.md) o'ting.

---

## Interval takrorlash algoritmi (qisqacha)

Trenajyor SM-2 ning soddalashtirilgan versiyasini ishlatadi:

| Kartochka holati | Ko'rsatilish tartibi |
|---|---|
| Hech qachon javob berilmagan / tiklangan | Birinchi navbatda |
| Ketma-ket 1-2 to'g'ri javob | Ikkinchi navbatda |
| Ketma-ket 3+ to'g'ri javob (o'rganilgan) | Kamdan-kam, mustahkamlash uchun |

Progress brauzeringizning `localStorage` da saqlanadi — sessiyalar o'rtasida saqlanadi, lekin qurilmalar o'rtasida sinxronlanmaydi.

---

!!! info "O'quv materiali"
    Bu sahifa forex treydingidan o'quv qo'llanmasining bir qismidir. Moliyaviy maslahat emas.
