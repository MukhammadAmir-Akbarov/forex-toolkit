# 🎓 Final Exam + Certificate

!!! abstract "How it works"
    18 questions covering the entire course: risk management, psychology, trading
    costs, and market mechanics. Passing score — **80%** (15 out of 18). Pass it
    and you get a **personalised PNG certificate** you can download and share.

    This is not a test of "genius" — it checks whether you have absorbed the
    principles that separate surviving beginners from a blown deposit. Your best
    result is saved in the browser.

!!! warning "Educational material — not financial advice"
    The correct answers reflect risk-management principles, not a guarantee of
    profit. The certificate confirms completion of the educational course, not
    professional trading qualification.

---

<div class="exam-widget calc-widget" id="exam-widget">

  <div id="exam-start">
    <p class="exam-best" id="exam-best"></p>
    <label class="exam-name-label">
      Name for the certificate
      <input type="text" id="exam-name" maxlength="40" placeholder="e.g. John Smith" autocomplete="name">
    </label>
    <button class="calc-button" id="exam-start-btn">▶ Start exam (18 questions)</button>
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
    <button class="calc-button" id="exam-next" style="display:none">Next →</button>
  </div>

  <div id="exam-result" style="display:none"></div>

  <div id="exam-cert-wrap" style="display:none">
    <canvas id="exam-cert" width="1000" height="700"></canvas>
    <button class="calc-button" id="exam-download-btn">⬇ Download certificate (PNG)</button>
  </div>
</div>

