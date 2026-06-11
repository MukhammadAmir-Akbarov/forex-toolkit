# 🎴 Flashcard Trainer (Forex Terms)

!!! abstract "How the trainer works"
    105 forex flashcards covering terms, patterns, and psychology.
    Click **"Show Answer"**, then honestly rate yourself — "Knew It" or "Didn't Know".
    The app saves your progress in the browser and shows difficult cards more often.

    **Goal:** reach 105/105 learned cards (≥3 correct in a row).

!!! warning "Educational material — not financial advice"
    All terms are provided for educational purposes only. Trading forex carries a high level of risk.

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
      <span>Progress: <span id="ftk-learned-count">0</span> / <span id="ftk-total-count">105</span> learned</span>
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
      <div class="ftk-stat-lbl">day streak</div>
    </div>
    <div class="ftk-stat">
      <div class="ftk-stat-num" id="ftk-session-ok">0</div>
      <div class="ftk-stat-lbl">"Knew It" this session</div>
    </div>
    <div class="ftk-stat">
      <div class="ftk-stat-num" id="ftk-session-fail">0</div>
      <div class="ftk-stat-lbl">"Didn't Know" this session</div>
    </div>
    <div class="ftk-stat">
      <div class="ftk-stat-num" id="ftk-remaining">105</div>
      <div class="ftk-stat-lbl">not yet learned</div>
    </div>
  </div>

  <!-- Filter -->
  <div class="ftk-filter-row">
    <label for="ftk-tag-select">Filter by topic:</label>
    <select id="ftk-tag-select">
      <option value="all">All cards (105)</option>
    </select>
    <button class="ftk-btn-reset" id="ftk-reset-btn" title="Reset progress for all cards">Reset Progress</button>
  </div>

  <!-- Card area -->
  <div class="ftk-card-area" id="ftk-card-area">
    <div class="ftk-card" id="ftk-card">
      <div class="ftk-card-face ftk-front" id="ftk-front">
        <div class="ftk-card-tag" id="ftk-card-tag">...</div>
        <div class="ftk-card-term" id="ftk-card-term">Loading...</div>
        <div class="ftk-card-hint">Click "Show Answer"</div>
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
    <button class="ftk-btn ftk-btn-show" id="ftk-show-btn">Show Answer</button>
    <button class="ftk-btn ftk-btn-knew" id="ftk-knew-btn" disabled>Knew It ✓</button>
    <button class="ftk-btn ftk-btn-didnt" id="ftk-didnt-btn" disabled>Didn't Know ✗</button>
  </div>

  <div class="ftk-empty" id="ftk-empty" style="display:none">
    All cards in this topic are learned! Choose another topic or reset progress.
  </div>

</div>

