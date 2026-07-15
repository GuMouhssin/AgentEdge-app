from db.models import Business
from db.ops import update_business
from enrichment.contact import find_contact_page
from enrichment.email import extract_emails
from enrichment.socials import extract_social_links
from enrichment.website import fetch_homepage

def score_lead(agency):
    score = 0
    
    # Google Maps signals (strongest)
    if agency["rating"] >= 4.5:
        score += 25
    elif agency["rating"] >= 4.0:
        score += 15
        
    if agency["reviews"] >= 100:
        score += 20
    elif agency["reviews"] >= 50:
        score += 10
    elif agency["reviews"] >= 20:
        score += 5
    
    # Website presence
    if agency["has_website"]:
        score += 15
    
    # Contact info completeness
    if agency["email"]:
        score += 15
    if agency["phone"]:
        score += 10
    
    # Social presence
    if agency["has_linkedin"]:
        score += 10
    if agency["has_facebook"]:
        score += 5
    
    # Business activity
    if agency["hours_available"]:
        score += 10
    
    return score

# Score interpretation:
# 80-100: Hot lead — contact immediately
# 60-79:  Warm lead — worth contacting
# 40-59:  Cold lead — lower priority
# 0-39:   Skip

def enrich_business(business: Business):
    if not business.website:
        business.status = "enriched"
        business.lead_score = 0
        return business
    html = fetch_homepage(business.website)
    if not html:
        business.status = "raw"
        business.lead_score = 0
        return business
    contact_page = find_contact_page(business.website, html)
    lead_score = 0 
    if business.rate:
        if business.rate == 4.5:
            lead_score += 25
        elif business.rate >= 4.0:
            lead_score += 15
    if contact_page:
        html = fetch_homepage(contact_page)
        emails = extract_emails(html)
        socials = extract_social_links(html)
    else:
        emails = extract_emails(business.website)
        socials = extract_social_links(business.website)

    if business.website:
        lead_score += 15

    if emails:
        lead_score += 15

    if socials["linkedin"]:
        lead_score += 15
    if socials["facebook"]:
        lead_score += 10
    if socials["instagram"]:
        lead_score += 15
    if socials["youtube"]:
        lead_score += 15
    return Business(
        name = business.name,
        website = business.website,
        phone = business.phone,
        maps_url = business.maps_url,
        rate = business.rate,
        status = "enriched",
        emails = emails,
        contact_page = contact_page,
        facebook = socials["facebook"],
        instagram = socials["instagram"],
        linkedin = socials["linkedin"],
        youtube = socials["youtube"],
        lead_score = lead_score
    ) 

def process_all_businesses(businesses):
    num = len(businesses)
    for i, business in enumerate(businesses, start = 1):
        print(f'enriching [{i}/{num}]: {business.name}')
        enriched = enrich_business(business)
        update_business(enriched)

