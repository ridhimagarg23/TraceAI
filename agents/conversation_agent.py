"""
conversation_agent.py

Adaptive Investigation Conversation Agent.
Generates natural replies based on the current
investigation state.
"""

from llm.llm_client import LLMClient

from tools.prompt_loader import PromptLoader
from tools.adaptive_investigation_engine import (
    InvestigationState,
)

from utils.schemas import (
    InvestigationResult,
    ConversationResult,
)


class ConversationAgent:

    def __init__(self):

        self.llm = LLMClient()

        self.prompt = PromptLoader.load(
            "conversation_prompt.txt"
        )

    def run(
        self,
        investigation: InvestigationResult,
        investigation_state: InvestigationState,
        latest_message: str,
        conversation_history: str = "",
    ) -> ConversationResult:

        final_prompt = f"""
{self.prompt}

==================================================
INVESTIGATION RESULT
==================================================

Threat Type:
{investigation.threat_type}

Risk Score:
{investigation.risk_score}

Risk Level:
{investigation.risk_level}

Summary:
{investigation.summary}

Detected URLs:
{investigation.urls}

Detected Phone Numbers:
{investigation.phone_numbers}

Detected Emails:
{investigation.emails}

Detected UPI IDs:
{investigation.upi_ids}

Detected Indicators:
{investigation.detected_indicators}

Recommendations:
{investigation.recommendations}

==================================================
INVESTIGATION PROFILE
==================================================

Communication Style:
{investigation_state.profile.communication_style}

Language:
{investigation_state.profile.language}

Digital Literacy:
{investigation_state.profile.digital_literacy}

==================================================
CURRENT OBJECTIVE
==================================================

{investigation_state.current_objective}

==================================================
CURRENT STRATEGY
==================================================

{investigation_state.current_strategy}

==================================================
CONVERSATION HISTORY
==================================================

{conversation_history}

==================================================
LATEST SCAMMER MESSAGE
==================================================

{latest_message}

==================================================
IMPORTANT
==================================================

Return ONLY valid JSON.

"""

        result = self.llm.generate(
            final_prompt,
            json_output=True
        )

        required_keys = [
            "reply",
            "objective",
            "expected_outcome",
        ]

        for key in required_keys:

            if key not in result:

                raise ValueError(
                    f"Missing '{key}' in LLM response."
                )

        return ConversationResult(
            **result
        )