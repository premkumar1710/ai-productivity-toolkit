"""
Day 6: Interactive Prompt Engineering Exercises
Beginner practice challenges with automated evaluation & scoring.
"""

from typing import Dict, Any, List


class PromptExerciseTester:
    """Evaluates student prompts against standardized prompt engineering test criteria."""

    @staticmethod
    def test_delimiter_isolation(student_prompt: str) -> Dict[str, Any]:
        """Checks if the prompt wraps user input in structured delimiters (XML or triple quotes)."""
        has_xml = "<user_input>" in student_prompt or "<document>" in student_prompt or "<text>" in student_prompt
        has_quotes = '"""' in student_prompt or "```" in student_prompt
        passed = has_xml or has_quotes
        return {
            "exercise": "Exercise 1: Delimiter Isolation",
            "passed": passed,
            "feedback": "Prompt properly isolates input with delimiters." if passed else "Missing delimiters! Use XML tags or triple quotes."
        }

    @staticmethod
    def test_negative_constraints(student_prompt: str) -> Dict[str, Any]:
        """Checks if the prompt specifies explicit negative constraints."""
        neg_indicators = ["do not", "never", "avoid", "under no circumstances", "without"]
        passed = any(ind in student_prompt.lower() for ind in neg_indicators)
        return {
            "exercise": "Exercise 2: Negative Constraints",
            "passed": passed,
            "feedback": "Prompt includes clear negative guardrails." if passed else "No negative constraints found. Use phrases like 'Do NOT include...'."
        }

    @staticmethod
    def test_role_definition(student_prompt: str) -> Dict[str, Any]:
        """Checks if the prompt explicitly assigns a professional persona/role."""
        role_indicators = ["you are a", "act as a", "as an expert", "role:"]
        passed = any(ind in student_prompt.lower() for ind in role_indicators)
        return {
            "exercise": "Exercise 3: Persona / Role Framing",
            "passed": passed,
            "feedback": "Role clearly defined." if passed else "Missing role definition! Begin with 'You are an expert...' or similar."
        }

    @staticmethod
    def test_few_shot_structure(student_prompt: str) -> Dict[str, Any]:
        """Checks if the prompt contains multiple demonstration pairs."""
        input_count = student_prompt.lower().count("input:") + student_prompt.lower().count("example")
        output_count = student_prompt.lower().count("output:") + student_prompt.lower().count("label:")
        passed = input_count >= 2 and output_count >= 2
        return {
            "exercise": "Exercise 4: Few-Shot Exemplars",
            "passed": passed,
            "feedback": f"Found {input_count} demonstration pairs." if passed else "Need at least 2 complete input/output exemplar pairs."
        }


def run_exercise_check():
    sample_student_prompt = """
    You are an expert Data Privacy Officer.
    Review the incoming user text and redact any Personally Identifiable Information (PII).
    
    <rules>
    - Do NOT include full credit card numbers or Social Security Numbers in the output.
    - Replace detected emails with [EMAIL_REDACTED].
    </rules>

    Examples:
    Input: Contact me at jane@example.com for info.
    Output: Contact me at [EMAIL_REDACTED] for info.

    Input: SSN is 000-12-3456.
    Output: SSN is [PII_REDACTED].

    <document>
    User inquiry: My email is bob@acme.org and phone is 555-0199.
    </document>
    Output:
    """

    tests = [
        PromptExerciseTester.test_delimiter_isolation(sample_student_prompt),
        PromptExerciseTester.test_negative_constraints(sample_student_prompt),
        PromptExerciseTester.test_role_definition(sample_student_prompt),
        PromptExerciseTester.test_few_shot_structure(sample_student_prompt),
    ]

    print("=" * 60)
    print("DAY 6: PROMPT ENGINEERING EXERCISE EVALUATION")
    print("=" * 60)
    total_passed = 0
    for t in tests:
        status = "PASSED [OK]" if t["passed"] else "FAILED [X]"
        print(f"{t['exercise']:<32} : {status} - {t['feedback']}")
        if t["passed"]:
            total_passed += 1

    print(f"\nFinal Score: {total_passed}/{len(tests)} exercises passed.")


if __name__ == "__main__":
    run_exercise_check()
