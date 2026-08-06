#!/usr/bin/env python3
"""Воронка маршрута по экспорту GoatCounter.

Зачем: правило проекта — «неделя метрик, затем чиним первый провал». События
собираются, но прочитать их как воронку было нечем, поэтому правило нельзя
было исполнить. Скрипт печатает шаги, конверсию и самый большой обрыв.

Как получить данные:
  GoatCounter -> Dashboard -> Export -> CSV. Подходит и экспорт хитов
  (колонка ``Path``), и любая сводка вида ``path,count``.

Запуск:
  python tools/funnel_report.py export.csv
  python tools/funnel_report.py export.csv --json
  python tools/funnel_report.py export.csv --stages first15_completed,exam_completed

Скрипт ничего не скачивает: у GoatCounter нет открытого API без токена, а
хранить токен в репозитории не нужно. Выгружаешь CSV руками — читаешь отчёт.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from dataclasses import dataclass
from pathlib import Path

# Шаги маршрута «от первого визита до разбора сделки». Порядок важен: конверсия
# считается от первого шага, обрыв — от предыдущего.
DEFAULT_STAGES: tuple[tuple[str, str], ...] = (
    ("first15_completed", "Прошёл «Первые 15 минут»"),
    ("calculator_completed", "Посчитал позицию"),
    ("trade_plan_saved", "Сохранил план сделки"),
    ("trade_plan_opened", "Открыл сделку по плану"),
    ("trade_review_completed", "Разобрал закрытую сделку"),
)

# Колонки, в которых GoatCounter отдаёт имя события в разных версиях экспорта.
PATH_COLUMNS = ("path", "event", "name", "page")
COUNT_COLUMNS = ("count", "hits", "visits", "total")


@dataclass(frozen=True)
class Step:
    event: str
    label: str
    count: int
    of_first: float
    drop_from_previous: float


def _pick(header: list[str], candidates: tuple[str, ...]) -> str | None:
    lowered = {name.strip().lower(): name for name in header}
    for candidate in candidates:
        if candidate in lowered:
            return lowered[candidate]
    return None


def count_events(rows: list[dict], header: list[str]) -> dict[str, int]:
    """Сводка «событие -> сколько раз». Понимает и хиты, и готовые счётчики."""
    path_column = _pick(header, PATH_COLUMNS)
    if path_column is None:
        raise ValueError(
            "в CSV нет колонки с событием — ожидалась одна из: "
            + ", ".join(PATH_COLUMNS)
        )
    count_column = _pick(header, COUNT_COLUMNS)

    counts: dict[str, int] = {}
    for row in rows:
        event = (row.get(path_column) or "").strip().strip("/")
        if not event:
            continue
        if count_column:
            raw = (row.get(count_column) or "").strip()
            try:
                step = int(float(raw)) if raw else 0
            except ValueError:
                step = 0
        else:
            step = 1
        counts[event] = counts.get(event, 0) + step
    return counts


def build_funnel(
    counts: dict[str, int],
    stages: tuple[tuple[str, str], ...] = DEFAULT_STAGES,
) -> list[Step]:
    """Шаги воронки с конверсией от первого и обрывом от предыдущего."""
    steps: list[Step] = []
    first = counts.get(stages[0][0], 0) if stages else 0
    previous: int | None = None
    for event, label in stages:
        count = counts.get(event, 0)
        of_first = count / first * 100 if first else 0.0
        if previous is None or previous == 0:
            drop = 0.0
        else:
            drop = max(0.0, (previous - count) / previous * 100)
        steps.append(Step(event, label, count, of_first, drop))
        previous = count
    return steps


def worst_drop(steps: list[Step]) -> Step | None:
    """Шаг с самым большим обрывом — с него и начинать чинить."""
    candidates = [step for step in steps[1:] if step.drop_from_previous > 0]
    if not candidates:
        return None
    return max(candidates, key=lambda step: step.drop_from_previous)


def render(steps: list[Step]) -> str:
    width = max((len(step.label) for step in steps), default=10)
    lines = ["", "  ВОРОНКА МАРШРУТА", "  " + "=" * (width + 34), ""]
    for index, step in enumerate(steps):
        bar = "█" * int(round(step.of_first / 5)) if step.of_first > 0 else ""
        drop = (
            f"  -{step.drop_from_previous:5.1f}%"
            if index and step.drop_from_previous
            else " " * 9
        )
        lines.append(
            f"  {step.label:<{width}}  {step.count:>6}  "
            f"{step.of_first:5.1f}%{drop}  {bar}"
        )
    lines.append("")

    if not steps or steps[0].count == 0:
        lines.append("  Данных пока нет: первый шаг воронки ни разу не случился.")
        lines.append("  Проверь, что экспорт содержит события, а не только страницы.")
        return "\n".join(lines) + "\n"

    weakest = worst_drop(steps)
    if weakest is None:
        lines.append("  Обрывов нет — воронка не теряет людей на этих шагах.")
    else:
        lines.append(
            f"  Самый большой обрыв: «{weakest.label}» "
            f"(-{weakest.drop_from_previous:.1f}% от предыдущего шага)."
        )
        lines.append("  По правилу проекта чинить надо именно его, а не следующий.")
    return "\n".join(lines) + "\n"


def read_csv(path: Path) -> tuple[list[dict], list[str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
        header = list(reader.fieldnames or [])
    return rows, header


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Воронка по экспорту GoatCounter")
    parser.add_argument("csv", type=Path, help="CSV-экспорт из GoatCounter")
    parser.add_argument("--json", action="store_true", help="Машинный вывод")
    parser.add_argument(
        "--stages",
        help="Свои шаги через запятую вместо маршрута по умолчанию",
    )
    args = parser.parse_args(argv)

    if not args.csv.exists():
        print(f"Файл не найден: {args.csv}", file=sys.stderr)
        return 1

    rows, header = read_csv(args.csv)
    try:
        counts = count_events(rows, header)
    except ValueError as error:
        print(str(error), file=sys.stderr)
        return 1

    if args.stages:
        stages = tuple((name.strip(), name.strip()) for name in args.stages.split(","))
    else:
        stages = DEFAULT_STAGES

    steps = build_funnel(counts, stages)
    if args.json:
        weakest = worst_drop(steps)
        print(
            json.dumps(
                {
                    "steps": [
                        {
                            "event": step.event,
                            "label": step.label,
                            "count": step.count,
                            "of_first_percent": round(step.of_first, 1),
                            "drop_from_previous_percent": round(
                                step.drop_from_previous, 1
                            ),
                        }
                        for step in steps
                    ],
                    "worst_drop": weakest.event if weakest else None,
                },
                ensure_ascii=False,
                indent=2,
            )
        )
    else:
        print(render(steps))
    return 0


if __name__ == "__main__":
    sys.exit(main())
