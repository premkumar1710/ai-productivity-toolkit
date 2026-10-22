"""
Workflow 1: Executive Summarizer
Summarizes long-form text, research papers, and meeting notes with custom formats and tone.
"""

from typing import Optional, Dict, Any
from day_10_productivity_toolkit.llm_client import LLMClient


class SummarizerWorkflow:
    """Production workflow for multi-format text summarization."""

    FORMAT_OPTIONS = ["Executive Brief", "TL;DR", "Action Items Only", "Full Digest"]

    def __init__(self, llm_client: Optional[LLMClient] = None):
        self.llm = llm_client or LLMClient()

    def summarize(
        self,
        document_text: str,
        format_type: str = "Executive Brief",
        audience: str = "Leadership & Stakeholders",
        max_words: int = 250,
        preserve_numbers: bool = True
    ) -> Dict[str, Any]:
        if not document_text or not document_text.strip():
            raise ValueError("Document text cannot be empty.")

        system_prompt = (
            f"You are a Principal Intelligence Analyst. "
            f"Your mission is to distill the provided content for {audience} with absolute factual fidelity."
        )

        constraints = [
            f"Maximum summary length: {max_words} words.",
            "Do NOT include conversational filler or preambles ('Here is your summary...').",
            "Under NO circumstances hallucinate numbers or statistics."
        ]
        if preserve_numbers:
            constraints.append("Explicitly preserve all key metrics, percentages, and dollar figures.")

        constraints_str = "\n".join(f"- {c}" for c in constraints)

        prompt = f"""
Format Type requested: {format_type}
Target Audience: {audience}

<constraints>
{constraints_str}
</constraints>

<source_document>
{document_text}
</source_document>

Produce the requested summary following standard markdown headings:
### Executive Summary
### Key Takeaways
### Action Items & Next Steps
"""

        summary_output = self.llm.generate(prompt=prompt, system_prompt=system_prompt)

        return {
            "format": format_type,
            "audience": audience,
            "summary": summary_output,
            "word_count": len(summary_output.split()),
            "status": "success"
        }
