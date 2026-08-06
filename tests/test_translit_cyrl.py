"""Паритет порта транслитерации (hooks/translit_cyrl.py) с translit.js.

Если эти тесты падают — Python-порт разошёлся с клиентским переключателем,
и статические /uz-cyrl/ страницы будут отличаться от того, что видит юзер по
тумблеру. Таблица повторяет правила translit.js:toCyrillic.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

_HOOK = Path(__file__).resolve().parent.parent / "hooks" / "translit_cyrl.py"
_spec = importlib.util.spec_from_file_location("translit_cyrl", _HOOK)
assert _spec and _spec.loader
translit_cyrl = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(translit_cyrl)

to_cyrillic = translit_cyrl.to_cyrillic
transliterate_html = translit_cyrl.transliterate_html


@pytest.mark.parametrize(
    ("latin", "cyrillic"),
    [
        ("o'zbek", "ўзбек"),  # o' → ў
        ("g'isht", "ғишт"),  # g' → ғ
        ("ta'rif", "таъриф"),  # tutuq belgisi ' → ъ
        ("shahar", "шаҳар"),  # sh → ш, h → ҳ
        ("chiroyli", "чиройли"),  # ch → ч
        ("yo'l", "йўл"),  # y + o' (pre-pass), не «yo»→ё
        ("Toshkent", "Тошкент"),  # регистр + sh
        ("savdo", "савдо"),
        ("e", "э"),  # e в начале слова → э
        ("men", "мен"),  # e внутри слова → е
        ("MT5", "МТ5"),  # аббревиатура + цифра
        ("ESMA", "ЭСМА"),  # все заглавные
        ("xato", "хато"),  # x → х (не sw с h)
        ("hisob", "ҳисоб"),  # h → ҳ
    ],
)
def test_to_cyrillic_parity(latin: str, cyrillic: str) -> None:
    assert to_cyrillic(latin) == cyrillic


def test_html_transliterates_only_visible_text() -> None:
    html = (
        "<p>Salom dunyo</p>"
        "<code>const narx = 1</code>"
        '<a href="/uz/withdrawal-guide/">havola</a>'
        '<span class="fx-no-translit">brand</span>'
    )
    out = transliterate_html(html)
    assert "Салом дунё" in out  # видимый текст кириллизован
    assert "<code>const narx = 1</code>" in out  # код не тронут
    assert 'href="/uz/withdrawal-guide/"' in out  # атрибут/ссылка не тронуты
    assert ">brand<" in out  # .fx-no-translit пропущен
    assert "ҳавола" in out  # текст ссылки кириллизован


def test_html_preserves_script_and_attrs() -> None:
    html = '<script>var pair="EURUSD";</script><input id="pp-pair" value="x">'
    assert transliterate_html(html) == html  # ничего видимого — байт-в-байт
