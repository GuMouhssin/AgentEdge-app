


def search_query(page, query):
    page.locator('input[name="q"]').fill(query)
    page.locator('input[name="q"]').press("Enter")
    page.wait_for_selector('a.hfpxzc', timeout = 10000)


def open_business_profile(context, link):
    new_page = context.new_page()
    new_page.goto(link, wait_until="domcontentloaded")
    new_page.wait_for_selector("h1")
    return new_page