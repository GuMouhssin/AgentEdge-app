from bs4 import BeautifulSoup
from urllib.parse import urljoin
from bs4 import MarkupResemblesLocatorWarning
import warnings

warnings.filterwarnings(
    "ignore",
    category=MarkupResemblesLocatorWarning
)

PRIORITY_KEYWORDS = [
    "contact",
    "contact-us",
    "get-in-touch",
    "team",
    "our-team",
    "meet-the-team",
    "about",
    "about-us",
    "staff",
]


def find_priority_pages(base_url, html):
    """
    Return a list of high-priority pages.

    - Homepage is always first.
    - Only real web pages are returned.
    - Duplicates are removed.
    """

    pages = [base_url]

    if not html:
        return pages

    soup = BeautifulSoup(html, "html.parser")

    seen = {base_url.rstrip("/")}

    for keyword in PRIORITY_KEYWORDS:

        for a in soup.find_all("a", href=True):

            href = a["href"].strip()
            text = a.get_text(strip=True)

            href_lower = href.lower()
            text_lower = text.lower()

            if (
                keyword not in href_lower
                and keyword not in text_lower
            ):
                continue

            # Skip non-web links
            if href_lower.startswith((
                "mailto:",
                "tel:",
                "javascript:",
                "#",
            )):
                continue

            # Skip downloads
            if href_lower.endswith((
                ".pdf",
                ".jpg",
                ".jpeg",
                ".png",
                ".gif",
                ".svg",
                ".webp",
            )):
                continue

            url = urljoin(base_url, href)

            # Only HTTP(S) pages
            if not url.startswith(("http://", "https://")):
                continue

            normalized = url.rstrip("/")

            if normalized not in seen:
                pages.append(url)
                seen.add(normalized)

    return pages[:3]