"""
Tests for Day 7: Structured Outputs & Core NLP Tasks
"""

import pytest
from pydantic import BaseModel
from day_07_structured_outputs.json_extractor import JSONExtractor
from day_07_structured_outputs.summarization_engine import SummarizationEngine, SummarizationResult
from day_07_structured_outputs.classification_suite import ClassificationSuite, TicketCategory, UrgencyLevel
from day_07_structured_outputs.generation_lab import GenerationLab


class SampleSchema(BaseModel):
    category: str
    score: int
    tags: list[str]


def test_json_extractor_clean_markdown():
    markdown_payload = """
    Here is your JSON response:
    ```json
    {
        "category": "INFRASTRUCTURE",
        "score": 95,
        "tags": ["cloud", "k8s"]
    }
    ```
    Have a nice day!
    """
    data = JSONExtractor.extract_json(markdown_payload)
    assert data["category"] == "INFRASTRUCTURE"
    assert data["score"] == 95
    assert len(data["tags"]) == 2

    # Pydantic parsing
    model = JSONExtractor.parse_as_model(markdown_payload, SampleSchema)
    assert model.category == "INFRASTRUCTURE"
    assert model.score == 95


def test_json_extractor_handles_trailing_comma():
    trailing_comma_json = """
    {
        "category": "DATABASE",
        "score": 80,
        "tags": ["postgres", "index"],
    }
    """
    model = JSONExtractor.parse_as_model(trailing_comma_json, SampleSchema)
    assert model.category == "DATABASE"
    assert model.score == 80


def test_summarization_engine():
    engine = SummarizationEngine()
    prompt = engine.build_prompt("Text about architecture and SLA.", max_words=100)
    assert "Executive Research Analyst" in prompt
    assert "reading_time_minutes" in prompt

    res = engine.mock_summarize("Text")
    assert isinstance(res, SummarizationResult)
    assert len(res.key_takeaways) >= 3
    assert len(res.action_items) >= 2


def test_classification_suite():
    suite = ClassificationSuite()
    # Security ticket test
    sec_ticket = "Emergency: security breach and api key leaked on public forum"
    report_sec = suite.mock_classify(sec_ticket)
    assert report_sec.category == TicketCategory.SECURITY
    assert report_sec.urgency == UrgencyLevel.P0_CRITICAL
    assert report_sec.requires_human_escalation is True

    # Billing ticket test
    bill_ticket = "Why was I charged twice for the monthly plan?"
    report_bill = suite.mock_classify(bill_ticket)
    assert report_bill.category == TicketCategory.BILLING
    assert report_bill.confidence_score >= 0.8


def test_generation_lab():
    lab = GenerationLab()
    notes = lab.mock_generate_release_notes("feat: add search\nfix: memory leak", "v2.0.0")
    assert notes.version == "v2.0.0"
    assert len(notes.features) > 0
    assert len(notes.bug_fixes) > 0
