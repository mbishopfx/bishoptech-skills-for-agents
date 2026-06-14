---
name: talk-loop
description: Text-to-Speech audio verification loop. Generates speech via Vercel AI Gateway, checks audio quality and word pronunciation counts, and refines synthesis parameters.
---

# 🗣️ Talk Loop: Speech Synthesis QA Agent Skill

This skill allows an agent to run an autonomous speech verification loop. It takes text prompts, synthesizes speech through providers (ElevenLabs, PlayHT) configured in the Vercel AI Gateway, runs a local audio quality validator (verifying word counts and checks for empty clippings), and self-corrects using SSML tags or voice configurations.

---

## 🔁 Execution Flow

```
                      ┌─────────────────────────────┐
                      │    1. Input Text Prompt     │
                      │    & Voice Configuration    │
                      └──────────────┬──────────────┘
                                     │
                      ┌──────────────▼──────────────┐
                      │ 2. Synthesize Speech Audio  │
                      │   (via Vercel AI Gateway)   │
                      └──────────────┬──────────────┘
                                     │
                      ┌──────────────▼──────────────┐
                      │  3. Analyze Audio Payload   │
                      │  (Word Counts / Clippings)  │
                      └──────────────┬──────────────┘
                                     │
                                     ├────────────────────────┐
                      ┌──────────────▼──────────────┐         │ (clippings/errors)
                      │    4. Audio Quality Pass?   │         │
                      └──────────────┬──────────────┘         │
                                     │ (clean audio)          │
                      ┌──────────────▼──────────────┐         │
                      │    5. Deploy Speech File    │◄────────┘
                      └─────────────────────────────┘
```

---

## 🛠️ Step-by-Step Instructions

### Step 1: Input Text Prompt & Voice Configuration
1. Load target text content for voice generation.
2. Select desired voice configuration (model, speed, pitch, provider).

### Step 2: Speech Synthesis
1. Run the speech synthesis orchestrator `generate_voice.py` pointing it to the text and configuration:
   ```bash
   python3 agentic-vercel/talk-loop/scripts/generate_voice.py \
     --text "Welcome to the BishopTech Agent Loops Registry." \
     --output "./welcome.mp3" \
     --gateway-url "$VERCEL_AI_GATEWAY_URL"
   ```
2. The script sends the request payload to the Vercel AI Gateway, routing it to the selected TTS engine (e.g. ElevenLabs).

### Step 3: Analyze Audio Payload
1. The validator reads the output audio file (`.mp3` or `.wav`).
2. Checks:
   - **File Size**: Check if the file is empty or too small (which indicates a connection timeout or empty response).
   - **Word Alignment**: Check if word pronunciation count matches the length of the original text.
   - **Silent Clips**: Scans for prolonged periods of silence.
3. **If audio checks fail**: Rebuild the prompt payload with specific SSML tags (e.g. `<break time="1s"/>`, `<emphasis>`) or tweak speed parameters, and rerun Step 2.
4. **If audio checks pass**: Deploy/store the generated voice file.
