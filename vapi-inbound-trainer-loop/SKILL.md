---
name: vapi-inbound-trainer-loop
description: Enterprise-ready inbound customer trainer loop. Deploys specialized buyer personas as Vapi assistants, polls recent trainer conversation logs, and refines system instructions when character consistency drifts.
---

# 🤖 Vapi Inbound Trainer Loop: Cognitive Buyer Persona Skill

This skill allows an agent to configure, deploy, and continuously optimize challenging buyer personas as inbound training phone agents. It pulls phone transcripts from Vapi, checks if the persona breaks character or becomes too compliant, and refines the assistant prompt instructions in a self-improving loop.

---

## 🔁 Execution Flow

```
                      ┌─────────────────────────────┐
                      │ 1. Load Objections Schema   │
                      │ (psychology_profiles.json)  │
                      └──────────────┬──────────────┘
                                     │
                      ┌──────────────▼──────────────┐
                      │ 2. Deploy Vapi Assistant    │
                      │ (create_trainer_assistant.py)│
                      └──────────────┬──────────────┘
                                     │
                      ┌──────────────▼──────────────┐
                      │ 3. User Completes Training  │
                      │          Phone Call         │
                      └──────────────┬──────────────┘
                                     │
                      ┌──────────────▼──────────────┐
                      │ 4. Read Call Logs & Check   │
                      │     Character Slippage      │
                      └──────────────┬──────────────┘
                                     │
                      ┌──────────────▼──────────────┐
                      │   5. Tune Assistant Prompt  │
                      │  (tune_assistant_prompt.py) │
                      └──────────────┬──────────────┘
                                     │
                      ┌──────────────▼──────────────┐
                      │ 6. Push Update to Vapi API  │
                      └─────────────────────────────┘
```

---

## 🛠️ Step-by-Step Instructions

### Step 1: Load Buyer Objections Profile
1. Read `/templates/psychology_profiles.json` to select a buyer objection level:
   - **Hostile/Defensive**: Rejects value statements, demands evidence.
   - **Analytical/Skeptical**: Needs quantitative breakdown, questions ROI.
   - **Complacent/Urgency-free**: Likes the current status quo, resists changing systems.

### Step 2: Create/Update Vapi Assistant
1. Run the assistant setup script, passing the target assistant ID (if updating) and the selected objections profile:
   ```bash
   python3 vapi-inbound-trainer-loop/scripts/create_trainer_assistant.py \
     --profile "skeptical" \
     --assistant-name "Skeptical Buyer Trainer"
   ```
2. Note the created `assistantId`.

### Step 3: Run Inbound Calls
1. Dial the trainer assistant's phone number or trigger an inbound session.
2. Instruct the human trainee (or simulation client) to complete a training conversation.

### Step 4: Audit Character Slippage
1. Pull the recent call logs and transcripts using Vapi CLI or API.
2. Parse the transcript to identify if the assistant was "too easy" (e.g. agreed to the pitch without resistance, accepted loose claims, or broke character).

### Step 5: Self-Optimize Prompt
1. Run `tune_assistant_prompt.py` against the transcript file:
   ```bash
   python3 vapi-inbound-trainer-loop/scripts/tune_assistant_prompt.py \
     --assistant-id "your-assistant-id" \
     --transcript-path "./training_call_log.txt"
   ```
2. The script identifies points where the agent became overly agreeable and inserts stricter behavioral instructions into the Vapi assistant configuration.
3. Update the Vapi assistant system prompt over the API.
