from __future__ import annotations

import pytest


@pytest.mark.parametrize("prefix", ["", "en/", "uz/"])
def test_replay_2_loads_market_catalog(site_url, pw_page, prefix):
    page = pw_page
    page.goto(f"{site_url}/{prefix}tools/replay-trainer/")
    page.wait_for_selector("#rp-pair")

    assert page.locator("#rp-pair option").count() == 4
    assert page.locator("#rp-tf option").count() == 2
    assert page.locator("#replay-canvas").is_visible()


def test_replay_places_levels_on_canvas_and_runs(site_url, pw_page):
    page = pw_page
    page.goto(f"{site_url}/tools/replay-trainer/")
    page.wait_for_selector("#rp-pair")

    page.select_option("#rp-pair", "USDJPY")
    page.select_option("#rp-tf", "D1")
    assert "USDJPY D1" in page.locator("#rp-meta").inner_text()

    page.click("#rp-buy")
    canvas = page.locator("#replay-canvas")
    box = canvas.bounding_box()
    assert box is not None
    x = box["width"] * 0.55
    canvas.click(position={"x": x, "y": box["height"] * 0.50})
    canvas.click(position={"x": x, "y": box["height"] * 0.72})
    canvas.click(position={"x": x, "y": box["height"] * 0.25})

    assert page.locator("#rp-value-entry").inner_text() != "--"
    assert page.locator("#rp-value-sl").inner_text() != "--"
    assert page.locator("#rp-value-tp").inner_text() != "--"
    assert page.locator("#rp-start").is_enabled()

    page.click("#rp-start")
    page.wait_for_selector("#rp-result", state="visible", timeout=6_000)


def test_replay_session_saves_v2_stats(site_url, pw_page):
    page = pw_page
    page.goto(f"{site_url}/tools/replay-trainer/")
    page.wait_for_selector("#rp-skip")

    for _ in range(6):
        page.click("#rp-skip")
        page.click("#rp-next")

    page.wait_for_selector(".rp-stats")
    stored = page.evaluate(
        "() => JSON.parse(localStorage.getItem('forex_replay_stats'))"
    )

    assert stored["version"] == 2
    assert stored["trades"] == 0
    assert stored["skips"] == 6
    assert stored["errors"] == []
