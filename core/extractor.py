from db.models import Business

def extract_business_data(page, maps_url):
    name = page.locator('h1.DUwDvf.lfPIob').first.inner_text()

    website_locator = page.locator('a.CsEnBe[jslog*="3443"]')
    website = (
        website_locator.first.get_attribute("href")
        if website_locator.count() > 0
        else None
    )

    phone_locator = page.locator(
        'button[data-item-id*="phone"] div.Io6YTe'
    )

    phone = (
        phone_locator.first.inner_text()
        if phone_locator.count() > 0
        else None
    )

    rate_locator = page.locator('div[class="F7nice "] span[aria-hidden="true"]')
    rate = (
        rate_locator.first.inner_text()
        if rate_locator.count() > 0
        else None
    )

    return Business(
        name = name,
        website = website,
        phone = phone,
        maps_url = maps_url,
        rate = float(rate.replace(",", "."))  if rate else None
    )

