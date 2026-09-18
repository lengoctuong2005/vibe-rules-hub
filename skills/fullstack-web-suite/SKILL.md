---
name: fullstack-web-suite
description: |
  Enterprise Fullstack Web Master Suite unifying modern frontend engineering (React 19, Next.js App Router, Tailwind v4, GSAP 60fps animations, WCAG 2.2 accessibility), robust backend services (Node/Bun/Go/Python, PostgreSQL connection pooling, Redis caching & queues), OWASP Top 10 defense-in-depth security, and autonomous subagent delegation (planner, architect, tdd-guide, react-reviewer, security-reviewer, e2e-runner).
triggers:
  - "fullstack"
  - "fullstack suite"
  - "fullstack-web-suite"
  - "nextjs fullstack"
  - "react19 backend"
  - "web architecture"
license: MIT
metadata:
  origin: ECC
---

# Fullstack Web Master Suite

Comprehensive, production-ready framework integrating next-generation frontend frameworks, high-throughput backend services, enterprise security controls, and autonomous multi-agent pipelines.

---

## 1. Architecture Topology

```
+-------------------------------------------------------------------------+
|                           CLIENT LAYER                                  |
|  React 19 (Server/Client Components) + Tailwind v4 + GSAP (60fps)       |
|  State: Server Actions, useActionState, useOptimistic, TanStack Query   |
+------------------------------------+------------------------------------+
                                     | HTTPS / HTTP2 / WSS
                                     v
+-------------------------------------------------------------------------+
|                           GATEWAY & AUTH                                |
|  HttpOnly, Secure, SameSite=Strict Cookies + CSRF Protection            |
|  Rate Limiting (Redis Token Bucket) + Input Sanitization                |
+------------------------------------+------------------------------------+
                                     |
                  +------------------+------------------+
                  v                                     v
+----------------------------------+  +-----------------------------------+
|        APPLICATION BACKEND       |  |        ASYNCHRONOUS WORKERS       |
|  Node.js / Bun / Go / Python     |  |  Redis Streams / BullMQ / Celery  |
|  Clean Hexagonal Architecture    |  |  Event-Driven Background Jobs     |
+-----------------+----------------+  +-----------------+-----------------+
                  |                                     |
                  +------------------+------------------+
                                     |
                                     v
+-------------------------------------------------------------------------+
|                             DATA LAYER                                  |
|  PostgreSQL (Connection Pooling / PgBouncer) + Prisma / Kysely ORM      |
|  Redis Distributed Cache (Cache-Aside + Read-Through)                   |
+-------------------------------------------------------------------------+
```

---

## 2. Frontend Engineering Standards

### React 19 & Next.js App Router Patterns
- **Server Component First**: Fetch data directly in React Server Components (`RSC`) without client waterfalls.
- **Client Boundary Containment**: Confine `"use client"` to interactive buttons, input fields, or canvas elements.
- **Server Actions**: Mutate state through server actions guarded with schema validation.

```tsx
// app/actions/update-profile.ts
'use server';

import { z } from 'zod';
import { db } from '@/lib/db';
import { revalidatePath } from 'next/cache';

const ProfileSchema = z.object({
  userId: z.string().uuid(),
  displayName: z.string().min(2).max(50),
  bio: z.string().max(200).optional(),
});

// ponytail: Native Server Action - single validation gate, direct DB write
export async function updateProfileAction(prevState: unknown, formData: FormData) {
  const parsed = ProfileSchema.safeParse({
    userId: formData.get('userId'),
    displayName: formData.get('displayName'),
    bio: formData.get('bio'),
  });

  if (!parsed.success) {
    return { success: false, errors: parsed.error.flatten().fieldErrors };
  }

  await db.user.update({
    where: { id: parsed.data.userId },
    data: { name: parsed.data.displayName, bio: parsed.data.bio },
  });

  revalidatePath('/profile');
  return { success: true, errors: null };
}
```

### Styling with Tailwind CSS v4
- Use semantic CSS theme tokens configured via standard CSS variables.
- Avoid inline layout magic numbers; use strict spacing and typography ladders.

```css
@theme {
  --color-brand-primary: oklch(0.65 0.22 260);
  --color-brand-surface: oklch(0.98 0.01 250);
  --color-brand-text: oklch(0.18 0.02 260);
  --font-sans: 'Inter Variable', system-ui, sans-serif;
}
```

