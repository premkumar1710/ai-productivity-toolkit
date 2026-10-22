"""
Day 9: Prompt Evaluation Harness & Benchmark Suite
Runs test datasets through candidate prompts, calculates rubric metrics, and exports reports.
"""

import sys
from pathlib import Path

# Ensure project root is in sys.path
root_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

# Safe UTF-8 encoding configuration for Windows terminals
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

import time
from dataclasses import dataclass
from typing import List, Dict, Any, Callable
from day_06_prompt_foundations.role_and_constraints import ConstraintValidator
from day_07_structured_outputs.json_extractor import JSONExtractor


@dataclass
class EvalTestCase:
    __test__ = False
    id: str
    input_text: str
    expected_category: str
    forbidden_words: List[str]
    max_words: int

TestCase = EvalTestCase


@dataclass
class EvalResult:
    test_id: str
    prompt_version: str
    output: str
    accuracy_passed: bool
    constraints_passed: bool
    schema_passed: bool
    latency_ms: float
    total_score: float  # 0 to 100


class PromptEvaluator:
    """Evaluates prompt variants against a test dataset and outputs benchmark metrics."""

    def __init__(self, test_cases: List[EvalTestCase]):
        self.test_cases = test_cases

    def evaluate_prompt_variant(
        self,
        version_label: str,
        runner_fn: Callable[[str], str]
    ) -> List[EvalResult]:
        results = []

        for tc in self.test_cases:
            start_t = time.perf_counter()
            output = runner_fn(tc.input_text)
            latency = (time.perf_counter() - start_t) * 1000.0

            # 1. Accuracy Check (does output contain expected category?)
            accuracy_passed = tc.expected_category.lower() in output.lower()

            # 2. Constraint Check (apologies, forbidden words, word limit)
            no_apology, _ = ConstraintValidator.check_no_apologies(output)
            no_forbidden, _ = ConstraintValidator.check_forbidden_terms(output, tc.forbidden_words)
            within_limit, _ = ConstraintValidator.check_word_limit(output, tc.max_words)
            constraints_passed = no_apology and no_forbidden and within_limit

            # 3. Schema Check (attempt JSON parsing if structured)
            schema_passed = True
            try:
                JSONExtractor.extract_json(output)
            except Exception:
                schema_passed = False

            score = 0.0
            if accuracy_passed:
                score += 40.0
            if constraints_passed:
                score += 30.0
            if schema_passed:
                score += 30.0

            results.append(
                EvalResult(
                    test_id=tc.id,
                    prompt_version=version_label,
                    output=output,
                    accuracy_passed=accuracy_passed,
                    constraints_passed=constraints_passed,
                    schema_passed=schema_passed,
                    latency_ms=round(latency, 2),
                    total_score=score
                )
            )

        return results

    @staticmethod
    def generate_markdown_report(results_v1: List[EvalResult], results_v2: List[EvalResult]) -> str:
        avg_score_v1 = sum(r.total_score for r in results_v1) / len(results_v1) if results_v1 else 0
        avg_score_v2 = sum(r.total_score for r in results_v2) / len(results_v2) if results_v2 else 0

        acc_v1 = sum(1 for r in results_v1 if r.accuracy_passed) / len(results_v1) * 100
        acc_v2 = sum(1 for r in results_v2 if r.accuracy_passed) / len(results_v2) * 100

        schema_v1 = sum(1 for r in results_v1 if r.schema_passed) / len(results_v1) * 100
        schema_v2 = sum(1 for r in results_v2 if r.schema_passed) / len(results_v2) * 100

        lines = [
            "# Prompt Engineering Benchmark Report",
            "\n## 1. Executive Summary",
            f"This benchmark compares **Prompt v1 (Baseline Zero-Shot)** against **Prompt v2 (Optimized Few-Shot + Schema Constraints)** across {len(results_v1)} standardized test scenarios.\n",
            "| Metric | Prompt v1 (Baseline) | Prompt v2 (Optimized) | Delta |",
            "|---|---|---|---|",
            f"| **Overall Quality Score** | {avg_score_v1:.1f}/100 | {avg_score_v2:.1f}/100 | +{avg_score_v2 - avg_score_v1:.1f} pts |",
            f"| **Ground-Truth Accuracy** | {acc_v1:.1f}% | {acc_v2:.1f}% | +{acc_v2 - acc_v1:.1f}% |",
            f"| **JSON Schema Compliance** | {schema_v1:.1f}% | {schema_v2:.1f}% | +{schema_v2 - schema_v1:.1f}% |",
            "\n## 2. Granular Test Case Results\n",
            "| Test ID | v1 Score | v1 Schema | v2 Score | v2 Schema | Accuracy Outcome |",
            "|---|---|---|---|---|---|"
        ]

        for r1, r2 in zip(results_v1, results_v2):
            lines.append(
                f"| `{r1.test_id}` | {r1.total_score:.0f} | {'YES' if r1.schema_passed else 'NO'} | "
                f"{r2.total_score:.0f} | {'YES' if r2.schema_passed else 'NO'} | "
                f"{'PASS' if r2.accuracy_passed else 'FAIL'} |"
            )

        lines.extend([
            "\n## 3. Key Findings & Recommendations",
            "- **Zero-shot prompts frequently omit strict JSON keys** and produce conversational preamble text.",
            "- **Few-shot exemplars with negative constraints** achieved 100% schema conformance and eliminated conversational fillers.",
            "- **Recommendation:** Deploy Prompt v2 for all automated downstream API endpoints."
        ])

        return "\n".join(lines)


def demonstrate():
    cases = [
        EvalTestCase(
            id="TC-01",
            input_text="My payment card was charged $99 instead of $49 promo rate.",
            expected_category="BILLING",
            forbidden_words=["sorry", "apologize"],
            max_words=60
        ),
        EvalTestCase(
            id="TC-02",
            input_text="The API latency spiked from 50ms to 4000ms after yesterday's deploy.",
            expected_category="PERFORMANCE",
            forbidden_words=["sorry", "apologize"],
            max_words=60
        ),
        EvalTestCase(
            id="TC-03",
            input_text="Unauthorized logins detected from unknown IP 192.168.1.100.",
            expected_category="SECURITY",
            forbidden_words=["sorry", "apologize"],
            max_words=60
        )
    ]

    # Baseline runner (v1: Free-form text without schema)
    def runner_v1(text: str) -> str:
        if "charged" in text:
            return "I apologize for the trouble. This looks like a billing issue."
        if "latency" in text:
            return "This seems to be a performance problem with the API."
        return "Security incident observed."

    # Optimized runner (v2: Structured JSON with negative constraints)
    def runner_v2(text: str) -> str:
        if "charged" in text:
            return '{"category": "BILLING", "urgency": "P2_MEDIUM", "confidence": 0.95}'
        if "latency" in text:
            return '{"category": "PERFORMANCE", "urgency": "P1_HIGH", "confidence": 0.92}'
        return '{"category": "SECURITY", "urgency": "P0_CRITICAL", "confidence": 0.99}'

    evaluator = PromptEvaluator(cases)
    results_v1 = evaluator.evaluate_prompt_variant("v1_baseline", runner_v1)
    results_v2 = evaluator.evaluate_prompt_variant("v2_optimized", runner_v2)

    report_md = evaluator.generate_markdown_report(results_v1, results_v2)
    print("=" * 60)
    print("DAY 9: PROMPT BENCHMARK REPORT GENERATOR")
    print("=" * 60)
    print(report_md)


if __name__ == "__main__":
    demonstrate()
