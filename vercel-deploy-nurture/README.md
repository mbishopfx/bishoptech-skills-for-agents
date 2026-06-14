# 🚀 Vercel Deploy & Nurture: Autonomous Delivery & Disk Cleanup Loop

> **"Build, deploy, verify, self-repair, and reclaim local storage space—automatically."**

Deploying web applications to Vercel is simple, but managing build logs, debugging remote serverless function failures, running sanity checks, and managing heavy local folders like `node_modules` and `.next` drains both developer time and system disk space.

`vercel-deploy-nurture` is an installable agent skill that automates your Vercel deployment lifecycle. It triggers the Vercel CLI build, logs and parses remote compilation errors (like TypeScript mismatches), self-corrects the code in a repair loop, runs post-deployment HTTP health checks, and deletes local `node_modules` upon success to keep your hard drive clean.

---

## ⚡ Key Capabilities

- **Vercel CLI Orchestration**: Triggers builds and parses target deployment preview URLs.
- **Log Parsing & Self-Repair**: Extracts remote logs and applies code edits to resolve TypeScript compiler errors.
- **HTTP Health checks**: Queries post-deploy URLs to verify latency and return status codes.
- **Node Modules Pruning**: Reclaims disk space by running automated `rm -rf node_modules` commands upon a successful remote deploy.

---

## 📂 Folder Structure

```
vercel-deploy-nurture/
├── SKILL.md                 # Agent execution guide
├── README.md                # Human user manual (this file)
├── scripts/
│   └── deploy_nurture.py    # Deployment orchestrator and health checker
└── templates/
    └── health_check_spec.json # Target endpoints and assertion criteria
```

---

## 🚀 Quick Start & Installation

```bash
# Register the skill with your agent CLI
agents skill install file:///Users/matthewbishop/BishopTech.dev/bishoptech-skills-for-agents/vercel-deploy-nurture
```

### 1. Login to Vercel
Make sure your Vercel CLI is authenticated locally:
```bash
vercel login
```

### 2. Configure Your Health Targets
Create a `health_check_spec.json` inside your project directory (use `templates/health_check_spec.json` as a guide) specifying endpoints to verify.

### 3. Run the Deploy & Nurture Loop
Execute the orchestrator script to build, verify, and clean:
```bash
python3 vercel-deploy-nurture/scripts/deploy_nurture.py \
  --project-path "/path/to/your/vercel/project" \
  --spec-path "vercel-deploy-nurture/templates/health_check_spec.json" \
  --max-retries 3
```
*If successful, the script deploys to Vercel, passes health checks, and deletes `node_modules` locally.*
