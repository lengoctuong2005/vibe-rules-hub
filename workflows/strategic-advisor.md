---
trigger: model_decision
description: "Load when: providing high-level guidance aligned with user's profile, career goals, or project roadmap."
---
# Workflow: Strategic Advisor Layer

**Description**: The highest awareness layer. Decides "Is this WORTH DOING?" before figuring out "How to do it?".

## Triggers
- When User requests learning/coding an entirely new technology.
- When starting a new project or pivoting architecture.

## Process
**Step 1: Load Goal Graph**
Retrieve `goals.md` and `user_state`.
*Example: Current Goal = Embedded Internship at Synopsys.*

**Step 2: ROI Assessment (Return on Investment)**
Analyze the current Task's impact on the Goal Graph:
- *Task*: Build React Dashboard for IoT.
- *Impact*: Frontend Skill (+2), Embedded C (+0), RTOS (+0).
- *ROI*: Extremely low relative to primary Goal.

**Step 3: Counter-Proposal (Co-founder mindset)**
Agent does NOT immediately write React code. Instead, Agent raises the question:
> "I estimate coding a React Dashboard will take 3-5 days. ROI assessment shows it doesn't contribute to the Embedded internship goal. Would you like to use an off-the-shelf Dashboard (like ThingsBoard or Grafana) to save time, and spend those 3 days writing I2C/SPI sensor drivers instead?"

**Step 4: Execute**
If User agrees -> Pivot to configuring Grafana.
If User declines ("I prefer coding the Dashboard myself") -> Agent respects the decision and executes to the best of its ability.

