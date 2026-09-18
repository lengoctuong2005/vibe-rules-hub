---
name: qa-testing-suite
description: |
  Master Quality Assurance, Test-Driven Development (TDD) & End-to-End (E2E) Suite unifying Playwright browser automation, Vitest/Jest/PyTest unit testing, visual regression snapshots, contract testing, and autonomous multi-agent verification gates (planner, tdd-guide, code-reviewer, e2e-runner).
triggers:
  - "qa testing"
  - "qa suite"
  - "qa-testing-suite"
  - "tdd guide"
  - "playwright e2e"
  - "vitest test"
  - "pytest testing"
  - "visual regression"
license: MIT
metadata:
  origin: ECC
---

# QA Testing & Continuous Quality Master Suite

Comprehensive quality engineering framework uniting unit, integration, visual regression, and multi-browser end-to-end testing with autonomous multi-agent quality gates.

---

## 1. Multi-Tier Testing Pyramid Architecture

```
                      ▲
                     / \
                    /   \
                   / E2E \       Playwright (Chromium, Firefox, WebKit)
                  /───────\      Critical flows & Visual Regression
                 / Integr- \     API routes, DB Transactions,
                /   ation   \    Service Boundaries (Supertest, Testcontainers)
               /─────────────\
              /     Unit      \  Vitest / Jest / PyTest
             /─────────────────\ Fast, isolated, pure function testing (>= 80% coverage)
```

---

## 2. Test-Driven Development (TDD) Workflow

### The Iron Rule of TDD
1. **Red**: Write a test for non-existent or modified functionality. Run it and verify failure.
2. **Green**: Write the simplest implementation that makes the test pass.
3. **Refactor**: Clean up the code while keeping all tests green.

```python
# ponytail: Python PyTest TDD - pure function boundary check
import pytest

def format_currency_cents(cents: int, currency: str = "USD") -> str:
    if cents < 0:
        raise ValueError("Currency amount cannot be negative")
    dollars = cents / 100.0
    return f"${dollars:,.2f} {currency}"

def test_format_currency_cents_standard():
    assert format_currency_cents(125050) == "$1,250.50 USD"

def test_format_currency_cents_zero():
    assert format_currency_cents(0) == "$0.00 USD"

def test_format_currency_cents_negative_raises():
    with pytest.raises(ValueError, match="cannot be negative"):
        format_currency_cents(-500)
```

---

## 3. Playwright E2E & Visual Regression Standards

### Best Practices
- **Resilient Selectors**: Prefer `getByRole`, `getByLabel`, `getByTestId` over brittle CSS/XPath selectors.
- **Auto-Waiting**: Avoid arbitrary `page.waitForTimeout()`. Rely on Playwright's built-in web-first assertions (`expect(locator).toBeVisible()`).
- **Visual Regression**: Use `expect(page).toHaveScreenshot()` with threshold configurations.

```typescript
// playwright.config.ts
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 2 : undefined,
  reporter: [['html', { open: 'never' }]],
  use: {
    baseURL: process.env.PLAYWRIGHT_BASE_URL || 'http://localhost:3000',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
  },
  projects: [
    { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
    { name: 'firefox', use: { ...devices['Desktop Firefox'] } },
    { name: 'webkit', use: { ...devices['Desktop Safari'] } },
    { name: 'Mobile Safari', use: { ...devices['iPhone 14'] } },
  ],
});
```

---

## 4. Contract & Schema Testing

Validate data transfer objects across system boundaries to guarantee API backwards compatibility:

```typescript
// ponytail: Zod Schema Contract Test
import { z } from 'zod';
import { describe, it, expect } from 'vitest';

export const UserContractSchema = z.object({
  id: z.string().uuid(),
  email: z.string().email(),
  role: z.enum(['admin', 'member', 'guest']),
  createdAt: z.string().datetime(),
});

describe('User Contract API Schema', () => {
  it('validates a compliant backend response payload', () => {
    const rawPayload = {
      id: 'a1b2c3d4-e5f6-7a8b-9c0d-1e2f3a4b5c6d',
      email: 'user@example.com',
      role: 'member',
      createdAt: '2026-09-18T12:00:00.000Z',
    };
    const result = UserContractSchema.safeParse(rawPayload);
    expect(result.success).toBe(true);
  });
});
```
