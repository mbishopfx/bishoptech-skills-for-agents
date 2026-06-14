---
name: runtime-guardrail-loop
description: Enterprise-ready pre-ship regression and runtime watchdog. Evaluates new prompts/models against a baseline test suite, samples production outputs on a cron, and ingests failures back into the suite.
---

# 🛡️ Runtime Guardrail Loop: Continuous Monitoring Agent Skill

This skill allows an agent to maintain system quality by running automated regression tests before deployment and sampling live executions in production. It closes the loop by automatically appending user-flagged bad outputs back into the local test suite as regression test cases.

---

## 🔁 Execution Flow

```
                      ┌─────────────────────────────┐
                      │    1. Load Test Suite &     │
                      │    Baseline Metrics JSON    │
                      └──────────────┬──────────────┘
                                     │
                      ┌──────────────▼──────────────┐
                      │ 2. Run Candidate Prompts    │
                      │   Against All Test Inputs   │
                      └──────────────┬──────────────┘
                                     │
                      ┌──────────────▼──────────────┐
                      │   3. Compute Delta Score    │
                      │   (regression_check.py)     │
                      └──────────────┬──────────────┘
                                     │
                                     ├────────────────────────┐
                      ┌──────────────▼──────────────┐         │ (score drops > 0.05)
                      │    4. Score >= Baseline?    │         │
                      └──────────────┬──────────────┘         │
                                     │ (green / stable)       │
                      ┌──────────────▼──────────────┐         │
                      │     5. Approve Deploy &      │◄───────┘
                      │     Sample Production        │
                      └──────────────┬──────────────┘
                                     │ (cron trigger)
                      ┌──────────────▼──────────────┐
                      │    6. Ingest Failures       │
                      │      (closed_loop.py)       │
                      └─────────────────────────────┘
```

---

## 🛠️ Step-by-Step Instructions

### Step 1: Load Test Suite
Parse the test suite JSON file (`/templates/test_suite.json`) containing inputs, historical ground truths, and target baseline scores.

### Step 2: Run Regression Test Suite
1. When a prompt edit or model swap is proposed, pass the new candidate pipeline into `regression_check.py`.
2. The script processes each test case, invokes the candidate prompt, and computes the performance scores.

### Step 3: Compute Score Delta
Calculate the difference between the candidate score and the historical baseline score.
- **If candidate average drops by > 0.05 or falls below 0.70**: Terminate deployment, output the delta scorecard, and return a non-zero exit code.
- **If candidate is equal or better**: Approve code/prompt checkout for merge.

### Step 4: Production Sampling (Watchdog)
1. Run a recurring agent task (cron scheduler) to pull a random 5% sample of production trace logs.
2. Evaluate each sample using the LLM-as-a-Judge script. 
3. Send a summary table of daily production quality scores to the dashboard or Slack.

### Step 5: Closed-Loop Ingest (Reinforcement)
1. When a human reviews production outputs and flags a bad result (e.g., via a thumbs-down webhook), invoke `closed_loop.py`.
2. Provide the input, the bad output, and the human's rejection reason.
3. The script automatically serializes this execution as a new test case in `/templates/test_suite.json` with a baseline score of `1.0` (target to resolve). This ensures the bug is never reintroduced in subsequent deploys.
