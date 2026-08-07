# 🎯 Quiz: Are You Ready for Real Trading?

!!! abstract "How it works"
    18 questions on forex fundamentals, risk management, and psychology. After each
    answer — a short explanation of **why** that is correct. At the end you get a
    percentage score and a verdict. Your best result is saved in the browser.

    **This is not an exam for a "market genius".** It checks whether you have
    absorbed the things that separate surviving beginners from those who blow their
    deposit in the first month.

!!! warning "Educational material — not financial advice"
    The correct answers reflect risk-management principles, not a guarantee of
    profit. Trading forex carries a high risk of loss.

---

<div class="quiz-widget calc-widget">
  <div id="quiz-start">
    <p class="quiz-best" id="quiz-best"></p>
    <button class="calc-button" onclick="quizStart()">▶ Start quiz (18 questions)</button>
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
    <button class="calc-button" id="quiz-next" style="display:none" onclick="quizNext()">Next →</button>
  </div>

  <div id="quiz-result" style="display:none"></div>
</div>

<script>
const QUIZ = [
  {
    q: "What is the maximum acceptable risk per trade for a beginner?",
    options: ["0.5–1% of deposit", "5–10% of deposit", "The entire free balance", "Depends on how confident you are in the trade"],
    correct: 0,
    explain: "For a beginner — 0.5–1% per trade. At 1% risk, even 10 consecutive losses only take ~10% of the deposit, and the account survives a losing streak. 5–10% can kill a deposit in a single bad week."
  },
  {
    q: "What must you set BEFORE entering a trade?",
    options: ["A large Take Profit", "A Stop Loss", "Leverage 1:500", "Telegram notifications"],
    correct: 1,
    explain: "A stop loss is a pre-made decision about where you admit you were wrong. Without it, a single market reversal can wipe the account. The stop is set BEFORE entry — not 'by feel'."
  },
  {
    q: "How long should you trade on demo at minimum before using real money?",
    options: ["A couple of days", "A week", "At least 3 months", "Demo is a waste of time"],
    correct: 2,
    explain: "At least 3 months of consistent demo trading with a journal. Demo teaches platform mechanics and discipline without losing money. Rushing to live trading is the most common mistake."
  },
  {
    q: "Win Rate 45%, RR (risk-reward) 1:2. The strategy in the long run is…",
    options: ["Unprofitable — too few wins", "Profitable mathematically", "Neutral", "Depends on luck"],
    correct: 1,
    explain: "EV = 0.45×2 − 0.55×1 = +0.35R per trade. With RR 1:2 you only need to win ~34% of trades to be profitable. Win rate alone means nothing without RR."
  },
  {
    q: "A broker promises 'guaranteed profit of 30% per month'. This is…",
    options: ["An excellent opportunity", "A sign of fraud", "Normal for forex", "Only for VIP clients"],
    correct: 1,
    explain: "Guaranteed profit does not exist in the market. 74–89% of retail traders lose money. Any 'guaranteed return' is a red flag for fraud."
  },
  {
    q: "What is high leverage (1:500) for?",
    options: ["To earn more", "It is dangerous — it amplifies losses too", "It is required for trading", "It reduces risk"],
    correct: 1,
    explain: "Leverage amplifies BOTH profit AND losses. Risk is controlled by position size and the stop, not by leverage. High leverage only lets you open a position larger than your deposit — and lose it faster."
  },
  {
    q: "Price is almost at your stop but 'is about to reverse'. What do you do?",
    options: ["Move the stop further away", "Nothing — a stop is a stop", "Add to the position (average down)", "Remove the stop manually"],
    correct: 1,
    explain: "Moving your stop against yourself is the path to a large loss. Your stop is a pre-made rule. 'It's about to reverse' is hope, not analysis."
  },
  {
    q: "What is the main purpose of a trading journal?",
    options: ["To show off your profits", "To find your own recurring mistakes", "A broker requirement", "To calculate taxes"],
    correct: 1,
    explain: "A journal reveals patterns: at what time, on which pairs, and in what mood you lose money. Without a journal you repeat the same mistakes without realising it."
  },
  {
    q: "You lost 3 trades in a row and want to 'get even' with a large position. This is…",
    options: ["A sensible plan", "Tilt — a stop signal", "Normal risk management", "The martingale strategy — it works"],
    correct: 1,
    explain: "The urge to get even (revenge trading) while on tilt blows up deposits. After a losing streak the correct response is to reduce size or take a break — not to increase the stake."
  },
  {
    q: "Your deposit dropped 50%. How much do you need to earn to get back to the start?",
    options: ["50%", "75%", "100%", "25%"],
    correct: 2,
    explain: "Drawdown math is brutal: −50% requires +100% to recover. That is why protecting capital matters more than chasing profit — large drawdowns are almost impossible to come back from."
  },
  {
    q: "Before a major news release (NFP, Fed meeting) the spread widens and price spikes. A beginner should…",
    options: ["Go all-in", "Avoid entering", "Remove stop losses", "Increase leverage"],
    correct: 1,
    explain: "During news releases sharp moves and slippage knock out stops at the worst price. It is safer for beginners not to trade a few minutes before and after major news events."
  },
  {
    q: "How do you choose a broker?",
    options: ["By the size of the deposit bonus", "By the presence of a regulator licence (FCA, CySEC, ASIC)", "By attractive advertising", "By promised leverage of 1:1000"],
    correct: 1,
    explain: "The main factor is regulation. An FCA/CySEC/ASIC licence means client fund segregation and oversight. Bonuses and massive leverage are marketing — often used by unregulated firms."
  },
  {
    q: "Deposit $1000, risk 1%, stop 25 pips, EUR/USD ($10/pip per lot). Position size?",
    options: ["0.04 lots", "0.4 lots", "1 lot", "0.004 lots"],
    correct: 0,
    explain: "Risk = $10. Lots = 10 / (25 × 10) = 0.04. First calculate the allowed risk in dollars, then the position size from the stop — never the other way around."
  },
  {
    q: "What is R (1R) in risk management?",
    options: ["The size of the profit", "The amount of your risk per trade (distance to the stop)", "Leverage", "Spread size"],
    correct: 1,
    explain: "1R is your unit of risk — your stop loss in dollars. It is convenient to measure profit in R: +2R means 'I made twice what I risked'. This makes trades comparable regardless of account size."
  },
  {
    q: "A backtest on historical data showed +200%. This means…",
    options: ["Live results will be the same", "The past does not guarantee the future; live results are usually worse", "You can go live immediately", "The strategy is perfect"],
    correct: 1,
    explain: "A backtest does not account for psychology, slippage, changing market conditions, or the risk of overfitting. Live results are almost always worse. A backtest filters bad ideas — it does not promise profit."
  },
  {
    q: "Can you trade with money set aside for rent or food?",
    options: ["Yes, if you are confident in the trade", "Absolutely not", "Only with half of it", "If the leverage is small"],
    correct: 1,
    explain: "Trade only with money whose loss you can absorb without affecting your daily life. 'Living-expense' money creates emotional pressure that destroys discipline."
  },
  {
    q: "A profitable trade is moving in your favour. When should you move the stop to break-even (BE)?",
    options: ["Immediately upon entry", "Once price has moved a reasonable distance in your direction", "Never move it", "When you get scared"],
    correct: 1,
    explain: "Moving to break-even after price passes a meaningful level protects profit and removes risk. But moving to BE too early (right at the start) gets you shaken out by normal price fluctuations."
  },
  {
    q: "The main reason beginners lose money is…",
    options: ["Bad indicators", "Lack of discipline and risk management", "Too small a deposit", "Wrong broker"],
    correct: 1,
    explain: "Not indicators, not a 'secret strategy'. People blow up by breaking their own rules: oversized risk, no stop loss, revenge trading, trading on emotions. Discipline matters more than any strategy."
  }
];

