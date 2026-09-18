---
name: fintech-accounting-suite
description: |
  Master Fintech & Accounting Suite for mission-critical financial engineering: immutable double-entry general ledgers, strict debit-credit mathematical balance constraints, zero floating-point math (exact integer cents/BigInt), payment gateway webhooks (Stripe/PayOS), and automated daily reconciliation engines.
triggers:
  - "fintech"
  - "fintech-accounting-suite"
  - "accounting"
  - "ledger"
  - "double-entry"
  - "stripe webhook"
  - "payment gateway"
license: MIT
metadata:
  origin: ECC
---

# Fintech Accounting Master Suite

Enterprise financial engineering framework for designing, implementing, securing, and operating mathematically rigorous double-entry ledgers, payment pipelines, and reconciliation systems.

---

## 1. System Architecture Topology

```
+─────────────────────────────────────────────────────────────────────────+
|                       EXTERNAL PAYMENT GATEWAYS                         |
|  Stripe · PayOS · PayPal · Bank Transfer Automated Clearing House (ACH) |
+────────────────────────────────────┬────────────────────────────────────+
                                     │ Webhooks with HMAC-SHA256 Signatures
                                     ▼
+─────────────────────────────────────────────────────────────────────────+
|                     PAYMENT GATEWAY INGESTION & IDEMPOTENCY             |
|  Timing-Safe Signature Check · 72h Deduplication Key · Replay Filter    |
+────────────────────────────────────┬────────────────────────────────────+
                                     │
                  ┌──────────────────┴──────────────────┐
                  ▼                                     ▼
+──────────────────────────────────┐  +───────────────────────────────────+
|     DOUBLE-ENTRY LEDGER ENGINE   |  |      DEAD-LETTER RECOVERY QUEUE   |
|  ACID Transaction Boundary       |  |  Failed Event Quarantine (DLQ)    |
|  Debit == Credit Invariant Check |  |  Exponential Backoff Retry        |
+─────────────────┬────────────────┘  +───────────────────────────────────+
                  │
                  ▼
+─────────────────────────────────────────────────────────────────────────+
|                    IMMUTABLE LEDGER DATA STORAGE                        |
|  Append-Only Journal Entries · Foreign Key Constraints · No Updates/Deletes|
+────────────────────────────────────┬────────────────────────────────────+
                                     │
                                     ▼
+─────────────────────────────────────────────────────────────────────────+
|                   DAILY RECONCILIATION & AUDIT ENGINE                   |
|  Gateway Settlement vs Ledger Comparison · 0-Variance Assertion         |
+─────────────────────────────────────────────────────────────────────────+
```

---

## 2. Double-Entry Posting Service (TypeScript / PostgreSQL)

```typescript
// services/ledger.service.ts
import { PoolClient } from 'pg';

export interface JournalEntryDTO {
  accountId: string;
  type: 'DEBIT' | 'CREDIT';
  amountCents: bigint;
}

export class LedgerService {
  // ponytail: Atomic double-entry transaction posting with balance check
  static async postTransaction(
    client: PoolClient,
    idempotencyKey: string,
    description: string,
    entries: JournalEntryDTO[]
  ): Promise<string> {
    if (entries.length < 2) {
      throw new Error('LEDGER_INVALID: Transaction must have at least 2 entries');
    }

    // Verify Sum(Debits) === Sum(Credits)
    let totalDebits = 0n;
    let totalCredits = 0n;

    for (const entry of entries) {
      if (entry.amountCents <= 0n) {
        throw new Error('LEDGER_INVALID: Amount must be positive');
      }
      if (entry.type === 'DEBIT') totalDebits += entry.amountCents;
      if (entry.type === 'CREDIT') totalCredits += entry.amountCents;
    }

    if (totalDebits !== totalCredits) {
      throw new Error(`LEDGER_UNBALANCED: Debits (${totalDebits}) != Credits (${totalCredits})`);
    }

    // Insert Transaction Record
    const txRes = await client.query(
      `INSERT INTO ledger_transactions (idempotency_key, description)
       VALUES ($1, $2)
       RETURNING id`,
      [idempotencyKey, description]
    );
    const transactionId = txRes.rows[0].id;

    // Insert Journal Entries
    for (const entry of entries) {
      await client.query(
        `INSERT INTO ledger_entries (transaction_id, account_id, entry_type, amount_cents)
         VALUES ($1, $2, $3, $4)`,
        [transactionId, entry.accountId, entry.type, entry.amountCents.toString()]
      );
    }

    return transactionId;
  }
}
```

---

## 3. Automated Reconciliation Balance Check

```typescript
// services/recon.service.ts
import { Pool } from 'pg';

export interface ReconciliationReport {
  accountId: string;
  totalDebitsCents: bigint;
  totalCreditsCents: bigint;
  calculatedBalanceCents: bigint;
}

export class ReconciliationService {
  static async auditAccountBalance(pool: Pool, accountId: string): Promise<ReconciliationReport> {
    const res = await pool.query(
      `SELECT
         COALESCE(SUM(CASE WHEN entry_type = 'DEBIT' THEN amount_cents ELSE 0 END), 0) as debits,
         COALESCE(SUM(CASE WHEN entry_type = 'CREDIT' THEN amount_cents ELSE 0 END), 0) as credits
       FROM ledger_entries
       WHERE account_id = $1`,
      [accountId]
    );

    const debits = BigInt(res.rows[0].debits);
    const credits = BigInt(res.rows[0].credits);

    return {
      accountId,
      totalDebitsCents: debits,
      totalCreditsCents: credits,
      calculatedBalanceCents: debits - credits,
    };
  }
}
```

---

## 4. Multi-Currency Exchange Calculator

```typescript
// services/currency.service.ts
export interface ExchangeRateLock {
  baseCurrency: string;
  targetCurrency: string;
  rateNumerator: bigint;   // e.g. 25000n
  rateDenominator: bigint; // e.g. 1n
}

export function convertCurrency(
  baseAmountCents: bigint,
  rate: ExchangeRateLock
): bigint {
  return (baseAmountCents * rate.rateNumerator) / rate.rateDenominator;
}
```

---

## 5. PCI-DSS Tokenization & Masking Utility

```typescript
// services/tokenization.service.ts
import crypto from 'node:crypto';

export class TokenizationService {
  static maskCardNumber(pan: string): string {
    const clean = pan.replace(/\D/g, '');
    if (clean.length < 12) return '****';
    const last4 = clean.slice(-4);
    const first6 = clean.slice(0, 6);
    return `${first6}${'*'.repeat(clean.length - 10)}${last4}`;
  }

  static generatePaymentToken(pan: string, salt: string): string {
    return crypto.createHmac('sha256', salt).update(pan).digest('hex');
  }
}
```

---

## 6. Subagent Delegation Matrix

| Subagent | Role & Objective | Deliverable |
|----------|------------------|-------------|
| `ledger-architect` | Double-entry schema & debit-credit invariants | SQL ledger schema |
| `payment-gateway-engineer` | Stripe/PayOS webhook integration & signature security | Webhook handlers |
| `reconciliation-auditor` | Automated reconciliation & variance checks | Recon report |
| `financial-security-reviewer`| PCI-DSS audit, timing-safe crypto & secret scan | Security audit |
| `compliance-officer` | Audit trail verification & exchange rate locks | Compliance sign-off |
