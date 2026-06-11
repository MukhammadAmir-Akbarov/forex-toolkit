# VPS Deployment Guide — botlarni 24/7 ishlatish

> Telegram-bot, MT5 EA yoki Streamlit **doimo ishlashi** uchun server kerak. Bu qo'llanma — **VPS (Virtual Private Server)** ni arzon narxda qanday sozlash haqida.

## VPS qachon kerak

- ✅ 24/7 signal yuboradigan Telegram-bot
- ✅ Siz uxlayotganingizda kechasi savdo qiladigan MT5 EA
- ✅ Ochiq kirish imkoniyatli Streamlit-ilova
- ✅ Cron-vazifalar (har kuni bektestlash, har hafta hisobot)

## VPS qachon KERAK EMAS

- ❌ Faqat demo-o'rganish
- ❌ Qo'l bilan savdo qilasiz (noutbuk har doim yoningizda)
- ❌ Oyiga 100 USD dan kam sarflashga tayyor (VPS — infratuzilma xarajati)

## Qancha turadi

| Provayder | Narx | Nima uchun mos |
|---|---|---|
| **Hetzner CX22** | ~€4/oy | Telegram-bot, Streamlit |
| **DigitalOcean Basic** | $6/oy | Har qanday Python-skript |
| **AWS EC2 t4g.small** | ~$15/oy | Yuqori unumdorlik |
| **Contabo VPS S** | €5/oy | Byudjet varianti |
| **Rossiya provayderlar** | $3-10/oy | MDH uchun, ammo sanksiyalar |

**Tavsiya:** Hetzner yoki DigitalOcean. Oddiy, ishonchli.

---

## 1-qism: Python-botlar uchun Linux VPS

### 1-qadam: Ro'yxatdan o'tish va VPS yaratish

#### Hetzner (misol)

