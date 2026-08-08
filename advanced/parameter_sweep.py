#!/usr/bin/env python3
"""
Parameter Sweep — автоматический подбор параметров стратегии.

Тестирует все комбинации параметров на сетке, находит «оптимальные»,
проверяет их через walk-forward (чтобы не было переобучения).

⚠️ ВНИМАНИЕ: «Оптимальные» параметры на истории — НЕ гарантия будущего.
Это инструмент для понимания, какие диапазоны параметров устойчивы.
"""

from __future__ import annotations

import argparse
import itertools
import sys
from dataclasses import dataclass
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "bot"))
from strategy import detect_signals, prepare_dataframe  # noqa: E402


@dataclass
class SweepResult:
    params: dict
    total_r: float
    win_rate: float
    profit_factor: float
    n_trades: int
    max_dd: float


def simulate(df: pd.DataFrame, signals, max_bars: int = 30) -> list[float]:
    """Возвращает список R-результатов сделок."""
    results = []
    busy = -1
    for s in signals:
        if s.bar_index <= busy:
            continue
        risk = abs(s.entry - s.stop)
        if risk == 0:
            continue
        end = min(s.bar_index + max_bars, len(df) - 1)
        exit_price = df.iloc[end]["close"]
        outcome = "timeout"
        exit_idx = end
        for j in range(s.bar_index + 1, end + 1):
            high, low = df.iloc[j]["high"], df.iloc[j]["low"]
            if s.direction.value == "long":
                if low <= s.stop:
                    exit_idx, exit_price, outcome = j, s.stop, "loss"
                    break
                if high >= s.take:
                    exit_idx, exit_price, outcome = j, s.take, "win"
                    break
            else:
                if high >= s.stop:
                    exit_idx, exit_price, outcome = j, s.stop, "loss"
                    break
                if low <= s.take:
                    exit_idx, exit_price, outcome = j, s.take, "win"
                    break
        if s.direction.value == "long":
            pnl = (exit_price - s.entry) / risk
        else:
            pnl = (s.entry - exit_price) / risk
        results.append(pnl)
        busy = exit_idx
    return results


def evaluate(df: pd.DataFrame, params: dict) -> SweepResult:
    """Прогоняет стратегию с заданными параметрами.

    ``pip_size`` необязателен и по умолчанию прежний — 0.0001. Он нужен для пар
    с иеной, где пункт равен 0.01, то есть в сто раз крупнее. Без него фильтр
    «цена в пределах N пунктов от EMA» считается в стократно завышенных
    единицах и почти не срабатывает: на USD/JPY выходило 4 сделки за два года,
    на GBP/JPY — ноль. Это выглядело как «стратегия не работает на иене», хотя
    было ошибкой измерения.
    """
    df_prep = prepare_dataframe(df)
    signals = detect_signals(
        df_prep,
        rr=params["rr"],
        stop_buffer_pips=params["stop_buffer"],
        ema_distance_pips=params["ema_dist"],
        pip_size=params.get("pip_size", 0.0001),
        rsi_long_range=(params["rsi_low"], params["rsi_high"]),
        rsi_short_range=(35, 60),
    )
    pnls = simulate(df, signals)
    if not pnls:
        return SweepResult(params, 0, 0, 0, 0, 0)

    wins = [p for p in pnls if p > 0]
    losses = [p for p in pnls if p < 0]
    pf = sum(wins) / -sum(losses) if losses else (99 if wins else 0)
    win_rate = len(wins) / len(pnls) * 100

    equity = np.cumsum(pnls)
    peak = -np.inf
    max_dd = 0
    for e in equity:
        peak = max(peak, e)
        max_dd = max(max_dd, peak - e)

    return SweepResult(
        params=params,
        total_r=sum(pnls),
        win_rate=win_rate,
        profit_factor=pf,
        n_trades=len(pnls),
        max_dd=max_dd,
    )


def grid_search(df: pd.DataFrame, param_grid: dict) -> list[SweepResult]:
    """Полный перебор сетки параметров."""
    keys = list(param_grid.keys())
    combinations = list(itertools.product(*[param_grid[k] for k in keys]))

    print(f"Параметров для теста: {len(combinations)}")
    results = []
    for i, combo in enumerate(combinations, 1):
        params = dict(zip(keys, combo))
        result = evaluate(df, params)
        results.append(result)
        if i % 10 == 0 or i == len(combinations):
            print(
                f"  Прогресс: {i}/{len(combinations)} "
                f"({i / len(combinations) * 100:.0f}%)"
            )
    return results


def find_robust(results: list[SweepResult], min_trades: int = 30) -> SweepResult:
    """Лучшие параметры из тех, что дали достаточно сделок."""
    qualified = [r for r in results if r.n_trades >= min_trades]
    if not qualified:
        return max(results, key=lambda r: r.total_r)

    # Сортируем по Profit Factor, но штрафуем за маленькое кол-во сделок
    qualified.sort(
        key=lambda r: r.profit_factor * np.log(r.n_trades + 1),
        reverse=True,
    )
    return qualified[0]


