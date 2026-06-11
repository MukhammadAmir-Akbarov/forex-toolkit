# Telegram Bot sozlash bo'yicha qo'llanma — signallarni Telegramda oling

## Bu nima beradi

Har soatda (yoki jadval bo'yicha) skript:
1. EUR/USD shamlarini yuklab oladi (yfinance)
2. Bizning strategiyamizni qo'llaydi
3. Yangi signal bo'lsa — Telegramda xabar yuboradi

Xabar namunasi:
```
🚨 Forex Signal

Juft: EURUSD
Yo'nalish: 🟢 LONG
Vaqt: 2026-05-20 14:00

Kirish: 1.08520
Stop Loss: 1.08270 (25 pip)
Take Profit: 1.09020 (R:R 1:2.0)

Sabab: BullEng

⚠️ Bu savdo tavsiyasi emas. Kirishdan oldin chek-listni tekshiring.
```

## 1-qadam: Telegram-bot yaratish

1. Telegramni oching, **@BotFather** kontaktini toping
2. `/newbot` yozing
3. BotFather **bot nomi**ni so'raydi — masalan: «Forex Signals My Bot»
4. Keyin **username** so'raydi — `bot` bilan tugashi kerak, masalan: `forex_signals_amir_bot`
5. **Token** bilan xabar olasiz:
   ```
   123456789:ABCdefGHIjklMNOpqrSTUvwxYZ
   ```
   **Bu sizning `TELEGRAM_BOT_TOKEN`. Hech kimga ko'rsatmang.**

## 2-qadam: chat_id olish

Bu sizning shaxsiy ID'ingiz — bot kimga yozishini bilishi uchun kerak.

### 1-usul (osonroq)

1. Telegramda **@userinfobot** ni toping
2. `/start` yozing
3. Sizning **ID** bilan xabar keladi, masalan:
   ```
   👤 Id: 123456789
   First name: Amir
   ```

   Bu sizning `TELEGRAM_CHAT_ID`.

### 2-usul (API orqali)

1. Yaratilgan botga Telegramda **biror narsa** yozing (istalgan xabar, masalan «salom»)
2. Brauzerda oching:
   ```
   https://api.telegram.org/bot<TWOI_TOKEN>/getUpdates
   ```
   (`<TWOI_TOKEN>` o'rniga 1-qadamdagi tokenni kiriting)
3. JSON-javobda `"chat":{"id":123456789,...}` ni toping — bu sizning chat_id

## 3-qadam: Muhit o'zgaruvchilarini sozlash

Loyiha terminalini oching:

```bash
cd /Users/mukhammadamir/Sites/WORK/trading

# O'z qiymatlaringizni kiriting
export TELEGRAM_BOT_TOKEN="123456789:ABCdef..."
export TELEGRAM_CHAT_ID="123456789"
```

O'zgaruvchilar sessiyalar orasida saqlanishi uchun — `~/.zshrc` ga qo'shing:

```bash
echo 'export TELEGRAM_BOT_TOKEN="123456789:ABCdef..."' >> ~/.zshrc
echo 'export TELEGRAM_CHAT_ID="123456789"' >> ~/.zshrc
source ~/.zshrc
```

## 4-qadam: Sinov ishga tushirish

Avval — **dry-run** (Telegramga yubormasdan):

```bash
.venv/bin/python advanced/telegram_alerts.py --symbol EURUSD --dry-run
```

Terminalda qaysi signallar **yuborilishi mumkinligi** ko'rsatiladi.

Natija yaxshi ko'rinsa — yuborish bilan ishga tushirish:

```bash
.venv/bin/python advanced/telegram_alerts.py --symbol EURUSD
```

Telegramni oching → signal kelishi kerak (agar so'nggi soatlarda mavjud bo'lsa).

## 5-qadam: Har soatda avtomatik ishga tushirish

### A-variant: cron (macOS / Linux)

```bash
crontab -e
```

Qatorni qo'shing:
```cron
0 * * * * cd /Users/mukhammadamir/Sites/WORK/trading && /Users/mukhammadamir/Sites/WORK/trading/.venv/bin/python advanced/telegram_alerts.py >> /tmp/telegram_alerts.log 2>&1
```

Bu qator skriptni **har soat boshida** ishga tushiradi. Loglar `/tmp/telegram_alerts.log` ga saqlanadi.

⚠️ Cronda muhit o'zgaruvchilari mavjud emas! Ularni buyruqqa qo'shing:
```cron
0 * * * * cd /Users/mukhammadamir/Sites/WORK/trading && TELEGRAM_BOT_TOKEN="123..." TELEGRAM_CHAT_ID="123..." /Users/mukhammadamir/Sites/WORK/trading/.venv/bin/python advanced/telegram_alerts.py >> /tmp/telegram_alerts.log 2>&1
```

Yoki `.env` faylidan foydalaning (quyida ko'ring).

### B-variant: launchd (macOS, to'g'riroq usul)

`~/Library/LaunchAgents/com.amir.forex-alerts.plist` faylini yarating:

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

Ishga tushiring:
```bash
launchctl load ~/Library/LaunchAgents/com.amir.forex-alerts.plist
```

Har soatda 5-daqiqada ishga tushadi.

To'xtatish:
```bash
launchctl unload ~/Library/LaunchAgents/com.amir.forex-alerts.plist
```

### V-variant: bulutli server (doimiy ishlash uchun)

Quyidagilarda joylashtirish mumkin:
- **Heroku** (bepul tarif — 550 soat/oy)
- **PythonAnywhere** (bepul, oddiy cron sozlash)
- **Render** (bepul tarif)
- **VPS-dagi konteyner** (agar mavjud bo'lsa)

Hozircha mahalliy ishga tushirishni o'zlashtirib oling — chuqurroq kirmaymiz.

## 6-qadam: Tokenni xavfsiz saqlash

**⚠️ Tokenni hech qachon Git'ga pushmang!**

Ildizda `.env` faylini yarating:

```bash
TELEGRAM_BOT_TOKEN=123456789:ABCdef...
TELEGRAM_CHAT_ID=123456789
```

`.env` allaqachon `.gitignore` da mavjud.

[python-dotenv](https://pypi.org/project/python-dotenv/) orqali yuklang:

```bash
.venv/bin/pip install python-dotenv
```

`telegram_alerts.py` boshiga (qo'shish mumkin):
```python
from dotenv import load_dotenv
load_dotenv()
```

## 7-qadam: Funksionallikni kengaytirish

Botni kengaytirish mumkin:

### Bir nechta juftlar
```bash
for pair in EURUSD GBPUSD USDJPY; do
  .venv/bin/python advanced/telegram_alerts.py --symbol $pair
done
```

### Bot buyruqlari (ikki tomonlama aloqa)
Botga yozish imkoniyati:
- `/status` → joriy ochiq signal
- `/stats` → so'nggi signallar statistikasi
- `/disable EURUSD` → juftni o'chirish

Bu `python-telegram-bot` kutubxonasini talab qiladi:
```bash
.venv/bin/pip install python-telegram-bot
```

### Do'stlar bilan signal guruhi
1. Telegramda guruh yarating
2. Botingizni guruhga qo'shing
3. Botni **admin** qiling (@BotFather orqali)
4. Guruh chat_id ni oling (`/getUpdates` orqali, JSON da manfiy ID bo'ladi)
5. Bu ID ni `TELEGRAM_CHAT_ID` sifatida ishlating

## 8-qadam: Signallar bilan nima qilish kerak

Bot signal yubordi — bu savdo qilish **buyrug'i emas**. Bu **bildirishnoma** — skriptimiz setap topganini anglatadi.

Savdoni ochishdan oldin:
1. ✅ MT5 ni oching → setap haqiqatan borligini tekshiring (bot xato qilishi mumkin)
2. ✅ [Chop etiladigan chek-list](../extras/checklist-printable.md) bo'yicha o'ting
3. ✅ [position_calculator.py](https://github.com/MukhammadAmir-Akbarov/forex-toolkit/blob/main/tools/position_calculator.py) ni ishga tushiring
4. ✅ Ochishdan OLDIN rejalashtirilgan parametrlarni jurnalga yozing
5. ✅ SL va TP bilan savdoni oching

**Hech qachon signaldan darhol tekshiruvsiz savdo oching.**

## Muammolarni bartaraf etish

### Bot /start ga javob bermayapti
- Ehtimol, token noto'g'ri
- Bot bloklanmaganligini tekshiring

### Xabarlar kelmayapti
- chat_id ni tekshiring — bu **sizning** ID'ingiz bo'lishi kerak, username emas
- `--dry-run` bilan ishga tushiring — signallar umuman generatsiya qilinayotganligini ko'rasiz

### yfinance ishlamay qoldi
- yfinance ba'zan tez-tez so'rovlarni bloklaydi → 10 daqiqa kuting
- Ehtimol, internet yo'q

### Signallar «eskirgan» ko'rinadi
- yfinance kotirovkalarni 15-30 daqiqa kechikish bilan beradi
- Real vaqtda savdo uchun broker API yoki pullik ma'lumotlar tasmasi kerak

---

## Yakuniy eslatma

🚨 **Telegram-bot — bu faqat bildirishnomalar.** Hech qanday avtomatik orderlar yo'q. Har bir savdo bo'yicha qarorni o'zingiz qabul qilasiz. Bot setaplarni **aniqlash** jarayonini tezlashtiradi, lekin sizning tahlil va intizomingizni almashtirmaydi.

---

[← Asosiy qo'llanmaga qaytish](../forex-guide.md)
