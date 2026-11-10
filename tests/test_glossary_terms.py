"""Данные тултипов глоссария: tools/build_glossary_terms.py → data JSON.

Глоссарий (_mkdocs/extras/glossary{,.en,.uz}.md) — единственный источник
терминов; JSON — производные данные, закоммиченные в репозиторий, которые
читает виджет javascripts/widgets/glossary-tooltips.js. Тесты здесь ловят
два класса тихих поломок: JSON, забытый при перегенерации после правки
глоссария (файлы не существуют / не парсятся / пустые), и дрейф локалей
(в одну локаль добавили записи, в другие — нет).

Почему число ТЕРМИНОВ между локалями не совпадает, а число ЗАПИСЕЙ — да:
русские и узбекские записи почти всегда несут английский алиас в скобках
(«Откат (Pullback, Retracement)» → 3 термина), английские — почти никогда,
поэтому ru ≈ 1.6 × en. А у узбекской локали есть дополнительная таблица
«Mahalliy o'zbekcha atamalar» (20 строк), которой нет в ru/en. Всё это —
свойство исходника, а не генератора, поэтому сравниваем записи строго,
а термины — с осмысленным допуском.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

from build_glossary_terms import (  # noqa: E402
    LOCALES,
    MAX_SHORT,
    SOURCES,
    _entries,
    parse_terms,
)

DATA = ROOT / "_mkdocs" / "data"

# Отношение самой «алиасной» локали к самой лаконичной. Сейчас 240/150 = 1.6;
# запас нужен, чтобы правка одной записи не роняла тест, но потеря половины
# локали — падала.
TERM_COUNT_RATIO = 1.8
# Узбекская локаль держит свою таблицу локальных терминов — записей больше,
# чем в ru/en, ровно на её размер (сейчас 20 строк; допуск — на правки).
UZ_EXTRA_ENTRIES_TOLERANCE = 30


def load(locale: str) -> list[dict]:
    return json.loads(
        (DATA / f"glossary-terms.{locale}.json").read_text(encoding="utf-8")
    )


@pytest.fixture(scope="module", params=sorted(LOCALES))
def terms(request) -> list[dict]:
    return load(request.param)


def test_json_exists_and_parses_for_every_locale() -> None:
    for locale in LOCALES:
        path = DATA / f"glossary-terms.{locale}.json"
        assert path.exists(), f"{path} — запусти tools/build_glossary_terms.py"
        data = json.loads(path.read_text(encoding="utf-8"))
        assert isinstance(data, list) and data, f"{path}: пустой или не список"


def test_every_term_is_well_formed(terms: list[dict]) -> None:
    for item in terms:
        assert set(item) == {"term", "short"}, f"лишние поля: {item}"
        assert item["term"].strip(), "пустой term"
        assert item["short"].strip(), f"пустой short у {item['term']}"
        assert len(item["short"]) <= MAX_SHORT, (
            f"short длиннее {MAX_SHORT}: {item['term']}"
        )


def test_terms_are_unique_within_locale(terms: list[dict]) -> None:
    """Виджет матчит регистронезависимо — дубли создают гонку определений."""
    lowered = [item["term"].lower() for item in terms]
    dupes = {t for t in lowered if lowered.count(t) > 1}
    assert not lowered or not dupes, f"дубли терминов: {sorted(dupes)}"


def test_locales_have_the_same_number_of_source_entries() -> None:
    """Записи глоссария должны добавляться во все локали одновременно."""
    counts = {
        lang: len(_entries(path.read_text(encoding="utf-8")))
        for lang, path in SOURCES.items()
    }
    assert counts["ru"] == counts["en"], (
        f"ru/en разъехались: {counts} — добавь запись в обе локали"
    )
    extra = counts["uz"] - counts["ru"]
    assert 0 <= extra <= UZ_EXTRA_ENTRIES_TOLERANCE, (
        f"uz отличается от ru на {extra} записей ({counts}); ожидаем только "
        f"таблицу «Mahalliy o'zbekcha atamalar» (≤ {UZ_EXTRA_ENTRIES_TOLERANCE})"
    )


def test_locales_have_close_term_counts() -> None:
    counts = {lang: len(load(lang)) for lang in LOCALES}
    ratio = max(counts.values()) / min(counts.values())
    assert ratio <= TERM_COUNT_RATIO, (
        f"локали разъехались сильнее алиасной асимметрии: {counts} "
        f"(ratio {ratio:.2f} > {TERM_COUNT_RATIO})"
    )


def test_parser_extracts_main_form_and_aliases() -> None:
    text = (
        "## О\n\n"
        "**Откат (Pullback, Retracement)** — временное движение против тренда.\n\n"
        "**Флэт / Range** — боковое движение без явного тренда.\n"
    )
    parsed = parse_terms(text, "ru")
    assert [item["term"] for item in parsed] == [
        "Откат",
        "Pullback",
        "Retracement",
        "Флэт",
        "Range",
    ]
    assert all("движение" in item["short"] for item in parsed)


def test_parser_resolves_see_references() -> None:
    """«Точечный (Pip) — см. Пипс.» наследует определение «Пипса»."""
    text = (
        "**Пипс (Pip)** — стандартная единица изменения цены.\n\n"
        "**Точечный (Pip)** — см. Пипс.\n\n"
        "**Призрак** — см. Несуществующий.\n"
    )
    parsed = {item["term"]: item["short"] for item in parse_terms(text, "ru")}
    assert parsed["Точечный"].startswith("стандартная единица")
    # Отсылка в никуда не должна попадать в данные.
    assert "Призрак" not in parsed
    # «Pip» встречается в двух записях — остаётся один, от полного определения.
    assert [t for t in parsed if t.lower() == "pip"] == ["Pip"]


def test_parser_strips_markdown_from_definitions() -> None:
    text = "**Усреднение (Averaging down)** — рост убыточной позиции. **Опасно.**\n"
    item, alias = parse_terms(text, "ru")
    assert item["term"] == "Усреднение" and alias["term"] == "Averaging down"
    assert "**" not in item["short"] and item["short"].endswith("Опасно.")


def test_parser_reads_abbreviation_tables() -> None:
    text = (
        "| Сокр. | Расшифровка | Перевод |\n"
        "|---|---|---|\n"
        "| **ATR** | Average True Range | Средний истинный диапазон |\n"
    )
    (item,) = parse_terms(text, "ru")
    assert item["term"] == "ATR"
    assert item["short"] == "Average True Range — Средний истинный диапазон"
