"""
Day 8: Code Refactoring & Security Audit Suite
Performs static analysis and LLM-assisted code review for anti-patterns, security risks, and clean code.
"""

import ast
from typing import List, Dict, Any
from pydantic import BaseModel, Field


class CodeSmell(BaseModel):
    category: str  # SECURITY, COMPLEXITY, STYLE, PERFORMANCE
    line_number: int
    description: str
    severity: str  # HIGH, MEDIUM, LOW
    recommendation: str


class AuditReport(BaseModel):
    file_name: str
    overall_health_score: int  # 0 to 100
    smells_detected: List[CodeSmell]
    refactored_code: str
    summary: str


class StaticCodeAuditor:
    """Performs deterministic static AST analysis to identify common security risks and smells."""

    @staticmethod
    def audit_python_code(source_code: str, file_name: str = "snippet.py") -> AuditReport:
        smells: List[CodeSmell] = []

        try:
            tree = ast.parse(source_code)
        except SyntaxError as e:
            return AuditReport(
                file_name=file_name,
                overall_health_score=0,
                smells_detected=[
                    CodeSmell(
                        category="SYNTAX_ERROR",
                        line_number=e.lineno or 1,
                        description=f"Syntax Error: {e.msg}",
                        severity="HIGH",
                        recommendation="Fix Python syntax syntax before refactoring."
                    )
                ],
                refactored_code=source_code,
                summary="Code could not be parsed due to syntax error."
            )

        for node in ast.walk(tree):
            # Check for eval() or exec()
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                if node.func.id in ("eval", "exec"):
                    smells.append(
                        CodeSmell(
                            category="SECURITY",
                            line_number=node.lineno,
                            description=f"Dangerous dynamic code execution using `{node.func.id}()`.",
                            severity="HIGH",
                            recommendation="Replace dynamic evaluation with explicit data parsing (e.g. json.loads or ast.literal_eval)."
                        )
                    )
            # Check for bare except:
            if isinstance(node, ast.ExceptHandler):
                if node.type is None:
                    smells.append(
                        CodeSmell(
                            category="RELIABILITY",
                            line_number=node.lineno,
                            description="Bare `except:` catches KeyboardInterrupt and SystemExit.",
                            severity="MEDIUM",
                            recommendation="Catch specific exceptions or `except Exception:`."
                        )
                    )
            # Check for hardcoded secrets
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        name_lower = target.id.lower()
                        if any(k in name_lower for k in ("secret", "token", "password", "api_key")):
                            if isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
                                if len(node.value.value) > 8:
                                    smells.append(
                                        CodeSmell(
                                            category="SECURITY",
                                            line_number=node.lineno,
                                            description=f"Hardcoded credential detected in variable `{target.id}`.",
                                            severity="HIGH",
                                            recommendation="Load secrets via environment variables (os.environ.get)."
                                        )
                                    )

        health_penalty = sum(30 if s.severity == "HIGH" else 15 for s in smells)
        score = max(0, 100 - health_penalty)

        refactored = source_code.replace("eval(", "json.loads(").replace("except:", "except Exception:")

        return AuditReport(
            file_name=file_name,
            overall_health_score=score,
            smells_detected=smells,
            refactored_code=refactored,
            summary=f"Found {len(smells)} issues. Health score: {score}/100."
        )


def demonstrate():
    sample_bad_code = """
import os

API_KEY = "sk_live_9384820194827104820"

def calculate_formula(expression):
    try:
        return eval(expression)
    except:
        return None
    """

    auditor = StaticCodeAuditor()
    report = auditor.audit_python_code(sample_bad_code, "legacy_service.py")

    print("=" * 60)
    print("DAY 8: CODE REFACTORING & SECURITY AUDIT")
    print("=" * 60)
    print(f"File: {report.file_name} | Score: {report.overall_health_score}/100")
    print(f"Summary: {report.summary}\n")
    print("Detected Issues:")
    for smell in report.smells_detected:
        print(f"  [{smell.severity}] Line {smell.line_number} ({smell.category}): {smell.description}")
        print(f"    -> Fix: {smell.recommendation}")


if __name__ == "__main__":
    demonstrate()
