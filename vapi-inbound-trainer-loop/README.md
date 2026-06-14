# 🤖 Vapi Inbound Trainer Loop: Cognitive Buyer Persona Simulator

> **"Train your sales teams against the hardest prospects—built and self-tuned by AI."**

Generic roleplay training is too easy. AI roleplay is usually even worse—the agent agrees to whatever you say and buys the product within 30 seconds of the call starting. Real buyers don't do that. Real buyers have objections, skepticism, and inertia.

`vapi-inbound-trainer-loop` is an installable agent skill that configures and maintains realistic, challenging buyer objection training bots on Vapi. It deploys specialized psychology-driven system prompts, attaches them to phone numbers, and evaluates recent logs to **self-tune the assistant** if it becomes too compliant.

---

## ⚡ Key Capabilities

- **Psychology-Driven Personas**: Deploys structured profiles (Defensive, Analytical, Urgency-Free) with complex objection pathways.
- **Character Compliance Audit**: Scans transcripts to determine if the agent was "too nice" or broke character.
- **Prompt Self-Tuning**: Rewrites the system prompt to patch behavioral exploits, raising the simulation difficulty.
- **Phone Number Linking**: Connects assistants directly to your phone lines via Vapi CLI.

---

## 📂 Repository Structure

```
vapi-inbound-trainer-loop/
├── SKILL.md                 # Procedural agent instructions
├── README.md                # Configuration and use manual (this file)
├── scripts/
│   ├── create_trainer_assistant.py # Deploys trainer assistants to Vapi
│   └── tune_assistant_prompt.py    # Audits compliance and updates prompt
└── templates/
    └── psychology_profiles.json    # Objections profile templates
```

---

## 🚀 Quick Start & Installation

```bash
# Register the skill with your agent CLI
agents skill install file:///Users/matthewbishop/BishopTech.dev/bishoptech-skills-for-agents/vapi-inbound-trainer-loop
```

### 1. Setup Vapi Credentials
Make sure your Vapi API keys are exported:
```bash
export VAPI_API_KEY="your-vapi-private-api-key"
```

### 2. Deploy a Trainer Assistant
Create a training bot using one of the pre-built buyer templates:
```bash
python3 vapi-inbound-trainer-loop/scripts/create_trainer_assistant.py \
  --profile "analytical" \
  --assistant-name "Analytical Buyer simulation"
```
*Note the Vapi Assistant ID returned by the script.*

### 3. Run a Training Call & Audit
Have your sales representative dial the assistant. Save the transcript (or fetch it from your Vapi call log), then run the audit loop:
```bash
python3 vapi-inbound-trainer-loop/scripts/tune_assistant_prompt.py \
  --assistant-id "your-vapi-assistant-id" \
  --transcript-path "./call_transcript.txt"
```
*The script will automatically update the assistant's prompts on Vapi to address any compliance gaps.*

---

## ⚙️ How the Self-Tuning Loop Works

```
[ obection template ] ──► [ create_trainer_assistant.py ] ──► [ Active Vapi Bot ]
                                                                     │
                                                                     ▼
[ Self-Tuning prompt ] ◄── [ tune_assistant_prompt.py ] ◄── [ Live Training Call ]
```

1. **Instantiation**: The system creates a Vapi assistant with a strict system prompt based on `templates/psychology_profiles.json`.
2. **Evaluation**: Trainees talk to the bot.
3. **Auditing**: `tune_assistant_prompt.py` inspects the conversation log. If the trainee succeeded too easily or the assistant violated its defense guidelines, the script marks the exploit.
4. **Correction**: The assistant's system instructions are rebuilt with explicit negative constraints blocking the trainee's exploit.
