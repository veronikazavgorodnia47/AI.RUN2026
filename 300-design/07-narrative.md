# 07 — Redesign Narrative

**Feature:** Meridian availability assistant — cross-channel click-&-collect
**Decided change:** Confidence colour badge + staleness tooltip on product page
**Owner:** Sarah Chen, Head of CX

---

## Benefit
Helps customers decide if it's worth the trip to pick up clothes by showing
how fresh the stock information is, preventing wasted journeys when inventory
data is unreliable. Addresses the root cause of the 7% phantom-stock
cancellation rate by moving the decision point from the store counter to the
product page.

## Engineering cost — Medium
Requires building a confidence scoring layer and connecting it to the existing
SAP inventory sync. No major backend changes required. Key work: server-side
confidence computation, sync-age tracking, and a 4s timeout fallback trigger.

## Design cost
Create the AvailabilityBadge, StoreCheckMessage, and AvailabilityDisclosure
components with all states (likely-available, limited-availability, fallback,
loading, skeleton). Write regional guidelines for badge usage, since store
capabilities and sync reliability vary across 22 countries.

## Content cost
Translate 4 key messages into 22 languages:
- "Likely available"
- "Limited availability"
- "Check in store"
- "Estimated from store data — not a guarantee."
Update store phone numbers for the "Check in store" fallback across all
1,400 store locations.

## Expected outcome metric
Reduce click-&-collect cancellation rate from **7% to under 4%**, measured
30 days post-launch against the same store cohort baseline.

---

## Runner-up — Nearest store with stock
Reactive recovery: surfaces 3 nearby stores with higher-confidence stock when
the primary store cannot fulfil. Recommended as a companion feature in a
later sprint. Does not address the pre-trip decision gap this redesign solves.
