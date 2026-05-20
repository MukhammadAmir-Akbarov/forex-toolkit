# VPS Deployment Guide — запуск ботов 24/7

> Чтобы Telegram-бот, MT5 EA или Streamlit работали **постоянно**, нужен сервер. Этот гайд — как настроить **VPS (Virtual Private Server)** недорого.

## Когда нужен VPS

- ✅ Telegram-бот, который должен слать сигналы 24/7
- ✅ MT5 EA, который должен торговать ночью когда ты спишь
- ✅ Streamlit-приложение с публичным доступом
- ✅ Cron-задачи (бэктест каждый день, отчёт каждую неделю)

## Когда НЕ нужен

- ❌ Только демо-обучение
- ❌ Торгуешь руками (ноут всегда с тобой)
- ❌ Менее 100 USD/мес готов тратить (VPS — это инфраструктурная статья)

## Сколько стоит

| Провайдер | Цена | Что подходит |
|---|---|---|
| **Hetzner CX22** | ~€4/мес | Telegram-бот, Streamlit |
| **DigitalOcean Basic** | $6/мес | Любой Python-скрипт |
| **AWS EC2 t4g.small** | ~$15/мес | Производительность |
| **Contabo VPS S** | €5/мес | Бюджетный вариант |
| **Российские провайдеры** | $3-10/мес | Для CIS, но санкции |

**Рекомендую:** Hetzner или DigitalOcean. Простые, надёжные.

---

## Часть 1: Linux VPS для Python-ботов

### Шаг 1: Регистрация и создание VPS

#### Hetzner (пример)

1. https://www.hetzner.com/cloud
2. Регистрация → email подтверждение
3. **Add Server**:
   - Location: **Helsinki** (быстрее для Узбекистана) или **Falkenstein**
   - OS: **Ubuntu 24.04**
   - Type: **CX22** (€4.51/мес: 2 vCPU, 4GB RAM, 40GB SSD)
   - Authentication: **Add SSH key** (создай локально, см. ниже)
   - Name: `forex-bot-server`
4. Жми **Create** → через 30 сек сервер готов

#### Генерация SSH ключа (на твоём Mac)

```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
# Enter, Enter, Enter (пароль необязателен)
cat ~/.ssh/id_ed25519.pub
# Скопируй вывод → вставь в Hetzner при создании сервера
```

### Шаг 2: Подключение к серверу

После создания получишь **IP-адрес**, например `116.203.45.67`.

```bash
ssh root@116.203.45.67
# первый раз спросит подтверждение, ответь yes
```

### Шаг 3: Базовая настройка сервера

```bash
# Обновить пакеты
apt update && apt upgrade -y

# Установить инструменты
apt install -y python3 python3-pip python3-venv git tmux htop curl

# Создать пользователя (не работать под root!)
adduser trader
usermod -aG sudo trader

# Настроить SSH для нового пользователя
mkdir -p /home/trader/.ssh
cp ~/.ssh/authorized_keys /home/trader/.ssh/
chown -R trader:trader /home/trader/.ssh
chmod 700 /home/trader/.ssh

# Запретить root-вход (безопасность)
nano /etc/ssh/sshd_config
# Найди и измени: PermitRootLogin no
systemctl restart ssh

# Файрвол
apt install ufw -y
ufw allow OpenSSH
ufw allow 8501  # streamlit (если нужен)
ufw enable

# Выйти из root
exit
```

С этого момента подключайся как `trader`:
```bash
ssh trader@116.203.45.67
```

### Шаг 4: Деплой бота

```bash
# На VPS
cd ~
git clone https://github.com/yourusername/trading.git
# ИЛИ скопируй файлы через scp с твоего Mac:
# scp -r /Users/mukhammadamir/Sites/WORK/trading trader@116.203.45.67:~/

cd trading

# Окружение
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt  # см. ниже
# Или вручную:
.venv/bin/pip install matplotlib numpy pandas python-docx jinja2 \
    yfinance requests beautifulsoup4 reportlab
```

Создай `requirements.txt`:

```bash
cd /Users/mukhammadamir/Sites/WORK/trading
.venv/bin/pip freeze > requirements.txt
```

### Шаг 5: Запуск Telegram-бота как сервиса

Создай systemd-юнит — это сервис, который перезапускается при сбое и стартует при ребуте:

```bash
sudo nano /etc/systemd/system/telegram-alerts.service
```

Вставь:
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

И таймер (запуск каждый час):
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

Запуск:
```bash
sudo systemctl daemon-reload
sudo systemctl enable telegram-alerts.timer
sudo systemctl start telegram-alerts.timer

# Проверка
systemctl status telegram-alerts.timer
journalctl -u telegram-alerts.service -n 50
```

### Шаг 6: Streamlit как сервис

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

Открой в браузере: `http://116.203.45.67:8501`

---

## Часть 2: VPS для MT5 (Windows)

⚠️ MT5 — Windows-приложение. Для запуска нужен **Windows VPS**, не Linux.

### Провайдеры с Windows

| Провайдер | Цена | Подходит |
|---|---|---|
| **Forex VPS** (специализированный) | $20-50/мес | Очень близко к серверам брокеров |
| **Vultr Windows** | $16/мес | Универсальный |
| **DigitalOcean (через WINE)** | $6/мес | Только для опытных |

### Forex VPS — главное преимущество

Серверы близко к серверам брокеров → **меньше latency** (задержка). Особенно важно для скальпинга. Многие предлагают:
- Готовая Windows 10
- MT5 / MT4 предустановлены
- 24/7 uptime
- Backup
- $20-30/мес

