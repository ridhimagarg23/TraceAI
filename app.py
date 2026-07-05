"""
app.py

TraceAI CLI Application
"""

from agents.investigation_agent import InvestigationAgent
from agents.conversation_agent import ConversationAgent
from agents.report_agent import ReportAgent

from tools.memory_manager import MemoryManager
from tools.adaptive_investigation_engine import (
    AdaptiveInvestigationEngine,
)
from tools.conversation_session import (
    ConversationSession,
)


def main():

    print("=" * 60)
    print(" TraceAI - AI Scam Investigation Platform ")
    print("=" * 60)

    message = input(
        "\nPaste suspicious message:\n\n"
    )

    # ---------------------------------
    # Investigation
    # ---------------------------------

    investigation = InvestigationAgent().run(
        message
    )

    # ---------------------------------
    # Adaptive Investigation Engine
    # ---------------------------------

    engine = AdaptiveInvestigationEngine()

    state = engine.initialize(
        investigation.threat_type
    )

    # ---------------------------------
    # Conversation Session
    # ---------------------------------

    session = ConversationSession()

    session.add_scammer_message(
        message
    )

    # ---------------------------------
    # Save Investigation
    # ---------------------------------

    memory = MemoryManager()

    memory.save(
        investigation.model_dump()
    )

    # ---------------------------------
    # Conversation
    # ---------------------------------

    conversation = ConversationAgent().run(
        investigation=investigation,
        investigation_state=state,
        latest_message=message,
        conversation_history=session.get_history()
    )

    session.add_traceai_reply(
        conversation.reply
    )

    # ---------------------------------
    # Report
    # ---------------------------------

    report = ReportAgent().run(
        investigation=investigation,
        conversation=conversation
    )

    # ---------------------------------
    # Output
    # ---------------------------------

    print("\n" + "=" * 60)
    print(" INVESTIGATION RESULT ")
    print("=" * 60)

    print(f"\nThreat Type : {investigation.threat_type}")
    print(f"Confidence  : {investigation.confidence}%")
    print(f"Risk Score  : {investigation.risk_score}")
    print(f"Risk Level  : {investigation.risk_level}")

    print("\nSummary:")
    print(investigation.summary)

    print("\n" + "=" * 60)
    print(" INVESTIGATION PROFILE ")
    print("=" * 60)

    print(f"Language             : {state.profile.language}")
    print(f"Communication Style  : {state.profile.communication_style}")
    print(f"Digital Literacy     : {state.profile.digital_literacy}")

    print("\nCurrent Objective:")
    print(state.current_objective)

    print("\nCurrent Strategy:")
    print(state.current_strategy)

    print("\nSuggested Safe Reply:")
    print(conversation.reply)

    print("\nExpected Outcome:")
    print(conversation.expected_outcome)

    print("\n" + "=" * 60)
    print(report.title)
    print("=" * 60)

    print(report.markdown)


if __name__ == "__main__":
    main()