---
name: enterprise-api-suite
description: |
  Comprehensive Enterprise API Master Suite orchestrating high-throughput, distributed API architectures: REST (OpenAPI 3.1), gRPC (Protobuf v3), GraphQL, Hexagonal Architecture, distributed rate limiting, circuit breakers, idempotency engines, OpenTelemetry distributed tracing, and automated subagent quality gates.
triggers:
  - "enterprise-api"
  - "enterprise-api-suite"
  - "api suite"
  - "grpc rest"
  - "microservice api"
  - "api architecture"
license: MIT
metadata:
  origin: ECC
---

# Enterprise API Master Suite

Production-grade framework for engineering, testing, securing, and operating mission-critical distributed APIs with extreme resilience, zero-downtime scalability, and end-to-end observability.

---

## 1. System Architecture Topology

```
+─────────────────────────────────────────────────────────────────────────+
|                           API CLIENTS                                   |
|  Single Page Apps (SPA) · Mobile Apps · Partner Microservices · CLIs    |
+────────────────────────────────────┬────────────────────────────────────+
                                     │ HTTPS / HTTP2 / gRPC
                                     ▼
+─────────────────────────────────────────────────────────────────────────+
|                         API GATEWAY & EDGE                              |
|  TLS Termination · OAuth2/OIDC Auth · WAF · CORS · Rate Limiter         |
|  Distributed Token Bucket (Redis) · W3C Trace Context Injection         |
+────────────────────────────────────┬────────────────────────────────────+
                                     │
                  ┌──────────────────┴──────────────────┐
                  ▼                                     ▼
+──────────────────────────────────┐  +───────────────────────────────────+
|        REST / HTTP SERVICE       |  |           gRPC SERVICE            |
|  OpenAPI 3.1 Contract            |  |  Protobuf v3 Binary Streams       |
|  RFC 7807 Error Standard         |  |  High-Throughput Inter-Service    |
+─────────────────┬────────────────┘  +─────────────────┬─────────────────+
                  │                                     │
                  └──────────────────┬──────────────────┘
                                     │
                                     ▼
+─────────────────────────────────────────────────────────────────────────+
|                      HEXAGONAL CORE DOMAIN (PORTS)                      |
|  Business Entities · Domain Rules · Use Cases · Outbound Interfaces     |
+────────────────────────────────────┬────────────────────────────────────+
                                     │
                  ┌──────────────────┴──────────────────┐
                  ▼                                     ▼
+──────────────────────────────────┐  +───────────────────────────────────+
|     POSTGRESQL ADAPTER (ACID)    |  |       REDIS ADAPTER (CACHE)       |
|  Connection Pooling (PgBouncer)  |  |  Idempotency Locks · Caching      |
+──────────────────────────────────┘  +───────────────────────────────────+
```

---

## 2. Hexagonal Clean Architecture Pattern

```typescript
// domain/ports/order-repository.port.ts
export interface OrderEntity {
  id: string;
  customerId: string;
  totalCents: number;
  currency: string;
  status: 'pending' | 'completed' | 'cancelled';
  createdAt: Date;
}

export interface OrderRepositoryPort {
  findById(id: string): Promise<OrderEntity | null>;
  save(order: OrderEntity): Promise<void>;
  updateStatus(id: string, status: OrderEntity['status']): Promise<void>;
}

// application/use-cases/create-order.use-case.ts
export class CreateOrderUseCase {
  constructor(private readonly orderRepo: OrderRepositoryPort) {}

  // ponytail: Minimalist Hexagonal Use-Case - straightforward validation and save
  async execute(dto: { customerId: string; totalCents: number; currency: string }): Promise<OrderEntity> {
    if (dto.totalCents <= 0) {
      throw new Error('ORDER_TOTAL_INVALID: Total must be greater than zero');
    }
    const order: OrderEntity = {
      id: crypto.randomUUID(),
      customerId: dto.customerId,
      totalCents: dto.totalCents,
      currency: dto.currency,
      status: 'pending',
      createdAt: new Date(),
    };
    await this.orderRepo.save(order);
    return order;
  }
}
```

---

## 3. Distributed Resilience & Idempotency Engine

