---
name: vercel-deploy-nurture
description: Enterprise Vercel deployment, health check, and disk cleanup loop. Automates pushing builds to Vercel, auditing build error logs, self-repairing code bugs, verifying URL status codes, and removing node_modules.
---

# 🚀 Vercel Deploy & Nurture Loop: Continuous Delivery Agent Skill

This skill allows an agent to run an autonomous deployment and verification loop for Vercel projects. It builds or deploys code via the Vercel CLI, monitors remote build logs, automatically analyzes and patches compilation errors (like TypeScript type conflicts), runs post-deployment endpoint health checks, and finally deletes local `node_modules` folders to reclaim disk space.

---

## 🔁 Execution Flow

```
                      ┌─────────────────────────────┐
                      │     1. Trigger Deploy       │
                      │     (vercel deploy --pre)   │
                      └──────────────┬──────────────┘
                                     │
                      ┌──────────────▼──────────────┐
                      │ 2. Check Build Logs/Status  │
                      └──────────────┬──────────────┘
                                     │
                                     ├────────────────────────┐
                      ┌──────────────▼──────────────┐         │ (build fails)
                      │      3. Build Clean?        │         │
                      └──────────────┬──────────────┘         │
                                     │ (yes, build passes)    │
                      ┌──────────────▼──────────────┐         │
                      │   4. Run Health Checks on   │         │
                      │       Deployment URL        │         │
                      └──────────────┬──────────────┘         │
                                     │ (checks pass)          │
                      ┌──────────────▼──────────────┐         │
                      │   5. Clean Disk Space       │◄────────┘ (Self-Repair
                      │    (rm -rf node_modules)    │            Code & Retry)
                      └─────────────────────────────┘
```

---

## 🛠️ Step-by-Step Instructions

### Step 1: Trigger Vercel Build/Deployment
1. Make sure you are logged into Vercel CLI.
2. Run a preview or production deployment:
   ```bash
   vercel deploy --yes > vercel_output.log
   ```
3. Extract the target deployment preview URL from the log output.

### Step 2: Check Logs & Troubleshoot
1. If the Vercel CLI returns a build failure or non-zero exit code, retrieve the Vercel remote build logs:
   ```bash
   vercel logs <deployment-url-or-project-id> > build_errors.log
   ```
2. **Self-Repair Loop**: Search the log for:
   - TypeScript compiler errors (e.g. `Type 'X' is not assignable to type 'Y'`).
   - Missing dependencies or incorrect imports.
   - Syntax errors in serverless functions.
3. Apply code modifications to resolve the errors, rebuild locally to confirm, and return to Step 1.

### Step 3: Post-Deploy Health Check
1. Once Vercel deploys successfully, load the endpoint targets specification from `templates/health_check_spec.json`.
2. Run the `deploy_nurture.py` validation checks on the target URL (checking for HTTP 200/301, latency, and JSON body structures).
3. If endpoints fail or return HTTP 500, check function logs via `vercel logs`, apply patches, and redeploy.

### Step 4: Clean Disk Space (Disk Nurturing)
1. After verifying a successful build and healthy deployment, reclaim local disk space.
2. Run the cleanup utility to delete the heavy node module dependencies:
   ```bash
   rm -rf node_modules .next
   ```
3. Confirm that the local repository is clean and ready for storage.
