"""
risk_engine.py

Weighted Risk Scoring Engine
"""

from typing import Dict


class RiskEngine:
    """
    Rule-based explainable risk scoring.
    """

    @classmethod
    def calculate(
        cls,
        investigation: Dict,
        entities: Dict,
        url_analysis: list[Dict]
    ) -> Dict:

        score = 0
        reasons = []

        # -------------------------
        # Scam Detection
        # -------------------------

        if investigation["is_scam"]:
            score += 40
            reasons.append("LLM detected a scam.")

        # -------------------------
        # Confidence
        # -------------------------

        confidence = investigation["confidence"]

        score += int(confidence * 0.30)

        # -------------------------
        # URLs
        # -------------------------

        if entities["urls"]:
            score += 10
            reasons.append("Suspicious URL detected.")

        # -------------------------
        # UPI
        # -------------------------

        if entities["upi_ids"]:
            score += 10
            reasons.append("UPI ID detected.")

        # -------------------------
        # Email / Phone
        # -------------------------

        if entities["emails"]:
            score += 5
            reasons.append("Email detected.")

        if entities["phone_numbers"]:
            score += 5
            reasons.append("Phone number detected.")

        # -------------------------
        # URL Analysis
        # -------------------------

        for url in url_analysis:

            if not url["https"]:
                score += 10
                reasons.append("Uses HTTP instead of HTTPS.")

            if url["shortened"]:
                score += 10
                reasons.append("Shortened URL detected.")

            if url["subdomain_count"] >= 2:
                score += 10
                reasons.append("Suspicious subdomain.")

        # -------------------------
        # Multiple IOC Bonus
        # -------------------------

        indicators = (
            len(entities["urls"])
            + len(entities["emails"])
            + len(entities["phone_numbers"])
            + len(entities["upi_ids"])
        )

        if indicators >= 3:
            score += 5
            reasons.append("Multiple indicators detected.")

        score = min(score, 100)

        if score >= 80:
            level = "HIGH"

        elif score >= 50:
            level = "MEDIUM"

        else:
            level = "LOW"

        return {
            "risk_score": score,
            "risk_level": level,
            "reasons": reasons
        }