# Telegram Bot Setup Guide — receive signals in Telegram

## What this gives you

Every hour (or on a schedule) the script:
1. Downloads EUR/USD candles (yfinance)
2. Applies our strategy
3. If there is a fresh signal — sends you a message in Telegram

Example message:
```
🚨 Forex Signal

Pair: EURUSD
Direction: 🟢 LONG
Time: 2026-05-20 14:00

Entry: 1.08520
Stop Loss: 1.08270 (25 pips)
Take Profit: 1.09020 (R:R 1:2.0)

Reason: BullEng

⚠️ This is not a trading recommendation. Check your checklist before entering.
```

## Step 1: Create a Telegram bot

1. Open Telegram and find the contact **@BotFather**
2. Send `/newbot`
3. BotFather will ask for a **bot name** — for example: "Forex Signals My Bot"
4. Then it will ask for a **username** — must end in `bot`, for example: `forex_signals_amir_bot`
5. You will receive a message containing your **token**:
   ```
   123456789:ABCdefGHIjklMNOpqrSTUvwxYZ
   ```
   **This is your `TELEGRAM_BOT_TOKEN`. Never share it with anyone.**

## Step 2: Get your chat_id

This is your personal ID so the bot knows who to write to.

### Method 1 (easier)

1. In Telegram find **@userinfobot**
2. Send `/start`
3. You will get a message with your **ID**, for example:
   ```
   👤 Id: 123456789
   First name: Amir
   ```

   This is your `TELEGRAM_CHAT_ID`.

### Method 2 (via API)

1. Send **any message** to your newly created bot in Telegram (any text, for example "hello")
2. Open in your browser:
   ```
   https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates
   ```
   (replace `<YOUR_TOKEN>` with the token from Step 1)
3. In the JSON response find `"chat":{"id":123456789,...}` — that is your chat_id

## Step 3: Set environment variables

Open a terminal in the project directory:

```bash
cd /Users/mukhammadamir/Sites/WORK/trading

# Replace with your own values
export TELEGRAM_BOT_TOKEN="123456789:ABCdef..."
export TELEGRAM_CHAT_ID="123456789"
```

To persist the variables across sessions — add them to `~/.zshrc`:

```bash
echo 'export TELEGRAM_BOT_TOKEN="123456789:ABCdef..."' >> ~/.zshrc
echo 'export TELEGRAM_CHAT_ID="123456789"' >> ~/.zshrc
source ~/.zshrc
```

## Step 4: Test run

First — a **dry-run** (without sending to Telegram):

```bash
.venv/bin/python advanced/telegram_alerts.py --symbol EURUSD --dry-run
```

You will see in the terminal which signals **would have been** sent.

If it looks good — run with actual sending:

```bash
.venv/bin/python advanced/telegram_alerts.py --symbol EURUSD
```

Open Telegram → a signal should arrive (if one exists in the recent hours).

## Step 5: Automatic run every hour

### Option A: cron (macOS / Linux)

```bash
crontab -e
```

Add this line:
```cron
0 * * * * cd /Users/mukhammadamir/Sites/WORK/trading && /Users/mukhammadamir/Sites/WORK/trading/.venv/bin/python advanced/telegram_alerts.py >> /tmp/telegram_alerts.log 2>&1
```

This line runs the script **at the start of every hour**. Logs are saved to `/tmp/telegram_alerts.log`.

⚠️ cron has no environment variables! Add them directly in the command:
```cron
0 * * * * cd /Users/mukhammadamir/Sites/WORK/trading && TELEGRAM_BOT_TOKEN="123..." TELEGRAM_CHAT_ID="123..." /Users/mukhammadamir/Sites/WORK/trading/.venv/bin/python advanced/telegram_alerts.py >> /tmp/telegram_alerts.log 2>&1
```

Or use a `.env` file (see below).

### Option B: launchd (macOS, the more robust approach)

Create the file `~/Library/LaunchAgents/com.amir.forex-alerts.plist`:

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

Load it:
```bash
launchctl load ~/Library/LaunchAgents/com.amir.forex-alerts.plist
```

It will run every hour at minute 5.

Stop it:
```bash
launchctl unload ~/Library/LaunchAgents/com.amir.forex-alerts.plist
```

### Option C: cloud server (for always-on operation)

You can deploy on:
- **Heroku** (free plan — 550 hours/month)
- **PythonAnywhere** (free, simple cron setup)
- **Render** (free plan)
- **Container on a VPS** (if you have one)

We won't go deeper here — get the local setup working first.

## Step 6: Store the token securely

**⚠️ Never push the token to Git!**

Create a `.env` file in the project root:

```bash
TELEGRAM_BOT_TOKEN=123456789:ABCdef...
TELEGRAM_CHAT_ID=123456789
```

`.env` is already in `.gitignore`.

Load it via [python-dotenv](https://pypi.org/project/python-dotenv/):

```bash
.venv/bin/pip install python-dotenv
```

Add to the top of `telegram_alerts.py` (optional):
```python
from dotenv import load_dotenv
load_dotenv()
```

## Step 7: Extend the functionality

You can extend the bot:

### Multiple pairs
```bash
for pair in EURUSD GBPUSD USDJPY; do
  .venv/bin/python advanced/telegram_alerts.py --symbol $pair
done
```

### Bot commands (two-way interaction)
Allow yourself to message the bot:
- `/status` → current open signal
- `/stats` → statistics of recent signals
- `/disable EURUSD` → disable a pair

This requires the `python-telegram-bot` library:
```bash
.venv/bin/pip install python-telegram-bot
```

### Signal group with friends
1. Create a group in Telegram
2. Add your bot to the group
3. Make the bot an **admin** (via @BotFather)
4. Get the group chat_id (also via `/getUpdates`, the JSON will contain a negative ID)
5. Use that ID as `TELEGRAM_CHAT_ID`

## Step 8: What to do with signals

The bot sends a signal — **that is not a command** to trade. It is a **notification** that our script found a setup.

Before opening a trade:
1. ✅ Open MT5 → verify that the setup is actually there (the bot can be wrong)
2. ✅ Go through the [printable checklist](../extras/checklist-printable.md)
3. ✅ Run [position_calculator.py](https://github.com/MukhammadAmir-Akbarov/forex-toolkit/blob/main/tools/position_calculator.py)
4. ✅ Write the planned parameters in your journal BEFORE opening
5. ✅ Open the trade with SL and TP

**Never open a trade immediately on a signal without verification.**

## Troubleshooting

### Bot does not respond to /start
- Possibly an incorrect token
- Check that the bot is not blocked

### Messages are not arriving
- Check the chat_id — it must be **your** ID, not a username
- Run with `--dry-run` — you will see whether signals are being generated at all

### yfinance crashes
- yfinance sometimes throttles frequent requests → wait 10 minutes
- Possibly no internet connection

### Signals seem "stale"
- yfinance delivers quotes with a 15–30 minute delay
- For real-time trading you need a broker API or a paid data feed

---

## Final reminder

🚨 **The Telegram bot is just notifications.** No automatic orders. You make the decision on every trade yourself. The bot speeds up the process of **finding** setups, but it does not replace your analysis and discipline.

---

[← Back to the main guide](../forex-guide.md)
