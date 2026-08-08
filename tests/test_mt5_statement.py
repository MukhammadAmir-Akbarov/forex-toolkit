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


# ─────────────── Разбор недоверенного ввода: чужие отчёты ───────────────
# Отчёт приходит от постороннего брокера, поэтому ветки разбора чисел, дат и
# направления — прямой риск исказить сумму сделки. До этих тестов они не были
# покрыты: модуль показывал 89%.


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        # Американский формат: запятая — разделитель тысяч.
        ("1,234.56", 1234.56),
        # Европейский: наоборот. Перепутать их — ошибиться в 1000 раз.
        ("1.234,56", 1234.56),
        ("1234,56", 1234.56),
        # Разделители тысяч, которые ставят разные терминалы.
        ("1 234,56", 1234.56),
        ("1'234.56", 1234.56),
        ("12 345.67", 12345.67),
        ("0,5", 0.5),
        # Убыток в скобках — так пишут в бухгалтерских выгрузках.
        ("(45.20)", -45.2),
        # Пустое и нечисловое не должно ронять импорт всего отчёта.
        ("", 0.0),
        ("   ", 0.0),
        ("n/a", 0.0),
        ("-", 0.0),
    ],
)
def test_number_understands_both_decimal_conventions(raw, expected):
    from forex_toolkit.mt5_statement import _number

    assert _number(raw) == pytest.approx(expected)


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        ("in", "in"),
        ("вход", "in"),
        ("out", "out"),
        ("выход", "out"),
        # Закрытие встречным ордером — тоже выход, иначе сделка не сойдётся.
        ("out by", "out"),
        ("close by", "out"),
        ("выход встречным", "out"),
        ("in/out", "inout"),
        ("разворот", "inout"),
        ("мусор", ""),
    ],
)
def test_entry_direction_covers_localised_and_close_by_deals(raw, expected):
    from forex_toolkit.mt5_statement import _entry

    assert _entry(raw) == expected


def test_unsupported_time_names_the_offending_value():
    from forex_toolkit.mt5_statement import _timestamp

    with pytest.raises(MT5StatementError, match="не дата"):
        _timestamp("не дата")


def _deals_table(rows: str) -> str:
    header = (
        "<tr><th colspan='14'>Deals</th></tr>"
        "<tr><th>Time</th><th>Deal</th><th>Symbol</th><th>Type</th>"
        "<th>Direction</th><th>Volume</th><th>Price</th><th>Order</th>"
        "<th>Commission</th><th>Fee</th><th>Swap</th><th>Profit</th>"
        "<th>Balance</th><th>Comment</th></tr>"
    )
    return f"<html><body><table>{header}{rows}</table></body></html>"


def test_open_position_is_reported_as_a_warning_not_a_silent_drop():
    """Незакрытая позиция не попадает в журнал — про неё надо сказать вслух."""
    html = _deals_table(
        "<tr><td>2026.06.01 09:10:00</td><td>1</td><td>EURUSD</td><td>buy</td>"
        "<td>in</td><td>0.10</td><td>1.10000</td><td>1</td><td>0</td><td>0</td>"
        "<td>0</td><td>0</td><td></td><td></td></tr>"
        "<tr><td>2026.06.01 10:00:00</td><td>2</td><td>EURUSD</td><td>sell</td>"
        "<td>out</td><td>0.04</td><td>1.10200</td><td>2</td><td>0</td><td>0</td>"
        "<td>0</td><td>8.00</td><td></td><td></td></tr>"
    )

    result = parse_mt5_html(html)

    assert len(result.trades) == 1
    assert any("open position" in w for w in result.warnings), result.warnings


def test_report_without_a_single_closed_trade_is_rejected():
    """Открытых позиций мало — импортировать нечего, и это ошибка, не тишина."""
    html = _deals_table(
        "<tr><td>2026.06.01 09:10:00</td><td>1</td><td>EURUSD</td><td>buy</td>"
        "<td>in</td><td>0.10</td><td>1.10000</td><td>1</td><td>0</td><td>0</td>"
        "<td>0</td><td>0</td><td></td><td></td></tr>"
    )

    with pytest.raises(MT5StatementError, match="No completed trades"):
        parse_mt5_html(html)


def test_path_and_html_string_give_the_same_result():
    from_path = parse_mt5_html(FIXTURE)
    from_text = parse_mt5_html(FIXTURE.read_text(encoding="utf-8"))

    assert from_path.trades == from_text.trades
