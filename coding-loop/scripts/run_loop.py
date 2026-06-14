#!/usr/bin/env python3
import os
import sys
import argparse
import subprocess
import shutil

# ANSI colors for beautiful terminal output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def log_info(msg):
    print(f"{Colors.OKBLUE}[INFO]{Colors.ENDC} {msg}")

def log_success(msg):
    print(f"{Colors.OKGREEN}[SUCCESS]{Colors.ENDC} {Colors.BOLD}{msg}{Colors.ENDC}")

def log_warn(msg):
    print(f"{Colors.WARNING}[WARN]{Colors.ENDC} {msg}")

def log_error(msg):
    print(f"{Colors.FAIL}[ERROR]{Colors.ENDC} {Colors.BOLD}{msg}{Colors.ENDC}")

def run_command(cmd, cwd=None):
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            cwd=cwd,
            text=True,
            capture_output=True,
            check=True
        )
        return result.stdout, result.stderr, 0
    except subprocess.CalledProcessError as e:
        return e.stdout, e.stderr, e.returncode

def main():
    parser = argparse.ArgumentParser(description="AAA Coding Loop Orchestrator")
    parser.add_argument("--project-path", required=True, help="Path to the target git repository")
    parser.add_argument("--prompt", required=True, help="Description of the task or ticket to solve")
    parser.add_argument("--test-command", required=True, help="Command to run the test suite (e.g. 'npm run test')")
    parser.add_argument("--max-retries", type=int, default=5, help="Maximum number of test/fix loops before halting")
    args = parser.parse_args()

    project_path = os.path.abspath(args.project_path)
    if not os.path.isdir(project_path):
        log_error(f"Project path does not exist: {project_path}")
        sys.exit(1)

    log_info(f"Targeting project: {project_path}")
    log_info(f"Task: {args.prompt}")

    # Check git status
    stdout, _, code = run_command("git rev-parse --is-inside-work-tree", cwd=project_path)
    if code != 0 or "true" not in stdout:
        log_error("Target project path is not a git repository.")
        sys.exit(1)

    # Define worktree details
    branch_name = "feature/agent-coding-loop"
    worktree_dir = os.path.join(os.path.dirname(project_path), "coding_loop_worktree")

    # Clean up old worktree if exists
    if os.path.exists(worktree_dir) or os.path.isdir(worktree_dir):
        log_warn(f"Cleaning up existing worktree directory: {worktree_dir}")
        run_command(f"git worktree remove -f {worktree_dir}", cwd=project_path)
        shutil.rmtree(worktree_dir, ignore_errors=True)

    # Create Git Worktree
    log_info(f"Creating isolated worktree at: {worktree_dir} on branch: {branch_name}")
    stdout, stderr, code = run_command(f"git worktree add -b {branch_name} {worktree_dir} main", cwd=project_path)
    if code != 0:
        # Retry with existing branch checkout if creation fails
        log_warn("Branch might already exist. Trying to checkout existing branch in worktree...")
        stdout, stderr, code = run_command(f"git worktree add {worktree_dir} {branch_name}", cwd=project_path)
        if code != 0:
            log_error(f"Failed to create git worktree: {stderr}")
            sys.exit(1)

    log_success("Git worktree created successfully.")

    # Begin the verification loop
    retry_count = 0
    test_passed = False

    while retry_count < args.max_retries:
        retry_count += 1
        log_info(f"--- Iteration {retry_count}/{args.max_retries} ---")
        
        # Execute tests/lints
        log_info(f"Executing validation command: '{args.test_command}'")
        stdout, stderr, code = run_command(args.test_command, cwd=worktree_dir)

        if code == 0:
            log_success("All tests and linters passed!")
            test_passed = True
            break
        else:
            log_warn(f"Validation failed with exit code: {code}")
            print(f"{Colors.FAIL}--- TEST OUTLINE / FAILURE LOG ---{Colors.ENDC}")
            # Output truncated stdout/stderr to prevent cluttering context
            combined_log = (stdout + "\n" + stderr).strip()
            lines = combined_log.split("\n")
            for line in lines[-20:]:  # Print last 20 lines of logs
                print(f"  {line}")
            print(f"{Colors.FAIL}-----------------------------------{Colors.ENDC}")
            
            log_info("Passing failure logs back to agent workspace for correction...")
            # Save error logs to worktree root for agent digestion
            with open(os.path.join(worktree_dir, "coding_loop_error.log"), "w") as f:
                f.write(combined_log)
            
            # Pause and ask the agent (this script runner) to fix the file.
            # In a real agent setup, the agent parses this script's stdout and modifies files.
            print(f"\n[ACTION REQUIRED] Please edit the files in the worktree to resolve the errors shown above.")
            print(f"Worktree Path: {worktree_dir}")
            print(f"Type 'continue' when ready to test again, or 'exit' to halt the loop.")
            
            # Simple interactive wait for demonstration/manual usage, or auto-exit for non-interactive
            if sys.stdin.isatty():
                user_input = input(">> ").strip().lower()
                if user_input == 'exit':
                    break
            else:
                # If non-interactive, exit so agent can edit and re-run python script
                log_warn("Non-interactive terminal. Exiting with status 1 to let the agent apply edits.")
                sys.exit(1)

    if test_passed:
        log_success("Coding loop complete. Code is ready for review/merge.")
        # Trigger adversarial check next
        sys.exit(0)
    else:
        log_error("Coding loop failed: Maximum retries exceeded without clearing test suite.")
        sys.exit(1)

if __name__ == "__main__":
    main()
