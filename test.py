from db.ops import get_all_businesses, delete_business
businesses = get_all_businesses()
for business in businesses:
    if business.status == "enriched":
        delete_business(business)