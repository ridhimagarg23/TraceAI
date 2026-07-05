"""
url_checker.py

Basic URL analysis utilities.
"""

from urllib.parse import urlparse


class URLChecker:
    """
    Performs lightweight URL inspection.
    """

    SHORTENERS = {
        "bit.ly",
        "tinyurl.com",
        "t.co",
        "goo.gl",
        "rb.gy",
        "ow.ly",
        "is.gd",
        "cutt.ly"
    }

    @classmethod
    def analyze(cls, url: str) -> dict:

        parsed = urlparse(url)

        domain = parsed.netloc.lower()

        return {
            "url": url,
            "domain": domain,
            "https": parsed.scheme == "https",
            "shortened": domain in cls.SHORTENERS,
            "subdomain_count": max(len(domain.split(".")) - 2, 0),
        }