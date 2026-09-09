"""
memory_manager.py

Stores and retrieves scam investigation history.
"""

import json
from pathlib import Path


class MemoryManager:

    def __init__(self):

        # Resolve relative to the repository root (tools is one level deep)
        project_root = Path(__file__).resolve().parent.parent
        self.memory_file = project_root / "database" / "threat_memory.json"

        # Create the database directory automatically if it doesn't exist
        self.memory_file.parent.mkdir(parents=True, exist_ok=True)

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