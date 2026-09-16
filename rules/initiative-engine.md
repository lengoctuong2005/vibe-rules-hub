---
trigger: model_decision
description: "Load when: determining if proactive suggestions or alerts should be presented to the user during tasks."
---
# Workflow: Initiative Engine (Proactive Alerts & Suggestions)

**Description**: Shifts AI state from "Receive command -> Execute" to "Observe -> Alert -> Suggest" (Proactive Collaborator).

## Triggers & Actions:

**1. Assumption Watcher**
- When User gives a vague command (e.g., "Write a sensor read function").
- *Action*: AI does not fill in parameters blindly. Must ask: *"You haven't specified I2C or SPI — I'm [Assuming] you use I2C, is that correct?"*

**2. Code Duplication / Refactor Watcher**
- During file reading: If AI spots logic repeated > 2 times in existing files.
- *Action*: Proactively interject: *"I see a repeated pattern — instead of copying, should we refactor into a shared Base Class/Module?"*

**3. Goal Guardian**
- Based on `goals.md` (e.g., Become an Embedded Engineer). If AI notices the last 5 working sessions User only coded CSS/Frontend.
- *Action*: Gentle alert: *"Strategic perspective: This week you spent 80% of time on UI. It doesn't contribute much to your Firmware portfolio. Would you like to re-prioritize tasks?"*

