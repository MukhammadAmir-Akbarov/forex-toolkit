#!/usr/bin/env python3
"""
Streamlit-приложение для интерактивного бэктеста.

Запуск:
  pip install streamlit
  streamlit run advanced/streamlit_app.py

Откроется веб-страница со слайдерами:
  - Выбрать параметры стратегии
  - Запустить бэктест
  - Увидеть статистику и equity curve в реальном времени
"""
from __future__ import annotations

import sys
from pathlib import Path

try:
    import streamlit as st
except ImportError:
    print("Установи: pip install streamlit")
    sys.exit(1)

import numpy as np
import pandas as pd
import plotly.graph_objects as go

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "bot"))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from strategy import detect_signals, prepare_dataframe  # noqa: E402
from strategies import breakout, mean_reversion, three_soldiers  # noqa: E402

st.set_page_config(page_title="Forex Backtest", page_icon="📊", layout="wide")
st.title("📊 Forex Backtest Dashboard")
st.caption("Интерактивный бэктест стратегий — изменяй параметры, "
           "смотри результат в реальном времени")


# === Сайдбар с параметрами ===
with st.sidebar:
    st.header("⚙️ Параметры")
    strategy_name = st.selectbox(
        "Стратегия",
        ["EMA50 Pullback", "Mean Reversion", "Breakout", "Three Soldiers"],
    )
    bars = st.slider("Свечей в выборке", 500, 5000, 2000, 100)
    rr = st.slider("R:R", 1.0, 5.0, 2.0, 0.1)
    seed = st.number_input("Random seed", 0, 9999, 42)
    risk = st.slider("Риск на сделку (%)", 0.1, 5.0, 1.0, 0.1)


# === Генерация данных ===
@st.cache_data
def generate_data(bars: int, seed: int) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    times = pd.date_range("2025-01-01", periods=bars, freq="h")
    closes = [1.08]
    for i in range(bars - 1):
        phase = (i % 1500) / 1500
        if phase < 0.35:
            drift = 0.0002
        elif phase < 0.55:
            drift = 0.0
        elif phase < 0.85:
            drift = -0.00015
        else:
            drift = 0.0
        closes.append(closes[-1] + rng.normal(drift, 0.001))
    closes = np.array(closes)
    opens = np.concatenate([[closes[0]], closes[:-1]])
    highs = np.maximum(opens, closes) + rng.uniform(0.0001, 0.001, bars)
    lows = np.minimum(opens, closes) - rng.uniform(0.0001, 0.001, bars)
    return pd.DataFrame({
        "open": opens, "high": highs, "low": lows, "close": closes,
    }, index=times)


df = generate_data(bars, seed)
df_indicators = prepare_dataframe(df)


# === Запуск стратегии ===
@st.cache_data
def run_strategy(df_hash: int, strategy: str, rr_val: float) -> list:
    if strategy == "EMA50 Pullback":
        return detect_signals(df_indicators, rr=rr_val)
    elif strategy == "Mean Reversion":
        return mean_reversion.detect(df, rr=rr_val)
    elif strategy == "Breakout":
        return breakout.detect(df, rr=rr_val)
    elif strategy == "Three Soldiers":
        return three_soldiers.detect(df, rr=rr_val)
    return []


signals = run_strategy(bars + seed, strategy_name, rr)


# === Симуляция сделок ===
def simulate(df, signals, max_bars=30):
    trades = []
    busy = -1
    for s in signals:
        if s.bar_index <= busy:
            continue
        risk_unit = abs(s.entry - s.stop)
        if risk_unit == 0:
            continue
        end = min(s.bar_index + max_bars, len(df) - 1)
        exit_idx, exit_price, outcome = end, df.iloc[end]["close"], "timeout"
        for j in range(s.bar_index + 1, end + 1):
            h, lo = df.iloc[j]["high"], df.iloc[j]["low"]
            direction = s.direction.value if hasattr(s.direction, "value") else s.direction
            if direction == "long":
                if lo <= s.stop:
                    exit_idx, exit_price, outcome = j, s.stop, "loss"; break
                if h >= s.take:
                    exit_idx, exit_price, outcome = j, s.take, "win"; break
            else:
                if h >= s.stop:
                    exit_idx, exit_price, outcome = j, s.stop, "loss"; break
                if lo <= s.take:
                    exit_idx, exit_price, outcome = j, s.take, "win"; break
        direction = s.direction.value if hasattr(s.direction, "value") else s.direction
        if direction == "long":
            pnl = (exit_price - s.entry) / risk_unit
        else:
            pnl = (s.entry - exit_price) / risk_unit
        trades.append({
            "entry_time": s.timestamp, "exit_time": df.index[exit_idx],
            "direction": direction, "outcome": outcome, "pnl_r": pnl,
        })
        busy = exit_idx
    return trades


trades = simulate(df, signals)
wins = [t for t in trades if t["outcome"] == "win"]
losses = [t for t in trades if t["outcome"] == "loss"]

# === Метрики ===
col1, col2, col3, col4 = st.columns(4)
col1.metric("Сделок", len(trades))
col2.metric(
    "Win rate",
    f"{len(wins)/len(trades)*100:.1f}%" if trades else "—",
)
if trades:
    gross_win = sum(t["pnl_r"] for t in wins) if wins else 0
    gross_loss = -sum(t["pnl_r"] for t in losses) if losses else 0
    pf = gross_win / gross_loss if gross_loss > 0 else 0
    total_r = sum(t["pnl_r"] for t in trades)
    col3.metric("Profit Factor", f"{pf:.2f}")
    col4.metric("Итого", f"{total_r:+.1f}R", f"{total_r * risk:+.2f}%")
else:
    col3.metric("Profit Factor", "—")
    col4.metric("Итого", "—")


# === Equity curve ===
st.subheader("📈 Equity curve")
if trades:
    cum = np.cumsum([t["pnl_r"] for t in trades])
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=list(range(len(cum))), y=cum,
        mode="lines", name="Equity",
        line=dict(color="#3b82f6", width=2.5),
        fill="tozeroy", fillcolor="rgba(59,130,246,0.1)",
    ))
    fig.add_hline(y=0, line_dash="dash", line_color="black")
    fig.update_layout(
        height=400,
        xaxis_title="Номер сделки",
        yaxis_title="Кумулятивный результат (R)",
        showlegend=False,
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Сделок нет — измени параметры")


# === Таблица сделок ===
st.subheader("📋 Сделки")
if trades:
    trades_df = pd.DataFrame(trades)
    trades_df["pnl_r"] = trades_df["pnl_r"].round(2)
    st.dataframe(trades_df.tail(50), use_container_width=True)


# === Ценовой график ===
st.subheader("📊 Ценовой график с сигналами")
fig = go.Figure()
fig.add_trace(go.Candlestick(
    x=df.index, open=df["open"], high=df["high"],
    low=df["low"], close=df["close"],
    name="Price",
))
# Маркеры сигналов
for s in signals[-50:]:
    direction = s.direction.value if hasattr(s.direction, "value") else s.direction
    color = "green" if direction == "long" else "red"
    fig.add_annotation(
        x=s.timestamp, y=s.entry,
        text="▲" if direction == "long" else "▼",
        showarrow=False, font=dict(size=14, color=color),
    )
fig.update_layout(height=500, xaxis_rangeslider_visible=False)
st.plotly_chart(fig, use_container_width=True)

st.caption(
    "Данные синтетические — для иллюстрации работы стратегии. "
    "Изменяй параметры в сайдбаре, чтобы увидеть, как меняется результат."
)
