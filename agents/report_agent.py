"""
report_agent.py

Generates a professional investigation report.
"""

from llm.llm_client import LLMClient

from tools.prompt_loader import PromptLoader

from utils.schemas import (
    InvestigationResult,
    ConversationResult,
    ReportResult,
)


class ReportAgent:

    def __init__(self):

        self.llm = LLMClient()

        self.prompt = PromptLoader.load(
            "report_prompt.txt"
        )

    def run(
        self,
        investigation: InvestigationResult,
        conversation: ConversationResult
    ) -> ReportResult:

        final_prompt = f"""
{self.prompt}

=====================================
INVESTIGATION RESULT
=====================================

Threat Type:
{investigation.threat_type}

Risk Score:
{investigation.risk_score}

Risk Level:
{investigation.risk_level}

Summary:
{investigation.summary}

Phone Numbers:
{investigation.phone_numbers}

Emails:
{investigation.emails}

URLs:
{investigation.urls}

UPI IDs:
{investigation.upi_ids}

Detected Indicators:
{investigation.detected_indicators}

Recommendations:
{investigation.recommendations}

=====================================
HONEYPOT RESPONSE
=====================================

Reply:
{conversation.reply}

Objective:
{conversation.objective}

Expected Outcome:
{conversation.expected_outcome}

=====================================
Return ONLY valid JSON.
=====================================
"""

        result = self.llm.generate(
            final_prompt,
            json_output=True
        )

        required_keys = [
            "title",
            "markdown"
        ]

        for key in required_keys:

            if key not in result:

                raise ValueError(
                    f"Missing '{key}' in LLM response."
                )

        return ReportResult(
            **result
        )