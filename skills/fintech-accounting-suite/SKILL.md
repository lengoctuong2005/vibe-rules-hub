---
name: fintech-accounting-suite
description: |
  Master Financial Engineering & Payments Suite unifying double-entry general ledger architecture, decimal integer precision, Stripe/Payment gateway integration, multi-currency conversion snapshots, PCI-DSS compliance, and autonomous multi-agent verification (planner, architect, security-reviewer, tdd-guide).
triggers:
  - "fintech"
  - "accounting"
  - "payments"
  - "stripe"
  - "double entry"
  - "ledger"
  - "decimal precision"
  - "fintech-accounting-suite"
license: MIT
metadata:
  origin: ECC
---

# Financial Engineering & Payments Master Suite

Production architecture and engineering patterns for fintech systems, payment processing, double-entry ledgers, and compliance auditing.

---

## 1. Double-Entry Accounting Core Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           PAYMENT GATEWAYS                              │
│       Stripe, PayPal, Adyen, Banking APIs, Crypto/Web3 Rails            │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │ Webhook / API
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                     IDEMPOTENCY & HMAC VERIFICATION                     │
│  Stripe HMAC Signature Check + Redis / PostgreSQL Idempotency Lock      │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                      DOUBLE-ENTRY LEDGER ENGINE                         │
│  ACID Database Transaction: sum(Debits) == sum(Credits)                 │
│  Immutable Journal Entries + Reconciled Account Balances                │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │
          ┌──────────────────────────┴──────────────────────────┐
          ▼                                                     ▼
┌──────────────────┐                                  ┌───────────────────┐
│  ASSET ACCOUNTS  │                                  │ REVENUE / LIABILITY│
│  Stripe Clearing │                                  │ Customer Balances │
│  Operating Bank  │                                  │ Accounts Payable  │
└──────────────────┘                                  └───────────────────┘
```

---

## 2. The Zero-Float Arithmetic Principle

### Mandatory Integer Cents / Decimal Types
- In PostgreSQL: Use `NUMERIC(20, 4)` or `BIGINT` (cents).
- In Python: Use `decimal.Decimal` with `ROUND_HALF_UP` or integer cents.
- In JavaScript/TypeScript: Use native `bigint` or `decimal.js`.

```python
# ponytail: Python Decimal Currency Calculation with explicit rounding
from decimal import Decimal, ROUND_HALF_UP

CENTS = Decimal("0.01")

def calculate_invoice_tax(subtotal: Decimal, tax_rate: Decimal) -> Decimal:
    """
    Computes tax with deterministic financial half-up rounding to nearest cent.
    """
    tax = subtotal * tax_rate
    return tax.quantize(CENTS, rounding=ROUND_HALF_UP)

# Example:
subtotal = Decimal("129.99")
tax_rate = Decimal("0.0825") # 8.25%
tax_amount = calculate_invoice_tax(subtotal, tax_rate) # Decimal('10.72')
total = subtotal + tax_amount # Decimal('140.71')
```

---

## 3. Database Schema for Double-Entry Ledgers

```sql
-- ponytail: Production Double-Entry PostgreSQL Schema
CREATE TABLE journal_entries (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    idempotency_key VARCHAR(128) UNIQUE NOT NULL,
    description TEXT NOT NULL,
    currency VARCHAR(3) NOT NULL DEFAULT 'USD',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE ledger_entries (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    journal_entry_id UUID NOT NULL REFERENCES journal_entries(id) ON DELETE RESTRICT,
    account_id UUID NOT NULL,
    entry_type VARCHAR(6) NOT NULL CHECK (entry_type IN ('DEBIT', 'CREDIT')),
    amount_cents BIGINT NOT NULL CHECK (amount_cents > 0),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_ledger_account_created ON ledger_entries (account_id, created_at);
```

---

## 4. Payment Gateway Webhook Handling & Idempotency

- Always store `idempotency_key` (e.g. `evt_1O...` from Stripe) with a unique constraint.
- Wrap event ingestion in a database transaction with row-level locks on account records.
- Reject unverified webhook payloads immediately with HTTP $400$.
