# 03 — Synthesis Decision

**Feature:** Meridian availability assistant — cross-channel click-&-collect
**Input:** `02-workshop.md`

---

## Chosen change

**Confidence colour badge + staleness tooltip on the product page availability label**
(e.g., amber badge + "Updated 20 min ago" — tap to expand on mobile)

**Owner:** Sarah Chen, Head of CX

---

## Rationale

The badge+tooltip solution wins because it prevents the wrong trip by giving customers upfront inventory confidence information, while nearest-store only fixes the problem after time, money, and the trip are already spent. Nearest-store remains valuable as post-failure recovery for phantom stock scenarios, but it is reactive rather than preventive. The winning solution carries two critical constraints: no green state that creates false confidence in structurally stale data, and the amber threshold must be validated against actual sync data before launch to ensure it does not mislead customers about availability risk.

---

## Runner-up

**Nearest store with stock suggestion** — surfaces 3 nearby stores with higher-confidence stock when the primary store cannot fulfil. High impact, low effort (3/1), but addresses failure after commitment rather than before. Recommended as a companion feature in a later sprint.

---

## Constraints carried forward

1. **No green state** — maximum confidence level is amber ("Likely available"). The design must never imply a guarantee given SAP sync is structurally 15–30 min stale.
2. **Threshold validation required** — the amber/red threshold must be calibrated against actual sync-window and stock-stability data before launch. Risk: wrong threshold silently suppresses good inventory.
