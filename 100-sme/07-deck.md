---
case: A
date: 2026-07-27
consumes: 05-canvas.md, 06-roi.md
use_case: "#4 — Real-time inventory availability predictor"
export: print to PDF via Gamma, Google Slides, or browser print
---

## Slide 1 — Context

Mid-market EU fashion retail, Western Europe, €1–5B revenue. Fragmented 22-country stacks.
GDPR and ESPR compliance pressure. Omnichannel promise outpacing operational capability.

*(22 words)*

> **Speaker note:** Meridian sits in a segment under pressure from both ends — Inditex above,
> Shein below. The 22-country fragmentation isn't tech debt — it's blocking the business model.

---

## Slide 2 — Problem

Shoppers reserve click-and-collect orders, arrive at stores, find items unavailable.
Root cause: 22 country inventory systems do not share a live view of stock.

*(24 words)*

> **Speaker note:** Zara's own site says availability is "tentative." For a benchmark player
> that's acceptable. For a mid-market retailer justifying store investment, it's a broken promise.

---

## Slide 3 — Opportunity

Real-time inventory availability prediction across all stores. Replace tentative stock signals
with a confidence-adjusted available-to-promise score per SKU.

*(18 words)*

> **Speaker note:** The data already exists across 22 systems — it just isn't unified.
> We're not asking for new data collection; we're asking for an aggregation layer.

---

## Slide 4 — Solution

A live available-to-promise signal at the product page. Confirmed availability, not tentative
guesses. Store staff alerted only when a confirmed order is at risk.

*(27 words)*

> **Speaker note:** The back end is invisible to the shopper. What changes is the certainty
> of the promise on the product page.

---

## Slide 5 — Value

≥30% reduction in click-and-collect cancellations against 15% sector baseline. Recovered order
value. Protected repeat purchase rate. Benchmark: Inditex stores-plus-digital model.

*(22 words)*

> **Speaker note:** The 30% threshold needs validating against client OMS data — it's the
> weakest number in this case. We confirm it in the spike.

---

## Slide 6 — ROI

Base case: €6.2M annual value, €2.85M one-time cost, 6-month payback.
Pessimistic: 51 months. All baselines unverified — confirm with client OMS data.

*(25 words)*

> **Speaker note:** The pessimistic case is honest — 51 months if integration overruns and
> adoption is partial. The base case is compelling but depends on the cancellation baseline.

---

## Slide 7 — Risks

Binding gate: cancellation rate baseline unverified. If actual rate is 5%, annual value drops
60%. Integration overrun risk on 22-system scope.

*(23 words)*

> **Speaker note:** The architecture spike answers both risks in 4 weeks. That's what the ask
> buys — de-risked investment, not just a feasibility check.

---

## Slide 8 — Ask

One architecture spike: 3 representative stacks, 4 weeks, 2 engineers. Validate integration
feasibility and confirm cancellation rate baseline from client OMS.

*(22 words)*

> **Speaker note:** We're not asking for the full build budget. We're asking for 4 weeks
> to answer the question that decides everything.

---

## Slide 9 — Timeline

Month 1–2: spike and baseline validation. Month 3–6: MVP on 3 stacks.
Month 7–12: rollout to 22 stacks. Month 13+: optimisation.

*(22 words)*

> **Speaker note:** 12 months to full rollout assumes a clean integration. The pessimistic case
> assumed 18. The spike narrows that range.

---

## Slide 10 — Next steps

Decision needed: approve architecture spike (est. €80K). Owner: Head of Omnichannel.
Deadline: TBD. Spike kickoff within 2 weeks of approval.

*(20 words)*

> **Speaker note:** One decision. Everything else flows from it. If the spike shows the baseline
> is wrong, we stop before spending €2.5M.
