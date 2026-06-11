# 🎯 Kviz: real savdoga tayyormisiz?

!!! abstract "Qanday ishlaydi"
    Forex asoslari, risk-menejment va psixologiya bo'yicha 18 ta savol. Har bir
    javobdan keyin — **nima uchun** shunday ekanligiga qisqa tushuntirish. Oxirida
    foiz va xulosa olasiz. Eng yaxshi natija brauzerda saqlanadi.

    **Bu «bozor dahosi» uchun imtihon emas.** Bu — omon qolgan yangi boshlovchilarni
    birinchi oyda depozitini yo'qotganlardan ajratib turuvchi narsalarni
    o'zlashtirgansiz yoki yo'qligini tekshirish.

!!! warning "O'quv materiali — moliyaviy maslahat emas"
    To'g'ri javoblar risk-menejment tamoyillarini aks ettiradi, foydani kafolatlamaydi.
    Forexda savdo katta yo'qotish xavfi bilan bog'liq.

---

<div class="quiz-widget calc-widget">
  <div id="quiz-start">
    <p class="quiz-best" id="quiz-best"></p>
    <button class="calc-button" onclick="quizStart()">▶ Kvizni boshlash (18 ta savol)</button>
  </div>

  <div id="quiz-play" style="display:none">
    <div class="quiz-progress">
      <span id="quiz-counter"></span>
      <span id="quiz-score"></span>
    </div>
    <div class="quiz-bar-track"><div class="quiz-bar-fill" id="quiz-bar"></div></div>
    <h3 class="quiz-question" id="quiz-question"></h3>
    <div class="quiz-options" id="quiz-options"></div>
    <div class="quiz-explain" id="quiz-explain" style="display:none"></div>
    <button class="calc-button" id="quiz-next" style="display:none" onclick="quizNext()">Keyingisi →</button>
  </div>

  <div id="quiz-result" style="display:none"></div>
</div>

