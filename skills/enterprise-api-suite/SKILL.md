---
name: enterprise-api-suite
description: |
  Enterprise API Master Suite providing architectural blueprints for Clean/Hexagonal systems, multi-protocol gateways (REST, gRPC, GraphQL), PostgreSQL connection pooling, Expand-Contract zero-downtime database migrations, Redis-backed 2-Phase Locking (2PL) distributed transactions, 3-strike circuit breakers, and subagent orchestration (architect, database-reviewer, security-reviewer, tdd-guide).
triggers:
  - "enterprise-api"
  - "enterprise api suite"
  - "enterprise-api-suite"
  - "hexagonal architecture"
  - "distributed lock"
  - "zero downtime migration"
  - "circuit breaker"
license: MIT
metadata:
  origin: ECC
---

# Enterprise API Master Suite

Robust, fault-tolerant backend system design engine supporting high-scale distributed APIs, deterministic concurrency control, and zero-downtime evolution.

---

## 1. Clean & Hexagonal Architecture Layout

```
src/
├── domain/                      # 100% Framework-agnostic business logic
│   ├── models/                  # Entities and Value Objects (Absolute precision)
│   └── errors/                  # Domain exceptions and invariant failures
├── application/                 # Use cases and orchestration
│   ├── ports/
│   │   ├── primary/             # Inbound interfaces (Use Case interfaces)
│   │   └── secondary/           # Outbound interfaces (Repository, Cache, EventBus)
│   └── use-cases/               # Orchestrates transactions and domain models
└── infrastructure/              # Adapters and external integrations
    ├── adapters/
    │   ├── primary/             # REST controllers, gRPC services, GraphQL resolvers
    │   └── secondary/           # Postgres Repositories, Redis Locks, Message Brokers
    └── config/                  # Database pools, telemetry, environment validation
```

---

## 2. Distributed Locking & 2-Phase Locking (2PL)

To avoid deadlocks across distributed workers or parallel subagents, all operations lock resources according to a strict global hierarchy.

### Global Resource Priority Hierarchy
1. **DB Migration / Schema** (Highest Priority)
2. **System Configurations & Environment**
3. **Core Business Entities (e.g. Accounts, Orders)**
4. **Ephemeral Sessions & Logs** (Lowest Priority)

```typescript
// infrastructure/locks/DistributedLockManager.ts
import { Redis } from 'ioredis';

export class DistributedLockManager {
  constructor(private readonly redis: Redis) {}

  // ponytail: Minimal 2PL acquisition with automatic backoff jitter
  async acquireWithRetry(
    resourceKey: string,
    ttlMs: number = 10000,
    maxRetries: number = 3
  ): Promise<string> {
    const token = crypto.randomUUID();
    for (let attempt = 0; attempt < maxRetries; attempt++) {
      const ok = await this.redis.set(`lock:${resourceKey}`, token, 'PX', ttlMs, 'NX');
      if (ok === 'OK') return token;
      
      const jitterMs = 50 + Math.floor(Math.random() * 100);
      await new Promise(res => setTimeout(res, jitterMs));
    }
    throw new Error(`[LOCK_TIMEOUT] Failed to acquire lock for ${resourceKey} after ${maxRetries} attempts`);
  }

  async release(resourceKey: string, token: string): Promise<boolean> {
    const luaScript = `
      if redis.call("get", KEYS[1]) == ARGV[1] then
        return redis.call("del", KEYS[1])
      else
        return 0
      end
    `;
    const result = await this.redis.eval(luaScript, 1, `lock:${resourceKey}`, token);
    return result === 1;
  }
}
```

---

## 3. Expand-Contract Zero-Downtime Migration Pattern

When altering database schemas in high-traffic enterprise environments:

```
Step 1: EXPAND
  - Add new column/table with NULLable constraints or sensible defaults.
  - Deploy code that writes to BOTH old and new columns (Dual-write).
  - Verify zero impact on active readers.

Step 2: BACKFILL
  - Execute idempotent batch updates to migrate historical rows.
  - Monitor database CPU, replication lag, and disk I/O.

Step 3: CONTRACT
  - Deploy code that reads EXCLUSIVELY from the new column.
  - Cease writes to the old column.
  - Drop deprecated column/index after release stability window.
```

---

## 4. 3-Strike Circuit Breaker State Machine

```typescript
// infrastructure/resilience/CircuitBreaker.ts
export type BreakerState = 'CLOSED' | 'OPEN' | 'HALF_OPEN';

export class CircuitBreaker {
  private failureCount = 0;
  private state: BreakerState = 'CLOSED';
  private lastFailureTime = 0;

  constructor(
    private readonly failureThreshold = 3,
    private readonly resetTimeoutMs = 15000
  ) {}

  // ponytail: 3-Strike Breaker - minimal state machine preventing downstream death spirals
  async execute<T>(action: () => Promise<T>, fallback: () => Promise<T>): Promise<T> {
    const now = Date.now();

    if (this.state === 'OPEN') {
      if (now - this.lastFailureTime > this.resetTimeoutMs) {
        this.state = 'HALF_OPEN';
      } else {
        return fallback();
      }
    }

    try {
      const result = await action();
      if (this.state === 'HALF_OPEN') {
        this.state = 'CLOSED';
        this.failureCount = 0;
      }
      return result;
    } catch (error) {
      this.failureCount++;
      this.lastFailureTime = Date.now();
      if (this.failureCount >= this.failureThreshold) {
        this.state = 'OPEN';
      }
      return fallback();
    }
  }
}
```

---

## 5. Subagent Delegation Matrix

| Subagent | Responsibility | Quality Gate |
|----------|----------------|--------------|
| `architect` | Hexagonal port segregation, protobuf definitions, API contracts | Pure domain logic, no framework leakage |
| `database-reviewer` | Expand-Contract migrations, index cardinality, connection pool sizing | Zero table-lock risk, rollback verified |
| `security-reviewer` | mTLS, JWT RS256 token verification, rate limit policies, secret scan | Zero secret leakage, OWASP compliance |
| `tdd-guide` | In-memory adapter test suite, contract tests | 100% green tests on business invariants |

---

## 6. Verification Checklist

```bash
# 1. Run unit and domain invariant tests
pnpm test:unit

# 2. Run contract and database migration tests
pnpm test:integration

# 3. Security pre-push scan
python scripts/safety_guard.py --scan-file .
```
