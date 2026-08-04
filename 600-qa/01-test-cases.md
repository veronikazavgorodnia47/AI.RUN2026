---
case: Meridian Retail Group — Click & Collect
feature: AI-enabled Click & Collect cross-channel pickup flow (Phase 1)
date: 2026-08-04
author: Veronika Zavgorodnia
kata: K 6.W.2
consumes_from: K 6.W.1 → 00-test-plan.md
---

# Test Cases — Meridian Click & Collect (Phase 1)

## In-scope reference (from 00-test-plan.md)

1. Web cart and reservation step
2. Identity stitch on first in-store pickup
3. SAP inventory check at pickup confirmation
4. Loyalty-points credit (cross-region)
5. POS pickup confirmation

---

## Seeds (hand-written, one per surface)

1. **Web reservation** — Italian customer reserves a home-goods item on `meridian.com` using Postepay, selects Milano store, completes Click & Collect reservation.
2. **Identity stitch** — Customer completes first in-store pickup after web sign-up, triggering merge between their web account and existing in-store loyalty card.
3. **SAP inventory check** — Customer arrives at store 23h into the 48h window; POS reads SAP inventory to confirm item is still available.
4. **Loyalty credit (cross-region)** — UK customer reserves item online, picks up at German store; loyalty points credited to their account within SLA after QR scan.
5. **POS confirmation** — Customer scans QR code at POS counter; reservation is resolved, SAP deducts stock, customer receives receipt/notification.

---

## Test case suite

