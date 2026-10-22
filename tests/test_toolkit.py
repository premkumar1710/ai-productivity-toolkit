"""
Tests for Day 10: AI Productivity Toolkit
Validates all 4 production workflows and LLM client fallback mechanisms.
"""

import pytest
from day_10_productivity_toolkit.config import ToolkitConfig
from day_10_productivity_toolkit.llm_client import LLMClient
from day_10_productivity_toolkit.modules.summarizer import SummarizerWorkflow
from day_10_productivity_toolkit.modules.email_assistant import EmailAssistantWorkflow
from day_10_productivity_toolkit.modules.resume_optimizer import ResumeOptimizerWorkflow, ResumeAnalysisResult
from day_10_productivity_toolkit.modules.coding_assistant import CodingAssistantWorkflow


@pytest.fixture
def client():
    # Use offline mock provider for deterministic CI testing
    cfg = ToolkitConfig(provider="mock", api_key=None, model_name="mock-model")
    return LLMClient(cfg)


def test_summarizer_workflow(client):
    wf = SummarizerWorkflow(client)
    sample_text = "Engineering sprint completed with 99.98% platform availability and reduced latency."
    result = wf.summarize(sample_text, format_type="Executive Brief", audience="Leadership")

    assert result["status"] == "success"
    assert "Executive Summary" in result["summary"]
    assert "Key Takeaways" in result["summary"]
    assert result["word_count"] > 10

    with pytest.raises(ValueError):
        wf.summarize("")


def test_email_assistant_workflow(client):
    wf = EmailAssistantWorkflow(client)
    sample_incoming = "Can you send the revised budget numbers before Friday's executive sync?"
    result = wf.generate_email(sample_incoming, mode="Reply to Email", tone="Executive & Crisp")

    assert result["status"] == "success"
    assert len(result["subject"]) > 0
    assert len(result["body"]) > 0
    assert "Re:" in result["subject"] or "Update" in result["subject"]

    with pytest.raises(ValueError):
        wf.generate_email("   ")


def test_resume_optimizer_workflow(client):
    wf = ResumeOptimizerWorkflow(client)
    sample_resume = "Software Engineer with 4 years building backend APIs in Python and working with PostgreSQL databases."
    sample_jd = "Senior Python Engineer required. Experience with Redis, Kubernetes, and high availability systems."

    analysis = wf.optimize(sample_resume, sample_jd)
    assert isinstance(analysis, ResumeAnalysisResult)
    assert 0 <= analysis.match_score <= 100
    assert len(analysis.strengths) >= 1
    assert len(analysis.skills_gap) >= 1
    assert len(analysis.enhanced_bullet_points) >= 1

    with pytest.raises(ValueError):
        wf.optimize("", "")


def test_coding_assistant_workflow(client):
    wf = CodingAssistantWorkflow(client)
    sample_code = "def add(a, b): return a + b"
    result = wf.process_code_task(sample_code, task="Generate Unit Tests", language="python")

    assert result["status"] == "success"
    assert "pytest" in result["result"].lower() or "python" in result["result"].lower()

    with pytest.raises(ValueError):
        wf.process_code_task("")
