"""Статические инварианты и сверка формулы виджета восстановления просадки.

Зачем: связь «страница объявляет виджет → виджет подключается → формула в JS
совпадает с эталоном» ломается тихо: сборка ``--strict`` проходит, а страница
просто перестаёт считать. Здесь три слоя защиты:

* все три локали страницы объявляют ``widgets: [drawdown]`` и содержат якорь;
* ``drawdown.js`` выставляет чистую функцию ``window.__fxDrawdownRecovery``;
* её математика совпадает с эталоном ``d / (100 - d) * 100`` на трёх точках.

Формула выполняется в песочнице Node (``tests/widget_sandbox.mjs``) — как в
``test_widget_logic.py``: арифметика здесь, отрисовка — в ``tests_e2e/``.
Если Node не установлен, сверка пропускается.
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
WIDGET = DOCS / "javascripts" / "widgets" / "drawdown.js"
SANDBOX = ROOT / "tests" / "widget_sandbox.mjs"
PAGES = [
    DOCS / "tools" / "drawdown-recovery.md",
    DOCS / "tools" / "drawdown-recovery.en.md",
    DOCS / "tools" / "drawdown-recovery.uz.md",
]

# Якорь, по которому виджет решает, что он на своей странице.
ANCHOR = "dd-result"

# Три точки эталонной формулы gain = d / (100 − d) × 100:
# симметричная середина (50 → 100), «почти симметричная» мелкая (10 → 11.1…)
# и типичная рабочая просадка (20 → 25).
FORMULA_CASES = [(50.0, 100.0), (10.0, 100.0 / 9.0), (20.0, 25.0)]


def test_all_locale_pages_exist() -> None:
    missing = [p.name for p in PAGES if not p.exists()]
    assert not missing, f"нет страниц: {missing}"


@pytest.mark.parametrize("page", PAGES, ids=lambda p: p.name)
def test_page_declares_widget_and_has_anchor(page: Path) -> None:
    text = page.read_text(encoding="utf-8")
    assert text.startswith("---\n"), f"{page.name}: нет front matter"
    head = text[4 : text.index("\n---\n", 4)]
    assert re.search(r"widgets:\s*\[[^\]]*\bdrawdown\b[^\]]*\]", head), (
        f"{page.name}: виджет drawdown не объявлен во front matter"
    )
    assert f'id="{ANCHOR}"' in text, f"{page.name}: нет якоря {ANCHOR}"
    assert 'id="dd-input"' in text, f"{page.name}: нет поля ввода dd-input"


def test_widget_exposes_pure_function_and_anchor() -> None:
    source = WIDGET.read_text(encoding="utf-8")
    assert "window.__fxDrawdownRecovery" in source, (
        "виджет не выставляет чистую функцию — сверять нечего"
    )
    first_anchor = re.search(r'getElementById\(["\']([\w-]+)["\']\)', source)
    assert first_anchor and first_anchor.group(1) == ANCHOR, (
        "первый getElementById должен быть якорем dd-result — "
        "по нему tests/test_widget_loading.py связывает виджет со страницей"
    )


def _call_js(d: float, locale: str = "ru") -> float:
    completed = subprocess.run(
        ["node", str(SANDBOX), str(WIDGET), "__fxDrawdownRecovery", "-", locale],
        input=json.dumps([d]),
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert completed.returncode == 0, completed.stderr
    payload = json.loads(completed.stdout)
    assert "error" not in payload, payload["error"]
    return payload["result"]


NO_NODE = shutil.which("node") is None


@pytest.mark.skipif(NO_NODE, reason="нет node — сверка пропускается")
@pytest.mark.parametrize(
    ("drawdown", "expected"),
    FORMULA_CASES,
    ids=[f"d={c[0]:.0f}" for c in FORMULA_CASES],
)
@pytest.mark.parametrize("locale", ["ru", "en", "uz"])
def test_formula_matches_reference(drawdown, expected, locale) -> None:
    """JS-формула обязана совпасть с эталоном на всех трёх локалях."""
    got = _call_js(drawdown, locale=locale)
    assert got == pytest.approx(expected, rel=1e-12), (
        f"[{locale}] d={drawdown}: JS={got} эталон={expected}"
    )