```typescript
// infrastructure/middleware/idempotency.middleware.ts
import { Request, Response, NextFunction } from 'express';
import { Redis } from 'ioredis';

export function createIdempotencyMiddleware(redis: Redis) {
  return async (req: Request, res: Response, next: NextFunction) => {
    const key = req.header('Idempotency-Key');
    if (!key) {
      return res.status(400).json({
        type: 'https://api.example.com/errors/missing-idempotency-key',
        title: 'Missing Idempotency-Key Header',
        status: 400
      });
    }

    const redisKey = `idempotency:${key}`;
    const cached = await redis.get(redisKey);
    if (cached) {
      const { statusCode, body } = JSON.parse(cached);
      return res.status(statusCode).json(body);
    }

    // Intercept response
    const originalJson = res.json.bind(res);
    res.json = (body: any) => {
      if (res.statusCode >= 200 && res.statusCode < 300) {
        redis.setex(redisKey, 86400, JSON.stringify({ statusCode: res.statusCode, body }));
      }
      return originalJson(body);
    };

    next();
  };
}
```

### Circuit Breaker Pattern (Opossum/Native)
```typescript
// infrastructure/resilience/circuit-breaker.ts
export class CircuitBreaker<T> {
  private failures = 0;
  private state: 'CLOSED' | 'OPEN' | 'HALF_OPEN' = 'CLOSED';
  private nextAttempt = Date.now();

  constructor(
    private readonly threshold: number = 5,
    private readonly resetTimeoutMs: number = 10000
  ) {}

  async execute(action: () => Promise<T>): Promise<T> {
    if (this.state === 'OPEN') {
      if (Date.now() < this.nextAttempt) {
        throw new Error('CIRCUIT_OPEN: Service temporarily unavailable');
      }
      this.state = 'HALF_OPEN';
    }

    try {
      const result = await action();
      this.state = 'CLOSED';
      this.failures = 0;
      return result;
    } catch (err) {
      this.failures++;
      if (this.failures >= this.threshold) {
        this.state = 'OPEN';
        this.nextAttempt = Date.now() + this.resetTimeoutMs;
      }
      throw err;
    }
  }
}
```

---

## 4. OpenTelemetry Observability Standard

```typescript
// infrastructure/observability/telemetry.ts
import { trace, context, SpanStatusCode } from '@opentelemetry/api';

const tracer = trace.getTracer('enterprise-api-service', '1.0.0');

export async function traceSpan<T>(
  name: string,
  operation: () => Promise<T>
): Promise<T> {
  return tracer.startActiveSpan(name, async (span) => {
    try {
      const result = await operation();
      span.setStatus({ code: SpanStatusCode.OK });
      return result;
    } catch (error: any) {
      span.recordException(error);
      span.setStatus({ code: SpanStatusCode.ERROR, message: error.message });
      throw error;
    } finally {
      span.end();
    }
  });
}
```

---

## 5. Security & Defense Matrix

| Attack Vector | Countermeasure | Implementation Mechanism |
|---------------|----------------|---------------------------|
| **BOLA / IDOR** | User-tenant scope validation | Enforce `WHERE user_id = :authUserId` on all queries |
| **Token Replay** | Short-lived JWTs + Redis JTI Denylist | JWT expiry < 15m; revocations stored in Redis |
| **API Denial of Service** | Multi-tier rate limiting | Leaky bucket by IP + Token bucket by API Key |
| **Data Tampering** | Cryptographic signatures | HMAC-SHA256 payload signatures on webhooks |

---

## 6. Subagent Delegation Matrix

| Subagent | Responsibility | Deliverable |
|----------|----------------|-------------|
| `planner` | Service boundaries & protocol selection | `api_plan.md` |
| `architect` | Contract generation (OpenAPI 3.1 / Proto v3) | Interface specs & DTO schemas |
| `tdd-guide` | Contract tests & idempotency test harnesses | Vitest / Jest test suites |
| `api-reviewer` | Hexagonal port isolation & RFC 7807 audits | Code review sign-off |
| `security-reviewer` | BOLA scans, rate limiting & secret scanning | Security checklist validation |
| `load-tester` | k6 stress and latency validation | Latency p95/p99 benchmark report |
