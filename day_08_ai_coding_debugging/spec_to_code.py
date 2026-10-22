"""
Day 8: Spec-Driven Code Generation
Transforms formal functional specifications into typed, documented, production-ready Python code.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional


@dataclass
class CodeSpec:
    function_name: str
    description: str
    inputs: List[Dict[str, str]]
    output_type: str
    constraints: List[str]
    exceptions_raised: List[Dict[str, str]]
    examples: List[Dict[str, str]]


class SpecToCodeGenerator:
    """Builds structured prompts and synthesizes Python functions from formal specs."""

    @staticmethod
    def build_prompt(spec: CodeSpec) -> str:
        inputs_str = ", ".join(f"{inp['name']}: {inp['type']}" for inp in spec.inputs)
        constraints_str = "\n".join(f"- {c}" for c in spec.constraints)
        exceptions_str = "\n".join(f"- {e['type']}: {e['condition']}" for e in spec.exceptions_raised)
        examples_str = "\n".join(f"  Input: {ex['input']} => Output: {ex['output']}" for ex in spec.examples)

        return f"""
You are a Principal Software Engineer writing enterprise Python 3.
Generate a production-ready implementation of `{spec.function_name}` based on this specification.

Specification:
- Description: {spec.description}
- Signature: def {spec.function_name}({inputs_str}) -> {spec.output_type}:
- Constraints:
{constraints_str}
- Exceptions Raised:
{exceptions_str}
- Examples:
{examples_str}

Implementation Requirements:
1. Complete type annotations on all parameters and return types.
2. Comprehensive Google-style docstrings with Args, Returns, and Raises sections.
3. Strict defensive input validation.
4. Clean code adhering to PEP 8 standards.
5. Provide 2 pytest test cases demonstrating happy path and error handling.
"""

    @staticmethod
    def mock_generate_code(spec: CodeSpec) -> str:
        """Simulated generated code output adhering to the specification."""
        return f'''from typing import List, Optional

def {spec.function_name}(rate_limit_per_minute: int, window_seconds: int = 60) -> bool:
    """
    Evaluates whether an incoming API request conforms to configured rate limits.

    Args:
        rate_limit_per_minute (int): Maximum allowed calls within the time window.
        window_seconds (int): Rolling window duration in seconds. Defaults to 60.

    Returns:
        bool: True if allowed, False if throttled.

    Raises:
        ValueError: If rate_limit_per_minute is non-positive or window_seconds <= 0.
    """
    if rate_limit_per_minute <= 0:
        raise ValueError("rate_limit_per_minute must be strictly greater than 0.")
    if window_seconds <= 0:
        raise ValueError("window_seconds must be strictly greater than 0.")
    
    # Internal token bucket calculation
    return True


# Pytest Test Cases
def test_{spec.function_name}_valid():
    assert {spec.function_name}(100, 60) is True

def test_{spec.function_name}_invalid_rate():
    import pytest
    with pytest.raises(ValueError):
        {spec.function_name}(-5, 60)
'''


def demonstrate():
    spec = CodeSpec(
        function_name="evaluate_rate_limit",
        description="Determines if an API client has exceeded their allowable request allowance.",
        inputs=[
            {"name": "rate_limit_per_minute", "type": "int"},
            {"name": "window_seconds", "type": "int = 60"}
        ],
        output_type="bool",
        constraints=[
            "Must execute in O(1) time complexity.",
            "Must throw ValueError for non-positive input thresholds."
        ],
        exceptions_raised=[
            {"type": "ValueError", "condition": "When rate_limit_per_minute <= 0 or window_seconds <= 0"}
        ],
        examples=[
            {"input": "rate_limit_per_minute=100, window_seconds=60", "output": "True"},
            {"input": "rate_limit_per_minute=0", "output": "ValueError"}
        ]
    )

    gen = SpecToCodeGenerator()
    prompt = gen.build_prompt(spec)
    print("=" * 60)
    print("DAY 8: SPEC-DRIVEN CODE GENERATION PROMPT")
    print("=" * 60)
    print(prompt)

    print("\n" + "=" * 60)
    print("SYNTHESIZED CODE OUTPUT")
    print("=" * 60)
    code = gen.mock_generate_code(spec)
    print(code)


if __name__ == "__main__":
    demonstrate()
