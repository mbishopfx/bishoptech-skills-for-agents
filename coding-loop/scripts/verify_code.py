#!/usr/bin/env python3
import os
import sys
import argparse
import subprocess
import re

# ANSI colors
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    END = '\033[0m'

def log_info(msg):
    print(f"[{Colors.BOLD}CHECKER{Colors.END}] {msg}")

def log_pass(msg):
    print(f"[{Colors.GREEN}PASS{Colors.END}] {msg}")

def log_warn(msg):
    print(f"[{Colors.YELLOW}WARN{Colors.END}] {msg}")

def log_fail(msg):
    print(f"[{Colors.RED}FAIL{Colors.END}] {Colors.BOLD}{msg}{Colors.END}")

def get_git_diff(project_path):
    try:
        # Get diff of modified and staged files
        res = subprocess.run(
            "git diff HEAD",
            shell=True,
            cwd=project_path,
            text=True,
            capture_output=True,
            check=True
        )
        return res.stdout
    except subprocess.CalledProcessError as e:
        log_fail(f"Failed to fetch git diff: {e.stderr}")
        return ""

def load_rules(project_path):
    rules_path = os.path.join(project_path, "RULES.md")
    if not os.path.exists(rules_path):
        # Fallback to templates/RULES.md
        rules_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates", "RULES.md")
    
    if not os.path.exists(rules_path):
        log_warn("No RULES.md found. Using default coding rules.")
        return []

    rules = []
    with open(rules_path, "r") as f:
        for line in f:
            line = line.strip()
            # Find markdown checklist items
            if line.startswith("- [ ]") or line.startswith("- [x]"):
                rule = line[5:].strip()
                rules.append(rule)
    return rules

def main():
    parser = argparse.ArgumentParser(description="Adversarial Code Compliance Checker")
    parser.add_argument("--project-path", required=True, help="Path to the git repository")
    args = parser.parse_args()

    project_path = os.path.abspath(args.project_path)
    log_info(f"Initiating adversarial check for project: {project_path}")

    diff = get_git_diff(project_path)
    if not diff:
        log_warn("No changes detected in git diff. Nothing to verify.")
        sys.exit(0)

    rules = load_rules(project_path)
    violations = 0

    # Parse additions in diff
    added_lines = []
    for line in diff.split("\n"):
        if line.startswith("+") and not line.startswith("+++"):
            added_lines.append(line[1:])

    # 1. Check for basic "slop" and debug residues
    log_info("Scanning diff for debug residue and comments...")
    
    debug_patterns = {
        r"console\.log": "Found console.log in code. Use proper logging structure.",
        r"print\(": "Found raw print() statement in Python code. Use logger.",
        r"TODO": "Unresolved TODO placeholder found in candidate code.",
        r"FIXME": "Unresolved FIXME comment found.",
        r"var_dump": "Found PHP var_dump debug statement.",
        r"debugger;": "Found JavaScript debugger breakpoint."
    }

    for pattern, reason in debug_patterns.items():
        for i, line in enumerate(added_lines):
            if re.search(pattern, line):
                log_fail(f"Line {i+1}: {reason}")
                print(f"  > {line.strip()}")
                violations += 1

    # 2. Check diff against loaded rules
    log_info(f"Validating changes against {len(rules)} project rules...")
    for rule in rules:
        # Match common rules using simple regex
        if "No raw SQL" in rule or "sql" in rule.lower():
            # Check if SELECT, INSERT, UPDATE etc are embedded in strings
            for i, line in enumerate(added_lines):
                if re.search(r"(select|insert|update|delete)\s+.*\s+from", line, re.IGNORECASE):
                    log_fail(f"Rule Violation: '{rule}'")
                    print(f"  > {line.strip()}")
                    violations += 1

        if "No external auth" in rule or "auth" in rule.lower():
            for i, line in enumerate(added_lines):
                if "firebase.auth" in line.lower() or "supabase.auth" in line.lower():
                    log_fail(f"Rule Violation: '{rule}'")
                    print(f"  > {line.strip()}")
                    violations += 1

    if violations == 0:
        log_pass("Adversarial verification check completed. All compliance tests passed!")
        sys.exit(0)
    else:
        log_fail(f"Adversarial verification failed with {violations} violation(s). Please fix before committing.")
        sys.exit(1)

if __name__ == "__main__":
    main()
