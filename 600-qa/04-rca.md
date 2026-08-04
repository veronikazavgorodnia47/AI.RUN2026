---
case: Meridian Retail Group — Click & Collect
kata: K 6.W.5
date: 2026-08-05
author: Veronika Zavgorodnia
defect: DEFECT-03
source: 03-defects.md
---

# Root Cause Analysis — DEFECT-03

---

## 1. Defect summary

**Title:** POS confirms Click & Collect pickup using a 45-second-stale SAP inventory result — phantom stock delivered to customer, original reservation holder turned away at counter

**Test case:** TC-16 | **Severity:** 1 | **Priority:** 1 | **Surface:** SAP inventory check

**Observed behaviour:** When the SAP stub returns an in-stock result timestamped 45s in the past (exceeding the 30s freshness ceiling), the POS does not inspect the timestamp. It accepts the result, confirms the pickup, deducts stock, and credits loyalty points — all against a stale snapshot. If a second customer reserved the same item in the 45s window, the stock deduction is against phantom inventory and the second customer is turned away at the counter.

**Business impact:** directly replicates the documented 7% phantom-stock cancellation rate; the primary exit criterion ("zero phantom-stock cancellations on SAP inventory check cases") is violated by this finding alone; blocks David Park's approval for country rollout expansion.

---

## 2. Root cause

**The condition that made this bug possible was that the SAP inventory read at pickup confirmation had no freshness validation — the POS accepted any non-zero in-stock result regardless of the result timestamp, and no held-stock token was written at reservation time to serve as a compensating state signal when the SAP read was stale.**

**Evidence trail (walked backward from failure):**

| Step | What was checked | Finding |
|---|---|---|
| Failure point | POS confirms pickup despite stale SAP data | POS never reads `result.timestamp`; it only checks `result.quantity > 0` |
| Missing constraint | Freshness ceiling on SAP read | No `max_staleness_seconds` parameter exists in the Apollo GraphQL resolver for the inventory check |
| Missing compensating state | Held-stock token at reservation time | The cart service does not write a hold event to the event store when a Click & Collect reservation is confirmed — there is no record to fall back on |
| Root condition | What state of the world made this possible | The integration contract between Apollo Gateway and the SAP read adapter (defined in `03-integrations.md`) specifies the inventory fields but does not include a `result_timestamp` or `held_stock_token` field — neither the resolver nor the POS client knows these values exist |

**Evidence to confirm:** inspect the Apollo Gateway resolver for `inventory.pickupCheck` — the resolver maps `quantity` and `sku` but has no `timestamp` or `staleness_ms` field in the response schema.

**Evidence to rule out:** check whether the SAP ECC adapter itself timestamps its responses — if it does not, the fix must be applied at the adapter layer, not just the resolver.

---

## 3. Guard test

The guard test exercises the *condition* (no freshness enforcement) through three different staleness values — not just the original 45s input. If the staleness check is ever removed or bypassed, all three cases must fail.

| ID | Title | Preconditions | Steps | Expected | Category | Priority | Surface |
|---|---|---|---|---|---|---|---|
| GT-01 | SAP result 31s old (just over threshold) blocks pickup confirmation | SAP stub returns in-stock result timestamped 31s ago; item genuinely available | 1. Customer scans QR at POS. 2. SAP stub returns stale result (31s). 3. Observe POS response. | POS blocks confirmation; staleness warning shown to staff with order ID; no stock deducted. | critical-path | 1 | SAP inventory check |
| GT-02 | SAP result 60s old blocks pickup confirmation | SAP stub returns in-stock result timestamped 60s ago; cross-region scenario (IT customer, DE store) | 1. Customer scans QR at München POS. 2. SAP stub returns 60s-stale result. 3. Observe POS response. | POS blocks confirmation; cross-region context preserved in the warning message; no stock deducted; no loyalty credit. | critical-path | 1 | SAP inventory check |
| GT-03 | SAP result 90s old with fashion SKU blocks pickup confirmation | SAP stub returns in-stock result timestamped 90s ago; fashion SKU (different category from GT-01/GT-02) | 1. Customer scans QR at POS with fashion-category order. 2. SAP stub returns 90s-stale result. 3. Observe POS response. | POS blocks confirmation regardless of SKU category; behaviour is consistent across home goods and fashion; no stock deducted. | critical-path | 1 | SAP inventory check |

**Why three cases:** the condition is missing freshness enforcement, not a single bad input. GT-01 tests the boundary (31s, just over), GT-02 tests a different staleness magnitude and a cross-region shape, GT-03 tests a different SKU category. If any of these passes when the fix is absent, the guard test would have missed a regression.

---

## 4. Fix recommendation

**Enforce a 30s maximum staleness on the SAP inventory read at pickup confirmation, and write a held-stock token to the cart event store at reservation time as a compensating signal.**

Specifically:
1. Add a `result_timestamp` field to the Apollo Gateway `inventory.pickupCheck` response schema and populate it from the SAP adapter's read timestamp.
2. In the POS client, compare `result_timestamp` against `now` before accepting the result — if `(now - result_timestamp) > 30s`, block confirmation and surface the staleness warning.
3. At Click & Collect reservation confirmation, write a `held_stock` event (SKU, quantity, store, expiry = reservation time + 48h) to the cart event store — so the POS has a reservation-time snapshot to fall back on if the SAP read is stale or times out.
4. Add GT-01, GT-02, GT-03 to the regression suite so this condition is checked on every SAP adapter change or Apollo Gateway schema update.
