---
name: ito-trade-suite
description: |
  Comprehensive Prediction Market & Asset Intelligence Suite for Itô and decentralized venues. Combines multi-asset basket comparison, background Data Atlas research agents, real-time market intelligence and sentiment analysis, and structured non-advisory trade planning worksheets.
triggers:
  - "ito trade"
  - "prediction markets"
  - "polymarket"
  - "kalshi"
  - "market intelligence"
  - "basket compare"
  - "trade planner"
license: MIT
metadata:
  origin: ECC
---

# Itô Prediction Market & Asset Intelligence Suite

Framework for prediction market research, thematic basket comparisons, background data indexing agents, and structured execution planning across Polymarket, Kalshi, and Itô venues.

---

## 1. Non-Advisory Guardrails & Risk Governance

- **Strict Non-Advisory Scope**: Never provide investment, legal, tax, or financial advice. Never instruct users to buy, sell, or leverage positions.
- **Execution Separation**: Analytical and research workflows must remain decoupled from trade execution engines. Require explicit human confirmation before placing orders.
- **Credential Security**: Never log, store, or transmit private keys, mnemonic seed phrases, or exchange API secrets.

---

## 2. Multi-Asset Basket Comparison & Portfolio Variance

Compare thematic prediction baskets against personal research theses, watchlists, or macroeconomic drivers:

```python
# ponytail: Prediction Basket Variance & Exposure Calculator
from dataclasses import dataclass
from typing import List, Dict

@dataclass(frozen=True)
class MarketContract:
    id: str
    question: str
    probability: float
    volume_24h_usd: float
    weight: float

def analyze_basket_exposure(contracts: List[MarketContract]) -> Dict[str, float]:
    """
    Computes weighted probability and aggregate liquidity for a thematic prediction basket.
    """
    total_weight = sum(c.weight for c in contracts)
    if total_weight == 0:
        return {"weighted_probability": 0.0, "total_liquidity_usd": 0.0}

    weighted_prob = sum(c.probability * (c.weight / total_weight) for c in contracts)
    total_vol = sum(c.volume_24h_usd for c in contracts)

    return {
        "weighted_probability": round(weighted_prob, 4),
        "total_liquidity_usd": round(total_vol, 2),
        "contract_count": len(contracts),
    }
```

---

## 3. Data Atlas Background Research Agents

Architecture for continuous market monitoring agents:
1. **Event Watcher**: Continuously indexes newly resolved or listed contracts across Polymarket and Kalshi APIs.
2. **Correlation Matrix**: Computes co-movement between related political, macroeconomic, and crypto event contracts.
3. **Parameter Drafting**: Generates candidate basket parameters (weights, strike ranges) and outputs markdown briefs for human review.

---

## 4. Market Intelligence & Liquidity Monitoring

- **Venue Spread Comparison**: Track price and probability discrepancies between Kalshi (CFTC-regulated) and Polymarket (Polygon/USDC).
- **Order Book Depth**: Monitor bid-ask spreads, slippage profiles for large sizes ($>\$10,000$), and market maker participation.
- **Sentiment & News Grounding**: Cross-reference news flow and social sentiment with market-implied probabilities.

---

## 5. Structured Trade Planning Worksheet

Before any manual execution, generate a structured trade plan:

| Parameter | Specification | Notes / Verification |
|-----------|---------------|----------------------|
| **Target Event** | `Fed Rate Decision Nov 2026` | Contract ID: `0x71a4...` |
| **Selected Venue** | Polymarket / Kalshi | Verify regulatory jurisdiction |
| **Max Allocation** | $\le 2\%$ Portfolio | Fixed risk envelope |
| **Entry Probability** | $0.34$ ($34\%$) | Limit order entry |
| **Invalidation Condition** | CPI Print $> 3.2\%$ | Trigger manual exit |
| **Exit Target** | $0.65$ ($65\%$) | Take profit threshold |
