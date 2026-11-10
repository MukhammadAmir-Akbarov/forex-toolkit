---
widgets: [drawdown]
---

# 🩹 Drawdown Recovery Calculator

!!! abstract "Why −50% does NOT mean 'just earn +50% back'"
    A drawdown is the fall of your account from its peak. The main beginner trap is that losses and gains in percent are **asymmetric**: after losing half of your account, you must **double** the remainder just to get back to breakeven.

    This calculator shows what gain your current hole requires — and why "winning it back fast" is mathematically out of reach.

---

## 🧮 Interactive Calculator

<div class="calc-widget">

<div class="calc-row">
  <label>Current drawdown (% from account peak)</label>
  <input type="number" id="dd-input" min="0" max="95" step="1" value="20">
  <span>%</span>
</div>

<button class="calc-button" id="dd-calc-btn">Calculate</button>

<div id="dd-result" class="calc-result"></div>

</div>

---

## 📐 The Formula (works without the calculator too)

If the account is down `d` percent, `100 − d` remains from the peak. To return to the original amount, the remainder must grow by:

```
required gain % = d / (100 − d) × 100
```

Example: a 20% drawdown → 80% remains → you need `20 / 80 × 100 = +25%` gain on the remainder.

---

## 📋 Cheat-Sheet Table

| Drawdown | Account remaining | Gain needed to recover | Times larger than the drawdown |
|---|---|---|---|
| −5% | 95% | +5.3% | ×1.05 |
| −10% | 90% | +11.1% | ×1.11 |
| −20% | 80% | +25.0% | ×1.25 |
| −30% | 70% | +42.9% | ×1.43 |
| −40% | 60% | +66.7% | ×1.67 |
| −50% | 50% | +100.0% | ×2.00 |

!!! warning "The danger zone starts at a 30% drawdown"
    Below −30% the required gain grows **faster** than the drawdown itself, and every additional percent of the hole costs more and more. Trying to "win it back" with increased risk usually ends in an even deeper hole — that is exactly how accounts get blown.

---

## 🎯 What This Means

1. **It is cheaper to avoid the hole than to climb out of it.** A −10% drawdown recovers almost symmetrically (+11.1%), while −50% demands a feat (+100%).
2. **Risking 1–2% per trade is protection against deep drawdowns.** A streak of 10 consecutive stops at 1% risk is −10% of the account (recoverable). At 10% risk it is −65% (you need +186% to recover).
3. **After a drawdown, reduce risk — never raise it.** "Revenge trading" with a bigger lot is the most reliable way to turn −20% into −50%.

---

## 🔗 What to Read Next

- [Risk of Ruin (Monte Carlo)](risk-of-ruin.md) — how drawdowns are distributed across scenarios
- [WinRate × RR calculator](winrate-rr-calculator.md) — the expected value of your strategy
- [Position calculator](position-calculator.md) — how to keep risk within 1–2%
- [LOT discipline](../practice/lot-discipline.md) — why lot size decides everything
- [Trading psychology](../extras/psychology.md) — why the urge to win it back is so strong

---

!!! note "Educational material"
    This calculator is intended **for educational purposes only** to understand the mathematics of risk. This is not financial advice and does not guarantee any result. Real trading always carries the risk of losing all invested capital.
