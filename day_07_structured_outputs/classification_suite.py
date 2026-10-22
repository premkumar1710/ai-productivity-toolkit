"""
Day 7: Classification Suite
Multi-class, multi-label text classification and triage routing with confidence scoring.
"""

from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field


class UrgencyLevel(str, Enum):
    P0_CRITICAL = "P0_CRITICAL"
    P1_HIGH = "P1_HIGH"
    P2_MEDIUM = "P2_MEDIUM"
    P3_LOW = "P3_LOW"


class TicketCategory(str, Enum):
    BILLING = "BILLING"
    TECHNICAL_BUG = "TECHNICAL_BUG"
    FEATURE_REQUEST = "FEATURE_REQUEST"
    SECURITY = "SECURITY"
    ACCOUNT_ACCESS = "ACCOUNT_ACCESS"


class ClassificationReport(BaseModel):
    category: TicketCategory
    urgency: UrgencyLevel
    sentiment: str = Field(description="POSITIVE, NEUTRAL, or FRUSTRATED")
    confidence_score: float = Field(ge=0.0, le=1.0)
    requires_human_escalation: bool
    reasoning: str
    suggested_routing: str


class ClassificationSuite:
    """Classifies incoming text with strict confidence intervals and routing rules."""

    @staticmethod
    def build_prompt(ticket_text: str) -> str:
        return f"""
You are an Enterprise Support Triage AI.
Analyze the following support inquiry and output a structured classification object in JSON.

<ticket>
{ticket_text}
</ticket>

Taxonomy:
- Categories: [BILLING, TECHNICAL_BUG, FEATURE_REQUEST, SECURITY, ACCOUNT_ACCESS]
- Urgency: [P0_CRITICAL, P1_HIGH, P2_MEDIUM, P3_LOW]
- Sentiment: [POSITIVE, NEUTRAL, FRUSTRATED]

Rules:
1. P0_CRITICAL should be assigned only to service outages, data breaches, or payment theft.
2. If confidence_score < 0.75, set requires_human_escalation = true.
3. Return ONLY valid JSON adhering to the specified schema.
"""

    @staticmethod
    def mock_classify(ticket_text: str) -> ClassificationReport:
        lower = ticket_text.lower()
        if "breach" in lower or "leak" in lower or "hacked" in lower:
            return ClassificationReport(
                category=TicketCategory.SECURITY,
                urgency=UrgencyLevel.P0_CRITICAL,
                sentiment="FRUSTRATED",
                confidence_score=0.98,
                requires_human_escalation=True,
                reasoning="Potential compromise detected; security protocol triggered.",
                suggested_routing="SecOps On-Call"
            )
        elif "charged" in lower or "refund" in lower or "invoice" in lower:
            return ClassificationReport(
                category=TicketCategory.BILLING,
                urgency=UrgencyLevel.P2_MEDIUM,
                sentiment="FRUSTRATED",
                confidence_score=0.91,
                requires_human_escalation=False,
                reasoning="Standard billing query regarding billing amount or refund.",
                suggested_routing="Billing Tier 1"
            )
        else:
            return ClassificationReport(
                category=TicketCategory.TECHNICAL_BUG,
                urgency=UrgencyLevel.P2_MEDIUM,
                sentiment="NEUTRAL",
                confidence_score=0.85,
                reasoning="User reported unexpected behavior in application flow.",
                requires_human_escalation=False,
                suggested_routing="Engineering Support"
            )


def demonstrate():
    sample_ticket = "URGENT: Our production cluster credentials were inadvertently exposed in a public repository! Please revoke them immediately."
    suite = ClassificationSuite()
    print("=" * 60)
    print("DAY 7: CLASSIFICATION TRIAGE DEMONSTRATION")
    print("=" * 60)
    result = suite.mock_classify(sample_ticket)
    print(f"Ticket: \"{sample_ticket}\"")
    print(f"- Category:    {result.category.value}")
    print(f"- Urgency:     {result.urgency.value}")
    print(f"- Sentiment:   {result.sentiment}")
    print(f"- Confidence:  {result.confidence_score * 100:.1f}%")
    print(f"- Human Escalation: {result.requires_human_escalation}")
    print(f"- Routing:     {result.suggested_routing}")
    print(f"- Reasoning:   {result.reasoning}")


if __name__ == "__main__":
    demonstrate()
