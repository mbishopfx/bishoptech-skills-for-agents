#!/usr/bin/env bash

# Exit immediately if a command exits with a non-zero status
set -e

MODE=$1
BASE_DIR="/Users/matthewbishop/BishopTech.dev/bishoptech-skills-for-agents"
SUBDIRS=("coding-loop" "marketing-eval-loop" "runtime-guardrail-loop" "vapi-outbound-loop" "vapi-inbound-trainer-loop" "agentic-vercel" "vercel-deploy-nurture")

if [[ "$MODE" != "monorepo" && "$MODE" != "subrepos" ]]; then
    echo "Usage: ./git_restore.sh [monorepo|subrepos]"
    exit 1
fi

echo -e "\033[1;34mSwitching workspace to mode: $MODE...\033[0m"

for SUB in "${SUBDIRS[@]}"; do
    SUB_PATH="$BASE_DIR/$SUB"
    if [ -d "$SUB_PATH" ]; then
        if [[ "$MODE" == "monorepo" ]]; then
            # Rename .git to .git_backup
            if [ -d "$SUB_PATH/.git" ]; then
                mv "$SUB_PATH/.git" "$SUB_PATH/.git_backup"
                echo "✓ Converted $SUB to Monorepo file tracking."
            else
                echo "- $SUB is already tracked under Monorepo."
            fi
        elif [[ "$MODE" == "subrepos" ]]; then
            # Rename .git_backup to .git
            if [ -d "$SUB_PATH/.git_backup" ]; then
                mv "$SUB_PATH/.git_backup" "$SUB_PATH/.git"
                echo "✓ Restored $SUB as separate Git repository."
            else
                echo "- $SUB is already tracked as a separate Git repository."
            fi
        fi
    fi
done

echo -e "\033[1;32m✓ Done!\033[0m"
