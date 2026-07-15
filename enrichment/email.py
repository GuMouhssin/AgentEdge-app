import re
from bs4 import BeautifulSoup

EMAIL_REGEX = re.compile(
    r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
    re.IGNORECASE
)

BAD_EXTENSIONS = (
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".svg",
    ".webp",
    ".css",
    ".js",
    ".ico",
)


def extract_emails(html):
    """
    Extract clean email addresses from HTML.
    Prioritizes visible text and mailto links.
    """

    if not html:
        return []

    soup = BeautifulSoup(html, "html.parser")

    found = set()

    # ---------- mailto links ----------
    for tag in soup.select('a[href^="mailto:"]'):
        href = tag.get("href", "")
        email = href.replace("mailto:", "").split("?")[0].strip().lower()

        if EMAIL_REGEX.fullmatch(email):
            found.add(email)

    # ---------- visible text ----------
    text = soup.get_text(" ", strip=True)

    for email in EMAIL_REGEX.findall(text):

        email = email.lower().strip(".,;:()[]<>\"'")

        if any(email.endswith(ext) for ext in BAD_EXTENSIONS):
            continue

        if len(email) > 254:
            continue

        found.add(email)

    return sorted(found)