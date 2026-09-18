---
name: frame-motion-templates
description: |
  High-impact animated frame motion templates for video overlays, interactive web stories, cinematic titles, and micro-interactions. Unifies NYT editorial data charts, sticky flowcharts, cyberpunk glitch kinetic typography, cinematic light leaks, liquid mesh gradient backgrounds, logo sting outros, and macOS notification banners.
triggers:
  - "frame motion"
  - "motion templates"
  - "video frames"
  - "glitch title"
  - "data chart frame"
  - "liquid hero"
  - "macos notification"
license: MIT
metadata:
  origin: ECC
---

# Frame Motion Templates & Video Overlays

Production collection of animated frame templates for video overlays, cinematic hero headers, editorial presentations, and interactive micro-visuals.

---

## 1. NYT-Style Editorial Data Chart Frames

Editorial typography, staggered line/bar reveal animations, and annotated callouts:

```html
<!-- ponytail: NYT Data Chart Frame - CSS Keyframe animated staggered SVG line -->
<div class="nyt-chart-frame bg-[#f8f8f8] dark:bg-[#121212] p-8 rounded-lg font-serif border border-neutral-300 dark:border-neutral-800 max-w-2xl">
  <div class="text-xs uppercase tracking-widest text-red-600 font-sans font-bold mb-1">Economic Indicator</div>
  <h2 class="text-2xl font-bold text-neutral-900 dark:text-neutral-100 mb-4">Global Semiconductor Production Volume</h2>
  <div class="relative h-64 w-full">
    <svg viewBox="0 0 500 200" class="w-full h-full overflow-visible">
      <line x1="0" y1="180" x2="500" y2="180" stroke="#ccc" stroke-dasharray="4 4" />
      <path
        d="M 0 160 Q 120 140 250 80 T 500 30"
        fill="none"
        stroke="#d32f2f"
        stroke-width="3"
        stroke-linecap="round"
        class="chart-line-animate"
      />
    </svg>
  </div>
  <p class="text-xs text-neutral-500 font-sans mt-2">Source: Semiconductor Industry Association • Monthly telemetry</p>
</div>

<style>
.chart-line-animate {
  stroke-dasharray: 600;
  stroke-dashoffset: 600;
  animation: drawLine 2s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}
@keyframes drawLine {
  to { stroke-dashoffset: 0; }
}
</style>
```

---

## 2. Cyberpunk Glitch Kinetic Title Frames

High-impact glitch titles with chromatic aberration (RGB offset), CRT scanlines, and data corruption noise:

```css
/* ponytail: Chromatic Aberration Glitch Animation */
.glitch-title {
  position: relative;
  font-family: 'JetBrains Mono', monospace;
  font-weight: 900;
  color: #fff;
  text-transform: uppercase;
}
.glitch-title::before, .glitch-title::after {
  content: attr(data-text);
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}
.glitch-title::before {
  left: 2px;
  text-shadow: -2px 0 #00ffff;
  clip-path: inset(20% 0 30% 0);
  animation: glitch-anim-1 2s infinite linear alternate-reverse;
}
.glitch-title::after {
  left: -2px;
  text-shadow: -2px 0 #ff007f;
  clip-path: inset(50% 0 10% 0);
  animation: glitch-anim-2 2.5s infinite linear alternate-reverse;
}
@keyframes glitch-anim-1 {
  0% { clip-path: inset(40% 0 61% 0); }
  50% { clip-path: inset(92% 0 1% 0); }
  100% { clip-path: inset(10% 0 70% 0); }
}
@keyframes glitch-anim-2 {
  0% { clip-path: inset(25% 0 58% 0); }
  50% { clip-path: inset(54% 0 30% 0); }
  100% { clip-path: inset(80% 0 5% 0); }
}
```

---

## 3. Liquid Mesh Gradient Hero Frames

Dynamic WebGL-style fluid backgrounds using CSS radial gradients and filter blending:

```html
<div class="relative w-full h-96 overflow-hidden rounded-2xl bg-neutral-950 flex items-center justify-center">
  <div class="absolute inset-0 filter blur-[80px] opacity-70">
    <div class="absolute w-72 h-72 rounded-full bg-purple-600 top-1/4 left-1/4 animate-pulse"></div>
    <div class="absolute w-80 h-80 rounded-full bg-cyan-500 bottom-1/4 right-1/4 animate-ping"></div>
    <div class="absolute w-64 h-64 rounded-full bg-pink-500 top-1/2 right-1/3"></div>
  </div>
  <div class="relative z-10 text-center px-6">
    <h1 class="text-4xl md:text-5xl font-extrabold text-white tracking-tight">Next-Generation Interface</h1>
  </div>
</div>
```

---

## 4. Realistic macOS Notification Banner Frame

Realistic frosted-glass banner overlay with icon, header, and body text:

```html
<div class="flex items-center gap-3 p-3 bg-neutral-900/80 backdrop-blur-xl border border-white/10 text-white rounded-2xl shadow-2xl max-w-sm">
  <div class="w-10 h-10 rounded-xl bg-gradient-to-tr from-blue-600 to-indigo-500 flex items-center justify-center text-lg font-bold shadow-md">
    ⚡
  </div>
  <div class="flex-1 min-w-0">
    <div class="flex justify-between items-baseline">
      <span class="text-xs font-semibold text-neutral-200">System Kernel</span>
      <span class="text-[10px] text-neutral-400">now</span>
    </div>
    <p class="text-xs font-medium text-white truncate">Build 9.5.0 Deployed</p>
    <p class="text-[11px] text-neutral-300 truncate">All regression checks and tests passed.</p>
  </div>
</div>
```
