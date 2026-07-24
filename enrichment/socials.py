from bs4 import BeautifulSoup
from bs4 import MarkupResemblesLocatorWarning
from urllib.parse import urlparse
import warnings
warnings.filterwarnings("ignore", category=MarkupResemblesLocatorWarning)

# These are generic/platform social pages that belong to website 
# builders, not the business itself
BLACKLIST = {
    "facebook.com/sharer",
    "facebook.com/wixstudio",
    "facebook.com/fasthostsinternet",
    "facebook.com/wix",
    "instagram.com/wix",
    "instagram.com/fasthosts",
    "linkedin.com/company/editorx",
    "linkedin.com/company/wix",
    "youtube.com/user/wix",
    "youtube.com/@wixstudio",
    "facebook.com/wordpress",
    "facebook.com/squarespace",
    "instagram.com/squarespace",
    "linkedin.com/company/squarespace",
    "facebook.com/shopify",
    "instagram.com/shopify",
    "linkedin.com/company/shopify",
    "facebook.com/bruntwooduk",      # parent company
    "instagram.com/bruntwood",
    "linkedin.com/company/bruntwood",
    "youtube.com/@ukbruntwood",
    "facebook.com/bruntwoodscitech",
    "instagram.com/bruntwoodscitech",
    "linkedin.com/company/bruntwood-scitech",
    "youtube.com/@bruntwoodscitech",
    "facebook.com/kellerwilliamsunitedkingdom",
    "instagram.com/keller_williams_uk",
    "linkedin.com/organization-guest/company/keller-williams-uk",
    "youtube.com/channel/uclqtoxxoywc9bhhtzi4biqa",
    "facebook.com/sequenceuk",
    "instagram.com/sequenceuk",
    "linkedin.com/company/sequence-uk-ltd",
    "facebook.com/martincouk",
    "instagram.com/martinco_uk",
    "linkedin.com/company/martin-and-co",
    "facebook.com/leaderslimited",
    "instagram.com/leadersltd",
    "linkedin.com/company/leaders-ltd",
    "facebook.com/northwooduk",
    "linkedin.com/company/northwooduk-com",
    "youtube.com/user/northwoodlettings",
    "facebook.com/huntersestateagent",
    "instagram.com/huntershomes",
    "linkedin.com/company/hunters-estate-agents",
    "facebook.com/reedsrains",
    "instagram.com/reedsrainsestateagents",
    "facebook.com/entwistlegreenproperty",
    "facebook.com/c21uk",
    "instagram.com/century21_uk",
    "linkedin.com/company/century21-united-kingdom",
    "youtube.com/channel/uc4htx6f5nfkbtttju4alaOfw",
}

SOCIAL_DOMAINS = {
    "facebook": "facebook.com",
    "instagram": "instagram.com",
    "linkedin": "linkedin.com",
    "youtube": "youtube.com",
}

def is_blacklisted(href):
    href_lower = href.lower()
    return any(b in href_lower for b in BLACKLIST)

def is_generic_share(href):
    """Detect share buttons and generic social links"""
    generic_patterns = [
        "sharer", "share?", "intent/tweet",
        "share/", "/share", "sharing",
        "?u=http", "?url=http",
    ]
    href_lower = href.lower()
    return any(p in href_lower for p in generic_patterns)

def looks_like_business_page(href, domain):
    """
    Check if this looks like a real business page
    vs a generic/personal profile or share link.
    """
    parsed = urlparse(href)
    path = parsed.path.strip("/").lower()
    
    if domain == "facebook.com":
        # Skip generic facebook paths
        skip = ["profile.php", "sharer", "share", "login", "home"]
        if any(s in path for s in skip):
            return False
        # Valid: facebook.com/AgencyName or facebook.com/pages/...
        return bool(path)
    
    if domain == "instagram.com":
        # Valid: instagram.com/username
        # Skip: instagram.com with no path
        return bool(path) and "/" not in path.strip("/")
    
    if domain == "linkedin.com":
        # Valid: linkedin.com/company/name or linkedin.com/in/name
        return "company/" in path or "/in/" in path
    
    if domain == "youtube.com":
        # Valid: youtube.com/@channel or /channel/ or /user/
        return any(p in path for p in ["@", "channel/", "user/"])
    
    return True

def extract_social_links(html):
    """
    Extract social media links from HTML.
    Filters out share buttons, blacklisted pages,
    and website builder social links.

    Returns:
        {
            "facebook": str | None,
            "instagram": str | None,
            "linkedin": str | None,
            "youtube": str | None,
        }
    """
    socials = {
        "facebook": None,
        "instagram": None,
        "linkedin": None,
        "youtube": None,
    }

    if not html:
        return socials

    soup = BeautifulSoup(html, "html.parser")

    for a in soup.find_all("a", href=True):
        href = a["href"].strip()

        # Skip empty, relative, or javascript links
        if not href or href.startswith("#") or href.startswith("javascript"):
            continue

        # Skip share buttons and generic links
        if is_generic_share(href):
            continue

        # Skip blacklisted pages
        if is_blacklisted(href):
            continue

        href_lower = href.lower()

        for platform, domain in SOCIAL_DOMAINS.items():
            if socials[platform] is None and domain in href_lower:
                if looks_like_business_page(href, domain):
                    socials[platform] = href
                break

    return socials