| ID | Title | Preconditions | Steps (≤4) | Expected | Category | Priority | Surface |
|---|---|---|---|---|---|---|---|
| TC-01 | German customer completes Click & Collect reservation via Klarna | Phase 1 QA build live; Klarna stub active for DE market; item in stock at Hamburg store | 1. Sign in as DE customer. 2. Add item to cart, select Click & Collect → Hamburg. 3. Complete Klarna split-pay SCA. 4. Confirm reservation. | Reservation confirmed; confirmation email received within 60s; order visible in account history. | smoke | 2 | Web reservation |
| TC-02 | Reservation attempted at 47h59m of the 48h pickup window | Existing reservation at 47h59m remaining; QA clock set to boundary time | 1. Open reservation link. 2. Attempt to confirm pickup slot at T-00h01m. | System accepts the reservation; window end-time displayed correctly; no premature expiry error. | edge | 3 | Web reservation |
| TC-03 ⛔ | PSD2 SCA failure rejects EU reservation and preserves cart | EU customer (IT) with Postepay; SCA stub configured to return failure | 1. Add item to cart, select Click & Collect → Milano. 2. Reach SCA challenge step. 3. Fail SCA (stub returns reject). | System rejects the reservation; cart is preserved with item still present; retry prompt displayed; order is NOT created. | critical-path | 1 | Web reservation |
| TC-04 | First in-store pickup stitches web and loyalty accounts | Customer has web account (email) and in-store loyalty card (IT, same email); no prior stitch | 1. Sign in to web account. 2. Complete Click & Collect pickup at Milano POS (QR scan). 3. Check account post-pickup. | Identity stitch completes; single merged record shown; all legacy loyalty points preserved; no duplicate account. | critical-path | 1 | Identity stitch |
| TC-05 | Dual-tier loyalty merge resolves to higher tier | Customer has Silver loyalty card (DE) and Gold loyalty card (IT) with same email; first cross-region pickup | 1. Complete Click & Collect pickup at Hamburg POS with IT loyalty number. 2. Check merged account tier. | Accounts merged to single record; customer retains Gold tier; merge event logged in account history. | edge | 2 | Identity stitch |
| TC-06 ⛔ | Corporate email domain must not merge two distinct customers | Two unrelated customers share `@company.com` domain; both have loyalty accounts | 1. Customer A completes Click & Collect pickup. 2. Inspect Customer B's account immediately after stitch logic runs. | Customer B's record is unchanged; no cross-customer data visible in Customer A's account; stitch log shows two separate identities. | critical-path | 1 | Identity stitch |
| TC-07 | SAP inventory confirmed fresh at pickup 6h post-reservation | Customer reserved 6h ago; item confirmed in stock in SAP sandbox; SAP freshness < 30s | 1. Customer arrives at French store. 2. Staff scans QR at POS. 3. POS queries SAP. | SAP returns in-stock result; POS confirms pickup; flow completes. | smoke | 2 | SAP inventory check |
| TC-08 | SAP inventory read at exact 30s staleness boundary triggers re-query | SAP sandbox configured to return a result timestamped exactly 30s old | 1. Staff scans QR at POS. 2. POS receives SAP result with 30s-old timestamp. | System treats result as at the staleness boundary; re-queries SAP before confirming; does not use stale result to confirm pickup. | edge | 1 | SAP inventory check |
| TC-09 ⛔ | SAP timeout at pickup blocks confirmation and surfaces fallback | SAP sandbox configured to return timeout (no response within SLA) | 1. Customer arrives at store. 2. Staff scans QR. 3. SAP query times out. | POS does not confirm pickup; staff sees a named fallback instruction (e.g., "Contact inventory manager — reference order ID"); no stock is deducted. | critical-path | 1 | SAP inventory check |
| TC-10 | Cross-region loyalty points credited within 60s (IT customer, UK pickup) | Italian customer with valid loyalty account; item reserved online; UK store in QA region | 1. Customer scans QR at UK POS. 2. Pickup confirmed. 3. Check loyalty account after 60s. | Points credited to Italian loyalty account within 60s; correct points value per item; cross-region flag in transaction log. | critical-path | 1 | Loyalty credit |
| TC-11 | Dual-region loyalty records receive exactly one points credit, no duplication | Customer has two regional loyalty records (IT + JP) linked to same email; pickup at UK store | 1. Complete Click & Collect pickup at UK POS. 2. Check IT loyalty account. 3. Check JP loyalty account. | Points credited to exactly one record (IT, higher tier); JP record unchanged; no duplicate credit. | edge | 2 | Loyalty credit |
| TC-12 ⛔ | Inactive loyalty card receives no points and surfaces resolution prompt | Customer's loyalty number on reservation belongs to an expired/inactive account | 1. Customer scans QR at POS. 2. Pickup confirmed. 3. Loyalty credit step executes. | No points credited; staff and/or customer sees a resolution prompt ("Loyalty account inactive — contact support"); transaction log notes skip with reason. | regression | 3 | Loyalty credit |
| TC-13 | QR scan at Madrid POS confirms reservation, deducts stock, notifies customer within 30s | Reservation active; item in stock at Madrid store; customer push notifications enabled | 1. Customer scans QR at POS. 2. POS confirms reservation with SAP. 3. Stock deducted. 4. Push notification sent. | All four outcomes complete within 30s of QR scan; customer receives notification; POS displays success confirmation. | critical-path | 1 | POS confirmation |
| TC-14 | Multi-item order partially fulfilled when one item unavailable at pickup | 2-item reservation; SAP confirms item A in stock, item B out of stock at pickup time | 1. Customer scans QR at POS. 2. POS queries SAP for both items. 3. Item B returns zero stock. | Item A confirmed and deducted; item B surfaced as unavailable; staff offered alternative or refund flow for item B; overall order not abandoned silently. | edge | 2 | POS confirmation |
| TC-15 ⛔ | Duplicate QR scan rejected — no second stock deduction | Reservation already completed and QR scan used once (status: fulfilled) | 1. Customer or staff scans the same QR code a second time at the same or different POS. | POS rejects the scan with an "already fulfilled" message; no additional stock deducted; no duplicate loyalty credit triggered; attempt logged. | regression | 2 | POS confirmation |
| TC-16 ⛔ | SAP returns 45s-stale inventory data — POS must block pickup confirmation | SAP sandbox configured to return an in-stock result timestamped 45s ago (exceeds 30s freshness ceiling) | 1. Customer arrives at store. 2. Staff scans QR at POS. 3. SAP returns stale in-stock result (45s old). | POS blocks pickup confirmation; does not use stale result to proceed; staff sees a freshness-failure message with order ID; no stock deducted. | critical-path | 1 | SAP inventory check |

---

## Summary

| | Count |
|---|---|
| Total cases | 16 |
| Critical-path | 7 (TC-03, TC-04, TC-06, TC-09, TC-10, TC-13, TC-16) |
| Smoke | 2 (TC-01, TC-07) |
| Edge | 5 (TC-02, TC-05, TC-08, TC-11, TC-14) |
| Regression | 2 (TC-12, TC-15) |
| **Explicit negatives ⛔** | **6 (TC-03, TC-06, TC-09, TC-12, TC-15, TC-16)** |
| Priority 1 | 8 (TC-03, TC-04, TC-06, TC-08, TC-09, TC-10, TC-13, TC-16) |
| Priority 2 | 6 |
| Priority 3 | 2 |

Every in-scope surface has at least one smoke/critical-path case and one explicit negative.
Risk 1 (phantom-stock) now covered by TC-08 (boundary P1), TC-09 (timeout P1), and TC-16 (stale data negative P1).
