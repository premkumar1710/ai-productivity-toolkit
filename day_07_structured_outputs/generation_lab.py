"""
Day 7: Structured Content Generation Lab
Generates release notes, technical announcements, and changelogs according to strict specifications.
"""

from typing import List
from pydantic import BaseModel, Field


class ReleaseNotes(BaseModel):
    version: str = Field(description="Semantic version string, e.g. v2.1.0")
    title: str = Field(description="Catchy, professional release headline")
    summary: str = Field(description="High-level overview of this release")
    features: List[str] = Field(description="New capabilities delivered")
    bug_fixes: List[str] = Field(description="Resolved issues and bug fixes")
    breaking_changes: List[str] = Field(description="Incompatible API changes, if any")
    migration_steps: List[str] = Field(description="Steps required for upgrade")


class GenerationLab:
    """Pipelines for generating technical and business communications."""

    @staticmethod
    def build_release_notes_prompt(raw_commit_log: str, version: str) -> str:
        return f"""
You are a Technical Product Manager preparing customer-facing release notes.
Transform the following raw git commit messages into structured release notes for version {version}.

<git_commits>
{raw_commit_log}
</git_commits>

Guidelines:
1. Group commits logically into features, bug_fixes, and breaking_changes.
2. Rephrase cryptic developer commit messages into clear, benefit-driven customer copy.
3. If no breaking changes occurred, provide an empty list.
4. Output strictly valid JSON conforming to the ReleaseNotes schema.
"""

    @staticmethod
    def mock_generate_release_notes(raw_commits: str, version: str = "v1.4.0") -> ReleaseNotes:
        return ReleaseNotes(
            version=version,
            title="Performance Enhancements and Advanced Filtering",
            summary="This release introduces low-latency database queries, dynamic filter widgets, and fixes memory leaks in background jobs.",
            features=[
                "Added multi-column filtering to the data explorer dashboard.",
                "Introduced asynchronous export of reports to PDF and CSV formats.",
                "Enabled dark mode support across all user settings."
            ],
            bug_fixes=[
                "Fixed race condition in session token refresh logic (#412).",
                "Corrected datetime parsing issue for UTC timestamps in email reports (#435)."
            ],
            breaking_changes=[],
            migration_steps=[
                "Run database migrations: `alembic upgrade head`",
                "Update config file to include `REDIS_CACHE_TTL=3600`"
            ]
        )


def demonstrate():
    commits = """
    feat: add multi-column filtering to table UI
    fix: race condition on session refresh (#412)
    feat: async PDF/CSV export worker
    fix: UTC timestamp parsing bug in daily digests (#435)
    style: dark mode styling variables
    """
    lab = GenerationLab()
    print("=" * 60)
    print("DAY 7: STRUCTURED CONTENT GENERATION (RELEASE NOTES)")
    print("=" * 60)
    notes = lab.mock_generate_release_notes(commits, "v1.4.0")
    print(f"Version: {notes.version} - {notes.title}")
    print(f"Summary: {notes.summary}\n")
    print("Key Features:")
    for f in notes.features:
        print(f"  + {f}")
    print("\nBug Fixes:")
    for b in notes.bug_fixes:
        print(f"  - {b}")
    print("\nMigration Steps:")
    for s in notes.migration_steps:
        print(f"  > {s}")


if __name__ == "__main__":
    demonstrate()
