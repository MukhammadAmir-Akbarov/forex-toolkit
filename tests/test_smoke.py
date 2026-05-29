"""Смоук-тесты: модули импортируются без падений, базовая математика верна,
инструменты используют общий fx_math.

Дёшевы, но ловят целый класс багов — например поломку импорта, из-за которой
раньше не работал установленный wheel CLI.
"""
from __future__ import annotations

import importlib

import pytest

# Модули инструментов, которые должны импортироваться в окружении [dev]
# (без опциональных reportlab/python-docx и без Windows-only MetaTrader5).
IMPORTABLE_TOOLS = [
    "pip_calculator",
    "position_calculator",
    "multi_position_sizer",
    "margin_calculator",
    "compound_calculator",
    "risk_exposure",
    "risk_profile",
    "broker_check",
    "journal_cli",
    "monte_carlo",
    "news_scraper",
    "market_correlations",
]

PACKAGE_MODULES = [
    "forex_toolkit",
    "forex_toolkit.cli",
    "forex_toolkit.fx_math",
    "forex_toolkit.indicators",
    "forex_toolkit.candles",
    "forex_toolkit.position_calculator",
]


@pytest.mark.parametrize("mod", PACKAGE_MODULES)
def test_package_module_imports(mod):
    assert importlib.import_module(mod) is not None


@pytest.mark.parametrize("mod", IMPORTABLE_TOOLS)
def test_tool_module_imports(mod):
    """Импорт не должен падать (ловит import-time ошибки)."""
    importlib.import_module(mod)


def test_cli_commands_callable():
    from forex_toolkit import cli

    for name in (
        "position_calculator", "backtest", "journal", "risk_profile",
        "broker_check", "news", "correlations", "monte_carlo",
    ):
        assert callable(getattr(cli, name))


def test_fx_math_consistency():
    from forex_toolkit import fx_math

    assert fx_math.pip_size("EURUSD") == 0.0001
    assert fx_math.pip_size("USDJPY") == 0.01
    assert fx_math.normalize_pair("eur/usd") == "EURUSD"
    assert fx_math.pip_value_in_quote(1.0, "EURUSD") == 10.0
    assert fx_math.calc_lots(10, 25, 10) == 0.04
    assert fx_math.calc_lots(10, 0, 10) == 0.0


def test_tools_use_shared_fx_math():
    """Калькуляторы должны брать формулы из fx_math — страж против дублей."""
    import multi_position_sizer
    import pip_calculator
    from forex_toolkit import fx_math

    assert multi_position_sizer.calc_lots is fx_math.calc_lots
    assert pip_calculator.pip_size is fx_math.pip_size
    assert pip_calculator.pip_value_in_quote is fx_math.pip_value_in_quote
