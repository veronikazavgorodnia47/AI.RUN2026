---
consumes_from: 00-feature.md, 01-vision.md, 02-personas-journey.md, 04-stories-acs.md, 05-backlog-notes.md
date: 2026-07-28
status: draft — pending OMS data-quality audit and S2 signal-availability spike
---

## Problem

Meridian loses ~7% of click-&-collect orders to pickup cancellation because the product page displays SAP inventory counts that diverge from physical shelf reality ("phantom stock"). Shoppers make wasted trips; channel trust erodes; repeat C&C usage declines. Existing workarounds — phoning the store, applying personal stock-count heuristics — are high-friction and unreliable. `[7% baseline: Meridian internal OMS report Q4 2025 — unverified; audit required before baseline is locked]`

---

## Vision

For Meridian shoppers on the product page about to reserve an item for click-&-collect, the AI availability assistant is the decision layer between the SAP inventory count and the physical shelf. It combines five signals — SAP inventory delta, POS transaction recency, store staff scan events, historical phantom-stock rate per store/SKU/size (30-day rolling), and day-of-week pickup demand — to return one of three plain-language verdicts: **Available** (≥ 80% confidence), **Low stock** (50–79%), or **Uncertain** (< 50%). When stock is uncertain, the nearest store with a confirmed Available verdict is surfaced. Phantom-stock cancellations fall from ~7% to ≤ 2%; repeat C&C usage recovers.

---

## Target users

| Persona | Behaviour | Failure today |
|---|---|---|
| **Clara — Careful Planner** | High-intent, prior phantom-stock experience; phones store before reserving | 5–10 min call per order; call often inconclusive; at risk of channel abandonment |
| **Ben — Time-Poor Opportunist** | Mobile, <90-second sessions; self-invented "10+ units" heuristic | Burned during high-demand periods; declining C&C frequency |

Both need one trustworthy signal before committing — no call, no heuristic.

---

## Top stories and acceptance criteria (compressed)

**S1 — Availability verdict** *(P1)*
- Given size + colour selected → verdict Available / Low stock / Uncertain in ≤ 5 s
- Variant change → verdict clears; re-query required
- No size/colour selected → prompt; no verdict shown
- WCAG 2.1 AA required (22 EU countries)

**S2 — Multi-signal confidence scorer** *(P1 — AI story)*
- Confidence thresholds: ≥ 80 = Available; 50–79 = Low stock; < 50 = Uncertain (boundary inclusive at upper tier)
- Signal "available" = present AND fresh (SAP lag ≤ 4 h; POS within 24 h rolling; scan events within 24 h)
- < 2 of 5 fresh signals → degraded mode (not a verdict)
- Score outside 0–100 or null → fallback to SAP count + staleness timestamp; no verdict label
- Staff scan events: anonymised/aggregated before use; DPIA required
- Eval target: ≥ 90% precision on Available verdicts; ≤ 20% false-negative rate; measured at 90 days post-launch

**S3 — Nearest alternative store** *(P1)*
- Uncertain verdict → nearest store within 25 km (road distance) with Available verdict shown
- Equidistant tie → higher confidence score wins
- No available store in radius → "No nearby store currently shows confirmed availability"
- Location: explicit GDPR lawful basis required; session-only retention; privacy notice before prompt
- Re-query at target store when shopper taps through (verdict may have changed)

**S4 — Degraded mode** *(P1 — launch gate)*
- SAP lag > 4 h OR < 2 POS events in rolling 24 h → degraded message + last-known count + staleness timestamp
- Signal API timeout → degraded mode within 8 s total; no error code surfaced
- SAP + model both down → degraded message only; no count shown
- Reservation CTA always visible; degraded-mode triggers logged + alerting if > 10% of checks in rolling hour

**S5 — Size/colour-specific verdict** *(P2, low marginal effort)*
- Phantom-stock rate signal calculated at SKU + size level; changing size or colour triggers a new query

---

## Scope boundary

| In | Out | Deferred |
|---|---|---|
| Availability verdict (S1) | Reserve-and-hold / slot locking | Data freshness indicator (S6) — no user research yet |
| AI confidence scorer (S2) | In-store staff notifications | Auditability dashboard (S9) — post-launch |
| Nearest alternative store (S3) | Stock replenishment triggers | Analytics by verdict type (S10) — BI/data track |
| Degraded mode (S4) | Availability for delivery orders | Mobile optimisation polish (S8) — sprint 2 |
| Size/colour-level scoring (S5) | | |

---

## Success metrics

| Metric | Baseline | Target | Measurement | Owner |
|---|---|---|---|---|
| Phantom-stock cancellation rate | ~7% `[unverified]` | ≤ 2% | OMS cancellation reason vs. matched-control stores; 30-day rolling window from GA | Operations analytics |
| Repeat C&C usage — Uncertain/Low-stock verdict recipients | TBD at launch | ≥ +5 pp vs. baseline | OMS session cohort, 60 days post-launch | Product analytics |

**Prerequisite:** OMS cancellation-reason data-quality audit must confirm the 7% baseline before metrics are locked. Fallback: store-staff-logged cancellation log or post-cancellation survey score ≥ 3.5 / 5.0.

---

## Decision Memory — DM-200-001

**Decision:** Surface a three-tier plain-language verdict (Available / Low stock / Uncertain) to shoppers rather than a raw probability percentage.

**Reason:** A numeric probability (e.g., "64% likely in stock") shifts the interpretation burden to the shopper and introduces a false precision signal — the model's confidence interval at launch is too wide to support a percentage display without misleading users. A three-tier verdict communicates the actionable outcome (proceed / proceed-with-caution / seek-alternative) without implying unwarranted precision.

**Rejected alternative:** Show raw confidence percentage with a tooltip explaining the model. Rejected because: (1) tooltip comprehension rates on mobile are low; (2) a percentage implies calibration accuracy we cannot guarantee at launch; (3) competitor benchmarking (Zara, IKEA) confirms plain-language verdict is the readable pattern in this category.

**Revisit trigger:** If post-launch data shows > 15% of shoppers tap for more detail on the verdict, revisit adding an optional "how we calculated this" disclosure layer (EU AI Act Article 13 may require this anyway).
