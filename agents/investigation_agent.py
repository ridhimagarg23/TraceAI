"""
investigation_agent.py

Main AI Investigation Agent.
"""

from llm.llm_client import LLMClient

from tools.prompt_loader import PromptLoader
from tools.entity_extractor import EntityExtractor
from tools.url_checker import URLChecker
from tools.risk_engine import RiskEngine

from utils.schemas import InvestigationResult


class InvestigationAgent:

    def __init__(self):

        self.llm = LLMClient()

        self.prompt = PromptLoader.load(
            "investigation_prompt.txt"
        )

    def run(
        self,
        message: str
    ) -> InvestigationResult:

        print("\n[1/5] Extracting entities...")

        entities = EntityExtractor.extract(
            message
        )

        print("[2/5] Analyzing URLs...")

        url_analysis = [

            URLChecker.analyze(url)

            for url in entities["urls"]

        ]

        print("[3/5] Investigating with AI...")

        final_prompt = f"""
{self.prompt}

=========================
SUSPICIOUS MESSAGE
=========================

{message}

=========================
EXTRACTED ENTITIES
=========================

Phone Numbers:
{entities["phone_numbers"]}

Emails:
{entities["emails"]}

URLs:
{entities["urls"]}

UPI IDs:
{entities["upi_ids"]}

Banks:
{entities["bank_names"]}

OTP Keywords:
{entities["otp_keywords"]}

Amounts:
{entities["amounts"]}

=========================
Return ONLY valid JSON.
=========================
"""

        result = self.llm.generate(
            final_prompt,
            json_output=True
        )

        # ----------------------------
        # Validate LLM Response
        # ----------------------------

        required_keys = [

            "is_scam",

            "confidence",

            "threat_type",

            "summary"

        ]

        for key in required_keys:

            if key not in result:

                raise ValueError(
                    f"Missing '{key}' in LLM response."
                )

        confidence = result["confidence"]

        if result["is_scam"] and confidence < 30:

            raise ValueError(
                "Invalid AI output. Scam detected with very low confidence."
            )

        if (not result["is_scam"]) and confidence > 90:

            raise ValueError(
                "Invalid AI output. Not scam with unusually high confidence."
            )

        print("[4/5] Calculating Risk...")

        risk = RiskEngine.calculate(

            result,

            entities,

            url_analysis

        )

        result.update({

            "phone_numbers":
                entities["phone_numbers"],

            "emails":
                entities["emails"],

            "urls":
                entities["urls"],

            "upi_ids":
                entities["upi_ids"],

            "otp_keywords":
                entities["otp_keywords"],

            "amounts":
                entities["amounts"],

            "bank_names":
                entities["bank_names"],

            "risk_score":
                risk["risk_score"],

            "risk_level":
                risk["risk_level"],

            "recommendations":
                risk["reasons"],

            "detected_indicators":
                risk["reasons"]

        })

        print("[5/5] Investigation Complete.\n")

        return InvestigationResult(
            **result
        )