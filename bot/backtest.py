#!/usr/bin/env python3
"""
Бэктестер для стратегии «Откат к EMA50 по тренду».

ЭТО НЕ ЖИВОЙ ТОРГОВЫЙ БОТ. Этот скрипт:
  1. Читает исторические OHLC данные (CSV) ИЛИ генерирует синтетические
  2. Применяет стратегию из strategy.py
  3. Считает статистику (win rate, profit factor, drawdown, equity curve)
  4. Строит график результатов

Запуск:
  python backtest.py                    # на синтетических данных
  python backtest.py --csv data.csv     # на своих данных

Формат CSV: колонки datetime,open,high,low,close (можно volume)
"""
from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass, field
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from strategy import Direction, Signal, detect_signals, prepare_dataframe


@dataclass
class Trade:
    entry_time: pd.Timestamp
    exit_time: pd.Timestamp
    direction: str
    entry: float
    stop: float
    take: float
    exit_price: float
    outcome: str          # "win" | "loss" | "timeout"
    pnl_pips: float
    pnl_r: float           # в единицах риска
    reason: str
    bars_held: int


# ---------- Risk Guardian (anti-tilt) ----------

@dataclass
class RiskGuardian:
    """
    Защита от тильта: блокирует новые сделки, если

      • подряд проиграно `max_consecutive_losses` сделок, или
      • дневной P&L опустился ниже `-daily_loss_limit_r` (в R).

    После триггера дневного лимита торговля возобновляется на следующий день.
    После триггера серии убытков — после первой выигрышной сделки счётчик
    обнуляется (то есть нужно дождаться нового дня и одной хорошей сделки).
    """
    max_consecutive_losses: int = 3
    daily_loss_limit_r: float = 2.0
    consecutive_losses: int = 0
    blocked_signals: int = 0
    triggered_dates: list[pd.Timestamp] = field(default_factory=list)
    _daily_pnl: dict = field(default_factory=dict)
    _last_block_reason: str = ""

    def should_block(self, ts: pd.Timestamp) -> bool:
        """Проверка ДО открытия сделки. True = пропустить сигнал."""
        date_key = pd.Timestamp(ts).normalize()
        daily = self._daily_pnl.get(date_key, 0.0)

        if self.consecutive_losses >= self.max_consecutive_losses:
            self._last_block_reason = (
                f"{self.consecutive_losses} убытков подряд — "
                f"торговля на паузе до выигрыша"
            )
            self.blocked_signals += 1
            self._record_trigger(date_key)
            return True

        if daily <= -abs(self.daily_loss_limit_r):
            self._last_block_reason = (
                f"дневной лимит -{self.daily_loss_limit_r}R исчерпан "
                f"({daily:+.2f}R) — пауза до завтра"
            )
            self.blocked_signals += 1
            self._record_trigger(date_key)
            return True

        return False

    def record_trade(self, ts: pd.Timestamp, pnl_r: float, outcome: str) -> None:
        """Регистрируем результат сделки ПОСЛЕ её закрытия."""
        date_key = pd.Timestamp(ts).normalize()
        self._daily_pnl[date_key] = self._daily_pnl.get(date_key, 0.0) + pnl_r

        if outcome == "loss":
            self.consecutive_losses += 1
        elif outcome == "win":
            self.consecutive_losses = 0
        # timeout не сбрасывает и не наращивает счётчик

    def _record_trigger(self, date_key: pd.Timestamp) -> None:
        if not self.triggered_dates or self.triggered_dates[-1] != date_key:
            self.triggered_dates.append(date_key)

    @property
    def last_block_reason(self) -> str:
        return self._last_block_reason


