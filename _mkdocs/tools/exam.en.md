---
widgets: [exam]
---

# 🎓 Final Exam + Certificate

!!! abstract "How it works"
    Every attempt draws **20 random questions from a bank of 45**, and the
    answer options are shuffled too — memorising the order will not work.
    Topics: risk management, position sizing, trading costs, psychology,
    market mechanics. Passing score — **80%** (16 out of 20). Pass it and
    you get a **personalised PNG certificate** you can download and share.

    More than half the questions ask you to calculate or judge a situation
    rather than recall a definition. If you fail, the exam lists the topics
    to revisit. Your best result is saved in the browser.

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
    <button class="calc-button" id="exam-start-btn">▶ Start the exam (20 of 45 questions)</button>
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
    "q": "What is a sensible maximum risk per trade for a beginner?",
    "options": [
      "5–10% of the account — otherwise it grows too slowly",
      "1–2% of the account",
      "It depends on how confident you are in the signal",
      "Enough for the profit to cover the previous loss"
    ],
    "answer": 1,
    "explain": "1–2% per trade. At 1%, even ten losses in a row take about 10% of the account and it survives the streak. \"By confidence\" is not risk management: confidence cannot be measured and peaks right before the worst trades."
  },
  {
    "q": "$1000 account, 2% risk, 50-pip stop on EUR/USD. What position size?",
    "options": [
      "0.04 lots",
      "0.4 lots",
      "1.0 lot",
      "0.02 lots"
    ],
    "answer": 0,
    "explain": "$20 risk ÷ (50 pips × $10 per pip per lot) = 0.04 lots. Size follows FROM risk and stop distance — it is never picked by feel."
  },
  {
    "q": "$2000 account, 1.5% risk, 30-pip stop on USD/JPY at 150.00. Position size?",
    "options": [
      "0.10 lots",
      "0.20 lots",
      "0.15 lots",
      "0.015 lots"
    ],
    "answer": 2,
    "explain": "A USD/JPY pip is NOT $10: 0.01 × 100,000 = ¥1000 ÷ 150 = $6.67 per lot. $30 risk ÷ (30 × 6.67) = 0.15 lots. Anyone who plugs in $10 out of habit gets 0.10 and takes only $20 of risk instead of $30."
  },
  {
    "q": "$500 account, 1:100 leverage. You want 0.5 lots of EUR/USD at 1.1000. How much margin is required?",
    "options": [
      "$55 — plenty of room",
      "$550 — the account is too small, the trade will not open",
      "$110",
      "$5.50"
    ],
    "answer": 1,
    "explain": "0.5 lots = 50,000 EUR ≈ $55,000. Margin = $55,000 ÷ 100 = $550, more than the account. Leverage does not \"give you money\" — it sets how much of the position must be locked up."
  },
  {
    "q": "Your stop was at 1.0950 but the position closed at 1.0938. This is…",
    "options": [
      "A terminal bug — reinstall it",
      "The broker cheating you; file a complaint",
      "Slippage: a stop is a trigger price, not a guaranteed fill",
      "Impossible, stops always fill exactly at the level"
    ],
    "answer": 2,
    "explain": "An ordinary stop becomes a market order once the level is touched. In a fast market the nearest available price is worse. That is why the real loss can exceed the planned one — only a separate \"guaranteed stop\" product removes this."
  },
  {
    "q": "Two $1000 accounts: one with 1:30 leverage, one with 1:500. Both open 0.1 lots of EUR/USD with a 20-pip stop. Who risks more money?",
    "options": [
      "The same — $20 each: risk comes from size and stop, not leverage",
      "The second one risks about 16× more",
      "The second one risks slightly more because of margin",
      "The first one — it locks up more money"
    ],
    "answer": 0,
    "explain": "0.1 lots × 20 pips × $1 = $20 for both. Leverage only changes the margin held ($367 vs $22). What is dangerous is not leverage itself but the size it lets you open."
  },
  {
    "q": "50% win rate, average win 1.5R, average loss 1R, spread and commission cost about 0.1R per trade. What is the expectancy?",
    "options": [
      "+0.25R",
      "+0.15R",
      "−0.10R",
      "+0.65R"
    ],
    "answer": 1,
    "explain": "0.5 × 1.5 − 0.5 × 1 − 0.1 = +0.15R. You get +0.25R only by ignoring costs — and that is exactly how a strategy that is profitable on paper turns into a losing one in practice."
  },
  {
    "q": "A strategy has a 90% win rate, average win 0.1R and average loss 1R. Over a long run it is…",
    "options": [
      "Profitable — nine wins out of ten",
      "Break-even",
      "Losing: expectancy is −0.01R per trade",
      "Profitable if you increase size"
    ],
    "answer": 2,
    "explain": "0.9 × 0.1 − 0.1 × 1 = −0.01R. A high win rate with tiny targets and wide stops is the most common trap: nine wins do not cover a single loss."
  },
  {
    "q": "R:R is 1:3. What is the minimum win rate needed to break even (ignoring costs)?",
    "options": [
      "33%",
      "50%",
      "25%",
      "75%"
    ],
    "answer": 2,
    "explain": "Break-even win rate = 1 ÷ (1 + 3) = 25%. 33% is the answer for 1:2 — a common mix-up. The higher the R:R, the less often you need to be right."
  },
  {
    "q": "Spread is 1.5 pips and you take 40 trades a month at 0.1 lots on EUR/USD. What does the spread cost per month?",
    "options": [
      "$6",
      "$1.50",
      "$600",
      "$60 — that is 6% of a $1000 account"
    ],
    "answer": 3,
    "explain": "1.5 × $1 per pip (0.1 lots) × 40 = $60. On a $1000 account that is 6% a month in costs alone — the strategy has to earn that back before it earns anything for you."
  },
  {
    "q": "A 10-pip stop with a 2-pip spread. What share of your risk does the spread consume?",
    "options": [
      "20%",
      "2%",
      "10%",
      "0.2%"
    ],
    "answer": 0,
    "explain": "2 ÷ 10 = 20% of the risk goes to the broker before price moves at all. That is why tight stops and scalping cost a beginner more than they look: the tighter the stop, the larger the cost share inside it."
  },
  {
    "q": "On which weekday is triple swap normally charged?",
    "options": [
      "Friday",
      "Monday",
      "Wednesday — the weekend rollover is settled through it",
      "Triple swap does not exist"
    ],
    "answer": 2,
    "explain": "Settlement runs on a T+2 schedule, so a position held through midweek takes three days of swap at once. Hold through Wednesday and you pay (or receive) triple."
  },
  {
    "q": "Three open positions at 1% risk each: long EUR/USD, long GBP/USD, short USD/CHF. What is the real portfolio risk?",
    "options": [
      "1% — the risks average out",
      "About 1.7% — partial diversification",
      "About 3% — all three are one bet against the dollar",
      "0.33% each"
    ],
    "answer": 2,
    "explain": "Three tickets, one bet: dollar down. A single strong dollar move takes out all three stops together. Measure risk by what one market move does, not by counting trades."
  },
  {
    "q": "An account loses 30%, then gains 30%. Where is it against the start?",
    "options": [
      "Exactly back at the start",
      "−9%",
      "−0.9%",
      "+9%"
    ],
    "answer": 1,
    "explain": "0.7 × 1.3 = 0.91, so −9%. Drawdown and recovery are not symmetric: after −50% you need +100%. That is why protecting capital beats chasing returns."
  },
  {
    "q": "With a 50% win rate you hit five losses in a row. What does the maths say?",
    "options": [
      "The strategy is broken and must be replaced",
      "The market has changed",
      "It is nearly impossible",
      "It is normal: such a streak shows up roughly once in 32 runs"
    ],
    "answer": 3,
    "explain": "0.5⁵ = 3.1%, about 1 in 32. A losing streak on its own proves nothing — changing a strategy over five trades means changing it in response to noise."
  },
  {
    "q": "Twenty trades produced +6R in total. What can you correctly say about that?",
    "options": [
      "The strategy has proven an edge",
      "You can safely double your risk",
      "The sample is too small: chance alone produces that result in about 13% of runs",
      "The win rate is now guaranteed to hold"
    ],
    "answer": 2,
    "explain": "Over 20 trades, skill and luck are indistinguishable. Run your own numbers through the \"Skill or luck\" check — it measures what share of random runs match your result."
  },
  {
    "q": "Entry 1.1000, stop 1.0950, exit at 1.1120. How many R is that?",
    "options": [
      "+1.2R",
      "+2.4R",
      "+0.4R",
      "+120R"
    ],
    "answer": 1,
    "explain": "Risk = 50 pips = 1R. Result = 120 pips = 120 ÷ 50 = +2.4R. Counting trades in R rather than dollars is the only way to compare them when position sizes differ."
  },
  {
    "q": "A strategy makes +0.2R per trade at 1% risk over 8 trades a month. What monthly return should you expect?",
    "options": [
      "About 16%",
      "About 1.6%",
      "About 8%",
      "About 0.2%"
    ],
    "answer": 1,
    "explain": "0.2R × 1% × 8 = 1.6% a month — and that is with a strategy that works. Real numbers look boring; anything promising 30% a month is promising risk of ruin, not return."
  },
  {
    "q": "Moving the stop to break-even right after entry…",
    "options": [
      "Is always right — the trade becomes free",
      "Cuts risk but gets you stopped out by noise more often: the rule must be set in advance",
      "Changes nothing",
      "Increases the average win"
    ],
    "answer": 1,
    "explain": "There are no free upgrades: removing risk costs you a share of trades that would have gone on to win. It is a legitimate choice, but it belongs in your written rules and should be tested on history — not decided mid-trade out of fear."
  },
  {
    "q": "The daily loss limit of −2R is used up by lunchtime. What does a disciplined trader do?",
    "options": [
      "Wins it back with one large trade",
      "Keeps trading at half size",
      "Closes the terminal until tomorrow — that is what a limit is for",
      "Rolls the limit over and trades to −4R"
    ],
    "answer": 2,
    "explain": "A limit you can move is not a limit, it is a preference. Half size sounds reasonable but is the same rule-bending — and right after a limit is hit is exactly when your decisions are worst."
  },
  {
    "q": "What separates a Stop Out from a Margin Call?",
    "options": [
      "A Margin Call closes positions, a Stop Out is only a warning",
      "They are the same thing",
      "A Margin Call warns that free margin is low; a Stop Out is the broker force-closing positions",
      "The trader sets the Stop Out and the broker sets the Margin Call"
    ],
    "answer": 2,
    "explain": "First the Margin Call level warns that free margin is running low. If the loss keeps growing, Stop Out triggers and the broker closes positions itself, at market, without asking you."
  },
  {
    "q": "For the year: $3000 in profits and $1200 in losses. At a 12% personal income tax rate, what is due (Uzbekistan resident)?",
    "options": [
      "$360",
      "$216",
      "$144",
      "$0 — forex is not taxed"
    ],
    "answer": 1,
    "explain": "You declare the net annual result: ($3000 − $1200) × 12% = $216. You get $360 only by taxing the profits and forgetting to subtract the losses. Check soliq.uz — rules change."
  },
  {
    "q": "0.01 lots of EUR/USD — how much currency is that and what is a pip worth?",
    "options": [
      "100 units, pip ≈ $1",
      "10,000 units, pip ≈ $1",
      "1,000 units, pip ≈ $0.10",
      "1,000 units, pip ≈ $1"
    ],
    "answer": 2,
    "explain": "A standard lot is 100,000 units, so 0.01 lots = 1,000 EUR and a pip is worth $0.10. A microlot is the right size for a first live account."
  },
  {
    "q": "You have a 20-pip stop and NFP is released in a minute. What can go wrong with that specific stop?",
    "options": [
      "Nothing — the stop guarantees exactly a 20-pip loss",
      "A price gap fills the stop beyond the level and the loss exceeds the plan",
      "The stop is cancelled automatically",
      "The broker widens the stop for you"
    ],
    "answer": 1,
    "explain": "On a news release price jumps over levels and the spread widens. The stop fills at the first available price, sometimes far past the level. Sitting out the release is cheaper for a beginner than paying for that fill."
  },
  {
    "q": "Two traders run the same strategy with +0.2R expectancy. One risks 1% per trade, the other 10%. Over 200 trades…",
    "options": [
      "The second earns exactly ten times more",
      "Results are the same in percentage terms",
      "The second has lower risk — they reach profit faster",
      "The second is far more likely to blow the account despite the same expectancy"
    ],
    "answer": 3,
    "explain": "A positive expectancy only pays the trader who survives long enough to reach it. At 10% risk, seven losses take over half the account and recovery becomes mathematically hopeless. Risk size decides whether you ever see your own edge."
  },
  {
    "q": "Three profitable months on demo. What does this NOT prove?",
    "options": [
      "That you will sit through the same drawdown when the money is real",
      "That you know your way around the terminal",
      "That the strategy rules can be followed mechanically",
      "That you can calculate position size"
    ],
    "answer": 0,
    "explain": "Demo tests mechanics and rules, not psychology. The only way to find out how you behave during a real loss is a live account with minimal size."
  },
  {
    "q": "Which of these is NOT, on its own, a sign of fraud?",
    "options": [
      "A guaranteed 30% profit per month",
      "Being asked to deposit more money in order to withdraw profits",
      "1:500 leverage",
      "No licence and no registered legal entity"
    ],
    "answer": 2,
    "explain": "High leverage is offered by legitimate non-EU brokers too — the danger is using it, not seeing it on a list. A guaranteed return and \"pay more to withdraw\", on the other hand, mean the money is already gone."
  },
  {
    "q": "What makes a journal entry usable for analysis?",
    "options": [
      "A chart screenshot with no notes",
      "The reason for entry and whether the rules were followed, written down BEFORE the outcome is known",
      "The month's total P/L",
      "An entry written from memory at the end of the week"
    ],
    "answer": 1,
    "explain": "Once a trade closes, memory rewrites the motive to fit the result: a win looks like analysis, a loss like bad luck. Only what you recorded in advance carries information."
  },
  {
    "q": "Why is the London–New York overlap easier for a beginner on EUR/USD?",
    "options": [
      "Price trends during those hours",
      "More volume and a tighter spread",
      "The risk of losing is lower then",
      "The broker lowers commission"
    ],
    "answer": 1,
    "explain": "Peak liquidity means a tight spread and less slippage — a cheaper entry and a fairer stop fill. Liquidity promises nothing about direction."
  },
  {
    "q": "Which skill decides a beginner's account over the long run?",
    "options": [
      "Accuracy in predicting direction",
      "Reacting quickly to the news",
      "A correctly tuned indicator",
      "Risk management and discipline"
    ],
    "answer": 3,
    "explain": "Nobody predicts direction consistently. The survivors are the ones who cap the loss and follow their own rules — which is what this entire exam was testing."
  },
  {
    "q": "What is a pip worth on EUR/JPY for one lot if USD/JPY is 150?",
    "options": [
      "$10 — the same as any major",
      "About $6.67",
      "About $66.70",
      "It depends on the EUR/USD rate"
    ],
    "answer": 1,
    "explain": "Pip value is set by the quote currency, not the base one. A pip on any yen pair is 0.01 × 100,000 = ¥1000, which in dollars is 1000 ÷ 150 = $6.67. That is why EUR/JPY and USD/JPY have the same pip value."
  },
  {
    "q": "$1000 account, $500 of margin in use, current floating loss of $300. What is the margin level?",
    "options": [
      "200%",
      "140%",
      "70%",
      "40%"
    ],
    "answer": 1,
    "explain": "Margin level = equity ÷ margin × 100% = (1000 − 300) ÷ 500 × 100% = 140%. Brokers usually set Stop Out between 20% and 50%: there is still room before a forced close, but it shrinks together with the loss."
  },
  {
    "q": "Commission is $7 per lot round turn (in and out). What does a 0.5-lot trade cost?",
    "options": [
      "$7.00",
      "$3.50",
      "$14.00",
      "$0.70"
    ],
    "answer": 1,
    "explain": "0.5 × $7 = $3.50, and that is before the spread. On tight stops the commission becomes a noticeable share of the risk — count it together with the spread, not separately."
  },
  {
    "q": "$1000 account, a steady +2% a month. After a year, withdrawing everything versus withdrawing nothing:",
    "options": [
      "The same — $1240",
      "Nothing withdrawn: $1268; everything withdrawn: the account stays $1000 and $240 is in hand",
      "Nothing withdrawn: $1240; everything withdrawn: $1268",
      "The difference is under a dollar"
    ],
    "answer": 1,
    "explain": "1000 × 1.02¹² = $1268 against $1000 plus $240 in hand. Over one year the gap is small, and that is the point: compounding works over years, not months. Promises to double your money in a month have nothing to do with it."
  },
  {
    "q": "You made $500 for the year and withdraw it by SWIFT for $52. What share of the profit does the withdrawal eat?",
    "options": [
      "10.4%",
      "1.04%",
      "5.2%",
      "52%"
    ],
    "answer": 0,
    "explain": "52 ÷ 500 = 10.4%. A flat fee hits small amounts hardest: on $5000 the same transfer would cost 1%. Work out the withdrawal cost before deciding how much you earned."
  },
  {
    "q": "You closed half the position at +1R, moved the rest to break-even and got stopped there. What is the result?",
    "options": [
      "+1R",
      "+0.5R",
      "0R",
      "+2R"
    ],
    "answer": 1,
    "explain": "Half gave +1R, the rest gave zero: +0.5R in total. Partial closes cut the spread of outcomes, but they also cut the top: calm costs you average R. It is a choice, not a free upgrade."
  },
  {
    "q": "The trade is in the red and you add the same size again to \"average the entry\". What happened to the risk?",
    "options": [
      "It doubled, and the original stop no longer protects the plan",
      "It stayed the same — the entry price improved",
      "It went down: the average price is closer to the market",
      "It grew by a third"
    ],
    "answer": 0,
    "explain": "The size doubled, so every pip against you now costs twice as much. The average price really did improve — and that is the trap: a trade that was already going wrong is now twice the size of the plan."
  },
  {
    "q": "Your stop was in place, but Monday opened with a gap far beyond it. What happened?",
    "options": [
      "The stop filled at the first price after the gap — the loss is larger than planned",
      "The broker must fill the stop at the price you set",
      "The stop carries over to the next week",
      "The position closed at break-even"
    ],
    "answer": 0,
    "explain": "The market does not trade at the weekend, but the news keeps coming. A gap jumps over the stop level and it fills at the first available price. Holding through the weekend is a separate decision with a separate risk."
  },
  {
    "q": "A demo account fills trades better than a live one. Why?",
    "options": [
      "Demo does not reproduce slippage, requotes or spread widening",
      "Demo charges lower commission",
      "Demo uses a different quote provider",
      "There is no difference; it only feels that way"
    ],
    "answer": 0,
    "explain": "Demo fills instantly at the quote; the real market fills against available liquidity. So a strategy with tight stops and frequent trades looks better on demo than it will turn out to be live."
  },
  {
    "q": "A strategy with eight tunable parameters shows +300% on history. What is most likely?",
    "options": [
      "The parameters are fitted to the past and the result falls apart on new data",
      "The strategy really is very good",
      "Live will be even better — history understates it",
      "You just need to increase the size"
    ],
    "answer": 0,
    "explain": "The more knobs there are, the easier it is to fit the curve to what already happened. There is one test: run it on data the strategy did not see while being tuned. Beautiful backtests are exactly what \"robots\" are sold on."
  },
  {
    "q": "A trade has gone nowhere for three days, neither to the stop nor to the target. What is reasonable?",
    "options": [
      "Close it on a time rule, if that rule was in the plan",
      "Wait as long as it takes — the stop protects you anyway",
      "Add to it, since price is not going against you",
      "Move the target closer"
    ],
    "answer": 0,
    "explain": "Money in a stalled trade is tied up and doing nothing while the risk stays on. A time limit is a normal part of a plan — but it has to be written down BEFORE the entry, otherwise it is just impatience."
  },
  {
    "q": "To take 2R with a 30-pip stop, the market must…",
    "options": [
      "Travel 60 pips your way without touching the stop on the way",
      "Travel 30 pips",
      "Travel 60 pips in any order",
      "Close above your entry"
    ],
    "answer": 0,
    "explain": "A 2R target means 60 pips, and the path matters as much as the distance: if price first goes 30 pips against you, the trade is over. Wide targets need not just movement but a particular shape of it."
  },
  {
    "q": "A swap-free account charges no swap. Where does the broker make it back?",
    "options": [
      "From a wider spread, a higher commission or a status fee",
      "Nowhere — it is charity",
      "From other clients' volume",
      "From interest on your deposit"
    ],
    "answer": 0,
    "explain": "\"Swap-free\" redistributes the cost rather than removing it. Compare the full cost of your own scenario on both account types: frequent short trades barely accrue swap anyway, while a wider spread is paid on every single trade."
  },
  {
    "q": "You funded the account in UZS while the broker holds it in dollars. What risk was added?",
    "options": [
      "Currency risk: your result in UZS depends on both trading and the USD/UZS rate",
      "None, the broker fixes the rate",
      "Only the conversion fee",
      "A tax one — the amount is counted twice"
    ],
    "answer": 0,
    "explain": "A profit in dollars can lose value if the som strengthens, and the other way round. This does not mean \"do not trade\"; it means the result should be counted in the currency you actually spend — the journal can show both."
  },
  {
    "q": "The swap-free account has a spread 0.5 pips wider. At 40 trades a month at 0.1 lots, that is…",
    "options": [
      "$20 a month of extra cost",
      "$2 a month",
      "$200 a month",
      "Nothing, half a pip is invisible"
    ],
    "answer": 0,
    "explain": "0.5 × $1 per pip (0.1 lots) × 40 = $20. \"Half a pip\" sounds trivial, but it multiplies by every trade. Account types have to be compared at your own trade count, not on a single trade."
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
