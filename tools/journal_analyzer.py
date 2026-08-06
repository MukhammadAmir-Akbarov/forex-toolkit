#!/usr/bin/env python3
"""
AI-помощник для анализа торгового журнала.

Читает твой CSV журнал и находит паттерны:
  - В какое время суток ты прибыльнее?
  - В какой день недели хуже всего?
  - На каких сетапах выигрываешь / проигрываешь чаще?
  - Влияет ли «следование правилам» на результат?
  - Корреляция между настроением (если есть в журнале) и P&L
  - Когда тебе пора прекращать торговать?

Никакого настоящего AI — просто статистика и эвристики. Но эффективно.
"""

from __future__ import annotations

import argparse
import csv
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path

JOURNAL = Path(__file__).resolve().parent.parent / "journal" / "my-trades.csv"


def load_trades(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with open(path, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    closed = [r for r in rows if r.get("outcome") in ("win", "loss", "be")]
    for r in closed:
        try:
            r["_pnl"] = float(r.get("result_usd", 0) or 0)
        except ValueError:
            r["_pnl"] = 0
        try:
            r["_risk"] = float(r.get("risk_usd", 0) or 0)
        except ValueError:
            r["_risk"] = 0
        r["_r"] = r["_pnl"] / r["_risk"] if r["_risk"] > 0 else 0
        try:
            r["_datetime"] = datetime.strptime(
                f"{r.get('date', '')} {r.get('time', '00:00')}",
                "%Y-%m-%d %H:%M",
            )
        except ValueError:
            r["_datetime"] = None
    return closed


def by_hour(trades: list[dict]) -> dict:
    buckets = defaultdict(list)
    for t in trades:
        if t["_datetime"]:
            buckets[t["_datetime"].hour].append(t["_r"])
    return {
        h: {
            "n": len(rs),
            "win_rate": sum(1 for r in rs if r > 0) / len(rs) * 100,
            "avg_r": sum(rs) / len(rs),
            "total_r": sum(rs),
        }
        for h, rs in buckets.items()
    }


def by_dayofweek(trades: list[dict]) -> dict:
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    buckets = defaultdict(list)
    for t in trades:
        if t["_datetime"]:
            buckets[days[t["_datetime"].weekday()]].append(t["_r"])
    return {
        d: {
            "n": len(rs),
            "win_rate": sum(1 for r in rs if r > 0) / len(rs) * 100 if rs else 0,
            "avg_r": sum(rs) / len(rs) if rs else 0,
            "total_r": sum(rs),
        }
        for d, rs in buckets.items()
    }


def by_pair(trades: list[dict]) -> dict:
    buckets = defaultdict(list)
    for t in trades:
        p = t.get("pair", "")
        if p:
            buckets[p].append(t["_r"])
    return {
        p: {
            "n": len(rs),
            "win_rate": sum(1 for r in rs if r > 0) / len(rs) * 100,
            "avg_r": sum(rs) / len(rs),
            "total_r": sum(rs),
        }
        for p, rs in buckets.items()
    }


def by_direction(trades: list[dict]) -> dict:
    buckets = defaultdict(list)
    for t in trades:
        d = t.get("direction", "")
        if d:
            buckets[d].append(t["_r"])
    return {
        d: {
            "n": len(rs),
            "win_rate": sum(1 for r in rs if r > 0) / len(rs) * 100,
            "avg_r": sum(rs) / len(rs),
            "total_r": sum(rs),
        }
        for d, rs in buckets.items()
    }


def by_rule_following(trades: list[dict]) -> dict:
    buckets = defaultdict(list)
    for t in trades:
        rules = t.get("followed_rules", "").lower()
        if rules in ("yes", "no"):
            buckets[rules].append(t["_r"])
    return {
        r: {
            "n": len(rs),
            "win_rate": sum(1 for r in rs if r > 0) / len(rs) * 100,
            "avg_r": sum(rs) / len(rs),
            "total_r": sum(rs),
        }
        for r, rs in buckets.items()
    }


def consecutive_losses(trades: list[dict]) -> dict:
    if not trades:
        return {"max_streak": 0, "current": 0}
    trades_sorted = sorted(trades, key=lambda t: t.get("_datetime") or datetime.min)
    max_streak = current = 0
    for t in trades_sorted:
        if t["_pnl"] < 0:
            current += 1
            max_streak = max(max_streak, current)
        else:
            current = 0
    # «Current» в самом конце
    final_streak = 0
    for t in reversed(trades_sorted):
        if t["_pnl"] < 0:
            final_streak += 1
        else:
            break
    return {"max_streak": max_streak, "current_streak": final_streak}


def print_table(title: str, data: dict, sort_by: str = "total_r"):
    print(f"\n📊 {title}")
    print("─" * 60)
    if not data:
        print("  (нет данных)")
        return
    sorted_items = sorted(data.items(), key=lambda x: x[1][sort_by], reverse=True)
    print(f"  {'Категория':<12} {'N':<5} {'WR':<8} {'Avg R':<10} {'Итого R':<10}")
    for cat, m in sorted_items:
        wr_str = f"{m['win_rate']:.0f}%"
        print(
            f"  {str(cat):<12} {m['n']:<5} "
            f"{wr_str:<8} {m['avg_r']:+.2f}      {m['total_r']:+.2f}"
        )


def insights(trades: list[dict]) -> list[str]:
    """Главные инсайты в человеко-читаемом виде."""
    out = []
    if len(trades) < 10:
        out.append(
            f"⚠️  Только {len(trades)} сделок. Для надёжной статистики нужно ≥ 30."
        )
        return out

    # 1. Best/Worst hour
    hours = by_hour(trades)
    if hours:
        best_hour = max(hours.items(), key=lambda x: x[1]["avg_r"])
        worst_hour = min(hours.items(), key=lambda x: x[1]["avg_r"])
        if best_hour[1]["n"] >= 5 and best_hour[1]["avg_r"] > 0.3:
            out.append(
                f"⏰ Лучшее время: {best_hour[0]}:00 — "
                f"avg {best_hour[1]['avg_r']:+.2f}R на {best_hour[1]['n']} сделках"
            )
        if worst_hour[1]["n"] >= 5 and worst_hour[1]["avg_r"] < -0.3:
            out.append(
                f"❌ Худшее время: {worst_hour[0]}:00 — "
                f"avg {worst_hour[1]['avg_r']:+.2f}R. Рассмотри прекратить торговать тогда."
            )

    # 2. Day of week
    days = by_dayofweek(trades)
    if days:
        worst_day = min(days.items(), key=lambda x: x[1]["avg_r"])
        if worst_day[1]["n"] >= 5 and worst_day[1]["avg_r"] < -0.3:
            out.append(
                f"📅 Худший день: {worst_day[0]} — avg {worst_day[1]['avg_r']:+.2f}R"
            )

    # 3. Rule following
    rules = by_rule_following(trades)
    if "yes" in rules and "no" in rules:
        diff = rules["yes"]["avg_r"] - rules["no"]["avg_r"]
        if diff > 0.5:
            out.append(
                f"📋 Когда следуешь правилам — выигрываешь {diff:+.2f}R "
                f"больше на сделку. **Дисциплина = деньги.**"
            )
        elif diff < -0.3:
            out.append(
                "🤔 Странность: «нарушения» правил приносят больше прибыли. "
                "Возможно, правила нужно пересмотреть, или это случайность."
            )

    # 4. Streaks
    streaks = consecutive_losses(trades)
    if streaks["max_streak"] >= 5:
        out.append(
            f"🔥 Максимальная серия убытков: {streaks['max_streak']}. "
            f"Психологически выдержал — хорошо. Но это сигнал на ревизию."
        )
    if streaks["current_streak"] >= 3:
        out.append(
            f"⚠️  Сейчас идёт серия {streaks['current_streak']} убытков подряд. "
            f"**Сделай паузу.** Перечитай anti-tilt protocol."
        )

    # 5. Direction bias
    dirs = by_direction(trades)
    if "long" in dirs and "short" in dirs:
        lng = dirs["long"]
        s = dirs["short"]
        if lng["n"] >= 10 and s["n"] >= 10:
            diff = lng["avg_r"] - s["avg_r"]
            if abs(diff) > 0.5:
                better = "LONG" if diff > 0 else "SHORT"
                out.append(
                    f"📈 У тебя bias к {better} — на {abs(diff):.2f}R лучше. "
                    f"Может быть, ты лучше «видишь» одно направление?"
                )

    # 6. Overall
    total_r = sum(t["_r"] for t in trades)
    wr = sum(1 for t in trades if t["_pnl"] > 0) / len(trades) * 100
    if wr < 30 and len(trades) >= 30:
        out.append(
            f"❌ Win rate {wr:.0f}% < 30% на {len(trades)} сделках. "
            f"Стратегия не работает в текущем виде. Пересмотри или останови."
        )
    if total_r < -10 and len(trades) >= 20:
        out.append(
            f"💸 Потерял {total_r:.1f}R за {len(trades)} сделок. "
            f"**Серьёзная просадка.** Демо или пауза."
        )
    if total_r > 20 and wr > 50:
        out.append(
            f"✅ Отличные результаты: +{total_r:.1f}R за {len(trades)} "
            f"сделок при WR {wr:.0f}%. Продолжай в том же духе, "
            f"НЕ увеличивая риск."
        )

    if not out:
        out.append(
            f"📊 Результаты в норме: {len(trades)} сделок, "
            f"WR {wr:.0f}%, всего {total_r:+.1f}R. Продолжай и наращивай статистику."
        )

    return out


def main() -> int:
    parser = argparse.ArgumentParser(
        description="AI-анализ торгового журнала",
    )
    parser.add_argument("--csv", type=Path, default=JOURNAL)
    args = parser.parse_args()

    trades = load_trades(args.csv)
    if not trades:
        print(f"Журнал пуст или не найден: {args.csv}")
        return 1

    print("=" * 60)
    print("  JOURNAL ANALYZER — анализ торгового журнала")
    print("=" * 60)
    print(f"\nИсточник: {args.csv}")
    print(f"Сделок закрыто: {len(trades)}")

    # Базовая статистика
    total_r = sum(t["_r"] for t in trades)
    wins = sum(1 for t in trades if t["_pnl"] > 0)
    win_rate = wins / len(trades) * 100 if trades else 0

    print(f"\nОбщий итог: {total_r:+.2f}R ({wins}/{len(trades)} = {win_rate:.1f}% WR)")

    # По категориям
    print_table("По часам суток", by_hour(trades))
    print_table("По дням недели", by_dayofweek(trades))
    print_table("По парам", by_pair(trades))
    print_table("По направлению", by_direction(trades))
    print_table("По следованию правилам", by_rule_following(trades))

    streaks = consecutive_losses(trades)
    print("\n🔥 Серии убытков:")
    print(f"  Максимальная за всё время: {streaks['max_streak']}")
    print(f"  Текущая (с конца):          {streaks['current_streak']}")

    print("\n" + "=" * 60)
    print("  💡 ИНСАЙТЫ")
    print("=" * 60)
    for insight in insights(trades):
        print(f"\n  {insight}")
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
