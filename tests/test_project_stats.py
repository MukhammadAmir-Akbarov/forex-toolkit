from pathlib import Path

from hooks.project_stats import count_tests, project_stats


def test_project_stats_are_derived_from_repository() -> None:
    stats = project_stats()
    assert stats["pages"] >= 80
    assert stats["tools"] >= 20
    assert stats["strategies"] == 6
    assert stats["tests"] == count_tests(Path("tests")) + count_tests(Path("tests_e2e"))
