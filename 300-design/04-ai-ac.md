# 04 — AI-Aware Acceptance Criteria

**Feature:** Meridian availability assistant — cross-channel click-&-collect
**Decided change:** Confidence colour badge + staleness tooltip on product page
**Input:** `03-decision.md`

---

## User Story

As a click-&-collect shopper, I want to see an availability confidence badge
and a tooltip showing how recently the stock was confirmed, so that I can
decide whether the trip is worth making.

---

## Base AC (supplied)

AC1. WHEN a product has store stock data, THEN the product page shows an
     availability indicator per nearby store.
AC2. WHEN no store within range has the item, THEN show "Not collectable
     nearby" + a delivery option.
AC3. WHEN stock data is missing for a store, THEN omit that store (don't guess).
AC4. WHEN the user taps a store, THEN show last-confirmed time + distance.

---

## AI-Specific AC

**AI-AC1 (confidence)**
WHEN confidence ≥ 0.7, THEN show "Likely available" (amber badge).
WHEN confidence < 0.7, THEN show "Limited availability" (amber badge, darker tone).
No green state at any confidence level.

**AI-AC2 (refusal/fallback)**
WHEN SAP sync for a store is > 30 min stale OR stock data is missing,
THEN hide the availability badge and show "Check in store" + the store phone number.

**AI-AC3 (latency)**
WHEN availability data is loading, THEN show a skeleton loader.
WHEN loading exceeds 1.5s (p95), THEN continue skeleton.
WHEN loading exceeds 4s, THEN trigger AI-AC2 fallback ("Check in store" + store phone).

**AI-AC4 (disclosure)**
WHEN the availability badge is shown, THEN display "Updated [time] ago" inline
at all times.
WHEN the shopper taps the information icon, THEN show "Estimated from store
data — not a guarantee."

**AI-AC5 (feedback)**
WHEN the shopper reaches the pickup confirmation screen, THEN show
"Was the item available?"
WHEN the shopper reports "No", THEN log store + SKU + timestamp for
model improvement.

**AI-AC6 (negative AC)**
The assistant MUST NOT show a green "In stock" badge at any confidence level,
display exact unit counts, or promise a guaranteed hold.
