"""
Day 7: Robust JSON Output Extractor and Validator
Sanitizes raw LLM outputs, extracts JSON payloads, and validates schemas using Pydantic.
"""

import json
import re
from typing import Type, TypeVar, Optional, Any, Dict
from pydantic import BaseModel, ValidationError

T = TypeVar("T", bound=BaseModel)


class JSONExtractor:
    """
    Extracts, cleans, and validates structured JSON payloads from raw LLM responses.
    Handles markdown wrappers, preamble text, trailing commas, and formatting noise.
    """

    @staticmethod
    def clean_text(raw_response: str) -> str:
        """Strips markdown code blocks, backticks, and extraneous whitespace."""
        text = raw_response.strip()
        # Remove ```json ... ``` or ``` ... ```
        pattern = r"```(?:json)?\s*([\s\S]*?)\s*```"
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            text = match.group(1).strip()
        return text

    @classmethod
    def extract_json(cls, raw_response: str) -> Dict[str, Any]:
        """
        Locates the outermost balanced curly braces or square brackets and parses JSON.
        """
        cleaned = cls.clean_text(raw_response)

        # Attempt direct parse first
        try:
            return json.loads(cleaned)
        except json.JSONDecodeError:
            pass

        # Find first { and last }
        start = cleaned.find("{")
        end = cleaned.rfind("}")
        if start != -1 and end != -1 and end > start:
            candidate = cleaned[start:end + 1]
            try:
                return json.loads(candidate)
            except json.JSONDecodeError:
                # Attempt light sanitization: remove trailing commas before closing braces
                repaired = re.sub(r",\s*([\}\]])", r"\1", candidate)
                return json.loads(repaired)

        # Find first [ and last ]
        start = cleaned.find("[")
        end = cleaned.rfind("]")
        if start != -1 and end != -1 and end > start:
            candidate = cleaned[start:end + 1]
            repaired = re.sub(r",\s*([\}\]])", r"\1", candidate)
            return json.loads(repaired)

        raise ValueError(f"Could not locate or parse valid JSON payload in response:\n{raw_response}")

    @classmethod
    def parse_as_model(cls, raw_response: str, model_class: Type[T]) -> T:
        """Parses raw text and validates against a specified Pydantic model."""
        payload = cls.extract_json(raw_response)
        return model_class.model_validate(payload)


# Example Pydantic Models for demonstration
class SentimentAnalysisOutput(BaseModel):
    sentiment: str
    confidence: float
    key_themes: list[str]
    action_required: bool
    summary: str


def demonstrate():
    # Simulated messy LLM response with conversational filler & markdown
    messy_llm_output = """
    Certainly! Here is the JSON analysis you requested:
    ```json
    {
        "sentiment": "NEGATIVE",
        "confidence": 0.94,
        "key_themes": ["slow response time", "billing glitch"],
        "action_required": true,
        "summary": "Customer expressed strong dissatisfaction regarding overcharge.",
    }
    ```
    I hope this helps!
    """

    print("=" * 60)
    print("DAY 7: JSON EXTRACTOR & SCHEMA VALIDATION")
    print("=" * 60)
    parsed: SentimentAnalysisOutput = JSONExtractor.parse_as_model(messy_llm_output, SentimentAnalysisOutput)
    print("Successfully parsed into Pydantic model:")
    print(f"- Sentiment:       {parsed.sentiment}")
    print(f"- Confidence:      {parsed.confidence}")
    print(f"- Key Themes:      {parsed.key_themes}")
    print(f"- Action Required: {parsed.action_required}")
    print(f"- Summary:         {parsed.summary}")


if __name__ == "__main__":
    demonstrate()
