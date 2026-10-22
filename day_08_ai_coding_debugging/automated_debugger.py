"""
Day 8: Automated Stack Trace Debugger & Patch Generator
Parses Python runtime tracebacks, isolates failure locations, and synthesizes root-cause patches.
"""

import re
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field


class DebugReport(BaseModel):
    exception_type: str
    error_message: str
    failed_line_number: Optional[int]
    root_cause_analysis: str
    suggested_fix: str
    diff_patch: str
    regression_test_code: str


class AutomatedDebugger:
    """Parses stack traces and constructs targeted remediation prompts."""

    @staticmethod
    def parse_traceback(traceback_text: str) -> Dict[str, Any]:
        """Extracts exception type, message, and the last offending line number."""
        lines = [line.strip() for line in traceback_text.strip().split("\n") if line.strip()]
        last_line = lines[-1] if lines else "Exception: Unknown error"
        
        # Match "ZeroDivisionError: division by zero" or "KeyError: 'user_id'"
        exc_match = re.match(r"^([\w\.]+Error|Exception):\s*(.*)$", last_line)
        exc_type = exc_match.group(1) if exc_match else "Exception"
        exc_msg = exc_match.group(2) if exc_match else last_line

        # Match line number in "File "app.py", line 42, in process"
        line_num = None
        for line in reversed(lines):
            line_match = re.search(r'line\s+(\d+)', line)
            if line_match:
                line_num = int(line_match.group(1))
                break

        return {
            "exception_type": exc_type,
            "error_message": exc_msg,
            "line_number": line_num
        }

    @classmethod
    def build_debug_prompt(cls, traceback_text: str, source_code: str) -> str:
        parsed = cls.parse_traceback(traceback_text)
        return f"""
You are an expert Python Debugging Engineer.
A runtime error occurred in production. Analyze the traceback and source code to produce a fix.

<traceback>
{traceback_text}
</traceback>

<source_code>
{source_code}
</source_code>

Diagnostics:
- Detected Exception: {parsed['exception_type']}
- Detected Message: {parsed['error_message']}
- Suspect Line Number: {parsed['line_number']}

Instructions:
1. Explain the exact Root Cause of the failure.
2. Provide a unified diff patch showing the fix.
3. Write a pytest regression test that reproduces the bug on unpatched code and passes on patched code.
"""

    @classmethod
    def mock_diagnose(cls, traceback_text: str, source_code: str) -> DebugReport:
        parsed = cls.parse_traceback(traceback_text)
        return DebugReport(
            exception_type=parsed["exception_type"],
            error_message=parsed["error_message"],
            failed_line_number=parsed["line_number"],
            root_cause_analysis="Attempted to access dictionary key 'total_amount' without verifying its existence or handling missing keys in optional webhook payloads.",
            suggested_fix="Use payload.get('total_amount', 0.0) with defensive default fallback.",
            diff_patch="""--- old_webhook.py
+++ new_webhook.py
@@ -14,2 +14,2 @@
-    amount = payload['total_amount']
+    amount = payload.get('total_amount', 0.0)
""",
            regression_test_code="""def test_webhook_handles_missing_total_amount():
    payload = {"transaction_id": "tx_998"}
    assert process_webhook(payload) == 0.0
"""
        )


def demonstrate():
    sample_trace = """
Traceback (most recent call last):
  File "payment_handler.py", line 18, in handle_webhook
    amount = payload['total_amount']
KeyError: 'total_amount'
    """
    sample_code = """
def handle_webhook(payload: dict) -> float:
    # Process incoming payment webhook
    tx_id = payload.get("tx_id", "anonymous")
    amount = payload['total_amount']
    return float(amount)
    """

    debugger = AutomatedDebugger()
    parsed = debugger.parse_traceback(sample_trace)
    print("=" * 60)
    print("DAY 8: AUTOMATED STACK TRACE PARSER")
    print("=" * 60)
    print(f"Parsed Exception : {parsed['exception_type']}")
    print(f"Error Message    : {parsed['error_message']}")
    print(f"Failed Line      : {parsed['line_number']}")

    report = debugger.mock_diagnose(sample_trace, sample_code)
    print("\n" + "=" * 60)
    print("ROOT CAUSE DIAGNOSIS & PATCH")
    print("=" * 60)
    print(f"Root Cause: {report.root_cause_analysis}\n")
    print(f"Unified Diff Patch:\n{report.diff_patch}")
    print(f"Regression Test:\n{report.regression_test_code}")


if __name__ == "__main__":
    demonstrate()