def simulate(
    df: pd.DataFrame,
    signals: list[Signal],
    max_bars_in_trade: int = 24,
    pip_size: float = 0.0001,
    spread_pips: float = 0.0,
    risk_guardian: RiskGuardian | None = None,
) -> list[Trade]:
    """
    Прогон сделок по сигналам.
    Правило: сделка закрывается по SL, TP, или после max_bars_in_trade свечей.
    Симулятор НЕ открывает новую сделку, пока есть открытая.

    Аргументы реализма:
      spread_pips   — суммарный спред (в пипсах), вычитается из PnL каждой
                      сделки. 0 = идеальная цена (по умолчанию для совместимости).
      risk_guardian — экземпляр RiskGuardian для anti-tilt защиты.
                      None = ограничений нет (по умолчанию).
    """
    trades: list[Trade] = []
    open_until_idx = -1

    for sig in signals:
        if sig.bar_index <= open_until_idx:
            continue  # пропускаем — позиция ещё открыта

        if risk_guardian is not None and risk_guardian.should_block(sig.timestamp):
            continue  # anti-tilt: пропускаем сигнал

        risk_per_unit = abs(sig.entry - sig.stop)
        if risk_per_unit == 0:
            continue

        # Прогоняем последующие свечи
        end_idx = min(sig.bar_index + max_bars_in_trade, len(df) - 1)
        exit_idx = end_idx
        exit_price = df.iloc[end_idx]["close"]
        outcome = "timeout"

        for j in range(sig.bar_index + 1, end_idx + 1):
            high = df.iloc[j]["high"]
            low = df.iloc[j]["low"]

            if sig.direction == Direction.LONG:
                # На свече касается стопа или тейка? Считаем приоритетом стоп
                hit_stop = low <= sig.stop
                hit_take = high >= sig.take
                if hit_stop and hit_take:
                    # Консервативно: считаем, что стоп сработал первым
                    exit_idx, exit_price, outcome = j, sig.stop, "loss"
                    break
                if hit_stop:
                    exit_idx, exit_price, outcome = j, sig.stop, "loss"
                    break
                if hit_take:
                    exit_idx, exit_price, outcome = j, sig.take, "win"
                    break
            else:  # SHORT
                hit_stop = high >= sig.stop
                hit_take = low <= sig.take
                if hit_stop and hit_take:
                    exit_idx, exit_price, outcome = j, sig.stop, "loss"
                    break
                if hit_stop:
                    exit_idx, exit_price, outcome = j, sig.stop, "loss"
                    break
                if hit_take:
                    exit_idx, exit_price, outcome = j, sig.take, "win"
                    break

        # PnL (с учётом спреда: вычитаем стоимость спреда из движения цены)
        if sig.direction == Direction.LONG:
            pnl_pips = (exit_price - sig.entry) / pip_size - spread_pips
        else:
            pnl_pips = (sig.entry - exit_price) / pip_size - spread_pips

        pnl_r = pnl_pips / (risk_per_unit / pip_size)

        trade = Trade(
            entry_time=sig.timestamp,
            exit_time=df.index[exit_idx],
            direction=sig.direction.value,
            entry=sig.entry,
            stop=sig.stop,
            take=sig.take,
            exit_price=exit_price,
            outcome=outcome,
            pnl_pips=pnl_pips,
            pnl_r=pnl_r,
            reason=sig.reason,
            bars_held=exit_idx - sig.bar_index,
        )
        trades.append(trade)
        open_until_idx = exit_idx

        if risk_guardian is not None:
            risk_guardian.record_trade(trade.exit_time, pnl_r, outcome)

    return trades


def stats(trades: list[Trade]) -> dict:
    """Считает основные метрики стратегии."""
    if not trades:
        return {"total": 0}

    wins = [t for t in trades if t.outcome == "win"]
    losses = [t for t in trades if t.outcome == "loss"]
    timeouts = [t for t in trades if t.outcome == "timeout"]

    total_r = sum(t.pnl_r for t in trades)
    gross_win = sum(t.pnl_r for t in trades if t.pnl_r > 0)
    gross_loss = -sum(t.pnl_r for t in trades if t.pnl_r < 0)

    # Equity curve в R
    equity = np.cumsum([t.pnl_r for t in trades])
    drawdowns = []
    peak = -np.inf
    for e in equity:
        peak = max(peak, e)
        drawdowns.append(peak - e)
    max_dd = max(drawdowns) if drawdowns else 0

    return {
        "total": len(trades),
        "wins": len(wins),
        "losses": len(losses),
        "timeouts": len(timeouts),
        "win_rate": len(wins) / len(trades) if trades else 0,
        "avg_win_r": np.mean([t.pnl_r for t in wins]) if wins else 0,
        "avg_loss_r": np.mean([t.pnl_r for t in losses]) if losses else 0,
        "profit_factor": gross_win / gross_loss if gross_loss > 0 else float("inf"),
        "expectancy_r": total_r / len(trades),
        "total_r": total_r,
        "max_drawdown_r": max_dd,
    }


