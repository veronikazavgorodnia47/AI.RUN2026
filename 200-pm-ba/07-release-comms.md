---
consumes_from: 06-prd.md, 06-traceability.md
date: 2026-07-28
---

## 1 — Release-scope confirmation

### In scope (shipped)

| Story | What ships |
|---|---|
| **S1** — Availability verdict display | Three-tier verdict (Available / Low stock / Uncertain) on the product page C&C flow; loading state; WCAG 2.1 AA |
| **S2** — Multi-signal confidence scorer | Five-signal AI model computing the confidence score behind S1; degraded-mode trigger when < 2 fresh signals |
| **S3** — Nearest alternative store | Surfaces nearest store within 25 km with Available verdict on Uncertain; re-queries at navigation; GDPR-compliant location flow |
| **S4** — Degraded mode (launch gate) | Fallback message + last-known count + staleness timestamp when signals are stale; observability logging and alerting |
| **S5** — Size/colour-specific verdict | Confidence score calculated at SKU + size level; verdict refreshes on variant change |

### Out of scope

- Reserve-and-hold / slot locking
- In-store staff notifications
- Stock replenishment triggers
- Availability checks for delivery (non-C&C) orders

### Deferred (post-launch)

- S6 — Data freshness indicator (no user research to validate; deferred pending post-launch signal)
- S8 — Mobile optimisation polish (sprint 2)
- S9 — Auditability dashboard for store operations (post-launch tooling track)
- S10 — Analytics by verdict type (BI/data track; runs in parallel, not gating launch)

---

## 2 — Open risks

| Risk | Owner | Mitigation |
|---|---|---|
| **OMS data quality** — the 7% phantom-stock baseline may be unreliable due to inconsistent manual cancellation-reason logging; if the baseline is wrong, the 90-day success measurement is unfalsifiable | Operations Analytics | Complete OMS cancellation-reason data-quality audit before GA; if the field fails the audit, agree a matched-control-store comparison as the primary measurement method before launch |
| **Signal availability (S2)** — staff scan events require a DPIA as employee personal data under GDPR; if the DPIA is not cleared before build, one of the five model signals is unavailable, reducing confidence precision | Engineering + Legal | Run a 2-week signal-availability spike in 3 pilot stores before full build commitment; if DPIA blocks staff scan events, fall back to a 4-signal model and re-baseline the 90-day precision target |
| **EU AI Act / GDPR compliance** — AI-generated verdicts influencing consumer purchasing decisions may require transparency disclosures (Article 13); S3 location processing requires an explicit lawful basis and session-only retention | Legal / Compliance | Legal review must complete before GA; contingency: add an optional "how we calculated this" disclosure layer (also partially satisfies Article 13 transparency) |

---

## 3 — Stakeholder notifications

### Delivery leads and engineering teams

**Subject:** AI availability assistant — GA scope, risks, and launch readiness

**Scope shipped:** S1–S5 as specified in `06-prd.md`. S6, S8, S9, S10 deferred.

**Three open risks requiring action before GA:**
1. OMS data-quality audit — Operations Analytics to confirm or replace the 7% baseline. Gate: audit complete and measurement method agreed.
2. Signal-availability spike — Engineering to complete 3-store pilot before full S2 build commitment. Gate: spike results reviewed; fallback model scoped if needed.
3. Legal review — Compliance to sign off on GDPR location-data flow (S3) and EU AI Act Article 13 transparency obligations. Gate: legal sign-off before GA.

**Metrics baseline:** 90-day measurement window starts on GA date. Matched-control-store comparison is the primary attribution method. Product Analytics and Operations Analytics to confirm instrumentation is live on day 1.

---

### Business and external stakeholders

**Subject:** What's shipping — AI availability assistant for click-and-collect

We're launching a new feature that tells shoppers whether an item will actually be on the shelf at their collection store before they reserve it.

**What it does:**
- Before reserving, shoppers see a plain-language signal: Available, Low stock, or Uncertain — based on real-time store data, not just the website's stock count.
- When a store shows Uncertain, we surface the nearest store where the item is confirmed available.
- The check is specific to the shopper's chosen size and colour.

**Why it matters:** Our current click-and-collect cancellation rate at pickup is approximately 7%. This feature is designed to reduce that to 2% or below within 90 days, by giving shoppers the confidence to choose a different store or time rather than arriving to find the item absent.

**Timeline:** General availability [date TBD — to be confirmed once launch gates clear]. Initial rollout to [pilot market TBD]; full 22-country rollout in sprint 2.

---

## 4 — What's New / release note

*Traceability check: each bullet verified against `06-traceability.md` before inclusion.*

**AI availability assistant — now live for click-and-collect**

- **Know before you go.** Before reserving an item for collection, you'll see a real-time availability signal — Available, Low stock, or Uncertain — based on live store data, not just the website count. *(traces to S1, S2 ✓)*
- **Honest about uncertainty.** When stock is uncertain, we tell you — and show you the nearest store where the item is confirmed available, so you can redirect your trip rather than discover the problem at the collection desk. *(traces to S3 ✓)*
- **Right for your size.** The availability check is specific to the size and colour you've selected, not a generic stock total. *(traces to S5 ✓)*
- **Always accessible.** If live data is temporarily unavailable, the feature shows the last-known stock count with a timestamp and keeps the reservation option open. *(traces to S4 ✓)*

*Cut: no bullets about reserve-and-hold (out of scope), raw confidence percentages (not shipped), or staff notifications (out of scope). All four bullets trace to shipped stories.*

---

## 5 — Spec sections to update after release

1. **`01-vision.md` — Outcome metrics section:** Replace the `[unverified]` 7% baseline with the audited figure once the OMS data-quality audit completes. Record actual day-90 cancellation rate vs. the ≤2% target and the repeat C&C usage delta vs. the +5pp target.
2. **`06-prd.md` — Status field:** Update from `draft — pending OMS data-quality audit and S2 signal-availability spike` to `shipped` with the GA date and actual launch scope.
3. **`06-traceability.md`:** Add a "post-launch signal" column recording whether each linked metric moved in the predicted direction within 90 days.
