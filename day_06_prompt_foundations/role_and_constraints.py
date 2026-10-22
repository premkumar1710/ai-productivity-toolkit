"""
Day 6: System Roles, Contexts, Delimiters, and Negative Constraints
Demonstrates strict prompt scaffolding and constraint compliance verification.
"""

import re
from typing import List, Dict, Any, Tuple


class PromptScaffold:
    """
    Builds production prompts adhering to the 5 Core Tenets:
    1. Persona (Role)
    2. Context
    3. Clear Instructions
    4. Delimiter Isolation
    5. Constraints & Negative Guardrails
    """

    def __init__(self, role: str, context: str):
        self.role = role
        self.context = context
        self.instructions: List[str] = []
        self.negative_constraints: List[str] = []
        self.output_format_instructions: List[str] = []

    def add_instruction(self, instruction: str) -> "PromptScaffold":
        self.instructions.append(instruction)
        return self

    def add_negative_constraint(self, constraint: str) -> "PromptScaffold":
        """Adds a negative constraint (e.g., 'Do NOT include conversational filler')."""
        self.negative_constraints.append(constraint)
        return self

    def set_output_format(self, format_spec: str) -> "PromptScaffold":
        self.output_format_instructions.append(format_spec)
        return self

    def assemble(self, user_payload: str, delimiter_tag: str = "user_input") -> str:
        """Combines all components with XML delimiter isolation to mitigate prompt injection."""
        sections = [
            f"<system_role>\n{self.role}\n</system_role>",
            f"<context>\n{self.context}\n</context>",
            "<instructions>",
            "\n".join(f"{i+1}. {inst}" for i, inst in enumerate(self.instructions)),
            "</instructions>",
        ]

        if self.negative_constraints:
            sections.extend([
                "<constraints>",
                "\n".join(f"- {c}" for c in self.negative_constraints),
                "</constraints>"
            ])

        if self.output_format_instructions:
            sections.extend([
                "<output_format>",
                "\n".join(self.output_format_instructions),
                "</output_format>"
            ])

        sections.extend([
            f"<{delimiter_tag}>\n{user_payload}\n</{delimiter_tag}>",
            "Output:"
        ])

        return "\n\n".join(sections)


class ConstraintValidator:
    """Validates whether an LLM response adhered to specified negative constraints."""

    @staticmethod
    def check_no_apologies(text: str) -> Tuple[bool, str]:
        apology_patterns = [r"\bi'm sorry\b", r"\bapologies\b", r"\bi apologize\b", r"\bsorry\b"]
        for pat in apology_patterns:
            if re.search(pat, text, re.IGNORECASE):
                return False, f"Constraint violated: Found apology matching '{pat}'."
        return True, "No apologies detected."

    @staticmethod
    def check_word_limit(text: str, max_words: int) -> Tuple[bool, str]:
        words = text.strip().split()
        if len(words) > max_words:
            return False, f"Constraint violated: Text has {len(words)} words, exceeding maximum of {max_words}."
        return True, f"Word count ({len(words)}) within limit ({max_words})."

    @staticmethod
    def check_forbidden_terms(text: str, forbidden_terms: List[str]) -> Tuple[bool, str]:
        found = [term for term in forbidden_terms if term.lower() in text.lower()]
        if found:
            return False, f"Constraint violated: Contains forbidden terms: {found}."
        return True, "No forbidden terms detected."


def demonstrate():
    scaffold = PromptScaffold(
        role="You are a Senior Site Reliability Engineer (SRE) writing incident post-mortems.",
        context="A critical microservice suffered a cascading outage due to connection pool exhaustion."
    )

    scaffold.add_instruction("Analyze the root cause and summarize the timeline.")
    scaffold.add_instruction("List 3 actionable remediations to prevent recurrence.")
    scaffold.add_negative_constraint("Do NOT apologize or use passive voice ('mistakes were made').")
    scaffold.add_negative_constraint("Do NOT mention competitor cloud providers.")
    scaffold.add_negative_constraint("Keep the entire summary under 120 words.")
    scaffold.set_output_format("Provide Markdown headings: ### Root Cause, ### Impact, ### Action Items.")

    raw_user_log = "09:00 Redis latencies spike to 5000ms. 09:05 Connection timeouts cascade. 09:15 Failover completed."
    prompt = scaffold.assemble(raw_user_log)

    print("=" * 60)
    print("DAY 6: STRUCTURED PROMPT SCAFFOLD WITH DELIMITERS")
    print("=" * 60)
    print(prompt)

    # Validate simulated response
    sample_response = (
        "### Root Cause\n"
        "Connection pool saturation on primary Redis cluster induced cascading timeout failures across consumer pods.\n\n"
        "### Impact\n"
        "15 minutes degraded availability affecting write traffic.\n\n"
        "### Action Items\n"
        "1. Implement exponential backoff jitter on reconnects.\n"
        "2. Scale pool headroom by 40%.\n"
        "3. Configure circuit breaker threshold at 80% utilization."
    )

    print("\n" + "=" * 60)
    print("VALIDATING RESPONSE AGAINST CONSTRAINTS")
    print("=" * 60)
    apology_ok, apology_msg = ConstraintValidator.check_no_apologies(sample_response)
    length_ok, length_msg = ConstraintValidator.check_word_limit(sample_response, 120)
    terms_ok, terms_msg = ConstraintValidator.check_forbidden_terms(sample_response, ["AWS", "Azure", "GCP"])

    print(f"Apology Check: {'PASS' if apology_ok else 'FAIL'} -> {apology_msg}")
    print(f"Word Limit:    {'PASS' if length_ok else 'FAIL'} -> {length_msg}")
    print(f"Forbidden:     {'PASS' if terms_ok else 'FAIL'} -> {terms_msg}")


if __name__ == "__main__":
    demonstrate()
