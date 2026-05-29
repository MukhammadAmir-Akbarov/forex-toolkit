# How to use this project — a tour

> Read this file **first**. It explains in simple language what you have, why you need it, and in what order to use everything.

---

## 1. What's actually in this folder?

You have **3 types of materials**:

| Type | What it is | Where it lives |
|---|---|---|
| 📚 **Books** (study texts) | Explain forex theory | `*.md` files in the root and in `docs/` |
| 📝 **Templates** | Ready-made forms for keeping a journal | `journal/` |
| 🛠️ **Programs** (Python) | Tools that compute things for you | `tools/`, `bot/` |

You can use **only the texts** (without Python at all) — that's enough to learn how to trade. Python is a bonus for those who want to automate calculations and understand the market more deeply.

---

## 2. The project map at a glance

```
trading/
│
├── 📖 КАК-ПОЛЬЗОВАТЬСЯ.md         ← you are here
├── 📖 README.md                    ← short project map
├── 📖 forex-guide.md               ← ⭐ MAIN TEXTBOOK (read this first)
│
├── 📚 docs/                        ← in-depth materials
│   ├── technical-analysis.md       ← how to read charts
│   ├── strategy-details.md         ← a specific trading strategy
│   └── images/                     ← pictures for the textbooks
│
├── 📝 journal/                     ← trade journal
│   ├── README.md                   ← journal instructions
│   ├── trading-journal-template.md ← template for Notion/Obsidian
│   └── trading-journal-template.csv← template for Google Sheets
│
├── 🛠️ tools/                       ← calculator
│   ├── position_calculator.py      ← calculates position size
│   └── chart_generator.py          ← creates charts for the textbooks
│
├── 🛠️ bot/                         ← strategy backtester
│   ├── strategy.py                 ← strategy rules in code
│   └── backtest.py                 ← runs the strategy on history
│
└── .venv/                          ← Python with libraries (don't touch)
```

---

## 3. The beginner's road — what to do in what order

### 🟢 Week 1: Read the theory

**Step 1.** Open [forex-guide.md](_mkdocs/forex-guide.md) — this is your main textbook.

Inside there are 14 sections: what forex is, how to read quotes, how trades work, how to choose a broker, risk management, common mistakes, and a six-month roadmap. About 700 lines, takes 2–3 hours to read. **Read it twice.**

**Step 2.** Open [docs/technical-analysis.md](_mkdocs/docs/technical-analysis.md) — an extended guide on "how to read a chart."

It contains **12 color charts**: what a candle is, reversal patterns, trends, indicators (EMA, RSI, MACD, Bollinger Bands), chart patterns (head and shoulders, triangles). It's the most "visual" document — examine the charts, don't just read.

**Step 3.** Open [docs/strategy-details.md](_mkdocs/docs/strategy-details.md) — a detailed breakdown of one trading strategy.

This is your first concrete **strategy**. It's called "Pullback to EMA50 with the trend." It's described from start to finish: when to enter, where to place the stop, where to take profit, and when the strategy does NOT work.

---

### 🟡 Week 2: Set up the infrastructure

**Step 4.** Register with a regulated broker (see section 4 in the main guide). Open **only a demo account**.

**Step 5.** Install MetaTrader 5 (free) from the broker's website. Connect to your demo account.

**Step 6.** Open [journal/](journal/) — choose where you'll keep your trade journal:

- **Google Sheets** (recommended for beginners): import `trading-journal-template.csv`. Instructions in [journal/README.md](journal/README.md).
- **Obsidian / Notion / Markdown**: copy `trading-journal-template.md`.

The journal is the single most important growth tool. Without it, you will not learn.

---

### 🟠 Weeks 3–12: Trade on demo

**Step 7.** Before **every** trade, run the position calculator:

```bash
.venv/bin/python tools/position_calculator.py
```

It will ask:
- Account balance (e.g., 1000)
- Risk % (0.5)
- Stop in pips (25)
- Pair (EURUSD)

And it will tell you **how many lots** to enter in the terminal. Without this, you'll be guessing by eye — the most common beginner mistake.

**Step 8.** After **every** trade, log it in your journal. At a minimum: date, pair, direction, entry, stop, take profit, result, followed the rules? (yes/no), takeaway.

**Step 9.** Once a week — weekly journal report (template is inside the journal file).

**Step 10.** Once a month — analysis: which trades followed the rules? Where are you making mistakes?

---

### 🔵 When it gets interesting — backtesting

