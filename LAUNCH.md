# 🚀 LAUNCH — готовые посты для соцсетей

Этот файл — для тебя как maintainer'а. **Не публикуется на сайте**, нужен чтобы скопировать-вставить готовый текст в нужную платформу. Подменяй цифры под актуальное состояние, добавляй скриншоты.

> **Стратегия запуска**: 1 пост в день, разные платформы. **Не спам**. Замеряй: за неделю отслеживай Star count, traffic в Insights → Traffic, новые Discussions/Issues.

---

## 1️⃣ Reddit — r/Forex

**Лучшее время**: вторник-четверг, 8–10 AM UTC.

**Title**:
```
I built a free open-source forex educational toolkit: handbook + 30 Python tools + interactive calculators (no signups, no shilling)
```

**Body**:
```
Hey r/Forex,

After spending months learning forex the hard way, I built a free, open-source educational toolkit to save other beginners the same pain. Posting because I want feedback before declaring it "done."

What's inside:

📖 Full handbook (RU + EN) — 700+ lines covering theory, technical analysis, psychology, strategies. Available as online site, downloadable PDF, and Word doc.

🛠️ 30+ Python tools — position calculator with live ECB rates, pip value calc, compound interest with realism warnings (it'll tell you if "5% per month" promises are scams), Monte Carlo simulator, journal CLI with HTML dashboard.

🤖 Backtester with anti-tilt Risk Guardian — stops trading after N consecutive losses + daily loss limit. Plus 6 strategies with unit tests (EMA50 pullback, mean reversion, breakout, London open range, etc.). 74/74 tests pass on CI matrix (Ubuntu/macOS × Py 3.10-3.12).

📐 Interactive web calculators — no install, no signup. Just open and use.

🌐 Multilingual site (RU/EN/Uzbek), MIT licensed.

🇺🇿 Bonus: local guide for Uzbekistan traders (taxes, brokers, deposit/withdrawal).

**This is education, NOT financial advice.** 74-89% of retail traders lose money — the project says this loudly on every page.

I'm not selling anything. No signals, no courses, no broker referrals. Just want this to be useful.

🔗 Site: https://mukhammadamir-akbarov.github.io/forex-toolkit/
🔗 GitHub: https://github.com/MukhammadAmir-Akbarov/forex-toolkit
🔗 Try the calculator: https://mukhammadamir-akbarov.github.io/forex-toolkit/tools/position-calculator/

Would love feedback — especially on the strategy backtests and the position calculator math.
```

---

## 2️⃣ Reddit — r/algotrading

**Title**:
```
[OC] Backtester with anti-tilt Risk Guardian + 6 unit-tested strategies (Python, MIT)
```

**Body**:
```
Built an educational forex backtester in Python with features I haven't seen in other open-source toolkits:

**Risk Guardian (anti-tilt)** — auto-stops trading after N consecutive losses OR when daily P&L hits configured limit. Backtests can now simulate what disciplined traders actually do, not idealized infinite-account scenarios.

**Realistic spread modeling** — `--spread-pips` flag subtracts broker spread from PnL of every trade. Ideal cost = 0; realistic ECN = 1-2 pips. Win rate often drops 5-10% with realistic spreads.

**6 strategies with unit tests** (74/74 passing on CI):
- EMA50 pullback (trend-following)
- Mean reversion (Bollinger Bands)
- Breakout v1 + v2 (with filters)
- London Open Range
- Three Soldiers / Crows
- Carry trade (theory + framework)

**Walk-forward optimization** to avoid in-sample overfitting (see `advanced/walk_forward.py`).

**Stack**: Python 3.10+, pandas, matplotlib, yfinance. No exotic deps.

```bash
python bot/backtest.py --csv data.csv --spread-pips 2 \
    --max-consecutive-losses 3 --daily-loss-limit-r 2
```

Live calculators on the site (JS port of the Python tools, with live ECB rates):
https://mukhammadamir-akbarov.github.io/forex-toolkit/tools/position-calculator/

GitHub: https://github.com/MukhammadAmir-Akbarov/forex-toolkit

MIT license, no monetization. Looking for feedback on strategy logic and missing features.
```

---

## 3️⃣ Hacker News — "Show HN"

**Title** (max 80 chars):
```
Show HN: Open-source forex education — handbook, Python tools, web calculators
```