def print_report(s: dict) -> None:
    print()
    print("╭" + "─" * 50 + "╮")
    print("│  РЕЗУЛЬТАТЫ БЭКТЕСТА" + " " * 28 + "│")
    print("╰" + "─" * 50 + "╯")
    print()
    if s["total"] == 0:
        print("Сделок нет.")
        return
    print(f"  Всего сделок:         {s['total']}")
    print(f"  Прибыльных (win):     {s['wins']}")
    print(f"  Убыточных (loss):     {s['losses']}")
    print(f"  Закрытых по времени:  {s['timeouts']}")
    print()
    print(f"  Win rate:             {s['win_rate']*100:.1f}%")
    print(f"  Средний win:          {s['avg_win_r']:+.2f}R")
    print(f"  Средний loss:         {s['avg_loss_r']:+.2f}R")
    print(f"  Profit Factor:        {s['profit_factor']:.2f}")
    print(f"  Expectancy:           {s['expectancy_r']:+.2f}R / сделку")
    print(f"  Итого:                {s['total_r']:+.2f}R")
    print(f"  Макс. просадка:       {s['max_drawdown_r']:.2f}R")
    print()
    # Интерпретация
    pf = s["profit_factor"]
    if pf >= 1.5:
        print("  ✅ Profit Factor ≥ 1.5 — статистика подходящая для дальнейшего теста.")
    elif pf >= 1.2:
        print("  ⚠️  Profit Factor 1.2–1.5 — стратегия на грани, нужна доработка.")
    else:
        print("  ❌ Profit Factor < 1.2 — стратегия в текущем виде убыточна.")
    print()


def plot_equity(trades: list[Trade], out_path: Path) -> None:
    """Рисует equity curve (в единицах R)."""
    if not trades:
        return
    pnl_r = [t.pnl_r for t in trades]
    equity = np.cumsum(pnl_r)
    times = [t.exit_time for t in trades]

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8),
                                    gridspec_kw={"height_ratios": [2, 1]},
                                    sharex=True)
    ax1.plot(times, equity, color="#2563eb", linewidth=2)
    ax1.fill_between(times, equity, 0,
                     where=(np.array(equity) >= 0),
                     color="#10b981", alpha=0.2)
    ax1.fill_between(times, equity, 0,
                     where=(np.array(equity) < 0),
                     color="#ef4444", alpha=0.2)
    ax1.axhline(0, color="black", linewidth=0.8)
    ax1.set_ylabel("Equity (R)")
    ax1.set_title("Equity curve — кумулятивный результат в единицах риска",
                  fontsize=12, weight="bold")
    ax1.grid(True, alpha=0.3)

    colors = ["#10b981" if r > 0 else "#ef4444" for r in pnl_r]
    ax2.bar(times, pnl_r, color=colors, width=pd.Timedelta(hours=2))
    ax2.axhline(0, color="black", linewidth=0.8)
    ax2.set_ylabel("P&L сделки (R)")
    ax2.set_xlabel("Время")
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(out_path, dpi=130)
    plt.close()
    print(f"  График сохранён: {out_path}")


def generate_synthetic_data(
    bars: int = 2000,
    seed: int = 42,
    start_price: float = 1.08,
) -> pd.DataFrame:
    """Генерирует синтетический H1-ряд с волнообразным трендом."""
    rng = np.random.default_rng(seed)
    times = pd.date_range("2026-01-01", periods=bars, freq="h")

    # Цикличный тренд: 800 свечей вверх, 800 вниз, 400 флэт
    closes = [start_price]
    for i in range(bars - 1):
        phase = (i % 2000) / 2000
        if phase < 0.4:
            drift = 0.00015
        elif phase < 0.8:
            drift = -0.00012
        else:
            drift = 0.0
        closes.append(closes[-1] + rng.normal(drift, 0.0008))

    closes = np.array(closes)
    opens = np.concatenate([[closes[0]], closes[:-1]])
    highs = np.maximum(opens, closes) + rng.uniform(0.0001, 0.001, bars)
    lows = np.minimum(opens, closes) - rng.uniform(0.0001, 0.001, bars)

    return pd.DataFrame({
        "open": opens, "high": highs, "low": lows, "close": closes,
    }, index=times)


