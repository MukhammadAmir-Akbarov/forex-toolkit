import re
from pathlib import Path

from hooks.project_stats import count_tests, project_stats

README = Path(__file__).resolve().parent.parent / "README.md"


def test_project_stats_are_derived_from_repository() -> None:
    stats = project_stats()
    assert stats["pages"] >= 80
    assert stats["tools"] >= 20
    assert stats["strategies"] == 6
    assert stats["tests"] == count_tests(Path("tests")) + count_tests(Path("tests_e2e"))


def test_readme_numbers_match_the_repository() -> None:
    """README обещал «156 unit-тестов» при 502 и «25+ инструментов» при 32.

    Сайт считает эти числа хуком во время сборки, README — нет, поэтому он
    молча устаревал. Числа тестов из README убраны совсем (менялись каждым
    PR), а страницы и инструменты сверяются с тем же счётчиком, что и сайт.
    """
    stats = project_stats()
    text = README.read_text(encoding="utf-8")

    pages = re.search(r"\*\*(\d+) страниц", text)
    tools = re.search(r"(\d+) Python-инструмент", text)
    assert pages and tools, "в README пропала строка с составом проекта"

    assert int(pages.group(1)) == stats["pages"]
    assert int(tools.group(1)) == stats["tools"]


def test_readme_does_not_hardcode_test_counts() -> None:
    """Точное число тестов меняется каждым PR — в README ему не место."""
    text = README.read_text(encoding="utf-8")
    stale = re.findall(r"\d+\s+unit-тест\w*", text)
    assert stale == [], f"убери число тестов из README: {stale}"
