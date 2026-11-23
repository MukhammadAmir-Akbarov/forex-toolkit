"""Челлендж 30 дней в кабинете: подсчёт дней по fx-activity-v1.

Логика (``window.__fxChallenge`` в dashboard.js) выполняется в Node-песочнице.
"""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
WIDGET = ROOT / "_mkdocs" / "javascripts" / "widgets" / "dashboard.js"
SANDBOX = ROOT / "tests" / "widget_sandbox.mjs"

pytestmark = pytest.mark.skipif(shutil.which("node") is None, reason="нет node")


def _state(start: str, days: list[str], today: str) -> dict:
    done = subprocess.run(
        ["node", str(SANDBOX), str(WIDGET), "__fxChallenge", "-", "ru"],
        input=json.dumps([start, days, today]),
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert done.returncode == 0, done.stderr
    payload = json.loads(done.stdout)
    assert "error" not in payload, payload["error"]
    return payload["result"]


def test_counts_done_missed_today_future() -> None:
    s = _state("2026-11-01", ["2026-11-01", "2026-11-03"], "2026-11-04")
    assert s["day"] == 4 and s["done"] == 2 and not s["finished"]
    assert s["cells"][:5] == ["done", "missed", "done", "today", "future"]
    assert len(s["cells"]) == 30


def test_activity_outside_window_is_ignored() -> None:
    s = _state("2026-11-10", ["2026-11-09", "2026-12-10", "2026-11-10"], "2026-11-10")
    assert s["done"] == 1 and s["day"] == 1


def test_crosses_month_and_finishes_after_day_30() -> None:
    days = ["2026-10-31", "2026-11-29"]  # день 1 и день 30
    s = _state("2026-10-31", days, "2026-11-30")
    assert s["finished"] and s["day"] == 31
    assert s["done"] == 2 and s["cells"][29] == "done"
