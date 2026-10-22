"""
Tests for Day 6: Prompt Engineering Foundations
"""

import pytest
from day_06_prompt_foundations.zero_vs_few_shot import PromptComparator
from day_06_prompt_foundations.role_and_constraints import PromptScaffold, ConstraintValidator
from day_06_prompt_foundations.exercises import PromptExerciseTester


def test_zero_vs_few_shot_prompt_building():
    comparator = PromptComparator(
        task_description="Classify error severity",
        label_options=["LOW", "MEDIUM", "HIGH"]
    )
    comparator.add_exemplar("CPU at 98%", "HIGH", "Near saturation point")
    comparator.add_exemplar("Cache miss rate 10%", "LOW", "Normal operating range")

    zero_shot = comparator.build_zero_shot_prompt("Memory at 88%")
    few_shot = comparator.build_few_shot_prompt("Memory at 88%", shot_count=2, include_cot=True)

    assert "Allowed Labels: [LOW, MEDIUM, HIGH]" in zero_shot
    assert "Example 1" in few_shot
    assert "Example 2" in few_shot
    assert "Reasoning: Near saturation point" in few_shot


def test_role_and_constraints_scaffolding():
    scaffold = PromptScaffold(
        role="Security Auditor",
        context="Reviewing IAM policies for HIPAA compliance"
    )
    scaffold.add_instruction("List all wildcards")
    scaffold.add_negative_constraint("Do NOT mention AWS console steps")
    scaffold.set_output_format("JSON array of policy names")

    prompt = scaffold.assemble('{"Statement": [{"Action": "*"}]}')
    assert "<system_role>" in prompt
    assert "<constraints>" in prompt
    assert "Do NOT mention AWS console steps" in prompt
    assert "<user_input>" in prompt


def test_constraint_validator():
    # Test apology detection
    valid_text = "The system encountered connection timeouts on port 5432."
    apologetic_text = "I'm sorry for the inconvenience, but connection failed."

    ok, _ = ConstraintValidator.check_no_apologies(valid_text)
    assert ok is True

    bad, msg = ConstraintValidator.check_no_apologies(apologetic_text)
    assert bad is False
    assert "apology" in msg.lower()

    # Test word limit
    within, _ = ConstraintValidator.check_word_limit("Short brief statement.", 5)
    assert within is True

    over, _ = ConstraintValidator.check_word_limit("One two three four five six seven words.", 5)
    assert over is False

    # Test forbidden terms
    clean, _ = ConstraintValidator.check_forbidden_terms("Internal server error.", ["AWS", "Azure"])
    assert clean is True

    violated, _ = ConstraintValidator.check_forbidden_terms("Hosted on AWS cloud.", ["AWS", "Azure"])
    assert violated is False


def test_exercise_testers():
    valid_prompt = """
    You are a Senior Legal Counsel.
    <document>
    Review this contract.
    </document>
    Do NOT include non-binding introductory remarks.
    Examples:
    Input: Clause A
    Output: Compliant
    Input: Clause B
    Output: Non-compliant
    """
    assert PromptExerciseTester.test_role_definition(valid_prompt)["passed"] is True
    assert PromptExerciseTester.test_delimiter_isolation(valid_prompt)["passed"] is True
    assert PromptExerciseTester.test_negative_constraints(valid_prompt)["passed"] is True
    assert PromptExerciseTester.test_few_shot_structure(valid_prompt)["passed"] is True