def load_csv(path: Path) -> pd.DataFrame:
    """Загружает OHLC из CSV. Ожидаемые колонки: datetime,open,high,low,close."""
    df = pd.read_csv(path)
    if "datetime" in df.columns:
        df["datetime"] = pd.to_datetime(df["datetime"], utc=True)
        df = df.set_index("datetime")
    elif "time" in df.columns:
        df["time"] = pd.to_datetime(df["time"], utc=True)
        df = df.set_index("time")
    else:
        df.index = pd.to_datetime(df.iloc[:, 0], utc=True)
        df = df.iloc[:, 1:]
    required = {"open", "high", "low", "close"}
    if not required.issubset(df.columns):
        raise ValueError(f"CSV должен содержать колонки {required}")
    return df[["open", "high", "low", "close"]].astype(float)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Бэктестер стратегии EMA50 pullback",
    )
    parser.add_argument("--csv", type=Path,
                        help="CSV с OHLC данными (опц.). "
                             "Без него — синтетические данные.")
    parser.add_argument("--rr", type=float, default=2.0,
                        help="Risk/Reward соотношение (по умолч. 2.0)")
    parser.add_argument("--out", type=Path,
                        default=Path("equity-curve.png"),
                        help="Путь для графика equity curve")
    parser.add_argument("--bars", type=int, default=2000,
                        help="Сколько синтетических свечей сгенерировать")
    parser.add_argument("--trades-csv", type=Path,
                        help="Сохранить список сделок в CSV")
    parser.add_argument("--spread-pips", type=float, default=0.0,
                        help="Спред брокера в пипсах (вычитается из PnL "
                             "каждой сделки). Реалистично: 1-3 для EUR/USD "
                             "на ECN, 2-5 на маркет-мейкере.")
    parser.add_argument("--max-consecutive-losses", type=int, default=0,
                        help="Anti-tilt: остановить торговлю после N "
                             "убытков подряд. 0 = выкл. (по умолч.). "
                             "Рекомендуется 3.")
    parser.add_argument("--daily-loss-limit-r", type=float, default=0.0,
                        help="Anti-tilt: дневной лимит потерь в R. "
                             "0 = выкл. (по умолч.). Рекомендуется 2.")
    args = parser.parse_args()

    if args.csv:
        print(f"Загружаю данные из {args.csv}…")
        df = load_csv(args.csv)
    else:
        print(f"Генерирую {args.bars} синтетических H1-свечей…")
        df = generate_synthetic_data(args.bars)

    print(f"Период: {df.index[0]} → {df.index[-1]} ({len(df)} свечей)")
    df = prepare_dataframe(df)

    print("Сканирую сигналы…")
    signals = detect_signals(df, rr=args.rr)
    print(f"  Найдено сигналов: {len(signals)}")

    guardian: RiskGuardian | None = None
    if args.max_consecutive_losses > 0 or args.daily_loss_limit_r > 0:
        guardian = RiskGuardian(
            max_consecutive_losses=(
                args.max_consecutive_losses
                if args.max_consecutive_losses > 0
                else 10**9
            ),
            daily_loss_limit_r=(
                args.daily_loss_limit_r
                if args.daily_loss_limit_r > 0
                else 10**9
            ),
        )
        print(
            f"  Risk Guardian активен: "
            f"max_losses={args.max_consecutive_losses or '∞'}, "
            f"daily_limit=-{args.daily_loss_limit_r or '∞'}R"
        )

    if args.spread_pips > 0:
        print(f"  Спред: {args.spread_pips} пипс/сделку")

    print("Прогоняю сделки…")
    trades = simulate(
        df,
        signals,
        spread_pips=args.spread_pips,
        risk_guardian=guardian,
    )
    print(f"  Реальных входов (без перекрытий): {len(trades)}")
    if guardian is not None:
        print(
            f"  Сигналов заблокировано Guardian: {guardian.blocked_signals} "
            f"(в {len(guardian.triggered_dates)} дн.)"
        )

    s = stats(trades)
    print_report(s)

    if trades:
        plot_equity(trades, args.out)

    if args.trades_csv:
        trades_df = pd.DataFrame([asdict(t) for t in trades])
        trades_df.to_csv(args.trades_csv, index=False)
        print(f"  Сделки сохранены: {args.trades_csv}")

    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
