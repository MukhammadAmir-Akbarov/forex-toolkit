# Forex Trading — полный учебный проект

[![Tests](https://github.com/MukhammadAmir-Akbarov/forex-toolkit/actions/workflows/test.yml/badge.svg)](https://github.com/MukhammadAmir-Akbarov/forex-toolkit/actions/workflows/test.yml)
[![Deploy Docs](https://github.com/MukhammadAmir-Akbarov/forex-toolkit/actions/workflows/deploy-docs.yml/badge.svg)](https://github.com/MukhammadAmir-Akbarov/forex-toolkit/actions/workflows/deploy-docs.yml)
[![Docs](https://img.shields.io/badge/docs-mkdocs-blue)](https://mukhammadamir-akbarov.github.io/forex-toolkit/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)

> Самодостаточный набор материалов: **80+ файлов**, 25 markdown-гайдов, 20+ учебных графиков, 25+ Python-инструментов, 6 стратегий, MT5 EA, Telegram-бот, Coach-бот, Streamlit-приложение, Word-документ и PDF-учебник.
>
> **⚠️ Образовательный материал. Не финансовый совет.** Forex — высокорисковая деятельность. 74–89% розничных трейдеров теряют деньги.

**📥 Скачать готовые материалы:**
- 📕 [PDF-учебник](https://github.com/MukhammadAmir-Akbarov/forex-toolkit/releases/latest/download/forex-handbook.pdf) (1.1 MB) — для печати
- 📄 [Word-версия](https://github.com/MukhammadAmir-Akbarov/forex-toolkit/releases/latest/download/forex-guide-rus.docx) (962 KB)
- 🌐 [Онлайн-сайт](https://mukhammadamir-akbarov.github.io/forex-toolkit/) — учебник в браузере с поиском и тёмной темой

## 🗂️ Полная структура

```
trading/
├── 📖 КАК-ПОЛЬЗОВАТЬСЯ.md             ← начать ОТСЮДА
├── 📖 README.md                       ← эта страница
├── 📖 forex-guide.md                  ← главный учебник (700 строк)
├── 📄 forex-guide-полный.docx         ← Word-версия (распространяется через GitHub Releases)
│
├── 📚 docs/                           ← углублённые материалы
│   ├── technical-analysis.md          ← теханализ с 12 графиками
│   ├── strategy-details.md            ← разбор стратегии
│   └── images/                        ← 18 учебных графиков (PNG)
│
├── 📚 extras/                         ← дополнения
│   ├── glossary.md                    ← словарь 200+ терминов
│   ├── checklist-printable.md         ← печатный чек-лист
│   ├── faq.md                         ← 30 типичных вопросов
│   ├── anki-cards.csv                 ← карточки для Anki
│   ├── mind-map.md                    ← карта концепций
│   ├── psychology.md                  ← психология трейдинга
│   └── brokers-comparison.md          ← сравнение 12 брокеров
│
├── 📝 journal/                        ← журнал сделок
│   ├── trading-journal-template.md    ← базовый шаблон (Markdown)
│   ├── trading-journal-template.csv   ← шаблон для Google Sheets
│   ├── journal-extended.md            ← расширенный с psychology
│   ├── mistakes-log.md                ← журнал ошибок
│   ├── demo-vs-real-comparison.md     ← переход с демо на реал
│   └── monthly_report.py              ← генератор месячного HTML-отчёта
│
├── 🛠️ tools/                          ← Python-инструменты
│   ├── position_calculator.py         ← размер позиции
│   ├── pip_calculator.py              ← стоимость пипса
│   ├── compound_calculator.py         ← сложный процент
│   ├── margin_calculator.py           ← калькулятор маржи
│   ├── multi_position_sizer.py        ← несколько сделок
│   ├── risk_exposure.py               ← общий риск с корреляциями
│   ├── monte_carlo.py                 ← Монте-Карло симулятор
│   ├── news_scraper.py                ← календарь Forex Factory
│   ├── pattern_scanner.py             ← поиск свечных паттернов
│   ├── journal_cli.py                 ← CLI для журнала
│   ├── journal_dashboard.py           ← HTML-дашборд
│   ├── chart_generator.py             ← базовые графики
│   ├── chart_generator_extra.py       ← дополнительные графики
│   └── build_docx.py                  ← сборка Word-документа
│
├── 📊 strategies/                     ← 5 учебных стратегий
│   ├── common.py                      ← общие индикаторы
│   ├── mean_reversion.py              ← возврат к среднему (BB)
│   ├── breakout.py                    ← пробой N-периодных high/low
│   ├── london_open.py                 ← пробой лондонского открытия
│   ├── three_soldiers.py              ← 3 свечи подряд
│   ├── carry_trade.md                 ← (только описание)
│   └── compare.py                     ← сравнительный бэктест
│
├── 🤖 bot/                            ← основной бэктестер
│   ├── strategy.py                    ← EMA50 pullback логика
│   └── backtest.py                    ← симулятор + статистика
│
├── 🚀 advanced/                       ← продвинутые инструменты
│   ├── EMA50Pullback.mq5              ← Expert Advisor для MT5
│   ├── mt5_connector.py               ← Python ↔ MT5 (Windows)
│   ├── telegram_alerts.py             ← Telegram-бот сигналов
│   ├── streamlit_app.py               ← веб-приложение бэктеста
│   ├── data_downloader.py             ← скачивание реальной истории
│   └── walk_forward.py                ← walk-forward оптимизация
│
├── 🇺🇿 uz/                            ← локально для Узбекистана
│   ├── tax-calculator.py              ← НДФЛ калькулятор
│   ├── withdrawal-guide.md            ← вывод денег в РУз
│   └── communities.md                 ← сообщества и ресурсы
│
├── 🌱 growth/                         ← продвинутые темы (после года)
│   ├── order-flow-volume-profile.md   ← Volume Profile, ICT концепции
│   ├── crypto-trading-guide.md        ← параллельный мир крипто
│   └── stocks-basics.md               ← ETF, долгосрочное инвестирование
│
├── 📄 forex-guide-полный.docx         ← Word-документ (см. GitHub Releases)
├── 📕 forex-handbook.pdf              ← PDF-учебник (см. GitHub Releases)
│
├── data/                              ← скачанные котировки (gitignored)
└── .venv/                             ← Python окружение

# Расширения после первых 100 дней:
extras/
├── trading-plan-template.md           ← контракт с собой
├── first-100-days.md                  ← пошаговый план 100 дней
├── anti-tilt-protocol.md              ← экстренная процедура
├── daily-routine.md                   ← режим дня трейдера
├── emergency-card.md                  ← карточка кризисных контактов
└── video-scripts.md                   ← 10 видео-сценариев для самозаписи

tools/ (дополнительно):
├── broker_check.py                    ← проверка регулирования брокера
├── risk_profile.py                    ← 30-вопросный тест готовности
├── market_correlations.py             ← DXY, gold, SPY корреляции
├── journal_analyzer.py                ← AI-инсайты по журналу
├── build_pdf.py                       ← сборка PDF-учебника
└── quiz.py                            ← spaced repetition тренажёр

advanced/ (дополнительно):
├── SETUP-mt5.md                       ← установка и настройка MT5
├── SETUP-streamlit.md                 ← запуск Streamlit-приложения
├── SETUP-telegram.md                  ← Telegram-бот пошагово
├── SETUP-vps-deployment.md            ← запуск 24/7 на сервере
├── parameter_sweep.py                 ← подбор параметров стратегии
├── coach_bot.py                       ← ежедневный коуч в Telegram
└── broker_api/                        ← унифицированный broker-API
    ├── base.py                        ← интерфейс
    ├── yfinance_broker.py             ← Yahoo (data only)
    ├── mt5_broker.py                  ← MetaTrader 5
    ├── binance_broker.py              ← Binance (crypto)
    └── example.py                     ← пример использования

strategies/ (дополнительно):
└── breakout_v2.py                     ← Breakout с фильтрами
```

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

Если случайно удалил `.venv/`:

```bash
cd /Users/mukhammadamir/Sites/WORK/trading
python3 -m venv .venv
.venv/bin/pip install matplotlib numpy pandas python-docx jinja2 \
    yfinance requests beautifulsoup4 reportlab
```

Для Streamlit (опционально):
```bash
.venv/bin/pip install streamlit plotly
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

## 📜 Дисклеймер

Все материалы — образовательные. Автор не лицензированный финансовый советник. Решения о торговле принимаешь только ты и под свою ответственность. Прежде чем торговать реальными деньгами — консультируйся с независимым специалистом.

---

📖 **Начни с** → [КАК-ПОЛЬЗОВАТЬСЯ.md](_mkdocs/КАК-ПОЛЬЗОВАТЬСЯ.md)
