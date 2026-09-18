---
name: frontend-engineering
description: |
  Comprehensive Frontend Engineering Master Skill unifying WCAG 2.2 accessibility, responsive design systems, distinct visual direction, React/Next.js component patterns, state management, performance optimization, and presentation slide deck engineering.
triggers:
  - "frontend engineering"
  - "frontend design"
  - "react patterns"
  - "nextjs frontend"
  - "ui a11y"
  - "frontend slides"
  - "web accessibility"
license: MIT
metadata:
  origin: ECC
---

# Frontend Engineering Master Skill

Comprehensive frontend engineering standards unifying semantic accessibility, visual direction, component patterns, web performance, and presentation deck engineering.

---

## 1. Accessibility Patterns (WCAG 2.2 AA/AAA)

Accessibility is foundational to production UI. Every interactive element must be keyboard operable, properly labeled, and compatible with assistive technology.

### Semantic Interactive Elements & Forms
- Always use native `<button>`, `<input>`, `<select>`, `<textarea>`, or `<a>` elements instead of clickable `<div>` or `<span>`.
- Associate every form control with an explicit `<label htmlFor="...">` or `aria-labelledby`.
- For visually hidden labels (e.g. icon buttons), provide `aria-label` or `.sr-only` span.

```tsx
// ponytail: Accessible Icon Button with native tooltip and sr-only label
interface IconButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  label: string;
  icon: React.ReactNode;
}

export function AccessibleIconButton({ label, icon, onClick, ...props }: IconButtonProps) {
  return (
    <button
      type="button"
      onClick={onClick}
      aria-label={label}
      title={label}
      className="inline-flex items-center justify-center p-2 rounded-lg hover:bg-neutral-100 dark:hover:bg-neutral-800 focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:outline-none transition-colors"
      {...props}
    >
      {icon}
      <span className="sr-only">{label}</span>
    </button>
  );
}
```

### Focus Management & Keyboard Navigation
- Interactive modal dialogs, drawers, and popovers must trap focus within the active overlay when opened.
- Restore focus to the triggering element when the overlay closes.
- Close overlays on `Escape` key press.

---

## 2. Visual Direction & Design Systems

Avoid generic template aesthetic. Apply deliberate styling decisions across typography, spacing scales, and color tokens.

### Typography Hierarchy & Spacing Rhythm
- Use a disciplined typographic scale (e.g., 12px, 14px, 16px, 20px, 24px, 32px, 48px).
- Enforce consistent line-heights ($1.2$ for headings, $1.5$ for body copy).
- Spacing must strictly follow a 4px base grid (`gap-1` = 4px, `gap-2` = 8px, `gap-4` = 16px, `gap-6` = 24px, `gap-8` = 32px).

### Design Tokens via CSS Variables
- Declare design tokens in CSS using modern `oklch` color spaces for uniform perceptual brightness.

```css
:root {
  --color-surface-bg: oklch(99% 0.005 240);
  --color-surface-card: oklch(100% 0 0);
  --color-surface-border: oklch(90% 0.01 240);
  --color-text-primary: oklch(15% 0.02 240);
  --color-text-secondary: oklch(45% 0.02 240);
  --color-accent: oklch(60% 0.22 250);
}

@media (prefers-color-scheme: dark) {
  :root {
    --color-surface-bg: oklch(12% 0.015 240);
    --color-surface-card: oklch(16% 0.02 240);
    --color-surface-border: oklch(24% 0.02 240);
    --color-text-primary: oklch(98% 0.005 240);
    --color-text-secondary: oklch(70% 0.015 240);
    --color-accent: oklch(68% 0.22 250);
  }
}
```

---

## 3. React & Next.js Component Patterns

### Composition Over Inheritance
- Use compound components and render props for complex reusable widgets (Accordions, Dropdowns, Tabs).
- Keep components focused and under 200 lines. Split container logic from presentational rendering.

```tsx
// ponytail: Compound Tabs - context-driven headless composition
import React, { createContext, useContext, useState } from 'react';

interface TabsContextValue {
  activeTab: string;
  setActiveTab: (tab: string) => void;
}

const TabsContext = createContext<TabsContextValue | null>(null);

export function Tabs({ defaultTab, children }: { defaultTab: string; children: React.ReactNode }) {
  const [activeTab, setActiveTab] = useState(defaultTab);
  return <TabsContext.Provider value={{ activeTab, setActiveTab }}>{children}</TabsContext.Provider>;
}

export function TabList({ children }: { children: React.ReactNode }) {
  return <div role="tablist" className="flex border-b border-neutral-200 dark:border-neutral-800">{children}</div>;
}

export function TabTrigger({ value, label }: { value: string; label: string }) {
  const ctx = useContext(TabsContext);
  if (!ctx) throw new Error('TabTrigger must be used inside Tabs');
  const isActive = ctx.activeTab === value;

  return (
    <button
      role="tab"
      aria-selected={isActive}
      onClick={() => ctx.setActiveTab(value)}
      className={`px-4 py-2 text-sm font-medium border-b-2 transition-colors ${
        isActive ? 'border-blue-600 text-blue-600 dark:text-blue-400' : 'border-transparent text-neutral-500 hover:text-neutral-800'
      }`}
    >
      {label}
    </button>
  );
}

export function TabPanel({ value, children }: { value: string; children: React.ReactNode }) {
  const ctx = useContext(TabsContext);
  if (!ctx || ctx.activeTab !== value) return null;
  return <div role="tabpanel" className="p-4">{children}</div>;
}
```

---

## 4. Performance & Core Web Vitals

- **LCP (Largest Contentful Paint)**: Preload hero media, use responsive `srcset` and `next/image` with `priority` for above-the-fold imagery.
- **CLS (Cumulative Layout Shift)**: Always set explicit `width` and `height` (or `aspect-ratio`) on images, videos, and embedded canvas widgets.
- **INP (Interaction to Next Paint)**: Keep JavaScript execution on the main thread short; defer heavy computation with Web Workers or `useTransition`.

---

## 5. Presentation Slide Decks & Interactive Talk Engineering

Engineering responsive, interactive presentation decks using web standards:
- **16:9 Viewport Scaling**: Use CSS container queries and `clamp()` to scale typography and layout seamlessly from mobile previews to 4K projectors.
- **Slide Navigation**: Implement keyboard listeners (`ArrowRight`, `ArrowLeft`, `Space`, `Backspace`) with smooth CSS scroll-snap or transforms.
- **Presenter Notes**: Use a secondary display sync channel (via `BroadcastChannel` API) for presenter view with timers and markdown speaker notes.
