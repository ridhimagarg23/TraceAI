"""
prompt_loader.py

Utility for loading prompt files.
"""

from pathlib import Path


class PromptLoader:
    """
    Loads prompt templates from the prompts folder.
    """

    PROMPTS_DIR = Path("prompts")

    @classmethod
    def load(cls, filename: str) -> str:
        """
        Load a prompt file.

        Args:
            filename: Prompt filename.

        Returns:
            Prompt text.
        """

        path = cls.PROMPTS_DIR / filename

        if not path.exists():
            raise FileNotFoundError(
                f"Prompt not found: {filename}"
            )

        return path.read_text(
            encoding="utf-8"
        ).strip()