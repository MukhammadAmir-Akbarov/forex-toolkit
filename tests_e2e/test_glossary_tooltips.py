"""e2e глоссарий-тултипов: термины подсвечиваются в главах, подсказка на месте."""

from __future__ import annotations


def test_glossary_terms_marked_up_with_definitions(pw_page, site_url):
    page = pw_page
    page.goto(f"{site_url}/docs/technical-analysis/")
    first = page.locator("article .fx-term").first
    first.wait_for(state="attached")
    assert first.get_attribute("data-definition").strip()
    assert first.get_attribute("aria-label").strip()
    # Лимит подсветок на страницу — не более 15.
    assert page.locator("article .fx-term").count() <= 15


def test_glossary_terms_follow_page_locale(pw_page, site_url):
    page = pw_page
    page.goto(f"{site_url}/en/docs/technical-analysis/")
    first = page.locator("article .fx-term").first
    first.wait_for(state="attached")
    definition = first.get_attribute("data-definition")
    # Определение должно быть английским, а не русским.
    assert not any("а" <= ch <= "я" for ch in definition.lower()), definition
