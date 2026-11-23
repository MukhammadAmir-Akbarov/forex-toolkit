"""Достижения в кабинете: пороги значков и самая длинная серия дней.

Логика (``window.__fxBadges`` и ``window.__fxLongestStreak`` в dashboard.js)
выполняется в Node-песочнице, как в ``test_challenge_widget.py``.
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

ZERO = {
    "pages": 0,
    "progressPct": 0,
    "quizPassed": 0,
    "quizTotal": 21,
    "examPassed": False,
    "maxStreak": 0,
    "flashLearned": 0,
    "drillBest": 0,
    "profile": None,
    "replayTrades": 0,
    "journalTrades": 0,
    "discipline": 0,
}


def _call(fn: str, *args):
    done = subprocess.run(
        ["node", str(SANDBOX), str(WIDGET), fn, "-", "ru"],
        input=json.dumps(list(args)),
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert done.returncode == 0, done.stderr
    payload = json.loads(done.stdout)
    assert "error" not in payload, payload["error"]
    return payload["result"]


def _unlocked(**overrides) -> set[str]:
    return {b["id"] for b in _call("__fxBadges", {**ZERO, **overrides}) if b["ok"]}


def test_fresh_user_has_nothing_and_every_badge_is_translated() -> None:
    badges = _call("__fxBadges", ZERO)
    ids = [b["id"] for b in badges]
    assert len(ids) == len(set(ids)) == 14
    assert not any(b["ok"] for b in badges)
    src = WIDGET.read_text(encoding="utf-8")
    for badge_id in ids:
        assert src.count(f"        {badge_id}: [") == 3, f"{badge_id}: нужны RU/EN/UZ"


@pytest.mark.parametrize(
    ("at", "below", "badge"),
    [
        ({"pages": 1}, {}, "firstPage"),
        ({"progressPct": 50}, {"progressPct": 49.9}, "halfGuide"),
        ({"progressPct": 100}, {"progressPct": 99.9}, "fullGuide"),
        ({"quizPassed": 1}, {}, "firstQuiz"),
        ({"quizPassed": 21}, {"quizPassed": 20}, "allQuizzes"),
        ({"examPassed": True}, {}, "exam"),
        ({"maxStreak": 7}, {"maxStreak": 6}, "week"),
        ({"maxStreak": 30}, {"maxStreak": 29}, "month"),
        ({"flashLearned": 50}, {"flashLearned": 49}, "cards"),
        ({"drillBest": 9}, {"drillBest": 8}, "drill"),
        ({"profile": {"percent": 10}}, {}, "profile"),
        ({"replayTrades": 50}, {"replayTrades": 49}, "replay"),
        ({"journalTrades": 1}, {}, "journal"),
        (
            {"journalTrades": 20, "discipline": 95},
            {"journalTrades": 19, "discipline": 100},
            "discipline",
        ),
    ],
)
def test_badge_unlocks_exactly_at_threshold(at, below, badge) -> None:
    assert badge in _unlocked(**at)
    assert badge not in _unlocked(**below)


def test_discipline_needs_rules_not_only_volume() -> None:
    assert "discipline" not in _unlocked(journalTrades=200, discipline=94.9)


def test_longest_streak_survives_a_broken_current_streak() -> None:
    days = ["2026-01-29", "2026-01-30", "2026-01-31", "2026-02-01", "2026-02-10"]
    assert _call("__fxLongestStreak", days) == 4  # через границу месяца


def test_longest_streak_ignores_duplicates_garbage_and_order() -> None:
    days = ["2026-03-30", "x", "2026-03-28", "2026-03-29", "2026-03-29", None]
    assert _call("__fxLongestStreak", days) == 3  # через переход на летнее время
    assert _call("__fxLongestStreak", []) == 0
