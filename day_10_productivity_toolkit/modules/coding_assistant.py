"""
Workflow 4: Coding & Research Assistant
Generates unit tests, explains complex algorithms, debugs errors, and summarizes technical research.
"""

from typing import Optional, Dict, Any
from day_10_productivity_toolkit.llm_client import LLMClient


class CodingAssistantWorkflow:
    """Production workflow for AI-assisted software development and research analysis."""

    TASKS = ["Explain Code", "Generate Unit Tests", "Debug & Refactor", "Research Summarization"]

    def __init__(self, llm_client: Optional[LLMClient] = None):
        self.llm = llm_client or LLMClient()

    def process_code_task(
        self,
        code_or_query: str,
        task: str = "Explain Code",
        language: str = "python",
        context: Optional[str] = None
    ) -> Dict[str, Any]:
        if not code_or_query.strip():
            raise ValueError("Code snippet or query cannot be empty.")

        system_prompt = (
            "You are a Staff Research Engineer. "
            "Provide production-grade code, rigorous unit tests, and deep architectural insights."
        )

        prompt = f"""
Task: {task}
Target Language: {language}
Additional Context: {context or 'None'}

<code_snippet>
{code_or_query}
</code_snippet>

Requirements:
- If generating code, include complete type annotations and docstrings.
- If writing tests, use pytest and test boundary conditions.
- If explaining, break down time/space complexity (Big-O) and design choices.
- Output clean, syntax-highlighted Markdown.
"""

        response = self.llm.generate(prompt=prompt, system_prompt=system_prompt)

        return {
            "task": task,
            "language": language,
            "result": response,
            "status": "success"
        }
