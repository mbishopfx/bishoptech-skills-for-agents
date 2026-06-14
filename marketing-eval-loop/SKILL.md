---
name: marketing-eval-loop
description: Enterprise-ready taste-gated marketing and content creation loop. Evaluates drafts against a strict taste rubric using an LLM judge, and triggers Slack/Telegram approvals before publishing.
---

# 🎨 Marketing Evaluation Loop: Taste-Gated Agent Skill

This skill allows an agent to draft and refine marketing copy, posts, emails, and landing page content. It mitigates generic AI "slop" by scoring drafts against a custom taste rubric (using an LLM-as-a-judge) and securing human-in-the-loop approvals before publishing.

---

## 🔁 Execution Flow

```
           ┌────────────────────────────────┐
           │     1. Load Brand Guidelines   │
           │     & Gold Standard Assets     │
           └───────────────┬────────────────┘
                           │
           ┌───────────────▼────────────────┐
           │        2. Generate Draft       │
           └───────────────┬────────────────┘
                           │
           ┌───────────────▼────────────────┐
           │   3. Adversarial Critique      │
           │   (judge_content.py Score)     │
           └───────────────┬────────────────┘
                           │
                           ├────────────────────────┐
           ┌───────────────▼────────────────┐         │ (score < 0.70)
           │    4. Score >= Threshold?      │         │
           └───────────────┬────────────────┘         │
                           │ (score >= 0.70)          │
           ┌───────────────▼────────────────┐         │
           │     5. Human Approval Gate     │◄────────┘
           │     (Slack/Telegram Pings)     │
           └───────────────┬────────────────┘
                           │ (approved)
           ┌───────────────▼────────────────┐
           │       6. Publish / Queue       │
           └────────────────────────────────┘
```

---

## 🛠️ Step-by-Step Instructions

### Step 1: Load Brand Guidelines & Gold Standard Assets
1. Read `/references/gold_standard/` containing your 20-50 top-performing historical emails, landing page copy, or social posts.
2. Read the custom voice and tone criteria in your rubric.

### Step 2: Generate Draft
Create the marketing piece according to the user brief. Do not use stock transitions, hedging phrases, or em-dash-heavy phrasing.

### Step 3: Adversarial Critique
1. Pass the generated draft into `judge_content.py` alongside your `rubric_template.md`.
2. The judge (using LLM-as-a-judge) returns a score from `0.0` to `1.0` for the following five criteria:
   - **Specificity**: Contains actionable steps or templates.
   - **Proof & Data**: Backs claims with concrete evidence.
   - **Voice Alignment**: Matches the brand voice, avoiding generic AI syntax.
   - **Differentiation**: Stands out from common competitor copy.
   - **Bookmark Value**: The reader would bookmark this to implement later.

### Step 4: Evaluate Score Threshold
- **If the average score is < 0.70**: Feed the judge's criticisms back into the generation prompt. Rewrite the draft and return to Step 3.
- **If the average score is >= 0.70**: Proceed to the Approval Gate.

### Step 5: Human Approval Gate
1. Invoke `slack_notifier.py` with the generated draft, average score, and criteria breakdown.
2. The script posts a Slack message with interactive approval buttons: `[Approve & Publish]` and `[Reject & Rewrite]`.
3. If approved, publish the output. If rejected, add the rejection reason to the agent's memory and restart the draft loop.
