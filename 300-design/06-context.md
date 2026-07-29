# CONTEXT.md — Availability Assistant

## Feature in one sentence
An AI availability indicator estimates whether an item is collectable at a
nearby Meridian store, showing confidence level, data freshness, and a
no-confirm fallback when data is too stale to trust.

## Who uses it
Click-&-collect shoppers on the product page — deciding whether the trip
to a nearby store is worth making before reserving.

## Technical environment
- Frontend: React
- Data source: SAP inventory sync (15–30 min latency); non-PII stock and
  store metadata only — customer identity and order history stay out of
  the AI path
- Estimate computed server-side
- GDPR/CCPA apply to any personalised surface
- EU AI Act high-risk classification unconfirmed — legal sign-off required
  before launch

## Hard constraints
- Must NOT show a green "In stock" badge at any confidence level
- Must NOT display exact unit counts
- Must NOT promise a guaranteed hold
- Must NOT show an availability estimate when SAP sync is > 30 min stale
- Amber threshold must be validated against actual sync-window data before
  launch — wrong threshold silently suppresses good inventory

## Out of scope
Reservation holds, loyalty, pricing, store associate tooling (separate workstream).

## Related artefacts
- `04-ai-ac.md` — full AI-aware acceptance criteria (6 clauses)
- `05-mockup.html` — clickable lo-fi prototype (3 screens)
- `03-decision.md` — decided change + rationale vs. runner-up
- `03-synthesis.md` — impact × effort scoring matrix
