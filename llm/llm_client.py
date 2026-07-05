"""
llm_client.py

Reusable LLM Client

Supports:
- OpenRouter
- JSON Output
- Automatic Retries
- JSON Cleanup
- Provider Agnostic Design
"""

from __future__ import annotations

import json
import time
from typing import Any

from openai import OpenAI

from config import settings


class LLMClient:
    """
    Reusable client for all AI agents.

    Every agent in this project uses ONLY this class.
    """

    def __init__(self):

        self.client = OpenAI(
            api_key=settings.OPENROUTER_API_KEY,
            base_url="https://openrouter.ai/api/v1",
        )

        self.model = settings.LLM_MODEL

    def generate(
        self,
        prompt: str,
        *,
        temperature: float = 0.2,
        json_output: bool = False,
        retries: int = 3,
    ) -> str | dict[str, Any]:

        last_error = None

        for attempt in range(retries):

            try:

                response = self.client.chat.completions.create(
                    model=self.model,
                    temperature=temperature,
                    messages=[
                        {
                            "role": "user",
                            "content": prompt,
                        }
                    ],
                )

                text = response.choices[0].message.content

                if text is None:
                    raise ValueError("Model returned empty response.")

                text = self._clean_response(text)

                if not json_output:
                    return text

                return json.loads(text)

            except json.JSONDecodeError as e:

                raise ValueError(
                    f"LLM returned invalid JSON.\n\n{text}"
                ) from e

            except Exception as e:

                last_error = e

                if attempt == retries - 1:
                    break

                wait = 2 ** attempt

                print(
                    f"\nRetry {attempt + 1}/{retries} "
                    f"after {wait}s..."
                )

                time.sleep(wait)

        raise RuntimeError(
            f"LLM request failed.\n\n{last_error}"
        )

    @staticmethod
    def _clean_response(text: str) -> str:
        """
        Removes markdown wrappers if the model returns:

        ```json
        {...}
        ```
        """

        text = text.strip()

        if text.startswith("```json"):
            text = text[7:]

        if text.startswith("```"):
            text = text[3:]

        if text.endswith("```"):
            text = text[:-3]

        return text.strip()