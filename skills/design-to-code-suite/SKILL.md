---
name: design-to-code-suite
description: |
  Design to Code Master Suite translating visual design tokens and layout architectures into pristine code. Integrates 150+ Design Systems (Apple, Stripe, Linear, Vercel, Neo-Brutalism, Bento Grid), 109 layout templates, W3C Design Tokens JSON, fluid CSS clamp() typography & spacing, GSAP 60fps compositor animations, and WCAG AAA accessibility with dedicated subagents (a11y-architect, react-reviewer, code-simplifier).
triggers:
  - "design-to-code"
  - "design suite"
  - "design-to-code-suite"
  - "design systems"
  - "apple stripe linear design"
  - "gsap animations"
  - "wcag accessibility"
license: MIT
metadata:
  origin: ECC
---

# Design to Code Master Suite

Comprehensive UI/UX translation engine converting design system specifications, tokens, and structural layout templates into production code.

---

## 1. Supported Design Systems (150+)

| Design System Category | Exemplar Brands | Key Visual Signatures |
|------------------------|-----------------|-----------------------|
| **Dark Luxury & Tech** | Apple, Linear, Arc, Raycast | Deep monochrome backgrounds, translucent glassmorphism (`backdrop-blur`), electric hairline borders (`border-white/10`) |
| **Fintech & Mesh Gradients** | Stripe, Ramp, Brex | Multi-color animated mesh gradients, crisp 4px grid spacing, elevated soft shadows |
| **Minimalist Engineering** | Vercel, Supabase, Cloudflare | High-contrast black/white, geometric monospaced accents, clean data tables |
| **Neo-Brutalism** | Gumroad, Retool, Figma Blog | Bold 2px black borders, sharp 4px hard drop shadows, saturated pop accents |
| **Bento & Editorial** | Apple Events, Notion, Framer | Asymmetric grid cards, varied aspect ratios, fluid typography (`clamp()`) |

---

## 2. W3C Design Tokens Schema & OKLCH Color Model

Colors are defined using OKLCH color space for uniform perceptual lightness across light and dark modes:

```json
{
  "color": {
    "brand": {
      "primary": {
        "value": "oklch(0.65 0.22 260)",
        "type": "color",
        "description": "Primary brand accent token"
      },
      "surface": {
        "value": "oklch(0.98 0.01 250)",
        "type": "color"
      }
    }
  },
  "spacing": {
    "base": { "value": "4px", "type": "dimension" },
    "section": { "value": "clamp(3rem, 2rem + 4vw, 8rem)", "type": "dimension" }
  }
}
```

---

## 3. Fluid Layout & Typography Engine

Eliminate abrupt breakpoint jumps by computing continuous fluid scales:

$$\text{CSS Clamp Value} = \text{clamp}(V_{\min}, \text{base} + \text{rate} \times \text{viewport width}, V_{\max})$$

```css
:root {
  /* Fluid Text Scaling (16px at 320px width -> 18px at 1440px width) */
  --text-body: clamp(1rem, 0.95rem + 0.25vw, 1.125rem);

  /* Fluid Heading Scaling (32px at 320px width -> 60px at 1440px width) */
  --text-display: clamp(2rem, 1.25rem + 3.75vw, 3.75rem);

  /* Fluid Section Spacing (48px -> 128px) */
  --space-section: clamp(3rem, 1.5rem + 7.5vw, 8rem);
}
```

---

## 4. Compositor-Only Motion (GSAP 60fps)

To prevent main-thread layout thrashing, animations are restricted to hardware-accelerated compositor properties:

```typescript
// components/AnimatedSurfaceCard.tsx
'use client';

import React, { useRef } from 'react';
import gsap from 'gsap';

export function AnimatedSurfaceCard({ children }: { children: React.ReactNode }) {
  const cardRef = useRef<HTMLDivElement>(null);

  // ponytail: GPU compositor hover tilt - purely on transform/opacity
  const handleMouseEnter = () => {
    gsap.to(cardRef.current, {
      scale: 1.02,
      y: -4,
      duration: 0.3,
      ease: 'power2.out',
    });
  };

  const handleMouseLeave = () => {
    gsap.to(cardRef.current, {
      scale: 1,
      y: 0,
      duration: 0.3,
      ease: 'power2.inOut',
    });
  };

  return (
    <div
      ref={cardRef}
      onMouseEnter={handleMouseEnter}
      onMouseLeave={handleMouseLeave}
      className="p-6 rounded-2xl bg-white dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800 shadow-sm transition-colors will-change-transform"
    >
      {children}
    </div>
  );
}
```

---

## 5. WCAG AAA Accessibility Standards

1. **Color Contrast**: Minimum $7:1$ for normal body text, $4.5:1$ for large text ($\ge 18\text{pt}$ or $\ge 14\text{pt}$ bold).
2. **Focus Visibility**: Custom high-visibility focus indicators (`focus-visible:ring-2 focus-visible:ring-offset-2`).
3. **Motion Sensitivity**: Automatically suppress GSAP animations when `prefers-reduced-motion: reduce` is active.

---

## 6. Subagent Quality Matrix

| Subagent | Responsibility | Pass Criteria |
|----------|----------------|---------------|
| `a11y-architect` | Accessibility verification, contrast math, ARIA landmark checks | 100% WCAG 2.2 AAA contrast compliance |
| `react-reviewer` | Layout shifts (CLS), component decomposition, hydration safety | 0 CLS layout shifts, clean RSC boundaries |
| `code-simplifier` | Ponytail CSS minimalism, token consolidation | Zero duplicate CSS rules or dead classes |

---

## 7. Verification Checklist

```bash
# 1. Automated Accessibility Audit (Axe / Lighthouse)
pnpm axe-core-check

# 2. CSS & Token Linting
pnpm stylelint "src/**/*.css"

# 3. Secret scan
python scripts/safety_guard.py --scan-file .
```
