# 🚦 Pre-Trade Checklist (Green Light)

!!! abstract "Why do you need this checklist?"
    Most beginners' losses happen not because the setup was "bad" — but because the trade was opened **without checking the basic conditions**: no stop, oversized risk, on emotion, or as a revenge trade.

    This checklist works like a **pilot's pre-flight check**: boring, but mandatory. If even one box is unchecked — **the trade does not open**.

!!! warning "Educational material — not financial advice"
    This page is part of an educational project. Everything described here is educational content and does not constitute financial advice. Trading involves real risk.

---

## 🚦 Checklist Before Entering a Trade

<style>
.pretrade-widget {
  background: var(--md-code-bg-color);
  border: 1px solid var(--md-default-fg-color--lightest);
  border-radius: 12px;
  padding: 1.5rem;
  margin: 1.5rem 0;
}

.pretrade-item {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
  padding: 0.75rem 0.9rem;
  margin-bottom: 0.5rem;
  border-radius: 8px;
  background: var(--md-default-bg-color);
  border: 1px solid var(--md-default-fg-color--lightest);
  cursor: pointer;
  transition: border-color 0.18s, background 0.18s;
  user-select: none;
}

.pretrade-item:hover {
  border-color: var(--md-primary-fg-color);
}

.pretrade-item.checked {
  border-color: #22c55e;
  background: rgba(34, 197, 94, 0.06);
}

.pretrade-item input[type="checkbox"] {
  margin-top: 3px;
  width: 18px;
  height: 18px;
  flex-shrink: 0;
  accent-color: #22c55e;
  cursor: pointer;
}

.pretrade-item-text {
  flex: 1;
  font-size: 0.96rem;
}

.pretrade-item-title {
  font-weight: 600;
  margin-bottom: 0.15rem;
}

.pretrade-item-hint {
  font-size: 0.82rem;
  color: var(--md-default-fg-color--light);
  margin-top: 0.1rem;
}

.pretrade-actions {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-top: 1.2rem;
  flex-wrap: wrap;
}

.pretrade-reset {
  background: none;
  border: 1px solid var(--md-default-fg-color--lighter);
  color: var(--md-default-fg-color--light);
  border-radius: 6px;
  padding: 0.5rem 1rem;
  font-size: 0.9rem;
  cursor: pointer;
}

.pretrade-reset:hover {
  border-color: var(--md-primary-fg-color);
  color: var(--md-primary-fg-color);
}

.pretrade-result {
  margin-top: 1.2rem;
  padding: 1.1rem 1.3rem;
  border-radius: 8px;
  border-left: 4px solid var(--md-primary-fg-color);
  background: var(--md-default-bg-color);
}

.pretrade-green {
  border-left-color: #22c55e;
  background: rgba(34, 197, 94, 0.07);
}

.pretrade-green .pt-verdict {
  color: #16a34a;
  font-size: 1.25rem;
  font-weight: 700;
  margin: 0 0 0.4rem;
}

.pretrade-red {
  border-left-color: #dc2626;
  background: rgba(220, 38, 38, 0.07);
}

.pretrade-red .pt-verdict {
  color: #dc2626;
  font-size: 1.25rem;
  font-weight: 700;
  margin: 0 0 0.4rem;
}

.pt-failed-list {
  margin: 0.6rem 0 0;
  padding-left: 1.2rem;
  font-size: 0.92rem;
}

.pt-failed-list li {
  margin-bottom: 0.3rem;
}

.pretrade-stats {
  margin-top: 1.2rem;
  padding: 0.9rem 1.2rem;
  background: var(--md-code-bg-color);
  border-radius: 8px;
  border: 1px solid var(--md-default-fg-color--lightest);
  font-size: 0.88rem;
}

