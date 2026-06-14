# 🦾 Coding Loop: Autonomous Engineering Agent

> **"Stop prompting your coding agents. Build loops that prompt your agents."**

The standard approach to coding with AI is broken. You write a prompt, copy the code, run it, hit an error, copy-paste the error back to the model, and repeat. You are acting as the compiler, the QA engineer, and the git manager.

`coding-loop` is an enterprise-ready, installable agent skill that automates this entire feedback cycle. It wires your agent directly into your environment using isolated **Git Worktrees**, automated test runners, and an adversarial **Maker-Checker** subagent split.

---

## ⚡ Key Capabilities

- **Isolated Execution (Worktrees)**: Spawns independent working directories for the agent to implement code. No file collisions with your working checkout.
- **Fail-Fast Verification**: Automatically runs your compilers, linters, and test suites. If a test fails, it self-corrects based on terminal output.
- **Adversarial Security Checker**: The agent writing the code is never the agent that approves it. A separate check subagent reviews the diff against your codebase security `RULES.md` before anything is committed.
- **Token Budget Protection**: Explicitly optimized for cost-effective frontier models (like DeepSeek V4) to prevent runaway infinite repair loops.

---

## 📂 Repository Structure

```
coding-loop/
├── SKILL.md                 # Procedural skill rules parsed by agents
├── README.md                # Human-facing instructions (this file)
├── scripts/
│   ├── run_loop.py          # Orchestrates worktrees, tests, and correction loop
│   └── verify_code.py       # Adversarial linter, regex, and compliance checker
└── templates/
    └── RULES.md             # Custom project rule constraints template
```

---

## 🚀 Quick Start & Installation

To install this skill into your local agent environment (such as Hermes or Claude Code):

```bash
# Register the skill with your agent CLI
agents skill install file:///Users/matthewbishop/BishopTech.dev/bishoptech-skills-for-agents/coding-loop
```

### 1. Configure Project Rules
Copy the `templates/RULES.md` to the root of your project:
```bash
cp coding-loop/templates/RULES.md /your/project/root/RULES.md
```
Edit this file to define absolute constraints (e.g., "All React components must use functional exports", "No raw SQL statements allowed").

### 2. Run the Loop
Run the orchestrator script, pointing it to your project root, a description of the task, and the command to run your test suite:
```bash
python3 coding-loop/scripts/run_loop.py \
  --project-path /your/project/root \
  --prompt "Fix the auth timeout token expiration bug" \
  --test-command "npm run test" \
  --max-retries 5
```

---

## ⚙️ How it Works under the Hood

```
[Issue Triage] ──► [Worktree Setup] ──► [Agent Edits Code]
                                                 │
                                                 ▼
[Push branch / PR] ◄── [Adversarial Check] ◄── [Test Runner]
                         (verify_code.py)
```

1. **Isolation**: The script creates a temporary branch and checkout using `git worktree`.
2. **Execution**: The agent performs code modifications based on the issue description.
3. **Validation**: The orchestrator executes the provided `--test-command`. If it returns a non-zero exit code, the logs are fed back into the agent to patch the code.
4. **Checker Gate**: `verify_code.py` performs static analysis and rule checks on the git diff.
5. **Human Gate**: Once verified, the worktree is cleaned up and a Git branch/PR is pushed.

---

## 🧠 Best Practices for Token Efficiency

> [!TIP]
> **Optimizing Costs**
> - **Budget limit**: Always set the `--max-retries` flag. The default is 5.
> - **Keep test suites narrow**: Run specific test files (e.g., `npm run test -- auth.test.js`) rather than your entire integration suite to speed up the loop.
> - **Use cheap models for checking**: Configure the orchestrator to run code generation with a frontier reasoning model, but run the checker script with a fast, high-concurrency model like DeepSeek Flash.
