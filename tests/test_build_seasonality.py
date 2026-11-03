"""Сезонность: месячные доходности и статистика ячеек — без файлов и сети.

Проверяем две чистые функции build_seasonality, от которых зависит честность
карты: дыра в данных не должна становиться «доходностью за месяц», а ячейка
без наблюдений обязана быть пустой, а не нулём.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))

from build_seasonality import monthly_returns, seasonality_stats  # noqa: E402


def test_monthly_returns_skip_the_first_month():
    closes = [
        ("2026-01-30", 1.10),
        ("2026-01-31", 1.11),  # последний день января
        ("2026-02-27", 1.155),
    ]

    returns = monthly_returns(closes)

    assert list(returns) == [(2026, 2)]
    assert math.isclose(returns[(2026, 2)], math.log(1.155 / 1.11))


def test_monthly_returns_ignore_gaps_in_data():
    """Пропущенный месяц — не «доходность за месяц», а дыра: пропускаем."""
    closes = [
        ("2026-01-30", 1.0),
        ("2026-03-31", 1.1),  # февраля нет вовсе
        ("2026-04-30", 1.05),
    ]

    returns = monthly_returns(closes)

    assert (2026, 3) not in returns
    assert math.isclose(returns[(2026, 4)], math.log(1.05 / 1.1))


def test_seasonality_stats_median_and_positive_share():
    returns = {
        (2021, 1): math.log(1.02),
        (2022, 1): math.log(1.03),
        (2022, 2): math.log(0.99),  # февраль не мешает январю
    }

    january, february = seasonality_stats(returns)[:2]

    assert january["n"] == 2
    assert january["pos"] == 1.0
    assert math.isclose(january["median"], (1.98 + 2.96) / 2, abs_tol=0.01)
    assert february["n"] == 1 and february["pos"] == 0.0


def test_seasonality_stats_empty_month_is_empty_not_zero():
    stats = seasonality_stats({(2026, 6): 0.01})

    assert stats[4]["n"] == 0
    assert stats[4]["avg"] is None
    assert stats[5]["n"] == 1