1. https://www.hetzner.com/cloud
2. Ro'yxatdan o'tish → email tasdiqlash
3. **Add Server**:
   - Location: **Helsinki** (O'zbekiston uchun tezroq) yoki **Falkenstein**
   - OS: **Ubuntu 24.04**
   - Type: **CX22** (€4.51/oy: 2 vCPU, 4GB RAM, 40GB SSD)
   - Authentication: **Add SSH key** (lokal yarating, pastga qarang)
   - Name: `forex-bot-server`
4. **Create** tugmasini bosing → 30 soniyadan keyin server tayyor

#### SSH kalitini yaratish (Mac'ingizda)

```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
# Enter, Enter, Enter (parol ixtiyoriy)
cat ~/.ssh/id_ed25519.pub
# Chiqishni nusxalang → server yaratishda Hetzner'ga joylashtiring
```

### 2-qadam: Serverga ulanish

Yaratilgandan so'ng **IP-manzil** olasiz, masalan `116.203.45.67`.

```bash
ssh root@116.203.45.67
# birinchi marta tasdiqlash so'raldi, yes deb javob bering
```

### 3-qadam: Serverni asosiy sozlash

```bash
# Paketlarni yangilash
apt update && apt upgrade -y

# Asboblarni o'rnatish
apt install -y python3 python3-pip python3-venv git tmux htop curl

# Foydalanuvchi yaratish (root ostida ishlamang!)
adduser trader
usermod -aG sudo trader

# Yangi foydalanuvchi uchun SSH sozlash
mkdir -p /home/trader/.ssh
cp ~/.ssh/authorized_keys /home/trader/.ssh/
chown -R trader:trader /home/trader/.ssh
chmod 700 /home/trader/.ssh

# Root kirish imkonini yopish (xavfsizlik)
nano /etc/ssh/sshd_config
# Topib o'zgartiring: PermitRootLogin no
systemctl restart ssh

# Xavfsizlik devori
apt install ufw -y
ufw allow OpenSSH
ufw allow 8501  # streamlit (agar kerak bo'lsa)
ufw enable

# Root'dan chiqish
exit
```

Bundan keyin `trader` sifatida ulaning:
```bash
ssh trader@116.203.45.67
```

### 4-qadam: Botni joylashtirish

```bash
# VPS da
cd ~
git clone https://github.com/yourusername/trading.git
# YOKI fayllarni Mac'ingizdan scp orqali ko'chiring:
# scp -r /Users/mukhammadamir/Sites/WORK/trading trader@116.203.45.67:~/

cd trading

# Virtual muhit
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt  # pastga qarang
# Yoki qo'lda:
.venv/bin/pip install matplotlib numpy pandas python-docx jinja2 \
    yfinance requests beautifulsoup4 reportlab
```

`requirements.txt` yarating:

```bash
cd /Users/mukhammadamir/Sites/WORK/trading
.venv/bin/pip freeze > requirements.txt
```

### 5-qadam: Telegram-botni servis sifatida ishga tushirish

Systemd-unit yarating — bu xizmat nosozlikda qayta ishga tushadi va qayta yuklaganda ham boshlanadi:

```bash
sudo nano /etc/systemd/system/telegram-alerts.service
```

Quyidagini joylashtiring:
```ini
[Unit]
Description=Forex Telegram Alerts
After=network.target

[Service]
Type=oneshot
User=trader
WorkingDirectory=/home/trader/trading
Environment="TELEGRAM_BOT_TOKEN=YOUR_TOKEN_HERE"
Environment="TELEGRAM_CHAT_ID=YOUR_CHAT_ID"
ExecStart=/home/trader/trading/.venv/bin/python advanced/telegram_alerts.py --symbol EURUSD

[Install]
WantedBy=multi-user.target
```

Va taymer (har soatda ishga tushirish):
```bash
sudo nano /etc/systemd/system/telegram-alerts.timer
```

```ini
[Unit]
Description=Run Forex Telegram Alerts every hour

[Timer]
OnCalendar=*-*-* *:05:00
Persistent=true

[Install]
WantedBy=timers.target
```

Ishga tushirish:
```bash
sudo systemctl daemon-reload
sudo systemctl enable telegram-alerts.timer
sudo systemctl start telegram-alerts.timer

# Tekshirish
systemctl status telegram-alerts.timer
journalctl -u telegram-alerts.service -n 50
```

### 6-qadam: Streamlit servis sifatida

```bash
sudo nano /etc/systemd/system/streamlit-forex.service
```

```ini
[Unit]
Description=Forex Streamlit App
After=network.target

[Service]
Type=simple
User=trader
WorkingDirectory=/home/trader/trading
ExecStart=/home/trader/trading/.venv/bin/streamlit run advanced/streamlit_app.py --server.address 0.0.0.0 --server.port 8501
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable streamlit-forex.service
sudo systemctl start streamlit-forex.service
```

Brauzerde oching: `http://116.203.45.67:8501`

---

## 2-qism: MT5 uchun VPS (Windows)

⚠️ MT5 — Windows-ilova. Ishlatish uchun **Windows VPS** kerak, Linux emas.

### Windows bilan provayderlar

| Provayder | Narx | Mos keladi |
|---|---|---|
| **Forex VPS** (ixtisoslashgan) | $20-50/oy | Broker serverlarga juda yaqin |
| **Vultr Windows** | $16/oy | Universal |
| **DigitalOcean (WINE orqali)** | $6/oy | Faqat tajribalilarga |

### Forex VPS — asosiy afzalligi

Serverlar broker serverlariga yaqin → **kamroq latency** (kechikish). Ayniqsa skalping uchun muhim. Ko'pchilik taklif etadi:
- Tayyor Windows 10
- MT5 / MT4 o'rnatilgan holda
- 24/7 uptime
- Zaxiralash (Backup)
- $20-30/oy

Misollar:
- **ForexVPS.net**
- **BeeksFX**
- **CNS** (Commercial Network Services)

### Windows VPS ga MT5 o'rnatish

1. RDP (Remote Desktop, Windows'ga o'rnatilgan) orqali ulaning
2. MT5 ni broker saytidan yuklab oling
3. Hisobingizga kiring
4. EA ni MQL5/Experts dan torting
5. Yuqori paneldagi **AutoTrading** ni yoqing
6. Oynani **kichiklashtiring** (yopmang!) — MT5 ishlashda davom etadi
7. RDP dan uzing — MT5 mustaqil ishlaydi

### Windows VPS xavfsizligi

- ✅ Antivirus o'rnating
- ✅ **Windows Firewall** ni yoqing
- ✅ RDP parollarini **saqlamang**
- ✅ Boshqa barcha foydalanuvchilar uchun **Kirish imkonini o'chiring**
- ✅ Bu serverda **saytlarni ochimang** — u faqat MT5 uchun

---

## 3-qism: Zaxiralash va monitoring

### Zaxiralash (Backup)

Konfiguratsiyalar va jurnallarni zaxiralash muhim.

#### Xuddi shu VPS'ga cron-zaxiralash

```bash
# crontab -e ichida
0 3 * * * tar -czf ~/backups/trading-$(date +\%Y\%m\%d).tar.gz ~/trading
```

#### S3 / Backblaze'ga zaxiralash (tashqi)

```bash
# rclone o'rnatish
curl https://rclone.org/install.sh | sudo bash
rclone config  # Backblaze B2 / AWS S3 sozlash

# cron da
0 4 * * * rclone sync ~/trading/journal/ remote:forex-backup/journal/
```

### Uptime monitoringi

Serveringizni **ping** qilib, yiqilsa xabar yuboradigan bepul xizmatlar:

- **UptimeRobot** — 50 ta monitor bepul
- **BetterStack** — premium
- **HealthChecks.io** — cron-vazifalar uchun

UptimeRobot sozlash:
1. Ro'yxatdan o'tish
2. Add monitor → HTTP
3. URL: `http://YOUR_IP:8501` (Streamlit)
4. Interval: 5 daqiqa
5. Xabar: email / Telegram

### Loglar

Barcha tizim servislari loglari:
```bash
# Oxirgi 100 qator
journalctl -u telegram-alerts.service -n 100

# Live tail (real vaqtda kuzatish)
journalctl -u streamlit-forex.service -f

# Oxirgi 24 soat uchun
journalctl --since "24 hours ago" -u telegram-alerts.service
```

---

## 4-qism: Xavfsizlik

### Asosiy qoidalar

1. **Kodda parol bo'lmasin.** `.env`-fayllar yoki systemd Environment ishlating.
2. **SSH faqat kalit orqali.** Parollarni o'chiring:
   ```bash
   sudo nano /etc/ssh/sshd_config
   # PasswordAuthentication no
   sudo systemctl restart ssh
   ```
3. **Fail2ban** — muvaffaqiyatsiz urinishlardan keyin IP ni bloklaydi:
   ```bash
   sudo apt install fail2ban -y
   ```
4. **Muntazam yangilanishlar:**
   ```bash
   sudo apt update && sudo apt upgrade -y
   ```
   Yoki avtomatik:
   ```bash
   sudo apt install unattended-upgrades -y
   ```
5. **Hech qanday skriptga root-kirish bermang.**

### Nima QILMASLIK kerak

- ❌ **Broker parollaringizni** VPS da ochiq saqlang
- ❌ MT5 ingizga **ommaviy kirish** bering
- ❌ GitHub dan **shaxsiy jurnal ma'lumotlari** bo'lgan repozitoryni klonlang
- ❌ Bir serverni bir nechta mijoz / do'stlar uchun ishlating

---

## 5-qism: Tejash

### Kamroq to'lash yo'llari

1. **Hetzner**: soatbay to'lov → kerak bo'lmaganda o'chirib qo'ying
2. **DigitalOcean credits** — yangi foydalanuvchilar uchun $100-200 promo-kodlar mavjud
3. **AWS Free Tier** — 1 yil bepul (t2.micro)
4. **Oracle Free Tier** — ARM-server umrbod bepul (4 CPU, 24GB RAM!)

### Telegram-bot uchun minimal konfiguratsiya

- 1 vCPU
- 512 MB RAM (yetarli)
- 10 GB SSD
- = **$3-5/oy**

MT5 uchun ko'proq kerak:
- 2+ vCPU
- 4 GB RAM
- Windows = +$10-20/oy

---

## 6-qism: VPS muqobillar

### Bepul / shartli bepul

| Xizmat | Nima | Cheklovlar |
|---|---|---|
| **GitHub Actions** | Cron-vazifalar | 2000 min/oy |
| **Railway.app** | Konteynerlar | $5/oy kredit |
| **Render.com** | Xizmatlar | Uyqu rejimli bepul daraja |
| **PythonAnywhere** | Python-skriptlar | Doimiy ishlatish uchun $5/oy |
| **Replit** | Har qanday kod | Har doim onlayn uchun pullik |

### Faqat Telegram-bot bo'lsa

VPS sotib olmasangiz ham bo'ladi — **GitHub Actions** dan foydalaning:

`.github/workflows/telegram-alerts.yml`:
```yaml
name: Telegram Alerts
on:
  schedule:
    - cron: '0 * * * *'  # har soat
  workflow_dispatch:

jobs:
  alert:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - env:
          TELEGRAM_BOT_TOKEN: ${{ secrets.TELEGRAM_BOT_TOKEN }}
          TELEGRAM_CHAT_ID: ${{ secrets.TELEGRAM_CHAT_ID }}
        run: python advanced/telegram_alerts.py
```

GitHub'ga joylang → Settings → Secrets → tokenlarni qo'shing → tayyor, bepul.

---

## VPS tayyor bo'lish nazorat ro'yxati

```
☐ VPS yaratildi va SSH ishlayapti
☐ Root bo'lmagan foydalanuvchi yaratildi
☐ Root SSH o'chirildi
☐ Xavfsizlik devori (ufw / Windows Firewall) sozlandi
☐ Loyiha klonlandi
☐ venv yaratildi, bog'liqliklar o'rnatildi
☐ .env fayli tokenlar bilan joyida (Git'da emas!)
☐ Systemd-servis sozlandi va ishga tushirildi
☐ Loglar tekshirildi
☐ UptimeRobot sozlandi
☐ Zaxiralash sozlandi
☐ unattended-upgrades yoqildi
```

**Barchasi ☑ → botingiz sizisiz 24/7 ishlaydi.**

---

[← Telegram setup ga](SETUP-telegram.md) · [← Asosiy qo'llanmaga](../forex-guide.md)
