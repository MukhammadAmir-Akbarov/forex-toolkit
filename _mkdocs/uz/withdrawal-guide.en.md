---
verified: 2026-06-10
---

# Guide to Withdrawing Money from a Broker to Uzbekistan

> ⚠️ This information is general, as of the date of compilation (verified 2026-06-10). Specific fees, timelines and **legal status** change — verify before making any transaction.

!!! danger "Important: P2P crypto exchange is illegal in Uzbekistan"
    Since **26 May 2025** Binance has disabled P2P for Uzbekistan residents, and the National
    Agency of Perspective Projects (**NAPP**) has clarified: transactions via P2P platforms
    and any activity with crypto assets **outside licensed providers are illegal**
    and carry legal liability (including criminal liability for illegal circulation
    of crypto assets).

    **The only legal way to exchange USDT for soums is through** NAPP-licensed providers:
    Binance — via partner **CoinPay** ([coinpay.uz](https://coinpay.uz)),
    **Telegram Wallet**, and exchanges **Kobea, Coinpay, Asterium** and licensed
    crypto shops. The current registry is at [napp.uz](https://napp.uz).
    Income through licensed providers, according to NAPP clarifications, is exempt from tax.

    If you don't want to deal with crypto — use the bank channels below
    (SWIFT / Visa-Mastercard / Wise): they are legal and simpler for reporting purposes.

    Sources: [spot.uz](https://www.spot.uz/ru/2025/05/28/blocked-p2p/),
    [gazeta.uz](https://www.gazeta.uz/en/2025/01/17/binance/),
    [podrobno.uz](https://podrobno.uz/cat/obchestvo/binance-mozhno-p2p-nelzya-napp-razyasnilo-poryadok-operatsiy-s-kripto-aktivami-dlya-grazhdan-uzbekis/),
    [napp.uz](https://napp.uz).

---

## Withdrawal Fee Calculator

!!! info "Educational material, not financial advice"
    The calculation is approximate: fees may change at any time. Always verify current terms on the broker's and payment system's website before making a real transfer.

<style>
.wd-calc-select {
  flex: 1 1 200px;
  padding: 0.45rem 0.7rem;
  font-size: 1rem;
  border: 1px solid var(--md-default-fg-color--lighter);
  border-radius: 6px;
  background: var(--md-default-bg-color);
  color: var(--md-default-fg-color);
  font-family: inherit;
}
.wd-calc-select:focus {
  outline: 2px solid var(--md-primary-fg-color);
  outline-offset: -1px;
}
.wd-best-row {
  margin-top: 0.9rem;
  padding: 0.65rem 0.9rem;
  border-radius: 6px;
  background: rgba(34, 197, 94, 0.1);
  border-left: 3px solid #22c55e;
  font-size: 0.92rem;
}
.wd-rate-hint {
  font-size: 0.78rem;
  color: var(--md-default-fg-color--light);
  margin-top: 0.25rem;
}
</style>

<div class="calc-widget">

<div class="calc-row">
  <label>Withdrawal amount (USD)</label>
  <input type="number" id="wd-amount" min="1" max="100000" step="1" value="500">
  <span>USD</span>
</div>

<div class="calc-row">
  <label>Withdrawal method</label>
  <select id="wd-method" class="wd-calc-select">
    <option value="usdt">💰 USDT TRC-20</option>
    <option value="visa">💳 Visa / Mastercard (USD)</option>
    <option value="swift">🏦 SWIFT to Uzbekistan bank</option>
    <option value="wise">📲 Wise</option>
    <option value="skrill">💵 Skrill / Neteller</option>
  </select>
</div>

<div class="calc-row">
  <label>USD → UZS rate</label>
  <input type="number" id="wd-rate" min="1000" max="99000" step="100" value="12600">
  <span>soum</span>
</div>
<div class="wd-rate-hint" style="margin-left:0; padding: 0 0 0.5rem 0;">
  Rate is approximate — check yourself at <a href="https://cbu.uz" target="_blank" rel="noopener">cbu.uz</a> or with your bank
</div>

<button class="calc-button" onclick="calcWithdrawal()">Calculate</button>

<div id="wd-result" class="calc-result"></div>

</div>

<script>
(function() {
  var METHODS = {
    usdt: {
      label: 'USDT → licensed exchange (CoinPay)',
      feeFixed: 4,
      feePct: 0,
      exchangeSpread: 0.02,
      speed: '15–60 min',
      note: 'Broker fee ~$3 + TRC-20 network ~$1. Selling USDT for soums — only via a NAPP-licensed provider (CoinPay/Kobea/Asterium, registry napp.uz), spread ~2%. P2P for UZ residents is closed and illegal.'
    },
    visa: {
      label: 'Visa / Mastercard',
      feeFixed: 0,
      feePct: 0.02,
      exchangeSpread: 0,
      speed: '1–5 days',
      note: 'Fee 1–3% of the amount. Midpoint 2% used.'
    },
    swift: {
      label: 'SWIFT to Uzbekistan bank',
      feeFixed: 52,
      feePct: 0,
      exchangeSpread: 0,
      speed: '3–7 business days',
      note: 'Fixed amount: broker $0–30 + correspondent bank $15–25 + your bank $0–20. Midpoint $52 used.'
    },
    wise: {
      label: 'Wise',
      feeFixed: 3,
      feePct: 0.0075,
      exchangeSpread: 0,
      speed: '1–3 days',
      note: 'Fixed ~$3 + 0.5–1% for conversion. Midpoint 0.75% used.'
    },
    skrill: {
      label: 'Skrill / Neteller',
      feeFixed: 0,
      feePct: 0.025,
      exchangeSpread: 0,
      speed: '1–2 days',
      note: 'Fee 2–3% of the amount. Midpoint 2.5% used.'
    }
  };

  function calcFee(amount, methodKey) {
    var m = METHODS[methodKey];
    var fee = m.feeFixed + amount * m.feePct + amount * m.exchangeSpread;
    return fee;
  }

  function findCheapest(amount) {
    var best = null;
    var bestFee = Infinity;
    Object.keys(METHODS).forEach(function(key) {
      var fee = calcFee(amount, key);
      if (fee < bestFee) {
        bestFee = fee;
        best = key;
      }
    });
    return { key: best, fee: bestFee };
  }

  function fmt(n) {
    return n.toFixed(2).replace(/\B(?=(\d{3})+(?!\d))/g, ' ');
  }

  function fmtUZS(n) {
    return Math.round(n).toLocaleString('en-US');
  }

  window.calcWithdrawal = function() {
    var amount = parseFloat(document.getElementById('wd-amount').value);
    var methodKey = document.getElementById('wd-method').value;
    var rate = parseFloat(document.getElementById('wd-rate').value);
    var resultEl = document.getElementById('wd-result');

    if (!amount || amount <= 0) {
      resultEl.innerHTML = '<div class="calc-warn"><h4>Enter the withdrawal amount</h4></div>';
      return;
    }
    if (!rate || rate < 1000) {
      resultEl.innerHTML = '<div class="calc-warn"><h4>Enter the USD → UZS rate</h4></div>';
      return;
    }

    var m = METHODS[methodKey];
    var fee = calcFee(amount, methodKey);
    var net = Math.max(0, amount - fee);
    var netUZS = net * rate;
    var feePct = (fee / amount) * 100;

    var statusClass = feePct <= 2 ? 'calc-ok' : feePct <= 4 ? 'calc-warn' : 'calc-error';
    var statusLabel = feePct <= 2 ? 'Low fees' : feePct <= 4 ? 'Moderate fees' : 'High fees';

    var cheapest = findCheapest(amount);
    var cheapestLabel = METHODS[cheapest.key].label;
    var isCheapestSelected = cheapest.key === methodKey;

    var cheapestHtml;
    if (isCheapestSelected) {
      cheapestHtml = '<div class="wd-best-row">The cheapest method for <strong>$' + fmt(amount) + '</strong> is <strong>' + cheapestLabel + '</strong> (already selected). Fee ~$' + fmt(cheapest.fee) + '.</div>';
    } else {
      cheapestHtml = '<div class="wd-best-row">The cheapest method for <strong>$' + fmt(amount) + '</strong> is <strong>' + cheapestLabel + '</strong> (~$' + fmt(cheapest.fee) + ' fee). You selected a different option — it costs $' + fmt(fee - cheapest.fee) + ' more.</div>';
    }

    var html = '<div class="' + statusClass + '">'
      + '<h4>' + statusLabel + ' — ' + m.label + '</h4>'
      + '<table class="calc-table">'
      + '<tr><td><strong>Withdrawal amount</strong></td><td>$' + fmt(amount) + '</td></tr>'
      + '<tr><td><strong>Estimated fee</strong></td><td>−$' + fmt(fee) + ' (' + feePct.toFixed(1) + '%)</td></tr>'
      + '<tr><td><strong>You will receive (USD)</strong></td><td><strong>$' + fmt(net) + '</strong></td></tr>'
      + '<tr><td><strong>Approximately in soums</strong></td><td><strong>' + fmtUZS(netUZS) + ' soum</strong></td></tr>'
      + '<tr><td><strong>Speed</strong></td><td>' + m.speed + '</td></tr>'
      + '</table>'
      + '<p style="margin:0.7rem 0 0; font-size:0.85rem; color:var(--md-default-fg-color--light);">Note: ' + m.note + '</p>'
      + '</div>'
      + cheapestHtml;

    resultEl.innerHTML = html;
  };

  document.addEventListener('DOMContentLoaded', function() {
    // Журнал знает прибыль за год и присылает её сюда: показанная там сумма
    // не равна тому, что придёт на карту, а раньше это была только сноска.
    var fromJournal = new URLSearchParams(window.location.search).get('amount');
    var asNumber = parseFloat(fromJournal);
    if (isFinite(asNumber) && asNumber > 0) {
      document.getElementById('wd-amount').value = Math.min(asNumber, 100000).toFixed(0);
    }
    window.calcWithdrawal();
    document.getElementById('wd-amount').addEventListener('input', window.calcWithdrawal);
    document.getElementById('wd-method').addEventListener('change', window.calcWithdrawal);
    document.getElementById('wd-rate').addEventListener('input', window.calcWithdrawal);
  });
})();
</script>

---

## The Golden Rule

**Never withdraw everything in a single transfer.** Split into 2–3 parts and test with a small amount first.

---

## Withdrawal Methods — Overview

| Method | Speed | Fee | Amount | Complexity | Legal in UZ |
|---|---|---|---|---|---|
| 💳 Visa/Mastercard USD | 1–5 days | 1–3% | up to $5k | 🟢 easy | ✅ bank channel |
| 🏦 SWIFT to UZ bank | 3–7 days | $25–50 | $1k+ | 🟡 moderate | ✅ bank channel |
| 📲 Wise | 1–3 days | 1–2% | up to $10k | 🟡 moderate | ✅ bank channel |
| 💵 Skrill / Neteller | 1–2 days | 2–3% | up to $5k | 🟢 easy | ⚠️ confirm with your bank upon deposit in UZ |
| 💰 USDT → licensed exchange | 15–60 min | ~2% + $4 | no limit | 🟡 moderate | ✅ only via CoinPay/Kobea/Asterium |
| ❌ USDT → P2P (Binance etc.) | — | — | — | — | 🚫 closed 26.05.2025, **illegal** |

---

## Method 1: USDT via Licensed Exchange (CoinPay/Kobea/Asterium)

Fast crypto route, but converting USDT to soums is **only** possible through a NAPP-licensed
provider. P2P on Binance and other foreign platforms for Uzbekistan residents
is closed and **illegal** — the step below replaces the old route with the legal one.

!!! warning "Do not use P2P"
    Previously this route ended with "sell USDT on P2P". **That is no longer allowed.**
    Sell USDT for soums only on a licensed platform (registry — [napp.uz](https://napp.uz)).
    If you don't need crypto — bank channels (Methods 2–3) are legal and simpler for tax purposes.

### Steps

#### 1. At the broker: withdraw to USDT
- Personal cabinet → Withdrawal → USDT TRC-20
- Provide your USDT address (you will get it in step 2)
- The broker typically charges a $1–5 fee + TRC-20 network fee ≈ $1
- Timeline: usually **15–60 minutes**, sometimes up to 24 hours

#### 2. Licensed provider (CoinPay / Kobea / Asterium / Telegram Wallet)
- Register and complete verification (KYC) on a NAPP-licensed platform.
  Binance works legally only via partner **CoinPay** ([coinpay.uz](https://coinpay.uz))
- In the platform wallet → Deposit → USDT TRC-20 → copy the address
- Give this address to your broker

#### 3. Selling USDT for soums — on the provider's platform (NOT P2P)
- On the licensed platform: sell USDT for UZS → withdraw to HUMO/UZCARD card
- Rate/spread is typically ~1–3% from market
- Card credit is generally the same day
- ✅ This is a legal channel; ❌ the "P2P" tab on Binance is unavailable and illegal for UZ residents

### Cost of the USDT → soum route

Example withdrawal of $1,000:
- Broker → USDT: −$3 fee
- TRC-20 network: −$1
- Licensed exchange spread ~2%: −$20
- **Total taken: ~$24 (2.4%)**

### Pros
- Fast
- Income through a licensed provider, per NAPP clarifications, is exempt from tax
- Low fees

### Cons
- Exchange verification required (passport + selfie)
- Only available through licensed providers — regular P2P sellers cannot be used

---

## Method 2: SWIFT to Uzbekistan Bank

### Steps

1. Open a **USD account** at a bank: Kapitalbank, Hamkorbank, Asaka, Anorbank, Uzpromstroibank
2. At the broker: Withdrawal → Bank Wire → enter SWIFT details
3. Timeline: **3–7 business days**, sometimes longer

### Cost

- Broker fee: $0–30 (depends on broker)
- Correspondent bank fee: $15–25
- Your bank fee: $0–20
- **Total: $30–75** regardless of amount (fixed)

**Cost-effective for amounts of $2,000+.**

### Cons
- Slow
- Bank may request documents (source of funds)
- Easier when withdrawing via a business entity; personal accounts sometimes see delays

---

## Method 3: Wise (formerly TransferWise)

### Steps

1. Register a Wise account (USD)
2. At the broker: Withdrawal → Wise (if supported) or SWIFT to Wise
3. On Wise, convert USD to UZS
4. Wise transfers to your HUMO/UZCARD card

### Cost
- Wise: 0.5–1% for USD → UZS transfer
- + $2–5 fixed fee

### Cons
- Not all brokers support direct withdrawal to Wise
- Wise limits depend on verification level

---

## ⚠️ What NOT to Do

### Do not sell USDT via P2P
- Binance P2P tab is closed for UZ residents as of 26.05.2025
- Per NAPP clarifications, P2P transactions by citizens are **illegal** and carry legal liability
- Exchange crypto for soums only through licensed providers (registry at [napp.uz](https://napp.uz))

### Do not use "no-KYC" Telegram exchangers
- Often scammers
- The rate may look attractive, but the risk of 100% loss is high

### Do not withdraw to "someone else's" USDT wallet
- A friend, relative, "manager" — no
- Only to your own wallet on an exchange

### Do not make large transfers in a single payment
- Amounts >$3,000–5,000 at once may attract the bank's attention
- Split into 2–3 transactions with an interval between them

### Do not withdraw everything on the same date
- Regular transfers look natural
- A sudden large withdrawal at year-end looks less natural

---

## Documents to Keep

After each withdrawal, save:

- 📄 **Broker confirmation** (withdrawal statement)
- 📄 **USDT transaction TXID** (if via crypto)
- 📄 **Screenshot of the P2P deal** (seller, time, amount)
- 📄 **Card statement** showing the soum credit
- 📄 **ATM receipt** when withdrawing cash

Keep for a **minimum of 3 years** in case of questions from the tax authority.

---

## Taxes — Brief Overview

See [tax-calculator.py](https://github.com/MukhammadAmir-Akbarov/forex-toolkit/blob/main/uz/tax-calculator.py) for calculations.

Key points:
- **Net annual income** is declared (profits − losses)
- Personal income tax 12% (as of 2026)
- Tax return filed by 1 April of the following year
- Paid on the **annual total**, not on each individual trade

---

## When to Hire an Accountant

- Trading income **> $5,000 / year**
- You have a primary job with an official salary → a correct combined return is needed
- You are unsure whether your filing is correct
- You received a **query from the tax authority** — consult a specialist immediately

---

## Contacts for Reference (not a recommendation, for information only)

| Where | What |
|---|---|
| soliq.uz | Official website of the Tax Committee |
| Personal taxpayer account | my.soliq.uz |
| soliq contact centre | 1198 |

---

[← Back to the main guide](../forex-guide.md)
