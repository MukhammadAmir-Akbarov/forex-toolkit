# VPS Deployment Guide — Running Bots 24/7

> For a Telegram bot, MT5 EA, or Streamlit app to run **continuously**, you need a server. This guide covers how to set up a **VPS (Virtual Private Server)** affordably.

## When You Need a VPS

- ✅ A Telegram bot that must send signals 24/7
- ✅ An MT5 EA that should trade at night while you sleep
- ✅ A Streamlit app with public access
- ✅ Cron jobs (daily backtest, weekly report)

## When You Do NOT Need One

- ❌ Demo-only learning
- ❌ Manual trading (your laptop is always with you)
- ❌ You are not ready to spend at least $100/month on infrastructure

## How Much Does It Cost

| Provider | Price | Best For |
|---|---|---|
| **Hetzner CX22** | ~€4/month | Telegram bot, Streamlit |
| **DigitalOcean Basic** | $6/month | Any Python script |
| **AWS EC2 t4g.small** | ~$15/month | Higher performance |
| **Contabo VPS S** | €5/month | Budget option |
| **CIS providers** | $3–10/month | Regional, but sanction risks |

**Recommendation:** Hetzner or DigitalOcean — simple and reliable.

---

## Part 1: Linux VPS for Python Bots

### Step 1: Sign Up and Create a VPS

#### Hetzner (example)

1. https://www.hetzner.com/cloud
2. Register → confirm email
3. **Add Server**:
   - Location: **Helsinki** (faster for Uzbekistan) or **Falkenstein**
   - OS: **Ubuntu 24.04**
   - Type: **CX22** (€4.51/month: 2 vCPU, 4 GB RAM, 40 GB SSD)
   - Authentication: **Add SSH key** (generate locally, see below)
   - Name: `forex-bot-server`
4. Click **Create** → server is ready in about 30 seconds

#### Generating an SSH Key (on your Mac)

```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
# Press Enter, Enter, Enter (passphrase is optional)
cat ~/.ssh/id_ed25519.pub
# Copy the output → paste it into Hetzner when creating the server
```

### Step 2: Connect to the Server

After creation you will receive an **IP address**, for example `116.203.45.67`.

```bash
ssh root@116.203.45.67
# First connection will ask for confirmation — type yes
```

### Step 3: Basic Server Setup

```bash
# Update packages
apt update && apt upgrade -y

# Install tools
apt install -y python3 python3-pip python3-venv git tmux htop curl

# Create a non-root user
adduser trader
usermod -aG sudo trader

# Configure SSH for the new user
mkdir -p /home/trader/.ssh
cp ~/.ssh/authorized_keys /home/trader/.ssh/
chown -R trader:trader /home/trader/.ssh
chmod 700 /home/trader/.ssh

# Disable root login (security)
nano /etc/ssh/sshd_config
# Find and change: PermitRootLogin no
systemctl restart ssh

# Firewall
apt install ufw -y
ufw allow OpenSSH
ufw allow 8501  # streamlit (if needed)
ufw enable

# Exit root session
exit
```

From this point on, connect as `trader`:
```bash
ssh trader@116.203.45.67
```

### Step 4: Deploy the Bot

```bash
# On the VPS
cd ~
git clone https://github.com/yourusername/trading.git
# OR copy files via scp from your Mac:
# scp -r /Users/mukhammadamir/Sites/WORK/trading trader@116.203.45.67:~/

cd trading

# Create virtual environment
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt  # see below
# Or manually:
.venv/bin/pip install matplotlib numpy pandas python-docx jinja2 \
    yfinance requests beautifulsoup4 reportlab
```

Create `requirements.txt`:

```bash
cd /Users/mukhammadamir/Sites/WORK/trading
.venv/bin/pip freeze > requirements.txt
```

### Step 5: Run the Telegram Bot as a Service

Create a systemd unit — a service that restarts on failure and starts on reboot:

```bash
sudo nano /etc/systemd/system/telegram-alerts.service
```

Paste:
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

And a timer (runs every hour):
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

Start it:
```bash
sudo systemctl daemon-reload
sudo systemctl enable telegram-alerts.timer
sudo systemctl start telegram-alerts.timer

# Check status
systemctl status telegram-alerts.timer
journalctl -u telegram-alerts.service -n 50
```

### Step 6: Streamlit as a Service

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

Open in your browser: `http://116.203.45.67:8501`

---

## Part 2: VPS for MT5 (Windows)

⚠️ MT5 is a Windows application. You need a **Windows VPS**, not Linux.

### Providers with Windows

| Provider | Price | Suitable For |
|---|---|---|
| **Forex VPS** (specialized) | $20–50/month | Very close to broker servers |
| **Vultr Windows** | $16/month | General purpose |
| **DigitalOcean (via WINE)** | $6/month | Experienced users only |

### Forex VPS — Main Advantage

Servers located close to broker servers → **lower latency**. Especially important for scalping. Most offer:
- Ready-made Windows 10
- MT5 / MT4 pre-installed
- 24/7 uptime
- Backup
- $20–30/month

