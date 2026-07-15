import random
import time
import requests
from playwright.sync_api import sync_playwright
from config import HEADERS, MAX_RETRIES

def fetch_homepage(url):
    """
    Downloads a webpage.

    Strategy:
    1. Try requests (fast)
    2. Fallback to Playwright (handles JS & anti-bot)
    """

    # ---------- Fallback ----------
    try:

        with sync_playwright() as p:

            browser = p.chromium.launch(
                headless = True
            )

            page = browser.new_page()

            page.goto(
                url,
                wait_until="domcontentloaded",
                timeout=30000
            )

            html = page.content()

            browser.close()

            return html

    except Exception as e:

        print(f"[Playwright ERROR] {url}")
        print(e)

        return None