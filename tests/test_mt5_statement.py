from __future__ import annotations

import csv
from argparse import Namespace
from pathlib import Path

import pytest

from forex_toolkit.mt5_statement import (
    MT5StatementError,
    parse_mt5_html,
    write_journal_csv,
)

FIXTURE = Path(__file__).parent / "fixtures" / "mt5-statement.html"


def test_parse_mt5_html_matches_partial_closes_and_costs():
    result = parse_mt5_html(FIXTURE)

    assert len(result.trades) == 3
    assert result.warnings == []

    first, second, third = result.trades
    assert first["pair"] == "EURUSD"
    assert first["direction"] == "long"
    assert float(first["lot_size"]) == pytest.approx(0.04)
    assert float(first["result_pips"]) == pytest.approx(20)
    assert float(first["result_usd"]) == pytest.approx(7.5)
    assert first["outcome"] == "win"

    assert float(second["lot_size"]) == pytest.approx(0.06)
    assert float(second["result_usd"]) == pytest.approx(-3.6)
    assert second["outcome"] == "loss"

    assert third["pair"] == "GBPUSD"
    assert third["direction"] == "short"
    assert float(third["result_pips"]) == pytest.approx(10)
    assert float(third["result_usd"]) == pytest.approx(17.5)


def test_write_journal_csv_is_compatible(tmp_path):
    result = parse_mt5_html(FIXTURE)
    output = write_journal_csv(result.trades, tmp_path / "imported.csv")

    with output.open(encoding="utf-8") as file:
        rows = list(csv.DictReader(file))
    assert len(rows) == 3
    assert rows[0]["entry_price"] == "1.1"
    assert rows[0]["close_price"] == "1.102"
    assert rows[0]["close_time"] == "2026-06-01 10:15"


def test_parse_mt5_html_rejects_unknown_report():
    with pytest.raises(MT5StatementError, match="No MT5 deals table"):
        parse_mt5_html("<html><table><tr><td>Orders</td></tr></table></html>")


def test_journal_cli_import_mt5(tmp_path):
    import journal_cli

    output = tmp_path / "from-cli.csv"
    code = journal_cli.cmd_import_mt5(Namespace(report=str(FIXTURE), out=output))

    assert code == 0
    with output.open(encoding="utf-8") as file:
        assert len(list(csv.DictReader(file))) == 3
