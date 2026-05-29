# Telegram Bot Setup Guide — получай сигналы в Telegram

## Что это даёт

Каждый час (или по расписанию) скрипт:
1. Скачивает свечи EUR/USD (yfinance)
2. Применяет нашу стратегию
3. Если есть свежий сигнал — присылает тебе сообщение в Telegram

Пример сообщения:
```
🚨 Forex Signal

Пара: EURUSD
Направление: 🟢 LONG
Время: 2026-05-20 14:00

Вход: 1.08520
Stop Loss: 1.08270 (25 пипсов)
Take Profit: 1.09020 (R:R 1:2.0)

Причина: BullEng

⚠️ Это не торговая рекомендация. Проверь чек-лист перед входом.
```

## Шаг 1: Создание Telegram-бота

1. Открой Telegram, найди контакт **@BotFather**
2. Напиши `/newbot`
3. BotFather попросит **имя бота** — например: «Forex Signals My Bot»
4. Затем попросит **username** — должен заканчиваться на `bot`, например: `forex_signals_amir_bot`
5. Получишь сообщение с **токеном**:
   ```
   123456789:ABCdefGHIjklMNOpqrSTUvwxYZ
   ```
   **Это твой `TELEGRAM_BOT_TOKEN`. Никому не показывай.**

## Шаг 2: Получение chat_id

Это твой персональный ID, чтобы бот знал, кому писать.

### Способ 1 (проще)

1. В Telegram найди **@userinfobot**
2. Напиши ему `/start`
3. Получишь сообщение с твоим **ID**, например:
   ```
   👤 Id: 123456789
   First name: Amir
   ```

   Это твой `TELEGRAM_CHAT_ID`.

### Способ 2 (через API)

1. Напиши **что-нибудь** созданному боту в Telegram (любое сообщение, например «привет»)
2. Открой в браузере:
   ```
   https://api.telegram.org/bot<TWOI_TOKEN>/getUpdates
   ```
   (вместо `<TWOI_TOKEN>` подставь токен из шага 1)
3. В JSON-ответе найди `"chat":{"id":123456789,...}` — это твой chat_id

## Шаг 3: Установка переменных окружения

Открой терминал в проекте:

```bash
cd /Users/mukhammadamir/Sites/WORK/trading

# Замени на свои значения
export TELEGRAM_BOT_TOKEN="123456789:ABCdef..."
export TELEGRAM_CHAT_ID="123456789"
```

Чтобы переменные сохранились между сессиями — добавь в `~/.zshrc`:

```bash
echo 'export TELEGRAM_BOT_TOKEN="123456789:ABCdef..."' >> ~/.zshrc
echo 'export TELEGRAM_CHAT_ID="123456789"' >> ~/.zshrc
source ~/.zshrc
```

## Шаг 4: Тестовый запуск

Сначала — **dry-run** (без отправки в Telegram):

```bash
.venv/bin/python advanced/telegram_alerts.py --symbol EURUSD --dry-run
```

Увидишь в терминале, какие сигналы **были бы** отправлены.

Если выглядит ок — запуск с отправкой:

```bash
.venv/bin/python advanced/telegram_alerts.py --symbol EURUSD
```

Открой Telegram → должен прийти сигнал (если он есть в последних часах).

## Шаг 5: Автоматический запуск каждый час

### Вариант А: cron (macOS / Linux)

```bash
crontab -e
```

Добавь строку:
```cron
0 * * * * cd /Users/mukhammadamir/Sites/WORK/trading && /Users/mukhammadamir/Sites/WORK/trading/.venv/bin/python advanced/telegram_alerts.py >> /tmp/telegram_alerts.log 2>&1
```

Эта строка запускает скрипт **в начале каждого часа**. Логи сохраняются в `/tmp/telegram_alerts.log`.

⚠️ В cron нет переменных окружения! Добавь их в команду:
```cron
0 * * * * cd /Users/mukhammadamir/Sites/WORK/trading && TELEGRAM_BOT_TOKEN="123..." TELEGRAM_CHAT_ID="123..." /Users/mukhammadamir/Sites/WORK/trading/.venv/bin/python advanced/telegram_alerts.py >> /tmp/telegram_alerts.log 2>&1
```

Или используй файл `.env` (см. ниже).

### Вариант Б: launchd (macOS, более правильный способ)

