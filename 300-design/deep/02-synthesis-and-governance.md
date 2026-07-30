# 02 — Evidence Synthesis + Governance Gate
**Kata K 3.D.2 | Consumes:** `deep/01-feasibility-and-scope.md`, journey map, heuristics, competitor teardown

---

## Evidence sources used

| ID | Source | Type | Date |
|---|---|---|---|
| JM | `01-journey-map.md` — Meridian click-&-collect journey (lived Zara experience) | Observation | 2026-07-27 |
| H | `01-heuristics.md` — Nielsen heuristic review, 8 findings | Heuristic audit | 2026-07-27 |
| CT | `02-primary-signal.md` — Zara competitor teardown | Teardown | 2026-07-27 |
| V | `02-primary-signal.md` — Zara App Store verbatims V1–V3 | Public review (single source) | 2026-07-27 |

*Single-source limitation: verbatims are from one public source (Zara App Store). Journey map and heuristics are from one lived experience. Findings are directional, not statistically validated for Meridian's user base. This synthesis feeds concept work only — not a substitute for primary Meridian research.*

---

## Theme 1 — Shoppers read any availability label as a firm state, not an estimate

**Claim:** Users treat the current "In stock" label as a reliable, near-real-time fact. When the label proves wrong, the failure lands as betrayal, not as expected uncertainty.

**Evidence:**
- JM Step 2: shopper sees "In stock," feels confident, reserves — no hesitation at the ambiguous label.
- JM Step 6: "Shocked — no warning before arrival; 'In stock' label proved false." Shock implies the label was read as a promise.
- H-F1: "The system knows its data may be outdated but presents it as live fact."
- H-F2: "Shoppers distinguish between 'available to ship' and 'on the shelf in-store'" — single-word label collapses both, mismatch goes undetected until arrival.

**Risk:** Over-trust. If the new assistant uses similar confident language ("Likely available"), it may inherit the same false-certainty reading — especially for users who have no prior context about SAP sync latency.

---

## Theme 2 — The failure has no recovery path; the system is silent until the worst moment

**Claim:** The phantom-stock failure is not just a data accuracy problem — it is a recovery design problem. No system intervention occurs before arrival; the only response is cancellation.

**Evidence:**
- JM Step 6 (drop-off): "No warning before arrival… no alternative offered proactively."
- JM Step 7: "Time lost; trip wasted; item now unavailable; no explanation of how it happened."
- H-F8: "When the item was missing, no screen prompted an alternative (different store, ship-to-home, rain-check). Only cancellation was offered." — confirmed from lived experience.

**Risk:** If the new assistant only replaces the label without adding a recovery path (fallback to manual check, nearby store, or ship-to-home), it reduces over-trust but does not close the drop-off. The feature must include a fallback action, not just a caveat.

---

## Theme 3 — Inventory uncertainty is a category-wide constraint, not a Meridian-specific failure

**Claim:** Even the market benchmark (Zara) cannot deliver real-time inventory certainty. The assistant must be framed as a calibrated estimate, not a competitive accuracy claim.

**Evidence:**
- CT: Zara's click-and-collect shows "tentative availability" — "can lead to disappointment or substitution on arrival." No live inventory confirmation exists at benchmark scale.
- CT: "Promise is speed, not accuracy" — Zara solves pickup speed, not inventory certainty.
- H-F3: Without a unit count, "the shopper must recall from prior experience whether 'In stock' at Meridian is reliable" — the category trains users to distrust the label over time.

**Risk:** If Meridian positions the assistant as solving what Zara cannot, it sets a higher trust expectation than the underlying data (15–30 min SAP sync) can meet. Positioning must be honest: this is a better estimate, not a guarantee.

---

## Contradictions and weak signals — human review required

**Contradiction 1 — Evidence base is single-source and competitor-only**
All user-facing evidence is from Zara (one competitor, one app store, one lived experience). The phantom-stock frequency, severity, and user behaviour for Meridian's actual 22-market base is unknown. The direction is credible; the magnitude is not. A Meridian-internal data pull (support tickets, NPS verbatims, store-associate logs) is needed before confidence thresholds or copy decisions are finalised.
*Human action required: validate frequency + severity with Meridian data before launch.*

**Contradiction 2 — Users showed satisfaction at the reservation step, suggesting pre-arrival friction may be resisted**
Journey map Step 3 reads "Satisfied" — the shopper felt the current reservation UX was acceptable. This suggests users may resist added steps (confirmation modals, extra disclosure screens) even if those steps improve accuracy. There is a real tension between trust design and conversion friction that Theme 1 alone does not resolve.
*Human action required: test whether confidence disclosure increases or decreases reservation completion rate. Do not assume more disclosure equals better UX without data.*

**Overfitting note — Theme 1 severity may be overstated; design priority should favour Theme 2**

