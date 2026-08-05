# Forex Trading — полный учебный проект

[![Tests](https://github.com/MukhammadAmir-Akbarov/forex-toolkit/actions/workflows/test.yml/badge.svg)](https://github.com/MukhammadAmir-Akbarov/forex-toolkit/actions/workflows/test.yml)
[![Deploy Docs](https://github.com/MukhammadAmir-Akbarov/forex-toolkit/actions/workflows/deploy-docs.yml/badge.svg)](https://github.com/MukhammadAmir-Akbarov/forex-toolkit/actions/workflows/deploy-docs.yml)
[![Docs](https://img.shields.io/badge/docs-mkdocs-blue)](https://mukhammadamir-akbarov.github.io/forex-toolkit/)
[![License: code MIT](https://img.shields.io/badge/code-MIT-green)](LICENSE)
[![License: content CC BY 4.0](https://img.shields.io/badge/content-CC%20BY%204.0-lightgrey)](LICENSE-CONTENT.md)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)

> Самодостаточный набор материалов: **80 страниц на RU + EN + UZ**, 20+ учебных графиков, 25+ Python-инструментов, 15+ браузерных инструментов, offline PWA, 6 стратегий, MT5 EA, Telegram-бот, Coach-бот, Streamlit-приложение, Word-документ и PDF-учебник.
>
> **⚠️ Образовательный материал. Не финансовый совет.** Forex — высокорисковая деятельность. 74–89% розничных трейдеров теряют деньги.

**📥 Скачать готовые материалы:**
- 📕 [PDF-учебник](https://github.com/MukhammadAmir-Akbarov/forex-toolkit/releases/latest/download/forex-handbook.pdf) (1.1 MB) — для печати
- 📄 [Word-версия](https://github.com/MukhammadAmir-Akbarov/forex-toolkit/releases/latest/download/forex-guide-rus.docx) (962 KB)
- 🌐 [Онлайн-сайт](https://mukhammadamir-akbarov.github.io/forex-toolkit/) — учебник в браузере с поиском и тёмной темой

## 🗂️ Полная структура

```
trading/
├── forex_toolkit/                 ← Python-пакет (публикуемый на PyPI)
│   ├── fx_math.py                 ← ЕДИНЫЙ источник формул (pip-value, calc_lots)
│   ├── indicators.py              ← EMA, SMA, RSI, ATR, Bollinger, MACD
│   ├── candles.py                 ← свечные паттерны (молот, доджи, поглощение)
│   ├── position_calculator.py     ← размер позиции по риск-менеджменту
│   └── cli.py                     ← 8 CLI-команд (forex-position, …)
│
├── _mkdocs/                       ← ★ ЕДИНСТВЕННЫЙ источник контента сайта
│   │                                 (RU/EN/UZ → GitHub Pages, docs_dir)
│   ├── forex-guide.md             ← главный учебник
│   ├── roadmap.md                 ← дорожная карта обучения
│   ├── docs/                      ← теханализ, стратегия, реальный анализ
│   ├── extras/                    ← глоссарий, FAQ, психология, шаблоны, чек-листы
│   ├── practice/                  ← «из практики»: золото, лот, BE, доливка, циклы
│   ├── journal/                   ← шаблоны журнала сделок
│   ├── tools/                     ← браузерные виджеты-калькуляторы (без Python)
│   ├── growth/                    ← после года: order flow, crypto, stocks
│   ├── uz/                        ← брокеры / вывод денег / сообщества (Узбекистан)
│   ├── advanced/                  ← SETUP-инструкции (MT5, Streamlit, Telegram, VPS)
│   └── stylesheets/, javascripts/ ← оформление и JS
│
├── tools/                         ← Python-утилиты (исходники)
│   ├── position_calculator.py · pip_calculator.py · compound_calculator.py
│   ├── monte_carlo.py · news_scraper.py · pattern_scanner.py · risk_profile.py
│   ├── journal_cli.py · journal_dashboard.py · chart_generator*.py
│   └── build_pdf.py · build_docx.py · check_docs_sync.py
│
├── bot/                           ← бэктестер: strategy.py, backtest.py
├── strategies/                    ← учебные стратегии + сравнительный бэктест
├── advanced/                      ← MT5, Telegram, Streamlit, walk-forward, broker_api/
├── uz/                            ← tax-calculator.py (локальные скрипты)
├── tests/                         ← 156 unit-тестов + 32 браузерных e2e
├── dist/                          ← собранный wheel
├── mkdocs.yml · pyproject.toml · CLAUDE.md
├── data/                          ← скачанные котировки (gitignored)
└── .venv/                         ← Python-окружение (gitignored)
```

> **Источник правды для контента — только `_mkdocs/`.** Корневых дублей `.md`
> (`docs/`, `extras/`, `journal/`…) больше нет — они удалены, чтобы материал не
> расходился. PDF/DOCX собираются из `_mkdocs/`. Переводы лежат рядом с RU-страницей
> как `page.en.md` и `page.uz.md` (суффиксный режим `mkdocs-static-i18n`).

## 🚀 Быстрый старт

### Если хочешь читать (минимум)

1. Открой [КАК-ПОЛЬЗОВАТЬСЯ.md](_mkdocs/КАК-ПОЛЬЗОВАТЬСЯ.md) — экскурсия по проекту
2. [forex-guide.md](_mkdocs/forex-guide.md) — главный учебник
3. [docs/technical-analysis.md](_mkdocs/docs/technical-analysis.md) — теханализ с картинками
4. [extras/psychology.md](_mkdocs/extras/psychology.md) — психология

### Если хочешь использовать инструменты

```bash
# Калькулятор позиции — ПЕРЕД каждой сделкой
.venv/bin/python tools/position_calculator.py --balance 1000 --risk 0.5 --stop 25 --pair EURUSD

# Журнал через CLI
.venv/bin/python tools/journal_cli.py add --pair EURUSD --dir long \
  --entry 1.0852 --sl 1.0827 --tp 1.0902 --lot 0.02 --risk 5 --rules yes

# Дашборд журнала (открыть HTML в браузере)
.venv/bin/python tools/journal_dashboard.py

# Бэктест на синтетике
.venv/bin/python bot/backtest.py

# Бэктест на РЕАЛЬНОЙ истории EUR/USD
.venv/bin/python advanced/data_downloader.py --symbol EURUSD --interval 1h --years 2
.venv/bin/python bot/backtest.py --csv data/EURUSD_1h.csv

# Сравнение всех 5 стратегий
.venv/bin/python strategies/compare.py

# Монте-Карло (10 000 симуляций стратегии)
.venv/bin/python tools/monte_carlo.py --simulations 10000 --winrate 0.5 --rr 2

# Walk-forward optimization
.venv/bin/python advanced/walk_forward.py

# Календарь новостей Forex Factory
.venv/bin/python tools/news_scraper.py --high-only

# Streamlit интерактивный дашборд
pip install streamlit
streamlit run advanced/streamlit_app.py
```

## 📚 Что есть в проекте

### Учебники
- ✅ Главный гайд (700 строк, 14 разделов)
- ✅ Технический анализ с 12 графиками
- ✅ Детальная стратегия
- ✅ Психология трейдинга
- ✅ Глоссарий 200+ терминов
- ✅ FAQ 30 вопросов
- ✅ Сравнение 12 брокеров
- ✅ Печатный чек-лист
- ✅ Mind map проекта
- ✅ Anki-карточки для запоминания

### Инструменты
- ✅ Калькулятор позиции
- ✅ Калькулятор пипса
- ✅ Калькулятор маржи
- ✅ Калькулятор сложного процента
- ✅ Risk exposure tracker (с корреляциями)
- ✅ Multi-position sizer
- ✅ Монте-Карло симулятор
- ✅ News scraper (Forex Factory)
- ✅ Pattern scanner (8 паттернов)
- ✅ Trading journal CLI
- ✅ HTML дашборд журнала
- ✅ Месячный отчёт-генератор

### Стратегии
- ✅ EMA50 pullback (trend-following)
- ✅ Mean Reversion (Bollinger)
- ✅ Breakout
- ✅ London Open Range
- ✅ Three Soldiers / Crows
- ✅ Carry trade (теория)
- ✅ Сравнительный бэктест всех

### Продвинутое
- ✅ MetaTrader 5 Expert Advisor (MQL5)
- ✅ Python ↔ MT5 коннектор (Windows)
- ✅ Telegram-бот алертов
- ✅ Streamlit веб-приложение
- ✅ Скачивание реальной истории (yfinance)
- ✅ Walk-forward optimization
- ✅ Word-документ (.docx) учебника

### Для Узбекистана
- ✅ Налоговый калькулятор
- ✅ Гид по выводу денег
- ✅ Локальные ресурсы и сообщества

## 🛠️ Установка с нуля

Проект — устанавливаемый пакет, зависимости описаны в `pyproject.toml`:

```bash
python3 -m venv .venv
.venv/bin/pip install -e ".[dev]"     # ядро + тесты/линт/mkdocs
.venv/bin/pytest -q                    # должны пройти все 156 unit-тестов
```

Опциональные группы зависимостей (extras):
```bash
.venv/bin/pip install -e ".[docs]"     # сборка PDF/DOCX (reportlab, python-docx)
.venv/bin/pip install -e ".[web]"      # Streamlit-приложение (streamlit, plotly)
.venv/bin/pip install -e ".[all]"      # всё сразу
```

Для Telegram-бота (опционально):
```bash
# (requests уже установлен)
export TELEGRAM_BOT_TOKEN="your_token"
export TELEGRAM_CHAT_ID="your_chat_id"
```

## 📋 Дорожная карта обучения

| Месяц | Действия |
|---|---|
| **1** | Читать главный гайд, теханализ, психологию. Открыть демо-счёт. |
| **2** | Стратегия 1 (EMA50). 30 сделок на демо с журналом. |
| **3** | Анализ через journal_dashboard. Доработка. Ещё 30 сделок. |
| **4** | Прочесть сравнение стратегий, выбрать вторую. Тестировать. |
| **5** | При стабильном плюсе → реал $100-300, микро-лоты, 0.5% риск. |
| **6+** | Только дисциплина. Никакого увеличения риска. |

## ⚠️ Главные правила

1. Никогда не торгуй деньгами, которые тебе нужны
2. Минимум 3 месяца демо перед реалом
3. Всегда ставь стоп-лосс
4. Риск ≤ 1% на сделку (новичку 0.5%)
5. Веди журнал каждой сделки
6. Не верь обещаниям лёгких денег

## 📄 Лицензия

Проект под **двумя лицензиями**: **код** (`forex_toolkit/`, `tools/`, `bot/`,
`advanced/`) — [MIT](LICENSE); **учебный контент** (`_mkdocs/`, PDF/DOCX) —
[CC BY 4.0](LICENSE-CONTENT.md). То есть материалы можно свободно переводить
(в т. ч. на узбекский) и переиспользовать **с указанием авторства**.
Подробности — в [LICENSE-CONTENT.md](LICENSE-CONTENT.md).

## 📜 Дисклеймер

Все материалы — образовательные. Автор не лицензированный финансовый советник. Решения о торговле принимаешь только ты и под свою ответственность. Прежде чем торговать реальными деньгами — консультируйся с независимым специалистом.

---

📖 **Начни с** → [КАК-ПОЛЬЗОВАТЬСЯ.md](_mkdocs/КАК-ПОЛЬЗОВАТЬСЯ.md)