let qDeck = [], qIdx = 0, qScore = 0, qAnswered = false;

function shuffle(list) {
  const a = [...list];
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

function showBest() {
  const best = localStorage.getItem("forex_quiz_best");
  const el = document.getElementById("quiz-best");
  el.textContent = best ? `🏆 Your best score: ${best}%` : "Not attempted yet — give it a try!";
}

function quizStart() {
  // Перемешиваем и вопросы, и варианты: раньше правильный ответ почти всегда
  // стоял вторым, и квиз проходился вслепую на 78%.
  qDeck = shuffle(QUIZ).map((item) => {
    const right = item.options[item.correct];
    const options = shuffle(item.options);
    return { ...item, options, correct: options.indexOf(right) };
  });
  qIdx = 0; qScore = 0;
  document.getElementById("quiz-start").style.display = "none";
  document.getElementById("quiz-result").style.display = "none";
  document.getElementById("quiz-play").style.display = "block";
  renderQuestion();
}

function renderQuestion() {
  qAnswered = false;
  const item = qDeck[qIdx];
  document.getElementById("quiz-counter").textContent = `Question ${qIdx + 1} of ${QUIZ.length}`;
  document.getElementById("quiz-score").textContent = `Score: ${qScore}`;
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
  const item = qDeck[qIdx];
  const buttons = document.querySelectorAll("#quiz-options .quiz-opt");
  buttons.forEach((b, i) => {
    b.disabled = true;
    if (i === item.correct) b.classList.add("quiz-correct");
    else if (i === choice) b.classList.add("quiz-wrong");
  });
  if (choice === item.correct) qScore++;
  document.getElementById("quiz-score").textContent = `Score: ${qScore}`;

  const ex = document.getElementById("quiz-explain");
  const ok = choice === item.correct;
  ex.className = "quiz-explain " + (ok ? "quiz-ex-ok" : "quiz-ex-bad");
  ex.innerHTML = `<strong>${ok ? "✅ Correct" : "❌ Incorrect"}.</strong> ${item.explain}`;
  ex.style.display = "block";
  document.getElementById("quiz-next").style.display = "inline-block";
  document.getElementById("quiz-next").textContent =
    qIdx + 1 < QUIZ.length ? "Next →" : "Show result";
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
  if (pct >= 85) { verdict = "🟢 Excellent foundation. You understand the fundamentals — risk management and discipline."; cls = "calc-ok"; }
  else if (pct >= 65) { verdict = "🟡 Not bad, but there are gaps. Re-read the sections where you made mistakes — especially on risk."; cls = "calc-warn"; }
  else { verdict = "🔴 Too early to think about real money. Go back to the guide: risk management and psychology."; cls = "calc-error"; }

  document.getElementById("quiz-play").style.display = "none";
  const res = document.getElementById("quiz-result");
  res.style.display = "block";
  res.innerHTML = `
    <div class="calc-result ${cls}">
      <h4>Result: ${qScore} out of ${QUIZ.length} (${pct}%)</h4>
      <p>${verdict}</p>
      ${isRecord ? "<p>🏆 <strong>New personal record!</strong></p>" : `<p>Your best score: ${Math.max(pct, prevBest)}%</p>`}
      <ul>
        <li>Re-read <a href="../forex-guide.md">the main guide</a> on weak topics.</li>
        <li>The <a href="../extras/psychology.md">psychology section</a> — if you missed questions about tilt and revenge trading.</li>
        <li><a href="flashcards.md">Flashcards</a> and the <a href="winrate-rr-calculator.md">WinRate × RR calculator</a> — to reinforce learning.</li>
      </ul>
      <button class="calc-button" onclick="quizStart()">↻ Retake quiz</button>
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

## 📚 Weak spots? Start here

- [Main guide](../forex-guide.md) — full theory from scratch
- [Trading psychology](../extras/psychology.md) — tilt, FOMO, revenge trading
- [Position calculator](position-calculator.md) — how to size a lot from risk
- [WinRate × RR](winrate-rr-calculator.md) — why the combination matters, not Win Rate alone
- [Flashcard trainer](flashcards.md) — 105 terms to memorise
- [Risk of ruin](risk-of-ruin.md) — Monte Carlo: chance of blowing the deposit