<script>
const QUIZ = [
  {
    q: "Yangi boshlovchi uchun bir savdodagi maksimal ruxsat etilgan xavf qancha?",
    options: ["Depozitning 0.5–1%", "Depozitning 5–10%", "Barcha erkin qoldiq", "Savdoga ishonch darajasiga qarab"],
    correct: 0,
    explain: "Yangi boshlovchi uchun — savdoga 0.5–1%. 1% xavfda ketma-ket 10 ta yo'qotish ham depozitning atigi ~10% ini oladi va hisob bir qator muvaffaqiyatsizliklardan omon qoladi. 5–10% yomon bir haftada depozitni yo'q qiladi."
  },
  {
    q: "Savdoga kirishdan OLDIN nima albatta qo'yilishi kerak?",
    options: ["Imkon qadar katta Take Profit", "Stop-loss", "1:500 kredit richagi", "Telegram bildirishnomalari"],
    correct: 1,
    explain: "Stop-loss — bu sizning xato qilganingizni tan olish haqidagi oldindan qabul qilingan qaror. Usiz bozorning bitta burilishi hisobni nolga tushirishi mumkin. Stop kirish DAN OLDIN qo'yiladi, «vaziyatga qarab» emas."
  },
  {
    q: "Real pulga o'tishdan oldin demo-da kamida qancha savdo qilish kerak?",
    options: ["Bir-ikki kun", "Bir hafta", "Kamida 3 oy", "Demo — vaqt isrof"],
    correct: 2,
    explain: "Jurnal bilan kamida 3 oy barqaror demo-savdo. Demo platforma mexanikasini va intizomni pulni yo'qotmay o'rgatadi. Realga shoshilish — eng keng tarqalgan xato."
  },
  {
    q: "Win Rate 45%, RR (risk-mukofot) 1:2. Strategiya uzoq muddatda…",
    options: ["Zararli — g'alabalar kam", "Matematik jihatdan foydali", "Neytral", "Omilga bog'liq"],
    correct: 1,
    explain: "EV = 0.45×2 − 0.55×1 = +0.35R savdoga. RR 1:2 da foyda ko'rish uchun savdolarning ~34% ini yutish kifoya. Win Rate o'z-o'zicha RR siz hech narsani anglatmaydi."
  },
  {
    q: "Broker «oyiga 30% kafolatlangan foyda» va'da qilmoqda. Bu…",
    options: ["Ajoyib imkoniyat", "Firibgarlik belgisi", "Forex uchun norma", "Faqat VIP-mijozlar uchun"],
    correct: 1,
    explain: "Bozorda kafolatlangan foyda mavjud emas. Chakana treyderlarning 74–89% pul yo'qotadi. Har qanday «daromad kafolati» — firibgarlikning qizil bayrog'i."
  },
  {
    q: "Katta kredit richagi (1:500) nima uchun kerak?",
    options: ["Ko'proq daromad olish uchun", "U xavfli — zararni ham kuchaytiradi", "Savdo uchun majburiy", "Xavfni kamaytiradi"],
    correct: 1,
    explain: "Richag HAM foydani, HAM zararni kuchaytiradi. Xavfni pozitsiya hajmi va stop boshqaradi, richag emas. Katta richag depozitdan katta pozitsiya ochishga imkon beradi — va uni tezroq yo'qotishga."
  },
  {
    q: "Narx stopga yaqin keldi, lekin «hozir buriladi» deb o'ylayapsiz. Nima qilish kerak?",
    options: ["Stopni naridan uzaytirish", "Hech narsa — stop bu stop", "Pozitsiyani qo'shish (o'rtalashtirish)", "Stopni qo'lda olib tashlash"],
    correct: 1,
    explain: "Stopni o'z zararingizga qarab siljitish katta zararga olib boradi. Stop — sizning oldindan qabul qilingan qoidangiz. «Hozir buriladi» — bu umid, tahlil emas."
  },
  {
    q: "Savdo jurnalining asosiy maqsadi nima?",
    options: ["Foydani ko'z-ko'z qilish", "O'zingizning takrorlanuvchi xatolaringizni topish", "Brokerning talabi", "Soliqlarni hisoblash"],
    correct: 1,
    explain: "Jurnal patternlarni ko'rsatadi: qaysi vaqtda, qaysi juftliklarda, qaysi kayfiyatda pul yo'qotishingizni. Jurnalsiz bir xil xatolarni qayta-qayta takrorlaysiz va buni sezmaysiz."
  },
  {
    q: "Ketma-ket 3 ta savdoda yutqazdingiz va katta pozitsiya bilan «qaytarib olmoqchi» bo'lyapsiz. Bu…",
    options: ["Oqilona reja", "Tilt — to'xtatish signali", "Oddiy risk-menejment", "Martingayl strategiyasi, u ishlaydi"],
    correct: 1,
    explain: "Qaytarib olish istagi (revenge trading) tilt holatida depozitlarni yo'q qiladi. Bir qator yo'qotishlardan keyin to'g'ri yo'l — hajmni kamaytirish yoki tanaffus olish, stavkani oshirish emas."
  },
  {
    q: "Depozit 50% ga tushdi. Boshqa nuqtaga qaytish uchun qancha daromad kerak?",
    options: ["50%", "75%", "100%", "25%"],
    correct: 2,
    explain: "Drawdown matematikasi murosasiz: −50% qayta tiklash uchun +100% talab qiladi. Shuning uchun kapitalini himoya qilish foydani quvib yetishdan muhimroq — katta drawdownlarni deyarli qoplayb bo'lmaydi."
  },
  {
    q: "Muhim yangilik (NFP, FED yig'ilishi) oldidan spred kengayadi va narx keskin harakat qiladi. Yangi boshlovchiga yaxshisi…",
    options: ["To'la pozitsiya bilan kirish", "Kirishdan saqlanish", "Stop-losslarni olib tashlash", "RichaGni oshirish"],
    correct: 1,
    explain: "Yangilik chiqish paytida keskin harakatlar va siljishlar stoplarni eng yomon narxda urib chiqaradi. Muhim yangiliklar oldidan va keyin bir necha daqiqa savdo qilmaslik yangi boshlovchi uchun xavfsizroq."
  },
  {
    q: "Brokerni qanday tanlash kerak?",
    options: ["Depozit bonusining hajmiga qarab", "Regulyator litsenziyasi mavjudligiga qarab (FCA, CySEC, ASIC)", "Chiroyli reklamaga qarab", "Va'da qilingan 1:1000 richaGga qarab"],
    correct: 1,
    explain: "Asosiysi — regulyatsiya. FCA/CySEC/ASIC litsenziyasi mijozlar mablag'larini ajratish va nazoratni bildiradi. Bonuslar va katta richag — ko'pincha litsenziyasiz kompaniyalarda marketing."
  },
  {
    q: "Depozit $1000, xavf 1%, stop 25 pips, EUR/USD ($10/pip lotga). Pozitsiya hajmi?",
    options: ["0.04 lot", "0.4 lot", "1 lot", "0.004 lot"],
    correct: 0,
    explain: "Xavf = $10. Lot = 10 / (25 × 10) = 0.04. Avval pullarda ruxsat etilgan xavfni hisoblaysiz, keyin — stopdan pozitsiya hajmini. Hech qachon teskari emas."
  },
  {
    q: "Risk-menejmentda R (1R) nima?",
    options: ["Foyda hajmi", "Savdodagi xavfingiz miqdori (stopgacha bo'lgan masofa)", "Kredit richagi", "Spred hajmi"],
    correct: 1,
    explain: "1R — xavf birligi, sizning stop-lossing giz pullarda. Foydani R da o'lchash qulay: +2R «xavf qilgandan ikki baravar ko'p oldim» degani. Bu savdolarni hajmidan qat'iy nazar taqqoslanadigan qiladi."
  },
  {
    q: "Tarixdagi backtest +200% ko'rsatdi. Bu nimani anglatadi…",
    options: ["Realda ham shunday bo'ladi", "O'tgan narsa kelajakni kafolatlamaydi, real odatda yomonroq", "Hoziroq realga o'tish mumkin", "Strategiya mukammal"],
    correct: 1,
    explain: "Backtest psixologiyani, siljishlarni, bozor o'zgarishini va ortiqcha moslashtirish xavfini (overfitting) hisobga olmaydi. Real natija deyarli har doim yomonroq. Backtest — yomon g'oyalar filtri, foyda va'dasi emas."
  },
  {
    q: "Ijara/ovqat uchun ajratilgan pullarga savdo qilish mumkinmi?",
    options: ["Ha, agar savdoga ishonchli bo'lsangiz", "Qat'iyan yo'q", "Faqat yarmiga", "Agar richag kichik bo'lsa"],
    correct: 1,
    explain: "Faqat yo'qotilsa ham hayotingizga ta'sir qilmaydigan pullarga savdo qiling. «Tirikchilik pullari» intizomni buzadigan hissiy bosim yaratadi."
  },
  {
    q: "Foydali savdo musbat tomonga ketdi. Stopni zararsizklikka (BE) qachon siljitish kerak?",
    options: ["Kirishdan darhol", "Narx siz tomonda ma'qul masofani bosib o'tganda", "Hech qachon siljitmaslik", "Qo'rquv paydo bo'lganda"],
    correct: 1,
    explain: "Muhim darajadan o'tgandan keyin zararsizklikka ko'chirish foydani himoya qiladi va xavfni olib tashlaydi. Lekin juda erta BE (boshida) oddiy narx tebranishlarida chiqarib yuboradi."
  },
  {
    q: "Yangi boshlovchilar pul yo'qotishining asosiy sababi…",
    options: ["Yomon indikatorlar", "Intizom va risk-menejmentning yo'qligi", "Kichik depozit", "Noto'g'ri broker"],
    correct: 1,
    explain: "Na indikatorlar, na «maxfiy strategiya». O'z qoidalarini buzish tufayli yo'qotadi: katta xavf, stopsiz kirish, qaytarib olishga urinish, his-tuyg'u asosida savdo. Intizom har qanday strategiyadan muhimroq."
  }
];

