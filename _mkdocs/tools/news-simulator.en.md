---
widgets: [news-sim]
---

# 📰 News simulator: what to do when NFP comes out

!!! abstract "What this is"
    Six situations every trader runs into: a red-flag news release in
    10 minutes while you hold an open position; the number is out and price is
    flying; an «insider tip» in Telegram. You pick an action and immediately see
    a breakdown based on the
    [news trading protocol](../practice/news-trading-protocol.md), the typical
    market reaction and a **real case from history**.

<div id="ns-widget"></div>

<script type="application/json" id="ns-scenarios">
[
  {
    "event": "🇺🇸 US inflation (CPI) in 10 minutes",
    "situation": "You are long USD/JPY: +40 pips in profit, stop 30 pips below entry. Analysts expect high inflation — «the dollar will only get stronger».",
    "options": [
      {"text": "Close the position before the release", "verdict": "best", "why": "CPI is a tier-1 event: 50–150+ pips within minutes in either direction. Profit is locked in before the release, not after."},
      {"text": "Move the stop to breakeven and hold", "verdict": "ok", "why": "Better than nothing, but at the release the spread widens and the stop may be filled with slippage — below breakeven."},
      {"text": "Add to the position — the analysts are sure, after all", "verdict": "bad", "why": "Analysts' expectations are already priced in. If the number comes in below the forecast, a doubled position doubles the hit too."},
      {"text": "Remove the stop so it doesn't get hit by a spike", "verdict": "bad", "why": "Without a stop the loss is unlimited, and after CPI a pair can move hundreds of pips in a day."}
    ],
    "reaction": "A surprise versus the forecast moves the dollar sharply and for a long time: in the first minutes there is a jerk with a wide spread, and then the move often continues all day.",
    "history": "On 10 November 2022, US inflation came in at ≈7.7% against the expected ≈8%. The dollar fell sharply: USD/JPY dropped from roughly 146–147 to ≈141–142 (≈−3–4%), and EUR/USD rose by ≈2 cents."
  },
  {
    "event": "🇺🇸 NFP came out far stronger than forecast",
    "situation": "You have no open positions. You have six months of demo behind you, and your trading plan has a rule for entering on news. The number is much better than forecast, EUR/USD fell 60 pips in 10 seconds — you want to sell right now.",
    "options": [
      {"text": "Sell at market immediately while it is falling", "verdict": "bad", "why": "In these seconds the spread is at its widest, and a market order will be filled with 5–30 pips of slippage. You are selling at the very bottom of the panic."},
      {"text": "Wait 5–15 minutes for the pullback to pass and the spread to narrow, then enter with a limit order according to your system", "verdict": "best", "why": "The «Wait for the dust to settle» strategy from the protocol: the direction is already visible, and the price and spread become fair."},
      {"text": "Skip this release and just watch", "verdict": "ok", "why": "Safe and useful. But you do have a rule for entering on news, and entering after the pullback according to the protocol is also acceptable."},
      {"text": "Open a double lot: the move is guaranteed, after all", "verdict": "bad", "why": "There are no guarantees: within 1–5 minutes price often pulls back 30–50% of the first move. A double lot on such a pullback means a double loss."}
    ],
    "reaction": "In the first seconds price jumps and the spread widens several times over. After 1–5 minutes there is often a pullback of 30–50% of the first move (a shakeout), and the direction of the day takes shape over 15–30 minutes.",
    "history": "On 3 February 2023, the US added ≈517 thousand new jobs against a forecast of ≈190 thousand; unemployment fell to 3.4%, the lowest since 1969. EUR/USD dropped ≈1% over the day, to ≈1.08."
  },
  {
    "event": "🇨🇭 The EUR/CHF 1.20 «floor» has held for three years",
    "situation": "The Swiss National Bank has promised for three years not to let EUR/CHF fall below 1.20. The pair is at 1.2010. The idea: a long with almost no risk — they «won't allow» it below 1.20, stop 30 pips away.",
    "options": [
      {"text": "Take more leverage: the risk is only 30 pips", "verdict": "bad", "why": "A 30-pip stop protects you only in a normal market. If the floor is scrapped, price will jump over the stop, and the loss will be many times larger than calculated."},
      {"text": "The usual 1% risk with a 30-pip stop", "verdict": "ok", "why": "Disciplined, but the calculation holds only without a price gap: if the floor breaks, the stop will be filled far lower, and 1% turns into a many times larger loss."},
      {"text": "A small size with a margin for a price gap, and a broker with negative balance protection", "verdict": "best", "why": "A central bank's promise is not a guarantee. Size is calculated to survive a price gap, not only the stop being triggered."},
      {"text": "No stop — they won't allow it below 1.20 anyway", "verdict": "bad", "why": "This is betting the whole deposit on the central bank's word. And that word changes without warning."}
    ],
    "reaction": "When a central bank suddenly changes policy, there is no liquidity: price does not move, it jumps over levels. Stop orders are filled at the first available price — sometimes hundreds of pips from the one you set.",
    "history": "On 15 January 2015, the Swiss National Bank abandoned the EUR/CHF = 1.20 lower limit without warning. Within minutes the pair fell to roughly 0.85–0.90: the euro lost ≈25–30% against the franc. Stops were filled far worse than set; the broker FXCM received a rescue loan of ≈$300 million, and Alpari UK went bankrupt."
  },
  {
    "event": "🇬🇧 Referendum results overnight",
    "situation": "In the evening you are long GBP/USD: polls promise that Britain will stay in the EU. The results will be announced overnight, while you are asleep.",
    "options": [
      {"text": "Close the position before night: the outcome is binary, and you are away from the terminal", "verdict": "best", "why": "Under the protocol, positions are closed around tier-1 events. Polls are not the result, and at night there is nobody to react."},
      {"text": "Reduce to the minimum size and set a stop", "verdict": "ok", "why": "The risk is smaller, but at night a stop can be filled with a price gap — allow for losing more than the distance to the stop."},
      {"text": "Hold as is — the polls are for «remain», after all", "verdict": "bad", "why": "Polls get it wrong. Holding full size through a binary event means putting your entire risk on a coin flip."},
      {"text": "Increase the position: the market doesn't fully believe in «remain» yet", "verdict": "bad", "why": "This is not analysis but a bet on the outcome of a vote with maximum size and no protection against an overnight price gap."}
    ],
    "reaction": "Binary events (referendums, elections) produce price gaps: the market reprices a currency within minutes, liquidity is thin at night, and stops are filled worse than set.",
    "history": "On the night of 24 June 2016, when the referendum results became known, GBP/USD fell from roughly 1.50 to ≈1.33 (≈−10%). This is the lowest level since 1985."
  },
  {
    "event": "🇯🇵 Japan's Ministry of Finance: «ready to act decisively»",
    "situation": "USD/JPY is near 152 — a multi-decade high. You are long with a good profit. Japan's authorities have been warning of possible intervention for weeks.",
    "options": [
      {"text": "Lock in part of the profit and hold the rest with a stop you can afford to lose even with slippage", "verdict": "best", "why": "Warnings from the authorities are a red flag. The trend may continue, but the risk of a sharp reversal is now different."},
      {"text": "Close the whole position", "verdict": "ok", "why": "Safe. The only downside is that you exit the trend completely; if your system's rules say so, that is fine."},
      {"text": "Buy more: the trend is strong, there will be no intervention anyway", "verdict": "bad", "why": "Building up a position against direct warnings from the authorities is a bet that they are bluffing."},
      {"text": "Remove the stop so volatility doesn't knock it out", "verdict": "bad", "why": "Intervention moves price by hundreds of pips within hours. Without a stop that is no longer volatility but an unlimited loss."}
    ],
    "reaction": "Intervention is not announced in advance: the move starts suddenly, often in a thin market, and covers hundreds of pips within hours.",
    "history": "On 21 October 2022, USD/JPY reached ≈152, a 32-year high. Then Japan's Ministry of Finance intervened, and within a few hours the pair fell to roughly 146. In October Japan spent a record ≈6.3 trillion yen (≈$43 billion)."
  },
  {
    "event": "📱 An «insider tip» in a Telegram channel",
    "situation": "A popular channel writes: «Urgent! The Fed will cut rates in an emergency in an hour». There is nothing in the economic calendar, and the Fed's website is silent.",
    "options": [
      {"text": "Sell the dollar right away, before everyone finds out", "verdict": "bad", "why": "You are trading a rumour with no source. If it is fake, the move will reverse within minutes — against you."},
      {"text": "Check official sources and do nothing until there is confirmation", "verdict": "best", "why": "Confirmed data is what gets traded: the calendar, the central bank's website, major news agencies. A rumour with no source is not a signal."},
      {"text": "Don't enter, but close your positions just in case", "verdict": "ok", "why": "Cautious, but with no real reason: you pay the spread for reacting to a rumour. Check the source first."},
      {"text": "Open a position with high leverage before it is too late", "verdict": "bad", "why": "Maximum size on an unverified rumour is exactly how fake news empties accounts."}
    ],
    "reaction": "Fake news moves price for seconds or minutes — until it is debunked. Then the move reverses, and those who jumped in last exit at the worst prices.",
    "history": "On 23 April 2013, hackers broke into the Twitter account of the AP agency and wrote about «explosions at the White House». The Dow Jones index fell by roughly 140–150 points (≈1%) within minutes, the S&P 500 briefly lost ≈$135 billion in market capitalisation — and the market recovered the drop within a few minutes."
  }
]
</script>

