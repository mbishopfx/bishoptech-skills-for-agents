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
    print(f"[{Colors.BOLD}LOGIC{Colors.END}] {msg}")

def log_pass(msg):
    print(f"[{Colors.GREEN}ROUTE-OK{Colors.END}] {msg}")

def log_warn(msg):
    print(f"[{Colors.YELLOW}ROUTE-WARN{Colors.END}] {msg}")

def log_fail(msg):
    print(f"[{Colors.RED}ROUTE-FAIL{Colors.END}] {msg}")

def query_gateway(prompt, model, gateway_url=None, token=None):
    """
    Submits a query to the Vercel AI Gateway proxy.
    """
    if not gateway_url or not token:
        # Simulate API response
        # Let's mock a failure for DeepSeek to demonstrate fallback, and success for GPT-4
        if "deepseek" in model.lower():
            # Mocking a corrupted JSON formatting error
            return "{\n  \"username\": \"admin\",\n  \"role\": admin // missing quotes\n}", 0.5
        else:
            return "{\n  \"username\": \"admin\",\n  \"role\": \"admin\"\n}", 0.95

    try:
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}]
        }
        req = urllib.request.Request(gateway_url, data=json.dumps(payload).encode('utf-8'), headers=headers, method='POST')
        with urllib.request.urlopen(req) as response:
            res = json.loads(response.read().decode('utf-8'))
            output = res['choices'][0]['message']['content']
            return output, 1.0
    except Exception as e:
        log_warn(f"Vercel Gateway error querying {model}: {e}")
        return "", 0.0

def verify_output(output):
    """
    Checks if output is valid JSON.
    """
    try:
        json.loads(output)
        return True, 1.0
    except Exception as e:
        return False, 0.4

def main():
    parser = argparse.ArgumentParser(description="Vercel AI Gateway Tiered Routing Engine")
    parser.add_argument("--prompt", required=True, help="User prompt to execute")
    parser.add_argument("--tier1", default="deepseek-flash", help="Fast, cost-effective model")
    parser.add_argument("--tier2", default="gpt-4o", help="High reasoning backup model")
    parser.add_argument("--gateway-url", default=os.getenv("VERCEL_AI_GATEWAY_URL"), help="Vercel AI Gateway URL")
    parser.add_argument("--token", default=os.getenv("VERCEL_AI_GATEWAY_TOKEN"), help="Gateway token")
    args = parser.parse_args()

    log_info(f"Task Prompt: '{args.prompt}'")
    
    # 1. Try Tier 1 Model
    log_info(f"Routing to Tier 1 Model ({args.tier1})...")
    output_t1, connection_score = query_gateway(args.prompt, args.tier1, args.gateway_url, args.token)
    
    passed_t1, score_t1 = verify_output(output_t1)
    
    print(f"\n{Colors.BOLD}--- TIER 1 EVALUATION ({args.tier1}) ---{Colors.END}")
    print(f"Validation Score : {Colors.GREEN if passed_t1 else Colors.RED}{score_t1 * 100:.0f}%{Colors.END}")
    print(f"Output Preview   : {output_t1.strip().replace(chr(10), ' '[:15])[:40]}...")
    print(f"{Colors.BOLD}--------------------------------------{Colors.END}")

    if passed_t1:
        log_pass("Tier 1 output verified. Task complete.")
        sys.exit(0)

    # 2. Fallback to Tier 2 Model
    log_warn("Tier 1 output failed verification. Triggering Vercel AI Gateway fallback to Tier 2...")
    log_info(f"Routing to Tier 2 Model ({args.tier2})...")
    
    output_t2, connection_score = query_gateway(args.prompt, args.tier2, args.gateway_url, args.token)
    passed_t2, score_t2 = verify_output(output_t2)

    print(f"\n{Colors.BOLD}--- TIER 2 EVALUATION ({args.tier2}) ---{Colors.END}")
    print(f"Validation Score : {Colors.GREEN if passed_t2 else Colors.RED}{score_t2 * 100:.0f}%{Colors.END}")
    print(f"Output Preview   : {output_t2.strip().replace(chr(10), ' '[:15])[:40]}...")
    print(f"{Colors.BOLD}--------------------------------------{Colors.END}")

    if passed_t2:
        log_pass("Tier 2 fallback output verified. Task complete.")
        sys.exit(0)

    # 3. Escalate to Human
    log_fail("Both Model Tiers failed quality checks. Triggering human review escalation gate.")
    sys.exit(1)

if __name__ == "__main__":
    main()
