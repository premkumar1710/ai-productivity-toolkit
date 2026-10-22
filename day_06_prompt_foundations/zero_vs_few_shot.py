"""
Day 6: Zero-Shot vs Few-Shot Prompting Engine
Demonstrates how in-context exemplars steer LLM classification and structured reasoning.
"""

from dataclasses import dataclass
from typing import List, Dict, Tuple, Optional


@dataclass
class Example:
    input_text: str
    expected_label: str
    reasoning: Optional[str] = None


class PromptComparator:
    """
    Constructs and inspects Zero-Shot, One-Shot, and Few-Shot prompt variants
    for complex NLP classification tasks.
    """

    def __init__(self, task_description: str, label_options: List[str]):
        self.task_description = task_description
        self.label_options = label_options
        self.exemplars: List[Example] = []

    def add_exemplar(self, input_text: str, label: str, reasoning: Optional[str] = None) -> None:
        if label not in self.label_options:
            raise ValueError(f"Label '{label}' is not in allowed options: {self.label_options}")
        self.exemplars.append(Example(input_text=input_text, expected_label=label, reasoning=reasoning))

    def build_zero_shot_prompt(self, target_input: str) -> str:
        """Constructs an instruction-only prompt with zero exemplars."""
        options_str = ", ".join(self.label_options)
        return (
            f"Task: {self.task_description}\n"
            f"Allowed Labels: [{options_str}]\n\n"
            f"Target Input: \"\"\"\n{target_input}\n\"\"\"\n\n"
            f"Instruction: Return ONLY the exact label from the allowed labels without additional commentary.\n"
            f"Label:"
        )

    def build_few_shot_prompt(self, target_input: str, shot_count: int = 3, include_cot: bool = False) -> str:
        """
        Constructs an in-context learning prompt with N exemplars.
        If include_cot=True, appends Step-by-Step Chain-of-Thought reasoning.
        """
        options_str = ", ".join(self.label_options)
        selected_shots = self.exemplars[:shot_count]

        prompt_lines = [
            f"Task: {self.task_description}",
            f"Allowed Labels: [{options_str}]",
            "\nDemonstrations:"
        ]

        for idx, shot in enumerate(selected_shots, 1):
            prompt_lines.append(f"--- Example {idx} ---")
            prompt_lines.append(f"Input: {shot.input_text}")
            if include_cot and shot.reasoning:
                prompt_lines.append(f"Reasoning: {shot.reasoning}")
            prompt_lines.append(f"Label: {shot.expected_label}\n")

        prompt_lines.append("--- Target Query ---")
        prompt_lines.append(f"Input: {target_input}")
        if include_cot:
            prompt_lines.append("Reasoning: [Step-by-step reasoning]")
        prompt_lines.append("Label:")

        return "\n".join(prompt_lines)

    def simulate_mock_response(self, prompt: str) -> str:
        """
        Deterministic mock responder simulating model behavior for offline testing.
        Identifies whether the prompt was few-shot or zero-shot to simulate expected behavior.
        """
        lower = prompt.lower()
        if "latency" in lower or "slow" in lower:
            if "Example 1" in prompt:
                return "PERFORMANCE_ISSUE"
            return "NEGATIVE"  # Zero-shot often collapses nuanced taxonomy into simple sentiment
        if "fraud" in lower or "unauthorized" in lower:
            return "SECURITY_ALERT"
        if "billing" in lower or "charged" in lower:
            return "BILLING_DISPUTE"
        return "GENERAL_INQUIRY"


def demonstrate():
    comparator = PromptComparator(
        task_description="Classify incoming enterprise support tickets into precise operational categories.",
        label_options=["BILLING_DISPUTE", "SECURITY_ALERT", "PERFORMANCE_ISSUE", "FEATURE_REQUEST", "GENERAL_INQUIRY"]
    )

    # In-context exemplars
    comparator.add_exemplar(
        input_text="My credit card was charged twice for the annual enterprise tier.",
        label="BILLING_DISPUTE",
        reasoning="Payment anomaly involving duplicated charges."
    )
    comparator.add_exemplar(
        input_text="We noticed logins from unknown IP address in Eastern Europe at 3:00 AM.",
        label="SECURITY_ALERT",
        reasoning="Suspicious unauthorized access vector."
    )
    comparator.add_exemplar(
        input_text="API responses went from 120ms to 4800ms after the v2.4 rollout.",
        label="PERFORMANCE_ISSUE",
        reasoning="High latency degradation impacting throughput."
    )

    test_input = "Database queries take 15 seconds to return and dashboard times out."

    zero_shot = comparator.build_zero_shot_prompt(test_input)
    few_shot = comparator.build_few_shot_prompt(test_input, shot_count=3, include_cot=True)

    print("=" * 60)
    print("DAY 6: ZERO-SHOT PROMPT")
    print("=" * 60)
    print(zero_shot)
    print("\nSimulated Zero-Shot Output:", comparator.simulate_mock_response(zero_shot))

    print("\n" + "=" * 60)
    print("DAY 6: FEW-SHOT (3-SHOT + COT) PROMPT")
    print("=" * 60)
    print(few_shot)
    print("\nSimulated Few-Shot Output:", comparator.simulate_mock_response(few_shot))


if __name__ == "__main__":
    demonstrate()
