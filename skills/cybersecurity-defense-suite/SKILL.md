---
name: cybersecurity-defense-suite
description: |
  Enterprise Cybersecurity Defense Master Suite: STRIDE threat modeling, Zero Trust identity architectures, Open Policy Agent (OPA) Rego policy enforcement, SAST/SCA security scanners, cryptographic tamper-proof logging (HMAC-SHA256, AES-256-GCM), and automated penetration testing gates.
triggers:
  - "cybersecurity"
  - "cybersecurity-defense-suite"
  - "security suite"
  - "threat modeling"
  - "zero trust"
  - "opa rego"
  - "cryptosecurity"
license: MIT
metadata:
  origin: ECC
---

# Cybersecurity Defense Master Suite

Production-ready application security and threat defense suite for modeling attack surfaces, enforcing Zero Trust authorization, securing cryptographic operations, and auditing vulnerability posture.

---

## 1. System Architecture Topology

```
+─────────────────────────────────────────────────────────────────────────+
|                         UNTRUSTED INGRESS BOUNDARY                      |
|  Strict Nonce CSP · TLS 1.3 · HSTS · Anti-DDoS · Rate Limiting          |
+────────────────────────────────────┬────────────────────────────────────+
                                     │
                                     ▼
+─────────────────────────────────────────────────────────────────────────+
|                      ZERO TRUST POLICY ENGINE (OPA)                     |
|  JWT Claims Validation · ABAC / RBAC Declarative Policies (Rego)        |
|  Contextual Risk Assessment (MFA status, IP reputation, Role scopes)    |
+────────────────────────────────────┬────────────────────────────────────+
                                     │
                  ┌──────────────────┴──────────────────┐
                  ▼                                     ▼
+──────────────────────────────────┐  +───────────────────────────────────+
|      CRYPTOGRAPHIC SERVICES      |  |     TAMPER-PROOF AUDIT LOGGING    |
|  Argon2id Password Hashing       |  |  HMAC-SHA256 Append-Only Logs     |
|  AES-256-GCM Data-at-Rest        |  |  SIEM & SOC Export Pipeline       |
+──────────────────────────────────┘  +───────────────────────────────────+
```

---

## 2. Open Policy Agent (OPA) Rego Authorization Engine

```rego
# authz/policy.rego
package app.authz

default allow = false

import future.keywords.in

# Decode JWT and evaluate claims
user := input.auth.user

# Rules for Document access
allow {
    input.action == "read"
    input.resource.type == "document"
    user.role in ["admin", "auditor"]
}

allow {
    input.action in ["read", "write"]
    input.resource.type == "document"
    input.resource.owner_id == user.id
    not user.suspended
}
```

```typescript
// authz/evaluator.ts
import { loadPolicy } from '@open-policy-agent/opa-wasm';

export class PolicyEvaluator {
  private policy: any;

  async init(wasmBuffer: Buffer) {
    this.policy = await loadPolicy(wasmBuffer);
  }

  // ponytail: Minimalist OPA wasm evaluation - fast memory-isolated evaluation
  evaluate(input: Record<string, any>): boolean {
    const resultSet = this.policy.evaluate(input);
    if (!resultSet || resultSet.length === 0) return false;
    return Boolean(resultSet[0].result?.allow);
  }
}
```

---

## 3. Cryptographic Service: AES-256-GCM & Argon2id

```typescript
// security/crypto.service.ts
import crypto from 'node:crypto';

export class CryptoService {
  private static readonly ALGORITHM = 'aes-256-gcm';
  private static readonly IV_LENGTH = 12; // 96 bits for GCM
  private static readonly TAG_LENGTH = 16;

  static encrypt(plaintext: string, keyBuffer: Buffer): { ciphertext: string; iv: string; tag: string } {
    const iv = crypto.randomBytes(this.IV_LENGTH);
    const cipher = crypto.createCipheriv(this.ALGORITHM, keyBuffer, iv);

    let encrypted = cipher.update(plaintext, 'utf8', 'hex');
    encrypted += cipher.final('hex');
    const tag = cipher.getAuthTag().toString('hex');

    return {
      ciphertext: encrypted,
      iv: iv.toString('hex'),
      tag,
    };
  }

  static decrypt(ciphertext: string, ivHex: string, tagHex: string, keyBuffer: Buffer): string {
    const decipher = crypto.createDecipheriv(
      this.ALGORITHM,
      keyBuffer,
      Buffer.from(ivHex, 'hex')
    );
    decipher.setAuthTag(Buffer.from(tagHex, 'hex'));

    let decrypted = decipher.update(ciphertext, 'hex', 'utf8');
    decrypted += decipher.final('utf8');
    return decrypted;
  }
}
```

---

## 4. CSP Nonce & Security Headers Middleware

```typescript
// security/headers.middleware.ts
import { Request, Response, NextFunction } from 'express';
import crypto from 'node:crypto';

export function securityHeadersMiddleware(req: Request, res: Response, next: NextFunction) {
  const nonce = crypto.randomBytes(16).toString('base64');
  res.locals.nonce = nonce;

  res.setHeader(
    'Content-Security-Policy',
    `default-src 'self'; script-src 'self' 'nonce-${nonce}'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; frame-ancestors 'none';`
  );
  res.setHeader('X-Content-Type-Options', 'nosniff');
  res.setHeader('X-Frame-Options', 'DENY');
  res.setHeader('Referrer-Policy', 'strict-origin-when-cross-origin');
  res.setHeader('Strict-Transport-Security', 'max-age=63072000; includeSubDomains; preload');

  next();
}
```

---

## 5. Timing-Safe Comparison & Session Revocation

```typescript
// security/session.service.ts
import crypto from 'node:crypto';
import { Redis } from 'ioredis';

export class SessionSecurityService {
  constructor(private readonly redis: Redis) {}

  static timingSafeEqual(a: string, b: string): boolean {
    const bufA = Buffer.from(a);
    const bufB = Buffer.from(b);
    if (bufA.length !== bufB.length) return false;
    return crypto.timingSafeEqual(bufA, bufB);
  }

  async revokeSession(userId: string, sessionId: string): Promise<void> {
    await this.redis.sadd(`revoked_sessions:${userId}`, sessionId);
    await this.redis.expire(`revoked_sessions:${userId}`, 86400 * 7); // 7 days
  }

  async isSessionRevoked(userId: string, sessionId: string): Promise<boolean> {
    const isMember = await this.redis.sismember(`revoked_sessions:${userId}`, sessionId);
    return isMember === 1;
  }
}
```

---

## 6. Subagent Delegation Matrix

| Subagent | Role & Objective | Deliverable |
|----------|------------------|-------------|
| `threat-modeler` | STRIDE analysis & trust boundary mapping | `threat_model.md` |
| `policy-architect` | OPA Rego policy implementation & tests | `policy.rego` |
| `sast-scanner` | Semgrep / Trivy static vulnerability scanning | Security report |
| `crypto-auditor` | Argon2id, AES-256-GCM & TLS validation | Crypto verification |
| `penetration-tester` | Automated exploit and BOLA testing | Pen-test findings |
