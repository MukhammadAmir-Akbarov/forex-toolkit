#!/usr/bin/env python3
"""Страж «свежести фактов» для региональных/срочных страниц.

Закон, налоги, брокеры, вывод денег в Узбекистане меняются — устаревший совет
опасен (был инцидент с незаконным P2P). Решение: помечать такие страницы в
front-matter датой проверки::

    ---
    verified: 2026-06-11
    ---

Скрипт читает все ``_mkdocs/**/*.md``, собирает ``verified``-даты и предупреждает,
если факт старше N месяцев (по умолчанию 6). По умолчанию — информационно
(код 0); с ``--fail`` валит CI при протухших или отсутствующих метках.

Запуск:
    python tools/check_freshness.py
    python tools/check_freshness.py --max-age-months 6 --fail
"""

from __future__ import annotations

import argparse
import datetime as dt
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MKDOCS = ROOT / "_mkdocs"

# Разделы, где свежесть критична (для подсказки о недостающих verified-метках).
# extras/brokers-comparison и extras/market-data-sources стареют так же быстро,
# как uz/ (M2): лицензии, спреды и ссылки меняются без предупреждения.
SENSITIVE_PREFIXES = (
    "uz/",
    "extras/brokers-comparison",
    "extras/market-data-sources",
)

# Витринные данные (K2): числа на витринах пересчитываются
# tools/rebuild_showcase_data.py и несут generated_at. Без гейта они устарели
# бы молча — читатель смотрел бы на «свежий пример» двухлетней давности.
SHOWCASE_DATA = (
    "overfitting.json",
    "multipair.json",
    "strategies.json",
    "replay-episodes.json",
)


def parse_front_matter(text: str) -> dict:
    """Минимальный парсер YAML-front-matter (нам нужен только ключ verified)."""
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end == -1:
        return {}
    meta: dict[str, str] = {}
    for line in text[3:end].splitlines():
        if ":" in line:
            key, _, val = line.partition(":")
            meta[key.strip()] = val.strip().strip("'\"")
    return meta


def as_date(value: str) -> dt.date | None:
    try:
        return dt.date.fromisoformat(value)
    except (ValueError, TypeError):
        return None


def months_between(old: dt.date, new: dt.date) -> int:
    return (new.year - old.year) * 12 + (new.month - old.month)


def main() -> int:
    parser = argparse.ArgumentParser(description="Проверка свежести verified-страниц")
    parser.add_argument("--max-age-months", type=int, default=6)
    parser.add_argument(
        "--fail",
        action="store_true",
        help="Вернуть код 1 при старых или отсутствующих verified-метках.",
    )
    args = parser.parse_args()

    today = dt.date.today()
    verified: list[tuple[Path, dt.date]] = []
    sensitive_without: list[Path] = []

    for md in sorted(MKDOCS.rglob("*.md")):
        rel = md.relative_to(MKDOCS)
        meta = parse_front_matter(md.read_text(encoding="utf-8"))
        date = as_date(meta.get("verified", ""))
        if date is not None:
            verified.append((md, date))
        elif str(rel).startswith(SENSITIVE_PREFIXES):
            sensitive_without.append(rel)

    hdr = f"verified-страниц: {len(verified)} (порог {args.max_age_months} мес.)"
    print(f"🗓️  {hdr}\n")
    stale: list[tuple[Path, int]] = []
    for md, date in verified:
        age = months_between(date, today)
        mark = "⚠️ " if age >= args.max_age_months else "✓ "
        print(f"  {mark}{date}  ({age} мес.)  {md.relative_to(MKDOCS)}")
        if age >= args.max_age_months:
            stale.append((md, age))

    if sensitive_without:
        print("\nℹ️  Региональные страницы без verified-метки (желательно добавить):")
        for rel in sensitive_without:
            print(f"     {rel}")

    # Витринные JSON: стареют по generated_at, пересборка — rebuild_showcase_data.py
    import json

    showcase_stale: list[str] = []
    showcase_unstamped: list[str] = []
    data_dir = MKDOCS / "data"
    for name in SHOWCASE_DATA:
        path = data_dir / name
        if not path.exists():
            showcase_unstamped.append(name)
            continue
        doc = json.loads(path.read_text(encoding="utf-8"))
        stamp = as_date(
            str(doc.get("meta", {}).get("generated_at") or doc.get("generated_at", ""))
        )
        if stamp is None:
            showcase_unstamped.append(name)
            continue
        age = months_between(stamp, today)
        mark = "⚠️ " if age >= args.max_age_months else "✓ "
        print(f"  {mark}{stamp}  ({age} мес.)  data/{name}")
        if age >= args.max_age_months:
            showcase_stale.append(name)
    if showcase_unstamped:
        print(
            "\n⚠️  Витрины без generated_at (пересобери: "
            "tools/rebuild_showcase_data.py): " + ", ".join(showcase_unstamped)
        )
    if showcase_stale:
        print("⚠️  Протухшие витрины (пересобери): " + ", ".join(showcase_stale))

    if stale:
        n, m = len(stale), args.max_age_months
        print(f"\n⚠️  Протухших страниц: {n} (старше {m} мес.) — перепроверь факты.")
    if args.fail and (
        stale or sensitive_without or showcase_stale or showcase_unstamped
    ):
        return 1
    else:
        print("\n✅ Все verified-страницы и витрины свежие.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