**Comment (your own first reply)**:
```
Hi HN — I'm the author. Background: spent 6+ months learning forex; realized most free resources are broker affiliate pages or "guru" course pitches with no actual content. So I built what I wished existed.

The toolkit has three layers:

1. **Education** — a 700-line handbook, online site (RU/EN/Uzbek), PDF, DOCX. With diagrams generated from real EUR/USD 2-year data, not idealized examples.

2. **Tools** — 30+ Python CLI scripts (position calculator, journal, Monte Carlo, broker checker), all unit-tested. Plus 3 interactive web calculators ported to JS that use real ECB rates via frankfurter.app (no API key, CORS-friendly).

3. **Strategies + backtester** — 6 strategies with unit tests, walk-forward optimization, anti-tilt "Risk Guardian" that stops trading after consecutive losses or hitting a daily loss limit.

Tech: Python 3.10+, mkdocs-material, GitHub Actions for CI + Pages deploy, no commercial dependencies, MIT.

What I'd love feedback on:
- The position-size calculator math — there's a Python version and a JS port; they should produce identical results for the same inputs
- Whether the realistic-spread modeling matches what algotraders expect
- Translation help — Uzbek pages mostly fall back to Russian; framework is in place via mkdocs-static-i18n

The site loudly says "education, not financial advice" on every page because forex is genuinely high-risk (74-89% retail loss rate per ESMA). The goal is to make beginners less likely to blow up.

Project: https://mukhammadamir-akbarov.github.io/forex-toolkit/
Repo: https://github.com/MukhammadAmir-Akbarov/forex-toolkit
```

---

## 4️⃣ Reddit — r/Python

**Title**:
```
Built a forex educational toolkit in Python — 30+ CLI tools, backtester, mkdocs site (MIT, looking for code review)
```

**Body**:
```
Hi r/Python,

I built `forex-toolkit` — a Python-heavy open-source project. Posting because I'd love code-level feedback from the community.

**Tech highlights**:
- 74/74 unit tests passing on CI matrix (Ubuntu + macOS × Python 3.10/3.11/3.12)
- Strict typing in new modules, pep8 throughout
- Docstrings with examples, RST-compatible
- pyproject.toml-driven setup with hatchling, optional extras (`dev`, `docs`, `web`, `mt5`, `crypto`)
- mkdocs-material site auto-deployed via GitHub Actions (multilingual via mkdocs-static-i18n)
- Reportlab PDF generation with embedded DejaVu fonts (Cyrillic support fix)
- Streamlit app, Telegram bot, MT5 Expert Advisor — all in one repo

**Project structure**:
```
tools/         — 30+ CLI utilities (position calc, journal, Monte Carlo, ...)
strategies/    — 6 trading strategies with unit tests
bot/           — backtester with anti-tilt Risk Guardian
advanced/      — Streamlit/Telegram/MT5 integrations
_mkdocs/       — mkdocs source (RU/EN/UZ)
```

**Things I'm proud of**:
- Pure-stdlib position calculator (no external deps for the most critical math)
- JS port of the Python calculators with identical formula — runs in the browser via mkdocs page
- Risk Guardian dataclass that injects into backtest loop without changing existing test signatures (backwards-compatible)

**What I'd like feedback on**:
- Code style: am I overusing `@dataclass`?
- Test coverage gaps: the live-rate fetcher in position_calculator has no tests because it hits network. Mock or skip?
- Project layout: `bot/strategy.py` is imported by both `bot/backtest.py` and tests via `sys.path` mutation in conftest. Cleaner alternative?

Repo: https://github.com/MukhammadAmir-Akbarov/forex-toolkit
Site: https://mukhammadamir-akbarov.github.io/forex-toolkit/
PRs welcome.
```

---

## 5️⃣ Узбекские Telegram-каналы (на русском)

Найди подходящие через поиск Telegram: «forex Узбекистан», «трейдинг Ташкент», «forex Россия». Не спамь — пиши в каналы с дискуссионным чатом.

