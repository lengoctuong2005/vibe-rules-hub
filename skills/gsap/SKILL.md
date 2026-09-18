---
name: gsap
description: |
  Comprehensive GreenSock Animation Platform (GSAP) skill covering Core API (to, from, fromTo, set, staggers, easing), Timelines & Choreography, ScrollTrigger & Pinning, React & Framework Integration (@gsap/react, useGSAP, Vue, Svelte), Official Plugins (Flip, Draggable, ScrollSmoother, SplitText, MorphSVG, Observer, MotionPath), Utility Methods (gsap.utils), and 60fps Performance Optimization.
triggers:
  - "gsap"
  - "gsap core"
  - "gsap timeline"
  - "scrolltrigger"
  - "gsap react"
  - "usegsap"
  - "gsap vue"
  - "gsap svelte"
  - "gsap plugins"
  - "gsap utils"
  - "gsap performance"
  - "web animation"
  - "flip animation"
  - "draggable"
license: MIT
od:
  mode: prototype
  category: animation-motion
  upstream: "https://github.com/greensock/gsap-skills"
---

# GSAP (GreenSock Animation Platform)

Unified, production-grade guide for high-performance web animations using GSAP 3.x across vanilla JavaScript, React, Vue, Svelte, and modern UI frameworks.

---

## 1. Core Tweening API

GSAP animates any numeric property, CSS style, SVG attribute, or JavaScript object value over time.

### Methods
- `gsap.to(target, vars)`: Animates from current state to specified end state.
- `gsap.from(target, vars)`: Animates from specified start state to current state.
- `gsap.fromTo(target, fromVars, toVars)`: Explicitly defines both start and end states.
- `gsap.set(target, vars)`: Applies properties immediately (zero-duration tween).

```javascript
import gsap from 'gsap';

// Basic tween
gsap.to('.box', {
  x: 200,
  yPercent: -50,
  rotation: 360,
  duration: 1.5,
  ease: 'power3.out'
});

// fromTo: guarantees initial state before animating
gsap.fromTo('.card', 
  { opacity: 0, y: 50, scale: 0.9 },
  { opacity: 1, y: 0, scale: 1, duration: 0.8, ease: 'back.out(1.7)' }
);

// Global defaults
gsap.defaults({
  duration: 0.6,
  ease: 'power2.out'
});
```

### Staggers
Animate multiple elements with incremental start delays:

```javascript
gsap.to('.list-item', {
  y: 0,
  opacity: 1,
  stagger: {
    amount: 0.8, // Total time distributed across all items
    from: 'center', // 'start' | 'end' | 'center' | 'edges' | index
    grid: [3, 4],   // Grid coordinate handling
    ease: 'power1.inOut'
  }
});
```

### Responsive & Reduced Motion (`gsap.matchMedia`)
Safely manage breakpoints and accessibility preferences:

```javascript
const mm = gsap.matchMedia();

mm.add({
  isDesktop: "(min-width: 1024px)",
  isMobile: "(max-width: 1023px)",
  reduceMotion: "(prefers-reduced-motion: reduce)"
}, (context) => {
  const { isDesktop, reduceMotion } = context.conditions;

  if (reduceMotion) {
    gsap.set('.hero-title', { opacity: 1, y: 0 });
    return;
  }

  gsap.to('.hero-title', {
    y: isDesktop ? -100 : -40,
    duration: 1
  });
});
```

---

## 2. Timelines & Choreography

Timelines sequence tweens seamlessly without manual delay math.

```javascript
const tl = gsap.timeline({
  defaults: { duration: 0.6, ease: 'power2.out' },
  onComplete: () => console.log('Timeline complete')
});

// Position Parameter syntax:
// absolute time: 2 (at 2s mark)
// relative offset: "+=0.5", "-=0.2"
// sync with previous: "<" (start together), "<0.2" (0.2s after prev starts)
// sync with prev end: ">"

tl.to('.header', { y: 0, opacity: 1 })
  .to('.sidebar', { x: 0 }, "-=0.3")
  .addLabel('contentIn')
  .to('.main-content', { opacity: 1, scale: 1 }, 'contentIn')
  .to('.cards', { y: 0, stagger: 0.1 }, 'contentIn+=0.2');

// Controls
tl.play();
tl.pause();
tl.reverse();
tl.seek(1.5);
tl.timeScale(2.0); // 2x speed
```

