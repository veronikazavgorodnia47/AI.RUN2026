# 01 — Heuristic Review: Click-&-Collect Screens

**Feature:** Meridian availability assistant — cross-channel click-&-collect
**Method:** Nielsen's 10 Heuristics applied to 3 screens
**Evidence source:** lived Zara click-&-collect experience + AI-assisted review (validated)

---

## Findings

**F1 — Product page: "In stock" label — no staleness signal**
Violated: H1 · Visibility of system status
The label shows a binary state with no timestamp and no acknowledgment that the SAP sync is 15–30 min stale. The system knows its data may be outdated but presents it as live fact.

---

**F2 — Product page: "In stock" — no online vs. in-store distinction**
Violated: H2 · Match between system and the real world
Shoppers distinguish between "available to ship" and "on the shelf in-store." The single label collapses both into one word, mismatching the user's real-world mental model.

---

**F3 — Product page: "In stock" — no unit count**
Violated: H6 · Recognition rather than recall
Without a quantity (e.g., "3 left"), the shopper must recall from prior experience whether "In stock" at Meridian is reliable or thin. The interface forces a memory judgment instead of surfacing the information needed to decide.

---

**F4 — Reservation confirmation: hold expiry absent**
Violated: H1 · Visibility of system status
The confirmation screen tells the shopper the reservation succeeded but omits when it expires. The system holds state the user needs (hold deadline) and withholds it.

---

**F5 — Reservation confirmation: breaks category-wide convention**
Violated: H4 · Consistency and standards
Every major click-&-collect operator (IKEA, Zara, M&S) shows a hold-until date/time on the confirmation screen. The absence breaks the convention shoppers have learned across the category.

---

**F6 — Pickup counter: zero status feedback during shelf check**
Violated: H1 · Visibility of system status
Once in queue, the shopper receives no feedback. The associate has begun a manual shelf check, but from the shopper's perspective the system is silent — no progress signal of any kind.

---

**F7 — Pickup counter: associate lookup forces recall on both sides**
Violated: H6 · Recognition rather than recall
The associate's system requires her to ask the shopper multiple identifying questions (name, order number, item) to locate the reservation, rather than surfacing it from a scan or simple lookup. The system forces recall on both sides of the counter instead of recognising the reservation from available signals.
*Source: confirmed from lived experience — associate at Zara asked repeated questions before locating the order.*

---

**F8 — Pickup counter: item-missing moment — no structured recovery flow**
Violated: H9 · Help users recognize, diagnose, and recover from errors
When the item was missing, no screen prompted an alternative (different store, ship-to-home, rain-check). The failure surfaced as cancellation only, with no system support for recovery.
*Source: confirmed from lived experience — only cancellation was offered, no alternatives.*

---

## Summary

| # | Screen | Heuristic | Element |
|---|---|---|---|
| F1 | Product page | H1 Visibility | "In stock" label — no staleness signal |
| F2 | Product page | H2 Real-world match | "In stock" — no online vs. in-store distinction |
| F3 | Product page | H6 Recognition | "In stock" — no unit count |
| F4 | Reservation confirmation | H1 Visibility | Confirmation screen — hold expiry absent |
| F5 | Reservation confirmation | H4 Consistency | Confirmation screen — breaks category convention |
| F6 | Pickup counter | H1 Visibility | Queue — zero status feedback during shelf check |
| F7 | Pickup counter | H6 Recognition | Associate lookup — forces recall on both sides |
| F8 | Pickup counter | H9 Error recovery | Item-missing moment — no structured recovery flow |
