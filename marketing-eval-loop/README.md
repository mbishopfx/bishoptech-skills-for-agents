# 🎨 Marketing Evaluation Loop: Taste-Gated Content Creator

> **"Marketing slop is not an input problem. It's an output-side quality control problem."**

Most AI-generated marketing copy sounds identical: generic transitions, repetitive lists of three, and vague promises. Swapping models or writing longer prompts won't solve this. If your system has no quality gate, it is playing a coin flip with your brand reputation.

`marketing-eval-loop` is an installable agent skill that ensures every email, landing page, and social post clears a high taste and specificity bar. It grades drafts against an objective scoring rubric using an independent **LLM-as-a-Judge** and integrates with Slack or Telegram to provide 1-click human approval.

---

## ⚡ Key Capabilities

- **Taste-Gating**: Validates content using objective criteria like **Bookmark Value**, **Differentiation**, and **Proof**.
- **LLM-as-a-Judge**: Evaluates drafts using a secondary LLM with no ego and strict scoring parameters.
- **Interactive Human Gate**: Automatically posts drafts, scores, and critiques directly into Slack/Telegram with quick-action approval buttons.
- **AI Word Cleansing**: Standardized rules to strip out typical AI tells (e.g. "delve", "testament", "tapestry").

---

## 📂 Repository Structure

```
marketing-eval-loop/
├── SKILL.md                 # Procedural skill rules parsed by agents
├── README.md                # Human-facing instructions (this file)
├── scripts/
│   ├── judge_content.py     # LLM judge runner that computes rubric scores
│   └── slack_notifier.py    # Slack/Telegram webhook notifier and approval poster
└── templates/
    └── rubric_template.md   # Objective criteria checklist template
```

---

## 🚀 Quick Start & Installation

```bash
# Register the skill with your agent CLI
agents skill install file:///Users/matthewbishop/BishopTech.dev/bishoptech-skills-for-agents/marketing-eval-loop
```

### 1. Set Up Your Gold Standard
Save 10 to 20 of your top-performing pieces of copy in a folder `/references/gold_standard/`. The agent will reference these to learn your brand voice.

### 2. Configure Your Slack Webhook
Export your Slack Webhook URL to your environment variables:
```bash
export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/YOUR_SLACK_WEBHOOK_URL"
```

### 3. Generate and Evaluate Content
Execute the evaluation loop. This script takes the copy to be judged, runs the LLM rubric check, and posts the results:
```bash
python3 marketing-eval-loop/scripts/judge_content.py \
  --draft-path "./draft_email.txt" \
  --rubric-path "marketing-eval-loop/templates/rubric_template.md" \
  --api-key "$GEMINI_API_KEY"
```

---

## 🏆 The Five Rubric Pillars

We score every candidate piece of content against the following five metrics, looking for a target score of **$\ge 0.70$** across the board:

1. **Specificity (Weight: 25%)**: Does this explain *how* to do something, or is it just a high-level vibe? Must contain actionable playbooks or templates.
2. **Proof & Evidence (Weight: 20%)**: Are the claims supported by statistics, studies, quotes, or screenshots?
3. **Voice & Style (Weight: 20%)**: Does it sound human, or is it littered with AI stock phrases ("in summary", "delve", "unlocking")?
4. **Differentiation (Weight: 20%)**: Does this offer a unique angle, or could this be published by any competitor?
5. **Bookmark Value (Weight: 15%)**: Would a reader bookmark this and return to implement it later?
