#!/usr/bin/env python3
"""Детектор дрейфа переводов: свежи ли ``.en.md``/``.uz.md`` относительно RU.

``check_translation_coverage.py`` проверяет *наличие* переводов; этот скрипт —
их *свежесть*. Манифест ``tools/i18n-manifest.json`` хранит sha256 RU-файла,
под который был сделан каждый перевод. Если RU-страницу поправили, а перевод
не обновили (и не пере-синхронизировали манифест) — перевод помечается
устаревшим. Это «страховка свежести» под 177 локализованных файлов (59×3):
``--strict`` сборка и coverage-гейт такой дрейф не ловят.

Рабочий цикл:
    1. Правишь ``_mkdocs/page.md``.
    2. ``python tools/check_translation_drift.py`` показывает page.en/uz как ❌ stale.
    3. Обновляешь переводы, затем фиксируешь:
       ``python tools/sync_translation_manifest.py --file page.md``.

Запуск:
    python tools/check_translation_drift.py                  # отчёт (код 0)
    python tools/check_translation_drift.py --fail-on-drift  # код 1 при дрейфе

Коды возврата:
    0 — нет устаревших переводов, либо информационный режим;
    1 — задан ``--fail-on-drift`` и найдены устаревшие переводы (или нет манифеста).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MKDOCS = ROOT / "_mkdocs"
MANIFEST = ROOT / "tools" / "i18n-manifest.json"

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


def sha256_of(path: Path) -> str:
    """sha256 содержимого файла (как есть, по байтам)."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def ru_sources() -> list[Path]:
    """Все RU-исходники в ``_mkdocs/`` (``.md`` без локального суффикса)."""
    return [p for p in sorted(MKDOCS.rglob("*.md")) if locale_of(p) is None]


def main() -> int:
    parser = argparse.ArgumentParser(description="Дрейф переводов _mkdocs/")
    parser.add_argument(
        "--fail-on-drift",
        action="store_true",
        help="Вернуть код 1, если есть устаревшие переводы.",
    )
    args = parser.parse_args()

    if not MANIFEST.exists():
        print("⚠️  Манифеста нет: tools/i18n-manifest.json")
        print("    Создай его: python tools/sync_translation_manifest.py --all")
        return 1 if args.fail_on_drift else 0

    entries = json.loads(MANIFEST.read_text(encoding="utf-8")).get("entries", {})

    stale: list[str] = []
    untracked_pages: list[str] = []
    untracked_trans: list[str] = []
    fresh = 0

    sources = ru_sources()
    for src in sources:
        rel = src.relative_to(MKDOCS).as_posix()
        cur = sha256_of(src)
        entry = entries.get(rel)
        if entry is None:
            # переводы есть, а страницы нет в манифесте — её надо засинкать
            if any(sibling(src, loc).exists() for loc in LOCALES):
                untracked_pages.append(rel)
            continue
        synced = entry.get("locales", {})
        for loc in LOCALES:
            if not sibling(src, loc).exists():
                continue
            synced_sha = synced.get(loc)
            if synced_sha is None:
                untracked_trans.append(f"{rel} [{loc}]")
            elif synced_sha != cur:
                stale.append(f"{rel} [{loc}]")
            else:
                fresh += 1

    # записи манифеста, у которых пропал RU-файл
    existing = {p.relative_to(MKDOCS).as_posix() for p in sources}
    ghost = [rel for rel in entries if rel not in existing]

    print(f"🔄 Свежих переводов: {fresh}")

    if stale:
        print(f"\n❌ Устаревшие переводы ({len(stale)}) — RU изменился после перевода:")
        for s in stale:
            print(f"     {s}")
        print(
            "    Обнови перевод, затем: "
            "python tools/sync_translation_manifest.py --file <page.md>"
        )
    if untracked_pages:
        print(f"\n⚠️  RU-страницы без записи в манифесте ({len(untracked_pages)}):")
        for s in untracked_pages:
            print(f"     {s}")
        print("    Добавь: python tools/sync_translation_manifest.py --all")
    if untracked_trans:
        print(f"\n⚠️  Переводы без отметки синхронизации ({len(untracked_trans)}):")
        for s in untracked_trans:
            print(f"     {s}")
    if ghost:
        print(f"\n⚠️  Записи манифеста без RU-файла ({len(ghost)}) — почисти `--all`:")
        for s in ghost:
            print(f"     {s}")

    if not (stale or untracked_pages or untracked_trans or ghost):
        print("✅ Все переводы свежие и отслеживаются.")

    return 1 if (args.fail_on_drift and stale) else 0


if __name__ == "__main__":
    sys.exit(main())
