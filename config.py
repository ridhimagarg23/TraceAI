"""
config.py

Loads configuration from .env
"""

import os

from dotenv import load_dotenv

# Load .env file
load_dotenv()


class Settings:
    """
    Central configuration for the project.
    """

    def __init__(self):

        # OpenRouter
        self.OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

        # Default model
        self.LLM_MODEL = os.getenv(
            "LLM_MODEL",
            "qwen/qwen3-32b"
        )

        # Validation
        if not self.OPENROUTER_API_KEY:
            raise ValueError(
                "OPENROUTER_API_KEY not found in .env"
            )


settings = Settings()