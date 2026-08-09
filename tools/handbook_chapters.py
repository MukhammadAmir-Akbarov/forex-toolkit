#!/usr/bin/env python3
"""Состав глав печатного учебника на трёх языках.

Вынесено из ``build_pdf.py`` отдельным модулем сознательно: сборка PDF требует
reportlab (extra ``docs``), а состав глав нужно проверять в обычном прогоне
тестов, где стоит только ``dev``. Импорт этого модуля ничего тяжёлого не тянет.

Правило: **порядок и состав задаёт только RU-список**, EN и UZ получаются из
него подстановкой суффикса локали. Раньше три списка писались руками и
разъехались — 14 глав на RU против 3 на EN и 5 на UZ, при том что все переводы
лежали рядом. Проверка живёт в ``tests/test_handbook_chapters.py``.
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "_mkdocs"

LOCALES = ("en", "uz")

# Главы в нужном порядке (RU). Источник — _mkdocs/ (единственный источник правды).
CHAPTERS_RU: list[tuple[str, Path]] = [
    ("Введение", SRC / "КАК-ПОЛЬЗОВАТЬСЯ.md"),
    ("Основной гайд", SRC / "forex-guide.md"),
    ("Технический анализ", SRC / "docs" / "technical-analysis.md"),
    ("Учебная стратегия", SRC / "docs" / "strategy-details.md"),
    ("Психология трейдинга", SRC / "extras" / "psychology.md"),
    ("Глоссарий", SRC / "extras" / "glossary.md"),
    ("FAQ", SRC / "extras" / "faq.md"),
    ("Сравнение брокеров", SRC / "extras" / "brokers-comparison.md"),
    ("Личный торговый план", SRC / "extras" / "trading-plan-template.md"),
    ("Первые 100 дней", SRC / "extras" / "first-100-days.md"),
    ("Anti-Tilt протокол", SRC / "extras" / "anti-tilt-protocol.md"),
    ("Daily Routine", SRC / "extras" / "daily-routine.md"),
    ("Чек-лист", SRC / "extras" / "checklist-printable.md"),
    ("Emergency Card", SRC / "extras" / "emergency-card.md"),
]

# Заголовки глав на EN и UZ. Ключ — русское название из CHAPTERS_RU, поэтому
# новая глава без перевода заголовка сразу видна: её здесь просто нет.
CHAPTER_TITLES: dict[str, dict[str, str]] = {
    "en": {
        "Введение": "How to use",
        "Основной гайд": "Main guide",
        "Технический анализ": "Technical analysis",
        "Учебная стратегия": "The teaching strategy",
        "Психология трейдинга": "Trading psychology",
        "Глоссарий": "Glossary",
        "FAQ": "FAQ",
        "Сравнение брокеров": "Broker comparison",
        "Личный торговый план": "Personal trading plan",
        "Первые 100 дней": "First 100 days",
        "Anti-Tilt протокол": "Anti-tilt protocol",
        "Daily Routine": "Daily routine",
        "Чек-лист": "Checklist",
        "Emergency Card": "Emergency card",
    },
    "uz": {
        "Введение": "Qanday foydalanish",
        "Основной гайд": "Asosiy qo'llanma",
        "Технический анализ": "Texnik tahlil",
        "Учебная стратегия": "O'quv strategiyasi",
        "Психология трейдинга": "Treyding psixologiyasi",
        "Глоссарий": "Lug'at",
        "FAQ": "Savol-javob",
        "Сравнение брокеров": "Brokerlarni taqqoslash",
        "Личный торговый план": "Shaxsiy savdo rejasi",
        "Первые 100 дней": "Birinchi 100 kun",
        "Anti-Tilt протокол": "Anti-Tilt protokoli",
        "Daily Routine": "Kunlik tartib",
        "Чек-лист": "Tekshiruv ro'yxati",
        "Emergency Card": "Favqulodda karta",
    },
}


def translated_path(ru_path: Path, lang: str) -> Path:
    """`extras/faq.md` + `uz` -> `extras/faq.uz.md` (суффиксный режим i18n)."""
    return ru_path.with_name(f"{ru_path.stem}.{lang}.md")


def chapters(lang: str) -> list[tuple[str, Path]]:
    """Список глав для локали: тот же порядок, что RU, но файлы перевода."""
    if lang == "ru":
        return list(CHAPTERS_RU)
    titles = CHAPTER_TITLES[lang]
    return [
        (titles.get(ru_title, ru_title), translated_path(ru_path, lang))
        for ru_title, ru_path in CHAPTERS_RU
    ]
