"""
memory_manager.py

Stores and retrieves scam investigation history.
"""

import json
from pathlib import Path


class MemoryManager:

    def __init__(self):

        self.memory_file = Path(
            "database/threat_memory.json"
        )

        if not self.memory_file.exists():

            self.memory_file.write_text(
                "[]",
                encoding="utf-8"
            )

    def save(
        self,
        investigation: dict
    ):

        memory = self.load()

        memory.append(
            investigation
        )

        self.memory_file.write_text(

            json.dumps(
                memory,
                indent=4
            ),

            encoding="utf-8"

        )

    def load(self):

        return json.loads(

            self.memory_file.read_text(
                encoding="utf-8"
            )

        )

    def search(
        self,
        threat_type: str
    ):

        memory = self.load()

        return [

            item

            for item in memory

            if item.get(
                "threat_type"
            ) == threat_type

        ]

    def clear(self):

        self.memory_file.write_text(

            "[]",

            encoding="utf-8"

        )