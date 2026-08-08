---
widgets: [pip]
---

# 💲 Pip Value Calculator

!!! abstract "Why it matters"
    A pip is the **smallest unit of price movement**. How much money you win or lose per pip depends on your **position size** and the **pair**. Without understanding pip value, you can't correctly calculate risk.

## Formula

```
Lot size       =  100,000 base-currency units
Pip size       =  0.0001 for most pairs, 0.01 for JPY pairs
Pip value (USD)=  pip_size × lot × position_size  /  rate (if USD is quote or base)
```

---

<div class="pos-calc-widget" id="pip-calc">

<form class="pos-calc-form" onsubmit="return false">
  <label>
    Currency pair
    <select id="pp-pair">
      <option value="EURUSD">EUR / USD</option>
      <option value="GBPUSD">GBP / USD</option>
      <option value="AUDUSD">AUD / USD</option>
      <option value="NZDUSD">NZD / USD</option>
      <option value="USDJPY">USD / JPY</option>
      <option value="USDCHF">USD / CHF</option>
      <option value="USDCAD">USD / CAD</option>
      <option value="EURJPY">EUR / JPY</option>
      <option value="GBPJPY">GBP / JPY</option>
      <option value="EURGBP">EUR / GBP</option>
      <option value="AUDJPY">AUD / JPY</option>
      <option value="CHFJPY">CHF / JPY</option>
      <option value="EURAUD">EUR / AUD</option>
      <option value="EURCHF">EUR / CHF</option>
    </select>
  </label>
  <label>
    Position size (lots)
    <input type="number" id="pp-lots" value="0.10" min="0.01" step="0.01" autocomplete="off">
    <span class="pc-meta">0.01 = micro, 0.1 = mini, 1.0 = standard.</span>
  </label>
  <label>
    USD→UZS rate (so'm, optional)
    <input type="number" id="pp-uzs" value="12600" min="0" step="any" autocomplete="off">
    <span class="pc-meta">Used only for the additional result in so'm.</span>
  </label>
  <label class="pc-checkbox pc-row-wide">
    <input type="checkbox" id="pp-live" checked>
    <span>Use live ECB rate (recommended)</span>
  </label>
  <button type="button" id="pp-calc-btn" class="pc-row-wide">Calculate</button>
</form>

<div id="pp-result" class="pc-result" style="display: none;">
  <div class="pc-headline" id="pp-headline">— $ / pip</div>
  <div class="pc-result-grid">
    <div class="pc-result-row"><span>Pair</span><span id="pp-out-pair">—</span></div>
    <div class="pc-result-row"><span>Position size</span><span id="pp-out-lots">—</span></div>
    <div class="pc-result-row"><span>Pip size</span><span id="pp-out-pipsize">—</span></div>
    <div class="pc-result-row"><span>Rate used</span><span id="pp-out-rate">—</span></div>
    <div class="pc-result-row"><span>1 pip value</span><span id="pp-out-pip">—</span></div>
    <div class="pc-result-row"><span>10 pips</span><span id="pp-out-10">—</span></div>
    <div class="pc-result-row" id="pp-out-uzs-row"><span>1 pip in so'm</span><span id="pp-out-uzs">—</span></div>
    <div class="pc-result-row" id="pp-out-uzs-10-row"><span>10 pips in so'm</span><span id="pp-out-uzs-10">—</span></div>
  </div>
  <div class="pc-warnings" id="pp-warnings"></div>
</div>


</div>

---

## Examples

| Pair | 1 pip on 0.1 lot | 1 pip on 1 lot (std) |
|---|---|---|
| EUR/USD | $1.00 | $10.00 |
| GBP/USD | $1.00 | $10.00 |
| USD/JPY (rate ~150) | $0.67 | $6.67 |
| USD/CHF (rate ~0.88) | $1.14 | $11.36 |
| EUR/JPY (rate EUR/JPY ~162) | $0.67 | $6.67 |
| EUR/GBP (GBP/USD ~1.27) | $1.27 | $12.70 |

## Why it matters

- **Verify broker calculator** — some platforms display inaccurate pip value
- **Compare pairs** — why the same 25-pip stop costs less on USDJPY than on EURUSD
- **Account currency conversion** — if your account isn't in USD, an extra step is needed

## Python equivalent

See [`tools/pip_calculator.py`](https://github.com/MukhammadAmir-Akbarov/forex-toolkit/blob/main/tools/pip_calculator.py).
