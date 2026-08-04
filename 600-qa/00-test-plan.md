---
case: Meridian Retail Group — Click & Collect
feature: AI-enabled Click & Collect cross-channel pickup flow (Phase 1)
date: 2026-08-04
author: Veronika Zavgorodnia
kata: K 6.W.1
---

# Test Plan — Meridian Click & Collect (Phase 1)

## In scope

1. **Web cart and reservation step** — customer adds item on `meridian.com`, selects Click & Collect, completes a reservation including PSD2 SCA for EU markets.
2. **Identity stitch on first in-store pickup** — customer's web account merges with their existing in-store loyalty account; no duplicate records, no cross-customer data bleed.
3. **SAP inventory check at pickup confirmation** — POS reads SAP inventory at the moment the customer arrives; staleness window must not allow phantom-stock confirmation.
4. **Loyalty-points credit (cross-region)** — points are credited to the customer's loyalty account within the SLA after QR scan, including cross-region orders (e.g., Italian customer, German pickup store).
5. **POS pickup confirmation** — QR scan at counter triggers reservation resolution, SAP deduct, and receipt/notification to customer.

## Out of scope

- **SAP ECC inventory ground-truth correctness** — owned by Finance, covered by their own controls; any defects in SAP's source data are out of scope for this test cycle.
- **Legacy Shopify storefronts** — being strangled away in Phase 1; Click & Collect runs on the new headless platform only.
- **Phase 2 cross-channel inventory reservation patterns** — cross-region multi-currency settlement is a Phase 2 commitment; not testable in Phase 1 QA region.

## Top 3 risks

**Risk 1 — Phantom-stock cancellation at pickup**
The SAP inventory read at pickup confirmation accepts data older than the reservation window, causing the POS to confirm pickup for an item that has already been reserved or removed from stock.
User impact: customer arrives at store, is turned away empty-handed with no immediate refund or alternative offered.
Business impact: replicates or worsens the documented 7% phantom-cancellation rate baseline; directly blocks David Park's approval for country rollout expansion.

**Risk 2 — Identity-merge collision contaminating loyalty history**
The identity stitch writes cross-customer loyalty data when two accounts share an email domain pattern or loyalty tier, merging records that belong to different customers.
User impact: customer sees another customer's order history or loyalty balance; personal data exposure.
Business impact: GDPR Article 5 violation, Asha Sundaram escalation, potential supervisory authority notification; Italy pilot at risk given Marco Rossi's local regulatory sensitivity.

**Risk 3 — PSD2 SCA failure silently cancels EU reservation**
EU customers whose SCA challenge fails during the reservation step have their Click & Collect order cancelled immediately, with no hold period or recovery flow.
User impact: customer believes item is reserved, travels to store, finds order does not exist.
Business impact: EU payment-flow non-compliance; drop-off on Italy and Nordics pilots (Marco Rossi, Klarna markets); Sarah Chen's CX regression concern materialises at launch.

## Entry criteria

1. Phase 1 build (unified identity + cart + checkout) deployed and smoke-tested in the QA region.
2. SAP sandbox seeded with representative inventory snapshots covering all five in-scope surfaces, including at least one cross-region scenario and one low-stock edge case.
3. Identity-provider stub configured for both single-account merge and dual-record collision scenarios, with GDPR-safe synthetic customer data loaded.

## Exit criteria

1. Pass rate ≥ 95% on all priority-1 (critical-path) test cases; no priority-1 case in an open-defect state.
2. Zero phantom-stock cancellations observed across the SAP inventory check test cases — direct regression of the 7% baseline pain point.
3. Named sign-off from David Park (Head of Retail Ops) and Sarah Chen (Head of CX) on the test report before rollout to the next country.
