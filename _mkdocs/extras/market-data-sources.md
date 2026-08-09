# 📡 Источники данных и сигналов

!!! warning "Важно про «сигналы»"
    Под «сигналом» в форексе часто понимают **платные подсказки от «гуру»** в стиле «BUY EURUSD сейчас». **Это в основном скам** — если бы кто-то делал точные сигналы, он бы не продавал их за $50/мес, а торговал сам.

    Эта страница про другое: **сайты, которые помогают тебе самостоятельно принимать решения**.

## 📅 1. Экономический календарь (главное)

| Сайт | Описание |
|---|---|
| **[ForexFactory.com](https://www.forexfactory.com/calendar)** | Стандарт индустрии. Фильтр по impact (🔴 high). Смотри **за 24 часа** до сделки. |
| **[Investing.com](https://www.investing.com/economic-calendar/)** | Альтернатива с русским языком. |
| **[FxStreet.com](https://www.fxstreet.com/economic-calendar)** | С прогнозами и интерпретацией. |

**Главные события**: NFP (первая пятница), FOMC, ECB, BoE, CPI, GDP.

!!! danger "Правило"
    **Не торгуй за 30 минут до и после high-impact события.** Спред расширяется в 5-10 раз, проскальзывание убивает стопы.

## 📈 2. Графики и анализ

| Сайт | Зачем |
|---|---|
| **[TradingView.com](https://www.tradingview.com/chart/)** | Золотой стандарт, бесплатно. Все индикаторы, мульти-таймфреймы, alerts. |
| **MT5 в твоём брокере** | Для реальных сделок, входов по цене, алертов на стопе/тейке. |
| **[Finviz.com/forex](https://finviz.com/forex.ashx)** | Heatmap по всем парам. Видно где сильное движение. |

## 📊 3. Sentiment / позиционирование

«Что делает толпа? Что делают институты?»

| Сайт | Что показывает |
|---|---|
| **[IG Client Sentiment](https://www.dailyfx.com/sentiment)** | % retail-трейдеров long vs short. Когда 80%+ розницы в одну сторону — рынок часто идёт **против них** (contrarian indicator). |
| **[CFTC COT Report](https://www.cftc.gov/MarketReports/CommitmentsofTraders/index.htm)** | Еженедельный отчёт о позициях крупных институтов. Запаздывает на 3 дня, но показывает «куда смотрят умные деньги». |
| **[Myfxbook Community Outlook](https://www.myfxbook.com/community/outlook)** | То же что IG, агрегировано по брокерам. |

## 📰 4. Новости и макро

| Сайт | Зачем |
|---|---|
| **[ForexLive.com](https://www.forexlive.com/)** | Лучшая агрегация breaking news для форекса. Бесплатно. |
| **[Reuters Markets](https://www.reuters.com/markets/)** | Официальная аналитика. |
| **[Federal Reserve calendar](https://www.federalreserve.gov/newsevents/calendar.htm)** | Расписание выступлений Fed. ECB / BoE / BoJ имеют аналогичные. |
| **[TradingEconomics: ставки](https://tradingeconomics.com/country-list/interest-rate)** | Текущая ставка каждой страны и дата последнего изменения. |

## 🔗 5. Корреляции

Очень важная и недооценённая тема. **Если торгуешь EURUSD long и GBPUSD long — это по сути одна сделка** (обе пары обратно коррелируют с USD).

| Сайт | Описание |
|---|---|
| **[Mataf Currency Correlation](https://www.mataf.net/en/forex/tools/correlation)** | Матрица корреляций в реальном времени. |
| **[Myfxbook Correlation](https://www.myfxbook.com/forex-market/correlation)** | Альтернатива. |
| `tools/market_correlations.py` (твой проект) | Локальный расчёт корреляций с DXY / gold / SPY. |

## ⚡ 6. Волатильность

«Насколько эта пара обычно двигается? Какой адекватный стоп?»

| Сайт | Зачем |
|---|---|
| **[Mataf Volatility](https://www.mataf.net/en/forex/tools/volatility)** | Средний дневной диапазон каждой пары в пипсах. |
| **[CBOE VIX](https://www.cboe.com/tradable_products/vix/)** | «Индекс страха» по S&P. Высокий VIX = нервный рынок = форекс тоже трясёт. |

## 🏦 7. Календарь центробанков

| Сайт | Описание |
|---|---|
| **[Календарь ЕЦБ](https://www.ecb.europa.eu/press/calendars/html/index.en.html)** | Кто и когда выступает. У Fed / BoE / BoJ есть такие же. |
| **[BIS: ставки центробанков](https://www.bis.org/statistics/cbpol.htm)** | Официальная сводка ставок от Банка международных расчётов. |

---

## 🚫 Что НЕ мониторить

| Источник | Почему |
|---|---|
| ❌ Платные «signal services» | 99% продают убыточные сигналы. Если бы они работали — продавцы бы торговали сами. |
| ❌ Telegram «гуру» с обещаниями 10× | Selection bias: показывают только выигрыши, выходят из проигрышей молча. |
| ❌ Twitter/X крикуны «BUY EURUSD NOW» | Без объяснения логики — это шум, не сигнал. |
| ❌ YouTube «I made $50K trading forex» | Клик-бейт ради YouTube-рекламы, а не для тебя. |
| ❌ Brokers' research desk | Конфликт интересов: чем больше торгуешь, тем больше им комиссии. |

## 🛠️ Твои собственные инструменты

В этом же проекте уже есть автоматизированные инструменты:

```bash
# News scraper — Forex Factory high-impact события на сегодня
.venv/bin/python tools/news_scraper.py --high-only

# Pattern scanner — поиск свечных паттернов на CSV
.venv/bin/python tools/pattern_scanner.py --csv data.csv

# Market correlations — корреляции с DXY / gold / SPY
.venv/bin/python tools/market_correlations.py

# Telegram alerts — алерты на пробой EMA50
.venv/bin/python advanced/telegram_alerts.py
```

---

## 🎯 Workflow на день (рекомендация)

| Время | Что | Где |
|---|---|---|
| **Утром (09:00)** | Календарь на день | ForexFactory |
| **Перед сделкой** | Sentiment + COT | DailyFX + CFTC |
| **Открытие позиции** | Расчёт размера | [Калькулятор позиции](../tools/position-calculator.md) |
| **В течение дня** | Алерты на пробой EMA50 | твой Telegram-бот |
| **Вечером (22:00)** | Запись в журнал | `tools/journal_cli.py` |
| **Раз в неделю** | Анализ + COT | `tools/journal_analyzer.py` + CFTC |

!!! tip "Главное правило"
    **80% времени — наблюдение, 20% — действие.** Большинство новичков делают наоборот: смотрят 5 минут, открывают сделку, потом весь день переживают и теребят стопы.

---

## ⚠️ Дисклеймер

Это **образовательный** обзор. Все ссылки — публичные, бесплатные, без партнёрских ссылок. Перед использованием сторонних сервисов **сам проверь** их актуальность и условия. Решения о торговле принимаешь ты, под свою ответственность.
