"""
Workflow 3: Resume & Career Optimizer
Matches resumes against Job Descriptions, calculates ATS scores, finds skill gaps, and enhances bullet points.
"""

from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field
from day_10_productivity_toolkit.llm_client import LLMClient
from day_07_structured_outputs.json_extractor import JSONExtractor


class ResumeAnalysisResult(BaseModel):
    match_score: int = Field(ge=0, le=100, description="ATS alignment score from 0 to 100")
    strengths: List[str] = Field(description="Strong matches between resume and job spec")
    skills_gap: List[str] = Field(description="Missing technical or domain skills")
    enhanced_bullet_points: List[str] = Field(description="Bullet points rewritten using Google's XYZ formula")
    tailored_cover_letter_snippet: str = Field(description="High-impact opening paragraph for cover letter")


class ResumeOptimizerWorkflow:
    """Production workflow for ATS resume auditing and career asset optimization."""

    def __init__(self, llm_client: Optional[LLMClient] = None):
        self.llm = llm_client or LLMClient()

    def optimize(
        self,
        resume_text: str,
        job_description: str,
        target_role: str = "Senior Software Engineer"
    ) -> ResumeAnalysisResult:
        if not resume_text.strip() or not job_description.strip():
            raise ValueError("Resume and Job Description cannot be empty.")

        system_prompt = (
            "You are a Principal Technical Recruiter and Career Strategist. "
            "Analyze candidates against exact job specifications with ruthless objectivity."
        )

        prompt = f"""
Target Role: {target_role}

<job_description>
{job_description}
</job_description>

<candidate_resume>
{resume_text}
</candidate_resume>

Tasks:
1. Calculate an ATS match score (0 to 100) based on requirements coverage.
2. Identify candidate's top 3 strengths aligned with this job.
3. Identify top 2-3 missing skills or gaps.
4. Rewrite 3 bullet points using Google's XYZ formula:
   'Accomplished [X] as measured by [Y], by doing [Z]'.
5. Draft a tailored cover letter opening paragraph.

Return ONLY a valid JSON object matching this schema:
{{
  "match_score": 85,
  "strengths": ["string"],
  "skills_gap": ["string"],
  "enhanced_bullet_points": ["string"],
  "tailored_cover_letter_snippet": "string"
}}
"""

        raw_output = self.llm.generate(prompt=prompt, system_prompt=system_prompt)

        try:
            return JSONExtractor.parse_as_model(raw_output, ResumeAnalysisResult)
        except Exception:
            # Fallback parsing
            data = JSONExtractor.extract_json(raw_output)
            return ResumeAnalysisResult.model_validate(data)
