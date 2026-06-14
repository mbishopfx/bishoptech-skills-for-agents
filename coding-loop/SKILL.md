---
name: coding-loop
description: Enterprise-ready autonomous coding agent loop. Integrates isolated git worktrees, incremental build/test execution, and adversarial subagent checks to deliver verified code changes with zero human intervention.
---

# 🦾 Coding Loop: Autonomous Engineering Agent Skill

This skill allows an agent to run an autonomous execution loop for resolving software tickets, bugs, or feature additions. It implements a strict **Maker-Checker** pattern, running the target code changes in an isolated Git worktree and validating against linters, tests, and compliance checkers before proposing a pull request.

---

## 🔁 Execution Flow

When triggered, you must move through the following 6-step loop until the stopping condition is satisfied or the retry limit (default: 5) is reached.

```
                  ┌─────────────────────────────┐
                  │   1. Read Project Context   │
                  │   (VISION.md / ARCH.md)     │
                  └──────────────┬──────────────┘
                                 │
                  ┌──────────────▼──────────────┐
                  │ 2. Create Git Worktree &   │
                  │   Plan Implementation       │
                  └──────────────┬──────────────┘
                                 │
                  ┌──────────────▼──────────────┐
                  │    3. Execute Code Edits    │
                  └──────────────┬──────────────┘
                                 │
                                 ├────────────────────────┐
                  ┌──────────────▼──────────────┐         │ (tests fail)
                  │    4. Run Tests & Linters   │         │
                  └──────────────┬──────────────┘         │
                                 │ (tests pass)           │
                  ┌──────────────▼──────────────┐         │
                  │   5. Adversarial Verification│◄───────┘
                  │   (Subagent Review Rules)   │
                  └──────────────┬──────────────┘
                                 │ (verifier approves)
                  ┌──────────────▼──────────────┐
                  │  6. Propose PR & Walkthrough│
                  └─────────────────────────────┘
```

---

## 🛠️ Step-by-Step Instructions

### Step 1: Read Project Context
Locate and parse the following project-level markdown context files if they exist in the root of the repository:
- `VISION.md`: The overarching product goals and core rules.
- `ARCHITECTURE.md`: Technical stack details, directory structure, and design conventions.
- `RULES.md` (or `coding-loop/templates/RULES.md`): Hard restrictions (e.g., "no raw SQL", "no external auth libraries", "use specific error boundary patterns").

### Step 2: Create Git Worktree & Plan
1. Do not make edits directly in your master checkout. Spin up a new Git worktree on an isolated branch to isolate your dependencies and working files:
   ```bash
   git worktree add -b feature/agent-loop ../worktrees/agent-loop main
   ```
2. Write a clear, step-by-step implementation plan detailing the files you will modify and the tests you will run.

### Step 3: Execute Code Edits
Perform code modifications inside the worktree directory. Use precise, targeted diff tools.

### Step 4: Run Tests & Linters
1. Run linting checks and the test suite:
   ```bash
   npm run lint && npm run test
   # Or the equivalent for Python, Go, Rust, etc.
   ```
2. **If failures occur**: Extract the error logs, formulate a debugging plan, apply fixes, and re-run Step 4. Do not proceed to Step 5 until all tests and linters are green.

### Step 5: Adversarial Verification (Subagent Check)
1. Split the "Maker" (yourself) from the "Checker" (a subagent or separate prompt context).
2. Instantiate a checker subagent with the `verify_code.py` parameters. Feed it the Git diff of your worktree and the test logs.
3. The checker must check the diff against `RULES.md` and verify it contains no hidden security flaws, styling violations, or structural slop.
4. **If the checker rejects**: Return to Step 3 with the checker's feedback.

### Step 6: Propose PR & Walkthrough
1. Once tests pass and the checker approves, push the branch and open a PR.
2. Generate a structured `walkthrough.md` detailing the changes made, the files touched, and the test results.

---

## 🚫 Guardrails & Token Optimization
- **Max Iterations**: Stop and alert the human if the loop exceeds 5 iterations without clearing the test suite. Do not burn tokens infinitely.
- **Fail Fast**: If a basic typecheck or syntax compilation fails, do not write more code. Halt and address the syntax error first.