The evidence for Theme 1 is drawn from a failure case (the item was missing). Users who found their item — likely the majority — are absent from this data. This is selection bias: the synthesis sees only the worst outcome and may over-weight the label-misreading problem as a result.

There is also a conflation worth naming: *surprise at failure* is not the same as *treating a label as a guarantee*. Step 3 reads "Satisfied" and Step 4 reads "Neutral" — not confident. Some prior uncertainty was already present. Zara's category-wide "tentative availability" framing suggests the market has already trained users to read these signals as directional, not definitive. Users proceed anyway — not because they are deceived, but because the trip cost feels acceptable relative to the reward.

If Theme 1 is overstated, over-investing in disclosure (more timestamps, more caveats, more uncertainty language) while under-investing in the recovery path would make the feature worse, not better. A user who understood the estimate was uncertain but had no exit when wrong is in a worse position than a user who over-trusted but found their item.

**Design implication:** Theme 2 (no recovery path) is the safer and better-evidenced priority. Theme 1 (label over-trust) is real but should inform copy calibration, not drive the interaction architecture. Do not let disclosure mechanics crowd out recovery design.

*Human action required: do not let Theme 1 drive modal confirmations or friction-heavy disclosure without first testing whether users already carry calibrated expectations.*

---

## Semantic-risk table

| User phrase / reading | Likely model interpretation | Bad outcome if misread | Mitigation |
|---|---|---|---|
| "Likely available" read as "it's there" | Model outputs estimate; user reads as certainty | Shopper travels; item gone; trust damage | Lead with "estimated" framing; always show freshness timestamp inline |
| "Reserve" read as "firm hold" | Soft-hold queued; no guarantee | Shopper assumes item is set aside; arrives to find it sold | Rename to "Request pickup" or "Check availability"; add no-guarantee disclosure on confirmation |
| "Updated 15 min ago" read as "effectively live" | Data is 15 min old; SAP may be 30 min stale | User trusts the estimate too highly; ignores caveat | Copy must read "stock data — may not reflect shelf right now" not "updated X ago" alone |
| "Limited availability" read as "hurry before it sells out" | Low-confidence estimate | Creates false urgency; shopper rushes; item was always out of stock | Use "Limited availability" only with explicit caveat; no urgency cue (no countdown, no "only 2 left") |
| "Check in store" read as "it's there, just confirm" | Fallback state — data unavailable | Shopper treats fallback as weak confirmation; still travels | Fallback copy must name the reason: "We can't confirm stock right now" + phone number |

---

## Data-readiness check

| Source | Freshness | Consent / Sensitivity | Missing / at-risk field |
|---|---|---|---|
| SAP inventory sync | 15–30 min stale | Non-PII; stock + store metadata only | Real-time shelf count — does not exist; no path to it |
| Confidence score | Computed at query time from stale SAP data | Non-PII | Algorithm and threshold unvalidated against real sync-window data |
| Store metadata (phone, location) | Assumed current | Non-PII | Accuracy per store not confirmed; may be outdated in fragmented 22-market stack |
| User feedback log (thumbs-down) | Not yet implemented | Non-PII if anonymised | Missing entirely; needed for model improvement loop |
| Reservation / hold queue | Out of scope (separate workstream) | Order history — must not enter AI path | Hold confirmation status not available to the assistant |

---

## Content-governance line

**Forbidden claims** (must not appear in any copy, at any fidelity):
- "In stock" (binary, no staleness signal)
- "Guaranteed" / "reserved" / "we'll hold it" (implies firm hold)
- Any green state or ✓ icon implying confirmed availability
- Exact unit counts ("3 left")
- Urgency language tied to low confidence ("only a few remaining")

**Copy owner:** UX Writer / Content Designer assigned to the feature. Must review all availability-state copy before any prototype leaves design.

**Review trigger:** Any change to confidence thresholds, SAP sync architecture, or hold-queue behaviour requires a copy review pass before shipping — these directly affect whether the current copy remains accurate.

---

## Governance verdict

> **Proceed with condition**
>
> The evidence is directional and sufficient to feed concept and flow work. Two conditions must be cleared before launch:
> 1. Meridian internal data (support tickets, NPS, store logs) must validate phantom-stock frequency and severity.
> 2. EU AI Act risk classification must be confirmed by Legal.
>
> **Accountable owner:** Product Owner (Sarah Chen, Head of CX) owns both conditions and signs off on the governance gate before the feature enters production build.

---

## Carry-forward to K 3.D.3+

- "Likely available" and "Limited availability" are the approved copy directions — neither implies certainty.
- Freshness timestamp must be inline (not tooltip) at all times when an estimate is shown.
- Fallback copy must name the reason for the fallback, not just prompt the user to visit the store.
- Feedback log (thumbs-down) is a missing data source — must be designed into the feature as a launch requirement, not a post-launch addition.
- Semantic-risk table feeds directly into prompt rules (K 3.D.3) and conversation flow (K 3.D.5).
