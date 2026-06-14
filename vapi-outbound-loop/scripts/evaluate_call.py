#!/usr/bin/env python3
import os
import sys
import argparse
import json
import urllib.request

# ANSI colors
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    END = '\033[0m'

def log_info(msg):
    print(f"[{Colors.BOLD}EVAL{Colors.END}] {msg}")

def log_pass(msg):
    print(f"[{Colors.GREEN}PASS{Colors.END}] {msg}")

def log_warn(msg):
    print(f"[{Colors.YELLOW}WARN{Colors.END}] {msg}")

def run_llm_judge(transcript_text, api_key=None):
    """
    Submits call transcript to LLM API for scoring.
    If no API key is present, runs local heuristic parsing.
    """
    if not api_key:
        log_warn("No API key provided. Running local regex heuristics on transcript...")
        return run_local_heuristics(transcript_text)

    log_info("Connecting to API for transcript qualification analysis...")

    system_prompt = (
        "You are an expert sales auditor. Analyze the following transcript between our voice assistant "
        "and a prospect. Score each qualification pillar from 0.0 (not mentioned/completely uninterested) "
        "to 1.0 (highly qualified/confirmed). "
        "Return ONLY a JSON object in this format: "
        '{"contact_verified": 1.0, "need_qualified": 0.8, "budget_discussed": 0.5, "next_steps_agreed": 0.9, '
        '"justifications": {"contact_verified": "...", "need_qualified": "...", "budget_discussed": "...", "next_steps_agreed": "..."}}'
    )

    try:
        url = f"https://generativetoolkit.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
        headers = {"Content-Type": "application/json"}
        payload = {
            "contents": [{"parts": [{"text": f"{system_prompt}\n\nTranscript:\n{transcript_text}"}]}],
            "generationConfig": {"responseMimeType": "application/json"}
        }
        
        req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers=headers, method='POST')
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            text_response = result['candidates'][0]['content']['parts'][0]['text']
            return json.loads(text_response)
    except Exception as e:
        log_warn(f"LLM API call failed ({e}). Falling back to local heuristic checks.")
        return run_local_heuristics(transcript_text)

def run_local_heuristics(transcript):
    """
    Scans transcripts for key phrases to build a mock scorecard.
    """
    scores = {
        "contact_verified": 0.5,
        "need_qualified": 0.5,
        "budget_discussed": 0.0,
        "next_steps_agreed": 0.0,
        "justifications": {}
    }

    transcript_lower = transcript.lower()

    # Contact verification check
    if "yes, this is" in transcript_lower or "speaking" in transcript_lower:
        scores["contact_verified"] = 1.0
        scores["justifications"]["contact_verified"] = "Prospect confirmed identity during greeting."
    else:
        scores["justifications"]["contact_verified"] = "Verification implicit or greeting unclear."

    # Need check
    need_keywords = ["slop", "consistency", "problem", "struggling", "need", "difficulty"]
    found_needs = [word for word in need_keywords if word in transcript_lower]
    if found_needs:
        scores["need_qualified"] = 0.90
        scores["justifications"]["need_qualified"] = f"Prospect highlighted key challenges: {', '.join(found_needs)}."
    else:
        scores["justifications"]["need_qualified"] = "No explicit needs or problems mentioned."

    # Budget check
    if "$" in transcript or "budget" in transcript_lower or "price" in transcript_lower:
        scores["budget_discussed"] = 0.80
        scores["justifications"]["budget_discussed"] = "Budget metrics or constraints discussed."
    else:
        scores["justifications"]["budget_discussed"] = "Price or pricing criteria was not introduced."

    # Next steps check
    if "tuesday" in transcript_lower or "invite" in transcript_lower or "demo" in transcript_lower or "book" in transcript_lower:
        scores["next_steps_agreed"] = 1.0
        scores["justifications"]["next_steps_agreed"] = "Demo calendar event scheduling agreed."
    else:
        scores["justifications"]["next_steps_agreed"] = "No clear booking or follow-up confirmed."

    return scores

def main():
    parser = argparse.ArgumentParser(description="Call Transcript Qualification Auditor")
    parser.add_argument("--transcript-path", required=True, help="Path to the transcript text file")
    parser.add_argument("--api-key", default=os.getenv("GEMINI_API_KEY"), help="Gemini API Key")
    args = parser.parse_args()

    if not os.path.exists(args.transcript_path):
        print(f"[ERROR] Transcript file not found: {args.transcript_path}")
        sys.exit(1)

    with open(args.transcript_path, "r") as f:
        transcript = f.read()

    results = run_llm_judge(transcript, args.api_key)

    print(f"\n{Colors.BOLD}--- CALL QUALIFICATION CARD ---{Colors.END}")
    
    pillars = ["contact_verified", "need_qualified", "budget_discussed", "next_steps_agreed"]
    total_score = 0.0

    for pillar in pillars:
        score = results.get(pillar, 0.0)
        total_score += score
        justification = results.get("justifications", {}).get(pillar, "No context.")
        
        color = Colors.GREEN if score >= 0.7 else (Colors.YELLOW if score >= 0.4 else Colors.RED)
        print(f"• {pillar.replace('_', ' ').capitalize()}: {color}{score:.2f}{Colors.END}")
        print(f"  Audit: {justification}")

    avg_score = total_score / len(pillars)
    print(f"{Colors.BOLD}--------------------------------{Colors.END}")
    
    color = Colors.GREEN if avg_score >= 0.7 else Colors.RED
    print(f"Call Qualification Index: {color}{avg_score:.2f}{Colors.END} (Target: 0.70)")

    if avg_score >= 0.70:
        log_pass("Lead qualified for hot status follow-up.")
        sys.exit(0)
    else:
        log_warn("Lead did not clear target qualification index.")
        sys.exit(0)

if __name__ == "__main__":
    main()
