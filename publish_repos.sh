#!/usr/bin/env bash

# Exit immediately if a command exits with a non-zero status
set -e

echo -e "\033[1;36m🦾 BishopTech Skills Repository Publisher\033[0m"
echo -e "Author: mbishopfx | mattbishopfx@gmail.com"
echo -e "Collaborator to invite: matt@bishoptech.dev\n"

# Verify gh CLI is installed
if ! command -v gh &> /dev/null; then
    echo -e "\033[1;31mError: GitHub CLI (gh) is not installed.\033[0m"
    echo -e "Please install it via: brew install gh"
    exit 1
fi

# Verify gh CLI is authenticated
if ! gh auth status &> /dev/null; then
    echo -e "\033[1;33mWarning: You are not authenticated with the GitHub CLI (gh).\033[0m"
    echo -e "Please run 'gh auth login' first to authenticate."
    exit 1
fi

SKILLS=("coding-loop" "marketing-eval-loop" "runtime-guardrail-loop" "vapi-outbound-loop" "vapi-inbound-trainer-loop" "agentic-vercel" "vercel-deploy-nurture")
BASE_DIR="/Users/matthewbishop/BishopTech.dev/bishoptech-skills-for-agents"

for SKILL in "${SKILLS[@]}"; do
    SKILL_PATH="$BASE_DIR/$SKILL"
    if [ -d "$SKILL_PATH" ]; then
        echo -e "\n\033[1;34m📦 Processing skill: $SKILL...\033[0m"
        cd "$SKILL_PATH"

        # Initialize git repo if not already done
        if [ ! -d ".git" ]; then
            git init
            git checkout -b main
        fi

        # Configure local git author
        git config user.name "mbishopfx"
        git config user.email "mattbishopfx@gmail.com"

        # Add files and commit
        git add .
        git commit -m "feat: initial commit of AAA agent $SKILL" --author="mbishopfx <mattbishopfx@gmail.com>" || echo "No changes to commit"

        # Create repo on GitHub (public, as user requested public use skills)
        REPO_NAME="agent-skill-$SKILL"
        echo -e "Creating GitHub repository: $REPO_NAME..."
        
        # Check if remote already exists, if not, create it
        if ! git remote get-url origin &> /dev/null; then
            gh repo create "$REPO_NAME" --public --confirm
            git remote add origin "https://github.com/mbishopfx/$REPO_NAME.git"
        else
            echo "Remote origin already configured."
        fi

        # Push to main
        echo "Pushing code to GitHub..."
        git push -u origin main --force

        # Invite collaborator
        echo -e "Inviting matt@bishoptech.dev (GitHub: bishoptechllc) as collaborator to $REPO_NAME..."
        gh api -X PUT "/repos/mbishopfx/$REPO_NAME/collaborators/bishoptechllc" -f permission=push || echo "Warning: Could not invite collaborator bishoptechllc"

        echo -e "\033[1;32m✓ Done processing $SKILL!\033[0m"
    else
        echo -e "\033[1;31mDirectory $SKILL does not exist. Skipping.\033[0m"
    fi
done

echo -e "\n\033[1;32m🎉 All repositories have been initialized, pushed, and collaborators invited successfully!\033[0m"
