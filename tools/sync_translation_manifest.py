#!/usr/bin/env python3
"""Синхронизация манифеста переводов ``tools/i18n-manifest.json``.

Отмечает текущие переводы как «сделанные под текущий RU-исходник» — пишет
sha256 RU-файла в манифест. Запускай после того, как перевёл/обновил страницы:
тогда ``check_translation_drift.py`` перестанет считать их устаревшими.

Запуск:
    python tools/sync_translation_manifest.py --all
        пересобрать весь манифест по текущему состоянию (первичный backfill
        и периодическая чистка «призрачных» записей);
    python tools/sync_translation_manifest.py --file docs/strategy-details.md
        отметить все существующие переводы одной страницы свежими;
    python tools/sync_translation_manifest.py --file page.md --locale en
        отметить свежим только EN (когда обновил лишь один язык).

Путь к файлу — относительно ``_mkdocs/`` (как в отчётах coverage/drift).
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

LOCALES = ("en", "uz")

_COMMENT = (
    "sha256 RU-исходника, под который сделаны переводы. "
    "Обновить: python tools/sync_translation_manifest.py. "
    "Проверка свежести: python tools/check_translation_drift.py."
)


def locale_of(path: Path) -> str | None:
    for loc in LOCALES:
        if path.name.endswith(f".{loc}.md"):
            return loc
    return None


def sibling(src: Path, loc: str) -> Path:
    return src.with_name(src.name[:-3] + f".{loc}.md")


def sha256_of(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def ru_sources() -> list[Path]:
    return [p for p in sorted(MKDOCS.rglob("*.md")) if locale_of(p) is None]


def load_entries() -> dict:
    if not MANIFEST.exists():
        return {}
    return json.loads(MANIFEST.read_text(encoding="utf-8")).get("entries", {})


def write_entries(entries: dict) -> None:
    payload = {"_comment": _COMMENT, "version": 1, "entries": entries}
    MANIFEST.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def sync_one(entries: dict, rel: str, only_locale: str | None) -> int:
    """Засинкать одну RU-страницу. Возвращает число обновлённых локалей."""
    src = MKDOCS / rel
    if locale_of(src) is not None:
        print(f"❌ Это перевод, а не RU-исходник: {rel}")
        return -1
    if not src.exists():
        print(f"❌ Нет файла: _mkdocs/{rel}")
        return -1
    cur = sha256_of(src)
    entry = entries.setdefault(rel, {"ru_sha256": cur, "locales": {}})
    entry["ru_sha256"] = cur
    locs = [only_locale] if only_locale else list(LOCALES)
    updated = 0
    for loc in locs:
        if sibling(src, loc).exists():
            entry["locales"][loc] = cur
            updated += 1
        elif only_locale:
            print(f"⚠️  Нет перевода {loc} для {rel} — пропуск.")
    return updated


def rebuild_all(entries: dict) -> tuple[int, int]:
    """Пересобрать манифест с нуля по текущему состоянию диска."""
    new: dict = {}
    pages = 0
    trans = 0
    for src in ru_sources():
        rel = src.relative_to(MKDOCS).as_posix()
        cur = sha256_of(src)
        locales = {loc: cur for loc in LOCALES if sibling(src, loc).exists()}
        new[rel] = {"ru_sha256": cur, "locales": locales}
        pages += 1
        trans += len(locales)
    entries.clear()
    entries.update(new)
    return pages, trans


def main() -> int:
    parser = argparse.ArgumentParser(description="Синк манифеста переводов")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--all", action="store_true", help="Пересобрать весь манифест.")
    group.add_argument(
        "--file", metavar="REL", help="RU-страница относительно _mkdocs/."
    )
    parser.add_argument(
        "--locale",
        choices=LOCALES,
        default=None,
        help="С --file: отметить свежим только эту локаль.",
    )
    args = parser.parse_args()

    entries = load_entries()

    if args.all:
        pages, trans = rebuild_all(entries)
        write_entries(entries)
        print(
            f"✅ Манифест пересобран: {pages} RU-страниц, "
            f"{trans} переводов отмечены свежими."
        )
        return 0

    updated = sync_one(entries, args.file, args.locale)
    if updated < 0:
        return 1
    write_entries(entries)
    print(f"✅ Засинкано: {args.file} ({updated} локал(и) отмечены свежими).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
