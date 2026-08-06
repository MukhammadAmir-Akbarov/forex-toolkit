"""Воронка по экспорту GoatCounter: подсчёт, обрывы и устойчивость к форматам."""

from __future__ import annotations

from pathlib import Path

import pytest
from funnel_report import (
    DEFAULT_STAGES,
    build_funnel,
    count_events,
    main,
    read_csv,
    render,
    worst_drop,
)

HITS = """Path,Title,Event,Bot,Date
/first15_completed,,true,0,2026-08-01
/first15_completed,,true,0,2026-08-01
/calculator_completed,,true,0,2026-08-02
/trade_plan_saved,,true,0,2026-08-02
"""

SUMMARY = """path,count
first15_completed,100
calculator_completed,60
trade_plan_saved,30
trade_plan_opened,6
trade_review_completed,3
"""


def write(tmp_path: Path, name: str, body: str) -> Path:
    path = tmp_path / name
    path.write_text(body, encoding="utf-8")
    return path


def test_counts_each_hit_row_as_one_event(tmp_path: Path) -> None:
    rows, header = read_csv(write(tmp_path, "hits.csv", HITS))
    counts = count_events(rows, header)
    assert counts["first15_completed"] == 2
    assert counts["calculator_completed"] == 1


def test_uses_the_count_column_when_the_export_is_a_summary(tmp_path: Path) -> None:
    rows, header = read_csv(write(tmp_path, "summary.csv", SUMMARY))
    counts = count_events(rows, header)
    assert counts["first15_completed"] == 100
    assert counts["trade_review_completed"] == 3


def test_leading_slash_and_bom_do_not_split_the_same_event(tmp_path: Path) -> None:
    body = "﻿path,count\n/calculator_completed,5\ncalculator_completed,5\n"
    rows, header = read_csv(write(tmp_path, "bom.csv", body))
    assert count_events(rows, header)["calculator_completed"] == 10


def test_missing_event_column_is_reported_clearly() -> None:
    with pytest.raises(ValueError, match="нет колонки с событием"):
        count_events([{"Browser": "Firefox"}], ["Browser"])


def test_funnel_reports_conversion_and_drop() -> None:
    counts = {
        "first15_completed": 100,
        "calculator_completed": 60,
        "trade_plan_saved": 30,
        "trade_plan_opened": 6,
        "trade_review_completed": 3,
    }
    steps = build_funnel(counts)
    assert [step.count for step in steps] == [100, 60, 30, 6, 3]
    assert steps[1].of_first == pytest.approx(60.0)
    assert steps[1].drop_from_previous == pytest.approx(40.0)
    # 30 -> 6 теряет 80%: самый крупный обрыв, его и надо чинить.
    assert steps[3].drop_from_previous == pytest.approx(80.0)
    assert worst_drop(steps).event == "trade_plan_opened"


def test_stage_that_never_happened_counts_as_zero() -> None:
    steps = build_funnel({"first15_completed": 10})
    assert steps[1].count == 0
    assert steps[1].drop_from_previous == pytest.approx(100.0)


def test_empty_data_does_not_divide_by_zero() -> None:
    steps = build_funnel({})
    assert all(step.count == 0 for step in steps)
    assert all(step.of_first == 0 for step in steps)
    assert worst_drop(steps) is None
    assert "Данных пока нет" in render(steps)


def test_render_names_the_worst_step() -> None:
    text = render(build_funnel({"first15_completed": 100, "calculator_completed": 10}))
    assert "Самый большой обрыв" in text
    assert "Посчитал позицию" in text


def test_cli_prints_json_and_flags_the_worst_drop(tmp_path, capsys) -> None:
    path = write(tmp_path, "summary.csv", SUMMARY)
    assert main([str(path), "--json"]) == 0
    payload = capsys.readouterr().out
    assert '"worst_drop": "trade_plan_opened"' in payload


def test_cli_reports_a_missing_file(tmp_path, capsys) -> None:
    assert main([str(tmp_path / "nope.csv")]) == 1
    assert "не найден" in capsys.readouterr().err


def test_custom_stages_override_the_default_route(tmp_path, capsys) -> None:
    path = write(tmp_path, "summary.csv", SUMMARY)
    assert main([str(path), "--stages", "trade_plan_saved,trade_plan_opened"]) == 0
    out = capsys.readouterr().out
    assert "trade_plan_saved" in out
    assert "Прошёл" not in out


def test_default_route_starts_from_the_first_fifteen_minutes() -> None:
    assert DEFAULT_STAGES[0][0] == "first15_completed"
