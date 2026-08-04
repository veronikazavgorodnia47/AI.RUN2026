---
case: Meridian Retail Group — Click & Collect
kata: K 6.W.4
date: 2026-08-04
author: Veronika Zavgorodnia
execution_method: Path C — manual observation against Meridian Phase 1 QA stub harness
target: Meridian Phase 1 QA stub harness (commercetools + Apollo GraphQL + SAP ECC read-only sync stub; identity-provider stub configured per K 6.W.1 entry criteria)
cases_run: TC-04, TC-06, TC-09, TC-16
---

# Defect Log — Meridian Click & Collect (Phase 1)

Cases run: TC-04, TC-06, TC-09, TC-16 (top 3 critical-path P1 + highest-priority negative)
Defects found: 3 | Passes: 1

Sorted by priority (P1 first).

---

## DEFECT-01 — Priority 1 | Severity 1

**Title:** Identity stitch merges two unrelated corporate customers sharing an email domain — customer B's loyalty history and order data visible to customer A

**Test case:** TC-06

**Input record:** two synthetic customers — `CUS-IT-00421` (g.ferretti.test@meridian-qa.invalid) and `CUS-DE-00837` (m.schoenberg.test@meridian-qa.invalid) — both registered with a shared corporate domain pattern (`@meridian-partner.com`) in the QA stub.

**Steps to reproduce:**
1. In the identity stub, register two distinct customers with different names, IDs, and loyalty histories but the same corporate email domain.
2. Customer A completes a Click & Collect QR scan at Milano POS, triggering the stitch flow.
3. Immediately after stitch, inspect Customer B's account via the loyalty API (`GET /customers/{id}/profile`).

**Expected:** Customer B's profile, loyalty points, and order history are unchanged. Stitch log records two separate identities for domain-matched records.

**Actual:** Stitch logic matches on email domain prefix (the segment before `@`) rather than exact email address. Customer B's loyalty account is merged into Customer A's record. Customer A's account now shows Customer B's order history and loyalty balance. Customer B's account returns a 404 after the merge.

**Severity:** 1 — GDPR Article 5 violation (personal data of Customer B processed under Customer A's identity without consent). Cross-customer data exposure at POS is immediately visible to store staff.

**Priority:** 1 — blocks Italy pilot ship. Asha Sundaram escalation path active; supervisory authority notification may be required.

---

## DEFECT-02 — Priority 1 | Severity 2

**Title:** SAP timeout during pickup confirmation leaves POS on a blank screen — staff manually proceed without logging the attempt, stock not deducted, no fallback instruction shown

**Test case:** TC-09

**Input record:** `CUS-FR-00712` (Élodie Marchais, Paris Haussmann, STR-FR-PA-005). SAP stub configured to return no response within the 5s SLA.

**Steps to reproduce:**
1. Configure SAP stub to time out (no response within 5s).
2. Customer scans QR code at POS counter.
3. POS sends SAP inventory query; SAP stub does not respond.
4. Observe POS display after 5s timeout elapses.

**Expected:** POS displays a named fallback instruction ("SAP inventory check timed out — contact inventory manager, reference order ORD-FR-20260804-0034"). No stock deducted. Timeout event logged with order ID and timestamp.

**Actual:** POS renders a blank white screen after 5s. No error message. No fallback instruction. Staff, seeing no rejection, manually hand over the item. SAP deduction never fires. Timeout is not written to the event log — the order remains in "pending pickup" state indefinitely.

**Severity:** 2 — customer receives the item but the order stays open; loyalty points are not credited; stock is not deducted in SAP. If the item was phantom stock, the customer received an item that was already reserved for someone else.

**Priority:** 1 — operational risk for David Park; blank screen during a live pilot is a store-staff confidence blocker. Logging gap means support cannot reconstruct what happened post-incident.

---

## DEFECT-03 — Priority 1 | Severity 1

**Title:** POS confirms Click & Collect pickup using a 45-second-stale SAP inventory result — phantom stock delivered to customer, original reservation holder turns away at counter

**Test case:** TC-16

**Input record:** `CUS-IT-00423` (Valentina Russo, cross-region IT→DE, STR-DE-MU-006). SAP stub configured to return an in-stock result timestamped 45s ago.

**Steps to reproduce:**
1. Configure SAP stub to return an in-stock result with a timestamp 45s in the past.
2. Customer scans QR code at München POS.
3. POS sends SAP inventory query; stub returns stale in-stock result.
4. Observe whether POS enforces the 30s freshness ceiling before confirming.

**Expected:** POS detects that the SAP result is 45s old (exceeds the 30s freshness ceiling). POS blocks pickup confirmation. Staff sees a staleness warning with the order ID. No stock deducted.

**Actual:** POS does not inspect the result timestamp. The staleness check is not implemented. POS confirms the pickup, deducts stock, and credits loyalty points — all against a stale inventory snapshot. If the item had been reserved by another customer in the 45s window, the stock deduction creates a phantom pickup for the second customer who then arrives at the counter.

**Severity:** 1 — directly replicates the documented 7% phantom-stock cancellation rate. Customer who reserved the item is turned away with no immediate remedy. Loyalty points credited incorrectly. Revenue impact and David Park rollout-block risk.

**Priority:** 1 — the single highest-risk defect in the suite; the primary exit criterion ("zero phantom-stock cancellations") is already violated by this finding.

---

## PASS

| TC | Result | Notes |
|---|---|---|
| TC-04 | PASS | Identity stitch on first in-store pickup completed correctly; single merged record; all loyalty points preserved; no duplicate account created. |

---

## Stories (not reproducible, leads for next session)

- During TC-06 reproduction, the loyalty API briefly returned a 500 error on the first `GET /customers/{id}/profile` call before succeeding on retry. Could not reproduce consistently — possible intermittent stub issue, not filed as a defect.
