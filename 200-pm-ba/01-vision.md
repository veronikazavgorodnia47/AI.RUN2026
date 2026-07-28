---
consumes_from: 00-feature.md
date: 2026-07-28
---

## Problem statement

Meridian loses ~7% of click-&-collect orders to cancellation at pickup because the product page displays SAP inventory counts that diverge from physical shelf reality ("phantom stock"), damaging customer trust and inflating operational cost across 1,400 stores.

## Target user

Click-&-collect shoppers actively browsing the Meridian product page who are about to commit to a reservation — specifically those with a prior collection history, where a repeated phantom-stock disappointment is most damaging to channel trust and most likely to trigger permanent channel abandonment.

## Vision

For Meridian shoppers on the product page who are about to reserve an item for click-&-collect, the AI availability assistant is the decision layer between the SAP inventory count and the physical shelf. It combines three input signals — SAP inventory delta since last sync, POS transaction recency at the target store, and store staff scan events — with two behavioural pattern types — historical phantom-stock rate per store/SKU pair (rolling 30 days) and day-of-week pickup demand at that store — to produce a numeric confidence score. That score maps to one of three plain-language verdicts:

- **Available** (confidence ≥ 80 %): shopper may proceed to reserve without friction.
- **Low stock** (confidence 50–79 %): shopper sees a warning and can still reserve.
- **Uncertain** (confidence < 50 %): shopper is shown the nearest store with an Available verdict; reservation at the original store is permitted but de-emphasised.

When signals are unavailable (SAP sync lag > 4 h, or < 2 POS events in 24 h at the target store), the assistant degrades gracefully: it shows "Live availability check unavailable — stock data may be delayed" and allows reservation without a confidence verdict.

The result is fewer wasted trips, lower operational cancellation cost, and measurable recovery of repeat click-&-collect usage.

## Outcome metrics

**Primary — cancellation rate**  
Reduce phantom-stock cancellations at pickup from ~7% to ≤2% of click-&-collect orders within 90 days of launch.  
- Source of 7% baseline: Meridian internal OMS report Q4 2025 (operations analytics) — `unverified; must be confirmed before baseline is locked`.  
- Measurement period: rolling 30-day window starting day 1 of general availability.  
- Attribution rule: cancellation rate is compared against a matched control group (stores without the feature, same SKU categories, same region) to isolate feature impact from seasonal or operational confounds.  
- Measurement: OMS cancellation-reason field "item not on shelf at collection."  
- **Prerequisite:** OMS cancellation-reason data quality audit required before baseline is locked. If the field is inconsistently populated, primary metric switches to store-staff-logged cancellation log (operations analytics to confirm).  
- Measurement owner: operations analytics team.

**Secondary — channel trust proxy**  
Repeat click-&-collect usage rate among shoppers who received an Uncertain or Low-stock verdict in their prior session, measured 60 days post-launch. A ≥ 5 percentage-point increase versus baseline indicates rebuilt channel trust.  
Fallback proxy if repeat-usage data is unavailable: post-cancellation survey score (target: cancellation satisfaction ≥ 3.5 / 5.0).

---

## AI critique log (fresh session)

**Critique 1 — Signal definition is a black box.**
"Synthesises real-time inventory signals with store-level behavioural patterns" names no actual signal. SAP delta, POS recency, RFID, shrinkage rates, and staff scan events all have different integration costs and data availability across 1,400 stores. "Behavioural patterns" is undefined — whose behaviour, over what window, at what granularity, updated how often? Without this, the confidence indicator has no computable definition and the engineering team cannot scope the work.

**Critique 2 — The outcome metric is unmeasurable as stated.**
The metric relies on OMS cancellation reasons being logged accurately as "item not on shelf at collection," but in a 1,400-store operation with manual staff categorisation that field is likely a garbage bucket. If the baseline 7% figure derives from the same unreliable field, the starting point is unverified and the 90-day delta is unfalsifiable. No measurement owner, audit plan, or confound exclusion is named.

**Critique 3 — The target user includes people the product cannot reach.**
"Buyers who now avoid the channel altogether" are not using click-&-collect and will never see the feature. The vision offers no re-engagement mechanism, making part of the user group fictional from a delivery standpoint. The remaining in-channel users are described only by a negative emotional state, leaving design with no behavioural proxy for targeting or usability testing recruitment.

---

## Revisions made

| Gap | Change |
|---|---|
| Signal black box (session 1) | Named three input signals: SAP delta, POS recency, staff scan events |
| Metric unmeasurable (session 1) | Added OMS audit prerequisite, named measurement owner, proxy fallback |
| Target user fictional (session 1) | Narrowed to in-session, in-channel shoppers about to reserve |
| Confidence indicator undefined (session 2) | Named input signals + two pattern types; defined thresholds (≥80% / 50–79% / <50%) |
| Behaviour patterns vague (session 2) | Explicit list: historical phantom-stock rate per store/SKU (30-day rolling), day-of-week pickup demand |
| Post-verdict action missing (session 2) | Defined block/warn/inform per verdict tier: Available = proceed, Low stock = warn + allow, Uncertain = suggest alternative + de-emphasise original |
| Fallback unspecified (session 2) | Degraded-mode spec: SAP sync lag > 4 h or < 2 POS events → show disclaimer, allow reservation |
| "Trust" metric unmeasured (session 2) | Added secondary metric: repeat C&C usage rate among Uncertain/Low-stock verdict recipients; fallback to post-cancellation survey score |
| 7%→2% unsourced (session 2) | Cited Q4 2025 OMS report (unverified), added attribution rule (matched control group), defined measurement period |
