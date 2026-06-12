#!/usr/bin/env python3
"""Генератор эпизодов для Replay Trainer (I9).

Читает data/<PAIR>_<TF>.csv, нарезает на сессии по CONTEXT + OUTCOME свечей,
отбирает разнообразные эпизоды (тренды, флэты, развороты) и сохраняет
компактный JSON для встраивания в _mkdocs/tools/replay-trainer.md.

Использование:
    python tools/replay_cutter.py                      # дефолт: EURUSD H1
    python tools/replay_cutter.py --pair GBPUSD --tf 1d --episodes 40
    python tools/replay_cutter.py --output custom.json
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DATA_DIR = REPO / "data"

CONTEXT = 40   # сколько свечей показывает виджет (история)
OUTCOME = 20   # сколько свечей проигрывается (будущее)
STEP = 30      # шаг выборки (избегаем перекрытия)


def load_csv(pair: str, tf: str) -> list[dict]:
    path = DATA_DIR / f"{pair}_{tf}.csv"
    if not path.exists():
        sys.exit(f"❌ Файл не найден: {path}")
    rows = []
    with path.open(encoding="utf-8") as f:
        f.readline()  # skip header row
        for line in f:
            parts = line.strip().split(",")
            if len(parts) < 5:
                continue
            rows.append(
                {
                    "t": parts[0][:16],  # 'YYYY-MM-DD HH:MM'
                    "o": round(float(parts[1]), 5),
                    "h": round(float(parts[2]), 5),
                    "l": round(float(parts[3]), 5),
                    "c": round(float(parts[4]), 5),
                }
            )
    return rows


def _atr(candles: list[dict], n: int = 14) -> float:
    trs = []
    for i in range(1, min(len(candles), n + 1)):
        tr = max(
            candles[i]["h"] - candles[i]["l"],
            abs(candles[i]["h"] - candles[i - 1]["c"]),
            abs(candles[i]["l"] - candles[i - 1]["c"]),
        )
        trs.append(tr)
    return sum(trs) / len(trs) if trs else 0.0


def _trend_strength(candles: list[dict]) -> float:
    """Линейная регрессия: наклон / ATR → мера тренда."""
    n = len(candles)
    if n < 2:
        return 0.0
    closes = [c["c"] for c in candles]
    mean_x = (n - 1) / 2
    mean_y = sum(closes) / n
    num = sum((i - mean_x) * (closes[i] - mean_y) for i in range(n))
    den = sum((i - mean_x) ** 2 for i in range(n))
    slope = num / den if den else 0.0
    atr = _atr(candles[-14:])
    return slope / atr if atr else 0.0


def _category(candles: list[dict]) -> str:
    strength = _trend_strength(candles)
    if strength > 0.15:
        return "uptrend"
    if strength < -0.15:
        return "downtrend"
    return "sideways"


def cut_episodes(
    candles: list[dict],
    n_episodes: int,
    context: int = CONTEXT,
    outcome: int = OUTCOME,
    step: int = STEP,
) -> list[dict]:
    total = len(candles)
    episodes = []
    seen_cats: dict[str, int] = {}

    # Простой отбор с диверсификацией по категориям
    i = context
    while i + outcome < total and len(episodes) < n_episodes * 2:
        ctx = candles[i - context : i]
        cat = _category(ctx)
        # Не более 50% от одной категории
        if seen_cats.get(cat, 0) >= n_episodes // 2 + 1:
            i += step
            continue
        fut = candles[i : i + outcome]
        atr = _atr(ctx[-14:])
        pip_size = 0.0001
        episodes.append(
            {
                "id": len(episodes),
                "category": cat,
                "context": ctx,
                "future": fut,
                # Рекомендуемые уровни для виджета (в пипсах)
                "atr_pips": round(atr / pip_size, 1),
                "entry": ctx[-1]["c"],
            }
        )
        seen_cats[cat] = seen_cats.get(cat, 0) + 1
        i += step

    # Обрезаем до нужного количества, выравниваем категории
    episodes.sort(key=lambda e: e["category"])
    selected: list[dict] = []
    per_cat = n_episodes // 3
    cat_counts: dict[str, int] = {}
    for ep in episodes:
        cat = ep["category"]
        if cat_counts.get(cat, 0) < per_cat:
            selected.append(ep)
            cat_counts[cat] = cat_counts.get(cat, 0) + 1
    # Добирем если не хватает
    for ep in episodes:
        if len(selected) >= n_episodes:
            break
        if ep not in selected:
            selected.append(ep)
    # Переназначить id по финальному порядку
    for idx, ep in enumerate(selected[:n_episodes]):
        ep["id"] = idx
    return selected[:n_episodes]


def main() -> None:
    ap = argparse.ArgumentParser(description="Генератор эпизодов Replay Trainer")
    ap.add_argument("--pair", default="EURUSD", help="Валютная пара (EURUSD, GBPUSD…)")
    ap.add_argument(
        "--tf", default="1h", choices=["1h", "1d"], help="Таймфрейм"
    )
    ap.add_argument(
        "--episodes", type=int, default=30, help="Количество эпизодов (по умолчанию 30)"
    )
    ap.add_argument(
        "--context", type=int, default=CONTEXT, help="Свечей истории"
    )
    ap.add_argument(
        "--outcome", type=int, default=OUTCOME, help="Свечей будущего"
    )
    ap.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Путь к выходному JSON (по умолчанию stdout)",
    )
    args = ap.parse_args()

    candles = load_csv(args.pair, args.tf)
    episodes = cut_episodes(
        candles,
        n_episodes=args.episodes,
        context=args.context,
        outcome=args.outcome,
    )

    cats = {}
    for ep in episodes:
        cats[ep["category"]] = cats.get(ep["category"], 0) + 1
    print(
        f"✅ {len(episodes)} эпизодов из {args.pair} {args.tf}: {cats}",
        file=sys.stderr,
    )

    def encode_episode(ep: dict) -> dict:
        """Компактное дельта-кодирование: пипсы от базовой цены эпизода."""
        pip = 0.0001
        base = round(ep["entry"] - (ep["entry"] % 0.0001), 4)

        def enc(c: dict) -> list[int]:
            return [
                round((c["o"] - base) / pip),
                round((c["h"] - base) / pip),
                round((c["l"] - base) / pip),
                round((c["c"] - base) / pip),
            ]

        # Сохраняем только дату (не время) для часовых + дату целиком для D1
        times = [c["t"][:10] for c in ep["context"]] + [
            c["t"][:10] for c in ep["future"]
        ]

        return {
            "id": ep["id"],
            "cat": ep["category"][:1],  # u=uptrend, d=downtrend, s=sideways
            "atr": ep["atr_pips"],
            "base": base,
            "pip": 0.0001,
            "ctx": len(ep["context"]),
            # Все свечи (контекст + будущее) в одном массиве
            "k": [enc(c) for c in ep["context"]] + [enc(c) for c in ep["future"]],
            # Только даты — для подписей при наведении
            "t": times,
        }

    result = {
        "pair": args.pair,
        "tf": args.tf,
        "context": args.context,
        "outcome": args.outcome,
        "episodes": [encode_episode(ep) for ep in episodes],
    }

    out_text = json.dumps(result, ensure_ascii=False, separators=(",", ":"))
    if args.output:
        args.output.write_text(out_text, encoding="utf-8")
        print(f"💾 Сохранено: {args.output}", file=sys.stderr)
    else:
        print(out_text)


if __name__ == "__main__":
    main()
