# MT5 Setup Guide — Step-by-Step MetaTrader 5 Installation

## Step 1: Register with a Broker

1. Choose a regulated broker (see [extras/brokers-comparison.md](../extras/brokers-comparison.md))
2. On the broker's website → **"Open a Demo Account"** (not a real one!)
3. Fill in the form: name, email, phone number
4. You will receive **3 pieces of information** by email:
   - **Login** (e.g. 50123456)
   - **Password** (investor password — for viewing only; master password — for trading)
   - **Server** (e.g. `Exness-Demo` or `ICMarkets-Demo01`)

> ⚠️ Save these credentials. You will need them to log into MT5.

## Step 2: Download MT5

### macOS

MetaTrader 5 for Mac comes in two variants:

**Option A: native (recommended)**
1. Open your broker's website → **"Download MT5"** section → **Mac**
2. A `.dmg` file (~60 MB) will download
3. Open it → drag MT5 into Applications
4. Launch it → if macOS blocks it, allow it in System Settings

**Option B: via WINE (if the native version doesn't work)**
1. Download **MetaTrader 5** from metaquotes.net
2. Install Wine: `brew install --cask wine-stable`
3. Open the .exe file through Wine

### Windows
1. Broker's website → Download → Windows
2. Run the .exe → install

### Linux
1. WINE: `sudo apt install wine`
2. Download the Windows .exe → run it through Wine

## Step 3: First Login

1. Launch MT5
2. Menu: **File → Login to Trade Account**
3. Fill in:
   ```
   Login:    [your broker login]
   Password: [password]
   Server:   [server from the email]
   ```
4. Tick the **"Save account info"** checkbox
5. Click **Login**

✅ In the bottom-right corner you will see green numbers — balance, equity, margin.

## Step 4: Chart Setup

### Enable Candlestick Chart
- Right-click on the chart → **Candlesticks**
- Or click the "candles" button in the top toolbar

### Switch the Timeframe to H1
- Top toolbar: M1, M5, M15, M30, **H1**, H4, D1, W1
- Click **H1**

### Add EMA 50
1. **Insert → Indicators → Trend → Moving Average**
2. Parameters:
   - Period: **50**
   - MA method: **Exponential**
   - Apply to: **Close**
   - Style: colour — **blue**, thickness **2**
3. OK

### Add EMA 200
Repeat the same steps, but set Period = **200**, colour — **red**.

### Add RSI
1. **Insert → Indicators → Oscillators → Relative Strength Index**
2. Period: **14**
3. Apply to: **Close**
4. OK

### Save a Template
So you don't have to configure this every time:
- Right-click on the chart → **Templates → Save Template** → name it "MyTemplate"
- Next time: right-click → Templates → MyTemplate

## Step 5: Opening a Trade

### The Correct Way to Open a Trade (with SL/TP from the start)

1. Press **F9** (or click the "New Order" button in the top toolbar)
2. Order window:
   ```
   Symbol:        EURUSD
   Volume:        0.01     ← calculate using position_calculator.py!
   Stop Loss:     1.0827   ← mandatory!
   Take Profit:   1.0902   ← mandatory!
   Type:          Market Execution
   ```
3. Click **Buy by Market** (long) or **Sell by Market** (short)

### Common Mistakes

❌ **Opening without a SL** → Never. Enter a SL first.
❌ **Guessing the volume by eye** → use the calculator.
❌ **"Type: Pending"** → this is a pending order; you are waiting for the price to reach a level. You don't need this right now.

## Step 6: Checking the Trade

After opening, in the bottom panel under **Trade**:
```
Symbol  Type  Volume  Open Price  S/L      T/P      Profit
EURUSD  buy   0.01    1.08520    1.08270  1.09020  +$1.50
```

✓ S/L and T/P are **not empty** — protection is in place.

## Step 7: Closing a Trade

**Best option:** don't close manually. Wait for the SL or TP to be hit.

**If you need to close early** (exceptional circumstances only):
- Right-click on the trade in the bottom panel → **Close Order**

## Step 8: Trade Journal in MT5

MT5 keeps its own log automatically:
- Bottom panel → **History**
- You can see all closed trades with their results
- Export via: right-click → **Report → Save as Report (HTML)**

It is worth **also** copying this history into your own Markdown/CSV journal, because MT5 has no fields for "emotions", "did I follow the rules", etc.

## Step 9: Frequently Used Keyboard Shortcuts

| Key | Action |
|---|---|
| **F9** | Open New Order |
| **F8** | Chart properties |
| **F11** | Full-screen mode |
| **Ctrl+T** | Terminal panel at the bottom |
| **Ctrl+N** | Navigator window |
| **+** / **−** | Zoom in / out |
| **PageDown** | Jump to the latest candles |

## Step 10: Installing Our Expert Advisor

If you want to run our [EMA50Pullback.mq5](https://github.com/MukhammadAmir-Akbarov/forex-toolkit/blob/main/advanced/EMA50Pullback.mq5) on a demo account:

1. In MT5: **File → Open Data Folder**
2. Open the `MQL5/Experts/` folder
3. Copy the `EMA50Pullback.mq5` file there
4. In MT5: **View → Navigator** (Ctrl+N)
5. **Expert Advisors** section → right-click → **Refresh**
6. You will see `EMA50Pullback` → drag it onto the EUR/USD H1 chart
7. In the settings window:
   - ✅ **Allow live trading** (only if you want the EA to trade)
   - Set the parameters (Risk_Percent, Risk_Reward, etc.)
   - **OK**
8. In the top-right corner of the chart you will see 😀 (running) or ❌ (not running)

**⚠️ IMPORTANT:** The EA is protected by a "demo only" check. It will refuse to run on a live account.

## Step 11: Demo Account vs Live — Key Differences

| Feature | Demo | Live |
|---|---|---|
| Execution | Perfect | With slippage |
| Spread | Often tighter | Real, may widen |
| Emotions | None (virtual money) | Present (your problem) |
| Swaps | Sometimes simplified | Real |
| Requotes | None | Possible during high volatility |

## Step 12: First-Month Strategy on MT5

Week 1:
- Installation, getting familiar with the interface
- 5–10 trial trades with the minimum volume of 0.01 lot
- Test SL/TP — make sure they work

Weeks 2–4:
- Trade according to the strategy rules (1–3 trades per day)
- Keep a journal in parallel
- Use the calculator before every trade

## Additional Tips

### If the Terminal Freezes
- Close all unnecessary chart tabs
- Bottom-right corner: right-click → **Connect Status** → it should show "Connected"
- If not — reconnect via File → Login

### If Quotes Stop Updating
- Your broker may restrict quotes on weekends
- Check whether it is Saturday/Sunday (the market is closed)

### Backing Up Your Settings
- File → Open Data Folder → copy the `config/` folder
- In the future you can restore it by clicking "Restore"

---

## MT5 Trading Readiness Checklist

- [ ] MT5 is installed and connected to a demo account
- [ ] I can see my balance in the bottom-right corner
- [ ] EUR/USD H1 chart is set up with EMA 50, EMA 200, and RSI
- [ ] Template is saved
- [ ] I know how to open a trade with SL and TP
- [ ] I know how to view the trade history
- [ ] Position calculator is open
- [ ] Trade journal is open (Google Sheets or Markdown)
- [ ] Printed [checklist](../extras/checklist-printable.md) is on the desk

**All ☑ → ready for your first demo trade.**

---

[← Back to the main guide](../forex-guide.md)
