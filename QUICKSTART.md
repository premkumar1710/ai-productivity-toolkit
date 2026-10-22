# 🚀 Quickstart Guide: AI Productivity Toolkit

Get up and running with the **AI Productivity Toolkit** in under 3 minutes!

---

## 1. Prerequisites
- Python 3.10+ (Tested up to Python 3.13)
- `pip` package manager

---

## 2. Installation

Clone or navigate into the repository directory:
```bash
cd ai-productivity-toolkit
```

Install requirements:
```bash
pip install -r requirements.txt
```

*(Optional)* Configure API keys if you wish to use live cloud LLMs (Gemini, OpenAI, Anthropic). If you do not configure an API key, the toolkit automatically operates with an **intelligent, deterministic offline mock engine**:
```bash
cp .env.example .env
# Edit .env and paste your GEMINI_API_KEY or OPENAI_API_KEY
```

---

## 3. Launching the Web Dashboard (Streamlit)

Launch the modern browser UI:
```bash
streamlit run day_10_productivity_toolkit/app.py
```
This opens the multi-tab productivity dashboard at `http://localhost:8501`.

---

## 4. Launching the Interactive Terminal CLI (Rich)

Run the interactive terminal interface:
```bash
python day_10_productivity_toolkit/cli.py
```

Or execute an automated demonstration run across all 4 workflows in one command:
```bash
python day_10_productivity_toolkit/cli.py --demo
```

---

## 5. Running the Day-by-Day Learning Modules

Explore and run the daily curriculum scripts directly:

### Day 6: Prompt Foundations
```bash
python day_06_prompt_foundations/zero_vs_few_shot.py
python day_06_prompt_foundations/role_and_constraints.py
python day_06_prompt_foundations/exercises.py
```

### Day 7: Structured Outputs & Core NLP Tasks
```bash
python day_07_structured_outputs/json_extractor.py
python day_07_structured_outputs/summarization_engine.py
python day_07_structured_outputs/classification_suite.py
python day_07_structured_outputs/generation_lab.py
```

### Day 8: AI Coding & Debugging
```bash
python day_08_ai_coding_debugging/spec_to_code.py
python day_08_ai_coding_debugging/automated_debugger.py
python day_08_ai_coding_debugging/code_refactoring_audit.py
```

### Day 9: Prompt Evaluation & Benchmarking
```bash
python day_09_eval_and_benchmarking/prompt_template_engine.py
python day_09_eval_and_benchmarking/prompt_evaluator.py
```

---

## 6. Running the Automated Test Suite

Run pytest to verify all days and toolkit workflows:
```bash
pytest -v tests/
```