Examples:
- **ForexVPS.net**
- **BeeksFX**
- **CNS** (Commercial Network Services)

### Installing MT5 on a Windows VPS

1. Connect via RDP (Remote Desktop, built into Windows)
2. Download MT5 from your broker's website
3. Log in to your account
4. Drag your EA into MQL5/Experts
5. Enable **AutoTrading** in the top toolbar
6. **Minimize** the window (do not close!) — MT5 will keep running
7. Disconnect from RDP — MT5 operates autonomously

### Windows VPS Security

- ✅ Install antivirus software
- ✅ Enable **Windows Firewall**
- ✅ **Do not save** RDP passwords
- ✅ **Disable login** for all other users
- ✅ **Do not browse websites** on this server — it is for MT5 only

---

## Part 3: Backup and Monitoring

### Backups

Configuration files and trade journals must be backed up.

#### Cron Backup on the Same VPS

```bash
# In crontab -e
0 3 * * * tar -czf ~/backups/trading-$(date +\%Y\%m\%d).tar.gz ~/trading
```

#### Off-Site Backup to S3 / Backblaze

```bash
# Install rclone
curl https://rclone.org/install.sh | sudo bash
rclone config  # configure Backblaze B2 / AWS S3

# In cron
0 4 * * * rclone sync ~/trading/journal/ remote:forex-backup/journal/
```

### Uptime Monitoring

Free services that **ping** your server and send an alert if it goes down:

- **UptimeRobot** — 50 free monitors
- **BetterStack** — premium tier
- **HealthChecks.io** — for cron jobs

Setting up UptimeRobot:
1. Register
2. Add monitor → HTTP
3. URL: `http://YOUR_IP:8501` (Streamlit)
4. Interval: 5 minutes
5. Alert: email / Telegram

### Logs

All system service logs:
```bash
# Last 100 lines
journalctl -u telegram-alerts.service -n 100

# Live tail (follow in real time)
journalctl -u streamlit-forex.service -f

# Last 24 hours
journalctl --since "24 hours ago" -u telegram-alerts.service
```

---

## Part 4: Security

### Core Rules

1. **No passwords in code.** Use `.env` files or systemd Environment.
2. **SSH key-only access.** Disable password authentication:
   ```bash
   sudo nano /etc/ssh/sshd_config
   # PasswordAuthentication no
   sudo systemctl restart ssh
   ```
3. **Fail2ban** — blocks IPs after repeated failed attempts:
   ```bash
   sudo apt install fail2ban -y
   ```
4. **Regular updates:**
   ```bash
   sudo apt update && sudo apt upgrade -y
   ```
   Or automatically:
   ```bash
   sudo apt install unattended-upgrades -y
   ```
5. **Never grant root access** to any scripts.

### What NOT to Do

- ❌ Do not store your **broker passwords** on the VPS in plain text
- ❌ Do not expose **public access** to your MT5
- ❌ Do not clone a GitHub repository that contains **personal journal data**
- ❌ Do not share one server across multiple clients or friends

---

## Part 5: Cost Savings

### How to Pay Less

1. **Hetzner**: hourly billing → shut it down when not needed
2. **DigitalOcean credits** — promo codes for $100–200 available for new users
3. **AWS Free Tier** — 1 year free (t2.micro)
4. **Oracle Free Tier** — ARM server free forever (4 CPU, 24 GB RAM!)

### Minimum Configuration for a Telegram Bot

- 1 vCPU
- 512 MB RAM (sufficient)
- 10 GB SSD
- = **$3–5/month**

MT5 requires more:
- 2+ vCPU
- 4 GB RAM
- Windows = +$10–20/month

---

## Part 6: VPS Alternatives

### Free / Conditionally Free

| Service | What | Limitations |
|---|---|---|
| **GitHub Actions** | Cron jobs | 2,000 min/month |
| **Railway.app** | Containers | $5/month in credits |
| **Render.com** | Services | Free tier sleeps when idle |
| **PythonAnywhere** | Python scripts | $5/month for always-on |
| **Replit** | Any code | Paid for always-online |

### If You Only Need a Telegram Bot

You may not need a VPS at all — use **GitHub Actions**:

`.github/workflows/telegram-alerts.yml`:
```yaml
name: Telegram Alerts
on:
  schedule:
    - cron: '0 * * * *'  # every hour
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

Push to GitHub → Settings → Secrets → add your tokens → done, completely free.

---

## VPS Readiness Checklist

```
☐ VPS created and SSH is working
☐ Non-root user created
☐ Root SSH login disabled
☐ Firewall (ufw / Windows Firewall) configured
☐ Project cloned
☐ venv created, dependencies installed
☐ .env file with tokens in place (not in Git!)
☐ Systemd service configured and running
☐ Logs verified
☐ UptimeRobot configured
☐ Backup configured
☐ unattended-upgrades enabled
```

**All ☑ → your bot runs 24/7 without you.**

---

[← Telegram setup](SETUP-telegram.md) · [← Main guide](../forex-guide.md)
