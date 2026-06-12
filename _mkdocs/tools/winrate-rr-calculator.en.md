# 📊 Win Rate × Risk-Reward — Profitability Calculator

!!! abstract "The Core Mathematics of Trading"
    From an experienced trader's practice: "This is the most common question — why am I not in profit?"

    **Answer:** your Win Rate (% of profitable trades) and your RR (Risk-Reward Ratio) are tied together by rigid mathematics. If you don't respect this relationship — you are losing **by mathematics**, not by "bad luck".

---

## 🧮 Interactive Calculator

<div class="calc-widget">

<div class="calc-row">
  <label>Win Rate (% of profitable trades)</label>
  <input type="number" id="wr-input" min="1" max="99" step="1" value="50">
  <span>%</span>
</div>

<div class="calc-row">
  <label>Risk-Reward Ratio (RR)</label>
  <input type="number" id="rr-input" min="0.1" max="20" step="0.1" value="1.5">
  <span>(1 risk : N reward)</span>
</div>

<div class="calc-row">
  <label>Number of trades (for forecast)</label>
  <input type="number" id="trades-input" min="10" max="1000" step="10" value="100">
</div>

<div class="calc-row">
  <label>Risk per trade (% of deposit)</label>
  <input type="number" id="risk-input" min="0.1" max="10" step="0.1" value="1">
  <span>%</span>
</div>

<button class="calc-button" id="wr-calc-btn">Calculate</button>

<div id="wr-result" class="calc-result"></div>

</div>


---

## 📋 Reference Table "WR vs Minimum RR"

| Win Rate | Minimum RR for breakeven | RR for +1% per trade (1% risk) | Realistic for a beginner? |
|---|---|---|---|
| 30% | 2.33 | 3.5+ | ❌ Difficult |
| 40% | 1.50 | 2.5 | ⚠️ Achievable |
| **50%** | **1.00** | **2.0** | ✅ Achievable |
| 60% | 0.67 | 1.5 | ✅ Achievable |
| 70% | 0.43 | 1.0 | ✅ Very achievable |
| 80% | 0.25 | 0.75 | ⚠️ Suspiciously high |
| 90% | 0.11 | 0.5 | ❌ Most likely a scam |

!!! warning "Win Rate above 75% — red flag"
    If someone promises a Win Rate of 85-90% — it is **mathematically possible**, but **only with tiny TP and huge SL** (RR < 0.5). In the long run such a strategy is **still** unprofitable, because 1 large stop-loss wipes out 5-10 small profits.

    **A realistic honest Win Rate for a profitable strategy: 45-65%** with RR ≥ 1.5.

---

## 💡 What This Means in Practice

### Example 1: The Beginner "who thinks he is right often"

```
WR = 70% (by their perception)
RR = 0.5 (they close profit early, hold losses long)

100 trades at 1% risk:
- 70 wins × 0.5% = +35%
- 30 losses × 1% = -30%
- Net: +5% over 100 trades

⚠️ There is profit, but it is microscopic. One rules violation → goes negative.
```

### Example 2: The Disciplined Trader

```
WR = 45% (they get stopped out often)
RR = 2.0 (but they hold for large TP)

100 trades at 1% risk:
- 45 wins × 2% = +90%
- 55 losses × 1% = -55%
- Net: +35% over 100 trades

✅ Strategy is profitable even with a low Win Rate.
```

### Example 3: The Greedy Trader

```
WR = 50%
RR = 0.8 (takes profit early, waits for a "better price")

100 trades at 1% risk:
- 50 wins × 0.8% = +40%
- 50 losses × 1% = -50%
- Net: -10% over 100 trades

❌ Strategy is negative. Greed kills.
```

---

## 🎯 Key Takeaways

1. **Win Rate is not the main thing** — what matters is the WR + RR combination
2. **RR 1:2 or higher** — the gold standard for a beginner
3. **Never move TP closer** "because price slowed down"
4. **Never move SL further** "because it almost reached"
5. **Calculate EV** before you start, not "we'll see how it goes"

---

## 💬 Practitioner's Quote

!!! quote
    *«Nega daromadga chiqmayapman degan savolga javob bo'ladigan — oddiy, lekin barcha bilishi zarur bo'lgan balans jadvali. Daromadga chiqish uchun ushbu jadval orqali siz Win rate ga qarab Risk rewardni qancha ushlashingiz kerakligi ko'rsatilgan.»*

    **Translation:** "The answer to the question 'why am I not in profit?' is a simple, yet essential table that everyone must know. It shows how much Risk-Reward you need to hold depending on your Win Rate."

---

## 🔗 What to Read Next

- [LOT discipline](../practice/lot-discipline.md) — without it neither WR nor RR will help
- [Breakeven Protocol (Move to BE)](../practice/breakeven-protocol.md) — protecting your achieved RR
- [Position Size Calculator](position-calculator.md) — calculate the correct lot size
- [Trading Psychology](../extras/psychology.md) — why you want to reduce RR
- [Study Strategy](../docs/strategy-details.md) — EMA50 Pullback with fixed RR=2