<script>
(function () {
  /* ─────────── данные карточек ─────────── */
  var CARDS = [
    {front:"Pip",back:"The standard unit of price movement. Usually the 4th decimal place. For JPY pairs — the 2nd decimal place.",tags:["forex","basic"]},
    {front:"Lot",back:"Unit of position size. 1 standard lot = 100,000 units of the base currency. Micro-lot = 0.01.",tags:["forex","basic"]},
    {front:"Spread",back:"The difference between Ask and Bid. The broker's fee for every trade.",tags:["forex","basic"]},
    {front:"Bid",back:"The price at which the broker BUYS currency from you (the price at which you sell). Lower than Ask.",tags:["forex","basic"]},
    {front:"Ask",back:"The price at which the broker SELLS currency to you (the price at which you buy). Higher than Bid.",tags:["forex","basic"]},
    {front:"Leverage",back:"Credit multiplier. 1:30 → a $100 deposit lets you open a $3,000 position. Amplifies BOTH profit AND loss.",tags:["forex","basic"]},
    {front:"Margin",back:"The amount locked as collateral for an open position.",tags:["forex","basic"]},
    {front:"Long",back:"A buy trade. Bet on the price going up.",tags:["forex","basic"]},
    {front:"Short",back:"A sell trade. Bet on the price going down.",tags:["forex","basic"]},
    {front:"Stop Loss (SL)",back:"An order that automatically closes a position at a set loss level. MANDATORY in every trade.",tags:["forex","risk"]},
    {front:"Take Profit (TP)",back:"An order that automatically closes a position when a profit target is reached.",tags:["forex","risk"]},
    {front:"Margin Call",back:"A broker warning that free margin is running low. Forced closure is approaching.",tags:["forex","risk"]},
    {front:"Stop Out",back:"Forced closure of positions by the broker when margin reaches a critical level (usually 20–50%).",tags:["forex","risk"]},
    {front:"Major",back:"The most liquid currency pairs with USD: EUR/USD, GBP/USD, USD/JPY, USD/CHF, AUD/USD, USD/CAD, NZD/USD.",tags:["forex","basic"]},
    {front:"Cross",back:"A currency pair without USD: EUR/GBP, EUR/JPY, GBP/JPY.",tags:["forex","basic"]},
    {front:"Exotic",back:"Pairs with an emerging-market currency: USD/TRY, USD/ZAR. DANGEROUS for beginners.",tags:["forex","basic"]},
    {front:"Swap",back:"Fee for rolling a position overnight. Can be positive or negative.",tags:["forex","basic"]},
    {front:"Base currency",back:"The first currency in a pair. In EUR/USD the base currency is EUR.",tags:["forex","basic"]},
    {front:"Quote currency",back:"The second (quoted) currency in a pair. In EUR/USD the quote currency is USD.",tags:["forex","basic"]},
    {front:"OHLC",back:"Open, High, Low, Close — the four prices that form a candle.",tags:["technical","candles"]},
    {front:"Bullish candle",back:"A bullish candle: Close > Open. Green or white.",tags:["technical","candles"]},
    {front:"Bearish candle",back:"A bearish candle: Close < Open. Red or black.",tags:["technical","candles"]},
    {front:"Body",back:"The candle body — the rectangle between Open and Close.",tags:["technical","candles"]},
    {front:"Wick / Shadow",back:"The candle wick — the lines above and below the body, reaching High and Low.",tags:["technical","candles"]},
    {front:"Hammer",back:"Small body at the top, long lower wick. Bullish reversal pattern at the end of a downtrend.",tags:["technical","patterns"]},
    {front:"Shooting Star",back:"Small body at the bottom, long upper wick. Bearish reversal pattern.",tags:["technical","patterns"]},
    {front:"Bullish Engulfing",back:"A large green candle that fully covers the body of the previous red candle. Signal of an upward reversal.",tags:["technical","patterns"]},
    {front:"Bearish Engulfing",back:"A large red candle that fully covers the body of the previous green candle. Signal of a downward reversal.",tags:["technical","patterns"]},
    {front:"Doji",back:"A candle with Open ≈ Close (tiny body). Indecision — bullish and bearish forces are balanced.",tags:["technical","patterns"]},
    {front:"Pin Bar",back:"A candle with a long wick and a small body. Reversal signal in the direction opposite the wick.",tags:["technical","patterns"]},
    {front:"Uptrend",back:"Rising trend. A series of higher highs (HH) and higher lows (HL).",tags:["technical","trends"]},
    {front:"Downtrend",back:"Falling trend. A series of lower highs (LH) and lower lows (LL).",tags:["technical","trends"]},
    {front:"Range / Flat",back:"Sideways / flat market. Price moves within a horizontal channel.",tags:["technical","trends"]},
    {front:"Support",back:"A level from which price has bounced upward.",tags:["technical","levels"]},
    {front:"Resistance",back:"A level from which price has bounced downward.",tags:["technical","levels"]},
    {front:"Breakout",back:"A break through a support or resistance level.",tags:["technical","levels"]},
    {front:"Retest",back:"Price returning to a broken level for confirmation.",tags:["technical","levels"]},
    {front:"Pullback / Retracement",back:"A temporary move against the main trend.",tags:["technical","trends"]},
    {front:"EMA",back:"Exponential Moving Average. Recent candles carry more weight than older ones.",tags:["technical","indicators"]},
    {front:"SMA",back:"Simple Moving Average. The plain average of closing prices over N periods.",tags:["technical","indicators"]},
    {front:"EMA 200",back:"The main trend-direction filter: price above EMA200 = longs only; below = shorts only.",tags:["technical","indicators"]},
    {front:"RSI",back:"Relative Strength Index. Oscillator 0–100. >70 = overbought, <30 = oversold.",tags:["technical","indicators"]},
    {front:"MACD",back:"Trend + momentum indicator. MACD = EMA(12) − EMA(26). Signals: crossovers, divergence.",tags:["technical","indicators"]},
    {front:"Bollinger Bands",back:"Middle band + 2 standard deviations. Price stays between the bands ~95% of the time.",tags:["technical","indicators"]},
    {front:"ATR",back:"Average True Range. Average candle size. Helps set stop-loss distances.",tags:["technical","indicators"]},
    {front:"Divergence",back:"Price makes a new extreme but the indicator does not. A signal of weakening momentum.",tags:["technical","patterns"]},
    {front:"Head and Shoulders",back:"Reversal top pattern: left shoulder → head (higher) → right shoulder.",tags:["technical","patterns"]},
    {front:"Double Top",back:"Price fails to break a level twice, then reverses downward.",tags:["technical","patterns"]},
    {front:"Triangle",back:"Ascending = usually breaks up. Descending = usually breaks down. Symmetrical = unpredictable.",tags:["technical","patterns"]},
    {front:"Flag",back:"Trend-continuation pattern: strong impulse move + short consolidation.",tags:["technical","patterns"]},
    {front:"Fibonacci",back:"Retracement levels: 23.6%, 38.2%, 50%, 61.8%, 78.6%. Used as entry zones on a pullback.",tags:["technical","levels"]},
    {front:"Risk Reward (R:R)",back:"Ratio of risk to potential profit. R:R 1:2 = targeting $2 profit for every $1 risked. Minimum for beginners: 1:2.",tags:["risk","basic"]},
    {front:"Win Rate",back:"Percentage of profitable trades. With R:R 1:2, ≥40% is good.",tags:["risk","metrics"]},
    {front:"Profit Factor",back:"Total profits / Total losses. ≥1.5 is good.",tags:["risk","metrics"]},
    {front:"Expectancy",back:"Expected result per trade: (WR × Avg Win) − (LR × Avg Loss). Must be > 0.",tags:["risk","metrics"]},
    {front:"Drawdown",back:"The decline of account balance from its peak.",tags:["risk","metrics"]},
    {front:"Max Drawdown",back:"Maximum drawdown over a period. <15% of deposit is good.",tags:["risk","metrics"]},
    {front:"R (Risk Unit)",back:"Your risk unit for one trade. If you risked $5 — that is 1R. +2R = +$10.",tags:["risk","metrics"]},
    {front:"Equity",back:"Current account balance plus the floating profit/loss of open trades.",tags:["risk","metrics"]},
    {front:"Equity Curve",back:"A chart of equity changes over time. The primary visual measure of a strategy.",tags:["risk","metrics"]},
    {front:"1% Rule",back:"Rule: risk per trade ≤1% of deposit. For beginners 0.5% is better.",tags:["risk","management"]},
    {front:"Tilt",back:"Emotional state after a loss: anger, urge to revenge-trade. The #1 account killer.",tags:["psychology","basic"]},
    {front:"FOMO",back:"Fear of Missing Out. Forces you to enter without a signal.",tags:["psychology","basic"]},
    {front:"Averaging Down",back:"Adding to a losing position hoping for a reversal. DANGEROUS technique — forbidden for beginners.",tags:["psychology","management"]},
    {front:"Demo Account",back:"Account with virtual money on real quotes. Mandatory learning stage: 2–3 months.",tags:["basic","broker"]},
    {front:"Live Account",back:"Real-money account. Switch only after consistently profitable results on demo.",tags:["basic","broker"]},
    {front:"Cent Account",back:"Account with balance in cents. $10 = 1,000 cents. Good for micro-practice.",tags:["basic","broker"]},
    {front:"ECN Account",back:"Direct market access. Tight spread + commission. For experienced traders.",tags:["basic","broker"]},
    {front:"Market Order",back:"An order executed at the current market price.",tags:["basic","orders"]},
    {front:"Limit Order",back:"A pending order to buy below / sell above the current price.",tags:["basic","orders"]},
    {front:"Stop Order",back:"A pending order to buy above / sell below the current price (for breakouts).",tags:["basic","orders"]},
    {front:"Slippage",back:"Actual execution price differs from the expected price. Especially common on news releases.",tags:["basic","orders"]},
    {front:"Liquidity",back:"How easily you can buy/sell without significantly moving the price.",tags:["basic","market"]},
    {front:"Volatility",back:"The amplitude of price fluctuations over a given period.",tags:["basic","market"]},
    {front:"NFP",back:"Non-Farm Payrolls. US employment data. Released first Friday of the month. The most important monthly news event.",tags:["fundamental","news"]},
    {front:"FOMC",back:"Federal Open Market Committee. The Fed's interest-rate meeting. 8 times per year.",tags:["fundamental","news"]},
    {front:"CPI",back:"Consumer Price Index. A measure of inflation.",tags:["fundamental","news"]},
    {front:"GDP",back:"Gross Domestic Product. Total economic output of a country.",tags:["fundamental","news"]},
    {front:"Interest Rate",back:"Central bank rate. Higher rate → stronger currency (simplified).",tags:["fundamental","news"]},
    {front:"Carry Trade",back:"Strategy: buy a high-interest-rate currency against a low-rate currency. Profit from swap differentials.",tags:["fundamental","strategy"]},
    {front:"Hedging",back:"Opening an opposing position to protect against risk.",tags:["risk","management"]},
    {front:"Diversification",back:"Spreading risk across different assets.",tags:["risk","management"]},
    {front:"Money Management (MM)",back:"Capital management: position sizing, risk control, diversification.",tags:["risk","management"]},
    {front:"Trailing Stop",back:"A stop that moves with the price in the profitable direction but never moves back.",tags:["risk","orders"]},
    {front:"Break-even",back:"Moving the stop-loss to the entry price so the trade cannot lose.",tags:["risk","orders"]},
    {front:"Scalping",back:"Trading on M1–M5 for small profits. Stressful — not for beginners.",tags:["style","trading"]},
    {front:"Day Trading",back:"All trades opened and closed within the same trading day.",tags:["style","trading"]},
    {front:"Swing Trading",back:"Trades held from a few hours to several days.",tags:["style","trading"]},
    {front:"Position Trading",back:"Trades held for weeks or months.",tags:["style","trading"]},
    {front:"Backtest",back:"Testing a strategy on historical price data.",tags:["strategy","testing"]},
    {front:"Forward Test",back:"Testing a strategy on a demo account in real time.",tags:["strategy","testing"]},
    {front:"Walk-Forward",back:"Walk-forward optimization: optimise parameters on one segment of history, then verify on the next.",tags:["strategy","testing"]},
    {front:"Overfitting",back:"The strategy is over-tuned to historical data and fails on new data.",tags:["strategy","testing"]},
    {front:"Expert Advisor (EA)",back:"An automated trading bot for MT4/MT5.",tags:["technology","bots"]},
    {front:"MQL5",back:"The programming language for writing EAs in MetaTrader 5.",tags:["technology","bots"]},
    {front:"API",back:"Programmatic interface for connecting to a broker (e.g. MetaTrader 5 Python API).",tags:["technology","bots"]},
    {front:"Spread Cost",back:"Cost of the spread. On EUR/USD a 1-pip spread = $1 per standard lot.",tags:["risk","costs"]},
    {front:"Pip Value",back:"Value of 1 pip. On EUR/USD for 1 standard lot ≈ $10. For 0.01 lot ≈ $0.10.",tags:["basic","costs"]},
    {front:"Lot Size",back:"Position size. Formula: (Deposit × Risk%) / (Stop in pips × Pip Value).",tags:["risk","management"]},
    {front:"Trading Session",back:"London session (10:00–19:00 UTC+3), US session (14:00–23:00 UTC+3).",tags:["basic","time"]},
    {front:"Asian Session",back:"Asian session (02:00–11:00 UTC+3). Low liquidity. Best skipped by beginners.",tags:["basic","time"]},
    {front:"Sniper Entry",back:"Patiently waiting for the perfect entry point according to your rules.",tags:["psychology","patience"]},
    {front:"Trading Plan",back:"Written rules: what, when, and how to trade.",tags:["psychology","discipline"]},
    {front:"Trading Journal",back:"A record of every trade. The most important tool for growth.",tags:["psychology","discipline"]}
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
    'forex':        'Forex: Basics',
    'technical':    'Technical Analysis',
    'risk':         'Risk Management',
    'psychology':   'Psychology',
    'fundamental':  'Fundamental Analysis',
    'basic':        'Basic Concepts',
    'strategy':     'Strategy & Testing',
    'style':        'Trading Style',
    'technology':   'Technology (EA, API)',
    'candles':      'Candlestick Analysis',
    'patterns':     'Patterns',
    'trends':       'Trends',
    'levels':       'Levels',
    'indicators':   'Indicators',
    'management':   'Capital Management',
    'metrics':      'Metrics',
    'orders':       'Orders',
    'news':         'News (Fundamental)',
    'broker':       'Account Types',
    'bots':         'Bots & Automation',
    'costs':        'Costs',
    'time':         'Trading Sessions',
    'testing':      'Strategy Testing',
    'discipline':   'Discipline',
    'patience':     'Patience & Entry'
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
      ? '✅ Learned (' + s.streak + ' correct in a row)'
      : s.streak > 0
        ? '🔄 Correct in a row: ' + s.streak + ' / ' + LEARNED_THRESHOLD
        : '🆕 New card';
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
    if (!confirm('Reset all flashcard progress? This will delete all results from your browser.')) return;
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

## How to study effectively

1. **10–15 minutes every day** — better than one hour once a week.
2. **Be honest**: click "Knew It" only if you genuinely recalled the definition BEFORE flipping.
3. **The algorithm sets priorities for you**: cards with a zero streak are shown most often.
4. **Goal**: 105/105 cards with 3+ correct answers in a row.

!!! tip "Next step after flashcards"
    Once you know all the terms, move on to the [WinRate × RR Calculator](winrate-rr-calculator.md) to understand the math behind a strategy.

---

## Spaced repetition algorithm (brief)

The trainer uses a simplified version of SM-2:

| Card state | Shown |
|---|---|
| Never answered / reset | First priority |
| 1–2 correct in a row | Second priority |
| 3+ correct in a row (learned) | Rarely, for reinforcement |

Progress is stored in your browser's `localStorage` — it persists between sessions but is not synchronised across devices.

---

!!! info "Educational material"
    This page is part of a forex trading tutorial. Not financial advice.
