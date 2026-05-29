# Forex Trading Toolkit

<div style="text-align: center; font-size: 1.5em; color: #1e40af;">
  📈 <strong>Полный учебный проект для изучения forex с нуля</strong>
</div>

<div style="text-align: center; margin: 1em 0; color: #6b7280;">
  130+ файлов · 25+ учебных гайдов · 30+ Python-инструментов · 6 стратегий · MT5/Telegram/Streamlit боты · 95 unit-тестов · 5 браузерных виджетов
</div>

<p align="center" markdown="1">
[![Tests](https://github.com/MukhammadAmir-Akbarov/forex-toolkit/actions/workflows/test.yml/badge.svg)](https://github.com/MukhammadAmir-Akbarov/forex-toolkit/actions/workflows/test.yml)
[![Deploy](https://github.com/MukhammadAmir-Akbarov/forex-toolkit/actions/workflows/deploy-docs.yml/badge.svg)](https://github.com/MukhammadAmir-Akbarov/forex-toolkit/actions/workflows/deploy-docs.yml)
[![License](https://img.shields.io/badge/license-MIT-green)](https://github.com/MukhammadAmir-Akbarov/forex-toolkit/blob/main/LICENSE)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)
[![GitHub](https://img.shields.io/badge/github-source-black?logo=github)](https://github.com/MukhammadAmir-Akbarov/forex-toolkit)
</p>

## 📥 Скачать готовые материалы

<div class="grid cards" markdown>

-   📕 **PDF-учебник** (1.1 MB)

    ---

    Полный учебник в PDF для печати и офлайн-чтения.

    [📥 Скачать PDF](https://github.com/MukhammadAmir-Akbarov/forex-toolkit/releases/latest/download/forex-handbook.pdf){ .md-button .md-button--primary }

-   📄 **Word-версия** (962 KB)

    ---

    Тот же учебник в редактируемом формате `.docx`.

    [📥 Скачать DOCX](https://github.com/MukhammadAmir-Akbarov/forex-toolkit/releases/latest/download/forex-guide-rus.docx){ .md-button }

-   🛠️ **Исходный код**

    ---

    Полный репозиторий: Python-инструменты, стратегии, тесты, боты.

    [⭐ GitHub](https://github.com/MukhammadAmir-Akbarov/forex-toolkit){ .md-button }

</div>

!!! warning "⚠️ ВАЖНОЕ ПРЕДУПРЕЖДЕНИЕ"
    Этот документ — **образовательный материал**, не финансовый совет.
    Forex — высокорисковая деятельность. По данным ESMA, **74–89%** розничных
    трейдеров теряют деньги. Никогда не торгуй на деньги, которые не готов потерять.

## 🚀 С чего начать

1. **[Как пользоваться](КАК-ПОЛЬЗОВАТЬСЯ.md)** — экскурсия по проекту
2. **[Главный учебник](forex-guide.md)** — 700 строк теории
3. **[Психология трейдинга](extras/psychology.md)** — главный навык

## 🎯 Рекомендуемый путь

```mermaid
graph TD
    A[Прочитал что такое forex] --> B[Прошёл risk_profile.py]
    B --> C{Результат?}
    C -->|< 50%| D[Stocks/ETF лучше]
    C -->|> 60%| E[Заполнил Trading Plan]
    E --> F[Открыл демо-счёт]
    F --> G[First 100 Days]
    G --> H[30+ сделок с журналом]
    H --> I{Стабильный плюс?}
    I -->|Да| J[Маленький реал-депозит]
    I -->|Нет| K[Ещё 3 месяца демо]
```

## 📊 Что внутри

### Учебники (RU + EN)
- Главный гайд (RU 638, EN 638 строк)
- Технический анализ с 20+ графиками
- Подробный разбор стратегии
- Глоссарий 200+ терминов
- 30 FAQ

### Инструменты
- Калькуляторы (позиции, маржи, сложного процента, пипса)
- Бэктестер с реальными данными по 8 парам
- Pattern scanner (8 свечных паттернов)
- Trading Journal CLI + HTML dashboard
- Monte Carlo симулятор
- Risk profile тест (30 вопросов)
- Broker license checker

### Боты
- MT5 Expert Advisor (MQL5)
- Telegram signals bot
- Daily Coach bot
- Streamlit веб-приложение

### Стратегии (с unit-тестами)
- EMA50 Pullback (trend-following)
- Mean Reversion (Bollinger)
- Breakout (с фильтрами в v2)
- London Open Range
- Three Soldiers / Crows
- Carry Trade (теория)

## 🧪 Качество кода

- **74/74** unit-теста проходят на каждом push (CI matrix: Ubuntu/macOS × Python 3.10-3.12)
- Тестировано на **8 валютных парах × 2 года** реальных данных
- Walk-forward optimization для проверки робастности
- Coverage отчёт встроен
- **Risk Guardian** (anti-tilt): автоматический стоп торговли после N убытков подряд + дневной лимит потерь
- **Live-цены** в калькуляторе позиции через yfinance — никаких устаревших табличных значений

## 📜 Дисклеймер

Все материалы — образовательные. Автор не лицензированный финансовый советник. Решения о торговле принимаешь ты, под свою ответственность.
