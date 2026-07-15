from playwright.sync_api import sync_playwright
import time
with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://www.google.com/maps/place/Genesis+Builders+Group+Inc./@51.1404427,-114.0647328,473m/data=!3m2!1e3!4b1!4m6!3m5!1s0x53716519bb213dbd:0xb05230052ea15a7!8m2!3d51.1404427!4d-114.0647328!16s%2Fg%2F1td2gl7r?entry=ttu&g_ep=EgoyMDI2MDcwOC4wIKXMDSoASAFQAw%3D%3D")
    time.sleep(15)
    reviews_locator = page.locator('div[class="F7nice "] span[aria-label="reviews"]')
    reviews = (
        reviews_locator.first.inner_text()
        if reviews_locator.count() > 0
        else None
    )
    browser.close
print(reviews)
input()