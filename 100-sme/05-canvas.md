---
case: A
date: 2026-07-27
consumes: 04-use-cases.md
use_case: "#4 — Real-time inventory availability predictor"
---

## Opportunity canvas

### Problem
We cannot promise shoppers accurate click-and-collect availability because our 22 country
inventory systems do not share a live view of stock.

---

### Users
**Primary:** Head of Omnichannel / VP E-commerce at mid-market EU fashion retailer.

**Sub-segments:**
- Store operations managers — responsible for fulfillment execution at store level
- End shoppers — experience the broken availability promise directly
- Supply chain planners — allocate stock across stores and regions

---

### Value
Reduces click-and-collect cancellation rate by ≥30% against a 15% sector baseline
(unverified — confirm with client OMS data before exec review), recovering order value
and protecting repeat purchase rate.

---

### Assumptions
1. ≥35% of click-and-collect cancellations are caused by stock count discrepancy between
   systems, not true out-of-stock situations.
   *Testable: cancellation reason codes from client OMS.*

2. Inventory API integration across 22 country stacks is achievable within 12 months using
   an event-driven abstraction layer.
   *Testable: technical spike with 3 representative stacks in sprint 1.*

3. Shoppers shown a confirmed availability signal convert to click-and-collect at ≥25%
   higher rate than those shown a tentative signal.
   *Testable: A/B test, minimum 1,000 sessions per arm.*

---

### Solution
Shoppers see a confirmed availability indicator at the product page instead of a tentative
stock message. Store staff receive alerts only for orders at risk of non-fulfillment.
Operations teams see a live stock-confidence view across all stores.
The promise changes; the back end stays invisible.

---

## Critique log

| Cell | Original weakness | Fix applied |
|---|---|---|
| Value | "≥40%" had no baseline or source | Revised to ≥30% against 15% baseline; flagged unverified |
| Assumption 2 | "6 months" was optimistic for 22-system integration | Revised to 12 months; added testability method |
| Solution | Described implementation details, not behaviour | Rewritten to describe user-facing behaviour only |
