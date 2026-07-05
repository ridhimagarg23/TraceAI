"""
adaptive_investigation_engine.py

Adaptive Investigation Engine

Maintains a stable investigation profile and
plans conversation objectives throughout
the investigation session.
"""

from dataclasses import dataclass, field


@dataclass
class InvestigationProfile:
    communication_style: str
    language: str
    digital_literacy: str


@dataclass
class InvestigationState:
    profile: InvestigationProfile
    current_objective: str
    current_strategy: str
    completed_objectives: list[str] = field(default_factory=list)
    turn_number: int = 1


class AdaptiveInvestigationEngine:

    def __init__(self):

        self.state = None

    # ------------------------------------

    def initialize(
        self,
        threat_type: str
    ) -> InvestigationState:

        profile = self._select_profile(threat_type)

        objective = self._first_objective(threat_type)

        strategy = self._choose_strategy(objective)

        self.state = InvestigationState(
            profile=profile,
            current_objective=objective,
            current_strategy=strategy
        )

        return self.state

    # ------------------------------------

    def update(
        self,
        objective_completed: bool
    ) -> InvestigationState:

        if objective_completed:

            self.state.completed_objectives.append(
                self.state.current_objective
            )

            self.state.current_objective = self._next_objective()

        self.state.current_strategy = self._choose_strategy(
            self.state.current_objective
        )

        self.state.turn_number += 1

        return self.state

    # ------------------------------------

    def get_state(self):

        return self.state

    # ====================================
    # PRIVATE METHODS
    # ====================================

    def _select_profile(
        self,
        threat_type: str
    ):

        threat = threat_type.lower()

        if "bank" in threat:

            return InvestigationProfile(
                communication_style="Polite",
                language="Hinglish",
                digital_literacy="Medium"
            )

        if "job" in threat:

            return InvestigationProfile(
                communication_style="Curious",
                language="English",
                digital_literacy="Medium"
            )

        if "investment" in threat:

            return InvestigationProfile(
                communication_style="Formal",
                language="English",
                digital_literacy="High"
            )

        return InvestigationProfile(
            communication_style="Neutral",
            language="English",
            digital_literacy="Low"
        )

    # ------------------------------------

    def _first_objective(
        self,
        threat_type: str
    ):

        threat = threat_type.lower()

        if "bank" in threat:
            return "Collect official verification website"

        if "job" in threat:
            return "Collect recruiter information"

        if "investment" in threat:
            return "Collect company information"

        return "Collect more information"

    # ------------------------------------

    def _next_objective(self):

        objectives = [

            "Collect official verification website",

            "Collect employee ID",

            "Collect payment method",

            "Keep conversation on chat",

            "Waste scammer time",

            "End investigation"

        ]

        for objective in objectives:

            if objective not in self.state.completed_objectives:

                return objective

        return "End investigation"

    # ------------------------------------

    def _choose_strategy(
        self,
        objective: str
    ):

        mapping = {

            "Collect official verification website":
                "Curious",

            "Collect employee ID":
                "Confused",

            "Collect payment method":
                "Cooperative",

            "Keep conversation on chat":
                "Busy",

            "Waste scammer time":
                "Skeptical",

            "End investigation":
                "Cautious"

        }

        return mapping.get(
            objective,
            "Curious"
        )