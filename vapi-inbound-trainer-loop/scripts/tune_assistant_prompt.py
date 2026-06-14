#!/usr/bin/env python3
import os
import sys
import argparse
import json
import urllib.request
import urllib.error

# ANSI colors
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'

def log_info(msg):
    print(f"[{Colors.BLUE}TUNER{Colors.END}] {msg}")

def log_pass(msg):
    print(f"[{Colors.GREEN}SUCCESS{Colors.END}] {Colors.BOLD}{msg}{Colors.END}")

def log_warn(msg):
    print(f"[{Colors.YELLOW}WARN{Colors.END}] {msg}")

def log_fail(msg):
    print(f"[{Colors.RED}ERROR{Colors.END}] {msg}")

def generate_optimized_prompt(transcript, current_prompt, api_key=None):
    """
    Calls LLM API to analyze the transcript for compliance slip-ups
    and generate stricter behavioral prompt instructions.
    """
    if not api_key:
        log_warn("No Gemini API key. Running heuristic prompt injection...")
        # Local heuristic injection
        exploit_rule = (
            "\n\n## Trainee Exploit Protection Rules (Auto-tuned):\n"
            "- DO NOT agree to a Tuesday demo or share your email until the trainee has explicitly quantified "
            "their pipeline's cost, transaction volume, or security framework details. Reject vague answers."
        )
        return current_prompt + exploit_rule

    log_info("Analyzing transcript for character slip-ups...")
    
    system_prompt = (
        "You are an expert prompt engineer and sales psychologist. You will analyze a sales training call "
        "transcript to find where the Vapi buyer agent broke character or became too agreeable. "
        "Generate an updated, modified version of the buyer agent's system prompt. You must append explicit "
        "negative constraints that prevent the trainee's specific exploit. Return ONLY the new system prompt."
    )

    prompt = f"Current Prompt:\n{current_prompt}\n\nTranscript:\n{transcript}"

    try:
        url = f"https://generativetoolkit.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
        headers = {"Content-Type": "application/json"}
        payload = {
            "contents": [{"parts": [{"text": f"{system_prompt}\n\n{prompt}"}]}]
        }
        
        req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers=headers, method='POST')
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result['candidates'][0]['content']['parts'][0]['text']
    except Exception as e:
        log_warn(f"LLM API call failed ({e}). Falling back to local prompt injection.")
        return current_prompt + "\n- Ensure you raise hard objections regarding budget and implementation hurdles."

def update_vapi_assistant(assistant_id, new_prompt, api_key):
    """
    Patches assistant on Vapi platform via HTTP PATCH.
    """
    url = f"https://api.vapi.ai/assistant/{assistant_id}"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": {
            "messages": [
                {"role": "system", "content": new_prompt}
            ]
        }
    }

    try:
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode('utf-8'),
            headers=headers,
            method='PATCH'
        )
        with urllib.request.urlopen(req) as response:
            res = json.loads(response.read().decode('utf-8'))
            return True, None
    except urllib.error.HTTPError as e:
        error_msg = e.read().decode('utf-8')
        return False, f"HTTP {e.code}: {error_msg}"
    except Exception as e:
        return False, str(e)

def main():
    parser = argparse.ArgumentParser(description="Vapi Prompt Self-Tuning Optimizer")
    parser.add_argument("--assistant-id", required=True, help="Vapi Assistant ID")
    parser.add_argument("--transcript-path", required=True, help="Path to the training call transcript")
    parser.add_argument("--api-key", default=os.getenv("VAPI_API_KEY"), help="Vapi API Private Key")
    parser.add_argument("--gemini-key", default=os.getenv("GEMINI_API_KEY"), help="Gemini API Key")
    args = parser.parse_args()

    if not os.path.exists(args.transcript_path):
        log_fail(f"Transcript log file not found: {args.transcript_path}")
        sys.exit(1)

    with open(args.transcript_path, "r") as f:
        transcript = f.read()

    # Load active state
    current_prompt = "You are a customer."
    state_path = "trainer_state.json"
    if os.path.exists(state_path):
        with open(state_path, "r") as f:
            state = json.load(f)
            current_prompt = state.get("active_prompt", current_prompt)

    optimized_prompt = generate_optimized_prompt(transcript, current_prompt, args.gemini_key)

    if args.api_key and not args.assistant_id.startswith("sim_"):
        log_info(f"Patching Vapi assistant {args.assistant_id}...")
        success, err = update_vapi_assistant(args.assistant_id, optimized_prompt, args.api_key)
        if not success:
            log_fail(f"Failed to update Vapi assistant prompt: {err}")
            sys.exit(1)
        log_pass("Successfully updated Vapi assistant prompt configuration over the API.")
    else:
        log_warn("Vapi API credentials or assistant ID missing. Simulating local state update...")
        log_pass("Successfully updated simulated assistant prompt in local configurations.")

    # Save state
    if os.path.exists(state_path):
        with open(state_path, "r") as f:
            state = json.load(f)
        state["active_prompt"] = optimized_prompt
        with open(state_path, "w") as f:
            json.dump(state, f, indent=2)

if __name__ == "__main__":
    main()
