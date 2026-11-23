"""Мастер «С чего начать?»: главные страницы, ссылки маршрута и логика.

Логика выполняется в Node-песочнице (``tests/widget_sandbox.mjs``).
"""

from __future__ import annotations

import json
import re
import shutil
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "_mkdocs"
WIDGET = DOCS / "javascripts" / "widgets" / "onboarding.js"
SANDBOX = ROOT / "tests" / "widget_sandbox.mjs"
HOMES = [DOCS / f"index{s}.md" for s in ("", ".en", ".uz")]


@pytest.mark.parametrize("page", HOMES, ids=lambda p: p.name)
def test_home_declares_widget(page: Path) -> None:
    text = page.read_text(encoding="utf-8")
    assert text.startswith("---\nwidgets: [onboarding]\n---")
    assert 'id="fx-onboarding"' in text


def test_route_urls_point_to_existing_pages() -> None:
    """Битая ссылка маршрута не ловится --strict: она собирается в JS."""
    src = WIDGET.read_text(encoding="utf-8")
    block = re.search(r"var URLS = \{(.*?)\};", src, re.S)
    assert block
    for url in re.findall(r"\"([^\"]+)\"", block.group(1)):
        path = url.split("#")[0].rstrip("/")
        candidates = [DOCS / f"{path}.md", DOCS / path / "README.md"]
        assert any(c.exists() for c in candidates), f"нет страницы для {url}"


def _route(answers: dict) -> dict:
    done = subprocess.run(
        ["node", str(SANDBOX), str(WIDGET), "__fxOnboardingRoute", "-", "ru"],
        input=json.dumps([answers]),
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert done.returncode == 0, done.stderr
    payload = json.loads(done.stdout)
    assert "error" not in payload, payload["error"]
    return payload["result"]


NO_NODE = shutil.which("node") is None


@pytest.mark.skipif(NO_NODE, reason="нет node")
def test_novice_starts_with_basics() -> None:
    r = _route({"exp": "none", "money": "none", "goal": "understand"})
    assert r["days"][0] == ["first15", "guide"]
    assert "exam" in r["days"][2]
    assert r["warn"] is None


@pytest.mark.skipif(NO_NODE, reason="нет node")
def test_experienced_skips_known_via_diagnostic() -> None:
    r = _route({"exp": "demo", "money": "big", "goal": "live"})
    assert r["days"][0] == ["diag"]
    assert {"readiness", "broker"} <= set(r["days"][2])
    assert r["days"][2].count("readiness") == 1


@pytest.mark.skipif(NO_NODE, reason="нет node")
def test_borrowed_money_puts_readiness_test_first() -> None:
    r = _route({"exp": "charts", "money": "borrowed", "goal": "demo"})
    assert r["days"][0][0] == "riskProfile"
    assert r["warn"] == "borrowed"
    assert "riskProfile" not in r["days"][1]


@pytest.mark.skipif(NO_NODE, reason="нет node")
def test_novice_wanting_live_is_warned() -> None:
    r = _route({"exp": "none", "money": "small", "goal": "live"})
    assert r["warn"] == "early"
