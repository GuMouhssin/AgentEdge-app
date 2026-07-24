from db.models import Business
from db.ops import update_business
from enrichment.contact import find_priority_pages
from enrichment.email import extract_emails
from enrichment.socials import extract_social_links
from enrichment.website import fetch_homepage


def enrich_business(business: Business):

    if not business.website:
        business.status = "enriched"
        business.lead_score = 0
        return business

    homepage_html = fetch_homepage(business.website)

    if not homepage_html:
        business.status = "raw"
        business.lead_score = 0
        return business

    pages = find_priority_pages(
        business.website,
        homepage_html
    )

    emails = set()

    socials = {
        "facebook": None,
        "instagram": None,
        "linkedin": None,
        "youtube": None,
    }

    contact_page = None

    for i, page in enumerate(pages):

        html = homepage_html if i == 0 else fetch_homepage(page)

        if not html:
            continue

        emails.update(extract_emails(html))

        page_socials = extract_social_links(html)

        for key in socials:

            if socials[key] is None and page_socials[key]:
                socials[key] = page_socials[key]

        if i > 0 and contact_page is None:
            contact_page = page

    emails = sorted(emails)

    lead_score = 0

    # Reviews
    if business.reviews >= 500:
        lead_score += 20
    elif business.reviews >= 100:
        lead_score += 15
    elif business.reviews >= 50:
        lead_score += 10
    elif business.reviews >= 20:
        lead_score += 5

    # Rating
    if business.rate:
        if business.rate >= 4.5:
            lead_score += 20
        elif business.rate >= 4.0:
            lead_score += 15
        elif business.rate >= 3.5:
            lead_score += 10
        elif business.rate >= 3.0:
            lead_score += 5

    if business.website:
        lead_score += 5


    if emails:
        lead_score += 15

    if socials["linkedin"]:
        lead_score += 15

    if socials["facebook"]:
        lead_score += 10

    if socials["instagram"]:
        lead_score += 10

    if socials["youtube"]:
        lead_score += 5

    return Business(
        name=business.name,
        website=business.website,
        phone=business.phone,
        maps_url=business.maps_url,
        rate=business.rate,
        reviews=business.reviews,
        status="enriched",
        emails=emails,
        contact_page=contact_page,
        facebook=socials["facebook"],
        instagram=socials["instagram"],
        linkedin=socials["linkedin"],
        youtube=socials["youtube"],
        lead_score=lead_score,
    )


def process_all_businesses(businesses):

    total = len(businesses)

    for i, business in enumerate(businesses, start=1):

        print(f"Enriching [{i}/{total}] : {business.name}")

        enriched = enrich_business(business)

        update_business(enriched)