"""
Tests for Day 9: Prompt Evaluation, Testing Framework & Benchmarking
"""

import pytest
from day_09_eval_and_benchmarking.prompt_template_engine import PromptTemplate, TemplateRegistry
from day_09_eval_and_benchmarking.prompt_evaluator import TestCase, PromptEvaluator


def test_prompt_template_engine():
    tmpl = PromptTemplate(
        name="test_prompt",
        template_str="Hello {name}, your role is {role}.",
        defaults={"role": "Architect"}
    )
    assert tmpl.slots == {"name", "role"}

    rendered = tmpl.render(name="Alice")
    assert rendered == "Hello Alice, your role is Architect."

    with pytest.raises(KeyError):
        # Missing required parameter 'name'
        empty_tmpl = PromptTemplate(name="missing", template_str="{target}")
        empty_tmpl.render()


def test_template_registry():
    reg = TemplateRegistry()
    t1 = PromptTemplate(name="summarizer", template_str="{text}", version="1.0.0")
    t2 = PromptTemplate(name="summarizer", template_str="{text} v2", version="2.0.0")

    reg.register(t1)
    reg.register(t2)

    assert reg.get("summarizer", "1.0.0").version == "1.0.0"
    assert reg.get("summarizer").version == "2.0.0"


def test_prompt_evaluator():
    cases = [
        TestCase(
            id="TC-01",
            input_text="Refund request for billing error",
            expected_category="BILLING",
            forbidden_words=["sorry"],
            max_words=50
        )
    ]

    evaluator = PromptEvaluator(cases)

    # Runner that violates constraints (contains 'sorry' and no JSON)
    def bad_runner(text):
        return "I am so sorry, this is billing."

    # Runner that passes all constraints & schema
    def good_runner(text):
        return '{"category": "BILLING", "status": "resolved"}'

    results_bad = evaluator.evaluate_prompt_variant("bad_v1", bad_runner)
    results_good = evaluator.evaluate_prompt_variant("good_v2", good_runner)

    assert results_bad[0].constraints_passed is False
    assert results_bad[0].schema_passed is False

    assert results_good[0].constraints_passed is True
    assert results_good[0].schema_passed is True
    assert results_good[0].total_score == 100.0

    report = evaluator.generate_markdown_report(results_bad, results_good)
    assert "Prompt Engineering Benchmark Report" in report
    assert "Delta" in report