---

## How the result is scored

| Move | Points | What it means |
|---|---|---|
| ✅ Best by the protocol | 2 | This is how professionals protect their account |
| 🟡 Acceptable, but risky | 1 | Not a disaster, but the risk stays with you |
| ❌ Dangerous | 0 | This is how news empties accounts |

80% and above — the protocol is in your head. Below 50% — it is too early for
real news: demo and observation first. Dangerous moves automatically go into the
[flashcards](flashcards.md) with the «🔁 My mistakes» filter — review them.

## Three rules behind all the scenarios

1. **Before red-flag news, close the position** or at least move it to
   breakeven — and remember that a stop at the release can be filled with slippage.
2. **At the moment of the release, do nothing.** Enter 5–15 minutes later, on the
   pullback, with a limit order, following your system's rules.
3. **Central bank promises, polls and rumours are not a guarantee.** Size is
   calculated to survive a price gap, not only the stop being triggered.

Details — in the [news trading protocol](../practice/news-trading-protocol.md)
and the [fundamental analysis guide](../docs/fundamental-analysis-guide.md).

## Sources of the historical examples

The figures are rounded: different sources give slightly different lows and highs.

- US CPI, 10.11.2022 — [Bloomberg](https://www.bloomberg.com/news/articles/2022-11-10/dollar-dives-as-cpi-surprise-cuts-fed-interest-rate-hike-outlook), [CNBC](https://www.cnbc.com/2022/11/11/dollar-dives-investors-cheer-after-us-inflation-misses-forecasts.html)
- NFP, 03.02.2023 — [CNBC](https://www.cnbc.com/2023/02/03/jobs-report-january-2023-.html)
- SNB, 15.01.2015 — [CRS](https://www.everycrsreport.com/reports/IN10230.html), [FCA on Alpari UK](https://www.fca.org.uk/news/statements/news-customers-alpari-uk-limited)
- Brexit referendum, 24.06.2016 — [CNN Money](https://money.cnn.com/2016/06/24/investing/pound-crash-eu-referendum/)
- Japan's intervention, 21.10.2022 — [Japan's Ministry of Finance](https://www.mof.go.jp/english/policy/international_policy/reference/feio/quarter/2022_4Qe.html)
- AP Twitter hack, 23.04.2013 — [Bloomberg](https://www.bloomberg.com/news/articles/2013-04-23/a-fake-ap-tweet-sinks-the-dow-for-an-instant)

!!! danger "Not financial advice"
    The simulator teaches you to protect your account around news, not to guess
    its outcome. Historical moves are shown to help you understand risk, not as
    a forecast.
