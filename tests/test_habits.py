"""Стоимость привычек за период.

Число в долларах убеждает там, где процент не убеждает, — но именно поэтому
оно обязано быть честным: не показывать привычку по двум сделкам и не выдавать
наблюдаемую разницу за доказанную причину.
"""

from __future__ import annotations

import pytest

from forex_toolkit.habits import (
    MIN_TRADES,
    expensive_habits,
    month_of,
    months_in,
    trades_of_month,
)


def trade(
    date="2026-03-01", pnl=10.0, rules="yes", emotion="calm", pair="EURUSD", setup="a"
):
    return {
        "date": date,
        "pnl": pnl,
        "rules": rules,
        "emotion": emotion,
        "pair": pair,
        "setup": setup,
    }


def test_broken_rules_cost_is_measured_against_your_own_norm():
    """Сравниваем не с нулём, а с тем, как человек торгует, соблюдая план."""
    trades = [trade(pnl=10.0) for _ in range(5)]
    trades += [trade(pnl=-20.0, rules="no") for _ in range(3)]

    habits = expensive_habits(trades)
    broken = next(h for h in habits if h.key == "broke_rules")

    assert broken.trades == 3
    assert broken.avg_with == pytest.approx(-20.0)
    assert broken.avg_without == pytest.approx(10.0)
    # (-20 - 10) * 3 = -90
    assert broken.cost == pytest.approx(-90.0)


def test_a_habit_with_too_few_trades_is_not_reported():
    """Одна неудачная сделка сделала бы «самой дорогой» любую привычку."""
    trades = [trade(pnl=10.0) for _ in range(10)]
    trades += [trade(pnl=-500.0, rules="no") for _ in range(MIN_TRADES - 1)]

    assert all(h.key != "broke_rules" for h in expensive_habits(trades))


def test_profitable_habit_is_not_called_expensive():
    """Список называется «дорогие привычки» — хвалить должен другой блок."""
    trades = [trade(pnl=1.0) for _ in range(5)]
    trades += [trade(pnl=50.0, emotion="fomo") for _ in range(4)]

    assert all(h.key != "traded_tense" for h in expensive_habits(trades))


def test_habits_come_back_worst_first_and_capped():
    trades = [trade(pnl=10.0) for _ in range(8)]
    trades += [trade(pnl=-30.0, rules="no") for _ in range(3)]
    trades += [trade(pnl=-5.0, emotion="fomo") for _ in range(3)]

    habits = expensive_habits(trades, limit=3)

    assert len(habits) <= 3
    assert habits == sorted(habits, key=lambda h: h.cost)


def test_worst_pair_counts_as_a_habit():
    """Выбор инструмента — тоже привычка, просто выраженная иначе."""
    trades = [trade(pnl=12.0, pair="EURUSD") for _ in range(6)]
    trades += [trade(pnl=-40.0, pair="GBPJPY") for _ in range(4)]

    keys = [h.key for h in expensive_habits(trades)]

    assert "pair:GBPJPY" in keys


def test_nothing_to_report_when_every_trade_shares_the_habit():
    """Без группы сравнения разница неизмерима — молчим, а не выдумываем."""
    trades = [trade(pnl=-10.0, rules="no") for _ in range(6)]

    assert all(h.key != "broke_rules" for h in expensive_habits(trades))


@pytest.mark.parametrize("broken_pnl", [None, "мусор", float("nan")])
def test_unreadable_amounts_are_skipped_not_zeroed(broken_pnl):
    trades = [trade(pnl=10.0) for _ in range(5)]
    trades += [trade(pnl=-20.0, rules="no") for _ in range(3)]
    trades += [trade(pnl=broken_pnl, rules="no")]

    broken = next(h for h in expensive_habits(trades) if h.key == "broke_rules")

    assert broken.trades == 3


def test_empty_journal_reports_nothing():
    assert expensive_habits([]) == []


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("2026-03-14", "2026-03"),
        ("2026-12-31", "2026-12"),
        ("2026-13-01", None),
        ("не дата", None),
        ("", None),
        (None, None),
    ],
)
def test_month_parsing_rejects_nonsense(value, expected):
    assert month_of(value) == expected


def test_months_come_back_newest_first():
    trades = [
        trade(date="2026-01-10"),
        trade(date="2026-03-02"),
        trade(date="2025-12-31"),
    ]

    assert months_in(trades) == ["2026-03", "2026-01", "2025-12"]


def test_trades_of_month_does_not_leak_neighbours():
    trades = [
        trade(date="2026-02-28"),
        trade(date="2026-03-01"),
        trade(date="2026-03-31"),
    ]

    assert len(trades_of_month(trades, "2026-03")) == 2
