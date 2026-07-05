"""
conversation_session.py

Maintains the investigation conversation session.
"""


class ConversationSession:

    def __init__(self):

        self.history = []

    def add_scammer_message(self, message: str):

        self.history.append({
            "role": "scammer",
            "message": message
        })

    def add_traceai_reply(self, reply: str):

        self.history.append({
            "role": "traceai",
            "message": reply
        })

    def get_history(self):

        if not self.history:
            return "No previous conversation."

        history = ""

        for item in self.history:

            history += (
                f"{item['role'].upper()}: "
                f"{item['message']}\n"
            )

        return history

    def clear(self):

        self.history.clear()