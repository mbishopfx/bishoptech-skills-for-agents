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
    print(f"[{Colors.BOLD}JUDGE{Colors.END}] {msg}")

def log_pass(msg):
    print(f"[{Colors.GREEN}PASS{Colors.END}] {msg}")

def log_warn(msg):
    print(f"[{Colors.YELLOW}WARN{Colors.END}] {msg}")

def log_fail(msg):
    print(f"[{Colors.RED}FAIL{Colors.END}] {msg}")

def run_llm_judge(draft_text, rubric_text, api_key=None, provider="gemini"):
    """
    Submits draft and rubric to LLM API for scoring.
    If no API key is present, falls back to a simulated heuristic score.
    """
    if not api_key:
        log_warn("No API key provided. Running heuristic local score simulation...")
        return run_local_heuristics(draft_text)

    log_info(f"Connecting to {provider.upper()} API for LLM-as-a-Judge rubric score...")

    # System instruction for JSON formatting
    system_prompt = (
        "You are an expert copy editor and marketing psychologist. Your job is to grade the user's draft "
        "against the provided rubric. You must be extremely strict and ignore stylistic prose if the criteria are unmet. "
        "Return ONLY a JSON object in this format: "
        '{"specificity": 0.8, "proof": 0.5, "voice": 0.9, "differentiation": 0.6, "bookmark_value": 0.7, '
        '"justifications": {"specificity": "...", "proof": "...", "voice": "...", "differentiation": "...", "bookmark_value": "..."}}'
    )

    prompt = f"Rubric:\n{rubric_text}\n\nDraft Content:\n{draft_text}"

    try:
        if provider == "gemini":
            # Call Gemini API
            url = f"https://generativetoolkit.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
            headers = {"Content-Type": "application/json"}
            payload = {
                "contents": [{"parts": [{"text": f"{system_prompt}\n\n{prompt}"}]}],
                "generationConfig": {"responseMimeType": "application/json"}
            }
            
            req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers=headers, method='POST')
            with urllib.request.urlopen(req) as response:
                result = json.loads(response.read().decode('utf-8'))
                text_response = result['candidates'][0]['content']['parts'][0]['text']
                return json.loads(text_response)
        else:
            log_fail(f"Unsupported provider: {provider}")
            sys.exit(1)
    except Exception as e:
        log_warn(f"LLM API call failed ({e}). Falling back to local heuristic checks.")
        return run_local_heuristics(draft_text)

def run_local_heuristics(draft_text):
    """
    Heuristics search for typical AI tells and formatting indicators.
    """
    scores = {
        "specificity": 0.5,
        "proof": 0.5,
        "voice": 0.8,
        "differentiation": 0.6,
        "bookmark_value": 0.5,
        "justifications": {}
    }

    # Voice check: search for AI words
    ai_tells = ["delve", "tapestry", "testament", "realm", "moreover", "in summary", "unlocking"]
    found_tells = [word for word in ai_tells if word in draft_text.lower()]
    if found_tells:
        scores["voice"] = max(0.2, 0.8 - (len(found_tells) * 0.15))
        scores["justifications"]["voice"] = f"Contains common AI stock phrases: {', '.join(found_tells)}."
    else:
        scores["justifications"]["voice"] = "Clean human-like phrasing detected."

    # Specificity check: search for lists or code codeblocks
    if "```" in draft_text or "playbook" in draft_text.lower() or "template" in draft_text.lower():
        scores["specificity"] = 0.8
        scores["justifications"]["specificity"] = "Contains structural playbook, codeblock, or template elements."
    else:
        scores["justifications"]["specificity"] = "Lacks copy-pasteable templates or playbooks."

    # Proof check: search for statistics or numbers
    numbers = re.findall(r'\b\d+%\b|\b\$\d+\b|\b\d{4}\b', draft_text)
    if len(numbers) >= 2:
        scores["proof"] = 0.85
        scores["justifications"]["proof"] = f"Supported by quantitative metrics or data points: {', '.join(numbers[:3])}."
    else:
        scores["justifications"]["proof"] = "Lacks quantitative proof or reference metrics."

    # Differentiation & Bookmark value logic
    if scores["specificity"] > 0.7 and scores["proof"] > 0.7:
        scores["differentiation"] = 0.75
        scores["bookmark_value"] = 0.8
        scores["justifications"]["differentiation"] = "High specificity separates this content from generic AI search results."
        scores["justifications"]["bookmark_value"] = "Highly actionable layout warrants bookmarking."
    else:
        scores["justifications"]["differentiation"] = "Standard editorial formatting."
        scores["justifications"]["bookmark_value"] = "High abstraction limits long-term bookmark value."

    return scores

def main():
    parser = argparse.ArgumentParser(description="LLM-as-a-Judge Content Evaluator")
    parser.add_argument("--draft-path", required=True, help="Path to the draft text file")
    parser.add_argument("--rubric-path", required=True, help="Path to the rubric markdown file")
    parser.add_argument("--api-key", default=os.getenv("GEMINI_API_KEY"), help="Google Gemini API Key")
    args = parser.parse_args()

    if not os.path.exists(args.draft_path):
        log_fail(f"Draft file not found: {args.draft_path}")
        sys.exit(1)

    if not os.path.exists(args.rubric_path):
        log_fail(f"Rubric file not found: {args.rubric_path}")
        sys.exit(1)

    with open(args.draft_path, "r") as f:
        draft = f.read()

    with open(args.rubric_path, "r") as f:
        rubric = f.read()

    results = run_llm_judge(draft, rubric, args.api_key)

    # Calculate weighted score
    weights = {
        "specificity": 0.25,
        "proof": 0.20,
        "voice": 0.20,
        "differentiation": 0.20,
        "bookmark_value": 0.15
    }

    total_score = 0.0
    print(f"\n{Colors.BOLD}--- EVALUATION SCORECARD ---{Colors.END}")
    for key, weight in weights.items():
        score = results.get(key, 0.0)
        total_score += score * weight
        justification = results.get("justifications", {}).get(key, "No comment.")
        
        # Color coding individual criteria
        color = Colors.GREEN if score >= 0.7 else (Colors.YELLOW if score >= 0.5 else Colors.RED)
        print(f"• {key.capitalize()}: {color}{score:.2f}{Colors.END} (Weight: {weight * 100:.0f}%)")
        print(f"  Justification: {justification}")

    print(f"{Colors.BOLD}----------------------------{Colors.END}")
    
    threshold = 0.70
    color = Colors.GREEN if total_score >= threshold else Colors.RED
    print(f"Average Weighted Score: {color}{total_score:.2f}{Colors.END} (Target: {threshold:.2f})")

    # Save results to a file for subsequent stages (Slack/Telegram)
    output_report = {
        "weighted_score": total_score,
        "passed": total_score >= threshold,
        "breakdown": results
    }
    with open("eval_report.json", "w") as f:
        json.dump(output_report, f, indent=2)

    if total_score >= threshold:
        log_pass("Content cleared taste-gate threshold.")
        sys.exit(0)
    else:
        log_fail("Content failed taste-gate threshold. Rework required.")
        sys.exit(1)

if __name__ == "__main__":
    main()
