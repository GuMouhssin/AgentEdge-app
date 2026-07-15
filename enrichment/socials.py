from bs4 import BeautifulSoup
from bs4 import MarkupResemblesLocatorWarning
import warnings
warnings.filterwarnings("ignore", category=MarkupResemblesLocatorWarning)

def extract_social_links(html):
    """
    Extract social media links from HTML.

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
        href = a["href"]
        if socials["facebook"] is None and "facebook.com" in href:
            socials["facebook"] = href
        elif socials["instagram"] is None and "instagram.com" in href:
            socials["instagram"] = href
        elif socials["linkedin"] is None and "linkedin.com" in href:
            socials["linkedin"] = href
        elif socials["youtube"] is None and "youtube.com" in href:
            socials["youtube"] = href
    return socials

# html = fetch_homepage("https://eddyherring.com/contact.html")
# print(extract_social_links(html))