#!/usr/bin/env python3
"""Помодульный гейт покрытия (M5).

Общий порог ``--cov-fail-under=90`` меряет среднее по пакету: при 96% можно
было не заметить, что ``risk_exposure.py`` просел до 86% — а это модуль,
который считает риск реальных денег. Среднее по больнице для финансового ядра
не подходит: пол любого модуля пакета не должен опускаться ниже пола.

Запуск ПОСЛЕ ``pytest --cov`` (читает данные из .coverage через coverage json):

    pytest --cov -q
    python tools/check_coverage_by_module.py            # пол 85%
    python tools/check_coverage_by_module.py --floor 90 # строже

Пол можно только повышать. Если модуль честно не дотягивает — пиши тест,
а не понижай пол: именно так risk_exposure.py просидел на 86% незамеченным.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Зеркало [tool.coverage.run] omit из pyproject.toml: cli.py — тонкая обвязка
# argparse, покрывается дымовыми --help, строчное покрытие бессмысленно.
OMIT = ("forex_toolkit/cli.py",)


def main() -> int:
    parser = argparse.ArgumentParser(description="Помодульный гейт покрытия")
    parser.add_argument(
        "--floor",
        type=float,
        default=85.0,
        help="минимальный %% покрытия любого модуля (по умолч. 85)",
    )
    args = parser.parse_args()

    proc = subprocess.run(
        [sys.executable, "-m", "coverage", "json", "-o", "-"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        sys.exit(
            "❌ coverage json не сработал — сначала прогони `pytest --cov -q`.\n"
            + proc.stderr.strip()
        )

    report = json.loads(proc.stdout)
    failures: list[tuple[str, float]] = []
    checked = 0
    for path, data in sorted(report["files"].items()):
        if not path.startswith("forex_toolkit/") or path in OMIT:
            continue
        checked += 1
        pct = data["summary"]["percent_covered"]
        missing = data["summary"]["missing_lines"]
        mark = "✓" if pct >= args.floor else "❌"
        detail = "" if pct >= args.floor else f" ({missing} строк без покрытия)"
        print(f"  {mark} {pct:5.1f}%  {path}{detail}")
        if pct < args.floor:
            failures.append((path, pct))

    if failures:
        names = ", ".join(f"{p} ({v:.1f}%)" for p, v in failures)
        print(f"\n❌ Ниже пола {args.floor:.0f}%: {names}")
        print("   Пиши тест, а не понижай пол — см. docstring скрипта.")
        return 1

    print(f"\n✅ Все {checked} модулей пакета ≥ {args.floor:.0f}% покрытия.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