This is **optional**, but very helpful for understanding. Run:

```bash
.venv/bin/python bot/backtest.py
```

The program:
1. Generates 2000 synthetic candles
2. Applies the strategy from `strategy-details.md` automatically
3. Shows statistics: win rate, profit factor, final result
4. Draws an **equity curve** (a chart of your balance across trades) at `bot/equity-curve.png`

This gives you an idea of **how the strategy behaves over the long run**, without you needing to manually check 100 trades.

---

## 4. How to open Markdown files (the `.md` ones)

Markdown is a text format with markup. You can open it **in several ways**:

### Option 1: VSCode (recommended)
1. Open the `trading/` folder in VSCode (File → Open Folder)
2. Click on any `.md` file on the left
3. **Ctrl+Shift+V** (or **Cmd+Shift+V** on Mac) — this opens a nice preview

In the preview, you'll see:
- Colored headings
- Clickable links
- Pictures right in the text
- Tables

### Option 2: GitHub / Obsidian
If you push the folder to GitHub, all `.md` files render beautifully automatically.

Obsidian / Notion are great apps for managing this kind of knowledge base.

### Option 3: Any text editor
You can even open them in Notepad, but it won't look nice (no formatting).

---

## 5. How to use the Python scripts

> If you've never written Python — don't worry. You don't need to know anything. Just run the commands.

### Step 1: Open the terminal

- **macOS:** Cmd+Space → "Terminal" → Enter
- **Windows:** Win+R → "cmd" → Enter
- **VSCode:** Terminal → New Terminal

### Step 2: Navigate to the project folder

```bash
cd /Users/mukhammadamir/Sites/WORK/trading
```

### Step 3: Run the commands

Any Python script is run like this:

```bash
.venv/bin/python <path-to-script>
```

**Examples:**

```bash
# Position calculator (will ask questions)
.venv/bin/python tools/position_calculator.py

# Calculator in one line (no questions)
.venv/bin/python tools/position_calculator.py --balance 1000 --risk 0.5 --stop 25 --pair EURUSD

# Strategy backtest
.venv/bin/python bot/backtest.py

# Regenerate all charts for the textbooks (usually not needed)
.venv/bin/python tools/chart_generator.py
```

### What is `.venv/`?

It's a **Python virtual environment** — an isolated little box with the `matplotlib`, `numpy`, `pandas` libraries installed. I created it in advance so you wouldn't have to install anything.

**Don't delete `.venv/`**, or the scripts will stop working. If you accidentally delete it — recreate it:

```bash
python3 -m venv .venv
.venv/bin/pip install matplotlib numpy pandas
```

---

## 6. What each script shows — with examples

### tools/position_calculator.py — position calculator

**Why:** calculates how many lots to put in a trade so you don't lose more than X% of your account.

**Example run:**

```bash
.venv/bin/python tools/position_calculator.py --balance 1000 --risk 0.5 --stop 25 --pair EURUSD
```

**What you'll see:**

```
╭─────────────────────────────────────────╮
│  POSITION SIZE CALCULATOR               │
╰─────────────────────────────────────────╯

Input data:
  Balance:           $1,000.00
  Risk:              0.50% = $5.00
  Stop loss:         25 pips
  Pair:              EURUSD
  Pip value:         $10.00 per 1 lot

Calculation:
  Size (exact):      0.0200 lots
  Size (rounded):    0.02 lots
  Real risk:         $5.00 (0.50%)

→ Enter in terminal: 0.02 lots
```

**How to read it:** "Enter in terminal: 0.02 lots" — this is the number you type into MetaTrader when opening the trade.

---

### bot/backtest.py — strategy backtester

**Why:** runs the strategy on historical data and tells you **whether it would have been profitable**.

**Example run:**

```bash
.venv/bin/python bot/backtest.py
```

**What you'll see:**

```
Generating 2000 synthetic H1 candles…
Period: 2026-01-01 → 2026-03-25 (2000 candles)
Scanning signals…
  Signals found: 11
Running trades…
  Real entries (no overlaps): 9

╭──────────────────────────────────────────────────╮
│  BACKTEST RESULTS                                │
╰──────────────────────────────────────────────────╯

  Total trades:         9
  Winning (win):        5
  Losing (loss):        4
  Win rate:             55.6%
  Profit Factor:        2.50
  Expectancy:           +0.67R / trade
  Total:                +6.00R

  ✅ Profit Factor ≥ 1.5 — solid statistics.

  Chart saved: bot/equity-curve.png
```

