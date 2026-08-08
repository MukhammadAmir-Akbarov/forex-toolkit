---
widgets: [sessions]
---

# 🕐 Trading Sessions and Market Hours

!!! abstract "Why this matters"
    Forex runs 24 hours a day, 5 days a week, but **activity is not equal at all times**.
    Volatility, spreads, and the character of price movement all depend on which session is
    currently open. Knowing session hours lets you choose the time when your pair actually
    moves — and avoid sitting in a "dead" market.

## Four Sessions

| Session | Hours (UTC) | Tashkent (UTC+5) | Character |
|---|---|---|---|
| 🇦🇺 Sydney | 22:00–07:00 | 03:00–12:00 | Quiet, opens the week |
| 🇯🇵 Tokyo (Asia) | 00:00–09:00 | 05:00–14:00 | JPY, AUD; moderate |
| 🇬🇧 London (Europe) | 08:00–17:00 | 13:00–22:00 | Highest volume, tight spreads |
| 🇺🇸 New York (US) | 13:00–22:00 | 18:00–03:00 | High volatility, US news |

!!! warning "Daylight Saving Time (DST)"
    London and New York **shift by one hour** when switching to summer/winter time
    (Uzbekistan does not observe DST). So the hours above are a guide ±1 hour. The widget
    below calculates based on real UTC and your local timezone automatically.

---

<div class="calc-widget" id="ts-widget">

<form class="pos-calc-form" onsubmit="return false">
  <label>
    Your timezone
    <select id="ts-tz">
      <option value="Asia/Tashkent" selected>Tashkent (UTC+5)</option>
      <option value="Asia/Almaty">Almaty / Astana (UTC+5)</option>
      <option value="Europe/Moscow">Moscow (UTC+3)</option>
      <option value="Europe/London">London</option>
      <option value="America/New_York">New York</option>
      <option value="Asia/Tokyo">Tokyo</option>
      <option value="UTC">UTC</option>
    </select>
  </label>
</form>

<div id="ts-result">
  <div class="pc-headline" id="ts-clock">—</div>
  <div class="pc-result-grid" id="ts-sessions"></div>
  <div class="pc-warnings" id="ts-warnings"></div>
</div>

</div>

---

## Overlaps — where the money is

The strongest moves happen when **two sessions are open simultaneously**:

- **London + New York** (13:00–17:00 UTC / 18:00–22:00 Tashkent) — **the main window**.
  Maximum volume, tightest spreads, best liquidity for EUR/USD, GBP/USD.
- **Tokyo + London** (08:00–09:00 UTC) — a short window that energises the European open.

If you have limited time, trade the **London/New York overlap**. The majority of daily
volatility on major pairs falls within that window.

## Which pairs are active when

| Session | Active pairs |
|---|---|
| Tokyo | USD/JPY, AUD/USD, NZD/USD, JPY crosses |
| London | EUR/USD, GBP/USD, EUR/GBP, USD/CHF |
| New York | EUR/USD, GBP/USD, USD/CAD, gold (XAU/USD) |

## Practical takeaways

1. **Asia is quiet for EUR/GBP majors.** You can sit out the flat and avoid false breakouts.
2. **Do not trade at Friday's close or Monday's open** — spreads are wider, gaps occur.
3. **US news releases during the New York session** — check the
   [calendar](../docs/technical-analysis.md) and do not enter right before a release.
4. **Tight spreads = lower costs.** London/New York is cheaper to enter than quiet
   Asia. Calculate the difference with the [cost calculator](../tools/cost-calculator.md).

---

!!! danger "Not financial advice"
    Session hours are a guide. Real activity depends on the day of the week, public holidays,
    and the news background. Always look at the current market, not just the schedule.
