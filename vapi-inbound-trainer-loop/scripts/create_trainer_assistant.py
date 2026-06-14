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
    print(f"[{Colors.BLUE}TRAINER-SETUP{Colors.END}] {msg}")

def log_pass(msg):
    print(f"[{Colors.GREEN}SUCCESS{Colors.END}] {Colors.BOLD}{msg}{Colors.END}")

def log_fail(msg):
    print(f"[{Colors.RED}ERROR{Colors.END}] {msg}")

def load_profile(profile_name):
    """
    Loads buyer psychology profile template.
    """
    script_dir = os.path.dirname(os.path.dirname(__file__))
    profiles_path = os.path.join(script_dir, "templates", "psychology_profiles.json")
    
    if not os.path.exists(profiles_path):
        log_fail(f"Objections profiles file not found: {profiles_path}")
        sys.exit(1)
        
    with open(profiles_path, "r") as f:
        profiles = json.load(f)
        
    return profiles.get(profile_name)

def create_vapi_assistant(name, system_prompt, api_key):
    """
    Creates assistant on Vapi platform via HTTP POST.
    """
    url = "https://api.vapi.ai/assistant"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    # Standard Vapi assistant structure
    payload = {
        "name": name,
        "model": {
            "provider": "openai",
            "model": "gpt-4-turbo",
            "messages": [
                {"role": "system", "content": system_prompt}
            ]
        },
        "voice": {
            "provider": "playht",
            "voiceId": "susan"
        },
        "transcriber": {
            "provider": "deepgram",
            "model": "nova-2",
            "language": "en"
        }
    }

    try:
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode('utf-8'),
            headers=headers,
            method='POST'
        )
        with urllib.request.urlopen(req) as response:
            res = json.loads(response.read().decode('utf-8'))
            return res.get("id"), None
    except urllib.error.HTTPError as e:
        error_msg = e.read().decode('utf-8')
        return None, f"HTTP {e.code}: {error_msg}"
    except Exception as e:
        return None, str(e)

def main():
    parser = argparse.ArgumentParser(description="Vapi Inbound Trainer Assistant Creator")
    parser.add_argument("--profile", required=True, choices=["hostile", "skeptical", "complacent"], help="Objections profile name")
    parser.add_argument("--assistant-name", required=True, help="Name of the Vapi assistant to create")
    parser.add_argument("--api-key", default=os.getenv("VAPI_API_KEY"), help="Vapi API Private Key")
    args = parser.parse_args()

    profile = load_profile(args.profile)
    if not profile:
        log_fail(f"Invalid profile or profile details missing for: {args.profile}")
        sys.exit(1)

    system_prompt = profile.get("system_prompt")
    log_info(f"Loaded objection profile: {profile.get('name')}")
    log_info(f"Targeting assistant creation: {args.assistant_name}")

    if args.api_key:
        assistant_id, err = create_vapi_assistant(args.assistant_name, system_prompt, args.api_key)
        if err:
            log_fail(f"Failed to create Vapi assistant: {err}")
            sys.exit(1)
        log_pass(f"Assistant deployed to Vapi successfully. ID: {assistant_id}")
    else:
        log_info("Vapi API key missing. Simulating local deployment...")
        assistant_id = f"sim_assistant_{args.profile}_98765"
        log_pass(f"Simulated assistant created successfully. Mock ID: {assistant_id}")

    # Write out local state
    state = {
        "assistant_id": assistant_id,
        "name": args.assistant_name,
        "profile": args.profile,
        "active_prompt": system_prompt
    }
    with open("trainer_state.json", "w") as f:
        json.dump(state, f, indent=2)

if __name__ == "__main__":
    main()
