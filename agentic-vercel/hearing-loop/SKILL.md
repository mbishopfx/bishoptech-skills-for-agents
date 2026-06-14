---
name: hearing-loop
description: Asynchronous speech transcription and audit check loop. Transcribes audio feeds via Vercel AI Gateway and verifies summary requirements.
---

# 👂 Hearing Loop: Transcription QA Agent Skill

This skill allows an agent to run an autonomous transcription verification loop. It takes raw audio feeds (e.g., recorded client calls or meetings), transcribes them using speech-to-text engines (e.g. Whisper) routed through the Vercel AI Gateway, and audits the resulting transcript against structural template guidelines, asking clarifying questions if key fields remain blank.

---

## 🔁 Execution Flow

```
                      ┌─────────────────────────────┐
                      │    1. Load Audio Payload    │
                      │     & Target Template       │
                      └──────────────┬──────────────┘
                                     │
                      ┌──────────────▼──────────────┐
                      │    2. Transcribe Audio      │
                      │   (via Vercel AI Gateway)   │
                      └──────────────┬──────────────┘
                                     │
                      ┌──────────────▼──────────────┐
                      │ 3. Extract Structured Fields│
                      │    (Meeting Summaries)      │
                      └──────────────┬──────────────┘
                                     │
                                     ├────────────────────────┐
                      ┌──────────────▼──────────────┐         │ (key metrics missing)
                      │    4. Template Complete?    │         │
                      └──────────────┬──────────────┘         │
                                     │ (all fields filled)    │
                      ┌──────────────▼──────────────┐         │
                      │  5. Export Summary Log / PR  │◄────────┘
                      └─────────────────────────────┘
```

---

## 🛠️ Step-by-Step Instructions

### Step 1: Load Audio File & Template
1. Identify the input audio file (`.wav`, `.mp3`).
2. Load the structural template mapping target headers (e.g., attendees, action items, core decisions).

### Step 2: Speech-to-Text Transcription
1. Invoke the transcriber script `transcribe_audio.py` on the input:
   ```bash
   python3 agentic-vercel/hearing-loop/scripts/transcribe_audio.py \
     --audio-path "./client_meeting.mp3" \
     --template-path "agentic-vercel/hearing-loop/templates/meeting_summary_spec.json" \
     --gateway-url "$VERCEL_AI_GATEWAY_URL"
   ```
2. The script sends the audio payload to Vercel AI Gateway, proxying to a transcriber endpoint.

### Step 3: Extract & Validate Fields
1. The script extracts metadata using the transcribed text.
2. Checks:
   - **Attendees Listed**: Did we verify who is present?
   - **Action Items Found**: Are there explicit checklist items for attendees?
   - **Date & Title**: Are context details provided?
3. **If critical fields are empty**: The script flags missing data points (e.g. "Missing action items"). Prompt the user or loop to request supplementary audio/notes to resolve the gap, then restart Step 2.
4. **If fields are complete**: Export the validated JSON scorecard and log it to your tracking dashboard.
