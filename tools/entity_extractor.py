"""
entity_extractor.py

Extracts Indicators of Compromise (IOCs)
using regex.
"""

import re


class EntityExtractor:

    # -----------------------------
    # Patterns
    # -----------------------------

    PHONE_PATTERN = r"(?:\+91[-\s]?)?[6-9]\d{9}"

    EMAIL_PATTERN = (
        r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[A-Za-z]{2,}"
    )

    URL_PATTERN = (
        r"(?:https?://|www\.)"
        r"[A-Za-z0-9.-]+\.[A-Za-z]{2,}"
        r"(?:/[A-Za-z0-9\-._~:/?#\[\]@!$&'()*+,;=%]*)?"
    )

    DOMAIN_PATTERN = (
        r"\b[A-Za-z0-9.-]+\.(?:com|in|org|net|co\.in)\b"
    )

    UPI_PATTERN = (
        r"\b[a-zA-Z0-9._-]{2,}@[a-zA-Z]{2,}\b"
    )

    OTP_PATTERN = (
        r"\bOTP\b|\bone[- ]?time password\b"
    )

    AMOUNT_PATTERN = (
        r"(?:₹|Rs\.?|INR)\s?\d+(?:,\d+)*(?:\.\d+)?"
    )

    BANK_PATTERN = (
        r"\b("
        r"SBI|HDFC|ICICI|Axis|PNB|BOB|"
        r"Kotak|Canara|Union Bank|"
        r"Paytm|PhonePe|Google Pay"
        r")\b"
    )

    # -----------------------------
    # Extract
    # -----------------------------

    @classmethod
    def extract(cls, text: str) -> dict:

        # -----------------------------
        # URLs
        # -----------------------------

        urls = []

        for url in re.findall(
            cls.URL_PATTERN,
            text,
            re.IGNORECASE
        ):

            # Remove words accidentally attached
            url = re.split(
                r"(Reference|Regards|Call|Email|Phone|OTP)",
                url,
                flags=re.IGNORECASE
            )[0]

            url = url.rstrip(
                ".,!?:;)]>\"'"
            )

            urls.append(url)

        # -----------------------------
        # Standalone Domains
        # -----------------------------

        for domain in re.findall(
            cls.DOMAIN_PATTERN,
            text,
            re.IGNORECASE
        ):

            if not any(
                domain in url
                for url in urls
            ):
                urls.append(domain)

        # -----------------------------
        # Remove emails before UPI search
        # -----------------------------

        clean_text = re.sub(
            cls.EMAIL_PATTERN,
            "",
            text,
            flags=re.IGNORECASE
        )

        # -----------------------------
        # Normalize
        # -----------------------------

        phones = sorted(
            set(
                re.findall(
                    cls.PHONE_PATTERN,
                    text,
                    re.IGNORECASE
                )
            )
        )

        emails = sorted(
            set(
                re.findall(
                    cls.EMAIL_PATTERN,
                    text,
                    re.IGNORECASE
                )
            )
        )

        upis = sorted(
            set(
                re.findall(
                    cls.UPI_PATTERN,
                    clean_text,
                    re.IGNORECASE
                )
            )
        )

        otp_keywords = sorted(
            set(
                re.findall(
                    cls.OTP_PATTERN,
                    text,
                    re.IGNORECASE
                )
            )
        )

        amounts = sorted(
            set(
                re.findall(
                    cls.AMOUNT_PATTERN,
                    text,
                    re.IGNORECASE
                )
            )
        )

        banks = sorted(
            set(
                re.findall(
                    cls.BANK_PATTERN,
                    text,
                    re.IGNORECASE
                )
            )
        )

        urls = sorted(set(urls))

        # -----------------------------
        # Return
        # -----------------------------

        return {

            "phone_numbers": phones,

            "emails": emails,

            "urls": urls,

            "upi_ids": upis,

            "otp_keywords": otp_keywords,

            "amounts": amounts,

            "bank_names": banks,
        }