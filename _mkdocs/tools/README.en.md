# Tools — utilities

| Script | Purpose |
|---|---|
| [`position_calculator.py`](https://github.com/MukhammadAmir-Akbarov/forex-toolkit/blob/main/tools/position_calculator.py) | Position size calculator (lots) based on risk management |
| [`margin_calculator.py`](https://github.com/MukhammadAmir-Akbarov/forex-toolkit/blob/main/tools/margin_calculator.py) | Margin calculator: how much of your deposit an open position will lock up |
| [`chart_generator.py`](https://github.com/MukhammadAmir-Akbarov/forex-toolkit/blob/main/tools/chart_generator.py) | Generating educational charts for the documentation |

## position_calculator.py

Calculates position size in lots based on your risk management settings.

### Interactive mode

```bash
.venv/bin/python tools/position_calculator.py
```

```
=== Position Size Calculator ===

Balance ($): 1000
Risk per trade (%, e.g. 0.5): 0.5
Stop-loss (in pips): 25
Pair (EURUSD / GBPUSD / USDJPY / ...): EURUSD

╭─────────────────────────────────────────╮
│  POSITION SIZE CALCULATOR               │
╰─────────────────────────────────────────╯

Input data:
  Balance:           $1,000.00
  Risk:              0.50% = $5.00
  Stop-loss:         25 pips
  Pair:              EURUSD
  Pip value:         $10.00 per 1 lot

Calculation:
  Size (exact):      0.0200 lots
  Size (rounded):    0.02 lots
  Actual risk:       $5.00 (0.50%)

→ Set in terminal: 0.02 lots
```

### One-line mode

```bash
.venv/bin/python tools/position_calculator.py --balance 1000 --risk 0.5 --stop 25 --pair EURUSD
```

### Parameters

| Flag | Meaning |
|---|---|
| `--balance` / `-b` | Deposit in USD |
| `--risk` / `-r` | Risk percentage (0.5 = 0.5%) |
| `--stop` / `-s` | Distance to stop-loss in pips |
| `--pair` / `-p` | Currency pair (EURUSD by default) |
| `--list-pairs` | Show the list of supported pairs |

### Rounding logic

The size is always rounded **down** to 0.01 (the minimum step for most brokers). This means the **actual risk is less** than planned, which is safer.

Minimum 0.01 lots. If the calculation yields less (small deposit + large stop), the script warns you: the actual risk may exceed the planned value.

### Warnings

- ⚠️ If actual risk > planned risk (due to rounding) — it will suggest reducing the position manually.
- ⚠️ If actual risk > 2% of deposit — a warning that this is a lot for a beginner.

---

## chart_generator.py

Generates PNG images for the documentation. It is run once — all images are already generated in `docs/images/`. Re-running is only needed if you want to change the visual style or add new illustrations.

```bash
.venv/bin/python tools/chart_generator.py
```

Creates:

- `candle-anatomy.png` — anatomy of a Japanese candlestick
- `candle-patterns.png` — hammer, engulfing, doji, shooting star
- `trend-types.png` — trend types (up / down / flat)
- `support-resistance.png` — support and resistance levels
- `ema-example.png` — EMA 50 and EMA 200
- `rsi-example.png` — RSI indicator
- `macd-example.png` — MACD indicator
- `bollinger-example.png` — Bollinger Bands
- `chart-patterns.png` — head and shoulders, triangle, double top
- `strategy-example.png` — strategy setup illustration
- `risk-reward.png` — win rate × R:R table
- `drawdown-math.png` — ruin math

All data is **synthetic** — for illustrating concepts, not real quotes.

---

[← Back to the main guide](../forex-guide.md)
