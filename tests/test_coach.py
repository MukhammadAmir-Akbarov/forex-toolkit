from __future__ import annotations

import csv
import subprocess
import sys
from pathlib import Path

from forex_toolkit.coach import analyze_trades, load_journal

ROOT = Path(__file__).resolve().parent.parent


def trade(
    index: int,
    *,
    hour: int,
    pair: str,
    pnl: float,
    rules: str,
) -> dict[str, str]:
    return {
        "id": str(index),
        "date": f"2026-07-{index:02d}",
        "time": f"{hour:02d}:00",
        "pair": pair,
        "result_usd": str(pnl),
        "risk_usd": "10",
        "outcome": "win" if pnl > 0 else "loss" if pnl < 0 else "be",
        "followed_rules": rules,
    }


def problem_journal() -> list[dict[str, str]]:
    rows = [
        trade(
            i,
            hour=19,
            pair="GBPUSD",
            pnl=-10,
            rules="no" if i <= 3 else "yes",
        )
        for i in range(1, 7)
    ]
    rows.extend(
        [
            trade(7, hour=10, pair="EURUSD", pnl=12, rules="yes"),
            trade(8, hour=11, pair="EURUSD", pnl=8, rules="yes"),
            trade(9, hour=12, pair="EURUSD", pnl=-10, rules="yes"),
            trade(10, hour=13, pair="EURUSD", pnl=-10, rules="yes"),
        ]
    )
    return rows


def test_analyze_prioritizes_three_personal_rules():
    report = analyze_trades(problem_journal())

    assert report.trade_count == 10
    assert [rule.code for rule in report.rules] == [
        "anti_tilt",
        "discipline",
        "evening_limit",
    ]
    assert "2 сделки" in report.rules[0].evidence
    assert "70.0%" in report.rules[1].evidence
    assert "6 сделок" in report.rules[2].evidence


def test_analyze_detects_consistently_weak_pair_without_inventing_alerts():
    rows = [trade(i, hour=10, pair="GBPUSD", pnl=-5, rules="yes") for i in range(1, 6)]
    rows.extend(
        trade(i, hour=11, pair="EURUSD", pnl=10, rules="yes") for i in range(6, 11)
    )

    report = analyze_trades(rows)

    assert report.rules[0].code == "weak_pair"
    assert report.rules[0].title == "Убери GBPUSD на 2 недели"
    assert len(report.rules) == 3
    assert "anti_tilt" not in {rule.code for rule in report.rules}


def test_load_journal_ignores_open_trades(tmp_path):
    path = tmp_path / "journal.csv"
    rows = problem_journal()
    rows.append(
        {
            **trade(11, hour=14, pair="USDJPY", pnl=0, rules="yes"),
            "outcome": "open",
            "result_usd": "",
        }
    )
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    assert len(load_journal(path)) == 10


def test_coach_cli_prints_exactly_three_rules(tmp_path):
    path = tmp_path / "journal.csv"
    rows = problem_journal()
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "advanced" / "coach_bot.py"),
            "analyze",
            "--csv",
            str(path),
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    assert result.stdout.count("\n1. ") == 1
    assert result.stdout.count("\n2. ") == 1
    assert result.stdout.count("\n3. ") == 1
    assert "\n4. " not in result.stdout
