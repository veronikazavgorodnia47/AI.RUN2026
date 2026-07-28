---
consumes_from: 00-feature.md, 02-personas-journey.md
date: 2026-07-28
research_status: unverified — built from model training knowledge; validate competitor feature details before using in stakeholder materials
---

> **Research note:** Web search was unavailable. Competitor feature descriptions are based on model training knowledge of publicly observable product behaviour. Claims marked `[unverified]` need validation against current product screenshots, app-store listings, or published reviews before committing.

---

## Comparison table

| | **IKEA** | **Zara** | **M&S** | **Us — Meridian (current)** |
|---|---|---|---|---|
| **Approach** | Shows exact unit count per store with last-sync timestamp and aisle/bin location | In-app "Find in store" with size/colour granularity; "Reserve in store" in some markets | Standard C&C with store-level stock check at reservation time; pickup confirmation sent when order is ready | SAP inventory count on product page; C&C reservation accepted if count > 0 |
| **Strength** | Transparent about data freshness (shows sync lag); RFID in warehouses gives high accuracy for large items `[unverified — RFID rollout scope]` | Size-level granularity; fast mobile UX; tightly integrated with their fulfilment model | Reliable operational process; strong pickup notification discipline | Integrated with existing SAP stack; no new infrastructure required |
| **Weakness** | No confidence scoring or predictive signal; RFID works for flat-pack goods but degrades for loose or frequently-moved fashion items; no alternative-store suggestion | Binary available/unavailable — no confidence indicator; high phantom-stock rate for fashion (items tried on, misplaced, misscanned); no visible fallback to nearest alternative store `[unverified]` | Stock check is a point-in-time snapshot at reservation — no signal about stock changes between reservation and collection; no confidence level shown | No confidence signal; no sync-lag transparency; 7% phantom-stock cancellation rate; no fallback store suggestion; no AI layer |
| **Differentiator dimension** | Data freshness transparency | Size/colour granularity | Operational reliability post-reservation | — |

---

## Named differentiator

**Estimate real shelf probability with a calibrated confidence level and a named fallback store — not just a binary stock count.**

All three competitors show whether stock exists at the time of the query. None of them:
- signals *how likely* that count reflects physical shelf reality (confidence scoring),
- surfaces the signal *recency* behind the verdict in a user-facing way,
- or proactively offers an alternative store when confidence is low.

The gap is not better data — IKEA has strong data discipline. The gap is translating uncertain inventory data into an honest, actionable decision for the shopper. Meridian can own that dimension in fashion C&C.

---

## AI capability

**Multi-signal confidence scorer for shelf availability.**

No competitor in the scan ships a user-facing confidence score derived from multiple real-time signals for fashion click-and-collect. The AI capability to carry forward:

> The assistant combines SAP inventory delta (since last sync), POS transaction recency at the target store, and store staff scan events with two behavioural pattern types — historical phantom-stock rate per store/SKU pair (30-day rolling) and day-of-week pickup demand — to produce a numeric confidence score that maps to Available / Low stock / Uncertain.

What this borrows from the scan:
- From **IKEA**: the principle of surfacing data freshness (sync-lag transparency) as a trust signal — applied here as an input to the confidence score rather than a raw timestamp.
- From **Zara**: size/colour granularity as a model input dimension (phantom-stock rate should be calculated at SKU + size level, not just SKU).

What no competitor currently does: expose the confidence score to the shopper in plain language, and pair an Uncertain verdict with a nearest-alternative store suggestion.

This AI capability carries into K 2.W.5 (stories and ACs) as the story requiring an AI Eval Card.

---

## Carry-forward to spec

| Item | Destination |
|---|---|
| Differentiator: confidence level + named fallback | Vision metric (`01-vision.md`), PRD scope boundary (`06-prd.md`) |
| AI capability: multi-signal confidence scorer | AI story + AI Eval Card stub in `04-stories-acs.md` |
| IKEA sync-lag transparency principle | NFR: confidence score must surface signal recency (max sync-lag threshold) |
| Zara size-level granularity | AC refinement: phantom-stock rate calculated at SKU + size, not SKU only |