Примеры:
- **ForexVPS.net**
- **BeeksFX**
- **CNS** (Commercial Network Services)

### Установка MT5 на Windows VPS

1. Подключись через RDP (Remote Desktop, встроен в Windows)
2. Скачай MT5 с сайта брокера
3. Войди в свой счёт
4. Перетащи EA из MQL5/Experts
5. Включи **AutoTrading** в верхней панели
6. **Минимизируй** окно (не закрывай!) — MT5 продолжит работать
7. Отключись от RDP — MT5 работает автономно

### Безопасность Windows VPS

- ✅ Установи антивирус
- ✅ Включи **Windows Firewall**
- ✅ **Не сохраняй** RDP пароли
- ✅ **Отключи Login** для всех других пользователей
- ✅ **Не открывай сайты** на этом сервере — он только для MT5

---

## Часть 3: Backup и мониторинг

### Бэкапы

Конфигурации и журналы важно бэкапить.

#### Cron-бэкап на тот же VPS

```bash
# В crontab -e
0 3 * * * tar -czf ~/backups/trading-$(date +\%Y\%m\%d).tar.gz ~/trading
```

#### Бэкап в S3 / Backblaze (off-site)

```bash
# Установка rclone
curl https://rclone.org/install.sh | sudo bash
rclone config  # настройка Backblaze B2 / AWS S3

# В cron
0 4 * * * rclone sync ~/trading/journal/ remote:forex-backup/journal/
```

### Мониторинг uptime

Бесплатные сервисы, которые **пингуют** твой сервер и шлют алерт, если упал:

- **UptimeRobot** — 50 мониторов бесплатно
- **BetterStack** — премиум
- **HealthChecks.io** — для cron-задач

Настройка UptimeRobot:
1. Регистрация
2. Add monitor → HTTP
3. URL: `http://YOUR_IP:8501` (Streamlit)
4. Interval: 5 минут
5. Alert: email / Telegram

### Логи

Все логи системных сервисов:
```bash
# Последние 100 строк
journalctl -u telegram-alerts.service -n 100

# Live tail (следить в реальном времени)
journalctl -u streamlit-forex.service -f

# За последние 24 часа
journalctl --since "24 hours ago" -u telegram-alerts.service
```

---

## Часть 4: Безопасность

### Главные правила

1. **Никаких паролей в коде.** Используй `.env`-файлы или systemd Environment.
2. **SSH только по ключу.** Отключи пароли:
   ```bash
   sudo nano /etc/ssh/sshd_config
   # PasswordAuthentication no
   sudo systemctl restart ssh
   ```
3. **Fail2ban** — блокирует IP после неудачных попыток:
   ```bash
   sudo apt install fail2ban -y
   ```
4. **Регулярные обновления:**
   ```bash
   sudo apt update && sudo apt upgrade -y
   ```
   Или автоматически:
   ```bash
   sudo apt install unattended-upgrades -y
   ```
5. **Не давай root-доступ** никаким скриптам.

### Что НЕ делать

- ❌ Не размещай свои **брокерские пароли** на VPS открыто
- ❌ Не давай **публичный доступ** к своему MT5
- ❌ Не клонируй с GitHub репозиторий с **личными данными** журнала
- ❌ Не используй один сервер для нескольких клиентов / друзей

---

## Часть 5: Экономия

### Как платить меньше

1. **Hetzner**: оплата за час → выключаешь когда не нужно
2. **DigitalOcean credits** — есть промокоды на $100-200 для новых пользователей
3. **AWS Free Tier** — 1 год бесплатно (t2.micro)
4. **Oracle Free Tier** — ARM-сервер бесплатно навсегда (4 CPU, 24GB RAM!)

### Минимальная конфигурация для Telegram-бота

- 1 vCPU
- 512 MB RAM (хватает)
- 10 GB SSD
- = **$3-5/мес**

Для MT5 нужно больше:
- 2+ vCPU
- 4 GB RAM
- Windows = +$10-20/мес

---

## Часть 6: Альтернативы VPS

### Бесплатные / условно-бесплатные

| Сервис | Что | Ограничения |
|---|---|---|
| **GitHub Actions** | Cron-задачи | 2000 мин/мес |
| **Railway.app** | Контейнеры | $5/мес кредитов |
| **Render.com** | Сервисы | Free tier с засыпанием |
| **PythonAnywhere** | Python-скрипты | $5/мес для постоянного запуска |
| **Replit** | Любой код | Платно для всегда-онлайн |

### Если только Telegram-бот

Можешь даже не покупать VPS — используй **GitHub Actions**:

`.github/workflows/telegram-alerts.yml`:
```yaml
name: Telegram Alerts
on:
  schedule:
    - cron: '0 * * * *'  # каждый час
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

Положи в GitHub → Settings → Secrets → добавь токены → готово, бесплатно.

---

## Чек-лист готовности VPS

```
☐ VPS создан и SSH работает
☐ Не-root пользователь создан
☐ root SSH отключён
☐ Firewall (ufw / Windows Firewall) настроен
☐ Проект склонирован
☐ venv создан, зависимости установлены
☐ .env файл с токенами на месте (не в Git!)
☐ Systemd-сервис настроен и запущен
☐ Логи проверены
☐ UptimeRobot настроен
☐ Бэкап настроен
☐ unattended-upgrades включены
```

**Все ☑ → твой бот работает 24/7 без тебя.**

---

[← К Telegram setup](SETUP-telegram.md) · [← К главному гайду](../forex-guide.md)