---

## 3. ScrollTrigger & Scroll-Driven Animation

`ScrollTrigger` links tweens and timelines directly to scroll progress or viewport entry.

### Registration & Setup
```javascript
import { ScrollTrigger } from 'gsap/ScrollTrigger';
gsap.registerPlugin(ScrollTrigger);
```

### Scroll-Linked Tween & Scrubbing
```javascript
gsap.to('.progress-bar', {
  scaleX: 1,
  transformOrigin: 'left center',
  ease: 'none',
  scrollTrigger: {
    trigger: '#article',
    start: 'top top',
    end: 'bottom bottom',
    scrub: 0.5 // Smooth scrubbing with 0.5s lag
  }
});
```

### Pinned Sections & Toggle Actions
```javascript
const scrubTl = gsap.timeline({
  scrollTrigger: {
    trigger: '.pinned-container',
    start: 'top top',
    end: '+=2000', // Pinned for 2000px of scroll
    pin: true,
    scrub: true,
    snap: 1 / 3, // Snap to closest 33% step
    anticipatePin: 1
  }
});

scrubTl.to('.panel-1', { xPercent: -100 })
       .to('.panel-2', { xPercent: 0 }, "<")
       .to('.panel-3', { scale: 1.2 });

// Viewport enter / leave actions
gsap.to('.reveal-box', {
  y: 0,
  opacity: 1,
  scrollTrigger: {
    trigger: '.reveal-box',
    start: 'top 80%',
    toggleActions: 'play none none reverse' 
    // onEnter, onLeave, onEnterBack, onLeaveBack
  }
});
```

### Batching & Refresh
```javascript
// Batch multiple scroll triggers to prevent layout thrashing
ScrollTrigger.batch('.card-item', {
  onEnter: batch => gsap.to(batch, { opacity: 1, y: 0, stagger: 0.15, overwrite: true }),
  onLeaveBack: batch => gsap.to(batch, { opacity: 0, y: 50, overwrite: true })
});

// Refresh after dynamic DOM changes / image loads
ScrollTrigger.refresh();
```

---

## 4. Framework Integrations

### React & Next.js (`@gsap/react`)
Always use the official `useGSAP` hook for automated context scoping and cleanup on unmount:

```bash
npm install gsap @gsap/react
```

```tsx
'use client';
import { useRef } from 'react';
import gsap from 'gsap';
import { useGSAP } from '@gsap/react';
import { ScrollTrigger } from 'gsap/ScrollTrigger';

gsap.registerPlugin(useGSAP, ScrollTrigger);

export function HeroSection() {
  const containerRef = useRef<HTMLDivElement>(null);

  useGSAP(() => {
    // Scoped queries: selects only inside containerRef
    gsap.from('.hero-badge', { y: -30, opacity: 0, duration: 0.6 });
    gsap.from('.hero-title', { y: 40, opacity: 0, duration: 0.8, delay: 0.2 });

    gsap.to('.scrolling-card', {
      scrollTrigger: {
        trigger: '.scrolling-card',
        start: 'top 80%',
        scrub: 1
      },
      scale: 1.05
    });
  }, { scope: containerRef, dependencies: [] });

  return (
    <div ref={containerRef} className="hero-container">
      <span className="hero-badge">New Release</span>
      <h1 className="hero-title">High Performance Motion</h1>
      <div className="scrolling-card">Content</div>
    </div>
  );
}
```

### Vue 3 / Nuxt
Use `gsap.context()` inside `onMounted` and revert in `onUnmounted`:

```vue
<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';

gsap.registerPlugin(ScrollTrigger);

const root = ref(null);
let ctx;

onMounted(() => {
  ctx = gsap.context((self) => {
    gsap.from('.box', {
      opacity: 0,
      y: 50,
      stagger: 0.2,
      scrollTrigger: {
        trigger: root.value,
        start: 'top 75%'
      }
    });
  }, root.value);
});

onUnmounted(() => {
  ctx?.revert(); // Cleans up tweens, timelines, and ScrollTriggers
});
</script>

<template>
  <div ref="root">
    <div class="box">Item 1</div>
    <div class="box">Item 2</div>
  </div>
</template>
```

