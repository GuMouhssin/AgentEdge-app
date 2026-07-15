from bs4 import BeautifulSoup
from urllib.parse import urljoin
from .website import fetch_homepage
from bs4 import MarkupResemblesLocatorWarning
import warnings
warnings.filterwarnings("ignore", category=MarkupResemblesLocatorWarning)

# Ordered from MOST likely to LEAST likely
CONTACT_KEYWORDS = [
    "contact",
    "contact-us",
    "contactus",
    "get-in-touch",
    "reach-us",
    "locations",
    "about",
]


def find_contact_page(base_url, html):
    """
    Find the most likely contact page.

    Args:
        base_url (str): Website URL.
        html (str): Homepage HTML.

    Returns:
        str | None
    """
    if not html:
        return None
    soup = BeautifulSoup(html, "html.parser")
    # Collect every link once
    links = []
    for a in soup.find_all("a", href=True):
        href = a["href"]
        text = a.get_text(strip=True)
        links.append({
            "href": href,
            "href_lower": href.lower(),
            "text_lower": text.lower()
        })
    # Search by keyword priority
    for keyword in CONTACT_KEYWORDS:
        for link in links:
            if (
                keyword in link["href_lower"]
                or keyword in link["text_lower"]
            ):
                return urljoin(base_url, link["href"])
    return None

# html = fetch_homepage("https://eddyherring.com/")
# print(find_contact_page("https://eddyherring.com/", html))