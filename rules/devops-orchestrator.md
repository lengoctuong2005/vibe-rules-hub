---
trigger: model_decision
description: "Workflow: DevOps Orchestrator - Load when implementing deployment, managing servers, or pipelines."
---

# Workflow: DevOps Orchestrator (Infrastructure Router)

**MANDATE**: Automate everything. Do not trust manual server setups. Treat infrastructure as code (IaC).

When receiving tasks related to Infrastructure, Deployment, or Pipelines, the Agent MUST follow this cycle:

## Step 1: Environment Standardization (Containerization)
- All applications should run inside containers.
- Load skill: `docker-patterns`.
- Ensure multi-stage builds are used in Dockerfile to minimize image sizes. Avoid running containers as the `root` user.

## Step 2: Secret Scanning & Safety Check (Mandatory Pre-Commit)
- BẮT BUỘC chạy `python scripts/safety_guard.py --scan-file .` trước khi commit hoặc build image để tránh lộ key, token, credentials.
- Sử dụng Worktree Isolation (git worktree) nếu cần thiết để build và deploy mà không ảnh hưởng tới branch đang làm việc chính.

## Step 3: Pipeline Automation (CI/CD)
- Load skill: `github-actions`, `continuous-agent-loop`, or related CI/CD pattern.
- The pipeline must contain at least 3 jobs: `Lint` -> `Test` -> `Build/Push`.

## Step 4: Deployment
- If using Kubernetes: Load `kubernetes-patterns`.
- If using bare servers: Load `terminal-ops`, `nginx-setup`.
- **Concurrency Guard**: If the deployment involves shared infrastructure state (e.g. Terraform state, shared K8s namespaces), acquire a lock using `python scripts/lock_manager.py --acquire deploy_lock` before executing the deployment, and release it after.
- Ensure zero-downtime deployment patterns are implemented.

## Step 5: Monitoring & Networking
- Load skill: `homelab-network-readiness`, `network-config-validation` to configure network and DNS parameters.
- Insert log collectors and health checks for the target application.

---
*Note: Never hardcode secrets in Dockerfiles or deployment manifests. Always instruct the user to configure secrets inside Git Repository variables.*
