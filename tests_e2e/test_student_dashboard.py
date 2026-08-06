"""e2e smoke для личного кабинета ученика."""

from __future__ import annotations

import json

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


@pytest.mark.parametrize("backup_version", [1, 2, 3])
def test_dashboard_full_backup_requires_preview_confirmation(
    pw_page, site_url, backup_version
):
    page = pw_page
    page.goto(f"{site_url}/extras/dashboard/")
    page.evaluate(
        """
        () => {
          localStorage.setItem('fx-progress-v1', JSON.stringify(['/old/']));
          localStorage.setItem('forex_journal_data_v2', JSON.stringify({text: 'old'}));
          localStorage.setItem('forex_trade_drafts_v1', JSON.stringify([]));
        }
        """
    )
    payload = {
        "version": backup_version,
        "exported_at": "2026-08-06T00:00:00.000Z",
        "localStorage": {
            "fx-progress-v1": json.dumps(["/one/", "/two/"]),
            "forex_journal_data_v2": json.dumps(
                {"text": "id,date\n1,2026-08-06", "name": "journal.csv"}
            ),
            "forex_trade_drafts_v1": json.dumps(
                [{"id": "plan-1", "status": "plan", "pair": "EURUSD"}]
            ),
            "forex_tool_settings_v1": json.dumps({"tradeDesk": {"riskPct": 1}}),
        },
    }
    if backup_version >= 2:
        payload["schema"] = "forex-toolkit-backup"
    page.set_input_files(
        "#sd-import",
        {
            "name": "forex-dashboard-backup.json",
            "mimeType": "application/json",
            "buffer": json.dumps(payload).encode(),
        },
    )

    page.locator("#sd-restore").wait_for(state="visible")
    assert "2" in page.locator("#sd-restore").inner_text()
    assert page.evaluate("JSON.parse(localStorage.getItem('fx-progress-v1'))") == [
        "/old/"
    ]

    page.click("#sd-confirm-restore")
    assert page.evaluate("JSON.parse(localStorage.getItem('fx-progress-v1'))") == [
        "/one/",
        "/two/",
    ]
    assert (
        page.evaluate("JSON.parse(localStorage.getItem('forex_trade_drafts_v1'))[0].id")
        == "plan-1"
    )


def test_dashboard_export_contains_full_local_data(pw_page, site_url):
    page = pw_page
    page.goto(f"{site_url}/extras/dashboard/")
    page.evaluate(
        """
        () => {
          localStorage.setItem('forex_journal_data_v2',
            JSON.stringify({text: 'full journal'}));
          localStorage.setItem('forex_trade_drafts_v1', JSON.stringify([{id: 'p1'}]));
          localStorage.setItem('forex_tool_settings_v1', JSON.stringify({risk: 1}));
        }
        """
    )
    with page.expect_download() as download_info:
        page.click("#sd-export")
    payload = json.loads(download_info.value.path().read_text())
    assert payload["version"] == 3
    assert payload["schema"] == "forex-toolkit-backup"
    assert payload["localStorage"]["forex_journal_data_v2"]
    assert payload["localStorage"]["forex_trade_drafts_v1"]
    assert payload["localStorage"]["forex_tool_settings_v1"]
    assert payload["localStorage"]["forex_data_meta_v1"]
    assert json.loads(payload["localStorage"]["forex_data_meta_v1"])["lastBackupAt"]
