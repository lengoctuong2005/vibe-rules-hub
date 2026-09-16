---
trigger: model_decision
description: "MASTER ROUTER - First entry point for planning any task. Outlines domains and points to correct Orchestrators."
---

# THE GRAND LIBRARY MAP (Antigravity Global Router)

**MANDATE**: The system contains >780 rules, skills, design systems, and templates. AI MUST NOT load files randomly. When starting a task, the AI must determine the target "Domain" and ONLY load the corresponding Orchestrator or skills.

---

## The Librarian Rule (Step-by-Step execution)
1. Receive request → Match target Domain below.
2. Load corresponding Orchestrator/skills.
3. Follow the Orchestrator guidelines → Load specific Skills/Templates.
4. **Never load the entire library. Load at most 3-5 skills per task.**

---

## Domain 1: Interface & User Experience (UI / UX / Frontend)
- **Keywords**: Web design, landing page, CSS, animation, GSAP, UI components, React/Vue/Nextjs, Tailwind, responsive design.
- **Orchestrator**: `~/.config/opencode/agents/workflows/design-orchestrator.md`
- **Resource Folders**:
  - `skills/open-design/` (e.g. frontend-design, gsap-core, shadcn-ui, ui-ux-pro-max)
  - `design-systems/` (e.g. apple, stripe, linear, vercel)
  - `design-templates/` (e.g. dashboard, landing, blog, pricing)

## Domain 2: Core Logic & Databases (Backend / Architecture)
- **Keywords**: API, Database, Prisma, SQL, Schema, Microservices, Python, Node.js, Authentication, REST, GraphQL.
- **Orchestrator**: `~/.config/opencode/agents/workflows/backend-orchestrator.md`
- **Resource Folders**:
  - `skills/backend/` (api-design, database-migrations, event-driven-architecture, grpc-microservices)
  - `skills/ecc-extracted/` (nestjs-patterns, django-patterns, fastapi-patterns, laravel-patterns, springboot-patterns, postgres-patterns, prisma-patterns, redis-patterns, mysql-patterns, error-handling)

## Domain 3: Deployment & Infrastructure (DevOps / SRE)
- **Keywords**: Docker, CI/CD, Github Actions, Nginx, AWS, Cloud, Kubernetes.
- **Orchestrator**: `~/.config/opencode/agents/workflows/devops-orchestrator.md`
- **Resource Folders**:
  - `skills/devops/` (kanban-orchestrator, kanban-worker)
  - `skills/ecc-extracted/` (docker-patterns, kubernetes-patterns, deployment-patterns, github-ops, git-workflow, terminal-ops)
  - `skills/ecc-extracted/` (homelab-network-*, network-config-validation, network-bgp-diagnostics)

## Domain 4: Security & Debugging
- **Keywords**: Debugging, runtime errors, memory leaks, authentication, permission audits, code review, security scans.
- **Orchestrator**: `~/.config/opencode/agents/workflows/security-audit.md` or `~/.config/opencode/agents/workflows/debug.md`
- **Resource Folders**:
  - `skills/performing-*-cybersecurity-assessment/` (Oil & Gas, Power Grid, Maritime, Transportation, etc.)
  - `skills/analyzing-*/` (APT groups, Active Directory ACL, Docker forensics, DNS exfiltration, Cobalt Strike profiles)
  - `skills/ecc-extracted/` (security-review, security-scan, security-bounty-hunter, hipaa-compliance, systematic-debugging)
  - `skills/workflows/` (audit_and_fix, deep-review)

## Domain 5: AI / ML / Agent (Artificial Intelligence & Orchestration)
- **Keywords**: LLM, Agent, Prompt Engineering, Training, Evaluation, MetaGPT, AutoGPT, SkillSpector, Multi-Agent.
- **Orchestrator**: `~/.config/opencode/rules/multi-agent-coordination.md`
- **Resource Folders**:
  - `MetaGPT/` (Software Company simulation, multi-agent roles)
  - `SkillSpector/` (Agent skill verification and testing framework)
  - `skills/autonomous-ai-agents/` (claude-code, codex, hermes-agent, opencode)
  - `skills/agent-reach/` (Advanced web scraping and context building)
  - `skills/evaluation/`
  - `skills/inference/`
  - `skills/mlops/`
  - `skills/models/`

## Domain 6: Code Quality & Tech Debt (Code Review)
- **Keywords**: Code review, tech debt, refactoring, code quality, PR analysis.
- **Orchestrator**: None (AI self-references the skills below)
- **Resource Folders**:
  - `skills/ponytail/` (ponytail-audit, ponytail-debt, ponytail-review, ponytail-gain)
  - `agents/` (code-reviewer, code-simplifier, silent-failure-hunter, pr-test-analyzer)

## Domain 7: Research & Documentation
- **Keywords**: Writing reports, academic papers, documentation search, data analysis, summarizing info.
- **Orchestrator**: None (AI self-references the skills below)
- **Resource Folders**:
  - `skills/research/` (arxiv, blogwatcher, llm-wiki, polymarket, research-paper-writing)
  - `skills/ecc-extracted/` (deep-research, literature-review, data-report, research-decision-room)

## Domain 8: IoT & Hardware (Firmware / Embedded / PCB)
- **Keywords**: Firmware, C/C++, RTOS, PCB, Quartus, FPGA, Bootloader, OTA, kernel, hardware.
- **Orchestrator**: None (AI self-references the skills below)
- **Resource Folders**:
  - `skills/iot-hardware/` (firmware-baremetal, hil-testing, kernel-debugging, ota-bootloader, pcb-design-review, rtos-concurrency)

## Domain 9: Mobile & Desktop App
- **Keywords**: iOS, Android, Swift, Kotlin, Flutter, React Native, Desktop applications.
- **Orchestrator**: None (AI self-references the skills below)
- **Resource Folders**:
  - `skills/apple/` (apple-notes, apple-reminders, findmy, imessage, macos-computer-use)
  - `skills/ecc-extracted/` (android-clean-architecture, swift-concurrency-6-2, swiftui-patterns, dart-flutter-patterns, compose-multiplatform-patterns, kotlin-patterns, mobile-app, mobile-onboarding)

## Domain 10: Creative Content
- **Keywords**: Writing articles, marketing copy, infographics, posters, video editing, presentation slides.
- **Orchestrator**: None (AI self-references the skills below)
- **Resource Folders**:
  - `skills/creative/` (architecture-diagram, ascii-art, baoyu-infographic, claude-design, excalidraw, hand-drawn-diagrams, manim-video, p5js, sprite-animation, video-editing)
  - `skills/open-design/` (copywriting, marketing-psychology, poster-hero, social-reddit-card, social-spotify-card, social-x-post-card, resume-modern, release-notes-one-pager)

---

## Fallback Plan (Unknown Domain)
If the task does not match any Domain:
1. Search the `RULES_MANIFEST.md` index using keywords.
2. Run `list_dir` on `~/.config/opencode/agents/skills/` to find similar capability titles.
3. If no match is found, alert the user and proceed with internal knowledge.

## System Statistics (Updated 2026-06-29)
- Rules: 18
- Workflows: 25
- Skills (SKILL.md): >760 (Includes Anthropic CyberSecurity, Ponytail, Open Design, Hermes)
- Design Systems (DESIGN.md): 150
- Design Templates: 109
- Memory Files: 24
- **Total Resources**: **>1100**