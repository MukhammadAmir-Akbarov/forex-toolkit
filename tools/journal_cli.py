#!/usr/bin/env python3
"""
Trading Journal CLI — добавление сделок в журнал через терминал.

Использование:
  python journal_cli.py add --pair EURUSD --dir long \\
    --entry 1.0852 --sl 1.0827 --tp 1.0902 --lot 0.02 --risk 5

  python journal_cli.py close 1 --price 1.0902
  python journal_cli.py list
  python journal_cli.py stats
  python journal_cli.py import-mt5 report.html --out journal/mt5-trades.csv
"""
from __future__ import annotations

import argparse
import csv
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

from forex_toolkit.mt5_statement import (
    MT5StatementError,
    parse_mt5_html,
    write_journal_csv,
)

def _resolve_journal_path() -> Path:
    """Где хранить журнал сделок.

    Приоритет: переменная окружения ``FOREX_JOURNAL`` → каталог ``journal/`` в
    репозитории (если он рядом со скриптом) → ``journal/`` в текущей рабочей
    директории. Последний вариант важен для установленного wheel, чтобы не
    писать в ``site-packages``.
    """
    env = os.environ.get("FOREX_JOURNAL")
    if env:
        return Path(env)
    repo_journal = Path(__file__).resolve().parent.parent / "journal"
    if repo_journal.is_dir():
        return repo_journal / "my-trades.csv"
    return Path.cwd() / "journal" / "my-trades.csv"


JOURNAL_PATH = _resolve_journal_path()

HEADERS = [
    "id", "date", "time", "pair", "direction", "entry", "stop", "take",
    "lot", "risk_usd", "rr_planned", "close_price", "close_time",
    "result_pips", "result_usd", "outcome", "followed_rules", "note",
]


