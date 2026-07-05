import unittest
from tools.adaptive_investigation_engine import AdaptiveInvestigationEngine, InvestigationState


class TestAdaptiveInvestigationEngine(unittest.TestCase):

    def test_engine_flow(self):
        engine = AdaptiveInvestigationEngine()
        
        # Test initialization
        state = engine.initialize("Banking Phishing")
        self.assertIsInstance(state, InvestigationState)
        self.assertEqual(state.turn_number, 1)
        self.assertIsNotNone(state.current_objective)
        self.assertIsNotNone(state.current_strategy)
        self.assertIsNotNone(state.profile)

        # Test state transition
        updated_state = engine.update(objective_completed=True)
        self.assertEqual(updated_state.turn_number, 2)
        self.assertIsNotNone(updated_state.current_objective)
        self.assertIsNotNone(updated_state.current_strategy)
