"""Тренажёр паттернов в настоящем браузере.

Быстрые сверки в `tests/test_widget_logic.py` гоняют чистые функции виджета в
песочнице Node, где `fetch` заглушён отказом. Значит они НЕ проверяют главного:
что страница вообще получает эпизоды. Путь к данным у трёх локалей разный
(`../../data/…` у русской, `../../../data/…` у en и uz — они на уровень глубже),
и ошибка в нём выглядит не как падение, а как вежливое «не удалось загрузить».

Здесь проверяем то, что видит человек: тренажёр дожил до вопроса, посчитал на
тех же данных, что и пакет, и объяснил исход после ответа.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from forex_toolkit.pattern_outcomes import (
    DEFAULT_HORIZON,
    collect_stats,
    decode_episode,
)

ROOT = Path(__file__).resolve().parent.parent
EPISODES = ROOT / "_mkdocs" / "data" / "replay-episodes.json"

LOCALES = ["", "en/", "uz/"]


def _series() -> list[list[dict]]:
    """Те же эпизоды, что грузит страница, — читаем их из источника сайта."""
    raw = json.loads(EPISODES.read_text(encoding="utf-8"))
    return [decode_episode(episode) for episode in raw["episodes"]]


def _open(page, site_url, prefix):
    page.goto(f"{site_url}/{prefix}tools/pattern-trainer/")
    # Или вопрос, или честное сообщение об ошибке — молча пустым быть не может.
    page.wait_for_selector(".pt-options, .calc-error", timeout=30_000)


@pytest.mark.parametrize("prefix", LOCALES, ids=["ru", "en", "uz"])
def test_trainer_gets_its_data(pw_page, site_url, prefix):
    """Самое дорогое место: относительный путь к эпизодам у каждой локали свой."""
    page = pw_page
    _open(page, site_url, prefix)

    assert page.locator(".calc-error").count() == 0, (
        f"[{prefix or 'ru'}] тренажёр не загрузил эпизоды: "
        f"{page.text_content('.calc-error')}"
    )
    assert page.locator(".pt-options .pt-option").count() >= 2, (
        f"[{prefix or 'ru'}] вопрос не собрался"
    )
    # Свечи показаны — иначе отвечать не на что.
    assert page.locator(".pt-table tbody tr").count() > 0


def test_browser_stats_match_the_package(pw_page, site_url):
    """Доли на странице — те же, что считает `forex_toolkit`, на тех же свечах.

    Одна локаль, а не три: файл виджета для всех локалей один, меняются только
    подписи. Гонять полный архив трижды — платить временем за тот же ответ.
    """
    page = pw_page
    _open(page, site_url, "")

    expected = collect_stats(_series(), horizon=DEFAULT_HORIZON)
    got = page.evaluate(
        f"s => window.__fxPatternStats(s, {DEFAULT_HORIZON})", _series()
    )
    assert got, "браузер не вернул статистику"
    assert set(got) == set(expected), (
        f"разный набор фигур: браузер {sorted(got)}, пакет {sorted(expected)}"
    )

    for key, python in expected.items():
        row = got[key]
        for field in ("found", "worked", "flat"):
            assert row[field] == getattr(python, field), (
                f"{key}: {field} разошлось — браузер {row[field]}, "
                f"пакет {getattr(python, field)}"
            )
        assert round(row["rate"], 6) == round(python.rate, 6), f"{key}: доля разошлась"


def test_answer_explains_the_outcome(pw_page, site_url):
    """Ради этого тренажёр и делался: после ответа видно, чем фигура кончилась.

    Тренажёр, который хвалит за распознавание и молчит про исход, учит ровно
    тому, против чего написана страница.
    """
    page = pw_page
    _open(page, site_url, "")

    # Два вопроса из десяти — «фигуры здесь нет», и для них доли исходов нет по
    # замыслу. Поэтому идём по вопросам до первого с фигурой, а не кликаем
    # наугад: иначе тест падал бы примерно каждый пятый раз.
    explained = 0
    for _ in range(10):
        page.locator(".pt-option").first.click()
        page.wait_for_selector("#pt-next")
        verdict = page.text_content("#pt-verdict")
        assert verdict and verdict.strip(), "после ответа ничего не сказано"

        if page.locator("#pt-verdict h4").count():
            assert "%" in verdict, f"есть разбор фигуры, но нет доли: {verdict!r}"
            assert page.locator(".pt-lesson").count(), "нет напоминания про урок"
            explained += 1
            break
        page.click("#pt-next")
        page.wait_for_selector(".pt-options")

    assert explained, "ни один вопрос не показал исход фигуры"


def test_doji_is_not_asked_but_is_still_reported(pw_page, site_url):
    """Доджи — почти в каждой второй свече, в вопросах он бы забил выборку.

    При этом из статистики его убирать нельзя: он и есть доказательство, что
    «нашёл фигуру» не равно «нашёл сигнал».
    """
    page = pw_page
    _open(page, site_url, "")

    keys = page.eval_on_selector_all(".pt-option", "els => els.map(e => e.dataset.key)")
    assert "doji" not in keys, "доджи попал в варианты ответа"

    got = page.evaluate(
        f"s => window.__fxPatternStats(s, {DEFAULT_HORIZON})", _series()
    )
    assert "doji" in got, "доджи пропал из статистики"
    assert got["doji"]["found"] > 0, "доджи есть в таблице, но ни разу не найден"
