"""Чекер внешних ссылок: разбор markdown и классификация ответов.

В сеть тесты не ходят: их дело — доказать, что мы правильно достаём ссылки из
исходников и правильно отличаем «страницы нет» от «до неё не дошли отсюда».
Второе важнее первого: если таймаут до soliq.uz считать поломкой, еженедельный
отчёт будет красным всегда и его перестанут читать.
"""

from __future__ import annotations

import check_external_links as cel


def _write(tmp_path, name: str, text: str):
    path = tmp_path / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def test_collects_markdown_and_bare_links(tmp_path) -> None:
    _write(
        tmp_path,
        "page.md",
        "[FCA](https://register.fca.org.uk/) и <https://asic.gov.au>",
    )
    links = cel.collect_links(tmp_path)
    assert set(links) == {"https://register.fca.org.uk/", "https://asic.gov.au"}
    assert links["https://asic.gov.au"] == ["page.md"]


def test_same_link_from_three_locales_is_probed_once(tmp_path) -> None:
    """Одна ссылка на RU/EN/UZ — один запрос, но видно все три страницы."""
    for name in ("uz/law-faq.md", "uz/law-faq.en.md", "uz/law-faq.uz.md"):
        _write(tmp_path, name, "[soliq](https://soliq.uz)")
    links = cel.collect_links(tmp_path)
    assert list(links) == ["https://soliq.uz"]
    assert len(links["https://soliq.uz"]) == 3


def test_ignores_relative_and_placeholder_links(tmp_path) -> None:
    _write(
        tmp_path,
        "page.md",
        "[внутренняя](../extras/faq.md) [пример](https://example.com/x) "
        "[локальный](http://localhost:8000/) [почта](mailto:a@b.uz)",
    )
    assert cel.collect_links(tmp_path) == {}


def test_only_filters_by_section(tmp_path) -> None:
    _write(tmp_path, "uz/law-faq.md", "[a](https://soliq.uz)")
    _write(tmp_path, "extras/faq.md", "[b](https://asic.gov.au)")
    assert list(cel.collect_links(tmp_path, only="uz/")) == ["https://soliq.uz"]


def test_trailing_punctuation_is_not_part_of_the_url(tmp_path) -> None:
    _write(tmp_path, "page.md", "Смотри <https://www.bis.org/statistics/cbpol.htm>.")
    assert list(cel.collect_links(tmp_path)) == [
        "https://www.bis.org/statistics/cbpol.htm"
    ]


def test_missing_domain_is_dead_but_timeout_is_not() -> None:
    """Главное различие инструмента: DNS отвечает всем, сеть — нет."""
    assert cel.classify(None, "gaierror: nodename nor servname provided") == "dead"
    assert cel.classify(None, "TimeoutError: timed out") == "unreachable"
    assert cel.classify(404, "Not Found") == "dead"
    assert cel.classify(200, "ok") == "ok"
    assert cel.classify(403, "Forbidden") == "blocked"


def test_error_description_unwraps_the_real_reason() -> None:
    """`URLError` одинаков для мёртвого домена и просроченного сертификата."""
    import socket
    import urllib.error

    dns = urllib.error.URLError(socket.gaierror(8, "nodename nor servname provided"))
    assert "gaierror" in cel._describe(dns)
    timeout = urllib.error.URLError(TimeoutError("timed out"))
    assert cel._describe(timeout).startswith("TimeoutError")
