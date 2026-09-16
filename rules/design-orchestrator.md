---
trigger: model_decision
description: "Workflow: Design Orchestrator - Load when implementing web UI/UX layouts, frontend components, or evaluating design. Manages selection from 300+ Design Systems & Templates."
---

# Workflow: Design Orchestrator (Frontend Design Router)

**MANDATE**: Never write user interfaces from scratch without referencing a verified Design System or structural Template. Visual excellence and premium aesthetics are non-negotiable.

When receiving tasks related to UI/UX or Frontend presentation, the Agent MUST follow this cycle:

## Step 1: Identify Brand Vibe & Styling Mappings
- Ask the user: *"Which brand design style do you want to target? (e.g. Apple, Stripe, Linear, Vercel, Notion...)"*
- Load the corresponding design rules: `view_file` the file `~/.gemini/antigravity/skills/design-systems/[brand-name]/DESIGN.md`.
- Extract color palettes, typography hierarchies, layout spacing scales, and corner radii rules.

## Step 2: Select Structural Layout Template
- Identify target layout components (e.g., Dashboard, Landing Page, Blog, Pricing page) by running `list_dir` on `~/.gemini/antigravity/skills/design-templates/`.
- Load the corresponding template rules (e.g. `design-templates/dashboard/SKILL.md`).
- Implement the HTML/DOM layout structure of the template, populating it with the user's actual data.

## Step 3: Load Core UI Skills (Frontend Libraries)
If the design requires specialized frontend capabilities, load the specific files under `~/.gemini/antigravity/skills/open-design/`:
- **UI & UX Mechanics**: Load `ui-ux-pro-max` or `frontend-design`.
- **UI Libraries**: If building with React and Tailwind, load `shadcn-ui`.
- **Data Visualization**: If charts or graphs are present, load `d3-visualization`.

## Step 4: Integrate Motion & Micro-interactions (Animations)
- Interfaces without transitions feel static. Micro-interactions are mandatory.
- Load `emilkowalski-motion` for smooth hover, focus, and layout transitions.
- Load the `gsap-core` and `gsap-scrolltrigger` packages if advanced scroll-linked timeline animations are requested.

## Quality Gate Checklist
Before reporting completion, the agent must run `/polish` (or load the `impeccable-design-polish` skill) to verify:
1. **WCAG Contrast**: Text contrast ratios meet accessibility standards.
2. **Spacing consistency**: Margins and paddings adhere strictly to a base-4 grid (4px, 8px, 16px, 24px, 32px).
3. **Typography Hierarchy**: Font weights and sizes cleanly differentiate H1, H2, H3, and Body copy.

---
*Note for Agent: Never load all 300+ skills at once. Limit loading to 1 Design System + 1 Structural Template + 1 Motion Skill per session.*
