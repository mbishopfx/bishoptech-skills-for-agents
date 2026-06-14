#!/usr/bin/env python3
import os
import sys
import json
import urllib.request

def log_info(msg):
    print(f"[SLACK-NOTIFIER] {msg}")

def log_error(msg):
    print(f"[SLACK-NOTIFIER] [ERROR] {msg}")

def build_slack_payload(draft_content, report):
    score = report.get("weighted_score", 0.0)
    passed = report.get("passed", False)
    breakdown = report.get("breakdown", {})
    justifications = breakdown.get("justifications", {})

    status_emoji = "✅ PASS" if passed else "❌ REJECT"
    status_color = "#2eb886" if passed else "#a30200"

    # Truncate draft to prevent payload size issues
    truncated_draft = draft_content[:800] + "..." if len(draft_content) > 800 else draft_content

    # Construct Block Kit layout
    payload = {
        "text": f"Agent Content Review: {status_emoji} (Score: {score:.2f})",
        "attachments": [
            {
                "color": status_color,
                "blocks": [
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f"*🤖 Agent Content Taste scorecard*\nStatus: *{status_emoji}* | Score: *{score:.2f}* (Target: 0.70)"
                        }
                    },
                    {
                        "type": "divider"
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": (
                                f"• *Specificity*: `{breakdown.get('specificity', 0.0):.2f}` - {justifications.get('specificity', '')}\n"
                                f"• *Proof & Evidence*: `{breakdown.get('proof', 0.0):.2f}` - {justifications.get('proof', '')}\n"
                                f"• *Voice Alignment*: `{breakdown.get('voice', 0.0):.2f}` - {justifications.get('voice', '')}\n"
                                f"• *Differentiation*: `{breakdown.get('differentiation', 0.0):.2f}` - {justifications.get('differentiation', '')}\n"
                                f"• *Bookmark Value*: `{breakdown.get('bookmark_value', 0.0):.2f}` - {justifications.get('bookmark_value', '')}"
                            )
                        }
                    },
                    {
                        "type": "divider"
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f"*Draft Preview:*\n```\n{truncated_draft}\n```"
                        }
                    },
                    {
                        "type": "actions",
                        "elements": [
                            {
                                "type": "button",
                                "text": {
                                    "type": "plain_text",
                                    "text": "👍 Approve & Deploy",
                                    "emoji": True
                                },
                                "style": "primary",
                                "value": "approve",
                                "action_id": "approve_content"
                            },
                            {
                                "type": "button",
                                "text": {
                                    "type": "plain_text",
                                    "text": "👎 Reject & Re-run",
                                    "emoji": True
                                },
                                "style": "danger",
                                "value": "reject",
                                "action_id": "reject_content"
                            }
                        ]
                    }
                ]
            }
        ]
    }
    return payload

def main():
    webhook_url = os.getenv("SLACK_WEBHOOK_URL")
    
    # Read evaluation report
    report_path = "eval_report.json"
    if not os.path.exists(report_path):
        log_error("eval_report.json not found. Run judge_content.py first.")
        sys.exit(1)

    with open(report_path, "r") as f:
        report = json.load(f)

    # Read draft file
    draft_path = None
    # Look for draft path arg or assume local draft.txt
    if len(sys.argv) > 1:
        draft_path = sys.argv[1]
    else:
        # Check standard file location
        draft_path = "draft_email.txt"

    if not os.path.exists(draft_path):
        # Create a mock draft for demonstration if empty
        with open(draft_path, "w") as f:
            f.write("Subject: Elevate your SaaS growth engine\n\nLet's delve into our tapestry of metrics to unlock synergies...")
    
    with open(draft_path, "r") as f:
        draft_content = f.read()

    payload = build_slack_payload(draft_content, report)

    if not webhook_url:
        log_info("SLACK_WEBHOOK_URL environment variable is empty.")
        log_info("Dumping interactive Block Kit payload to console (local validation pass):")
        print(json.dumps(payload, indent=2))
        sys.exit(0)

    # Send payload to Slack
    try:
        req = urllib.request.Request(
            webhook_url,
            data=json.dumps(payload).encode('utf-8'),
            headers={"Content-Type": "application/json"},
            method='POST'
        )
        with urllib.request.urlopen(req) as response:
            if response.status == 200:
                log_info("Successfully pushed scorecard and approval card to Slack!")
            else:
                log_error(f"Slack returned response status: {response.status}")
    except Exception as e:
        log_error(f"Failed to post to Slack: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
