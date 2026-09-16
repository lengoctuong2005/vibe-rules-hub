---
trigger: load_on_demand
description: "Dead-End Recovery - Strategic failure protocol. After 3 failed patches, stop coding, zoom out to architecture level, and offer rollback."
---
# Dead-End Recovery (Giao thức Thoát Khỏi Ngõ Cụt)

## Purpose
When local fixes repeatedly fail, force the AI to stop, zoom out to a higher abstraction level, and offer a clean rollback.

## Trigger
Load when 3+ fix attempts on the same issue fail, or when confidence drops below 30%.

## Protocol

### 1. Dead-End Detection
If 3 patches have been proposed and all failed:
- STOP WRITING CODE.
- Declare: `[DEAD END REACHED] Local approaches are not resolving this issue.`

### 2. Zoom-Out Thinking
Shift from Code level (micro) to Architecture or Environment level (macro).
Ask the User 3 diagnostic questions:
1. "Has anything changed in the environment recently (dependencies, OS, runtime version)?"
2. "Is this issue reproducible in a clean environment (different machine, fresh install)?"
3. "Would a workaround (different approach entirely) be acceptable while we investigate?"

### 3. Rollback Offer
Propose reverting to the last known good state:
- `git stash` to save current work
- `git reset --hard <last_good_commit>` to revert
- Or `git checkout -b debug/<issue>` to isolate the investigation

Present these options and let the User choose.

### 4. Alternative Strategy
After rollback, propose a fundamentally different approach:
- If fixing at the application level failed, investigate infrastructure.
- If fixing logic failed, investigate data.
- If fixing code failed, investigate configuration.

### 5. Escalation
If the alternative strategy also fails, recommend:
- Filing an issue with the library/framework maintainer.
- Seeking input from a domain expert.
- Accepting the limitation and documenting a known issue.
