# 👀 Vision Loop: Visual QA & Design Regression Checker

> **"Code compiling is only half the battle. Your layout needs to match the spec."**

Automated tests check database queries and API endpoints, but they can't tell you if your main CTA button is hidden behind a modal overlay or if text is overlapping on mobile displays.

`vision-loop` is an installable agent skill that gives your agent a **Vision Sense**. It captures page screenshots, routes them through your **Vercel AI Gateway** to a multimodal foundation model, compares the output to your design mockup, and provides a structured JSON bug report. If visual issues are found, the agent uses the layout coordinates to self-correct the CSS code.

---

## ⚡ Key Capabilities

- **Multimodal Visual QA**: Compares screenshots against design mockups or mobile specs.
- **Vercel AI Gateway Proxying**: Routes payload through Vercel's unified gateway, using caching to avoid duplicate token costs on unchanged layouts.
- **Coordinate Bug Mapping**: Pinpoints the exact overlay locations where text collisions or spacing bugs occur.
- **Self-Correcting CSS Loops**: Re-runs the visual check loop until visual discrepancy scores are below the tolerance threshold.

---

## 📂 Folder Structure

```
vision-loop/
├── SKILL.md                 # Agent execution guide
├── README.md                # Human user manual (this file)
└── scripts/
    └── verify_ui.py         # Multi-modal comparison orchestrator
```

---

## 🚀 Quick Start & Installation

```bash
# Register the skill with your agent CLI
agents skill install file:///Users/matthewbishop/BishopTech.dev/bishoptech-skills-for-agents/agentic-vercel/vision-loop
```

### 1. Export Gateway URLs
```bash
export VERCEL_AI_GATEWAY_URL="https://gateway.ai.vercel.com/v1/projects/YOUR_PROJECT_SLUG/gateways/YOUR_GATEWAY_ID"
export VERCEL_AI_GATEWAY_TOKEN="your-vercel-ai-gateway-api-key"
```

### 2. Run Visual Check
Pass the candidate screenshot and target spec to the verification script:
```bash
python3 agentic-vercel/vision-loop/scripts/verify_ui.py \
  --current-ui "./current_dev_page.png" \
  --target-mockup "./figma_design_spec.png"
```
*The script outputs a layout compliance score and blocks execution if visual anomalies are detected.*
