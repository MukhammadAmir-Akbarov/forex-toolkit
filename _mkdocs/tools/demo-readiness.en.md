---
widgets: [readiness]
---

# 🚦 Am I ready for live? — demo verdict

!!! abstract "An honest answer instead of “it kind of works”"
    Enter your demo account stats — the tool checks them against the [demo-to-live checklist](../journal/demo-vs-real-comparison.md) and tells you straight: **ready** or **too early, and here is what to work on**. There is no “almost”: every unmet item costs real money on a live account.

    Take the numbers from your [trading journal](../journal/README.md) or MT5 report. Nothing is sent to a server.

---

## 🧮 Your demo stats

<div class="calc-widget">

<div class="calc-row"><label>Months trading on demo</label><input type="number" id="rd-months" min="0" step="1" value="1"></div>
<div class="calc-row"><label>Closed trades</label><input type="number" id="rd-trades" min="0" step="1" value="20"></div>
<div class="calc-row"><label>Win rate (share of winning trades)</label><input type="number" id="rd-winrate" min="0" max="100" step="1" value="45"><span>%</span></div>
<div class="calc-row"><label>Average RR (average win / average loss)</label><input type="number" id="rd-rr" min="0.1" step="0.1" value="1.5"></div>
<div class="calc-row"><label>Max drawdown of the demo account</label><input type="number" id="rd-dd" min="0" max="100" step="1" value="12"><span>%</span></div>
<div class="calc-row"><label>Trades that broke your own rules</label><input type="number" id="rd-viol" min="0" max="100" step="1" value="10"><span>%</span></div>
<div class="calc-row"><label><input type="checkbox" id="rd-journal"> I journal every trade</label></div>
<div class="calc-row"><label><input type="checkbox" id="rd-canlose"> I can afford to lose the whole live amount</label></div>

<button class="calc-button" id="rd-calc-btn">Check</button>

<div id="rd-result" class="calc-result"></div>

</div>

---

## 📋 Criteria and why

| Item | Threshold | Why |
|---|---|---|
| Time on demo | ≥ 3 months | One lucky month looks just like a system |
| Number of trades | ≥ 50 | On 10–20 trades the stats are noise |
| Win rate | ≥ 40% | Below that, losing streaks are hard to bear even with good RR |
| Profit Factor | ≥ 1.5 | A margin for spread, commission and slippage on a live account |
| Max drawdown | ≤ 20% | Deeper, and [recovery](drawdown-recovery.md) needs an outsized gain |
| Rule violations | < 5% of trades | The result should come from the system, not improvisation |
| Journal + “can afford to lose” | yes | No journal — nothing to fix; no cushion — pressure on every trade |

Profit Factor is derived from win rate and RR: `PF = winrate × RR / (1 − winrate)`. Expectancy in R per trade: `winrate × RR − (1 − winrate)`. More in the [WinRate × RR calculator](winrate-rr-calculator.md).

---

## 🔗 What next

- [Readiness test](risk-profile.md) — psychology and financial cushion (complements this verdict)
- [Demo vs Real](../journal/demo-vs-real-comparison.md) — how to move to live gradually
- [Risk of ruin](risk-of-ruin.md) — how your stats survive bad streaks

---

!!! note "Educational material"
    The verdict is a **learning guide**, not financial advice and not a guarantee of results. A completed checklist does not protect you from losses: live trading always carries the risk of losing all invested funds.
