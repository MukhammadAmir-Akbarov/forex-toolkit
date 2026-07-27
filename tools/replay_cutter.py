#!/usr/bin/env python3
"""Генератор эпизодов для Replay Trainer (I9).

Читает data/<PAIR>_<TF>.csv, нарезает на сессии по CONTEXT + OUTCOME свечей,
отбирает разнообразные эпизоды (тренды, флэты, развороты) и сохраняет
компактный JSON для встраивания в _mkdocs/tools/replay-trainer.md.

Использование:
    python tools/replay_cutter.py                      # дефолт: EURUSD H1
    python tools/replay_cutter.py --pairs EURUSD,GBPUSD --timeframes 1h,1d
    python tools/replay_cutter.py --output custom.json
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DATA_DIR = REPO / "data"

CONTEXT = 40   # сколько свечей показывает виджет (история)
OUTCOME = 20   # сколько свечей проигрывается (будущее)
STEP = 30      # шаг выборки (избегаем перекрытия)


def pip_size(pair: str) -> float:
    """Return the conventional pip size for a currency pair."""
    return 0.01 if pair.upper().endswith("JPY") else 0.0001


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
    pip: float = 0.0001,
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
        episodes.append(
            {
                "id": len(episodes),
                "category": cat,
                "context": ctx,
                "future": fut,
                # Рекомендуемые уровни для виджета (в пипсах)
                "atr_pips": round(atr / pip, 1),
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


def encode_episode(ep: dict, pair: str, tf: str) -> dict:
    """Compactly encode one episode in pips from a base price."""
    pip = pip_size(pair)
    digits = 2 if pip == 0.01 else 4
    base = round(math.floor(ep["entry"] / pip) * pip, digits)
    display_tf = {"1h": "H1", "1d": "D1"}[tf.lower()]

    def enc(candle: dict) -> list[int]:
        return [
            round((candle["o"] - base) / pip),
            round((candle["h"] - base) / pip),
            round((candle["l"] - base) / pip),
            round((candle["c"] - base) / pip),
        ]

    return {
        "id": f"{pair}-{tf}-{ep['id']}",
        "pair": pair,
        "tf": display_tf,
        "cat": ep["category"][:1],
        "atr": ep["atr_pips"],
        "base": base,
        "pip": pip,
        "ctx": len(ep["context"]),
        "k": [enc(c) for c in ep["context"]]
        + [enc(c) for c in ep["future"]],
        "t": [candle["t"] for candle in ep["context"]]
        + [candle["t"] for candle in ep["future"]],
    }


def build_catalog(
    pairs: list[str],
    timeframes: list[str],
    episodes_per_market: int,
    context: int = CONTEXT,
    outcome: int = OUTCOME,
) -> dict:
    """Build a Replay 2.0 catalog for multiple markets."""
    encoded: list[dict] = []
    for pair in pairs:
        pair = pair.upper()
        for tf in timeframes:
            tf = tf.lower()
            market_episodes = cut_episodes(
                load_csv(pair, tf),
                n_episodes=episodes_per_market,
                context=context,
                outcome=outcome,
                pip=pip_size(pair),
            )
            encoded.extend(
                encode_episode(ep, pair, tf) for ep in market_episodes
            )

    return {
        "version": 2,
        "pairs": pairs,
        "timeframes": [
            {"1h": "H1", "1d": "D1"}[tf.lower()] for tf in timeframes
        ],
        "context": context,
        "outcome": outcome,
        "episodes": encoded,
    }


def _csv_values(value: str) -> list[str]:
    return [item.strip() for item in value.split(",") if item.strip()]


def main() -> None:
    ap = argparse.ArgumentParser(description="Генератор эпизодов Replay Trainer")
    ap.add_argument("--pair", default="EURUSD", help="Валютная пара (EURUSD, GBPUSD…)")
    ap.add_argument(
        "--tf", default="1h", choices=["1h", "1d"], help="Таймфрейм"
    )
    ap.add_argument(
        "--pairs",
        help="Несколько пар через запятую; переопределяет --pair",
    )
    ap.add_argument(
        "--timeframes",
        help="Несколько TF через запятую (1h,1d); переопределяет --tf",
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

    pairs = [pair.upper() for pair in _csv_values(args.pairs or args.pair)]
    timeframes = [
        tf.lower() for tf in _csv_values(args.timeframes or args.tf)
    ]
    invalid_timeframes = set(timeframes) - {"1h", "1d"}
    if invalid_timeframes:
        ap.error(
            "неподдерживаемые таймфреймы: "
            + ", ".join(sorted(invalid_timeframes))
        )

    result = build_catalog(
        pairs,
        timeframes,
        episodes_per_market=args.episodes,
        context=args.context,
        outcome=args.outcome,
    )

    markets = len(pairs) * len(timeframes)
    print(
        f"✅ {len(result['episodes'])} эпизодов для {markets} рынков",
        file=sys.stderr,
    )

    out_text = json.dumps(result, ensure_ascii=False, separators=(",", ":"))
    if args.output:
        args.output.write_text(out_text, encoding="utf-8")
        print(f"💾 Сохранено: {args.output}", file=sys.stderr)
    else:
        print(out_text)


if __name__ == "__main__":
    main()