.pretrade-stats-title {
  font-weight: 700;
  font-size: 0.92rem;
  margin-bottom: 0.5rem;
  color: var(--md-default-fg-color--light);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.pt-stat-row {
  display: flex;
  justify-content: space-between;
  padding: 0.22rem 0;
  border-bottom: 1px dashed var(--md-default-fg-color--lightest);
}

.pt-stat-row:last-child { border-bottom: none; }

.pt-stat-value {
  font-family: var(--md-code-font-family);
  font-weight: 700;
}

.pt-stat-green { color: #16a34a; }
.pt-stat-red { color: #dc2626; }

.pt-discipline-bar-wrap {
  margin-top: 0.6rem;
}

.pt-discipline-label {
  font-size: 0.82rem;
  color: var(--md-default-fg-color--light);
  margin-bottom: 0.2rem;
}

.pt-discipline-bar-bg {
  width: 100%;
  height: 8px;
  background: var(--md-default-fg-color--lightest);
  border-radius: 99px;
  overflow: hidden;
}

.pt-discipline-bar-fill {
  height: 100%;
  border-radius: 99px;
  background: #22c55e;
  transition: width 0.4s ease;
}
</style>

<div class="pretrade-widget">

<div id="pt-item-0" class="pretrade-item" onclick="ptToggle(0)">
  <input type="checkbox" id="pt-cb-0" onclick="event.stopPropagation(); ptToggle(0)">
  <div class="pretrade-item-text">
    <div class="pretrade-item-title">🛑 Stop-loss is set</div>
    <div class="pretrade-item-hint">SL level is defined before entry and placed in the terminal — not just "in your head"</div>
  </div>
</div>

<div id="pt-item-1" class="pretrade-item" onclick="ptToggle(1)">
  <input type="checkbox" id="pt-cb-1" onclick="event.stopPropagation(); ptToggle(1)">
  <div class="pretrade-item-text">
    <div class="pretrade-item-title">💰 Risk ≤ 1% of account balance</div>
    <div class="pretrade-item-hint">Lot size is calculated so that the loss on this trade will not exceed 1% of the account</div>
  </div>
</div>

<div id="pt-item-2" class="pretrade-item" onclick="ptToggle(2)">
  <input type="checkbox" id="pt-cb-2" onclick="event.stopPropagation(); ptToggle(2)">
  <div class="pretrade-item-text">
    <div class="pretrade-item-title">🧮 Position size calculated with a calculator</div>
    <div class="pretrade-item-hint">Lot taken from the calculator — not "by eye" or "as usual"</div>
  </div>
</div>

<div id="pt-item-3" class="pretrade-item" onclick="ptToggle(3)">
  <input type="checkbox" id="pt-cb-3" onclick="event.stopPropagation(); ptToggle(3)">
  <div class="pretrade-item-text">
    <div class="pretrade-item-title">😤 This is not a revenge trade</div>
    <div class="pretrade-item-hint">I am not entering because I just got stopped out and want to "get my money back"</div>
  </div>
</div>

<div id="pt-item-4" class="pretrade-item" onclick="ptToggle(4)">
  <input type="checkbox" id="pt-cb-4" onclick="event.stopPropagation(); ptToggle(4)">
  <div class="pretrade-item-text">
    <div class="pretrade-item-title">📅 Economic calendar checked</div>
    <div class="pretrade-item-hint">No high-impact news in the next 30 minutes (NFP, rate decision, CPI, etc.)</div>
  </div>
</div>

<div id="pt-item-5" class="pretrade-item" onclick="ptToggle(5)">
  <input type="checkbox" id="pt-cb-5" onclick="event.stopPropagation(); ptToggle(5)">
  <div class="pretrade-item-text">
    <div class="pretrade-item-title">📋 Setup matches the trading plan</div>
    <div class="pretrade-item-hint">This entry is described in my trading plan. I am not trading a "new idea" on the fly</div>
  </div>
</div>

<div id="pt-item-6" class="pretrade-item" onclick="ptToggle(6)">
  <input type="checkbox" id="pt-cb-6" onclick="event.stopPropagation(); ptToggle(6)">
  <div class="pretrade-item-text">
    <div class="pretrade-item-title">📐 RR ≥ 1.5 (potential profit at least 1.5× the risk)</div>
    <div class="pretrade-item-hint">Distance to TP is at least 1.5 times greater than the distance to SL</div>
  </div>
</div>

<div id="pt-item-7" class="pretrade-item" onclick="ptToggle(7)">
  <input type="checkbox" id="pt-cb-7" onclick="event.stopPropagation(); ptToggle(7)">
  <div class="pretrade-item-text">
    <div class="pretrade-item-title">🔢 Daily trade limit not exceeded</div>
    <div class="pretrade-item-hint">I have not yet reached my maximum trades for today (typically 2–3 maximum)</div>
  </div>
</div>

<div class="pretrade-actions">
  <button class="calc-button" onclick="ptCheck()">Check</button>
  <button class="pretrade-reset" onclick="ptReset()">Reset</button>
</div>

<div id="pt-result" class="pretrade-result" style="display:none;"></div>

<div id="pt-stats" class="pretrade-stats">
  <div class="pretrade-stats-title">Discipline Statistics (this browser)</div>
  <div class="pt-stat-row">
    <span>Green checks (all OK)</span>
    <span class="pt-stat-value pt-stat-green" id="pt-green-count">—</span>
  </div>
  <div class="pt-stat-row">
    <span>Red attempts (not all OK)</span>
    <span class="pt-stat-value pt-stat-red" id="pt-red-count">—</span>
  </div>
  <div class="pt-stat-row">
    <span>Discipline coefficient</span>
    <span class="pt-stat-value" id="pt-discipline-pct">—</span>
  </div>
  <div class="pt-discipline-bar-wrap">
    <div class="pt-discipline-label">% of submissions with full checklist</div>
    <div class="pt-discipline-bar-bg">
      <div class="pt-discipline-bar-fill" id="pt-disc-bar" style="width:0%"></div>
    </div>
  </div>
</div>

</div>

<script>
(function () {
  var TOTAL = 8;
  var KEY_RED = 'ftk-pretrade-redattempts';
  var KEY_GREEN = 'ftk-pretrade-greenattempts';

  function getCount(key) {
    return parseInt(localStorage.getItem(key) || '0', 10);
  }

  function incCount(key) {
    localStorage.setItem(key, getCount(key) + 1);
  }

  function ptToggle(idx) {
    var cb = document.getElementById('pt-cb-' + idx);
    var item = document.getElementById('pt-item-' + idx);
    cb.checked = !cb.checked;
    item.classList.toggle('checked', cb.checked);
  }

  window.ptToggle = ptToggle;

  window.ptCheck = function () {
    var failed = [];
    var labels = [
      'Stop-loss is set',
      'Risk ≤ 1% of account balance',
      'Position size calculated with a calculator',
      'This is not a revenge trade',
      'Economic calendar checked',
      'Setup matches the trading plan',
      'RR ≥ 1.5',
      'Daily trade limit not exceeded'
    ];

    for (var i = 0; i < TOTAL; i++) {
      if (!document.getElementById('pt-cb-' + i).checked) {
        failed.push(labels[i]);
      }
    }

    var resultEl = document.getElementById('pt-result');
    resultEl.style.display = 'block';

    if (failed.length === 0) {
      incCount(KEY_GREEN);
      resultEl.className = 'pretrade-result pretrade-green';
      resultEl.innerHTML =
        '<div class="pt-verdict">✅ You may open the trade</div>' +
        '<p style="margin:0;font-size:0.93rem;">All conditions are met. Open the trade strictly according to plan — do not move your stop or target after entry.</p>';
    } else {
      incCount(KEY_RED);
      var listItems = failed.map(function (f) { return '<li>' + f + '</li>'; }).join('');
      resultEl.className = 'pretrade-result pretrade-red';
      resultEl.innerHTML =
        '<div class="pt-verdict">🛑 DO NOT open</div>' +
        '<p style="margin:0 0 0.5rem;font-size:0.93rem;"><strong>' + failed.length + '</strong> of ' + TOTAL + ' conditions not met:</p>' +
        '<ul class="pt-failed-list">' + listItems + '</ul>' +
        '<p style="margin:0.7rem 0 0;font-size:0.85rem;color:var(--md-default-fg-color--light);">Fix all items, then click “Check” again.</p>';
    }

    updateStats();
    resultEl.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  };

  window.ptReset = function () {
    for (var i = 0; i < TOTAL; i++) {
      var cb = document.getElementById('pt-cb-' + i);
      var item = document.getElementById('pt-item-' + i);
      cb.checked = false;
      item.classList.remove('checked');
    }
    var resultEl = document.getElementById('pt-result');
    resultEl.style.display = 'none';
    resultEl.innerHTML = '';
  };

  function updateStats() {
    var green = getCount(KEY_GREEN);
    var red = getCount(KEY_RED);
    var total = green + red;

    document.getElementById('pt-green-count').textContent = green;
    document.getElementById('pt-red-count').textContent = red;

    if (total === 0) {
      document.getElementById('pt-discipline-pct').textContent = '—';
      document.getElementById('pt-disc-bar').style.width = '0%';
    } else {
      var pct = Math.round((green / total) * 100);
      document.getElementById('pt-discipline-pct').textContent = pct + '%';
      document.getElementById('pt-disc-bar').style.width = pct + '%';
      var bar = document.getElementById('pt-disc-bar');
      if (pct >= 80) {
        bar.style.background = '#22c55e';
      } else if (pct >= 50) {
        bar.style.background = '#f59e0b';
      } else {
        bar.style.background = '#dc2626';
      }
    }
  }

  window.addEventListener('DOMContentLoaded', updateStats);
}());
</script>

---

## 📖 Why Each Item Matters

### 1. Stop-loss is set

A stop in the terminal — not "in your head". A professional places it **before** opening the position. Without a stop you don't know how much you can lose: that is no longer trading, it is gambling.

### 2. Risk ≤ 1%

With a streak of 10 consecutive losses (rare, but it happens) you lose ~10% of your deposit — and the account survives. With 5% risk per trade — 10 losses = -50% of deposit, and your psychology is broken.

### 3. Position size with a calculator

"By eye" and "as usual" are the main reasons for violating the 1% rule. [Use the position calculator](../tools/position-calculator.md). 30 seconds that save money.

### 4. This is not a revenge trade

Got stopped out and now feel the urge to "get the money back right now"? That is a **revenge trade**. Such trades are statistically losing: you enter on emotion, not on logic. The [Anti-Tilt Protocol](anti-tilt-protocol.md) is your tool.

### 5. Economic calendar

NFP, Fed rate decision, CPI — these are "nuclear" news events. At the moment of release the spread widens and stops slip. For beginners — **do not trade 15–30 minutes before and after** major news.

!!! tip "Where to check"
    [Investing.com/economic-calendar](https://www.investing.com/economic-calendar/) or [ForexFactory.com](https://www.forexfactory.com/calendar) — free, filter events by "High Impact".

### 6. Setup matches the plan

If this setup is not in your [trading plan](trading-plan-template.md) — you have not tested it. Do not trade what has not been verified at least on a demo account. "Looks like a good entry" is not a trading plan.

### 7. RR ≥ 1.5

With a 50% win rate and RR = 1.5 → the mathematical expectancy is **positive**. With RR = 0.8 — it is negative. The [WinRate × RR Calculator](../tools/winrate-rr-calculator.md) will show you the exact numbers.

| RR | Win rate needed to break even |
|---|---|
| 0.5 | 67% |
| 1.0 | 50% |
| **1.5** | **40%** |
| 2.0 | 33% |

### 8. Daily trade limit

More trades does not mean more profit. For beginners, overtrading is one of the top-3 reasons for blowing an account. Decide in advance: a maximum of **2–3 trades per day**. Once the limit is reached — close the computer.

---

## 🧠 What to do if you cannot check a box?

!!! danger "Red flag: \"I know I'm breaking the rule, but I'll enter anyway\""
    If you consciously ignore the checklist — that is not "experienced trader confidence". That is the beginning of tilt.

    Close the terminal. Read the [Anti-Tilt Protocol](anti-tilt-protocol.md).

**Cannot set SL** — either the platform does not allow it at the moment (a technical issue — solve that first), or you are hoping to "exit manually". That does not work.

**Risk > 1%** — the temptation to "increase size because this setup is really good" is a trap. Good setups happen regularly. This one is not the last.

**Revenge trade** — the only correct response: a 30-minute pause after a stop. Stand up, drink some water. The market is not going anywhere.

---

## 📋 Quick Reference Card

```
PRE-TRADE CHECKLIST — short version

☐  Stop-loss placed in the terminal
☐  Risk ≤ 1% of deposit
☐  Lot calculated with a calculator
☐  This is NOT a revenge trade
☐  News checked (≥ 30 min before event)
☐  Setup is in the trading plan
☐  RR ≥ 1.5
☐  Daily trade limit not exceeded

ALL 8 — green light ✅
Even one NO — stop 🛑
```

> **Print it out and keep it next to your monitor.**
> Until the checklist becomes a habit — use the paper version.

---

## 🔗 Related Pages

- [Anti-Tilt Protocol](anti-tilt-protocol.md) — what to do when you feel like breaking the rules
- [Emergency Card](emergency-card.md) — emergency help in a crisis
- [Position Calculator](../tools/position-calculator.md) — calculate the correct lot size
- [WinRate × RR Calculator](../tools/winrate-rr-calculator.md) — verify the math of your setup
- [Trading Plan — Template](trading-plan-template.md) — if you don't have a plan yet
- [Trading Psychology](psychology.md) — why the brain sabotages the rules
