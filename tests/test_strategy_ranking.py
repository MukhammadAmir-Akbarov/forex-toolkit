"""Проверка устойчивости рейтинга стратегий.

Страница утверждает, что порядок стратегий не переносится из прошлого в
будущее. Утверждение держится на ранговой корреляции, а её легко посчитать
неправильно на равных значениях — тогда порядок объявления стратегий начнёт
влиять на результат. Это проверяется отдельно.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from forex_toolkit.strategy_ranking import (
    _ranks,
    rank_correlation,
    summarize,
    to_results,
)

ROOT = Path(__file__).resolve().parent.parent
DATASET = ROOT / "_mkdocs" / "data" / "strategies.json"


def strategy(name, past, future, past_trades=50, future_trades=50):
    return {
        "name": name,
        "past": {"total_r": past, "trades": past_trades},
        "future": {"total_r": future, "trades": future_trades},
    }


def document(*strategies):
    return {"meta": {}, "strategies": list(strategies)}


def test_ranks_start_at_one_and_go_by_descending_value():
    assert _ranks([10.0, 5.0, 1.0]) == [1, 2, 3]
    assert _ranks([1.0, 5.0, 10.0]) == [3, 2, 1]


def test_equal_values_share_an_average_place():
    """Иначе порядок объявления стратегий влиял бы на связь."""
    assert _ranks([5.0, 5.0, 1.0]) == [1.5, 1.5, 3]
    assert _ranks([9.0, 5.0, 5.0]) == [1, 2.5, 2.5]


def test_identical_order_gives_one():
    assert rank_correlation([3.0, 2.0, 1.0], [30.0, 20.0, 10.0]) == pytest.approx(1.0)


def test_reversed_order_gives_minus_one():
    assert rank_correlation([3.0, 2.0, 1.0], [10.0, 20.0, 30.0]) == pytest.approx(-1.0)


def test_no_variation_gives_zero_instead_of_dividing_by_zero():
    assert rank_correlation([1.0, 1.0, 1.0], [3.0, 2.0, 1.0]) == 0.0
    assert rank_correlation([], []) == 0.0
    assert rank_correlation([1.0], [2.0]) == 0.0


def test_best_of_the_past_can_be_last_in_the_future():
    summary = summarize(
        document(
            strategy("A", 30.0, -10.0),
            strategy("B", 20.0, 5.0),
            strategy("C", 10.0, 40.0),
        )
    )
    assert summary.best_past.name == "A"
    assert summary.best_future.name == "C"
    assert summary.best_past_rank_future == 3
    assert summary.kept_place == 1, "место сохранила только средняя"
    assert summary.rank_correlation == pytest.approx(-1.0)
    assert summary.order_held is False


def test_thin_strategies_are_skipped_not_counted_as_zero():
    summary = summarize(
        document(
            strategy("A", 30.0, 10.0),
            strategy("B", 20.0, 5.0),
            strategy("редкая", 99.0, 99.0, past_trades=3, future_trades=3),
        ),
        min_trades=20,
    )
    assert summary.considered == 2
    assert summary.skipped == 1
    assert summary.best_past.name == "A", "стратегия с тремя сделками не может выиграть"


def test_less_than_two_strategies_is_not_a_comparison():
    assert summarize(document(strategy("A", 1.0, 1.0))) is None
    assert summarize(document()) is None


def test_order_held_uses_a_stated_threshold():
    high = summarize(document(strategy("A", 3.0, 30.0), strategy("B", 1.0, 10.0)))
    assert high.rank_correlation == pytest.approx(1.0)
    assert high.order_held is True


def test_broken_entries_are_skipped_without_crashing():
    kept, skipped = to_results({"strategies": [{}, strategy("A", 1.0, 1.0)]})
    assert [r.name for r in kept] == ["A"]
    assert skipped == 1


# ── Настоящий набор, который читает сайт ───────────────────────────────────


@pytest.mark.skipif(not DATASET.exists(), reason="набор ещё не посчитан")
def test_the_shipped_dataset_still_says_what_the_page_claims():
    summary = summarize(json.loads(DATASET.read_text(encoding="utf-8")))

    assert summary is not None
    assert summary.considered >= 5, "меньше пяти стратегий — сравнение слабое"
    assert summary.skipped == 0, (
        "стратегия без сделок означает ошибку измерения, а не её свойство "
        "(см. временной индекс у london_open)"
    )
    assert summary.order_held is False, (
        "урок страницы: порядок стратегий не переносится в будущее"
    )
    assert summary.best_past_rank_future > 1, (
        "урок страницы: лучшая на прошлом не осталась лучшей"
    )


@pytest.mark.skipif(not DATASET.exists(), reason="набор ещё не посчитан")
def test_every_strategy_actually_traded():
    """Защита от повторения ошибки с london_open.

    Стратегия, которая молча вернула пустой список из-за неправильного индекса,
    выглядит в отчёте как «не нашла сигналов». Ноль сделок при 12 тысячах
    свечей — это признак поломки инструмента, а не свойство стратегии.
    """
    document_ = json.loads(DATASET.read_text(encoding="utf-8"))
    for entry in document_["strategies"]:
        for half in ("past", "future"):
            assert entry[half]["trades"] > 0, (
                f"{entry['name']}: ноль сделок на половине «{half}» — "
                "похоже, стратегия не получила нужных данных"
            )
