---
name: figma
description: |
  Comprehensive Figma design-to-code and design system suite covering Figma Plugin API execution, Canvas Inspection & Manipulation, 1:1 Design-to-Code Implementation, Code-to-Figma Screen Generation, Design System Token & Rules Definition, Library Generation from Codebases, Code Connect Component Syncing, and Automated File Creation.
triggers:
  - "figma"
  - "figma to code"
  - "code to figma"
  - "figma code connect"
  - "figma design system"
  - "figma plugin api"
  - "figma canvas"
  - "figma library"
  - "figma tokens"
  - "figma fidelity"
license: MIT
od:
  mode: design-system
  category: figma
  upstream: "https://github.com/figma/skills"
metadata:
  origin: ECC
---

# Figma Design & Code Integration Suite

Production-grade guide for bi-directional Figma workflows: inspecting canvas nodes, extracting design tokens, translating Figma frames into 1:1 code, synchronizing components with Code Connect, and programmatically creating libraries via the Figma Plugin API.

---

## 1. Core Figma Plugin API Execution (`figma-use`)

Run programmatic scripts against Figma files, canvas nodes, variables, and components.

### Canvas Inspection & Node Traversal
```typescript
// Inspect selected frame or search by name
const selection = figma.currentPage.selection;
if (selection.length === 0) {
  figma.notify("Please select a frame or component to inspect.");
} else {
  const node = selection[0];
  console.log(`Node: ${node.name} (type: ${node.type}, id: ${node.id})`);
  
  if ("fills" in node) {
    console.log("Fills:", node.fills);
  }
  if ("layoutMode" in node) {
    console.log(`AutoLayout: ${node.layoutMode}, Padding: [${node.paddingTop}, ${node.paddingRight}, ${node.paddingBottom}, ${node.paddingLeft}], Gap: ${node.itemSpacing}`);
  }
}
```

### Programmatic Canvas Generation
```typescript
// Create a new component frame with AutoLayout
const frame = figma.createFrame();
frame.name = "Button / Primary";
frame.layoutMode = "HORIZONTAL";
frame.primaryAxisAlignItems = "CENTER";
frame.counterAxisAlignItems = "CENTER";
frame.paddingLeft = frame.paddingRight = 16;
frame.paddingTop = frame.paddingBottom = 10;
frame.cornerRadius = 8;
frame.fills = [{ type: 'SOLID', color: { r: 0.12, g: 0.44, b: 0.98 } }];

// Add text child
await figma.loadFontAsync({ family: "Inter", style: "Medium" });
const text = figma.createText();
text.characters = "Click Me";
text.fontSize = 14;
text.fills = [{ type: 'SOLID', color: { r: 1, g: 1, b: 1 } }];
frame.appendChild(text);

figma.currentPage.appendChild(frame);
figma.viewport.scrollAndZoomIntoView([frame]);
```

---

## 2. 1:1 Design-to-Code Implementation (`figma-implement-design`)

Transform Figma designs into pixel-perfect, accessible HTML/CSS, React, Tailwind, or SwiftUI code.

### Translation Protocol
1. **Layout Mapping**:
   - `layoutMode: HORIZONTAL` → `flex flex-row items-[counterAxis] justify-[primaryAxis]`
   - `layoutMode: VERTICAL` → `flex flex-col items-[counterAxis] justify-[primaryAxis]`
   - `itemSpacing` → `gap-[N]px`
   - `paddingLeft/Right/Top/Bottom` → `px-[N] py-[N]`
2. **Typography Mapping**:
   - Extract `fontFamily`, `fontSize`, `fontWeight`, `lineHeight`, and `letterSpacing`.
3. **Color & Token Resolution**:
   - Check if paint fills reference a Figma Variable or Style (`getVariableById` or `fillStyleId`). Map to CSS variables / Tailwind tokens (`var(--color-primary)`).
4. **Interactive States**:
   - Extract component variant properties (Default, Hover, Active, Disabled) and map to CSS pseudo-classes or React state props.

---

## 3. Code Connect Integration (`figma-code-connect-components`)

Connect production components directly to Figma design system components for real-time Dev Mode inspection.

### Setting up Code Connect (`figma.config.json`)
```json
{
  "codeConnect": {
    "include": ["src/components/**/*.{ts,tsx}"],
    "parser": "react"
  }
}
```

### Component Code Connect Mapping (`Button.figma.tsx`)
```tsx
import React from 'react';
import { figma } from '@figma/code-connect';
import { Button } from './Button';

figma.connect(Button, 'https://www.figma.com/design/KEY/Design-System?node-id=123-456', {
  props: {
    variant: figma.enum('Variant', {
      Primary: 'primary',
      Secondary: 'secondary',
      Destructive: 'destructive'
    }),
    size: figma.enum('Size', {
      Small: 'sm',
      Medium: 'md',
      Large: 'lg'
    }),
    disabled: figma.boolean('Disabled'),
    label: figma.string('Label Text'),
    hasIcon: figma.boolean('Show Icon')
  },
  example: (props) => (
    <Button 
      variant={props.variant} 
      size={props.size} 
      disabled={props.disabled}
    >
      {props.label}
    </Button>
  )
});
```

---

## 4. Design System Tokens & Rules (`figma-create-design-system-rules`)

Export and synchronize Design Tokens across Figma Variables and Codebase Tokens (`tokens.css` / `tailwind.config.js`).

### Token Structure Schema
```json
{
  "color": {
    "brand": {
      "primary": { "value": "#1E40AF", "type": "color" },
      "primary-hover": { "value": "#1D4ED8", "type": "color" }
    },
    "surface": {
      "canvas": { "value": "#F9FAFB", "type": "color" },
      "card": { "value": "#FFFFFF", "type": "color" }
    }
  },
  "spacing": {
    "1": { "value": "4px", "type": "spacing" },
    "2": { "value": "8px", "type": "spacing" },
    "4": { "value": "16px", "type": "spacing" },
    "6": { "value": "24px", "type": "spacing" }
  },
  "radii": {
    "sm": { "value": "4px", "type": "borderRadius" },
    "md": { "value": "8px", "type": "borderRadius" },
    "lg": { "value": "12px", "type": "borderRadius" }
  }
}
```

---

## 5. Code-to-Figma Screen & Library Generation (`figma-generate-design`, `figma-generate-library`)

Generate matching Figma canvases from existing React / Tailwind code components or design specs.

### Scripting Library Generation
```typescript
// Script to bulk import tokens into Figma Variables Collection
async function importTokensToFigma(tokens) {
  const collection = figma.variables.createVariableCollection("Design Tokens");
  const modeId = collection.modes[0].modeId;

  for (const [key, token] of Object.entries(tokens.color.brand)) {
    const variable = figma.variables.createVariable(`brand/${key}`, collection, "COLOR");
    const rgb = hexToRgb(token.value);
    variable.setValueForMode(modeId, rgb);
  }
  figma.notify("Tokens imported to Figma Variables successfully!");
}
```

---

## 6. Automated File & Workshop Creation (`figma-create-new-file`)

Initialize blank Design files or FigJam workshop spaces programmatically via the Figma REST API:

```bash
curl -X POST \
  -H "X-Figma-Token: $FIGMA_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "Sprint 42 Design Workshop", "parent_id": "PROJECT_ID"}' \
  "https://api.figma.com/v1/files"
```
