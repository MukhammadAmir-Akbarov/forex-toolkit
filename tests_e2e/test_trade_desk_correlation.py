"""Корреляционные предупреждения в Trade Desk.

Если по сильно связанной паре уже есть открытая сделка, виджет обязан
подсветить, что риск удваивается (то же направление) или что сделки частично
гасят друг друга (противоположное направление). Матрица корреляций подгружается
из market-analytics.json, поэтому тесты ждут сетевой ответ, а не полагаются на
тайминги.
"""


def _seed_plans(page, plans):
    page.evaluate(
        """
        (plans) => {
          localStorage.setItem('forex_trade_drafts_v1', JSON.stringify(plans));
        }
        """,
        plans,
    )


def _goto_desk(page, site_url):
    page.goto(f"{site_url}/tools/trade-desk/")


def test_correlation_double_risk_warning(pw_page, site_url):
    """Открытый long GBPUSD + новый long EURUSD (корреляция 0.80) = удвоение риска."""
    page = pw_page
    _goto_desk(page, site_url)
    _seed_plans(
        page,
        [
            {
                "id": "o1",
                "status": "open",
                "pair": "GBPUSD",
                "direction": "long",
                "risk_pct": 1,
                "risk_usd": 100,
            }
        ],
    )
    with page.expect_response("**/data/market-analytics.json"):
        page.reload()
    page.fill("#td-pair", "EURUSD")
    warning = page.wait_for_selector(".td-corr--double", timeout=10000)
    assert warning is not None
    text = page.locator(".td-corr--double").first.inner_text()
    assert "GBPUSD" in text


def test_correlation_hedge_warning_on_opposite_direction(pw_page, site_url):
    """Открытый long GBPUSD + short EURUSD: связанные пары гасят друг друга."""
    page = pw_page
    _goto_desk(page, site_url)
    _seed_plans(
        page,
        [
            {
                "id": "o1",
                "status": "open",
                "pair": "GBPUSD",
                "direction": "long",
                "risk_pct": 1,
                "risk_usd": 100,
            }
        ],
    )
    with page.expect_response("**/data/market-analytics.json"):
        page.reload()
    page.fill("#td-pair", "EURUSD")
    page.select_option("#td-direction", "short")
    warning = page.wait_for_selector(".td-corr--hedge", timeout=10000)
    assert warning is not None
    text = page.locator(".td-corr--hedge").first.inner_text()
    assert "GBPUSD" in text


def test_no_correlation_warning_without_open_trades(pw_page, site_url):
    """Без открытых сделок предупреждений быть не должно даже после загрузки матрицы."""
    page = pw_page
    _goto_desk(page, site_url)
    _seed_plans(page, [])
    with page.expect_response("**/data/market-analytics.json"):
        page.reload()
    page.fill("#td-pair", "EURUSD")
    page.wait_for_timeout(400)  # даём fetch.then отработать и перерисовать блок
    assert page.locator(".td-corr").count() == 0


def test_correlation_warning_ignores_same_pair(pw_page, site_url):
    """Та же самая пара не считается корреляционным дублем (это видно и по журналу)."""
    page = pw_page
    _goto_desk(page, site_url)
    _seed_plans(
        page,
        [
            {
                "id": "o1",
                "status": "open",
                "pair": "EURUSD",
                "direction": "long",
                "risk_pct": 1,
                "risk_usd": 100,
            }
        ],
    )
    with page.expect_response("**/data/market-analytics.json"):
        page.reload()
    page.fill("#td-pair", "EURUSD")
    page.wait_for_timeout(400)
    assert page.locator(".td-corr").count() == 0
