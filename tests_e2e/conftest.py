"""Фикстуры для браузерных (e2e) тестов виджетов-калькуляторов.

Эти тесты лежат ОТДЕЛЬНО от ``tests/`` (там ``testpaths=["tests"]``), поэтому
обычный ``pytest -q`` их не собирает. Запуск:

    pip install -e ".[dev,e2e]" && python -m playwright install chromium
    pytest tests_e2e/

Идея: собрать сайт (``mkdocs build``), отдать ``site/`` локальным http-сервером и
проверить браузером, что JS-математика виджетов совпадает с каноном из
``tools/`` (``margin_required`` / ``project_growth``). Виджеты используют
inline-JS и кнопку пересчёта, поэтому тест не зависит от темы Material.
"""

from __future__ import annotations

import functools
import http.server
import socketserver
import subprocess
import sys
import threading
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
# чтобы импортировать эталонные функции из tools/ по голому имени
sys.path.insert(0, str(ROOT / "tools"))

playwright_api = pytest.importorskip(
    "playwright.sync_api",
    reason="нужен playwright: pip install -e '.[e2e]' && playwright install chromium",
)


@pytest.fixture(scope="session")
def site_url() -> str:
    """Собрать сайт, отдать site/ http-сервером, вернуть базовый URL."""
    subprocess.run(
        [sys.executable, "-m", "mkdocs", "build", "-q"], cwd=ROOT, check=True
    )
    handler = functools.partial(
        http.server.SimpleHTTPRequestHandler, directory=str(SITE)
    )

    class Quiet(socketserver.TCPServer):
        allow_reuse_address = True

    httpd = Quiet(("127.0.0.1", 0), handler)
    port = httpd.server_address[1]
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    try:
        yield f"http://127.0.0.1:{port}"
    finally:
        httpd.shutdown()


@pytest.fixture(scope="session")
def _browser():
    with playwright_api.sync_playwright() as p:
        browser = p.chromium.launch()
        try:
            yield browser
        finally:
            browser.close()


@pytest.fixture
def pw_page(_browser):
    context = _browser.new_context()
    page = context.new_page()
    try:
        yield page
    finally:
        context.close()