### React 19 Optimistic UI Implementation
```tsx
'use client';

import { useOptimistic, useTransition } from 'react';
import { updateProfileAction } from '@/app/actions/update-profile';

interface ProfileProps {
  user: { id: string; name: string; bio?: string };
}

export function ProfileForm({ user }: ProfileProps) {
  const [isPending, startTransition] = useTransition();
  const [optimisticUser, setOptimisticUser] = useOptimistic(
    user,
    (state, update: Partial<typeof user>) => ({ ...state, ...update })
  );

  return (
    <form action={(formData) => {
      const name = formData.get('displayName') as string;
      startTransition(async () => {
        setOptimisticUser({ name });
        await updateProfileAction(null, formData);
      });
    }}>
      <input type="hidden" name="userId" value={user.id} />
      <input
        name="displayName"
        defaultValue={optimisticUser.name}
        className="rounded border px-3 py-2 text-brand-text"
      />
      <button type="submit" disabled={isPending} className="btn-primary">
        {isPending ? 'Saving...' : 'Save Profile'}
      </button>
    </form>
  );
}
```

---

## 3. Backend & Data Layer Patterns

### Database Connection Pooling (PostgreSQL)
Ensure database pool limits match application concurrency limits to avoid connection exhaustion.

```typescript
// lib/db.ts
import { Pool } from 'pg';
import { PrismaPg } from '@prisma/adapter-pg';
import { PrismaClient } from '@prisma/client';

const connectionString = process.env.DATABASE_URL!;
const pool = new Pool({
  connectionString,
  max: 20,
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 2000,
});

const adapter = new PrismaPg(pool);
export const db = new PrismaClient({ adapter });
```

### Redis Caching (Cache-Aside Pattern)

```typescript
// lib/cache.ts
import { Redis } from 'ioredis';

const redis = new Redis(process.env.REDIS_URL || 'redis://localhost:6379');

export async function fetchWithCache<T>(
  key: string,
  ttlSeconds: number,
  fetchFn: () => Promise<T>
): Promise<T> {
  const cached = await redis.get(key);
  if (cached) return JSON.parse(cached) as T;

  const data = await fetchFn();
  if (data !== null && data !== undefined) {
    await redis.setex(key, ttlSeconds, JSON.stringify(data));
  }
  return data;
}
```

### Distributed Rate Limiter (Token Bucket)
```typescript
// lib/rate-limit.ts
import { Redis } from 'ioredis';

export async function checkRateLimit(
  redis: Redis,
  identifier: string,
  limit: number = 60,
  windowSeconds: number = 60
): Promise<{ allowed: boolean; remaining: number }> {
  const key = `rate_limit:${identifier}`;
  const current = await redis.incr(key);
  if (current === 1) {
    await redis.expire(key, windowSeconds);
  }
  return {
    allowed: current <= limit,
    remaining: Math.max(0, limit - current)
  };
}
```

---

## 4. Defense-in-Depth Security Protocol

1. **Authentication & Session Tokens**:
   - Session tokens stored exclusively in `HttpOnly`, `Secure`, `SameSite=Strict` cookies.
   - JWT validation with asymmetric public/private keys (RS256 / EdDSA).
2. **OWASP Top 10 Mitigation**:
   - **A01 Broken Access Control**: Verify user permissions on every Server Action and API route.
   - **A02 Cryptographic Failures**: Passwords hashed with `Argon2id` or `bcrypt` (cost >= 12).
   - **A03 Injection**: 100% Parameterized queries via ORM / Query Builder.
   - **A07 Identification Failures**: Rate limit authentication attempts (Redis Token Bucket).
3. **Secret Scanning**:
   - Mandatory execution of `python scripts/safety_guard.py --scan-file <target>` prior to commits.

---

## 5. Subagent Orchestration & Role Matrix

| Subagent | Role & Objective | Invocation Trigger |
|----------|------------------|--------------------|
| `planner` | Vertical slice decomposition, minimal abstraction scoping | Start of new fullstack feature |
| `architect` | Schema design, DTO definitions, API interface contracts | Database or cross-layer change |
| `tdd-guide` | Red-Green-Refactor test cycle enforcement | Before writing business logic |
| `react-reviewer` | Hook dependencies, RSC boundary verification, CSS performance | After frontend component changes |
| `security-reviewer` | OWASP Top 10 audit, cookie parameters, secret scans | Before pull requests / commits |
| `e2e-runner` | Playwright integration, Core Web Vitals, accessibility audit | Staging & release verification |

---

## 6. Verification & Quality Gates

Run the verification pipeline before releasing:
```bash
# 1. Type check
pnpm tsc --noEmit

# 2. Unit & Integration tests
pnpm test

# 3. Secret scan
python scripts/safety_guard.py --scan-file .

# 4. E2E & Performance run
pnpm playwright test
```
