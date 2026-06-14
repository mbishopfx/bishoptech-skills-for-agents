---
name: vapi-outbound-loop
description: Enterprise-ready autonomous outbound calling agent loop. Parses lead lists, triggers Vapi phone calls, monitors call state, retrieves transcripts, and runs post-call LLM-as-a-judge criteria scoring.
---

# 📞 Vapi Outbound Loop: Autonomous Voice Campaign Skill

This skill allows an agent to run an autonomous outbound call loop to qualify leads, follow up on signups, or check project status. It reads a list of phone numbers, initiates a Vapi call using the Vapi API or CLI, polls for call completion, retrieves the transcript, and evaluates candidate responses against an objective checklist.

---

## 🔁 Execution Flow

```
                     ┌─────────────────────────────┐
                     │     1. Read Lead List       │
                     │   (campaign_leads.json)     │
                     └──────────────┬──────────────┘
                                    │
                     ┌──────────────▼──────────────┐
                     │    2. Trigger Vapi Call     │
                     │    (outbound_campaign.py)   │
                     └──────────────┬──────────────┘
                                    │
                     ┌──────────────▼──────────────┐
                     │ 3. Poll Call Status until   │
                     │         Terminated          │
                     └──────────────┬──────────────┘
                                    │
                     ┌──────────────▼──────────────┐
                     │  4. Retrieve Transcript     │
                     │      & Call Recording       │
                     └──────────────┬──────────────┘
                                    │
                     ┌──────────────▼──────────────┐
                     │    5. Grade Call Success    │
                     │     (evaluate_call.py)      │
                     └──────────────┬──────────────┘
                                    │
                     ┌──────────────▼──────────────┐
                     │    6. Update Leads Database │
                     │      (Or Alert human)       │
                     └─────────────────────────────┘
```

---

## 🛠️ Step-by-Step Instructions

### Step 1: Read Lead List
1. Locate the targets list file, typically a JSON database of leads (e.g. `campaign_leads.json`).
2. Verify contact credentials: phone number, name, and background context keys.

### Step 2: Trigger Call
1. Start an outbound session for a contact using Vapi. Pass the target assistant ID and contact information:
   ```bash
   python3 vapi-outbound-loop/scripts/outbound_campaign.py \
     --lead-id "lead_001" \
     --assistant-id "your-assistant-id" \
     --phone-number-id "your-vapi-phone-number-id"
   ```
2. Save the returned Vapi `callId` for tracking.

### Step 3: Monitor Call Status
1. Poll the Vapi API endpoint `/call/{callId}` every 10 seconds.
2. Wait until status transitions to `ended`. If call fails (busy, no answer), log the failure state and proceed to the next lead or schedule a retry.

### Step 4: Extract transcript
1. Upon call termination, fetch the call detail record payload using `/call/{callId}`.
2. Read the full `transcript` text and save it locally.

### Step 5: Score the Conversation (Adversarial Judge)
1. Run the `evaluate_call.py` script on the transcript.
2. Evaluate success criteria:
   - **Contact Verified**: Did the agent talk to the correct person?
   - **Need Qualified**: Did the contact express pain points or need?
   - **Interest Level**: High, Medium, or Low interest?
   - **Next Steps Agreed**: Was a meeting booked or a follow-up agreed?
3. Save the scorecard to the lead database. If interest is *High* and a follow-up is needed, post a notification to Slack.
