#!/usr/bin/env python3
import os
import sys
import argparse
import json
import time
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
    print(f"[{Colors.BLUE}CAMPAIGN{Colors.END}] {msg}")

def log_pass(msg):
    print(f"[{Colors.GREEN}CALL-OK{Colors.END}] {msg}")

def log_warn(msg):
    print(f"[{Colors.YELLOW}CALL-WAIT{Colors.END}] {msg}")

def log_fail(msg):
    print(f"[{Colors.RED}CALL-ERR{Colors.END}] {msg}")

def make_vapi_call(phone_number, assistant_id, phone_number_id, api_key):
    """
    Triggers outbound call using Vapi REST API.
    """
    url = "https://api.vapi.ai/call/phone"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "customer": {"number": phone_number},
        "assistantId": assistant_id,
        "phoneNumberId": phone_number_id
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

def poll_call_status(call_id, api_key):
    """
    Polls the Vapi call status endpoint until the call is completed.
    """
    url = f"https://api.vapi.ai/call/{call_id}"
    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    
    max_polls = 60  # Wait up to 10 minutes (60 * 10 seconds)
    poll_count = 0

    while poll_count < max_polls:
        poll_count += 1
        try:
            req = urllib.request.Request(url, headers=headers, method='GET')
            with urllib.request.urlopen(req) as response:
                res = json.loads(response.read().decode('utf-8'))
                status = res.get("status")
                
                log_warn(f"Call {call_id} status: {status.upper()} (poll {poll_count})")
                
                if status in ["ended", "failed"]:
                    return res, None
                    
            time.sleep(10)
        except Exception as e:
            return None, str(e)
            
    return None, "Polling timeout exceeded."

def run_simulation(lead_name, phone_number):
    """
    Simulates call progression for testing without credentials.
    """
    log_info(f"Simulating dialing {lead_name} ({phone_number})...")
    time.sleep(2)
    log_warn("Simulating state: RINGING...")
    time.sleep(2)
    log_warn("Simulating state: IN-PROGRESS...")
    time.sleep(3)
    log_pass("Simulating state: ENDED.")
    
    # Generate a realistic mock sales transcript
    mock_transcript = (
        f"Assistant: Hello, is this {lead_name}?\n"
        f"Customer: Yes, this is {lead_name}. Who is calling?\n"
        f"Assistant: Hi {lead_name}, I'm calling from BishopTech regarding your interest in our Agent Loop systems. "
        f"Do you have two minutes to discuss your current AI pipeline?\n"
        f"Customer: Oh, yeah! Actually, our team is struggling with AI slop and consistency. We run about 50,000 requests a day. "
        f"Our budget is around $2,000/month. We need a system that checks output before deploying.\n"
        f"Assistant: That's exactly what our Loop Engineering skills do. Would you be open to booking a short demo next Tuesday?\n"
        f"Customer: Tuesday at 10 AM works. Send me an invite at lead@company.com.\n"
        f"Assistant: Perfect, I will register that. Thank you!"
    )
    return {
        "id": "sim_call_12345",
        "status": "ended",
        "transcript": mock_transcript
    }

def main():
    parser = argparse.ArgumentParser(description="Vapi Outbound Campaign Orchestrator")
    parser.add_argument("--leads-path", required=True, help="Path to campaign_leads.json")
    parser.add_argument("--assistant-id", help="Vapi Assistant ID")
    parser.add_argument("--phone-number-id", help="Vapi Phone Number ID")
    parser.add_argument("--api-key", default=os.getenv("VAPI_API_KEY"), help="Vapi API Private Key")
    args = parser.parse_args()

    if not os.path.exists(args.leads_path):
        log_fail(f"Leads list not found: {args.leads_path}")
        sys.exit(1)

    with open(args.leads_path, "r") as f:
        leads_data = json.load(f)

    leads = leads_data.get("leads", [])
    if not leads:
        log_warn("No leads found in campaign list.")
        sys.exit(0)

    log_info(f"Initializing campaign loop with {len(leads)} contacts.")

    for lead in leads:
        lead_id = lead.get("id")
        name = lead.get("name")
        phone = lead.get("phone")
        status = lead.get("status", "pending")

        if status == "completed":
            log_info(f"Skipping lead {name} (already completed).")
            continue

        log_info(f"Triggering outbound call to: {name} ({phone})")

        # Run real Vapi call or fallback to simulator
        if args.api_key and args.assistant_id and args.phone_number_id:
            call_id, err = make_vapi_call(phone, args.assistant_id, args.phone_number_id, args.api_key)
            if err:
                log_fail(f"Failed to initiate call to {name}: {err}")
                continue
                
            log_info(f"Outbound call initiated. Vapi CallID: {call_id}")
            log_info("Polling Vapi for call completion...")
            call_result, poll_err = poll_call_status(call_id, args.api_key)
            if poll_err:
                log_fail(f"Error polling call progress: {poll_err}")
                continue
            
            transcript = call_result.get("transcript", "")
        else:
            log_warn("Vapi API key or IDs missing. Running call simulation...")
            call_result = run_simulation(name, phone)
            transcript = call_result.get("transcript", "")

        log_pass(f"Call with {name} finished.")
        
        # Write out the transcript for evaluation
        transcript_path = f"transcript_{lead_id}.txt"
        with open(transcript_path, "w") as f:
            f.write(transcript)
        log_info(f"Saved transcript to: {transcript_path}")

        # Mark lead status locally
        lead["status"] = "completed"
        lead["transcript_file"] = transcript_path

    # Save lead list updates
    with open(args.leads_path, "w") as f:
        json.dump(leads_data, f, indent=2)

    log_pass("Outbound campaign loop complete.")

if __name__ == "__main__":
    main()