**How to read it:**

- **Win rate 55.6%** — more than half the trades were winners.
- **Profit Factor 2.50** — for every $1 of loss, there was $2.50 of profit. Good (the benchmark is ≥ 1.5).
- **Expectancy +0.67R** — *on average*, one trade brings in 0.67 of what you risked. Over 100 trades = +67R.
- **Total +6.00R** — the cumulative result: 6 times the size of a single risk.

What is **R**? It's **one unit of your risk**. If you risked $5 — that's "1R." A $10 profit = "+2R." Handy for measuring results independently of how big your account is.

The image `bot/equity-curve.png` shows how your notional balance grew/fell from trade to trade.

---

### bot/strategy.py — strategy code (not required reading)

This is the **"brain" of the backtester**: the strategy rules are programmed here — EMA50, RSI, candle patterns, entry conditions.

You **don't need to touch it**. Open it if you're curious: you'll see how theory turns into code.

---

### tools/chart_generator.py — textbook image generator

**Already run once.** It generated 12 PNG files in `docs/images/` that are displayed in the textbooks.

You only need to run it again if you want to change the style of the charts.

---

## 7. What to do on your first day — a concrete plan

If you've just sat down at the computer right now:

1. **0:00** — open VSCode, open the `trading/` folder
2. **0:05** — open [forex-guide.md](_mkdocs/forex-guide.md), turn on preview (Cmd+Shift+V)
3. **0:10** — start reading. **Read sections 1–7** (the most important: what forex is, terminology, risk management). That's ~1.5 hours.
4. **1:30** — take a **30-minute break**. Don't try to read everything in one go.
5. **2:00** — continue with sections 8–14. Another ~1 hour.
6. **3:00** — open [docs/technical-analysis.md](_mkdocs/docs/technical-analysis.md). You don't need to understand everything on the first pass — **study the pictures**, read the captions.
7. **4:00** — take a look at [docs/strategy-details.md](_mkdocs/docs/strategy-details.md), without going deep yet.
8. **4:30** — run the position calculator once — just to see how it works:
   ```bash
   .venv/bin/python tools/position_calculator.py
   ```
9. **5:00** — close the computer. **Tomorrow**, re-read the main guide, then start picking a broker.

**Don't rush.** It's better to spend a week reading than two weeks fixing mistakes from rushing into a real account.

---

## 8. What NOT to do

- ❌ **Do not open a real account immediately** after reading. At least 2–3 months on demo.
- ❌ **Don't run `backtest.py` and think it's "a bot that trades for you"**. It's a history simulator, not a live auto-trader.
- ❌ **Do not edit `.venv/`** — that's a service folder.
- ❌ **Do not push the `journal/` folder with real trades publicly** to GitHub (it contains your personal stats). `.gitignore` is already set up to protect it, but double-check.
- ❌ **Do not believe promises of easy money** — not from bloggers, not from channels, not from "gurus."

---

## 9. If something doesn't work

### A script won't run — "command not found"
Check that you're in the `trading/` folder:

```bash
pwd
# should show: /Users/mukhammadamir/Sites/WORK/trading
```

If not — `cd /Users/mukhammadamir/Sites/WORK/trading`.

### Script says "No module named 'matplotlib'"
Run it through `.venv/bin/python`, not just `python` or `python3`:

```bash
# ❌ This won't work:
python tools/position_calculator.py

# ✅ This works:
.venv/bin/python tools/position_calculator.py
```

### Images in Markdown aren't displaying
Open the Markdown through **VSCode preview** (Cmd+Shift+V) or upload the folder to GitHub.

### `position_calculator.py` says "no such pair"
Majors are supported. Full list:

```bash
.venv/bin/python tools/position_calculator.py --list-pairs
```

---

## 10. Summary

You have:

- 🎓 **A textbook in 4 Markdown files** (~1500 lines of theory with pictures)
- 📝 **A ready-made journal template** in two formats
- 🧮 **A position size calculator** for every trade
- 📊 **A backtester** to test the strategy on history
- 🖼️ **12 educational charts** styled like a real trading terminal

About 25 files total. It's a **self-sufficient course**: you can learn without buying any paid courses.

**The main rule:** don't rush. 6 months on demo → then a small real account → then gradual growth. You have everything you need. The rest is just your discipline.

---

📖 Next step → open [forex-guide.md](_mkdocs/forex-guide.md) and start reading.