<script type="application/json" id="exam-questions">
[
  {
    "q": "What is the maximum recommended risk per trade for a beginner?",
    "options": ["10% of deposit", "1–2% of deposit", "50% of deposit", "Whatever you can afford to lose"],
    "answer": 1,
    "explain": "1–2% per trade — even a streak of 10 losses won't destroy the account. This is the primary rule of survival."
  },
  {
    "q": "Deposit $1000, risk 2%, stop 50 pips on EUR/USD. What is the position size?",
    "options": ["0.04 lots", "0.4 lots", "1.0 lot", "0.004 lots"],
    "answer": 0,
    "explain": "Risk $20 / (50 pips × $10/pip per lot) = 0.04 lots. Position size is calculated FROM the risk, not guessed."
  },
  {
    "q": "What is a stop-loss?",
    "options": ["A take-profit level", "A pre-set level at which the losing trade is closed", "Leverage size", "Broker commission"],
    "answer": 1,
    "explain": "A stop-loss limits the loss in advance. Trading without a stop is the fastest route to blowing an account."
  },
  {
    "q": "Leverage 1:500 means…",
    "options": ["A guaranteed profit 500 times over", "The ability to control a position 500× the deposit (and risk is also ×)", "A broker discount", "A deposit bonus"],
    "answer": 1,
    "explain": "Leverage amplifies both profit and loss. High leverage ≠ high risk BY ITSELF — risk is controlled by position size and the stop."
  },
  {
    "q": "What does the mathematical expectation (EV) of a strategy show?",
    "options": ["How much money you will definitely earn", "The average result per trade over the long run", "The commission size", "Win rate"],
    "answer": 1,
    "explain": "EV = (win rate × average win) − (losses). If EV ≤ 0 — even a million trades won't save you."
  },
  {
    "q": "Win rate 40%, R:R = 1:2. The strategy is…",
    "options": ["Unprofitable", "Profitable over the long run", "Depends on the broker", "Impossible"],
    "answer": 1,
    "explain": "With R:R 1:2 the break-even win rate is ≈ 33%. 40% > 33% → positive EV. A high win rate is not required."
  },
  {
    "q": "The spread is…",
    "options": ["A government tax", "The difference between the buy and sell price", "Stop size", "Leverage"],
    "answer": 1,
    "explain": "The spread (Ask − Bid) is a cost you pay immediately when a trade is opened."
  },
  {
    "q": "A swap is…",
    "options": ["A fee for holding a position overnight", "A volume bonus", "A type of order", "A withdrawal commission"],
    "answer": 0,
    "explain": "A swap is charged for holding a position overnight and depends on the interest rate differential between the currencies."
  },
  {
    "q": "40 small trades per month whose spreads eat up a significant portion of the deposit — this is an example of…",
    "options": ["Smart trading", "Overtrading (costs kill the account)", "Hedging", "Risk-free scalping"],
    "answer": 1,
    "explain": "Costs across hundreds of trades are a 'silent deposit killer'. Trade less frequently and more deliberately."
  },
  {
    "q": "After 5 consecutive losses the best course of action is…",
    "options": ["Double the size to recover losses", "Take a break and review your discipline", "Switch broker", "Increase leverage"],
    "answer": 1,
    "explain": "Revenge trading (martingale, tilt) blows up accounts. A losing streak is a signal to pause and review — not to increase risk."
  },
  {
    "q": "Why keep a trading journal?",
    "options": ["For tax purposes only", "To identify your own error patterns and improve", "It's optional", "To show off"],
    "answer": 1,
    "explain": "A journal turns experience into data: when and on what you lose and win. Without it, progress is random."
  },
  {
    "q": "A demo account is for…",
    "options": ["Earning real money", "Learning the platform and testing a strategy without risk", "Getting a bonus", "Avoiding taxes"],
    "answer": 1,
    "explain": "Demo is for mechanics and strategy testing. But demo doesn't replicate the psychology of real money — switch to live with a small size."
  },
  {
    "q": "A manager promises 'guaranteed 30% profit per month' — this is…",
    "options": ["An excellent opportunity", "A sign of a scam / pyramid scheme", "Normal for forex", "A bank service"],
    "answer": 1,
    "explain": "Guaranteed high returns do not exist. This is a classic sign of fraud."
  },
  {
    "q": "What is declared for trading income tax (UZ resident)?",
    "options": ["Each trade separately", "The annual net result: profits minus losses", "Withdrawals only", "Nothing"],
    "answer": 1,
    "explain": "The annual net result is declared, personal income tax 12%. Check soliq.uz."
  },
  {
    "q": "A Margin Call level means…",
    "options": ["The broker pays you extra", "Free margin is low — forced closure is at risk", "The trade was closed in profit", "A bonus"],
    "answer": 1,
    "explain": "Margin Call is a warning that funds are insufficient for the open position. Next comes Stop Out (forced closure)."
  },
  {
    "q": "The best volatility window for majors is…",
    "options": ["Night time in Tashkent", "London + New York session overlap", "Sydney open", "Weekends"],
    "answer": 1,
    "explain": "The London/New York overlap has the highest volume and tight spreads on EUR/USD and GBP/USD."
  },
  {
    "q": "Risk of ruin increases when…",
    "options": ["Risk per trade is small", "Risk per trade is large and/or EV is negative", "A stop-loss is in place", "You keep a journal"],
    "answer": 1,
    "explain": "A large risk per trade sharply raises the chance of wiping the account even with a working strategy. Control the risk size."
  },
  {
    "q": "The most important survival skill for a beginner is…",
    "options": ["Guessing direction", "Risk management and discipline", "High leverage", "Lots of trades"],
    "answer": 1,
    "explain": "Markets cannot be predicted consistently. Survival comes from risk management and discipline, not from entry accuracy."
  }
]
</script>

---

## What's next

Passed the exam? Congratulations — you have absorbed the fundamentals. But the real
exam is the **market**. Start on [demo](README.md), keep a
[journal](../journal/trading-journal-template.md), size your risk with the
[position calculator](position-calculator.md), and go live with a **small** size.

Didn't pass? No problem — go back to the [main guide](../index.md) and the
[pre-trade checklist](../extras/pre-trade-check.md), then try again.

---

!!! danger "Not financial advice"
    The certificate is an educational achievement, not a licence or guarantee of
    profit. Forex trading carries a high risk of capital loss.
