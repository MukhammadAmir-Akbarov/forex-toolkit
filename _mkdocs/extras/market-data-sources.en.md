# 📡 Market data sources

!!! warning "Important about "signals""
    In forex, "signal" often means **paid tips from a "guru"** like "BUY EURUSD NOW." **This is mostly a scam** — if someone had accurate signals, they wouldn't sell them for $50/month, they'd trade them.

    This page is about something else: **websites that help you make your own decisions.**

## 📅 1. Economic calendar (the main one)

| Site | Description |
|---|---|
| **[ForexFactory.com](https://www.forexfactory.com/calendar)** | Industry standard. Filter by impact (🔴 high). Check **24 hours** before opening a trade. |
| **[Investing.com](https://www.investing.com/economic-calendar/)** | Alternative with prediction polls. |
| **[FxStreet.com](https://www.fxstreet.com/economic-calendar)** | Forecasts + analyst interpretation. |

**Key events**: NFP (first Friday), FOMC, ECB, BoE, CPI, GDP.

!!! danger "Rule"
    **Don't trade in the 30 minutes before or after a high-impact event.** Spreads widen 5-10×, slippage will eat your stops.

## 📈 2. Charts & analysis

| Site | Why |
|---|---|
| **[TradingView.com](https://www.tradingview.com/chart/)** | Gold standard, free. All indicators, multi-timeframe, alerts. |
| **MT5 from your broker** | For real entries, exits, and stop/take alerts. |
| **[Finviz.com/forex](https://finviz.com/forex.ashx)** | Heatmap across all pairs — instantly see where movement is. |

## 📊 3. Sentiment / positioning

"What's the crowd doing? What are institutions doing?"

| Site | What it shows |
|---|---|
| **[IG Client Sentiment](https://www.dailyfx.com/sentiment)** | % of retail traders long vs short. When 80%+ retail is one side, the market often goes **against them** (contrarian indicator). |
| **[CFTC COT Report](https://www.cftc.gov/MarketReports/CommitmentsofTraders/index.htm)** | Weekly report of large institutional positions. 3-day lag but shows where "smart money" is looking. |
| **[Myfxbook Community Outlook](https://www.myfxbook.com/community/outlook)** | Same as IG, aggregated across brokers. |

## 📰 4. News & macro

| Site | Why |
|---|---|
| **[ForexLive.com](https://www.forexlive.com/)** | Best aggregation of forex breaking news. Free. |
| **[Reuters Markets](https://www.reuters.com/markets/)** | Official market analysis. |
| **[Federal Reserve calendar](https://www.federalreserve.gov/newsevents/calendar.htm)** | Schedule of Fed speeches. ECB / BoE / BoJ have equivalents. |
| **[TradingEconomics: rates](https://tradingeconomics.com/country-list/interest-rate)** | Current rate per country and the date it last changed. |

## 🔗 5. Correlations

Underrated topic. **If you're long EURUSD AND long GBPUSD — that's essentially one trade** (both inversely correlate with USD).

| Site | Description |
|---|---|
| **[Mataf Currency Correlation](https://www.mataf.net/en/forex/tools/correlation)** | Live correlation matrix. |
| **[Myfxbook Correlation](https://www.myfxbook.com/forex-market/correlation)** | Alternative. |
| `tools/market_correlations.py` (your project) | Local correlations with DXY / gold / SPY. |

## ⚡ 6. Volatility

"How much does this pair usually move? What's a reasonable stop?"

| Site | Why |
|---|---|
| **[Mataf Volatility](https://www.mataf.net/en/forex/tools/volatility)** | Average daily range of each pair in pips. |
| **[CBOE VIX](https://www.cboe.com/tradable_products/vix/)** | S&P "fear index". High VIX = nervous market = forex shakes too. |

## 🏦 7. Central bank calendar

| Site | Description |
|---|---|
| **[ECB calendar](https://www.ecb.europa.eu/press/calendars/html/index.en.html)** | Who speaks when. Fed / BoE / BoJ publish the same. |
| **[BIS: central bank policy rates](https://www.bis.org/statistics/cbpol.htm)** | The official summary from the Bank for International Settlements. |

---

## 🚫 What NOT to follow

| Source | Why |
|---|---|
| ❌ Paid "signal services" | 99% sell losing signals. If they worked, the seller would trade them. |
| ❌ Telegram "gurus" promising 10× | Selection bias: they show winning trades, quietly exit losers. |
| ❌ Twitter/X shouters "BUY EURUSD NOW" | No logic explained — that's noise, not a signal. |
| ❌ YouTube "I made $50K trading forex" | Clickbait for YouTube ads, not for you. |
| ❌ Broker research desks | Conflict of interest: more trades = more commissions for them. |

## 🛠️ Your own tools

The project already has automated tools:

```bash
# News scraper — today's high-impact events on Forex Factory
.venv/bin/python tools/news_scraper.py --high-only

# Pattern scanner — candle patterns on CSV
.venv/bin/python tools/pattern_scanner.py --csv data.csv

# Market correlations — vs DXY / gold / SPY
.venv/bin/python tools/market_correlations.py

# Telegram alerts — EMA50 crossover alerts
.venv/bin/python advanced/telegram_alerts.py
```

---

## 🎯 Suggested daily workflow

| Time | What | Where |
|---|---|---|
| **Morning (09:00)** | Check calendar | ForexFactory |
| **Before opening** | Sentiment + COT | DailyFX + CFTC |
| **Open position** | Size calculation | [Position calculator](../tools/position-calculator.md) |
| **During the day** | EMA50 break alerts | your Telegram bot |
| **Evening (22:00)** | Journal entry | `tools/journal_cli.py` |
| **Weekly** | Review + COT update | `tools/journal_analyzer.py` + CFTC |

!!! tip "Main rule"
    **80% of the time is observation, 20% is action.** Most beginners do the opposite: glance for 5 minutes, open a trade, then spend the day moving stops emotionally.

---

## ⚠️ Disclaimer

This is **educational**. All links are public, free, no affiliate links. Before using any third-party service, **verify it yourself**. All trading decisions are yours alone.
