from .navigator import search_query, open_business_profile
from .scroll import load_more_results
from db.ops import insert_business, get_all_businesses, delete_business
from db.db import init_db
from .extractor import extract_business_data
from playwright.sync_api import sync_playwright
import csv
# from config import HEADLESS

def scrape(query, max_results):
    with sync_playwright() as p:
        print("Launching the browser...")
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        try:
            print("Opening maps...")
            page = context.new_page()
            page.goto("https://www.google.com/maps")
            print(f'Searching for {query}...')
            search_query(page, query)
            print("Loading results...")
            load_more_results(page, max_results)
            print('STARTING TO SCRAPE...')
            results = page.locator('a.hfpxzc')
            links_count = results.count()
            parsed_results = []
            seen_links = set()
            reviews = page.locator('span[class="UY7F9"]')
            j = 0
            for i in range(min(links_count, max_results)):
                print(f"scrape {i+1}/{min(links_count, max_results)}....")
                link = results.nth(i).get_attribute("href")
                review = reviews.nth(i-j).inner_text()
                if not link or link in seen_links:
                    continue
                try:
                    business_page = open_business_profile(context, link)
                    business = extract_business_data(business_page, link, review)
                    if business.reviews == 0:
                        j += 1
                    insert_business(business)
                    parsed_results.append(business)
                    business_page.close()
                except Exception as e:
                    print(f"Error scraping {link}: {e}")
                seen_links.add(link)
            return len(parsed_results)
        finally:
            context.close()
            browser.close()


