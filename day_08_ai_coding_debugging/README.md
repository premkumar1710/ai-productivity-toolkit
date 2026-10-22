# Day 8: AI-Assisted Coding, Debugging & Refactoring

Welcome to **Day 8**! In software engineering, Large Language Models excel when paired with systematic engineering practices: **Spec-Driven Generation**, **Root-Cause Traceback Debugging**, and **Automated Code Reviews**.

---

## 1. Spec-Driven Code Generation
Rather than prompting an AI with vague queries like `"Write a function to process payments"`, production-grade AI coding requires a formal **Specification Prompt**:

```text
Write a Python 3.13 function `process_transaction`:
1. Signature: def process_transaction(user_id: str, amount_cents: int, currency: str = "USD") -> TransactionReceipt:
2. Preconditions:
   - amount_cents must be positive (> 0).
   - currency must be in ["USD", "EUR", "GBP"].
3. Error Handling:
   - Raise ValueError on invalid currency or non-positive amount.
   - Raise InsufficientFundsError on overdraft.
4. Output: Complete code with full type annotations, Google-style docstrings, and two pytest test cases.
```

---

## 2. Automated Stack Trace Debugging

When an exception occurs in production, an AI debugging pipeline should ingest:
1. The **Full Stack Trace** (including file path, line number, exception type).
2. The **Enclosing Code Snippet** (context of 20-30 lines).
3. The **Runtime Variable State** (if captured in logs).

### Prompt Template for Debugging:
```text
You are a Staff Software Engineer debugging a runtime error.
Analyze the following traceback and source code snippet.

Identify:
1. Root Cause: Exact reason for failure.
2. Fix: Drop-in replacement code.
3. Regression Test: A minimal pytest test case that reproduces the failure and verifies the fix.
```

---

## 3. Code Refactoring & Security Auditing
AI models can perform multi-dimensional code quality reviews:
- **Style & PEP 8:** Variable naming, redundant comprehension, formatting.
- **Complexity:** Flattening nested if/else pyramids into guard clauses.
- **Security:** Auditing for SQL injection, unsafe deserialization (`pickle`), path traversal, and hardcoded secrets.

---

## 4. Code Modules in this Directory

| File | Purpose |
|---|---|
| `spec_to_code.py` | Converts functional natural language specifications into typed, production-ready Python modules |
| `automated_debugger.py` | Automated stack trace diagnosis, unified diff patcher, and regression test generator |
| `code_refactoring_audit.py` | Code audit engine checking for anti-patterns, security vulnerabilities, and cyclomatic complexity |
