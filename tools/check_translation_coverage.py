#!/usr/bin/env python3
"""Отчёт о покрытии переводов сайта.

RU — дефолтная локаль: каждый «исходник» — это ``page.md`` в ``_mkdocs/``.
Перевод лежит рядом суффиксом: ``page.en.md`` / ``page.uz.md``
(режим ``docs_structure: suffix`` плагина mkdocs-static-i18n).

Скрипт считает, у скольких RU-страниц есть EN- и UZ-версии, печатает проценты
и список непереведённых. Заменяет ручной подсчёт «RU 52 / EN 12 / UZ 9» в
TODO.md и служит мягким индикатором приоритета №1 (переводы) в CI.

Запуск:
    python tools/check_translation_coverage.py
    python tools/check_translation_coverage.py --locale uz --fail-under 25

Коды возврата:
    0 — по умолчанию (информационный режим) или порог выполнен;
    1 — задан ``--fail-under`` и покрытие указанной локали ниже порога.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MKDOCS = ROOT / "_mkdocs"

# Локали-переводы (RU — дефолтная, у неё суффикса нет).
LOCALES = ("en", "uz")


def locale_of(path: Path) -> str | None:
    """Локаль файла по суффиксу (``page.en.md`` → ``en``), иначе None (RU)."""
    for loc in LOCALES:
        if path.name.endswith(f".{loc}.md"):
            return loc
    return None


def sibling(src: Path, loc: str) -> Path:
    """Путь перевода для RU-исходника: ``page.md`` → ``page.<loc>.md``."""
    return src.with_name(src.name[:-3] + f".{loc}.md")


def main() -> int:
    parser = argparse.ArgumentParser(description="Покрытие переводов _mkdocs/")
    parser.add_argument(
        "--locale",
        choices=LOCALES,
        default=None,
        help="Локаль для проверки порога (по умолчанию — только отчёт).",
    )
    parser.add_argument(
        "--fail-under",
        type=float,
        default=None,
        help="Вернуть код 1, если покрытие --locale ниже этого процента.",
    )
    args = parser.parse_args()

    all_md = sorted(MKDOCS.rglob("*.md"))
    ru_sources = [p for p in all_md if locale_of(p) is None]

    # Сироты-переводы: есть page.en.md, но нет page.md — повод проверить.
    orphans: list[Path] = []
    for p in all_md:
        loc = locale_of(p)
        if loc is not None:
            base = p.with_name(p.name[: -len(f".{loc}.md")] + ".md")
            if base not in set(ru_sources):
                orphans.append(p)

    total = len(ru_sources)
    print(f"📄 RU-страниц (исходников): {total}\n")

    coverage: dict[str, float] = {}
    for loc in LOCALES:
        have = [s for s in ru_sources if sibling(s, loc).exists()]
        missing = [s for s in ru_sources if not sibling(s, loc).exists()]
        pct = (len(have) / total * 100) if total else 0.0
        coverage[loc] = pct
        head = f"🌐 {loc.upper()}: {len(have)}/{total} ({pct:.0f}%)"
        print(f"{head} — не хватает {len(missing)}")
        for s in missing:
            print(f"     ✗ {s.relative_to(MKDOCS)}")
        print()

    if orphans:
        print("⚠️  Переводы без RU-исходника (проверь имя файла):")
        for o in orphans:
            print(f"     {o.relative_to(MKDOCS)}")
        print()

    if args.fail_under is not None:
        loc = args.locale or "uz"
        pct = coverage.get(loc, 0.0)
        thr = f"{args.fail_under:.0f}%"
        cur = f"{loc.upper()} {pct:.0f}%"
        if pct < args.fail_under:
            print(f"❌ Покрытие {cur} < порога {thr}")
            return 1
        print(f"✅ Покрытие {cur} ≥ порога {thr}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
