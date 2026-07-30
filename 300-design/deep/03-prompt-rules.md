# 03 — Project Prompt Rules
**Kata K 3.D.3 | Consumes:** `deep/01-feasibility-and-scope.md`, `deep/02-synthesis-and-governance.md`

---

## Reusable CONTEXT block

```
CONTEXT — Meridian availability assistant

Feature: Meridian shows an availability estimate for click-&-collect items at nearby stores.
Stock data comes from SAP inventory sync and is 15–30 minutes stale. There is no real-time
shelf scan and no firm hold. A hold request is a soft request, not a reservation guarantee.

User: A click-&-collect shopper on the product page deciding whether the trip is worth making.

Hard constraints:
- Do not show a green "In stock" state at any confidence level.
- Do not display exact unit counts.
- Do not promise a guaranteed hold or reservation.
- When stock data is older than 30 minutes, lead with a caveat and offer a manual path.
- Always surface data freshness inline — not in a tooltip only.

Approved copy directions: "Likely available" (confidence ≥ 0.7) / "Limited availability"
(confidence < 0.7). Neither implies certainty. Both require a freshness note.

Out of scope: pricing, loyalty, store associate tooling, reservation holds.
```

---

## Structured prompt — availability-state copy

```
Role:
Senior UX writer for a retail availability assistant. You write copy that is honest about
uncertainty without alarming users or suppressing action.

Context:
{{paste CONTEXT block above}}

Style:
Plain, calm, honest. Confidence is expressed in words, not percentages or unit counts.
No urgency language. No green states. Freshness is always acknowledged.

Scope:
Draft user-facing availability copy for four states: high-confidence fresh data,
low-confidence fresh data, stale data, and refusal / feed failure.
Do not draft checkout, returns, or loyalty copy.

Constraints:
- Must not present an estimate as a firm hold.
- Must surface data freshness in every state where an estimate is shown.
- Must offer a manual path (store phone or "check in store") in every fallback state.
- Must name the reason for the fallback — do not just say "check in store."
- Must not use: "In stock", "guaranteed", "reserved", "we'll hold it", exact counts,
  urgency cues, or green/confirmed iconography.
```

---

## 5 Project rules

**Rule 1 — AI boundary**
The assistant estimates; it does not decide. It may say "Likely available" or "Limited availability." It must not say "In stock," "Available," or any phrase that implies confirmed, real-time shelf truth. The confidence threshold (0.7) is a product decision — AI may not adjust it.

**Rule 2 — Data handling**
Use anonymised Meridian data only. Do not paste live order IDs, customer records, store-level sales data, or proprietary inventory figures into non-approved tools. Stock count and store metadata (non-PII) may be used. Customer identity and purchase history must not enter the AI path.

**Rule 3 — Tone**
Plain, calm, honest. Confidence appears as words, not percentages. No urgency language ("only a few left", "selling fast"). No catastrophising in fallback states. The goal is to inform a decision, not to drive or suppress a conversion.

**Rule 4 — Trust language**
Forbidden phrases: "In stock", "guaranteed", "reserved", "we'll hold it", "confirmed available", exact unit counts, any urgency frame tied to low confidence. Required in every estimate state: a freshness cue. Required in every fallback state: the reason for the fallback + a manual path.

**Rule 5 — Evidence traceability**
Every copy direction must trace to a constraint in the feasibility gate (K 3.D.1), a semantic-risk row (K 3.D.2), or an AI-AC clause (Wide `04-ai-ac.md`). Do not introduce copy patterns that cannot be grounded in one of those sources. If a pattern is new, flag it for product review before use.

---

## Test cases — v1 results

**Test 1 — High confidence, fresh data (normal path)**

Input: confidence = 0.82, SAP sync age = 8 min, store = Oak Street

Expected: "Likely available" label + freshness note + no firm-hold language.

Prompt output (v1):
> *Likely available at Oak Street*
> *Stock data updated 8 minutes ago — not a guarantee.*

Pass/fail: **Pass.** Estimate present, freshness inline, no certainty claim.

---

**Test 2 — Low confidence, fresh data**

Input: confidence = 0.55, SAP sync age = 12 min, store = Oak Street

Expected: hedged label + freshness note + reduced action pressure + recovery option.

Prompt output (v1):
> *Limited availability at Oak Street*
> *Stock data updated 12 minutes ago. We'd recommend calling ahead before making the trip.*
> *Oak Street: +44 20 7946 0958*

Pass/fail: **Pass.** Hedged, freshness shown, recovery offered. One patch applied: initial draft omitted the phone number — added after review against Rule 4 (manual path required).

---

**Test 3 — Stale data / refusal**

Input: SAP sync age = 38 min (> 30 min threshold), confidence data = null

Expected: fallback copy naming the reason, no estimate shown, manual path offered.

Prompt output (v1):
> *We can't confirm stock right now — our store data hasn't refreshed in a while.*
> *Call Oak Street to check before travelling: +44 20 7946 0958*

Pass/fail: **Pass.** Reason named ("data hasn't refreshed"), no estimate shown, manual path present. No "Check in store" without explanation — satisfies K 3.D.2 semantic-risk row for that phrase.

---

## Version note

**v1** — prompt drafted and tested against three states (2026-07-30). One patch: low-confidence state required manual addition of phone number after first output omitted it. Rule 4 now explicitly names "manual path required" to prevent recurrence. Next version trigger: any change to confidence thresholds, SAP sync window, or hold-queue behaviour (per governance line in K 3.D.2).