def ensure_journal_exists() -> None:
    if not JOURNAL_PATH.exists():
        JOURNAL_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(JOURNAL_PATH, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(HEADERS)


def read_all() -> list[dict[str, str]]:
    ensure_journal_exists()
    with open(JOURNAL_PATH, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def write_all(rows: list[dict[str, Any]]) -> None:
    with open(JOURNAL_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=HEADERS)
        writer.writeheader()
        for r in rows:
            writer.writerow({h: r.get(h, "") for h in HEADERS})


def cmd_add(args: argparse.Namespace) -> int:
    rows = read_all()
    next_id = max([int(r["id"]) for r in rows] + [0]) + 1
    now = datetime.now()
    stop_pips = abs(args.entry - args.sl) * 10_000
    take_pips = abs(args.entry - args.tp) * 10_000
    rr = take_pips / stop_pips if stop_pips > 0 else 0

    row = {
        "id": next_id,
        "date": now.strftime("%Y-%m-%d"),
        "time": now.strftime("%H:%M"),
        "pair": args.pair.upper(),
        "direction": args.dir,
        "entry": args.entry,
        "stop": args.sl,
        "take": args.tp,
        "lot": args.lot,
        "risk_usd": args.risk,
        "rr_planned": round(rr, 2),
        "close_price": "",
        "close_time": "",
        "result_pips": "",
        "result_usd": "",
        "outcome": "open",
        "followed_rules": args.rules or "",
        "note": args.note or "",
    }
    rows.append(row)
    write_all(rows)

    print(f"\n✓ Сделка #{next_id} добавлена:")
    print(f"  {args.pair.upper()} {args.dir.upper()}  "
          f"{args.entry} → SL {args.sl} / TP {args.tp}")
    print(f"  Лот: {args.lot}, риск ${args.risk}, R:R = 1:{rr:.1f}")
    return 0


def cmd_close(args: argparse.Namespace) -> int:
    rows = read_all()
    target = None
    for r in rows:
        if int(r["id"]) == args.id:
            target = r
            break
    if not target:
        print(f"Сделка #{args.id} не найдена.")
        return 1
    if target["outcome"] != "open":
        print(f"Сделка #{args.id} уже закрыта ({target['outcome']}).")
        return 1

    entry = float(target["entry"])
    direction = target["direction"]
    lot = float(target["lot"])

    diff = args.price - entry if direction == "long" else entry - args.price
    pips = round(diff * 10_000, 1)
    # Грубо: 1 пипс на 1 лот EUR/USD ≈ $10
    usd = round(pips * lot * 10, 2)

    target["close_price"] = args.price
    target["close_time"] = datetime.now().strftime("%Y-%m-%d %H:%M")
    target["result_pips"] = pips
    target["result_usd"] = usd
    if pips > 0:
        target["outcome"] = "win"
    elif pips < 0:
        target["outcome"] = "loss"
    else:
        target["outcome"] = "be"

    write_all(rows)
    print(f"\n✓ Сделка #{args.id} закрыта: "
          f"{target['outcome'].upper()} {pips:+.1f} пипсов ${usd:+.2f}")
    return 0


def cmd_list(args: argparse.Namespace) -> int:
    rows = read_all()
    if not rows:
        print("Журнал пуст.")
        return 0

    print(f"\n{'#':<4} {'Дата':<11} {'Пара':<8} {'Dir':<6} "
          f"{'Вход':<9} {'Исход':<8} {'P&L $':>9}")
    print("─" * 65)
    for r in rows[-20:]:
        outcome = r["outcome"]
        emoji = "✓" if outcome == "win" else "✗" if outcome == "loss" else "○"
        pnl = r.get("result_usd", "")
        print(f"{r['id']:<4} {r['date']:<11} {r['pair']:<8} "
              f"{r['direction']:<6} {r['entry']:<9} "
              f"{emoji} {outcome:<6} ${pnl if pnl else '—':>8}")
    return 0


def cmd_stats(args: argparse.Namespace) -> int:
    rows = [r for r in read_all() if r["outcome"] in ("win", "loss", "be")]
    if not rows:
        print("Нет закрытых сделок.")
        return 0

    wins = [r for r in rows if r["outcome"] == "win"]
    losses = [r for r in rows if r["outcome"] == "loss"]
    total_pnl = sum(float(r["result_usd"]) for r in rows
                    if r["result_usd"])
    win_pnl = sum(float(r["result_usd"]) for r in wins
                  if r["result_usd"])
    loss_pnl = sum(float(r["result_usd"]) for r in losses
                   if r["result_usd"])

    win_rate = len(wins) / len(rows) * 100 if rows else 0
    pf = win_pnl / -loss_pnl if loss_pnl < 0 else float("inf")
    avg_win = win_pnl / len(wins) if wins else 0
    avg_loss = loss_pnl / len(losses) if losses else 0
    expectancy = total_pnl / len(rows) if rows else 0

    print("\n" + "=" * 50)
    print("  СТАТИСТИКА ЖУРНАЛА")
    print("=" * 50)
    print(f"  Всего сделок:      {len(rows)}")
    print(f"  Прибыльных:        {len(wins)}")
    print(f"  Убыточных:         {len(losses)}")
    print(f"  Win rate:          {win_rate:.1f}%")
    print(f"  Avg Win:           ${avg_win:+.2f}")
    print(f"  Avg Loss:          ${avg_loss:+.2f}")
    print(f"  Profit Factor:     {pf:.2f}")
    print(f"  Expectancy:        ${expectancy:+.2f} / сделку")
    print(f"  Чистый P&L:        ${total_pnl:+.2f}")
    print()
    return 0


def cmd_import_mt5(args: argparse.Namespace) -> int:
    """Convert an MT5 HTML account statement to the web-journal CSV schema."""
    source = Path(args.report)
    if not source.is_file():
        print(f"Отчёт не найден: {source}")
        return 1
    try:
        result = parse_mt5_html(source)
        output = write_journal_csv(result.trades, args.out)
    except (MT5StatementError, OSError) as exc:
        print(f"Не удалось импортировать MT5-отчёт: {exc}")
        return 1

    print(f"\n✓ Импортировано закрытых сделок: {len(result.trades)}")
    print(f"  CSV: {output}")
    for warning in result.warnings:
        print(f"  ⚠ {warning}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Trading Journal CLI")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_add = sub.add_parser("add", help="Добавить сделку")
    p_add.add_argument("--pair", required=True)
    p_add.add_argument("--dir", choices=["long", "short"], required=True)
    p_add.add_argument("--entry", type=float, required=True)
    p_add.add_argument("--sl", type=float, required=True)
    p_add.add_argument("--tp", type=float, required=True)
    p_add.add_argument("--lot", type=float, required=True)
    p_add.add_argument("--risk", type=float, required=True,
                       help="Риск в USD")
    p_add.add_argument("--rules", choices=["yes", "no"],
                       help="Следовал ли правилам?")
    p_add.add_argument("--note", help="Заметка")
    p_add.set_defaults(func=cmd_add)

    p_close = sub.add_parser("close", help="Закрыть сделку")
    p_close.add_argument("id", type=int)
    p_close.add_argument("--price", type=float, required=True,
                         help="Цена закрытия")
    p_close.set_defaults(func=cmd_close)

    p_list = sub.add_parser("list", help="Показать последние 20 сделок")
    p_list.set_defaults(func=cmd_list)

    p_stats = sub.add_parser("stats", help="Показать статистику")
    p_stats.set_defaults(func=cmd_stats)

    p_import = sub.add_parser(
        "import-mt5",
        help="Преобразовать HTML-отчёт MetaTrader 5 в CSV журнала",
    )
    p_import.add_argument("report", help="Путь к MT5 HTML report")
    p_import.add_argument(
        "--out",
        type=Path,
        default=Path("journal/mt5-trades.csv"),
        help="Куда сохранить CSV (по умолчанию journal/mt5-trades.csv)",
    )
    p_import.set_defaults(func=cmd_import_mt5)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
