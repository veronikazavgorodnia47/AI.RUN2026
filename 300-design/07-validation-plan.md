# 07 — Validation Plan

**Feature:** Meridian availability assistant — cross-channel click-&-collect
**Decided change:** Confidence colour badge + staleness tooltip on product page
**Input:** `03-decision.md`, `05-mockup.html`

---

## Usability Test Tasks

**Task 1 — Happy path: decision to reserve**
You need a black blazer for a job interview tomorrow. Find a blazer that shows
"Likely available" and walk me through how you'd decide whether to reserve it
for pickup today.

**Task 2 — Low-confidence state: decision under uncertainty**
You're looking for a specific pair of jeans in your size as a birthday gift
for your partner. You find the style you want that shows "Limited availability."
Show me what you'd do next and explain your decision-making process.

**Task 3 — Fallback state: no estimate available**
You're searching for a particular designer dress you saw online. The product
page shows "Check in store" with a phone number. Demonstrate how you'd proceed
to get this item.

**Task 4 — Reservation flow**
You've decided to reserve a winter coat that shows "Likely available" in your
size. Walk me through the complete process from this product page to confirming
your reservation.

**Task 5 — Post-pickup feedback (failure scenario)**
Imagine you just went to pick up a sweater that had shown "Likely available"
but the store couldn't find your reservation when you arrived. Show me where
you'd expect to give feedback about this experience.

---

## Success signals per task

| Task | Pass condition |
|---|---|
| T1 | Shopper reads the badge + timestamp before deciding — does not treat "Likely available" as a guarantee |
| T2 | Shopper understands "Limited availability" is a warning, not a block — makes a conscious go/no-go decision |
| T3 | Shopper uses the phone number or changes plan — does not interpret missing badge as "in stock" |
| T4 | Shopper completes reservation without expecting a hold confirmation or exact unit count |
| T5 | Shopper locates the "Was the item available?" prompt on the pickup confirmation screen |
