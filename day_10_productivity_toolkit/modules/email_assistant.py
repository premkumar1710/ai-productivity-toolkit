"""
Workflow 2: Smart Email Assistant
Drafts professional replies, cold outreaches, and follow-ups with customizable tone and intent.
"""

from typing import Optional, Dict, Any
from day_10_productivity_toolkit.llm_client import LLMClient


class EmailAssistantWorkflow:
    """Production workflow for enterprise communication and email generation."""

    MODES = ["Reply to Email", "Cold Outreach", "Follow-up", "Meeting Scheduling"]
    TONES = ["Executive & Crisp", "Warm & Collaborative", "Direct & Assertive", "Polite De-escalation"]

    def __init__(self, llm_client: Optional[LLMClient] = None):
        self.llm = llm_client or LLMClient()

    def generate_email(
        self,
        context_or_incoming: str,
        mode: str = "Reply to Email",
        tone: str = "Executive & Crisp",
        sender_name: str = "Alex Morgan",
        recipient_name: str = "Team",
        key_points_to_cover: Optional[str] = None
    ) -> Dict[str, Any]:
        if not context_or_incoming or not context_or_incoming.strip():
            raise ValueError("Input context or incoming email cannot be empty.")

        system_prompt = (
            f"You are an Executive Communications Specialist. "
            f"Draft high-impact business emails with a '{tone}' tone."
        )

        instructions = [
            f"Mode: {mode}",
            f"Sender Name: {sender_name}",
            f"Recipient Name: {recipient_name}",
            "Provide a clear, engaging Subject line at the very top starting with 'Subject:'.",
            "Be concise, actionable, and eliminate unnecessary corporate fluff.",
            "Do NOT include conversational preambles outside the email text."
        ]

        if key_points_to_cover:
            instructions.append(f"Ensure the following points are addressed: {key_points_to_cover}")

        inst_str = "\n".join(f"- {i}" for i in instructions)

        prompt = f"""
Instructions:
{inst_str}

<incoming_context>
{context_or_incoming}
</incoming_context>

Generate the complete email now:
"""

        email_output = self.llm.generate(prompt=prompt, system_prompt=system_prompt)

        # Extract subject line if present
        subject = "Project Update & Proposed Next Steps"
        body = email_output
        lines = email_output.strip().split("\n")
        if lines and lines[0].lower().startswith("subject:"):
            subject = lines[0][len("subject:"):].strip()
            body = "\n".join(lines[1:]).strip()

        return {
            "mode": mode,
            "tone": tone,
            "subject": subject,
            "body": body,
            "full_text": email_output,
            "status": "success"
        }
