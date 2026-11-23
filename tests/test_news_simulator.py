"""Симулятор новостей: сценарии на трёх языках, вердикты и подсчёт очков.

Исторические примеры сверены с источниками (список — внизу страницы), поэтому
переводы обязаны сохранять те же числа и тот же лучший ход в каждом сценарии.
Подсчёт (``window.__fxNewsScore`` в news-sim.js) выполняется в Node-песочнице.
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
WIDGET = DOCS / "javascripts" / "widgets" / "news-sim.js"
SANDBOX = ROOT / "tests" / "widget_sandbox.mjs"
LOCALES = ("", ".en", ".uz")
PAGES = [DOCS / "tools" / f"news-simulator{s}.md" for s in LOCALES]
PROTOCOL = [DOCS / "practice" / f"news-trading-protocol{s}.md" for s in LOCALES]
FIELDS = ("event", "situation", "reaction", "history")


def _scenarios(page: Path) -> list[dict]:
    text = page.read_text(encoding="utf-8")
    block = re.search(r'id="ns-scenarios">(.*?)</script>', text, re.S)
    assert block, f"{page.name}: нет JSON-блока #ns-scenarios"
    return json.loads(block.group(1))


@pytest.mark.parametrize("page", PAGES, ids=lambda p: p.name)
def test_page_wires_the_widget(page: Path) -> None:
    text = page.read_text(encoding="utf-8")
    assert text.startswith("---\nwidgets: [news-sim]\n---")
    assert '<div id="ns-widget"></div>' in text
    assert "news-trading-protocol.md" in text


@pytest.mark.parametrize("page", PAGES, ids=lambda p: p.name)
def test_every_scenario_has_one_best_move(page: Path) -> None:
    for sc in _scenarios(page):
        verdicts = [o["verdict"] for o in sc["options"]]
        assert set(verdicts) <= {"best", "ok", "bad"}
        assert verdicts.count("best") == 1 and "bad" in verdicts, sc["event"]
        assert all(sc[f].strip() for f in FIELDS)
        assert all(o["text"].strip() and o["why"].strip() for o in sc["options"])
        assert re.search(r"\b(19|20)\d\d\b", sc["history"]), "пример без года"


def _numbers(text: str) -> list[str]:
    return sorted(re.findall(r"\d+", text))


@pytest.mark.parametrize("page", PAGES[1:], ids=lambda p: p.name)
def test_translations_keep_verdicts_and_historical_numbers(page: Path) -> None:
    ru, tr = _scenarios(PAGES[0]), _scenarios(page)
    assert len(tr) == len(ru)
    for a, b in zip(ru, tr):
        verdicts = [o["verdict"] for o in a["options"]]
        assert verdicts == [o["verdict"] for o in b["options"]]
        assert _numbers(a["history"]) == _numbers(b["history"]), b["event"]


@pytest.mark.parametrize("page", PROTOCOL, ids=lambda p: p.name)
def test_protocol_links_to_the_simulator(page: Path) -> None:
    assert "../tools/news-simulator.md" in page.read_text(encoding="utf-8")


def _score(answers: list[str]) -> dict:
    done = subprocess.run(
        ["node", str(SANDBOX), str(WIDGET), "__fxNewsScore", "-", "ru"],
        input=json.dumps([answers]),
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert done.returncode == 0, done.stderr
    payload = json.loads(done.stdout)
    assert "error" not in payload, payload["error"]
    return payload["result"]


@pytest.mark.skipif(shutil.which("node") is None, reason="нет node")
@pytest.mark.parametrize(
    ("answers", "pct", "tier"),
    [
        (["best"] * 6, 100, "ready"),
        (["best"] * 4 + ["ok", "bad"], 75, "almost"),
        (["ok"] * 6, 50, "almost"),
        (["ok", "bad", "bad", "bad", "best", "bad"], 25, "early"),
        ([], 0, "early"),
    ],
)
def test_score_and_tier(answers: list[str], pct: int, tier: str) -> None:
    s = _score(answers)
    assert (s["pct"], s["tier"], s["max"]) == (pct, tier, len(answers) * 2)
