"""MkDocs-хук: подстановка языкового словаря терминов на каждую страницу.

Подсказки терминов (`abbr` + `content.tooltips`) — это чистое совпадение по
тексту и они не знают про язык страницы. Поэтому к каждой странице мы добавляем
определения именно на её языке: определяем локаль по URL (`en/…`, `uz/…`, иначе
`ru`) и дописываем содержимое `includes/abbreviations.<lang>.md`.

Так одни и те же аббревиатуры (RSI, MACD, SL…) получают подсказку на нужном
языке: на русской странице — по-русски, на английской — по-английски и т.д.
"""

from __future__ import annotations

from pathlib import Path

# includes/ лежит рядом с репозиторием (hooks/ и includes/ — соседи).
_INCLUDES = Path(__file__).resolve().parent.parent / "includes"
_SUPPORTED = ("ru", "en", "uz")


def _locale_from_url(url: str) -> str:
    """Локаль страницы из её URL (mkdocs-static-i18n кладёт EN в en/, UZ в uz/)."""
    head = url.split("/", 1)[0]
    return head if head in ("en", "uz") else "ru"


def _definitions(lang: str) -> str:
    path = _INCLUDES / f"abbreviations.{lang}.md"
    try:
        return path.read_text(encoding="utf-8")
    except OSError:
        return ""


def on_page_markdown(markdown: str, *, page, config, files) -> str:  # noqa: ARG001
    lang = _locale_from_url(page.url)
    defs = _definitions(lang)
    if not defs:
        return markdown
    return f"{markdown}\n\n{defs}"