Создай файл `~/Library/LaunchAgents/com.amir.forex-alerts.plist`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
"http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key>
  <string>com.amir.forex-alerts</string>
  <key>ProgramArguments</key>
  <array>
    <string>/Users/mukhammadamir/Sites/WORK/trading/.venv/bin/python</string>
    <string>/Users/mukhammadamir/Sites/WORK/trading/advanced/telegram_alerts.py</string>
  </array>
  <key>EnvironmentVariables</key>
  <dict>
    <key>TELEGRAM_BOT_TOKEN</key>
    <string>123456789:ABCdef...</string>
    <key>TELEGRAM_CHAT_ID</key>
    <string>123456789</string>
  </dict>
  <key>StartCalendarInterval</key>
  <dict>
    <key>Minute</key>
    <integer>5</integer>
  </dict>
  <key>StandardOutPath</key>
  <string>/tmp/telegram_alerts.log</string>
  <key>StandardErrorPath</key>
  <string>/tmp/telegram_alerts.error.log</string>
</dict>
</plist>
```

Запусти:
```bash
launchctl load ~/Library/LaunchAgents/com.amir.forex-alerts.plist
```

Будет запускаться каждый час в 5 минут.

Остановить:
```bash
launchctl unload ~/Library/LaunchAgents/com.amir.forex-alerts.plist
```

### Вариант В: облачный сервер (для постоянной работы)

Можно развернуть на:
- **Heroku** (бесплатный план — 550 часов/месяц)
- **PythonAnywhere** (бесплатно, простая настройка cron)
- **Render** (бесплатный план)
- **Контейнер на VPS** (если есть)

Не буду углубляться — сначала разберись с локальным запуском.

## Шаг 6: Хранение токена безопасно

**⚠️ Никогда не пушь токен в Git!**

Создай файл `.env` в корне:

```bash
TELEGRAM_BOT_TOKEN=123456789:ABCdef...
TELEGRAM_CHAT_ID=123456789
```

`.env` уже в `.gitignore`.

Загружай через [python-dotenv](https://pypi.org/project/python-dotenv/):

```bash
.venv/bin/pip install python-dotenv
```

В начале `telegram_alerts.py` (можно добавить):
```python
from dotenv import load_dotenv
load_dotenv()
```

## Шаг 7: Расширение функциональности

Можно расширить бота:

### Несколько пар
```bash
for pair in EURUSD GBPUSD USDJPY; do
  .venv/bin/python advanced/telegram_alerts.py --symbol $pair
done
```

### Команды бота (двусторонняя связь)
Сделать так, чтобы ты мог писать боту:
- `/status` → текущий открытый сигнал
- `/stats` → статистика последних сигналов
- `/disable EURUSD` → выключить пару

Это требует библиотеки `python-telegram-bot`:
```bash
.venv/bin/pip install python-telegram-bot
```

### Группа сигналов с друзьями
1. Создай группу в Telegram
2. Добавь твоего бота в группу
3. Сделай бота **админом** (через @BotFather)
4. Получи group chat_id (тоже через `/getUpdates`, в JSON будет отрицательный ID)
5. Используй этот ID как `TELEGRAM_CHAT_ID`

## Шаг 8: Что делать с сигналами

Бот шлёт сигнал — **это не команда** торговать. Это **уведомление**, что наш скрипт нашёл сетап.

Перед открытием сделки:
1. ✅ Открой MT5 → проверь, действительно ли есть сетап (бот может ошибаться)
2. ✅ Пройди по [printable чек-листу](../extras/checklist-printable.md)
3. ✅ Запусти [position_calculator.py](https://github.com/MukhammadAmir-Akbarov/forex-toolkit/blob/main/tools/position_calculator.py)
4. ✅ Запиши планируемые параметры в журнал ДО открытия
5. ✅ Открой сделку с SL и TP

**Никогда не открывай сделку сразу по сигналу без проверки.**

## Troubleshooting

### Бот не отвечает на /start
- Возможно, неправильный токен
- Проверь, что бот не заблокирован

### Сообщения не приходят
- Проверь chat_id — должен быть **твой** ID, не username
- Запусти с `--dry-run` — увидишь, генерируются ли сигналы вообще

### yfinance падает
- yfinance иногда блокирует частые запросы → жди 10 минут
- Возможно, нет интернета

### Сигналы кажутся «не свежими»
- yfinance отдаёт котировки с задержкой 15-30 минут
- Для торговли в реальном времени нужен API брокера или платный data feed

---

## Финальное напоминание

🚨 **Telegram-бот — это просто уведомления.** Никаких автоматических ордеров. Ты сам принимаешь решение по каждой сделке. Бот ускоряет процесс **обнаружения** сетапов, но не заменяет твой анализ и дисциплину.

---

[← К главному гайду](../forex-guide.md)
