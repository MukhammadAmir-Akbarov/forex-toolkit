# Streamlit Setup Guide — interactive backtest in the browser

## What you get

Once launched you will have a **web page with sliders** where you can:
- Choose a strategy from a drop-down list
- Move the R:R, win rate, and candle-count sliders
- Instantly see the **updated** equity curve, metrics, and trade table
- A price chart with signal markers

This is far more convenient than re-running a Python script with different parameters each time.

## Step 1: Install Streamlit

```bash
cd /Users/mukhammadamir/Sites/WORK/trading
.venv/bin/pip install streamlit plotly
```

This installs Streamlit (~30 MB).

## Step 2: Launch

```bash
.venv/bin/streamlit run advanced/streamlit_app.py
```

What happens:
1. The terminal will display:
   ```
   You can now view your Streamlit app in your browser.
   Local URL: http://localhost:8501
   ```
2. **The browser opens automatically** at http://localhost:8501
3. If it did not open — navigate to the URL manually

## Step 3: Using the app

### Left panel (sidebar) — parameters

- **Strategy** — choose from 4 strategies
- **Candles in sample** — how many H1 candles to generate (more = more trades)
- **R:R** — Risk/Reward ratio (1.0–5.0)
- **Random seed** — for reproducibility (same number = same data)
- **Risk per trade** — used to calculate the final %

### Main page area

1. **Metrics** at the top (4 cards):
   - Trades
   - Win rate
   - Profit Factor
   - Total

2. **Equity curve** — interactive chart
   - Hover with the mouse to see exact values
   - Zoom is supported

3. **Trade table** — last 50 trades

4. **Candlestick price chart** — shows signal markers (▲ long, ▼ short)

## Step 4: Experiments

Try these:

### Experiment 1: Impact of R:R
- Move R:R from 1.0 to 5.0
- Watch how the final profit changes
- **Takeaway:** with a higher R:R fewer trades win, but each winner is more profitable

### Experiment 2: Comparing strategies
- Switch the strategy (EMA50 → Mean Reversion → Breakout → Three Soldiers)
- Same seed = same data
- **Takeaway:** which one performs best on this data?

### Experiment 3: Data dependency
- Change the random seed (1, 42, 100, 9999)
- The same strategy will produce **very different** results
- **Takeaway:** the outcome depends on luck + the amount of data

## Step 5: Stopping the app

Press **Ctrl+C** in the terminal — Streamlit will stop.

To restart — repeat Step 2.

## Running in the background (optional)

If you want Streamlit to keep running:

```bash
.venv/bin/streamlit run advanced/streamlit_app.py &
```

When you no longer need it:
```bash
pkill -f streamlit
```

## Access from another device (optional)

By default Streamlit is only visible on your own machine. To open it from a phone on the same Wi-Fi network:

```bash
.venv/bin/streamlit run advanced/streamlit_app.py --server.address 0.0.0.0
```

Then on your phone open:
```
http://<your-Mac-IP>:8501
```

To find your IP: `ifconfig | grep "inet 192"`

## Cloud deployment (advanced)

Streamlit Cloud (free) or Render / Railway:
1. Upload the project to GitHub
2. Sign up at streamlit.io/cloud
3. Connect your repository → select `advanced/streamlit_app.py`
4. You will receive a public URL

**⚠️** Do not publish a trade journal containing real trading data in a public repository.

## Troubleshooting

### `streamlit: command not found`
Launch via `.venv/bin/streamlit`, not just `streamlit`.

### Browser did not open
Open manually: http://localhost:8501

### Port 8501 is busy
```bash
.venv/bin/streamlit run advanced/streamlit_app.py --server.port 8502
```

### Streamlit crashes with an import error
Check that all dependencies are installed:
```bash
.venv/bin/pip install streamlit plotly pandas numpy matplotlib
```

### Charts are not updating
- Clear the cache: top-right corner of the page → menu → **Clear cache**
- Reload the page (Cmd+R)

## What's inside (for the curious)

The file [streamlit_app.py](https://github.com/MukhammadAmir-Akbarov/forex-toolkit/blob/main/advanced/streamlit_app.py) is a web app in ~150 lines of Python:
- `st.sidebar` — left panel
- `st.slider`, `st.selectbox` — controls
- `st.cache_data` — caching so the whole backtest is not recalculated on every change
- `plotly.graph_objects` — interactive charts
- Backtest logic is the same as in `bot/backtest.py`

You can edit the file and see changes immediately (Streamlit reloads the page automatically).

---

[← Back to the main guide](../forex-guide.md)
