# 👂 Hearing Loop: Asynchronous Transcription & Audit Gate

> **"Transcribing audio is only the first step. You need to verify that you actually heard what matters."**

Simply transcribing an audio file using speech-to-text engines is not enough. Critical details like action items, dates, and names are often slurred, omitted, or misparsed. 

`hearing-loop` is an installable agent skill that gives your agent a **Hearing Sense**. It transcribes files through your **Vercel AI Gateway**, runs the text through a structural parser, and audits it to check if key template items (such as action items or dates) are missing. If gaps are found, the loop prompts the agent to request clarifying inputs or re-run transcription.

---

## ⚡ Key Capabilities

- **Gateway-Routed Transcription**: Proxies binary audio requests to Whisper or Deepgram via the Vercel AI Gateway.
- **Structural Audit Checks**: Parses transcripts into structured meeting minutes JSON and flags missing categories.
- **Failover Capabilities**: Switches between transcriber models if primary connections time out.

---

## 📂 Folder Structure

```
hearing-loop/
├── SKILL.md                 # Agent execution guide
├── README.md                # Human user manual (this file)
└── scripts/
    └── transcribe_audio.py  # Transcriber and audit validator
```

---

## 🚀 Quick Start & Installation

```bash
# Register the skill with your agent CLI
agents skill install file:///Users/matthewbishop/BishopTech.dev/bishoptech-skills-for-agents/agentic-vercel/hearing-loop
```

### 1. Export Gateway URLs
```bash
export VERCEL_AI_GATEWAY_URL="https://gateway.ai.vercel.com/v1/projects/YOUR_PROJECT_SLUG/gateways/YOUR_GATEWAY_ID"
export VERCEL_AI_GATEWAY_TOKEN="your-vercel-ai-gateway-api-key"
```

### 2. Run Hearing Loop
Pass audio path for transcription and verification:
```bash
python3 agentic-vercel/hearing-loop/scripts/transcribe_audio.py \
  --audio-path "./client_interview.mp3" \
  --template-path "agentic-vercel/hearing-loop/templates/meeting_summary_spec.json"
```
*The script extracts text and evaluates compliance. It exits with 0 if key meeting data is complete.*
