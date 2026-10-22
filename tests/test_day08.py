"""
Tests for Day 8: AI-Assisted Coding, Debugging & Refactoring
"""

import pytest
from day_08_ai_coding_debugging.spec_to_code import CodeSpec, SpecToCodeGenerator
from day_08_ai_coding_debugging.automated_debugger import AutomatedDebugger, DebugReport
from day_08_ai_coding_debugging.code_refactoring_audit import StaticCodeAuditor, AuditReport


def test_spec_to_code():
    spec = CodeSpec(
        function_name="sanitize_username",
        description="Sanitizes user handles for URL safety",
        inputs=[{"name": "raw_handle", "type": "str"}],
        output_type="str",
        constraints=["Only alphanumeric and underscores allowed"],
        exceptions_raised=[{"type": "ValueError", "condition": "Empty string"}],
        examples=[{"input": "raw_handle='@John_Doe'", "output": "'john_doe'"}]
    )

    gen = SpecToCodeGenerator()
    prompt = gen.build_prompt(spec)
    assert "sanitize_username" in prompt
    assert "ValueError" in prompt

    code = gen.mock_generate_code(spec)
    assert "sanitize_username" in code
    assert "rate_limit" in code or "sanitize" in code


def test_automated_debugger():
    traceback = """
Traceback (most recent call last):
  File "main.py", line 45, in get_item
    item = cache[item_id]
KeyError: 'item_id'
    """
    debugger = AutomatedDebugger()
    parsed = debugger.parse_traceback(traceback)
    assert parsed["exception_type"] == "KeyError"
    assert parsed["line_number"] == 45

    report = debugger.mock_diagnose(traceback, "cache[item_id]")
    assert isinstance(report, DebugReport)
    assert report.exception_type == "KeyError"
    assert "diff" in report.diff_patch or "---" in report.diff_patch


def test_static_code_auditor():
    bad_code = """
import os

TOKEN = "secret_token_123456789"

def run_script(payload):
    try:
        eval(payload)
    except:
        pass
    """
    auditor = StaticCodeAuditor()
    report = auditor.audit_python_code(bad_code, "test_script.py")

    assert isinstance(report, AuditReport)
    categories = [s.category for s in report.smells_detected]
    assert "SECURITY" in categories  # eval and hardcoded token
    assert "RELIABILITY" in categories  # bare except
    assert report.overall_health_score < 70
