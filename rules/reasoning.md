---
trigger: always_on
description: >
  Load when: the user asks to debug code, diagnose errors, analyze system crashes,
  design system architecture, choose between technical options, evaluate pros/cons (trade-offs),
  or perform root-cause analysis (mechanistic understanding).
  Contains: 12-layer thinking pipeline (surface, intent, assumption, info, hypothesis, evidence,
  falsification, recursive, solution, cascade, uncertainty, meta), 4-critic simulation
  (performance, security, maintainability, cost), 4-pass reliability check, red flags,
  differential diagnosis, Bayesian updating, and trade-off tables.
  Do NOT load for: simple code edits, file formatting, UI adjustments, or trivial operations.
---
# Reasoning & Diagnosis Engine

## 1. Red Flag Detector
When reading code/requirements, scan for Red Flags. Stop immediately if detected:
- "RTOS with ISR > 50 lines" → RED FLAG.
- "Solo dev trying to build 20 Microservices" → RED FLAG.

## 2. Diagnostic Pipeline (Scientific Method)
1. **Observation**: Identify Symptoms and Weak Signals (e.g., 3% CPU increase).
2. **Differential Diagnosis**: List 3-4 probable Root Causes with probability (%). Never blame a single cause.
3. **Experiment Design**: Propose isolation tests to eliminate hypotheses. Never guess blindly.
4. **Evidence Collection**: Only trust Measurement/Logs, not feelings.
5. **Bayesian Updating**: When user provides new evidence, update probabilities immediately.
6. **Conclusion**: Trace `Symptom → Mechanism → Root Cause`. Explain at the physical/logic layer.

## 3. Deep Thinking Pipeline (12-Layer Filter)
Every reasoning chain must pass through:
1. [SURFACE]: Literal meaning of the request
2. [INTENT]: Real problem the user wants solved
3. [ASSUMPTION]: Dig out hidden assumptions (e.g., "optimize faster" = reduce Latency or increase Throughput?)
4. [INFORMATION]: Check information gaps
5. [HYPOTHESIS]: Generate at least 3 hypotheses (no Tunnel Vision)
6. [EVIDENCE]: Filter by evidence (only Measurement/Logs)
7. [FALSIFICATION]: Try to disprove your own hypothesis
8. [RECURSIVE (5 Whys)]: Keep asking why
9. [SOLUTION]: Propose solution
10. [CASCADE]: Evaluate consequences at order 1, 2, 3
11. [UNCERTAINTY]: Quantify risk
12. [META]: Self-check for bias

## 4. Adversarial Reasoning (4-Critic Simulation)
Before finalizing architecture decisions, silently run 4 critics:
1. **Performance Critic**: CPU/Memory bottleneck?
2. **Security & Reliability Critic**: Race Condition? Single Point of Failure?
3. **Maintainability Critic**: Readable? Maintainable in 2 years?
4. **Cost & Opportunity Critic**: Is there a dumb-but-sufficient approach that saves 3 days?

Present the balanced solution from all 4 perspectives.

## 5. Multi-Pass Reliability (4-Pass Pipeline)
No single-pass answers for non-trivial tasks:
1. **Generate & Assume**: Build rough solution, list all [ASSUMPTION]s explicitly
2. **Self-Critique**: Break assumptions, play Critic Agent, find security/memory/logic errors
3. **Reality Check**: What could make this fail? Fits user's resources and deadline?
4. **Final Polish**: Attach confidence label (e.g., `[Confidence: 90% - verified via datasheet]`)

## 6. Trade-off Engine
Never say "The best solution is...". Every solution must include a Trade-off table:
- Example: Rust (High safety, Steep learning) vs C (High performance, Memory leak risk)

## 7. Second-Order Thinking
Don't stop at direct impact:
- Order 1: Using Queue → Code is easier
- Order 2: Queue consumes heap RAM
- Order 3: Insufficient heap → silent crashes under load → Propose Static Allocation
