"""MkDocs-хук: структурированные данные schema.org (JSON-LD) для SEO.

Зачем: дать поисковикам машиночитаемый контекст страниц — это даёт rich-
результаты в выдаче (раскрытые вопросы у FAQ, имя/организация сайта). Особенно
ценно для узбекских запросов, где выдача занята партнёрками брокеров.

Что генерируем:
- ``Organization`` — на каждой странице (издатель).
- ``WebSite``     — на главной каждой локали.
- ``FAQPage``     — на страницах FAQ (вопросы парсятся из готового HTML).

JSON-LD внедряется в ``<head>`` финальной страницы. Хук подключается в
``mkdocs.yml`` (секция ``hooks``) и не требует доп. зависимостей.
"""
from __future__ import annotations

import json
import re

ORG_NAME = "Forex Trading Toolkit"
GITHUB = "https://github.com/MukhammadAmir-Akbarov/forex-toolkit"

_HEADING_RE = re.compile(r"<h([23])[^>]*>(.*?)</h\1>", re.S)
_HEADERLINK_RE = re.compile(r'<a class="headerlink".*?</a>', re.S)
_TAG_RE = re.compile(r"<[^>]+>")
_WS_RE = re.compile(r"\s+")


def _text(html: str) -> str:
    """HTML-фрагмент → чистый текст (без тегов, ссылок-якорей и лишних пробелов)."""
    html = _HEADERLINK_RE.sub("", html)
    return _WS_RE.sub(" ", _TAG_RE.sub("", html)).strip()


def _lang(page) -> str:
    """Локаль страницы по префиксу URL (i18n строит en/ и uz/ поддиректориями)."""
    url = page.url or ""
    if url == "en/" or url.startswith("en/"):
        return "en"
    if url == "uz/" or url.startswith("uz/"):
        return "uz"
    return "ru"


def _is_home(page) -> bool:
    if getattr(page, "is_homepage", False):
        return True
    return (page.url or "").rstrip("/") in ("", "en", "uz")


def _faq_items(content: str) -> list[tuple[str, str]]:
    """Из HTML FAQ: пары (вопрос, ответ). h3 — вопрос, текст до след. h2/h3 — ответ."""
    items: list[tuple[str, str]] = []
    matches = list(_HEADING_RE.finditer(content))
    for i, m in enumerate(matches):
        if m.group(1) != "3":  # h2 — это разделы («Общие», «Технические»)
            continue
        question = re.sub(r"^\d+\.\s*", "", _text(m.group(2)))
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(content)
        answer = _text(content[start:end])
        if question and answer:
            items.append((question, answer))
    return items


def _organization(config: dict) -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": ORG_NAME,
        "url": config.get("site_url") or GITHUB,
        "sameAs": [GITHUB],
    }


def _website(config: dict, page) -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": config.get("site_name", ORG_NAME),
        "url": config.get("site_url") or GITHUB,
        "inLanguage": _lang(page),
    }


def _faqpage(items: list[tuple[str, str]], page) -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "inLanguage": _lang(page),
        "mainEntity": [
            {
                "@type": "Question",
                "name": q,
                "acceptedAnswer": {"@type": "Answer", "text": a},
            }
            for q, a in items
        ],
    }


def on_post_page(output: str, *, page, config) -> str:
    """Внедряет JSON-LD в <head> готовой страницы."""
    blocks: list[dict] = [_organization(config)]
    if _is_home(page):
        blocks.insert(0, _website(config, page))

    if "extras/faq" in (page.file.src_uri or ""):
        items = _faq_items(page.content or "")
        if items:
            blocks.append(_faqpage(items, page))

    scripts = "\n".join(
        '<script type="application/ld+json">'
        + json.dumps(b, ensure_ascii=False, separators=(",", ":"))
        + "</script>"
        for b in blocks
    )
    return output.replace("</head>", scripts + "\n</head>", 1)