### Svelte / SvelteKit
```svelte
<script>
  import { onMount, onDestroy } from 'svelte';
  import gsap from 'gsap';

  let container;
  let ctx;

  onMount(() => {
    ctx = gsap.context(() => {
      gsap.from('.item', { opacity: 0, scale: 0.8, stagger: 0.1 });
    }, container);
  });

  onDestroy(() => {
    ctx?.revert();
  });
</script>

<div bind:this={container}>
  <div class="item">Svelte 1</div>
  <div class="item">Svelte 2</div>
</div>
```

---

## 5. Official Plugins & Capabilities

### Plugin Registration
Always register plugins prior to execution:
```javascript
import gsap from 'gsap';
import { Flip } from 'gsap/Flip';
import { Draggable } from 'gsap/Draggable';
import { Observer } from 'gsap/Observer';
import { ScrollToPlugin } from 'gsap/ScrollToPlugin';

gsap.registerPlugin(Flip, Draggable, Observer, ScrollToPlugin);
```

### Flip (First, Last, Invert, Play)
Seamless layout transitions when moving elements across DOM containers or resizing:

```javascript
// 1. Record initial state
const state = Flip.getState('.grid-item');

// 2. Mutate DOM (e.g. toggle class or move element)
document.querySelector('.grid').classList.toggle('list-view');

// 3. Animate smoothly from old to new bounds
Flip.from(state, {
  duration: 0.7,
  ease: 'power1.inOut',
  stagger: 0.05,
  absolute: true,
  onEnter: elements => gsap.fromTo(elements, { opacity: 0 }, { opacity: 1 }),
  onLeave: elements => gsap.to(elements, { opacity: 0 })
});
```

### Draggable & Inertia
```javascript
Draggable.create('.knob', {
  type: 'x,y',
  bounds: '#boundary-container',
  edgeResistance: 0.65,
  inertia: true,
  onDrag: function() {
    console.log(`Current position: ${this.x}, ${this.y}`);
  }
});
```

### Observer (Unified Pointer & Wheel Interactions)
```javascript
Observer.create({
  target: window,
  type: 'wheel,touch,pointer',
  onUp: () => prevSlide(),
  onDown: () => nextSlide(),
  tolerance: 10,
  preventDefault: true
});
```

### ScrollToPlugin
```javascript
gsap.to(window, {
  duration: 1,
  scrollTo: { y: '#section-target', offsetY: 80 },
  ease: 'power2.inOut'
});
```

---

## 6. GSAP Utilities (`gsap.utils`)

High-performance math and array helpers:

```javascript
// Clamping and mapping
const clamp = gsap.utils.clamp(0, 100);
clamp(150); // 100

const mapper = gsap.utils.mapRange(0, window.innerWidth, -100, 100);
mapper(window.innerWidth / 2); // 0

// Interpolation & Snap
const lerp = gsap.utils.interpolate(0, 500, 0.5); // 250
const snapToGrid = gsap.utils.snap(20); // snaps to nearest multiple of 20

// Array helpers & Distribution
const elements = gsap.utils.toArray('.card');
const wrapValue = gsap.utils.wrap(0, 5); // 6 -> 1

// Piping utility functions
const transform = gsap.utils.pipe(
  gsap.utils.clamp(0, 1000),
  gsap.utils.mapRange(0, 1000, 0, 1),
  gsap.utils.snap(0.01)
);
```

---

## 7. Performance & 60fps Optimization

### Strict Property Rules
1. **Always prefer GPU compositor transforms**:
   - Use `x`, `y`, `xPercent`, `yPercent`, `rotation`, `scale`, `opacity`.
   - Never animate layout properties (`top`, `left`, `margin`, `width`, `height`, `padding`) unless strictly unavoidable.
2. **Avoid Layout Thrashing**:
   - Read DOM properties first, then write animations in batches.
   - Use `ScrollTrigger.batch()` for long lists.
3. **Use `will-change` selectively**:
   - Set `willChange: 'transform'` in tweens only during heavy animations.
4. **Always Clean Up Memory**:
   - Revert contexts (`ctx.revert()`) on component unmount to prevent ghost ScrollTriggers and memory leaks.
