---
name: design-to-code-suite
description: |
  Master Design-to-Code Suite for transforming Figma designs and Design Token Community Group (DTCG) tokens into production React component systems, Tailwind CSS v4 design tokens, fluid typography, GSAP micro-interactions, WCAG 2.2 AAA accessibility, and visual regression pipelines.
triggers:
  - "design-to-code"
  - "design-to-code-suite"
  - "design tokens"
  - "figma to code"
  - "component system"
  - "ui polish"
license: MIT
metadata:
  origin: ECC
---

# Design to Code Master Suite

Comprehensive framework for translating design artifacts into production-grade, accessible, and responsive component libraries with automated visual quality controls.

---

## 1. System Architecture Topology

```
+─────────────────────────────────────────────────────────────────────────+
|                        FIGMA DESIGN & DTCG TOKENS                       |
|  Color Palette (oklch) · Spacing Scale · Fluid Typography · Elevations   |
+────────────────────────────────────┬────────────────────────────────────+
                                     │ Automated Token Sync
                                     ▼
+─────────────────────────────────────────────────────────────────────────+
|                       CSS TOKEN & THEME COMPILER                        |
|  Tailwind CSS v4 @theme · CSS Custom Properties · Dark/Light Themes     |
+────────────────────────────────────┬────────────────────────────────────+
                                     │
                  ┌──────────────────┴──────────────────┐
                  ▼                                     ▼
+──────────────────────────────────┐  +───────────────────────────────────+
|    HEADLESS ACCESSIBLE CORE      |  |         MOTION & CHOREOGRAPHY     |
|  Radix UI / Ark UI Primitives    |  |  GSAP Timelines (60/120fps)       |
|  Keyboard Traps & ARIA Roles     |  |  prefers-reduced-motion Handling  |
+─────────────────┬────────────────┘  +─────────────────┬─────────────────+
                  │                                     │
                  └──────────────────┬──────────────────┘
                                     │
                                     ▼
+─────────────────────────────────────────────────────────────────────────+
|                      PRODUCTION COMPONENT SYSTEM                        |
|  Compound React 19 Components · Strict Props Interface · Zero Overheads|
+────────────────────────────────────┬────────────────────────────────────+
                                     │
                                     ▼
+─────────────────────────────────────────────────────────────────────────+
|                     VISUAL REGRESSION QUALITY GATE                      |
|  Playwright Multi-Breakpoint Snapshots · Pixel Diff Threshold < 0.1%    |
+─────────────────────────────────────────────────────────────────────────+
```

---

## 2. Fluid Typography & Design Tokens Setup

```css
/* src/styles/tokens.css */
:root {
  /* Colors in oklch */
  --color-canvas: oklch(0.99 0.002 240);
  --color-card: oklch(0.97 0.005 240);
  --color-border: oklch(0.90 0.01 240);
  --color-text-main: oklch(0.15 0.02 240);
  --color-brand: oklch(0.60 0.24 265);

  /* Fluid typography */
  --text-xs: clamp(0.75rem, 0.7rem + 0.25vw, 0.875rem);
  --text-base: clamp(1rem, 0.95rem + 0.25vw, 1.125rem);
  --text-xl: clamp(1.25rem, 1.15rem + 0.5vw, 1.5rem);
  --text-hero: clamp(2.5rem, 2rem + 2.5vw, 4.5rem);

  /* Shadows */
  --shadow-subtle: 0 1px 3px 0 rgb(0 0 0 / 0.05), 0 1px 2px -1px rgb(0 0 0 / 0.05);
  --shadow-float: 0 10px 25px -5px rgb(0 0 0 / 0.08), 0 8px 10px -6px rgb(0 0 0 / 0.05);
}

[data-theme="dark"] {
  --color-canvas: oklch(0.12 0.01 240);
  --color-card: oklch(0.18 0.015 240);
  --color-border: oklch(0.28 0.02 240);
  --color-text-main: oklch(0.96 0.005 240);
  --color-brand: oklch(0.68 0.22 265);
}
```

---

## 3. Accessible Dialog Compound Component

```tsx
// src/components/ui/Dialog.tsx
import React, { createContext, useContext, useState, useEffect } from 'react';

interface DialogContextType {
  isOpen: boolean;
  setIsOpen: (open: boolean) => void;
}

const DialogContext = createContext<DialogContextType | undefined>(undefined);

export function DialogRoot({ children }: { children: React.ReactNode }) {
  const [isOpen, setIsOpen] = useState(false);
  return (
    <DialogContext.Provider value={{ isOpen, setIsOpen }}>
      {children}
    </DialogContext.Provider>
  );
}

export function DialogTrigger({ children }: { children: React.ReactElement }) {
  const context = useContext(DialogContext);
  if (!context) throw new Error('DialogTrigger must be used within DialogRoot');

  return React.cloneElement(children, {
    onClick: () => context.setIsOpen(true),
    'aria-haspopup': 'dialog',
    'aria-expanded': context.isOpen,
  });
}

// ponytail: Accessible Modal Overlay with Escape key listener
export function DialogContent({ children }: { children: React.ReactNode }) {
  const context = useContext(DialogContext);
  if (!context) throw new Error('DialogContent must be used within DialogRoot');

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape') context.setIsOpen(false);
    };
    if (context.isOpen) {
      window.addEventListener('keydown', handleKeyDown);
      document.body.style.overflow = 'hidden';
    }
    return () => {
      window.removeEventListener('keydown', handleKeyDown);
      document.body.style.overflow = 'unset';
    };
  }, [context.isOpen]);

  if (!context.isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm">
      <div
        role="dialog"
        aria-modal="true"
        className="w-full max-w-lg rounded-2xl bg-card p-6 shadow-float border border-border"
      >
        {children}
      </div>
    </div>
  );
}
```

---

## 4. Accessible Dropdown Menu Compound Component

```tsx
// src/components/ui/Dropdown.tsx
import React, { useState, useRef, useEffect } from 'react';

export function DropdownMenu({ trigger, items }: { trigger: React.ReactNode; items: Array<{ label: string; onClick: () => void }> }) {
  const [open, setOpen] = useState(false);
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (containerRef.current && !containerRef.current.contains(event.target as Node)) {
        setOpen(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  return (
    <div className="relative inline-block text-left" ref={containerRef}>
      <button onClick={() => setOpen(!open)} className="btn-secondary" aria-expanded={open}>
        {trigger}
      </button>
      {open && (
        <div className="absolute right-0 mt-2 w-48 rounded-xl bg-card p-1 shadow-float border border-border z-50">
          {items.map((item, idx) => (
            <button
              key={idx}
              onClick={() => { item.onClick(); setOpen(false); }}
              className="w-full text-left px-3 py-2 text-sm rounded-lg hover:bg-brand/10 transition-colors"
            >
              {item.label}
            </button>
          ))}
        </div>
      )}
    </div>
  );
}
```

---

## 5. Subagent Delegation Matrix

| Subagent | Role & Objective | Deliverable |
|----------|------------------|-------------|
| `design-token-parser` | DTCG token parsing to Tailwind v4 CSS | `tokens.css` |
| `component-architect` | Headless, accessible compound UI components | Component library |
| `ui-polish-reviewer` | Spacing grid consistency & GSAP micro-motion | Animation polish |
| `accessibility-auditor` | WCAG 2.2 AAA contrast & keyboard navigation | A11y report |
| `visual-regression-runner`| Playwright visual diffs across screen sizes | Visual test suite |
