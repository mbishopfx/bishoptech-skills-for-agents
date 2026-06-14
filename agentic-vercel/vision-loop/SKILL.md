---
name: vision-loop
description: Multimodal UI and design layout verification loop. Compares visual screenshots to baseline target designs via Vercel AI Gateway and reports design discrepancies.
---

# 👀 Vision Loop: Visual QA Agent Skill

This skill allows an agent to run an autonomous visual verification loop. It takes a screenshot (or accepts an image path of the generated layout), routes it through the Vercel AI Gateway to a multimodal model, compares it against a target design, and loops to fix the layout code if design drift or layout overlap is detected.

---

## 🔁 Execution Flow

```
                      ┌─────────────────────────────┐
                      │    1. Capture Screenshot    │
                      │    or Read Image Path       │
                      └──────────────┬──────────────┘
                                     │
                      ┌──────────────▼──────────────┐
                      │ 2. Submit to Multimodal LLM │
                      │   (via Vercel AI Gateway)   │
                      └──────────────┬──────────────┘
                                     │
                      ┌──────────────▼──────────────┐
                      │  3. Compare Layout against  │
                      │       Baseline Mock         │
                      └──────────────┬──────────────┘
                                     │
                                     ├────────────────────────┐
                      ┌──────────────▼──────────────┐         │ (drifts/bugs found)
                      │    4. Design Drift Found?   │         │
                      └──────────────┬──────────────┘         │
                                     │ (no drift / green)     │
                      ┌──────────────▼──────────────┐         │
                      │    5. Approve Deploy / PR   │◄────────┘
                      └─────────────────────────────┘
```

---

## 🛠️ Step-by-Step Instructions

### Step 1: Capture Screenshot
1. Locate the UI elements or run a browser harness screenshot (e.g. `screenshot.png` or an export from playwright/puppeteer).
2. Save the screenshot to a local verification path.

### Step 2: Multimodal Verification
1. Invoke the multimodal checker script `verify_ui.py`, pointing it to the current screenshot and the target design mockup:
   ```bash
   python3 agentic-vercel/vision-loop/scripts/verify_ui.py \
     --current-ui "./current_screenshot.png" \
     --target-mockup "./design_spec.png" \
     --gateway-url "$VERCEL_AI_GATEWAY_URL"
   ```
2. The script sends both images to the Vercel AI Gateway, which proxies to a multimodal model (like Claude 3.5 Sonnet or Gemini 1.5 Pro).

### Step 3: Parse Scorecard
1. The judge evaluates the screenshot against the mockup on:
   - **Alignment & Spacing**: Grid alignment, padding, margin compliance.
   - **Text Overflow**: Overlapping text boxes or truncated headers.
   - **Component Integrity**: Missing assets or broken styling states.
2. **If drift or visual bugs are identified**: Extract the specific layout coordinates and CSS suggestions returned in the JSON payload, apply edits to the source code, rebuild, and return to Step 1.
3. **If no drift is found**: Approve the visual deploy step.