**Текст**:
```
Привет 👋

Сделал бесплатный open-source проект по форексу — учебник + Python-инструменты + интерактивные калькуляторы. Без подписок, без сигналов, без рекламы брокеров.

📖 Что внутри:
• Полный учебник на 3 языках (RU/EN/узбекский в разработке)
• Калькулятор размера позиции с актуальными курсами ECB
• Калькулятор сложного процента с предупреждениями про обещания «50% в месяц» (это скам)
• Бэктестер с anti-tilt защитой (стоп после 3 убытков подряд)
• Журнал сделок CLI + HTML дашборд
• 6 стратегий с unit-тестами
• Раздел для трейдеров из Узбекистана (брокеры, вывод денег, налоги)

🎯 Образовательный материал. НЕ финансовый совет. 74-89% розничных трейдеров теряют деньги — это статистика ESMA, проект говорит это на каждой странице.

🔗 Сайт: https://mukhammadamir-akbarov.github.io/forex-toolkit/
🔗 Калькулятор: https://mukhammadamir-akbarov.github.io/forex-toolkit/tools/position-calculator/
🔗 GitHub (звезда поможет распространению): https://github.com/MukhammadAmir-Akbarov/forex-toolkit

Если есть вопросы или нашли ошибку — лучше через [Discussions](https://github.com/MukhammadAmir-Akbarov/forex-toolkit/discussions), не в личку. Спасибо!
```

---

## 6️⃣ Twitter / X

3 поста в разные дни — не сразу.

**Пост 1 — анонс**:
```
Built an open-source forex education toolkit:

📖 Full handbook (RU/EN/UZ)
📐 Live position calculator
🤖 Backtester w/ anti-tilt Risk Guardian
🔧 30+ Python tools
✅ 74/74 unit tests, MIT licensed

🚫 No signals. No shilling. No "guru" courses.

https://mukhammadamir-akbarov.github.io/forex-toolkit/
```

**Пост 2 — фича**:
```
Most "5% per month" forex promises are scams.

My compound calculator shows why: that's 79.6%/year. Best hedge funds do 20-30%.

Built it to help beginners spot the math:

https://mukhammadamir-akbarov.github.io/forex-toolkit/tools/compound-calculator/

#forex #trading #opensource
```

**Пост 3 — техническое (для Python-аудитории)**:
```
Cool thing in my forex backtester: anti-tilt Risk Guardian.

After N consecutive losses OR hitting daily loss limit, it BLOCKS new trades.

Backtests now simulate disciplined traders, not idealized infinite-account scenarios.

Python, MIT:
https://github.com/MukhammadAmir-Akbarov/forex-toolkit

#Python #algotrading
```

---

## 7️⃣ Dev.to (статья на 500-1000 слов)

**Title**:
```
What I learned building an open-source forex toolkit with Python and mkdocs
```

**Skeleton**:
1. Why I built it (1-2 paragraphs about the bad state of free forex education)
2. Architecture (Python tools + mkdocs site + interactive JS calculators + CI/CD)
3. Two interesting technical problems I solved:
   - Cyrillic in reportlab PDF (font tofu → DejaVu Sans embedding)
   - Live position calculator without backend (frankfurter.app + JS)
4. Multi-language via mkdocs-static-i18n (RU/EN/UZ)
5. The non-obvious design: anti-tilt Risk Guardian in the backtester
6. Lessons + links

Drives traffic from Python and tech audience.

---

## 📊 Что измерять после запуска

| Метрика | Где смотреть | Цель за неделю |
|---|---|---|
| ⭐ Stars на GitHub | Repo header | ≥ 10 |
| 👁️ Уникальные посетители сайта | Insights → Traffic | ≥ 100 |
| 💬 Новые Discussions | discussions/categories/q-a | ≥ 2 |
| 🐛 Issues | issues | ≥ 1 (любой) |
| 📥 Release downloads | Insights → Traffic → "Most downloaded" | ≥ 20 PDF |
| 🔍 Clone count | Insights → Traffic | ≥ 5 |

**Если за неделю всё по нулям** — пост не достиг аудитории. Меняй платформу или подачу. Не добавляй фичи — ищи фидбек.

**Если есть хоть один реальный отзыв** — это **в 1000 раз ценнее** любой новой функции. Дай человеку ответ, попроси конкретное предложение, реализуй за 1 день.

---

## ❌ Чего НЕ делать

- ❌ Кросс-постить идентичный текст за минуту во все Reddit'ы — забанят
- ❌ Спамить в личку трейдерам в Telegram
- ❌ Покупать звёзды на GitHub (детектируется, бан репо)
- ❌ Обещать прибыль в постах — это против правил почти всех платформ
- ❌ Создавать accounts только для upvote своего поста — забанят

---

**Удачи! Один реальный пользователь > 10 новых фич.** 🚀
