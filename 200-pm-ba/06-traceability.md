---
consumes_from: 06-prd.md, 04-stories-acs.md, 01-vision.md
date: 2026-07-29
---

## Traceability matrix

Rows = top stories. Columns = outcome metrics from `01-vision.md`.

| Story | Metric A: Phantom-stock cancellation rate (7% → ≤2%) | Metric B: Repeat C&C usage — Uncertain/Low-stock recipients (+5pp) | How it moves the metric |
|---|---|---|---|
| **S1 — Availability verdict display** (includes former S7: Uncertain verdict → CTA remains visible) | ✓ Primary | ✓ Supporting | Shoppers with an accurate verdict before reserving are less likely to arrive at a phantom-stock situation; direct reduction in cancellation rate. The non-blocking Uncertain path (S7 content) ensures Uncertain verdicts convert to reservations rather than dead-ends, preserving the journey. |
| **S2 — Multi-signal confidence scorer** | ✓ Primary | ✓ Supporting | S1 without S2 is just a relabelled SAP count; the model is what makes the verdict accurate enough to reduce cancellations — S2 is the mechanism behind Metric A |
| **S3 — Nearest alternative store** | ✓ Supporting | ✓ Primary | Converts Uncertain verdicts from abandoned journeys into completed purchases at an alternative store; directly reduces cancellations from phantom stock at the original store; re-engages shoppers who would otherwise exit |
| **S4 — Degraded mode** | ✓ Supporting | — | Prevents false-confidence verdicts when signals are stale; without S4, a degraded signal could produce a spurious Available verdict that increases cancellations rather than reducing them |
| **S5 — Size/colour-specific verdict** | ✓ Primary | — | Phantom-stock rate varies by size (popular sizes stock out faster); a verdict calculated at SKU-only level systematically overestimates availability for popular sizes — S5 is a precision requirement for Metric A |

---

## Coverage check

| Metric | Stories linked | Gap? |
|---|---|---|
| A — Phantom-stock cancellation rate | S1, S2, S3, S4, S5 | None — all five top stories contribute |
| B — Repeat C&C usage (Uncertain/Low-stock recipients) | S1, S2, S3 | S4 and S5 do not directly affect repeat usage; acceptable — they are accuracy/reliability stories, not trust-recovery stories |

**Stories with no linked metric:** S8 (mobile polish), S9 (auditability), S10 (analytics). These are delivery enablers, not outcome drivers. Acceptable for deferred/post-launch scope.

**S7:** Removed as standalone story. Content merged into S1 (AC: "Uncertain verdict — CTA visible"). No separate traceability row required.

**Metrics with no linked story:** None — both metrics have at least one story.

---

## Dependency chain

The stories are not independent. The delivery sequence implied by traceability:

```
S2 (confidence scorer)
  └─▶ S5 (size/colour scoring — depends on S2 signal model)
        └─▶ S1 (verdict display — depends on S2+S5 producing accurate scores)
              ├─▶ S3 (alternative store — fires only when S1 returns Uncertain)
              └─▶ S4 (degraded mode — ships with S1 as a launch gate)
```

Metric A cannot be measured until S1 + S2 are live. Metric B cannot be measured until S3 is live. S4 must ship with S1 — it is a launch gate, not an optional story.
