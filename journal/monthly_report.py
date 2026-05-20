#!/usr/bin/env python3
"""
Месячный отчёт по журналу — генерирует HTML с детальной аналитикой.

Запуск:
  python journal/monthly_report.py --month 2026-05
"""
from __future__ import annotations

import argparse
import csv
import sys
from datetime import datetime
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

JOURNAL = Path(__file__).resolve().parent / "my-trades.csv"


def load_trades(path: Path, month_filter: str | None = None) -> list[dict]:
    if not path.exists():
        return []
    with open(path, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    if month_filter:
        rows = [r for r in rows if r.get("date", "").startswith(month_filter)]
    return rows


def make_charts(trades: list[dict], out_dir: Path) -> dict:
    """Создаёт графики и возвращает пути к ним."""
    closed = [t for t in trades if t.get("outcome") in ("win", "loss", "be")]
    paths = {}
    if not closed:
        return paths

    # 1. Equity curve
    pnls = [float(t.get("result_usd", 0) or 0) for t in closed]
    cum = np.cumsum(pnls)
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(range(len(cum)), cum, color="#3b82f6", linewidth=2.5)
    ax.axhline(0, color="black", linewidth=0.8)
    ax.fill_between(range(len(cum)), cum, 0,
                    where=(cum >= 0), color="#10b981", alpha=0.2)
    ax.fill_between(range(len(cum)), cum, 0,
                    where=(cum < 0), color="#ef4444", alpha=0.2)
    ax.set_xlabel("Сделка")
    ax.set_ylabel("Кумулятивный P&L ($)")
    ax.set_title("Equity curve за месяц", fontsize=12, weight="bold")
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    eq_path = out_dir / "monthly-equity.png"
    plt.savefig(eq_path, dpi=130)
    plt.close()
    paths["equity"] = eq_path

    # 2. Win/Loss pie
    fig, ax = plt.subplots(figsize=(6, 6))
    wins = sum(1 for t in closed if t["outcome"] == "win")
    losses = sum(1 for t in closed if t["outcome"] == "loss")
    bes = sum(1 for t in closed if t["outcome"] == "be")
    labels = ["Win", "Loss"]
    sizes = [wins, losses]
    colors = ["#10b981", "#ef4444"]
    if bes > 0:
        labels.append("BE")
        sizes.append(bes)
        colors.append("#9ca3af")
    ax.pie(sizes, labels=labels, autopct="%1.0f%%", colors=colors,
           startangle=90)
    ax.set_title("Распределение исходов", fontsize=12, weight="bold")
    pie_path = out_dir / "monthly-pie.png"
    plt.savefig(pie_path, dpi=130, bbox_inches="tight")
    plt.close()
    paths["pie"] = pie_path

    # 3. По дням недели
    by_day = {}
    for t in closed:
        try:
            d = datetime.strptime(t["date"], "%Y-%m-%d")
            wd = d.strftime("%a")
            by_day.setdefault(wd, []).append(float(t.get("result_usd", 0) or 0))
        except Exception:
            continue

    if by_day:
        days_order = ["Mon", "Tue", "Wed", "Thu", "Fri"]
        days_show = [d for d in days_order if d in by_day]
        totals = [sum(by_day[d]) for d in days_show]

        fig, ax = plt.subplots(figsize=(8, 5))
        colors = ["#10b981" if v >= 0 else "#ef4444" for v in totals]
        ax.bar(days_show, totals, color=colors, edgecolor="black", alpha=0.7)
        ax.axhline(0, color="black", linewidth=0.8)
        ax.set_ylabel("P&L ($)")
        ax.set_title("Результаты по дням недели", fontsize=12, weight="bold")
        ax.grid(True, alpha=0.3)
        day_path = out_dir / "monthly-by-day.png"
        plt.savefig(day_path, dpi=130)
        plt.close()
        paths["by_day"] = day_path

    return paths


def generate_report(trades: list[dict], month: str, out_dir: Path) -> Path:
    closed = [t for t in trades if t.get("outcome") in ("win", "loss", "be")]
    wins = [t for t in closed if t["outcome"] == "win"]
    losses = [t for t in closed if t["outcome"] == "loss"]
    pnls = [float(t.get("result_usd", 0) or 0) for t in closed]
    win_pnls = [p for p in pnls if p > 0]
    loss_pnls = [p for p in pnls if p < 0]

    total = sum(pnls)
    win_rate = len(wins) / len(closed) * 100 if closed else 0
    pf = sum(win_pnls) / abs(sum(loss_pnls)) if loss_pnls else (
        99 if win_pnls else 0
    )
    avg_win = sum(win_pnls) / len(win_pnls) if win_pnls else 0
    avg_loss = sum(loss_pnls) / len(loss_pnls) if loss_pnls else 0

    charts = make_charts(trades, out_dir)

    html = f"""<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<title>Месячный отчёт {month}</title>
<style>
  body {{ font-family: -apple-system, BlinkMacSystemFont, sans-serif;
         background: #f9fafb; padding: 30px; color: #1f2937; }}
  h1 {{ color: #1e40af; }}
  .subtitle {{ color: #6b7280; margin-bottom: 24px; }}
  .grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; }}
  .card {{ background: white; padding: 16px; border-radius: 8px;
          box-shadow: 0 1px 3px rgba(0,0,0,0.08); }}
  .label {{ font-size: 11px; color: #6b7280; text-transform: uppercase; }}
  .value {{ font-size: 24px; font-weight: 700; margin-top: 4px; }}
  .green {{ color: #10b981; }}
  .red {{ color: #ef4444; }}
  .blue {{ color: #3b82f6; }}
  img {{ max-width: 100%; margin: 16px 0; border-radius: 8px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1); }}
  h2 {{ margin-top: 32px; color: #374151; }}
  table {{ width: 100%; background: white; border-collapse: collapse;
          border-radius: 8px; overflow: hidden; }}
  th {{ background: #1e40af; color: white; padding: 10px; text-align: left; }}
  td {{ padding: 8px 10px; border-bottom: 1px solid #e5e7eb; }}
</style>
</head>
<body>
<h1>📊 Месячный отчёт — {month}</h1>
<div class="subtitle">Сгенерирован {datetime.now().strftime("%Y-%m-%d %H:%M")}</div>

<div class="grid">
  <div class="card"><div class="label">Сделок</div>
    <div class="value blue">{len(closed)}</div></div>
  <div class="card"><div class="label">Win rate</div>
    <div class="value {'green' if win_rate >= 40 else 'red'}">{win_rate:.1f}%</div></div>
  <div class="card"><div class="label">Profit Factor</div>
    <div class="value {'green' if pf >= 1.5 else 'red'}">{pf:.2f}</div></div>
  <div class="card"><div class="label">Чистый P&L</div>
    <div class="value {'green' if total >= 0 else 'red'}">${total:+.2f}</div></div>
</div>

<h2>📈 Equity curve</h2>
{f'<img src="{charts["equity"].name}">' if "equity" in charts else "Нет данных"}

<h2>🎯 Распределение</h2>
{f'<img src="{charts["pie"].name}" style="max-width: 400px;">' if "pie" in charts else "Нет данных"}

<h2>📅 По дням недели</h2>
{f'<img src="{charts["by_day"].name}">' if "by_day" in charts else "Нет данных"}

<h2>📋 Все сделки месяца</h2>
<table>
<thead>
<tr><th>Дата</th><th>Пара</th><th>Dir</th><th>Вход</th><th>Исход</th><th>P&L $</th></tr>
</thead>
<tbody>
{chr(10).join(f"<tr><td>{t.get('date','')}</td><td>{t.get('pair','')}</td>"
              f"<td>{t.get('direction','')}</td><td>{t.get('entry','')}</td>"
              f"<td>{t.get('outcome','')}</td>"
              f"<td>${t.get('result_usd','')}</td></tr>" for t in closed)}
</tbody>
</table>

</body>
</html>"""

    out_path = out_dir / f"monthly-report-{month}.html"
    out_path.write_text(html, encoding="utf-8")
    return out_path


def main() -> int:
    parser = argparse.ArgumentParser(description="Месячный отчёт")
    parser.add_argument("--month", required=True, help="Например 2026-05")
    parser.add_argument("--csv", type=Path, default=JOURNAL)
    parser.add_argument("--out-dir", type=Path,
                        default=Path(__file__).resolve().parent.parent
                        / "journal-reports")
    args = parser.parse_args()

    args.out_dir.mkdir(parents=True, exist_ok=True)
    trades = load_trades(args.csv, args.month)
    if not trades:
        print(f"Нет сделок за {args.month} в {args.csv}")
        return 1

    out_file = generate_report(trades, args.month, args.out_dir)
    print(f"✓ Отчёт: {out_file}")
    print(f"  Открыть: open {out_file}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
