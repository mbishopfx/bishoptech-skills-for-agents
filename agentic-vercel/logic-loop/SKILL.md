---
name: logic-loop
description: Enterprise cost-optimized model routing and provider fallback loop. Integrates Vercel AI Gateway retries, failovers, and human escalation gates.
---

# 🧠 Logic Loop: Cognitive Routing & Fallbacks Agent Skill

This skill allows an agent to run an autonomous reasoning and fallback loop. It cost-optimizes LLM execution by routing user queries through the Vercel AI Gateway to a cheap model first, running verification checks, and failing over to high-capacity reasoning models or a human review queue if quality falls below threshold.

---

## 🔁 Execution Flow

```
                      ┌─────────────────────────────┐
                      │    1. Input Query/Task      │
                      └──────────────┬──────────────┘
                                     │
                      ┌──────────────▼──────────────┐
                      │    2. Call Tier 1 Model     │
                      │    (Fast / Cost-Effective)  │
                      └──────────────┬──────────────┘
                                     │
                      ┌──────────────▼──────────────┐
                      │ 3. Run Quality Verification │
                      └──────────────┬──────────────┘
                                     │
                                     ├────────────────────────┐
                      ┌──────────────▼──────────────┐         │ (score < 0.70)
                      │    4. Verification Pass?    │         │
                      └──────────────┬──────────────┘         │
                                     │ (green / clean)        │
                      ┌──────────────▼──────────────┐         │
                      │ 5. Return Success Output    │◄────────┘ (Tier 2 Call /
                      └─────────────────────────────┘            Human Escalate)
```

---

## 🛠️ Step-by-Step Instructions

### Step 1: Query Execution
1. Send the prompt to your Tier 1 model (e.g. DeepSeek Flash or GPT-4o-Mini) routed via Vercel AI Gateway:
   ```bash
   python3 agentic-vercel/logic-loop/scripts/gateway_fallback.py \
     --prompt "Summarize our sales database report" \
     --tier1 "deepseek/flash" \
     --tier2 "openai/gpt-4o"
   ```
2. The script configures Vercel AI Gateway's caching and automatic retry policies.

### Step 2: Quality Verification Check
1. Evaluate the Tier 1 response using local checks (valid JSON structure, schema limits, or regex patterns).
2. **If verification fails (score < 0.70)**: Route the same query to the Tier 2 model (high-capacity frontier model like GPT-4o or Claude 3.5 Sonnet) via Vercel AI Gateway's failover proxy.
3. **If Tier 2 verification still fails**: Trigger the human review gate (send a Slack notification requesting human input) to avoid shipping bad output to production.
4. **If verification passes**: Return the result.
