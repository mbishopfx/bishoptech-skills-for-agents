# 🦾 BishopTech Agent Skills: Loop Engineering Registry

Welcome to the **BishopTech Agent Loop Skills** workspace. This repository houses three enterprise-ready, installable agent skills designed for **Hermes, Codex, Antigravity, and Claude Code**.

By moving from manual prompting to structured **Loop Engineering**, these skills replace human checking with automated, multi-agent feedback systems.

---

## ⚡ The Agent Loop Stack

This registry contains the following three installable skills. Each directory is a standalone Git repository containing its own `SKILL.md` (for agent discovery) and a production-ready `README.md` (for human configuration).

| Skill Directory | Purpose | Core Feedback Signal | Stop Condition |
| :--- | :--- | :--- | :--- |
| [📂 `coding-loop`](./coding-loop/) | Autonomous developer agent loop | Test suite execution & Adversarial linter/security review | All tests/lints green & Checker approves |
| [📂 `marketing-eval-loop`](./marketing-eval-loop/) | Taste-gated content/copy creation | LLM-as-a-Judge objective rubric scoring | Rubric score $\ge 0.70$ & Human Slack/Telegram approval |
| [📂 `runtime-guardrail-loop`](./runtime-guardrail-loop/) | Pre-ship regression + production watchdog | Test suite delta tracking & production sampling | Stable production metrics & Closed-loop failure ingestion |
| [📂 `vapi-outbound-loop`](./vapi-outbound-loop/) | Autonomous outbound lead calling loop | Call status polling & LLM transcript scorecard | Completion of lead list & Human scorecard check |
| [📂 `vapi-inbound-trainer-loop`](./vapi-inbound-trainer-loop/) | Inbound agent buyer psychology trainer | Call log verification & transcript-based prompt tuning | Character-stable behavior & Challenging feedback |
| [📂 `vercel-deploy-nurture`](./vercel-deploy-nurture/) | Vercel build, deploy, health check & nurture loop | Build status, error log parse & post-deploy URL checks | Verified endpoint status & completed disk cleanup |

---

## 🚀 Installation & Git Publishing

To make these skills globally available for your agents or public distribution:

### 1. Locally Linking a Skill
To point your agent (e.g., Hermes or Claude Code) to one of these skills:
```bash
# Add the skill directory to your agent's config or search path
# Example: Adding the coding-loop
agents skill install file:///Users/matthewbishop/BishopTech.dev/bishoptech-skills-for-agents/coding-loop
```

### 2. Publishing to GitHub
We have provided a utility script [`publish_repos.sh`](./publish_repos.sh) at the root of this workspace. It automates:
- Setting the git author to `mbishopfx` (`mattbishopfx@gmail.com`).
- Creating remote repositories on GitHub.
- Pushing local commits.
- Inviting `matt@bishoptech.dev` as a repository collaborator.

To publish all skills at once, run:
```bash
chmod +x publish_repos.sh
./publish_repos.sh
```

---

## 🧠 Why Loop Engineering?

Traditional prompting focuses on the **input** (prompts, context, instructions). Loop Engineering focuses on the **output** (gates, checks, metrics, and iteration). 

### The 5 Stages of Every Loop
1. **Discover**: Triage issues, logs, or briefs.
2. **Plan**: Formulate the implementation design.
3. **Execute**: Isolated execution (using Git Worktrees to prevent collisions).
4. **Verify**: Objective tests, validations, and adversarial checker feedback.
5. **Iterate**: Feed errors and critique back to the execution brain, repeating until verification succeeds.

> *"One reliable loop is worth a thousand perfect prompts."*
