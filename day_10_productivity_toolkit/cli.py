"""
AI Productivity Toolkit - Interactive CLI
Built with Rich for high-signal, beautiful terminal workflows.
"""

import sys
from pathlib import Path

# Safe UTF-8 encoding configuration for Windows terminals
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# Ensure project root is in sys.path
root_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

import argparse
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt, IntPrompt
from rich.markdown import Markdown

from day_10_productivity_toolkit.config import ToolkitConfig
from day_10_productivity_toolkit.llm_client import LLMClient
from day_10_productivity_toolkit.modules.summarizer import SummarizerWorkflow
from day_10_productivity_toolkit.modules.email_assistant import EmailAssistantWorkflow
from day_10_productivity_toolkit.modules.resume_optimizer import ResumeOptimizerWorkflow
from day_10_productivity_toolkit.modules.coding_assistant import CodingAssistantWorkflow

console = Console()


def print_banner():
    console.print(
        Panel.fit(
            "[bold cyan]AI PRODUCTIVITY TOOLKIT[/bold cyan]\n"
            "[dim]Reusable Workflows: Summarization · Email · Resume · Coding & Research[/dim]\n"
            f"[yellow]Active Provider: {ToolkitConfig.load().provider.upper()} ({ToolkitConfig.load().model_name})[/yellow]",
            border_style="cyan"
        )
    )


def handle_summarizer(client: LLMClient, interactive: bool = True):
    console.print("\n[bold green]=== Executive Summarizer ===[/bold green]")
    doc = ""
    if interactive:
        doc = Prompt.ask("Enter or paste text to summarize (or press Enter for default sample)")
    if not doc.strip():
        doc = (
            "During Q3, engineering achieved 99.98% platform uptime, exceeding the 99.95% SLA. "
            "P99 latency decreased from 450ms to 230ms after implementing Redis clustering. "
            "Monthly cloud database costs fell by $14,000. For next sprint, Bob must finalize "
            "the multi-region failover and Sarah will lead the security penetration audit."
        )
        console.print(f"[dim]Using sample input ({len(doc.split())} words)...[/dim]")

    wf = SummarizerWorkflow(client)
    with console.status("[bold green]Generating structured executive summary..."):
        result = wf.summarize(doc)

    console.print("\n[bold]Output Summary:[/bold]")
    console.print(Markdown(result["summary"]))


def handle_email(client: LLMClient, interactive: bool = True):
    console.print("\n[bold green]=== Smart Email Assistant ===[/bold green]")
    incoming = ""
    if interactive:
        incoming = Prompt.ask("Enter incoming email context (or press Enter for default sample)")
    if not incoming.strip():
        incoming = "Can you send over the updated project timeline and confirm if we're on track for Friday's release?"
        console.print("[dim]Using sample inquiry...[/dim]")

    wf = EmailAssistantWorkflow(client)
    with console.status("[bold green]Drafting professional email..."):
        result = wf.generate_email(incoming, tone="Executive & Crisp")

    table = Table(title="Generated Email Draft", border_style="blue")
    table.add_column("Field", style="cyan", width=12)
    table.add_column("Content", style="white")
    table.add_row("Subject", result["subject"])
    table.add_row("Body", result["body"])
    console.print(table)


def handle_resume(client: LLMClient, interactive: bool = True):
    console.print("\n[bold green]=== Resume & Career Optimizer ===[/bold green]")
    console.print("[dim]Running ATS keyword matching and XYZ formula enhancement on sample profile...[/dim]")

    sample_resume = "Software Engineer with 4 years building backend APIs in Python and working with PostgreSQL databases."
    sample_jd = "Senior Python Engineer required. Must have experience scaling microservices, Redis caching, Kubernetes, and high availability systems."

    wf = ResumeOptimizerWorkflow(client)
    with console.status("[bold green]Analyzing resume against job description..."):
        analysis = wf.optimize(sample_resume, sample_jd)

    console.print(f"\n[bold yellow]ATS Match Score: {analysis.match_score}/100[/bold yellow]")
    console.print("\n[bold]Identified Strengths:[/bold]")
    for s in analysis.strengths:
        console.print(f"  [green]+[/green] {s}")

    console.print("\n[bold]Skills Gap to Address:[/bold]")
    for g in analysis.skills_gap:
        console.print(f"  [red]-[/red] {g}")

    console.print("\n[bold]Enhanced Bullet Points (Google XYZ Formula):[/bold]")
    for b in analysis.enhanced_bullet_points:
        console.print(f"  [cyan]•[/cyan] {b}")


def handle_coding(client: LLMClient, interactive: bool = True):
    console.print("\n[bold green]=== Coding & Research Assistant ===[/bold green]")
    sample_code = """
def find_duplicates(numbers):
    duplicates = []
    for i in range(len(numbers)):
        for j in range(i + 1, len(numbers)):
            if numbers[i] == numbers[j] and numbers[i] not in duplicates:
                duplicates.append(numbers[i])
    return duplicates
    """
    console.print("[dim]Target: Optimize O(N^2) duplicate finder and generate pytest suite...[/dim]")

    wf = CodingAssistantWorkflow(client)
    with console.status("[bold green]Analyzing code and generating test suite..."):
        result = wf.process_code_task(sample_code, task="Debug & Refactor")

    console.print(Markdown(result["result"]))


def run_all_demos():
    client = LLMClient()
    print_banner()
    handle_summarizer(client, interactive=False)
    handle_email(client, interactive=False)
    handle_resume(client, interactive=False)
    handle_coding(client, interactive=False)
    console.print("\n[bold green][SUCCESS] All 4 Productivity Toolkit workflows executed successfully![/bold green]")


def main():
    parser = argparse.ArgumentParser(description="AI Productivity Toolkit CLI")
    parser.add_argument("--demo", action="store_true", help="Run automated demonstration across all 4 workflows")
    args = parser.parse_args()

    if args.demo:
        run_all_demos()
        return

    client = LLMClient()
    print_banner()

    while True:
        console.print("\n[bold]Select a Workflow:[/bold]")
        console.print("1. Executive Summarizer")
        console.print("2. Smart Email Assistant")
        console.print("3. Resume & Career Optimizer (ATS Analyzer)")
        console.print("4. Coding & Research Assistant")
        console.print("5. Run All Workflows Demo")
        console.print("6. Exit")

        choice = Prompt.ask("Choose an option", choices=["1", "2", "3", "4", "5", "6"], default="5")
        if choice == "1":
            handle_summarizer(client)
        elif choice == "2":
            handle_email(client)
        elif choice == "3":
            handle_resume(client)
        elif choice == "4":
            handle_coding(client)
        elif choice == "5":
            run_all_demos()
        elif choice == "6":
            console.print("[dim]Goodbye![/dim]")
            break


if __name__ == "__main__":
    main()
