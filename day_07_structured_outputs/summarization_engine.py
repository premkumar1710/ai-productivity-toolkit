"""
Day 7: Multi-Format Summarization Engine
Generates executive summaries, bullet takeaways, and action items with structured schemas.
"""

import sys
from pathlib import Path

# Ensure project root is in sys.path
root_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from day_07_structured_outputs.json_extractor import JSONExtractor


class SummarizationResult(BaseModel):
    executive_summary: str = Field(description="High-level 2-3 sentence overview")
    key_takeaways: List[str] = Field(description="Bullet points of essential factual insights")
    action_items: List[Dict[str, str]] = Field(description="Actionable tasks with assigned owner/context")
    reading_time_minutes: int = Field(description="Estimated reading time in minutes")


class SummarizationEngine:
    """Builds and manages structured summarization pipelines."""

    @staticmethod
    def build_prompt(
        document_text: str,
        target_audience: str = "Engineering Leadership",
        max_words: int = 250
    ) -> str:
        return f"""
You are an expert Executive Research Analyst.
Your goal is to summarize the document below for: {target_audience}.

<document>
{document_text}
</document>

Instructions:
1. Provide a concise executive summary (maximum 3 sentences).
2. Extract 3 to 5 core key takeaways.
3. Identify all concrete action items. If an owner is not mentioned, mark owner as 'Unassigned'.
4. Total length of summary must not exceed {max_words} words.
5. Return ONLY a valid JSON object matching this exact schema:
{{
    "executive_summary": "string",
    "key_takeaways": ["point 1", "point 2"],
    "action_items": [
        {{"task": "description", "owner": "name or role"}}
    ],
    "reading_time_minutes": 2
}}
"""

    @staticmethod
    def mock_summarize(document_text: str) -> SummarizationResult:
        """Deterministic mock response for offline testing."""
        return SummarizationResult(
            executive_summary="The Q3 engineering review showed 99.98% platform uptime, with significant velocity improvements after migrating to containerized microservices.",
            key_takeaways=[
                "Uptime exceeded the 99.95% SLA target.",
                "P99 latency dropped by 42% following Redis caching optimizations.",
                "Database infrastructure costs were reduced by $18,000/month."
            ],
            action_items=[
                {"task": "Complete Redis cluster cross-region replication", "owner": "DevOps Team"},
                {"task": "Audit IAM permissions for new staging accounts", "owner": "Security Team"}
            ],
            reading_time_minutes=2
        )


def demonstrate():
    sample_text = """
    During today's architectural sync, the team reviewed Q3 operational performance.
    We achieved 99.98% availability against our 99.95% SLA. P99 API response latencies dropped
    from 420ms to 240ms after transitioning to Redis clusters. Monthly AWS database expenditures
    dropped by $18,000. For next sprint, Alice needs to finalize the multi-region replica deployment,
    and Dave will conduct the security audit on our Kubernetes cluster role bindings.
    """

    engine = SummarizationEngine()
    prompt = engine.build_prompt(sample_text)

    print("=" * 60)
    print("DAY 7: STRUCTURED SUMMARIZATION PROMPT")
    print("=" * 60)
    print(prompt)

    print("\n" + "=" * 60)
    print("GENERATED STRUCTURED SUMMARY RESULT")
    print("=" * 60)
    result = engine.mock_summarize(sample_text)
    print(f"Executive Summary: {result.executive_summary}\n")
    print("Key Takeaways:")
    for pt in result.key_takeaways:
        print(f"  * {pt}")
    print("\nAction Items:")
    for item in result.action_items:
        print(f"  - [{item['owner']}]: {item['task']}")


if __name__ == "__main__":
    demonstrate()
