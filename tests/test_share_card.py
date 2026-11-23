"""Карточка «поделиться результатом»: заголовок, плитки и отсутствие денег.

Текст карточки (``window.__fxShareSummary`` в dashboard.js) выполняется в
Node-песочнице. Рисование на canvas и Web Share проверяются в браузере.
"""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
WIDGETS = ROOT / "_mkdocs" / "javascripts" / "widgets"
SANDBOX = ROOT / "tests" / "widget_sandbox.mjs"
DASHBOARD = WIDGETS / "dashboard.js"

pytestmark = pytest.mark.skipif(shutil.which("node") is None, reason="нет node")

STATS = {
    "progressPct": 34.6,
    "quizPassed": 5,
    "quizTotal": 21,
    "examPassed": False,
    "examBest": 0,
    "maxStreak": 3,
}
BADGES = [
    {"id": "firstPage", "icon": "📖", "ok": True},
    {"id": "exam", "icon": "🏅", "ok": False},
    {"id": "week", "icon": "🔥", "ok": True},
]


def _summary(locale: str = "ru", **overrides) -> dict:
    done = subprocess.run(
        ["node", str(SANDBOX), str(DASHBOARD), "__fxShareSummary", "-", locale],
        input=json.dumps([{**STATS, **overrides}, BADGES]),
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert done.returncode == 0, done.stderr
    payload = json.loads(done.stdout)
    assert "error" not in payload, payload["error"]
    return payload["result"]


def test_passed_exam_is_the_headline() -> None:
    s = _summary(examPassed=True, examBest=90, maxStreak=12)
    assert s["headline"] == "Экзамен Forex Toolkit сдан на 90% 🔥"


def test_streak_headline_uses_russian_plural() -> None:
    assert _summary(maxStreak=12)["headline"].startswith("🔥 12 дней учёбы подряд")
    assert _summary(maxStreak=21)["headline"].startswith("🔥 21 день учёбы подряд")


def test_rows_icons_and_text() -> None:
    s = _summary()
    assert s["headline"] == "📚 Учу форекс с Forex Toolkit"
    assert [r[1] for r in s["rows"]] == ["35%", "5/21", "—", "3", "2/3"]
    assert s["icons"] == "📖 🔥"
    assert s["text"].startswith(s["headline"] + "\n")


@pytest.mark.parametrize("locale", ["ru", "en", "uz"])
def test_every_locale_has_text_and_no_money(locale: str) -> None:
    for overrides in ({}, {"maxStreak": 7}, {"examPassed": True, "examBest": 85}):
        s = _summary(locale, **overrides)
        assert "undefined" not in s["text"] and "$" not in s["text"], s["text"]
        assert all(r[0] for r in s["rows"])


def test_exam_share_button_is_translated() -> None:
    src = (WIDGETS / "exam.js").read_text(encoding="utf-8")
    assert src.count("shareText: function") == 3
    assert "window.FXW && window.FXW.shareCanvas" in src  # без _i18n.js — без кнопки
