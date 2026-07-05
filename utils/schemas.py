"""
schemas.py

Pydantic schemas used throughout TraceAI.
"""

from pydantic import BaseModel, Field


class InvestigationResult(BaseModel):
    """
    Output of Investigation Agent.
    """

    is_scam: bool

    confidence: int = Field(
        ge=0,
        le=100
    )

    threat_type: str

    summary: str

    # ---------- Extracted IOCs ----------

    phone_numbers: list[str] = []

    emails: list[str] = []

    urls: list[str] = []

    upi_ids: list[str] = []

    otp_keywords: list[str] = []

    amounts: list[str] = []

    bank_names: list[str] = []

    # ---------- Risk ----------

    risk_score: int = Field(
        ge=0,
        le=100
    )

    risk_level: str

    # ---------- Investigation ----------

    detected_indicators: list[str] = []

    recommendations: list[str] = []


class ConversationResult(BaseModel):

    reply: str

    objective: str

    expected_outcome: str


class ReportResult(BaseModel):

    title: str

    markdown: str