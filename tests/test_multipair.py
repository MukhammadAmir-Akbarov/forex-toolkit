"""Проверка сводки по переносу настройки между парами.

Вывод страницы держится на трёх числах: сколько пар осталось в плюсе, каков
разброс и у скольких пар свои лучшие параметры. Отдельно проверяем то, на чём
я уже ошибся один раз: пара, где сделок почти не было, НЕ должна выглядеть
результатом. Первый прогон показывал такие пары как «+0.0R», и пара с четырьмя
сделками попадала в «в плюсе».
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from forex_toolkit.multipair import summarize, to_results

ROOT = Path(__file__).resolve().parent.parent
DATASET = ROOT / "_mkdocs" / "data" / "multipair.json"

HOME = {"rr": 3.0, "stop_buffer": 5}


def pair(name, transferred, own_r, own_params=None, trades=40):
    return {
        "pair": name,
        "transferred": {"total_r": transferred, "trades": trades},
        "own_best": {
            "params": HOME if own_params is None else own_params,
            "result": {} if own_r is None else {"total_r": own_r},
        },
    }


def document(*pairs, home_params=None):
    return {
        "meta": {"home_pair": "EURUSD", "home_params": home_params or HOME},
        "pairs": list(pairs),
    }


def test_best_and_worst_are_by_the_transferred_result():
    summary = summarize(
        document(
            pair("EURUSD", 30.0, 30.0),
            pair("GBPUSD", -12.0, 8.0, {"rr": 1.5}),
            pair("USDJPY", 4.0, 9.0, {"rr": 2.0}),
        )
    )
    assert summary.best.pair == "EURUSD"
    assert summary.worst.pair == "GBPUSD"
    assert summary.spread == pytest.approx(42.0)


def test_profitable_counts_only_the_plus():
    summary = summarize(
        document(pair("A", 1.0, 1.0), pair("B", 0.0, 1.0), pair("C", -1.0, 1.0))
    )
    assert summary.profitable == 1, "ноль — не прибыль"
    assert summary.pairs == 3


def test_a_pair_with_almost_no_trades_is_not_a_result():
    """Главный урок прошлой ошибки: «мало сделок» ≠ «ноль».

    Пара с четырьмя сделками не может ни попасть в «в плюсе», ни оказаться
    худшей: она вообще не участвовала в измерении.
    """
    summary = summarize(
        document(
            pair("EURUSD", 20.0, 20.0),
            pair("USDJPY", 4.0, None, {}, trades=4),
        ),
        min_trades=20,
    )
    assert summary.measurable == 1
    assert summary.thin == 1
    assert summary.profitable == 1, "пара с 4 сделками не должна считаться прибыльной"
    assert summary.worst.pair == "EURUSD", "непосчитанная пара не может быть худшей"

    thin = next(r for r in summary.results if r.pair == "USDJPY")
    assert thin.enough is False
    assert thin.own_best_r is None, "нет достаточной выборки — нет и числа"
    assert thin.gap is None
    assert thin.as_dict()["own_best_r"] is None


def test_everything_thin_returns_none():
    assert summarize(document(pair("A", 1.0, None, {}, trades=3))) is None


def test_own_params_differ_ignores_pairs_without_a_best():
    summary = summarize(
        document(
            pair("EURUSD", 30.0, 30.0),
            pair("GBPUSD", -12.0, 8.0, {"rr": 1.5}),
            pair("USDJPY", 4.0, None, {}, trades=4),
        )
    )
    assert summary.own_params_differ == 1, "пустые параметры — не «другие параметры»"


def test_gap_shows_the_price_of_fitting_each_pair():
    summary = summarize(document(pair("GBPUSD", -12.0, 8.0, {"rr": 1.5})))
    assert summary.results[0].gap == pytest.approx(20.0)


def test_home_pair_is_found_by_name():
    summary = summarize(document(pair("EURUSD", 30.0, 30.0), pair("A", 1.0, 1.0)))
    assert summary.home is not None and summary.home.pair == "EURUSD"


def test_median_of_an_even_number_of_pairs():
    summary = summarize(
        document(
            pair("A", 1.0, 1.0),
            pair("B", 3.0, 1.0),
            pair("C", 5.0, 1.0),
            pair("D", 11.0, 1.0),
        )
    )
    assert summary.median_r == pytest.approx(4.0)


def test_broken_entries_do_not_crash_the_report():
    results = to_results({"pairs": [{}, {"pair": "X"}, pair("A", 1.0, 1.0)]})
    assert len(results) == 3
    assert results[0].transferred_r == 0.0


def test_nothing_to_compare_returns_none():
    assert summarize({}) is None
    assert summarize({"pairs": []}) is None


# ── Настоящий набор, который читает сайт ───────────────────────────────────


@pytest.mark.skipif(not DATASET.exists(), reason="набор ещё не посчитан")
def test_the_shipped_dataset_still_says_what_the_page_claims():
    summary = summarize(json.loads(DATASET.read_text(encoding="utf-8")))

    assert summary is not None
    assert summary.pairs >= 6, "меньше шести пар — вывод о переносе слабый"
    assert summary.thin == 0, (
        "все пары обязаны быть измеримыми: пустая выборка означает ошибку "
        "измерения, а не свойство рынка (см. размер пункта у иеновых пар)"
    )
    assert summary.home is not None, "опорной пары нет в наборе"

    # Урок страницы: разброс между парами больше, чем сам результат опорной.
    assert summary.spread > abs(summary.home.transferred_r), (
        "разброс между парами должен быть заметнее результата опорной пары"
    )
    # Урок страницы: у большинства пар свои лучшие параметры.
    assert summary.own_params_differ > summary.pairs / 2, (
        "у большинства пар лучшие параметры должны отличаться от опорных"
    )
    # Урок страницы: подгонка под пару обещает заметно больше, чем перенос.
    gaps = [r.gap for r in summary.results if r.gap is not None]
    assert sum(gaps) > 0, "подгонка под пару обязана выглядеть красивее переноса"


@pytest.mark.skipif(not DATASET.exists(), reason="набор ещё не посчитан")
def test_jpy_pairs_were_measured_with_their_own_pip():
    """Защита от повторения моей ошибки.

    Первый прогон шёл с общим размером пункта 0.0001, и на иеновых парах
    выходило 0–4 сделки за два года. Это выглядело как вывод про рынок, а было
    ошибкой измерения. Здесь проверяем и сам размер пункта, и его следствие.
    """
    document_ = json.loads(DATASET.read_text(encoding="utf-8"))
    for entry in document_["pairs"]:
        if entry["pair"].upper().endswith("JPY"):
            assert entry.get("pip_size") == 0.01, entry["pair"]
            assert entry["transferred"]["trades"] > 20, (
                f"{entry['pair']}: сделок почти нет — похоже, пункт снова общий"
            )
