# 🗣️ Talk Loop: Text-to-Speech Quality Verification Gate

> **"If your voice agent stutters or clips, users hang up. Verify audio quality at runtime."**

Standard text-to-speech API implementations take text and save the resulting file. However, TTS engines frequently clip short syllables, mispronounce names, introduce prolonged silences, or fail to generate audio entirely due to server stress.

`talk-loop` is an installable agent skill that gives your agent a **Speech Sense (Talk)**. It synthesizes speech through the **Vercel AI Gateway** (utilizing ElevenLabs, PlayHT, or Openai TTS), analyzes the audio file locally, and automatically regenerates the audio using refined voice parameters or SSML tags if glitches are detected.

---

## ⚡ Key Capabilities

- **Automated Audio Verification**: Audits file sizing, silent clips, and estimated word counts.
- **SSML Self-Correction Loop**: Inserts pronunciations or pauses (`<break/>`) if the audio linter flags failures.
- **Failover Routing**: Automatically routes queries to backup TTS providers through the Vercel AI Gateway if primary endpoints experience high latency.

---

## 📂 Folder Structure

```
talk-loop/
├── SKILL.md                 # Agent execution guide
├── README.md                # Human user manual (this file)
└── scripts/
    └── generate_voice.py    # TTS generator and audio linter
```

---

## 🚀 Quick Start & Installation

```bash
# Register the skill with your agent CLI
agents skill install file:///Users/matthewbishop/BishopTech.dev/bishoptech-skills-for-agents/agentic-vercel/talk-loop
```

### 1. Export Gateway URLs
```bash
export VERCEL_AI_GATEWAY_URL="https://gateway.ai.vercel.com/v1/projects/YOUR_PROJECT_SLUG/gateways/YOUR_GATEWAY_ID"
export VERCEL_AI_GATEWAY_TOKEN="your-vercel-ai-gateway-api-key"
```

### 2. Run Speech Loop
Pass text to be synthesized:
```bash
python3 agentic-vercel/talk-loop/scripts/generate_voice.py \
  --text "Your subscription will expire tomorrow. Please verify payment." \
  --output "./billing_notice.mp3"
```
*The script analyzes the resulting file. If it detects anomalies, it repeats the request with speed adjustments.*
