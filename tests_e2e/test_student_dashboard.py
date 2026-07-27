"""e2e smoke для личного кабинета ученика."""

from __future__ import annotations

import pytest


@pytest.mark.parametrize("prefix", ["", "en/", "uz/"])
def test_student_dashboard_empty_state(pw_page, site_url, prefix):
    page = pw_page
    page.goto(f"{site_url}/{prefix}extras/dashboard/")
    page.wait_for_selector("#student-dashboard .sd-hero")

    assert page.locator(".sd-card").count() == 4
    assert "0%" in page.text_content(".sd-hero")
    assert page.text_content("#sd-next-text").strip()


def test_student_dashboard_reads_existing_local_state(pw_page, site_url):
    page = pw_page
    page.goto(f"{site_url}/extras/dashboard/")
    page.evaluate(
        """
        () => {
          localStorage.setItem('fx-progress-v1', JSON.stringify(
            Array.from({length: 90}, (_, i) => '/demo/page-' + i + '/')
          ));
          localStorage.setItem('forex_exam_passed', '1');
          localStorage.setItem('forex_exam_best', '92');
          localStorage.setItem(
            'forex_replay_stats',
            JSON.stringify({
              version: 2, trades: 5, wins: 3, losses: 2, skips: 0,
              wr: 60, avgR: '0.80', weakCategory: 's'
            })
          );
          localStorage.setItem(
            'forex_journal_summary',
            JSON.stringify({
              trades: 12, discipline: 96.5, pnl: 87.25, totalR: 4.2
            })
          );
        }
        """
    )
    page.reload()
    page.wait_for_selector("#student-dashboard .sd-hero")

    assert "92%" in page.text_content("#student-dashboard")
    assert "12 сделок" in page.text_content("#student-dashboard")
    assert "Live Caution" in page.text_content("#student-dashboard")
    assert "флэт" in page.text_content("#sd-next-text")
