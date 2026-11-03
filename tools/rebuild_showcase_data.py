#!/usr/bin/env python3
"""Пересборка витринных данных сайта одной командой (K1).

Пять витрин — переобучение, перенос между парами, рейтинг стратегий, банк
эпизодов Replay и рыночная аналитика (волатильность/корреляции) — построены
на числах, которые раньше никто не мог пересчитать, не изучая скрипты по
отдельности. Этот файл фиксирует канонические параметры прогона и
пересобирает все пять JSON разом:

    python tools/rebuild_showcase_data.py            # пересобрать
    python tools/rebuild_showcase_data.py --check    # проверить воспроизводимость

В каждый JSON записывается ``generated_at`` (дата расчёта) — по традиции из
ENGINEERING-NOTES §1.3: число на витрине обязано говорить, когда и на каком
периоде оно посчитано. Пара, таймфрейм и период выборки уже пишут сами
генераторы (meta.from / meta.to).

Данные (``data/*.csv``) в репозитории не хранятся — см. docstring сканеров.
--check пересобирает витрины во временный каталог и сравнивает с лежащими
в ``_mkdocs/data/``, игнорируя ``generated_at``: расходится — значит либо
обновились котировки (тогда честно пересобрать без --check), либо кто-то
правил JSON руками (тогда это уже не данные, а украшение).
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DATA_DIR = REPO / "data"
OUT_DIR = REPO / "_mkdocs" / "data"

# Канонический набор пар Replay: все, для которых лежат котировки в data/.
# До H3 банк использовал четыре пары из восьми — половина архива простаивала.
REPLAY_PAIRS = [
    "EURUSD",
    "GBPUSD",
    "USDJPY",
    "EURJPY",
    "AUDUSD",
    "GBPJPY",
    "NZDUSD",
    "USDCAD",
]

# Каждая витрина: какой генератор, с какими аргументами, куда писать и куда
# ставить дату расчёта (в meta — там, где генератор уже пишет параметры
# прогона; в корень — у каталога Replay, у которого meta нет).
SHOWCASES = [
    {
        "name": "overfitting",
        "script": "tools/overfit_scan.py",
        "args": ["--csv", "data/EURUSD_1h.csv"],
        "out": "overfitting.json",
        "stamp": "meta",
    },
    {
        "name": "multipair",
        "script": "tools/multipair_scan.py",
        "args": ["--timeframe", "1h"],
        "out": "multipair.json",
        "stamp": "meta",
    },
    {
        "name": "strategies",
        "script": "tools/strategy_scan.py",
        "args": ["--csv", "data/EURUSD_1h.csv"],
        "out": "strategies.json",
        "stamp": "meta",
    },
    {
        "name": "replay-episodes",
        "script": "tools/replay_cutter.py",
        "args": [
            "--pairs",
            ",".join(REPLAY_PAIRS),
            "--timeframes",
            "1h,1d",
            "--episodes",
            "10",
            "--context",
            "30",
            "--outcome",
            "15",
        ],
        "out": "replay-episodes.json",
        "stamp": "root",
    },
    {
        "name": "market-analytics",
        "script": "tools/build_market_analytics.py",
        "args": [],
        "out": "market-analytics.json",
        "stamp": "meta",
    },
    {
        "name": "weekly-review",
        "script": "tools/build_weekly_review.py",
        "args": [],
        "out": "weekly-review.json",
        "stamp": "meta",
    },
    {
        "name": "seasonality",
        "script": "tools/build_seasonality.py",
        "args": [],
        "out": "seasonality.json",
        "stamp": "meta",
    },
]


def _run_generator(spec: dict, out_path: Path) -> None:
    """Запускает генератор витрины; падение любого из них роняет всю сборку."""
    cmd = [
        sys.executable,
        str(REPO / spec["script"]),
        *spec["args"],
        "--out" if spec["script"] != "tools/replay_cutter.py" else "--output",
        str(out_path),
    ]
    proc = subprocess.run(cmd, cwd=REPO, capture_output=True, text=True)
    if proc.returncode != 0:
        sys.exit(
            f"❌ {spec['script']} упал с кодом {proc.returncode}:\n"
            f"{proc.stderr.strip()}"
        )


def _stamp(out_path: Path, where: str, when: str) -> dict:
    """Вписывает дату расчёта, сохраняя стиль форматирования генератора."""
    document = json.loads(out_path.read_text(encoding="utf-8"))
    target = document.setdefault("meta", {}) if where == "meta" else document
    target["generated_at"] = when
    compact = out_path.name == "replay-episodes.json"
    out_path.write_text(
        json.dumps(
            document,
            ensure_ascii=False,
            separators=(",", ":") if compact else None,
            indent=None if compact else 1,
        ),
        encoding="utf-8",
    )
    return document


def _describe(document: dict) -> str:
    """Одна строка: пара, таймфрейм, период, дата расчёта."""
    meta = document.get("meta", {})
    pair = (
        meta.get("home_pair") or meta.get("pair") or "/".join(document.get("pairs", []))
    )
    timeframe = meta.get("timeframe") or "/".join(document.get("timeframes", []))
    period = f"{str(meta.get('from', '?'))[:10]} → {str(meta.get('to', '?'))[:10]}"
    if not meta.get("from"):
        starts = [e.get("t", ["?"])[0] for e in document.get("episodes", [])]
        period = f"эпизодов: {len(document.get('episodes', []))}, с {min(starts)[:10]}"
    stamp = meta.get("generated_at") or document.get("generated_at", "?")
    return f"{pair} · {timeframe} · {period} · расчёт {stamp}"


def _strip_stamp(document: dict) -> dict:
    """Убирает generated_at — в --check сравниваем числа, а не дату прогона."""
    document = json.loads(json.dumps(document))
    document.pop("generated_at", None)
    if isinstance(document.get("meta"), dict):
        document["meta"].pop("generated_at", None)
    return document


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument(
        "--check",
        action="store_true",
        help="не перезаписывать витрины, а проверить их воспроизводимость",
    )
    ap.add_argument("--out-dir", type=Path, default=OUT_DIR, help=argparse.SUPPRESS)
    args = ap.parse_args()

    missing = [
        f"{pair}_{tf}"
        for pair in REPLAY_PAIRS
        for tf in ("1h", "1d")
        if not (DATA_DIR / f"{pair}_{tf}.csv").exists()
    ]
    if missing:
        sys.exit("❌ Нет котировок: " + ", ".join(missing))

    when = dt.date.today().isoformat()
    workdir = Path(tempfile.mkdtemp(prefix="showcase-")) if args.check else args.out_dir
    workdir.mkdir(parents=True, exist_ok=True)

    failures = 0
    for spec in SHOWCASES:
        out_path = workdir / spec["out"]
        print(f"⚙️  {spec['name']}: {spec['script']} …")
        _run_generator(spec, out_path)
        document = _stamp(out_path, spec["stamp"], when)

        if args.check:
            current_path = args.out_dir / spec["out"]
            if not current_path.exists():
                print(f"❌ {spec['out']} отсутствует в {args.out_dir}")
                failures += 1
                continue
            current = json.loads(current_path.read_text(encoding="utf-8"))
            if _strip_stamp(current) == _strip_stamp(document):
                print(f"✅ {spec['out']} воспроизводится · {_describe(document)}")
            else:
                print(
                    f"❌ {spec['out']} НЕ воспроизводится — числа расходятся.\n"
                    f"   Если обновлялись котировки в data/ — пересобери без --check."
                )
                failures += 1
        else:
            print(f"✅ {spec['out']} · {_describe(document)}")

    if args.check:
        if failures:
            print(f"\n❌ Не воспроизводятся: {failures} из {len(SHOWCASES)}.")
            return 1
        print("\n✅ Все витрины пересчитываются одной командой и совпадают.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
