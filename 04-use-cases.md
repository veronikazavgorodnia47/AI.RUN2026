---
case: A
date: 2026-07-27
consumes: 03-research-audit.md, 01-context-brief.md
---

## Input pains (from 03-research-audit.md)

1. Compliance cost spike — EPR and DPP require SKU-level traceability data; mid-market
   players cannot generate it without a unified product layer. (sourced)
2. Store productivity gap — fragmented inventory visibility makes omnichannel fulfillment
   unreliable; fulfillment cost elevated above sector median. (confirmed by verbatims)
3. Mid-market squeeze — value players attack price floor, Zalando moves upmarket;
   undifferentiated retailers lose margin from both ends. (sharpened by teardown)

---

## Ten candidate use cases

| # | Use case | Type | Pain |
|---|---|---|---|
| 1 | SKU material composition classifier — reads supplier data, auto-populates DPP fields | classical-ML | 1 |
| 2 | EPR/DPP compliance report generator — takes product data, outputs per-country compliance reports | generative | 1 |
| 3 | Supply chain traceability agent — queries supplier APIs, flags non-compliant SKUs, initiates remediation | agentic | 1 |
| 4 | Real-time inventory availability predictor — true "available to promise" per store across all stacks | classical-ML | 2 |
| 5 | Click-and-collect notification generator — personalised pickup and delay alerts by region and language | generative | 2 |
| 6 | Omnichannel fulfillment orchestration agent — routes orders across stores/warehouses, monitors SLAs | agentic | 2 |
| 7 | Customer CLV segmentation model — identifies premium vs price-sensitive segments per region | classical-ML | 3 |
| 8 | Regional product description generator — adapts tone and positioning by segment | generative | 3 |
| 9 | Competitive pricing intelligence agent — monitors Shein/Temu/Zalando, flags margin risk per SKU | agentic | 3 |
| 10 | Unified product data golden record builder — deduplicates and unifies product master across 22 stacks | classical-ML | 1+2 |

### Dedup flags
- #1 and #10 partially overlap (product data scope). Different enough to keep — #1 is narrow
  (DPP fields only), #10 is foundational (full master data). Partial overlap noted.
- #5 and #8 are simple generative tasks with likely commodity solutions. Flagged for
  commodity check.

---

## Scoring

| # | Use case | Value (1–5) | Value rationale | Feasibility (1–5) | Feasibility rationale | Score |
|---|---|---|---|---|---|---|
| 1 | SKU material composition classifier | 3 | Reduces manual DPP data entry but narrow scope | 4 | Well-defined ML task, structured supplier input | 12 |
| 2 | EPR/DPP compliance report generator | 4 | High compliance cost avoided; regulatory obligation not optional | 3 | Output needs legal review; hallucination risk in regulatory context | 12 |
| 3 | Supply chain traceability agent | 5 | Addresses full DPP mandate and consumer trust | 2 | Blocked by supplier API availability and data quality across 22 markets | 10 |
| 4 | Real-time inventory availability predictor | 5 | Directly reduces fulfillment cost and improves click-and-collect promise | 3 | Blocked by unified data feed requirement across 22 country stacks | 15 |
| 5 | Click-and-collect notification generator | 2 | UX improvement only; low business impact | 5 | Trivially buildable; off-the-shelf | 10 |
| 6 | Omnichannel fulfillment orchestration agent | 5 | Highest impact on fulfillment cost and SLA | 2 | Most complex integration; requires all 22 stacks connected | 10 |
| 7 | Customer CLV segmentation model | 3 | Personalization uplift limited without unified customer data | 4 | Well-established ML technique; data dependency manageable | 12 |
| 8 | Regional product description generator | 2 | Marginal UX improvement; easily replicated | 5 | Off-the-shelf generative task | 10 |
| 9 | Competitive pricing intelligence agent | 4 | Live margin threat from Shein/Temu; margin protection is urgent | 3 | Pricing API complexity manageable; vendor landscape exists | 12 |
| 10 | Unified product data golden record builder | 5 | Foundation for Pain 1+2; enables DPP and inventory visibility | 2 | Master data management across 22 systems is a major integration programme | 10 |

---

## Top three

| Rank | # | Use case | Score | Why selected |
|---|---|---|---|---|
| 1 | 4 | Real-time inventory availability predictor | 15 | Highest score; directly addresses dominant business problem |
| 2 | 2 | EPR/DPP compliance report generator | 12 | Regulatory urgency; non-optional compliance obligation by 2026 |
| 3 | 9 | Competitive pricing intelligence agent | 12 | Live margin threat; most actionable of the tied 12-scorers |

## Commodity check

| # | Use case | Commodity? | Verdict |
|---|---|---|---|
| 4 | Real-time inventory predictor | No | Unified inventory across 22 stacks requires custom integration — not off-the-shelf | 
| 2 | EPR/DPP compliance report generator | Borderline | DPP vendors exist (Sphera, Sustainalize) but product data integration is custom — keep |
| 9 | Competitive pricing intelligence agent | Borderline | Tools exist (Prisync, Competera) but mid-market fashion margin integration is custom — keep |

No swaps required. Top three stands.