let qOrder = [], qIdx = 0, qScore = 0, qAnswered = false;

function shuffle(a) {
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

function showBest() {
  const best = localStorage.getItem("forex_quiz_best");
  const el = document.getElementById("quiz-best");
  el.textContent = best ? `🏆 Sizning eng yaxshi natijangiz: ${best}%` : "Hali topshirmagansiz — sinab ko'ring!";
}

function quizStart() {
  qOrder = shuffle([...Array(QUIZ.length).keys()]);
  qIdx = 0; qScore = 0;
  document.getElementById("quiz-start").style.display = "none";
  document.getElementById("quiz-result").style.display = "none";
  document.getElementById("quiz-play").style.display = "block";
  renderQuestion();
}

function renderQuestion() {
  qAnswered = false;
  const item = QUIZ[qOrder[qIdx]];
  document.getElementById("quiz-counter").textContent = `Savol ${qIdx + 1} / ${QUIZ.length}`;
  document.getElementById("quiz-score").textContent = `Ball: ${qScore}`;
  document.getElementById("quiz-bar").style.width = `${(qIdx / QUIZ.length) * 100}%`;
  document.getElementById("quiz-question").textContent = item.q;
  document.getElementById("quiz-explain").style.display = "none";
  document.getElementById("quiz-next").style.display = "none";

  const box = document.getElementById("quiz-options");
  box.innerHTML = "";
  item.options.forEach((opt, i) => {
    const btn = document.createElement("button");
    btn.className = "quiz-opt";
    btn.textContent = opt;
    btn.onclick = () => quizAnswer(i, btn);
    box.appendChild(btn);
  });
}

function quizAnswer(choice, btn) {
  if (qAnswered) return;
  qAnswered = true;
  const item = QUIZ[qOrder[qIdx]];
  const buttons = document.querySelectorAll("#quiz-options .quiz-opt");
  buttons.forEach((b, i) => {
    b.disabled = true;
    if (i === item.correct) b.classList.add("quiz-correct");
    else if (i === choice) b.classList.add("quiz-wrong");
  });
  if (choice === item.correct) qScore++;
  document.getElementById("quiz-score").textContent = `Ball: ${qScore}`;

  const ex = document.getElementById("quiz-explain");
  const ok = choice === item.correct;
  ex.className = "quiz-explain " + (ok ? "quiz-ex-ok" : "quiz-ex-bad");
  ex.innerHTML = `<strong>${ok ? "✅ To'g'ri" : "❌ Noto'g'ri"}.</strong> ${item.explain}`;
  ex.style.display = "block";
  document.getElementById("quiz-next").style.display = "inline-block";
  document.getElementById("quiz-next").textContent =
    qIdx + 1 < QUIZ.length ? "Keyingisi →" : "Natijani ko'rsatish";
}

function quizNext() {
  qIdx++;
  if (qIdx < QUIZ.length) renderQuestion();
  else quizFinish();
}

function quizFinish() {
  const pct = Math.round((qScore / QUIZ.length) * 100);
  const prevBest = parseInt(localStorage.getItem("forex_quiz_best") || "0", 10);
  const isRecord = pct > prevBest;
  if (isRecord) localStorage.setItem("forex_quiz_best", String(pct));

  let verdict, cls;
  if (pct >= 85) { verdict = "🟢 Ajoyib baza. Siz asosiyni tushunasiz — risk-menejment va intizom."; cls = "calc-ok"; }
  else if (pct >= 65) { verdict = "🟡 Yomon emas, lekin kamchiliklar bor. Xato qilgan bo'limlarni qayta o'qing — ayniqsa risk haqida."; cls = "calc-warn"; }
  else { verdict = "🔴 Real pulga o'tish uchun erta. Qo'llanmaga qayting: risk-menejment va psixologiya."; cls = "calc-error"; }

  document.getElementById("quiz-play").style.display = "none";
  const res = document.getElementById("quiz-result");
  res.style.display = "block";
  res.innerHTML = `
    <div class="calc-result ${cls}">
      <h4>Natija: ${qScore} / ${QUIZ.length} (${pct}%)</h4>
      <p>${verdict}</p>
      ${isRecord ? "<p>🏆 <strong>Yangi shaxsiy rekord!</strong></p>" : `<p>Sizning eng yaxshi natijangiz: ${Math.max(pct, prevBest)}%</p>`}
      <ul>
        <li>Zaif mavzular bo'yicha <a href="../forex-guide.md">asosiy qo'llanmani</a> qayta o'qing.</li>
        <li><a href="../extras/psychology.md">Psixologiya bo'limi</a> — tilt va qaytarib olish savollari bo'yicha xato qilgan bo'lsangiz.</li>
        <li><a href="flashcards.md">Kartochkalar</a> va <a href="winrate-rr-calculator.md">WinRate × RR kalkulyatori</a> — mustahkamlash uchun.</li>
      </ul>
      <button class="calc-button" onclick="quizStart()">↻ Qaytadan topshirish</button>
    </div>
  `;
}

window.addEventListener("DOMContentLoaded", showBest);
</script>

<style>
.quiz-progress {
  display: flex;
  justify-content: space-between;
  font-size: 0.85rem;
  font-weight: 600;
  color: var(--md-default-fg-color--light);
  margin-bottom: 0.4rem;
}
.quiz-bar-track {
  width: 100%;
  height: 8px;
  background: var(--md-default-fg-color--lightest);
  border-radius: 4px;
  overflow: hidden;
  margin-bottom: 1.2rem;
}
.quiz-bar-fill {
  height: 100%;
  width: 0;
  background: var(--md-primary-fg-color);
  transition: width 0.3s ease;
}
.quiz-question {
  font-size: 1.15rem;
  margin: 0.3rem 0 1rem;
}
.quiz-options { display: flex; flex-direction: column; gap: 0.6rem; }
.quiz-opt {
  text-align: left;
  padding: 0.7rem 1rem;
  font-size: 0.95rem;
  border: 1px solid var(--md-default-fg-color--lighter);
  border-radius: 8px;
  background: var(--md-default-bg-color);
  color: var(--md-default-fg-color);
  cursor: pointer;
  transition: background 0.15s, border-color 0.15s;
}
.quiz-opt:hover:not(:disabled) { border-color: var(--md-primary-fg-color); }
.quiz-opt:disabled { cursor: default; opacity: 0.95; }
.quiz-opt.quiz-correct {
  background: rgba(34, 197, 94, 0.15);
  border-color: #22c55e;
  font-weight: 600;
}
.quiz-opt.quiz-wrong {
  background: rgba(220, 38, 38, 0.12);
  border-color: #dc2626;
}
.quiz-explain {
  margin-top: 1rem;
  padding: 0.9rem 1.1rem;
  border-radius: 8px;
  font-size: 0.92rem;
  line-height: 1.5;
}
.quiz-ex-ok { background: rgba(34, 197, 94, 0.1); border-left: 4px solid #22c55e; }
.quiz-ex-bad { background: rgba(245, 158, 11, 0.1); border-left: 4px solid #f59e0b; }
.quiz-best { font-weight: 600; margin-bottom: 1rem; }
#quiz-result .calc-result ul { margin: 0.6rem 0; }
</style>

---

## 📚 Zaif joylar? Mana yerga

- [Asosiy qo'llanma](../forex-guide.md) — noldan butun nazariya
- [Treyding psixologiyasi](../extras/psychology.md) — tilt, FOMO, qaytarib olish
- [Pozitsiya kalkulyatori](position-calculator.md) — xavfdan lot qanday hisoblanadi
- [WinRate × RR](winrate-rr-calculator.md) — nima uchun bog'liqlik muhim, Win Rate emas
- [Kartochka trenajoyi](flashcards.md) — yodlash uchun 105 ta atama
- [Barbod bo'lish xavfi](risk-of-ruin.md) — Monte-Karlo: depozitni yo'qotish ehtimoli
