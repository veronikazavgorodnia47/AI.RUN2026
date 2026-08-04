---
case: Meridian Retail Group — Click & Collect
kata: K 6.W.6
date: 2026-08-05
author: Veronika Zavgorodnia
status: DRAFT — not signed off
consumes_from: 00-test-plan.md, 01-test-cases.md, 02-test-data.json, 03-defects.md, 04-rca.md
---

# Test Report — Meridian Click & Collect (Phase 1)

---

## 1. Coverage

**Tested:** identity stitch on first in-store pickup (2 cases) and SAP inventory check at pickup confirmation (2 cases), across 4 input records drawn from `02-test-data.json` (IT, FR, IT cross-region, IT→DE).

**Not tested this cycle:** web cart and reservation step (TC-01–03), loyalty-points credit cross-region (TC-10–12), and POS pickup confirmation end-to-end flow (TC-13–15) — these surfaces have written cases in `01-test-cases.md` but were outside the 4-case execution budget. Guard tests GT-01–03 (from `04-rca.md`) are not yet in the regression suite.

**Explicitly out of scope (per `00-test-plan.md`):** SAP ECC inventory ground-truth correctness (Finance-owned), legacy Shopify storefronts, Phase 2 cross-channel inventory reservation patterns.

---

## 2. Pass rate and defect density

| Surface | Cases run | Pass | Defects | Pass rate | Defects / case |
|---|---|---|---|---|---|
| Identity stitch | 2 | 1 | 1 | 50% | 0.5 |
| SAP inventory check | 2 | 0 | 2 | 0% | 1.0 |
| Web reservation | 0 | — | — | not run | — |
| Loyalty credit | 0 | — | — | not run | — |
| POS confirmation | 0 | — | — | not run | — |
| **Total** | **4** | **1** | **3** | **25%** | **0.75** |

All 3 defects are Priority 1. 2 of 3 are Severity 1 (data exposure + phantom stock). The SAP inventory check surface has a 100% defect rate across the cases run — both cases failed.

---

## 3. Top 2 problematic areas

**Area 1 — SAP inventory check (2 defects / 2 cases):**
The SAP inventory read at pickup confirmation has no freshness validation (DEFECT-03, S1 P1) and no timeout fallback (DEFECT-02, S2 P1). The POS accepts any non-zero SAP result regardless of timestamp, directly replicating the documented 7% phantom-cancellation rate. The blank-screen timeout leaves staff without guidance and produces no event log entry.

**Area 2 — Identity stitch (1 defect / 2 cases):**
The stitch logic matches on email domain prefix rather than exact email address, merging two unrelated corporate customers into a single record (DEFECT-01, S1 P1). Customer B's loyalty history and order data become visible to Customer A — a GDPR Article 5 violation. The basic single-account merge (TC-04) passed; the failure is isolated to the domain-matching branch of the stitch logic.

---

## 4. Improvement backlog

Ranked by impact; top = highest.

| Rank | Item | Why it matters | Owner | Priority |
|---|---|---|---|---|
| 1 | Add `result_timestamp` to Apollo Gateway `inventory.pickupCheck` schema and enforce a 30s staleness ceiling at POS — block confirmation if `(now − result_timestamp) > 30s` | Closes DEFECT-03; directly addresses the 7% phantom-cancellation rate; required for the exit criterion "zero phantom-stock cancellations" | Engineering — Tomás Reyes | P1 |
| 2 | Write a `held_stock` event to the cart event store at Click & Collect reservation confirmation (SKU, qty, store, expiry = +48h) | Provides a compensating snapshot when the SAP read is stale or times out; closes the residual race window on DEFECT-03; prerequisite for timeout fallback correctness | Engineering — Tomás Reyes | P1 |
| 3 | Fix identity stitch to match on exact email address, not domain prefix; add a deterministic rule for domain-collision cases (flag for manual review rather than auto-merge) | Closes DEFECT-01; prevents GDPR Article 5 violation; Asha Sundaram sign-off required before Italy pilot launch | Engineering + Privacy — Asha Sundaram | P1 |
| 4 | Implement a named SAP timeout fallback at POS: display "SAP inventory check timed out — contact inventory manager, reference [order ID]" and write a timeout event to the log | Closes DEFECT-02; gives David Park's store staff a clear action; closes the event-log gap that makes post-incident reconstruction impossible | Engineering — Tomás Reyes | P1 |
| 5 | Add guard tests GT-01, GT-02, GT-03 (from `04-rca.md`) to the regression suite and wire to CI — run on every SAP adapter change and Apollo Gateway schema update | Prevents the phantom-stock condition from returning silently through a neighbouring change; gives Tomás Reyes' team a regression signal before the defect reaches QA again | QA + Engineering | P2 |

---

## 5. Residual risk

| Risk | Evidence gap | Who is affected | Why it remains |
|---|---|---|---|
| PSD2 SCA failure silently cancels EU reservation (Risk 3 from test plan) | TC-03 not run; no evidence the cart-preserve behaviour works | EU customers (IT, Nordics); Marco Rossi Italy pilot | Web reservation surface not executed this cycle |
| Loyalty credit routing failure on cross-region pickup | TC-10, TC-11 not run | IT/GB/JP customers picking up outside home region | Loyalty credit surface not executed this cycle |
| POS QR flow notification timing outside 30s SLA | TC-13 not run | All customers at pickup counter | POS confirmation surface not executed this cycle |
| SAP staleness fix introduces new timestamp parsing edge cases | Fix not yet implemented or verified against real SAP adapter | All Click & Collect markets | Improvement backlog item 1 is pending; guard tests not yet in CI |
| Identity stitch domain-fix breaks single-account merge (TC-04 passed) | Fix not yet applied; regression risk on the passing case | All new web-signup customers with in-store loyalty cards | Improvement backlog item 3 is pending |

---

## 6. Release recommendation

**Status: HOLD** `[DRAFT — requires Eva Müller or accountable release owner sign-off]`

Three Priority-1 defects are open, two of which are Severity 1 (GDPR data exposure and phantom-stock confirmation). The primary exit criterion — zero phantom-stock cancellations on SAP inventory check cases — is violated. Three of the five in-scope surfaces were not executed in this cycle.

**Conditions to move to Ship:**

| # | Condition | Accountable owner |
|---|---|---|
| 1 | DEFECT-01 (identity stitch GDPR merge) patched, TC-06 re-run green, Asha Sundaram written sign-off | Engineering + Asha Sundaram |
| 2 | DEFECT-03 (SAP staleness) fix implemented, GT-01/GT-02/GT-03 all green | Engineering — Tomás Reyes |
| 3 | DEFECT-02 (SAP timeout fallback) implemented, TC-09 re-run green | Engineering — Tomás Reyes |
| 4 | Second test cycle executed covering web reservation (TC-01–03), loyalty credit (TC-10–12), and POS confirmation (TC-13–15) with pass rate ≥ 95% on all P1 cases | QA |
| 5 | David Park (Head of Retail Ops) and Sarah Chen (Head of CX) sign off on the updated report | David Park, Sarah Chen |

Eva Müller to confirm rollout decision for Italy pilot (country 1 → country 2) once all five conditions are met.
