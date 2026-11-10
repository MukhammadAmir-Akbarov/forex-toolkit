#!/usr/bin/env python3
"""Генератор данных для тултипов глоссария в главах.

Парсит _mkdocs/extras/glossary{,.en,.uz}.md и складывает по одному JSON на
локаль: _mkdocs/data/glossary-terms.{ru,en,uz}.json вида

    [{"term": "Безубыток", "short": "Закрытие сделки в ноль…"}, …]

Эти файлы читает виджет javascripts/widgets/glossary-tooltips.js: он
подчёркивает термины точками прямо в тексте глав и показывает короткое
определение при наведении/фокусе. JSON закоммичены в репозиторий — это данные,
а не артефакт сборки; после правки glossary*.md скрипт нужно перезапустить.

Формат исходника (единый для трёх локалей):
  * записи — параграфы «**Термин (Alias, Alias2)** — определение.» внутри
    секций «## Буква»;
  * в конце — таблицы «| **СОКР** | Расшифровка | Перевод |» (у UZ есть ещё
    таблица локальных терминов, поэтому у uz-локали терминов больше).

Из заголовка записи извлекаются все формы термина: основная («Откат»),
алиасы из скобок («Pullback», «Retracement») и варианты через « / »
(«Flat / Range»). Записи-отсылки («см. Пипс», «see ECN», «ECN ga qarang»)
разрешаются в определение цели; если цель не нашлась — запись пропускается.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCES = {
    "ru": ROOT / "_mkdocs" / "extras" / "glossary.md",
    "en": ROOT / "_mkdocs" / "extras" / "glossary.en.md",
    "uz": ROOT / "_mkdocs" / "extras" / "glossary.uz.md",
}
LOCALES = tuple(SOURCES)
OUT_DIR = ROOT / "_mkdocs" / "data"

# Верхний предел длины подсказки: тултип — не статья. Тест держит ту же границу.
MAX_SHORT = 300

# «**Термин (Алиас)** — определение.» — записи начинаются с жирного заголовка.
ENTRY_RE = re.compile(r"^\*\*(?P<head>.+?)\*\*\s*—\s*(?P<body>.+?)\s*$")
# «| **ATR** | Average True Range | Средний истинный диапазон |» — таблицы сокращений.
ROW_RE = re.compile(r"^\|\s*\*\*(?P<term>.+?)\*\*\s*\|(?P<cells>.*)$")
# Заголовок записи: основная форма + необязательные алиасы в скобках.
HEAD_RE = re.compile(r"^(?P<main>[^()]+?)(?:\s*\((?P<paren>[^()]*)\))?\s*$")

# Записи-отсылки на другой термин, по локали: «см. Пипс.», «see Pip above.»,
# «ECN ga qarang.».
SEE_RES = {
    "ru": re.compile(r"^см\.?\s+(?P<target>.+?)\.?$", re.IGNORECASE),
    "en": re.compile(
        r"^see\s+(?P<target>.+?)(?:\s+(?:above|below))?\.?$", re.IGNORECASE
    ),
    "uz": re.compile(r"^(?P<target>.+?)\s+ga\s+qarang\.?$", re.IGNORECASE),
}


def strip_md(text: str) -> str:
    """Убирает markdown-разметку из определения: жирный, курсив, код, ссылки."""
    text = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", text)  # [текст](url) → текст
    return text.replace("**", "").replace("__", "").replace("`", "").strip()


def split_head(head: str) -> list[str]:
    """Все формы термина из заголовка записи.

    «Откат (Pullback, Retracement)» → [Откат, Pullback, Retracement];
    «Flat / Range» → [Flat, Range]. Дробь без пробелов («Risk/Reward») —
    один термин, её не трогаем.
    """
    match = HEAD_RE.match(head.strip())
    if not match:
        return []
    parts = match.group("main").split(" / ")
    if match.group("paren"):
        parts.extend(match.group("paren").split(","))
    return [part.strip() for part in parts if part.strip()]


def shorten(body: str) -> str:
    """Определение для тултипа: чистый текст, не длиннее MAX_SHORT."""
    short = strip_md(body)
    if len(short) <= MAX_SHORT:
        return short
    cut = short[: MAX_SHORT - 1]
    # Режем по границе предложения, если она не слишком близко к началу.
    dot = max(cut.rfind(". "), cut.rfind("! "), cut.rfind("? "))
    if dot > MAX_SHORT // 2:
        return cut[: dot + 1]
    return cut.rstrip(" ,;:") + "…"


def _entries(text: str) -> list[tuple[list[str], str]]:
    """Сырые записи файла: (формы термина, определение) в порядке следования."""
    found: list[tuple[list[str], str]] = []
    for line in text.splitlines():
        entry = ENTRY_RE.match(line)
        if entry:
            terms = split_head(entry.group("head"))
            if terms:
                found.append((terms, entry.group("body")))
            continue
        row = ROW_RE.match(line)
        if row:
            cells = [c.strip() for c in row.group("cells").split("|") if c.strip()]
            if len(cells) < 2:
                continue
            full, meaning = cells[0], cells[1]
            short = (
                meaning
                if full.lower() == row.group("term").lower()
                else f"{full} — {meaning}"
            )
            found.append((split_head(row.group("term")), short))
    return found


def parse_terms(text: str, lang: str) -> list[dict[str, str]]:
    """Готовый список терминов локали: дедупликация и разрешение отсылок."""
    raw = _entries(text)
    # Сначала собираем полные определения — на них ссылаются записи «см. …».
    definitions: dict[str, str] = {}
    for terms, body in raw:
        if SEE_RES[lang].match(body):
            continue
        for term in terms:
            definitions.setdefault(term.lower(), body)

    seen: set[str] = set()
    result: list[dict[str, str]] = []
    for terms, body in raw:
        see = SEE_RES[lang].match(body)
        if see:
            target = definitions.get(see.group("target").lower())
            if target is None:
                continue  # отсылка в никуда — пропускаем, а не показываем «см.»
            body = target
        for term in terms:
            key = term.lower()
            if key in seen:
                continue
            seen.add(key)
            result.append({"term": term, "short": shorten(body)})
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out-dir", type=Path, default=OUT_DIR)
    args = parser.parse_args()

    args.out_dir.mkdir(parents=True, exist_ok=True)
    counts: dict[str, int] = {}
    for lang, source in SOURCES.items():
        if not source.exists():
            sys.exit(f"❌ Нет глоссария: {source}")
        terms = parse_terms(source.read_text(encoding="utf-8"), lang)
        out = args.out_dir / f"glossary-terms.{lang}.json"
        out.write_text(
            json.dumps(terms, ensure_ascii=False, indent=1) + "\n", encoding="utf-8"
        )
        counts[lang] = len(terms)
        print(f"✅ {out.relative_to(ROOT)}: {len(terms)} терминов")
    print("Итого: " + ", ".join(f"{lang}={n}" for lang, n in counts.items()))
    return 0


if __name__ == "__main__":
    sys.exit(main())
