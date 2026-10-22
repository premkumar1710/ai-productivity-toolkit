"""
AI Productivity Toolkit - Configuration Management
Loads API keys, default models, and provider configurations from environment.
"""

import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class ToolkitConfig:
    provider: str  # "mock", "gemini", "openai", "anthropic"
    api_key: Optional[str]
    model_name: str
    temperature: float = 0.7
    max_tokens: int = 2048

    @classmethod
    def load(cls) -> "ToolkitConfig":
        # Check environment variables in priority order
        gemini_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        openai_key = os.getenv("OPENAI_API_KEY")
        anthropic_key = os.getenv("ANTHROPIC_API_KEY")

        if gemini_key:
            return cls(
                provider="gemini",
                api_key=gemini_key,
                model_name=os.getenv("TOOLKIT_MODEL", "gemini-1.5-flash"),
                temperature=float(os.getenv("TOOLKIT_TEMPERATURE", "0.7"))
            )
        elif openai_key:
            return cls(
                provider="openai",
                api_key=openai_key,
                model_name=os.getenv("TOOLKIT_MODEL", "gpt-4o-mini"),
                temperature=float(os.getenv("TOOLKIT_TEMPERATURE", "0.7"))
            )
        elif anthropic_key:
            return cls(
                provider="anthropic",
                api_key=anthropic_key,
                model_name=os.getenv("TOOLKIT_MODEL", "claude-3-5-sonnet-20241022"),
                temperature=float(os.getenv("TOOLKIT_TEMPERATURE", "0.7"))
            )
        else:
            # Fall back to high-fidelity built-in Mock Provider
            return cls(
                provider="mock",
                api_key=None,
                model_name="mock-neural-engine",
                temperature=0.7
            )
