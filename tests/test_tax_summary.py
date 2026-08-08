"""Годовой итог для декларации.

Число отсюда человек переписывает в декларацию, поэтому проверяем не только
happy path, но и то, что журнал не теряет записи молча и не превращает
убыточный год в отрицательный налог.
"""

from __future__ import annotations

import pytest

from forex_toolkit.tax_summary import (
    DEFAULT_RATE,
    declaration_deadline,
    summarize_all,
    summarize_year,
)

TRADES = [
    {"date": "2025-03-04", "pnl": 300.0},
    {"date": "2025-06-18", "pnl": -120.0},
    {"date": "2025-11-02", "pnl": 45.5},
    {"date": "2026-01-09", "pnl": -80.0},
    {"date": "2026-02-14", "pnl": 200.0},
]


def test_net_result_is_profits_minus_losses():
    """Декларируется чистый годовой результат, а не сумма прибыльных сделок."""
    year = summarize_year(TRADES, 2025)

    assert year.trades == 3
    assert year.profit == pytest.approx(345.5)
    assert year.loss == pytest.approx(120.0)
    assert year.net == pytest.approx(225.5)
    assert year.tax == pytest.approx(225.5 * DEFAULT_RATE)


def test_losing_year_owes_nothing_and_never_goes_negative():
    """Отрицательный налог — бессмыслица, а перенос убытка правила не дают."""
    losing = summarize_year([{"date": "2025-05-01", "pnl": -500.0}], 2025)

    assert losing.net == pytest.approx(-500.0)
    assert losing.taxable == 0.0
    assert losing.tax == 0.0


def test_trades_from_other_years_do_not_leak_in():
    year = summarize_year(TRADES, 2026)

    assert year.trades == 2
    assert year.net == pytest.approx(120.0)


@pytest.mark.parametrize(
    "broken",
    [
        {"date": "2025-07-01", "pnl": None},
        {"date": "2025-07-01", "pnl": "не число"},
        {"date": "2025-07-01", "pnl": float("nan")},
        {"date": "2025-07-01"},
    ],
)
def test_unreadable_amount_is_counted_as_skipped_not_as_zero(broken):
    """Битую запись надо показать пользователю, а не тихо посчитать нулём."""
    year = summarize_year([{"date": "2025-01-01", "pnl": 100.0}, broken], 2025)

    assert year.trades == 1
    assert year.skipped == 1
    assert year.net == pytest.approx(100.0)


@pytest.mark.parametrize("bad_date", ["", None, "не дата", "20-05-2025", "0001-01-01"])
def test_unreadable_date_drops_out_of_every_year(bad_date):
    assert summarize_all([{"date": bad_date, "pnl": 100.0}]) == []


def test_years_come_back_newest_first():
    years = [item.year for item in summarize_all(TRADES)]

    assert years == [2026, 2025]


def test_rate_is_configurable_because_the_law_changes():
    year = summarize_year(TRADES, 2025, rate=0.15)

    assert year.tax == pytest.approx(225.5 * 0.15)


def test_negative_rate_is_rejected():
    with pytest.raises(ValueError, match="отрицательной"):
        summarize_year(TRADES, 2025, rate=-0.1)


def test_deadline_is_the_first_of_april_next_year():
    assert declaration_deadline(2025) == "2026-04-01"


def test_zero_pnl_counts_as_a_trade_but_moves_nothing():
    """Сделка в ноль — это сделка: она должна быть в счётчике."""
    year = summarize_year([{"date": "2025-01-01", "pnl": 0.0}], 2025)

    assert year.trades == 1
    assert year.profit == 0.0
    assert year.loss == 0.0
    assert year.net == 0.0


def test_as_dict_rounds_money_to_cents():
    year = summarize_year([{"date": "2025-01-01", "pnl": 10.005}], 2025)

    assert year.as_dict()["profit"] == 10.0 or year.as_dict()["profit"] == 10.01
    assert isinstance(year.as_dict()["trades"], int)
