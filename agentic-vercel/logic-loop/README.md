# 🧠 Logic Loop: Cost-Optimized Gateway Routing & Fallbacks

> **"Querying frontier reasoning models for simple tasks is a waste of money. Route dynamically."**

Frontier LLM queries are expensive. Running all agent steps on your highest-tier model drains budgets quickly. However, relying solely on cheap models increases the risk of hallucinated parameters, schema formatting errors, or reasoning breakdowns.

`logic-loop` is an installable agent skill that gives your agent a **Thinking/Logic Sense**. It routes tasks through the **Vercel AI Gateway** using a multi-tiered architecture. It queries a fast, cost-effective model first, validates the structure, and automatically escalates to a high-capacity model (or a human review queue) if quality falls below the threshold.

---

## ⚡ Key Capabilities

- **Multi-Tiered Routing**: Queries Tier 1 (fast/cheap) first, falling back to Tier 2 (high reasoning) only if needed.
- **Failover Proxying**: Automatically switches providers (e.g. from Anthropic to OpenAI) via the Vercel AI Gateway if outages or rate limits are hit.
- **Human Escalation Gate**: Halts deployment and pings Slack for human intervention if both model tiers fail verification checks.

---

## 📂 Folder Structure

```
logic-loop/
├── SKILL.md                 # Agent execution guide
├── README.md                # Human user manual (this file)
└── scripts/
    └── gateway_fallback.py  # Tiered router and fallback manager
```

---

## 🚀 Quick Start & Installation

```bash
# Register the skill with your agent CLI
agents skill install file:///Users/matthewbishop/BishopTech.dev/bishoptech-skills-for-agents/agentic-vercel/logic-loop
```

### 1. Export Gateway URLs
```bash
export VERCEL_AI_GATEWAY_URL="https://gateway.ai.vercel.com/v1/projects/YOUR_PROJECT_SLUG/gateways/YOUR_GATEWAY_ID"
export VERCEL_AI_GATEWAY_TOKEN="your-vercel-ai-gateway-api-key"
```

### 2. Run Logic Router
```bash
python3 agentic-vercel/logic-loop/scripts/gateway_fallback.py \
  --prompt "Generate a user login schema JSON" \
  --tier1 "deepseek-flash" \
  --tier2 "gpt-4o"
```
*The script queries Tier 1, validates the JSON output, and escalates to Tier 2 if the JSON structure is invalid.*
