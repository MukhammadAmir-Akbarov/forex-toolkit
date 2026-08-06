#!/usr/bin/env python3
"""
HTML-дашборд для журнала сделок.

Читает CSV (journal/my-trades.csv или указанный) и генерирует
красивую веб-страницу со статистикой, equity curve и таблицей сделок.

Открыть в браузере: open journal-dashboard.html
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

from jinja2 import Template

TEMPLATE = """<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<title>Trading Journal Dashboard</title>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    background: #f3f4f6;
    color: #1f2937;
    padding: 24px;
  }
  h1 { color: #1e40af; margin-bottom: 8px; }
  .subtitle { color: #6b7280; margin-bottom: 24px; font-size: 14px; }
  .grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 16px;
    margin-bottom: 24px;
  }
  .card {
    background: white;
    padding: 18px;
    border-radius: 8px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.08);
  }
  .card .label {
    font-size: 12px;
    color: #6b7280;
    text-transform: uppercase;
    margin-bottom: 8px;
  }
  .card .value {
    font-size: 28px;
    font-weight: 700;
  }
  .green { color: #10b981; }
  .red { color: #ef4444; }
  .blue { color: #3b82f6; }
  .neutral { color: #6b7280; }
  table {
    width: 100%;
    background: white;
    border-collapse: collapse;
    border-radius: 8px;
    overflow: hidden;
    box-shadow: 0 1px 3px rgba(0,0,0,0.08);
  }
  th, td {
    text-align: left;
    padding: 10px 14px;
    border-bottom: 1px solid #e5e7eb;
  }
  th {
    background: #1e40af;
    color: white;
    font-size: 13px;
    text-transform: uppercase;
    font-weight: 600;
  }
  tbody tr:hover { background: #f9fafb; }
  .equity-svg {
    width: 100%;
    height: 280px;
    background: white;
    border-radius: 8px;
    padding: 16px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.08);
    margin-bottom: 24px;
  }
  .pill {
    display: inline-block;
    padding: 2px 10px;
    border-radius: 12px;
    font-size: 12px;
    font-weight: 600;
  }
  .pill.win { background: #d1fae5; color: #065f46; }
  .pill.loss { background: #fee2e2; color: #7f1d1d; }
  .pill.be { background: #e5e7eb; color: #374151; }
  .pill.open { background: #dbeafe; color: #1e40af; }
  h2 { margin: 24px 0 12px; color: #374151; }
  .footer {
    margin-top: 32px;
    color: #9ca3af;
    font-size: 12px;
    text-align: center;
  }
</style>
</head>
<body>
  <h1>📊 Trading Journal Dashboard</h1>
  <div class="subtitle">Автогенерация из {{ csv_path }} · обновлено {{ generated_at }}</div>

  <div class="grid">
    <div class="card">
      <div class="label">Всего сделок</div>
      <div class="value neutral">{{ stats.total }}</div>
    </div>
    <div class="card">
      <div class="label">Win rate</div>
      <div class="value {{ 'green' if stats.win_rate >= 40 else 'red' }}">
        {{ "%.1f"|format(stats.win_rate) }}%
      </div>
    </div>
    <div class="card">
      <div class="label">Profit Factor</div>
      <div class="value {{ 'green' if stats.profit_factor >= 1.5 else 'red' }}">
        {{ "%.2f"|format(stats.profit_factor) }}
      </div>
    </div>
    <div class="card">
      <div class="label">Чистый P&L</div>
      <div class="value {{ 'green' if stats.total_pnl >= 0 else 'red' }}">
        ${{ "%+.2f"|format(stats.total_pnl) }}
      </div>
    </div>
    <div class="card">
      <div class="label">Avg Win</div>
      <div class="value green">${{ "%.2f"|format(stats.avg_win) }}</div>
    </div>
    <div class="card">
      <div class="label">Avg Loss</div>
      <div class="value red">${{ "%.2f"|format(stats.avg_loss) }}</div>
    </div>
    <div class="card">
      <div class="label">Expectancy</div>
      <div class="value {{ 'green' if stats.expectancy >= 0 else 'red' }}">
        ${{ "%+.2f"|format(stats.expectancy) }}
      </div>
    </div>
    <div class="card">
      <div class="label">Открытых сейчас</div>
      <div class="value blue">{{ stats.open }}</div>
    </div>
  </div>

  <h2>📈 Equity curve</h2>
  <div class="equity-svg">
    {{ equity_svg|safe }}
  </div>

  <h2>📋 Последние 30 сделок</h2>
  <table>
    <thead>
      <tr>
        <th>#</th><th>Дата</th><th>Пара</th><th>Dir</th>
        <th>Вход</th><th>SL</th><th>TP</th>
        <th>Исход</th><th>P&L $</th><th>R</th>
      </tr>
    </thead>
    <tbody>
      {% for t in trades %}
      <tr>
        <td>{{ t.id }}</td>
        <td>{{ t.date }}</td>
        <td>{{ t.pair }}</td>
        <td>{{ t.direction }}</td>
        <td>{{ t.entry }}</td>
        <td>{{ t.stop }}</td>
        <td>{{ t.take }}</td>
        <td><span class="pill {{ t.outcome }}">{{ t.outcome }}</span></td>
        <td class="{{ 'green' if t.result_usd_num > 0 else 'red' if t.result_usd_num < 0 else 'neutral' }}">
          {{ "${:+.2f}".format(t.result_usd_num) if t.result_usd_num != 0 else "—" }}
        </td>
        <td>{{ "%.2f"|format(t.r_value) if t.r_value else "—" }}</td>
      </tr>
      {% endfor %}
    </tbody>
  </table>

  <div class="footer">
    Generated by journal_dashboard.py · forex-trading project
  </div>
</body>
</html>"""


def parse_float(s: str) -> float:
    try:
        return float(s)
    except (ValueError, TypeError):
        return 0.0


def load_trades(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with open(path, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    for r in rows:
        r["result_usd_num"] = parse_float(r.get("result_usd", ""))
        r["risk_num"] = parse_float(r.get("risk_usd", ""))
        r["r_value"] = r["result_usd_num"] / r["risk_num"] if r["risk_num"] > 0 else 0
        if not r.get("outcome"):
            r["outcome"] = "open"
    return rows


def calc_stats(trades: list[dict]) -> dict:
    closed = [t for t in trades if t["outcome"] in ("win", "loss", "be")]
    wins = [t for t in closed if t["outcome"] == "win"]
    losses = [t for t in closed if t["outcome"] == "loss"]

    total_pnl = sum(t["result_usd_num"] for t in closed)
    win_pnl = sum(t["result_usd_num"] for t in wins)
    loss_pnl = sum(t["result_usd_num"] for t in losses)

    pf = (win_pnl / -loss_pnl) if loss_pnl < 0 else (float("inf") if win_pnl > 0 else 0)
    if pf == float("inf"):
        pf = 99.99

    return {
        "total": len(closed),
        "open": len(trades) - len(closed),
        "win_rate": len(wins) / len(closed) * 100 if closed else 0,
        "profit_factor": pf,
        "total_pnl": total_pnl,
        "avg_win": win_pnl / len(wins) if wins else 0,
        "avg_loss": loss_pnl / len(losses) if losses else 0,
        "expectancy": total_pnl / len(closed) if closed else 0,
    }


def make_equity_svg(trades: list[dict], width: int = 1000, height: int = 260) -> str:
    closed = [t for t in trades if t["outcome"] in ("win", "loss", "be")]
    if not closed:
        return (
            '<text x="50%" y="50%" text-anchor="middle" fill="#9ca3af">'
            "Нет закрытых сделок</text>"
        )

    cum = []
    s = 0
    for t in closed:
        s += t["result_usd_num"]
        cum.append(s)

    pad = 20
    mn, mx = min(cum + [0]), max(cum + [0])
    if mx == mn:
        mx += 1
    n = len(cum)
    points = []
    for i, v in enumerate(cum):
        x = pad + i * (width - 2 * pad) / max(n - 1, 1)
        y = pad + (mx - v) / (mx - mn) * (height - 2 * pad)
        points.append(f"{x:.1f},{y:.1f}")

    zero_y = pad + mx / (mx - mn) * (height - 2 * pad)

    return f"""
<svg viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">
  <line x1="{pad}" y1="{zero_y}" x2="{width - pad}" y2="{zero_y}"
        stroke="#9ca3af" stroke-width="1" stroke-dasharray="3,3"/>
  <polyline points="{" ".join(points)}"
            stroke="#3b82f6" stroke-width="2.5" fill="none"/>
  <text x="{width - pad}" y="{pad + 10}" text-anchor="end"
        fill="#1e40af" font-weight="600">${cum[-1]:+.2f}</text>
</svg>"""


def main() -> int:
    parser = argparse.ArgumentParser(
        description="HTML-дашборд журнала сделок",
    )
    parser.add_argument(
        "--csv",
        type=Path,
        default=Path(__file__).resolve().parent.parent / "journal" / "my-trades.csv",
        help="Путь к CSV с журналом",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=Path(__file__).resolve().parent.parent / "journal-dashboard.html",
    )
    args = parser.parse_args()

    if not args.csv.exists():
        # Если своего журнала нет — используем шаблон с примерами
        template_csv = (
            Path(__file__).resolve().parent.parent
            / "journal"
            / "trading-journal-template.csv"
        )
        if template_csv.exists():
            print(f"Свой журнал не найден — использую шаблон {template_csv}")
            args.csv = template_csv
        else:
            print(f"Журнал не найден: {args.csv}")
            return 1

    trades = load_trades(args.csv)
    stats = calc_stats(trades)
    equity_svg = make_equity_svg(trades)

    from datetime import datetime

    template = Template(TEMPLATE)
    html = template.render(
        trades=trades[-30:],
        stats=stats,
        equity_svg=equity_svg,
        csv_path=str(args.csv),
        generated_at=datetime.now().strftime("%Y-%m-%d %H:%M"),
    )

    args.out.write_text(html, encoding="utf-8")
    print(f"✓ Дашборд: {args.out}")
    print(f"  Открыть: open {args.out}")
    return 0


if __name__ == "__main__":
    import sys

    sys.exit(main())
