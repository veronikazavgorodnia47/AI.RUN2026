---
case: A
date: 2026-07-27
version: 1.0
consumes: 00-playground.md, 01-context-brief.md, 02-primary-signal.md, 03-research-audit.md, 04-use-cases.md, 05-canvas.md, 06-roi.md
status: draft — all baselines unverified; confirm with client OMS before exec review
---

# Opportunity Brief — Meridian Retail Group

---

## 1. Problem statement

Mid-market EU fashion retailers operating 22-country omnichannel stacks cannot
promise shoppers accurate click-and-collect availability at order time. Country
inventory systems do not share a live view of stock, so the promise shown to the
shopper is tentative. Orders are confirmed, customers arrive at stores, items are
unavailable. Root cause: no unified available-to-promise signal across 22 systems.

---

## 2. Falsifiable value hypothesis

A real-time inventory availability predictor will reduce click-and-collect
cancellation rate by ≥30% against the 15% sector baseline (unverified),
recovering annualised order value and protecting repeat purchase rate.

**Falsification test:** If the spike shows actual cancellation rate is ≤5%,
or that ≥35% of cancellations are not caused by stock discrepancy between
systems, the value hypothesis does not hold. Stop before the full build.

---

## 3. ROI hypothesis

**Tied metric:** click-and-collect cancellation rate and recovered order value.

| Scenario | One-time cost | Annual run | Annual value | Payback |
|---|---|---|---|---|
| Pessimistic | €4.1M | €500K/yr | €1.4M/yr | ~51 months |
| Base | €2.85M | €280K/yr | €6.2M/yr | ~6 months |
| Optimistic | €1.65M | €150K/yr | €10.5M/yr | ~2 months |

Top sensitivity drivers: cancellation rate baseline (10–15%, unverified) and
C&C revenue base (€80M–€150M, unverified). All assumptions require replacement
with client OMS data and architecture estimates before exec go/no-go.

---

## 4. Target customer / segment

**Primary buyer:** Head of Omnichannel / VP E-commerce, mid-market EU fashion
retailer, €1–5B revenue, Western Europe, 22-country fragmented stack.

**Adjacent stakeholders:** Store operations managers (execution), supply chain
planners (stock allocation), end shoppers (broken availability promise).

Segment characteristics: under margin pressure from both ends (Inditex above,
Shein/Temu below); GDPR and ESPR compliance obligations; store network investment
that needs an omnichannel return.

---

## 5. Four-risk-gate evaluation

| Gate | Signal | Verdict |
|---|---|---|
| **Value** | ≥30% cancellation reduction recovers €5–9M/yr (base–optimistic); weakest assumption is cancellation rate baseline (unverified) | Conditional — validate with client OMS |
| **Usability** | Shopper sees confirmed indicator vs tentative; store staff get at-risk alerts only; behaviour change is minimal | Pass — solution description is behaviour-only |
| **Feasibility** | 22-system API abstraction achievable within 12 months using event-driven layer; blocked by unified data feed requirement | Conditional — architecture spike (3 stacks, 4 weeks) required to confirm |
| **Viability** | Base payback ~6 months if baselines hold; pessimistic 51 months if integration overruns and adoption partial | Conditional — depends on OMS data and architecture estimate |

**Binding gate verdict:** Feasibility is the binding gate. No go to full build
without the architecture spike result. Value gate is contingent on cancellation
baseline confirmation.

---

## 6. Commodity-vs-novel classification

**Novel.** Unified available-to-promise signal across 22 legacy country stacks
requires custom event-driven integration. No off-the-shelf vendor solves this
end-to-end for mid-market EU fashion at this stack fragmentation level.

Commodity components within the solution: ML inference layer (well-established),
notification generation (off-the-shelf), store dashboard UI (commodity). The
novel constraint is the data unification layer — this is the moat.

---

## 7. Responsible-AI section

**Model risk:** Inventory predictor may surface false-confidence signals if
training data is sparse for low-volume SKUs or new-season lines. Mitigation:
confidence interval surfaced to shopper ("available" vs "likely available");
no binary promise on sparse SKUs.

**Fairness:** Algorithmic allocation recommendations must not systematically
disadvantage smaller or lower-revenue stores. Review required before rollout.

**Data handling:** Stock data from 22 country systems may include personally
identifiable commercial data under GDPR. Data pipeline must be GDPR-compliant;
cross-border data flows require legal review per jurisdiction.

**Human oversight:** All fulfillment decisions remain with store staff. The
predictor surfaces signals; no automated cancellation or re-routing without
human confirmation at MVP stage.

---

## 8. Source trail with provenance

| Claim | Source | Status |
|---|---|---|
| Mid-market EU fashion retail under margin squeeze | Strategy& (2026) | sourced |
| ESPR/DPP compliance obligations for EU fashion | European Parliament WFD (2025-09-09) | sourced |
| Inditex stores-plus-digital as benchmark | Inditex FY2025 Annual Report (2026-03-07) | sourced |
| Click-and-collect stock availability issue (Zara "tentative") | Zara product page teardown (2026-07-27) | sourced |
| Shopper verbatims on delivery and tracking failure | Zara App Store reviews, public (2026-07-27) | sourced |
| 15% C&C cancellation rate baseline | Unverified — no external citation found | **unverified** |
| C&C revenue base €80M–€150M | Unverified — estimated from revenue band midpoint | **unverified** |
| 40% fulfillment cost above sector median | Unverified — AI-generated; no external citation | **unverified** |
| Store network trend (Claim 8, K 1.W.4) | Unverified | **unverified** |

All `unverified` claims must be replaced with client data before exec review.

---

## 9. No-go line

**Do not proceed to full build if any of the following are true:**

- Architecture spike shows API integration across 22 stacks requires >24 months
  or >€5M one-time cost (pessimistic case breaks beyond executive tolerance)
- Client OMS data shows actual C&C cancellation rate is ≤5% (value hypothesis fails)
- Legal review finds cross-border stock data flows cannot be GDPR-compliant
  within the 22-country structure without country-by-country data residency
- Responsible-AI review flags unacceptable fairness risk in allocation model
- Client cannot confirm the binding assumption (cancellation root cause) within
  the spike window

**This brief does not constitute a go decision or a client commitment.
Human-owned: problem selection, go/no-go at each stage gate, all stakeholder
commitments.**
