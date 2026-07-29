# 02 — Workshop Plan: Availability Assistant

**Feature:** Meridian availability assistant — cross-channel click-&-collect
**Input:** `01-journey-map.md`, `01-heuristics.md`

---

## Decision to close

Do we show inventory quantities with confidence indicators at all times
(e.g., "3 available — updated 20 min ago"), or hide specific quantities
entirely and always show "Available for pickup — confirm at store"
regardless of sync freshness?

**Decision-owner:** Sarah Chen, Head of CX

---

## Workshop skeleton

| | |
|---|---|
| **Goal** | Close the show/hide availability decision |
| **Decision-owner** | Sarah Chen (Head of CX) |
| **Participants** | Sarah Chen (CX), David Park (Retail Ops), Marco Rossi (regional GM), engineering lead |
| **Timeboxes** | 5 min frame · 15 min diverge (HMW + ideas) · 10 min converge |
| **Out of scope** | Pricing, loyalty |

**Goals split:**
- **Decide:** show vs. hide inventory quantities with confidence indicators
- **Explore:** how to communicate data freshness; recovery flows when stock is missing

---

## How-Might-We questions

### Theme 1 — Pre-trip decision
*How might we help the shopper feel confident enough to make the trip?*

1. HMW build customer confidence in inventory accuracy when we know the data might be 15–30 min stale?
2. HMW communicate data freshness without creating anxiety about item availability?
3. HMW help customers make informed decisions about whether to start their journey to the store?
4. HMW help customers understand the difference between online warehouse stock and actual in-store inventory?
5. HMW communicate how long items will be held without creating false urgency or abandonment anxiety?
6. HMW set clear expectations about reservation guarantees when inventory data is 15–30 min stale?

### Theme 2 — At-store experience & recovery
*How might we handle the moment when the item isn't there?*

7. HMW reduce the disappointment of customers who arrive at stores for unavailable items?
8. HMW proactively warn customers about potential stock issues before they travel to the store?
9. HMW provide immediate alternatives (ship to home, reserve at nearby store, rain check) when the phantom-stock scenario occurs?

### Theme 3 — Staff & system readiness
*How might we make sure the associate has the same picture as the shopper?*

10. HMW provide associates with the same inventory confidence information that customers see online?

---

## Ideas (diverge — no judging yet)

### Theme 1 — Pre-trip decision
1. **Confidence colour badges** — colour-coded label on product page (green/amber/red) reflecting data freshness and estimated stock reliability
2. **Staleness tooltips** — expandable tooltip on the availability label showing last sync time and what "likely available" means
3. **Store callback confirmation** — shopper can request a callback from the store to verbally confirm availability before making the trip

### Theme 2 — At-store experience & recovery
4. **Recovery coupon** — automatic discount voucher issued when phantom stock is confirmed, as compensation for the wasted trip
5. **Nearest store with stock** — when item is missing, system surfaces the 3 nearest stores with higher confidence stock and estimated travel time
6. **Free ship-to-home** — when item is unavailable in-store, offer free home delivery from the online warehouse at no extra cost

### Theme 3 — Staff & system readiness
7. **Associate customer view** — associate's POS/tablet shows the same confidence label and data freshness the customer saw online when reserving
8. **QR code order lookup** — customer shows a QR code on their phone; associate scans to instantly surface the reservation without manual questioning
9. **Passkey / order code** — unique short code on the reservation confirmation the customer can read aloud for fast lookup (to clarify: may overlap with QR; flag for convergence)
