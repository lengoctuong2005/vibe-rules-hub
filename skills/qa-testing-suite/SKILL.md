---
name: qa-testing-suite
description: |
  Master QA Testing Suite for end-to-end quality assurance: Test Pyramid orchestration, Vitest/Jest unit testing, Testcontainers integration testing (PostgreSQL/Redis), Pact contract testing, Playwright headless E2E automation, k6 load benchmarking, and automated flaky test quarantine.
triggers:
  - "qa"
  - "qa-testing-suite"
  - "testing suite"
  - "playwright"
  - "vitest"
  - "testcontainers"
  - "load testing"
  - "k6"
license: MIT
metadata:
  origin: ECC
---

# QA Testing Master Suite

Enterprise quality assurance framework implementing rigorous multi-tier testing, containerized integration environments, end-to-end browser automation, and performance benchmarks.

---

## 1. System Architecture Topology

```
+─────────────────────────────────────────────────────────────────────────+
|                         THE TESTING PYRAMID                             |
|                                                                         |
|                          /  E2E (10%)  \                                |
|                         /  Playwright   \                               |
|                        /─────────────────\                              |
|                       / INTEGRATION (20%) \                             |
|                      /   Testcontainers    \                            |
|                     /───────────────────────\                           |
|                    /       UNIT (70%)        \                          |
|                   /       Vitest / Pytest     \                         |
|                  /─────────────────────────────\                        |
+────────────────────────────────────┬────────────────────────────────────+
                                     │ Continuous Execution Gate
                                     ▼
+─────────────────────────────────────────────────────────────────────────+
|                       PERFORMANCE & CHAOS TESTING                       |
|  k6 Load Benchmarks (p95 < 30ms) · Network Latency Fault Injection      |
+────────────────────────────────────┬────────────────────────────────────+
                                     │
                                     ▼
+─────────────────────────────────────────────────────────────────────────+
|                     FLAKY TEST QUARANTINE ENGINE                        |
|  Auto-Retry (Max 2) · Quarantine Tagging · Flakiness Tracker            |
+─────────────────────────────────────────────────────────────────────────+
```

---

## 2. Integration Test with Testcontainers & PostgreSQL

```typescript
// tests/integration/user-repo.test.ts
import { describe, it, beforeAll, afterAll, expect } from 'vitest';
import { PostgreSqlContainer, StartedPostgreSqlContainer } from '@testcontainers/postgresql';
import { Pool } from 'pg';

describe('UserRepository Integration Test', () => {
  let container: StartedPostgreSqlContainer;
  let pool: Pool;

  beforeAll(async () => {
    container = await new PostgreSqlContainer('postgres:16-alpine')
      .withDatabase('testdb')
      .withUsername('testuser')
      .withPassword('testpass')
      .start();

    pool = new Pool({ connectionString: container.getConnectionUri() });

    // Run schema migrations
    await pool.query(`
      CREATE TABLE users (
        id UUID PRIMARY KEY,
        email VARCHAR(255) NOT NULL UNIQUE
      );
    `);
  }, 30000);

  afterAll(async () => {
    await pool.end();
    await container.stop();
  });

  it('inserts and retrieves user by id', async () => {
    const id = crypto.randomUUID();
    await pool.query('INSERT INTO users (id, email) VALUES ($1, $2)', [id, 'qa@example.com']);

    const res = await pool.query('SELECT * FROM users WHERE id = $1', [id]);
    expect(res.rows.length).toBe(1);
    expect(res.rows[0].email).toBe('qa@example.com');
  });
});
```

---

## 3. Playwright Page Object Model (POM) E2E Test

```typescript
// tests/e2e/pages/LoginPage.ts
import { Page, Locator } from '@playwright/test';

export class LoginPage {
  readonly page: Page;
  readonly emailInput: Locator;
  readonly passwordInput: Locator;
  readonly submitButton: Locator;

  constructor(page: Page) {
    this.page = page;
    this.emailInput = page.locator('input[name="email"]');
    this.passwordInput = page.locator('input[name="password"]');
    this.submitButton = page.locator('button[type="submit"]');
  }

  async goto() {
    await this.page.goto('/login');
  }

  async login(email: string, pass: string) {
    await this.emailInput.fill(email);
    await this.passwordInput.fill(pass);
    await this.submitButton.click();
  }
}
```

---

## 4. Redis Testcontainers Integration Testing

```typescript
// tests/integration/rate-limiter.test.ts
import { describe, it, beforeAll, afterAll, expect } from 'vitest';
import { GenericContainer, StartedTestContainer } from 'testcontainers';
import { Redis } from 'ioredis';

describe('Redis Rate Limiter Integration', () => {
  let redisContainer: StartedTestContainer;
  let redis: Redis;

  beforeAll(async () => {
    redisContainer = await new GenericContainer('redis:7-alpine')
      .withExposedPorts(6379)
      .start();

    const host = redisContainer.getHost();
    const port = redisContainer.getMappedPort(6379);
    redis = new Redis({ host, port });
  }, 20000);

  afterAll(async () => {
    await redis.quit();
    await redisContainer.stop();
  });

  it('increments and sets ttl on rate limit keys', async () => {
    const key = 'rate_limit:test_user';
    const count = await redis.incr(key);
    await redis.expire(key, 60);

    expect(count).toBe(1);
    const ttl = await redis.ttl(key);
    expect(ttl).toBeGreaterThan(0);
  });
});
```

---

## 5. Flaky Test Quarantine Manager

```typescript
// tests/utils/quarantine.ts
export function runWithQuarantine<T>(
  testName: string,
  testFn: () => Promise<T>,
  maxRetries: number = 2
): Promise<T> {
  let attempt = 0;
  async function execute(): Promise<T> {
    try {
      return await testFn();
    } catch (err) {
      attempt++;
      if (attempt <= maxRetries) {
        console.warn(`[QUARANTINE_RETRY] Test "${testName}" failed (Attempt ${attempt}/${maxRetries}). Retrying...`);
        return await execute();
      }
      throw err;
    }
  }
  return execute();
}
```

---

## 6. Subagent Delegation Matrix

| Subagent | Role & Objective | Deliverable |
|----------|------------------|-------------|
| `test-planner` | Risk-based test matrix and coverage strategy | `test_plan.md` |
| `tdd-guide` | Red-Green-Refactor unit test suite implementation | Vitest test suites |
| `integration-tester` | Testcontainers integration testing | Repository integration tests |
| `e2e-runner` | Playwright browser automation & POM suites | E2E test specs |
| `performance-benchmarker`| k6 load and SLA benchmark execution | Performance report |
