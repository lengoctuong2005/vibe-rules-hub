---
name: motion
description: |
  Production-grade Motion and Interaction System for React/Next.js and Web apps. Covers motion foundations (physics springs, duration scales, reduced motion accessibility), copy-paste UI motion patterns (buttons, modals, toasts, staggered lists, page transitions), and advanced motion (gestures, drag & drop, SVG path drawing, kinetic typography, useAnimate sequences).
triggers:
  - "motion"
  - "animation"
  - "framer motion"
  - "motion react"
  - "gsap motion"
  - "ui animation"
  - "gestures"
license: MIT
metadata:
  origin: ECC
---

# Motion & Interaction Master System

Complete motion engineering framework uniting physics-based spring foundations, accessible UI interaction patterns, and advanced gesture/timeline orchestration for React, Next.js, and modern web applications.

---

## 1. Motion Foundations & Tokens

Motion must serve spatial continuity and reduce cognitive load. Never animate layout-triggering properties (`width`, `height`, `top`, `left`, `margin`, `padding`). Animate compositor-friendly properties exclusively: `transform` (`scale`, `x`, `y`, `rotate`) and `opacity`.

### Spring Physics & Duration Scales
- **Snappy Micro-Interaction**: `stiffness: 400, damping: 30` (Buttons, toggles, badges)
- **Smooth Surface Transition**: `stiffness: 260, damping: 25` (Modals, cards, dropdowns)
- **Gentle Fluid Flow**: `stiffness: 120, damping: 14` (Page transitions, ambient floating)

```typescript
// ponytail: Motion Token Constants - unified physics parameters
export const MOTION_SPRINGS = {
  snappy: { type: 'spring', stiffness: 400, damping: 30 },
  smooth: { type: 'spring', stiffness: 260, damping: 25 },
  gentle: { type: 'spring', stiffness: 120, damping: 14 },
} as const;

export const MOTION_DURATIONS = {
  fast: 0.15,
  normal: 0.25,
  slow: 0.45,
} as const;

export const MOTION_EASINGS = {
  outExpo: [0.16, 1, 0.3, 1],
  inOutQuad: [0.45, 0, 0.55, 1],
} as const;
```

### Accessibility: `prefers-reduced-motion`
Always provide a zero-duration or instant opacity fallback when the user prefers reduced motion:

```tsx
import { useReducedMotion, motion } from 'framer-motion';

export function FadeInCard({ children }: { children: React.ReactNode }) {
  const shouldReduceMotion = useReducedMotion();

  const variants = {
    hidden: { opacity: 0, y: shouldReduceMotion ? 0 : 16 },
    visible: { opacity: 1, y: 0 },
  };

  return (
    <motion.div
      initial="hidden"
      animate="visible"
      variants={variants}
      transition={shouldReduceMotion ? { duration: 0 } : MOTION_SPRINGS.smooth}
      className="p-6 rounded-xl bg-white dark:bg-neutral-900 shadow-sm border border-neutral-200 dark:border-neutral-800"
    >
      {children}
    </motion.div>
  );
}
```

---

## 2. Core UI Motion Patterns

### Staggered List Reveals
Stagger entry animations to establish natural visual hierarchy when loading lists or grids:

```tsx
// ponytail: Stagger Container & Item Variants
export const listContainerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: { staggerChildren: 0.06, delayChildren: 0.1 },
  },
};

export const listItemVariants = {
  hidden: { opacity: 0, y: 12 },
  visible: { opacity: 1, y: 0, transition: MOTION_SPRINGS.snappy },
};
```

### Modal Dialog Entrance & Exit (`AnimatePresence`)
```tsx
import { AnimatePresence, motion } from 'framer-motion';

export function Modal({ isOpen, onClose, children }: { isOpen: boolean; onClose: () => void; children: React.ReactNode }) {
  return (
    <AnimatePresence>
      {isOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={onClose}
            className="fixed inset-0 bg-black/50 backdrop-blur-xs"
          />
          <motion.div
            initial={{ opacity: 0, scale: 0.95, y: 8 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.95, y: 8 }}
            transition={MOTION_SPRINGS.smooth}
            className="relative z-10 w-full max-w-lg p-6 bg-white dark:bg-neutral-900 rounded-2xl shadow-xl"
          >
            {children}
          </motion.div>
        </div>
      )}
    </AnimatePresence>
  );
}
```

---

## 3. Advanced Gestures & Kinetic Sequences

### Swipe & Drag-to-Dismiss
- Use constraints (`dragConstraints={{ top: 0, bottom: 0 }}`) and elastic bounds (`dragElastic={0.2}`).
- Calculate velocity on drag end to trigger dismissal if flicked quickly.

### SVG Path Drawing & Morphing
- Animate `pathLength` from `0` to `1` with `strokeDashoffset` for checkmarks, progress rings, and animated illustrations.

### Imperative Timelines via `useAnimate`
```tsx
import { useAnimate } from 'framer-motion';

export function SequenceExample() {
  const [scope, animate] = useAnimate();

  const handleTrigger = async () => {
    await animate('button', { scale: 0.92 }, { duration: 0.1 });
    await animate('button', { scale: 1 }, { duration: 0.15 });
    await animate('.success-icon', { opacity: 1, scale: [0.5, 1.2, 1] }, { duration: 0.3 });
  };

  return (
    <div ref={scope}>
      <button onClick={handleTrigger} className="px-4 py-2 bg-blue-600 text-white rounded-lg">Execute</button>
      <span className="success-icon opacity-0 ml-2">✓</span>
    </div>
  );
}
```
