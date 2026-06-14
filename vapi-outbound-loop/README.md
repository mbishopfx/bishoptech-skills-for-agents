# 📞 Vapi Outbound Loop: Autonomous Voice Campaign Agent

> **"Give your agents ears and a voice—without turning them into a spam machine."**

Most outbound AI voice implementations trigger a call, hang up, and hope for the best. There is no feedback loop. You don't know if the call reached the target person, if they hung up immediately, or if the conversation actually resolved your campaign goals.

`vapi-outbound-loop` is an installable agent skill that coordinates voice campaigns. It handles lead distribution, starts outbound phone calls using Vapi, monitors the call status asynchronously, retrieves transcripts, and uses an adversarial **LLM scorecard** to grade the conversation before updating your CRM.

---

## ⚡ Key Capabilities

- **Lead Queue Management**: Parses local lead lists and handles dialing pacing.
- **Asynchronous Monitoring**: Polls the Vapi network until the call completes, handling busy signals, voicemail drops, and disconnects.
- **Speech-to-Text Scorecard**: Automatically evaluates the transcript for sales qualification metrics (Need, Authority, Budget, and Next Steps).
- **CRM/Webhooks Integration**: Triggers post-call events (e.g. posting hot leads to Slack or updating JSON logs).

---

## 📂 Repository Structure

```
vapi-outbound-loop/
├── SKILL.md                 # Procedural agent instructions
├── README.md                # Configuration and use manual (this file)
├── scripts/
│   ├── outbound_campaign.py # Triggers calls and polls Vapi API for completion
│   └── evaluate_call.py     # Grades call transcripts against campaign rubrics
└── templates/
    └── campaign_leads.json  # Schema template for lead queues
```

---

## 🚀 Quick Start & Installation

```bash
# Register the skill with your agent CLI
agents skill install file:///Users/matthewbishop/BishopTech.dev/bishoptech-skills-for-agents/vapi-outbound-loop
```

### 1. Setup Vapi Credentials
Make sure your Vapi API keys are exported:
```bash
export VAPI_API_KEY="your-vapi-private-api-key"
```

### 2. Configure Your Lead List
Create a `campaign_leads.json` file inside your project directory (use `templates/campaign_leads.json` as a guide).

### 3. Execute the Campaign Loop
Run the orchestrator script to dial through your leads:
```bash
python3 vapi-outbound-loop/scripts/outbound_campaign.py \
  --leads-path "vapi-outbound-loop/templates/campaign_leads.json" \
  --assistant-id "your-vapi-assistant-id" \
  --phone-number-id "your-vapi-phone-number-id"
```

---

## ⚙️ How it Works under the Hood

```
[Lead List] ──► [outbound_campaign.py] ──► [Vapi Call API]
                       ▲                         │
                       │                         ▼
[Update JSON/CRM] ◄── [evaluate_call.py] ◄── [Poll Call Status]
```

1. **Triggering**: The campaign manager sends an HTTP POST request to `api.vapi.ai/call/phone` mapping the contact's details to the Vapi assistant variables.
2. **Polling**: The script polls Vapi call status. If it encounters a busy signal or voicemail, it logs it and marks it for retry.
3. **Transcription**: Once status is `ended`, the transcript is downloaded.
4. **Grading**: `evaluate_call.py` reads the transcript and scores specific columns. If a meeting was agreed, a high-priority Slack webhook is fired.