def plot_heatmap(
    results: list[SweepResult], param_x: str, param_y: str, metric: str, out_path: Path
) -> None:
    """Heatmap по двум параметрам, остальные усредняются."""
    df = pd.DataFrame(
        [
            {
                **r.params,
                "total_r": r.total_r,
                "pf": r.profit_factor,
                "win_rate": r.win_rate,
                "n_trades": r.n_trades,
            }
            for r in results
        ]
    )

    pivot = df.pivot_table(
        index=param_y,
        columns=param_x,
        values=metric,
        aggfunc="mean",
    )

    fig, ax = plt.subplots(figsize=(10, 7))
    im = ax.imshow(pivot.values, cmap="RdYlGn", aspect="auto")

    ax.set_xticks(range(len(pivot.columns)))
    ax.set_yticks(range(len(pivot.index)))
    ax.set_xticklabels(pivot.columns)
    ax.set_yticklabels(pivot.index)
    ax.set_xlabel(param_x)
    ax.set_ylabel(param_y)
    ax.set_title(
        f"Heatmap: {metric} по {param_x} × {param_y}", fontsize=12, weight="bold"
    )

    for i in range(len(pivot.index)):
        for j in range(len(pivot.columns)):
            v = pivot.values[i, j]
            if not pd.isna(v):
                ax.text(j, i, f"{v:.2f}", ha="center", va="center", fontsize=9)

    fig.colorbar(im, ax=ax, label=metric)
    plt.tight_layout()
    plt.savefig(out_path, dpi=130)
    plt.close()


def main() -> int:
    parser = argparse.ArgumentParser(description="Parameter sweep")
    parser.add_argument(
        "--csv",
        type=Path,
        default=Path(__file__).resolve().parent.parent / "data" / "EURUSD_1h.csv",
    )
    parser.add_argument("--out", type=Path, default=Path("sweep-heatmap.png"))
    args = parser.parse_args()

    if not args.csv.exists():
        print(f"Файл {args.csv} не найден.")
        print("Сначала скачай данные: .venv/bin/python advanced/data_downloader.py")
        return 1

    print(f"Загружаю {args.csv}...")
    df = pd.read_csv(args.csv)
    if "datetime" in df.columns:
        df["datetime"] = pd.to_datetime(df["datetime"], utc=True)
        df = df.set_index("datetime")
    df = df[["open", "high", "low", "close"]].astype(float)
    print(f"  {len(df)} свечей")

    # Сетка параметров
    param_grid = {
        "rr": [1.5, 2.0, 2.5, 3.0],
        "stop_buffer": [3, 5, 7],
        "ema_dist": [5, 10, 15, 20],
        "rsi_low": [35, 40, 45],
        "rsi_high": [60, 65, 70],
    }

    print(f"\nСетка параметров:")
    total = 1
    for k, v in param_grid.items():
        print(f"  {k}: {v} ({len(v)} значений)")
        total *= len(v)
    print(f"\nВсего комбинаций: {total}")

    results = grid_search(df, param_grid)

    print("\n" + "=" * 70)
    print("  ТОП-10 ПО PROFIT FACTOR (с минимум 20 сделок)")
    print("=" * 70)
    qualified = [r for r in results if r.n_trades >= 20]
    qualified.sort(key=lambda r: r.profit_factor, reverse=True)

    print(
        f"\n{'RR':<6}{'SB':<5}{'ED':<5}{'RSI':<10}"
        f"{'N':<7}{'WR':<8}{'PF':<8}{'Итого':<8}{'DD':<7}"
    )
    print("─" * 70)
    for r in qualified[:10]:
        p = r.params
        rsi = f"{p['rsi_low']}-{p['rsi_high']}"
        print(
            f"{p['rr']:<6}{p['stop_buffer']:<5}{p['ema_dist']:<5}"
            f"{rsi:<10}{r.n_trades:<7}"
            f"{r.win_rate:<6.1f}%  {r.profit_factor:<6.2f}  "
            f"{r.total_r:+6.1f}R  {r.max_dd:5.1f}R"
        )

    # Лучший «робастный»
    robust = find_robust(results, min_trades=30)
    print("\n" + "=" * 70)
    print("  РОБАСТНЫЕ ПАРАМЕТРЫ (PF × log(N))")
    print("=" * 70)
    print(f"  Параметры: {robust.params}")
    print(f"  N сделок:  {robust.n_trades}")
    print(f"  Win rate:  {robust.win_rate:.1f}%")
    print(f"  PF:        {robust.profit_factor:.2f}")
    print(f"  Total:     {robust.total_r:+.1f}R")
    print(f"  Max DD:    {robust.max_dd:.1f}R")

    # Heatmap
    plot_heatmap(results, "rr", "ema_dist", "profit_factor", args.out)
    print(f"\nHeatmap: {args.out}")

    print("\n" + "─" * 70)
    print("⚠️  ВАЖНО:")
    print("  • «Лучшие» параметры на истории — НЕ гарантия будущего.")
    print("  • Это переобучение (overfitting), если у тебя только 1 набор данных.")
    print("  • Проверяй найденные параметры через walk-forward optimization.")
    print("  • Используй полученные знания, чтобы понять, в каких ЗОНАХ")
    print("    параметры устойчивы — а не точечные оптимумы.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
