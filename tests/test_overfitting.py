"""Проверка сводки по переобучению.

Числа отсюда попадают на страницу как довод «подбор параметров ловит шум».
Довод обязан быть верным, поэтому проверяем не только счастливый путь, но и то,
что фильтр по числу сделок работает: без него «победителем» станет комбинация с
двумя удачными сделками, и урок развалится.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from forex_toolkit.overfitting import (
    Combo,
    correlation,
    summarize,
    to_combos,
)

ROOT = Path(__file__).resolve().parent.parent
DATASET = ROOT / "_mkdocs" / "data" / "overfitting.json"


def row(name, in_r, out_r, in_trades=50, out_trades=50):
    return {
        "params": {"rr": name},
        "in": {"total_r": in_r, "trades": in_trades},
        "out": {"total_r": out_r, "trades": out_trades},
    }


def test_best_on_the_past_is_not_the_best_on_the_future():
    summary = summarize([row("a", 30.0, -10.0), row("b", 5.0, 12.0)])
    assert summary.best_in.params["rr"] == "a"
    assert summary.best_out.params["rr"] == "b"
    assert summary.rank_out == 2, "лучшая по прошлому должна быть второй по будущему"
    assert summary.degradation == pytest.approx(40.0)


def test_rank_counts_from_one():
    summary = summarize([row("a", 30.0, 99.0), row("b", 5.0, 12.0)])
    assert summary.rank_out == 1


def test_thin_samples_cannot_win():
    """Две удачные сделки не должны становиться «лучшими параметрами»."""
    rows = [
        row("везучая", 99.0, 99.0, in_trades=2, out_trades=2),
        row("настоящая", 10.0, 3.0),
    ]
    summary = summarize(rows, min_trades=20)
    assert summary.considered == 1
    assert summary.best_in.params["rr"] == "настоящая"


def test_nothing_to_compare_returns_none():
    assert summarize([]) is None
    assert summarize([row("a", 1.0, 1.0, in_trades=1, out_trades=1)]) is None


def test_median_is_the_middle_not_the_mean():
    rows = [row("a", 1.0, 0.0), row("b", 2.0, 0.0), row("c", 3.0, 300.0)]
    summary = summarize(rows)
    assert summary.median_out == 0.0
    assert summary.mean_out == pytest.approx(100.0)


def test_correlation_is_zero_when_one_side_never_moves():
    assert correlation([1.0, 1.0, 1.0], [3.0, 7.0, 11.0]) == 0.0
    assert correlation([], []) == 0.0
    assert correlation([1.0], [2.0]) == 0.0


def test_correlation_recognises_a_straight_line():
    assert correlation([1.0, 2.0, 3.0], [2.0, 4.0, 6.0]) == pytest.approx(1.0)
    assert correlation([1.0, 2.0, 3.0], [6.0, 4.0, 2.0]) == pytest.approx(-1.0)


def test_beat_median_is_honest_about_a_loss():
    summary = summarize([row("a", 30.0, -10.0), row("b", 5.0, 12.0)])
    assert summary.beat_median is False


def test_combo_filter_reads_broken_rows_without_crashing():
    combos = to_combos([{}, {"in": None, "out": None}, row("a", 1.0, 1.0)])
    assert len(combos) == 1


def test_dataclass_round_trips_through_as_dict():
    combo = Combo({"rr": 2}, 1.234567, 30, -2.5, 25)
    assert combo.as_dict()["in_total_r"] == 1.235


# ── Настоящий набор, который читает сайт ───────────────────────────────────


@pytest.mark.skipif(not DATASET.exists(), reason="набор ещё не посчитан")
def test_the_shipped_dataset_still_says_what_the_page_claims():
    """Страница утверждает конкретные числа. Если набор пересчитают и вывод
    поменяется, тест должен упасть, а не оставить на сайте старое утверждение.
    """
    document = json.loads(DATASET.read_text(encoding="utf-8"))
    summary = summarize(document["rows"])

    assert summary is not None
    assert summary.best_in.in_total_r > 0, "на прошлом лучшая обязана быть в плюсе"
    assert summary.best_in.out_total_r < 0, (
        "урок страницы: лучшая на прошлом ушла в минус на будущем"
    )
    assert summary.rank_out > summary.considered / 2, (
        "урок страницы: лучшая на прошлом оказалась хуже половины остальных"
    )
    assert abs(summary.correlation) < 0.3, (
        "урок страницы: связи между прошлым и будущим нет"
    )
    assert summary.considered == 54


@pytest.mark.skipif(not DATASET.exists(), reason="набор ещё не посчитан")
def test_dataset_names_its_source():
    """Число без указания пары и периода — это уже не измерение, а лозунг."""
    meta = json.loads(DATASET.read_text(encoding="utf-8"))["meta"]
    for field in ("pair", "timeframe", "from", "split_at", "to", "bars_total"):
        assert meta.get(field), f"в наборе нет поля {field}"
    assert meta["bars_in"] + meta["bars_out"] == meta["bars_total"]
