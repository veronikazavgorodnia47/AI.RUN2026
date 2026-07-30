# 08 — Trust Surface + AI Risk Register
**Kata K 3.D.8 | Consumes:** `deep/01–07`, `05-conversation-flow.md` (HITL table), `06-spec-and-ac.md` (hard constraints), `07-code-prototype/parity-checklist.md` (open items)

---

## 1 — Mental-model gaps

Five user internal sentences, ranked by disappointment impact (most damaging first).

| Rank | User sentence | Expected outcome | Actual outcome | Disappointment trigger |
|---|---|---|---|---|
| 1 | "I've requested pickup — it's being held for me." | Item set aside; trip is safe to make | Soft hold queued; no guarantee; item may sell | Shopper arrives; item is gone. Highest-impact failure: wasted trip + no fallback. |
| 2 | "Likely available means it's there." | Certainty; no need to call ahead | Calibrated estimate from 15–30 min stale data | Shopper arrives; item is not there. Over-trust on the "fresh" label despite amber caveats. |
| 3 | "Stock data updated 8 min ago — that's close enough to live." | 8 minutes = safe; the estimate is reliable | SAP sync may be 30 min stale; 8 min is the age of the last known sync, not a shelf count | Shopper reads the timestamp as a near-real-time guarantee and discounts the caveat entirely. |
| 4 | "Limited availability means I should hurry." | Low confidence = urgency signal; item selling fast | Low confidence = data uncertainty; item status unknown | Shopper rushes based on a misread urgency cue; arrives to find item may have always been unavailable. |
| 5 | "If they can't confirm it, it's probably out of stock." | Stale / error state = negative signal | Stale / error state = data unavailable, not absence confirmed | Shopper abandons a potentially valid trip. Less catastrophic than a wasted trip, but erodes feature trust over time. |

**Design implication:** Gaps 1 and 2 are the primary calibration targets. The no-green rule, the no-firm-hold modal disclosure, and the freshness timestamp inline address both. Gap 3 is addressed by tooltip copy ("Estimated from store data — not a guarantee"), which names the estimation nature rather than just the timestamp. Gaps 4 and 5 require copy calibration — the "Limited" label must not carry urgency connotation; the stale/error copy must name the reason, not just prompt a call.

---

## 2 — Trust surface decisions

### Confidence
**Decision:** Two amber states only — no green, no red. Both states display the word "available"; confidence is communicated by the qualifier ("Likely" vs "Limited") and badge intensity, not by colour polarity.

**Rationale:** Colour is read faster than copy. A green badge is read as "confirmed" regardless of qualifier text — the mental-model gap 2 failure. Using amber at both confidence levels keeps the signal honest: the assistant is always an estimate. The two-tone amber system (amber-500 / amber-700) signals relative caution without implying certainty at either end.

**Threshold:** 0.70 is a calibration boundary, not a confidence threshold. It must be validated against real SAP sync-window data before launch (O-8). Treat as provisional.

### Source / freshness
**Decision:** Freshness timestamp ("Stock data updated [X] min ago") is inline at all times in `fresh` and `low-confidence` states. Never tooltip-only. SAP sync window (15–30 min) described in tooltip copy ("Estimated from store data — not a guarantee"), not in badge copy.

**Rationale:** The freshness timestamp is the primary trust-calibration signal for users who will naturally question "but is this current?" Hiding it in a tooltip means the majority who don't tap the info icon never see it. Inline placement is a launch constraint, not a preference.

**Stale / error:** When `sapSyncAge > 30`, the timestamp is removed entirely. Nothing to timestamp. Reason copy names the gap ("data hasn't refreshed") so the user understands why the estimate is absent.

### Refusal
**Decision:** Two distinct refusal states with different copy and same layout structure: `stale` (data too old) and `error` (feed unavailable / model cannot answer). A third sub-case — unsafe over-promise suppression — renders as the error state.

**Rationale:** Silent refusal ("Check in store") transfers responsibility to the user without explaining why. Named refusal ("We can't confirm stock right now — our data hasn't refreshed") is honest and preserves trust even in the failure case. The two states use different reason copy because the cause matters to the user: one is predictable (sync window); the other is unexpected (feed error).

**Unsafe over-promise:** When `confidenceScore > 0.95` OR feed returns certainty-implying output, suppress and render error state. This is not a user-facing refusal explanation — it is a system-layer guardrail before anything reaches the UI.

### Feedback
**Decision:** Post-pickup feedback prompt fires after the "pickup completed" event — not at request confirmation. Binary question: "Was the item available when you arrived?" with `notification-done` (✓) / `content-clear` (✗) icon buttons. Log payload: `{ store_id, sku, confidence_score, sap_sync_age, timestamp }` — no PII.

**Rationale:** Feedback at request-time is prediction. Feedback post-pickup is ground truth. The model cannot improve its calibration without knowing whether the estimate was correct. A negative response (✗) is the signal that catches model-wrong failures (risk R1). Binary question is answerable without subjective judgment.

**Timing confirmation required:** The "pickup completed" event source must be confirmed with Product + Backend before launch (O-5). The feedback prompt has no trigger without it.

### Disclosure
**Decision:** Three-layer disclosure. Layer 1 — badge copy ("Likely" / "Limited") signals estimate at glance. Layer 2 — freshness timestamp inline names data age. Layer 3 — tooltip on `notification-info` icon: "Estimated from store data — not a guarantee." Confirmation modal adds explicit no-guarantee clause before the user can commit to a pickup request.

**Rationale:** Different users read at different depths. The layered structure ensures the minimum (layer 1) is read by everyone; layers 2 and 3 reward users who pause. The modal checkpoint is the final disclosure gate for any user who proceeds to commitment — the no-guarantee clause must appear before the confirm button, not after.

---

## 3 — HITL classification

Extends the table from `05-conversation-flow.md` with error-state assignments.

| Action | Classification | Reason |
|---|---|---|
| Show availability estimate | Agent-led | Low consequence; user reads and decides. No commitment made. |
| Show low-confidence badge + recovery | Agent-led | Informs user; recovery path visible but no action taken by system. |
| Request pickup — happy path | Confirm-then-act | User explicitly taps CTA; modal displays no-guarantee disclosure before confirm. |
| Request pickup — low confidence | Confirm-then-act | Secondary CTA; recovery path ("call ahead") shown first as recommended action. |
| Hold when stale or error | Human-only | Data untrustworthy; no AI-generated action offered. Phone path only. |
| Unsafe over-promise suppression | Human-only | Trust boundary violated; output suppressed; only phone path available. |
| Item missing at store (post-visit) | Human-only | Post-visit failure; store associate and customer service own recovery. |
| 4s timeout auto-error | Agent-led → error → Human-only | Skeleton holds; after 4s, API client sets `hasError = true`; error state renders; only phone path available. |
| Malformed / null-score response | Agent-led → error → Human-only | Component validates inputs; falls to error state if `confidenceScore == null` or response is malformed. |

---

## 4 — Error states

### E1 — model-wrong
**Trigger:** Model produces a `fresh` estimate (confidence ≥ 0.70) for an item that is not at the store. Calibration failure — the score was computed from stale SAP data that had not yet registered the sale.

**User experience:** No visible failure at render time. Shopper sees "Likely available", travels, finds item gone. This is the highest-impact failure mode.

**Design-layer response:** The negative AC (no guarantee, no firm hold) is the only design-layer guard. The feature cannot detect model-wrong at render time — the confidence score was technically valid given the data available.

**Detection mechanism:** `onFeedback(false)` log payload `{ store_id, sku, confidence_score, sap_sync_age, timestamp }` is the signal source. Without the feedback log, calibration failure rate is invisible. See risk R1.

**HITL assignment:** Human-only post-visit. Store associate and CS own recovery. The design cannot intercept this failure after the shopper has left.

**Emitted AC:** see §5 ERR-AC4.

---

### E2 — model-slow
**Trigger:** Model or SAP feed takes > 4s to respond (AC3 timeout threshold).

**User experience:** Skeleton persists; user waits. After 4s, error state renders automatically — "Something went wrong checking availability for this store." — with phone and retry link.

**Design-layer response:** Skeleton is the only visible state during the wait. The component does not show partial data at any point during loading.

**Ownership:** The API client layer must set `hasError = true` after 4s. The `AvailabilityAssistantCard` component cannot set its own props.

**HITL assignment:** Agent-led → timeout → Human-only. Transition is automatic; recovery is human (phone path).

**Emitted AC:** see §5 ERR-AC1.

---

### E3 — model-refusing
**Trigger:** Feed or model returns output that would violate the trust boundary. Two sub-cases:
- `confidenceScore > 0.95` (near-certain or out-of-range)
- Response contains certainty-implying content ("In stock", `confidence == 1.0`, or any output that would fail the no-green rule)

**User experience:** Error state renders. No estimate shown. Phone path is the primary forward action. User sees: "Something went wrong checking availability for this store."

**Design-layer response:** Suppression is a system-layer guardrail before any output reaches the component. The AC2 "unsafe over-promise" rule defines the threshold. Note: 0.95 ceiling is a placeholder — confirm with product before build (O-4).

**HITL assignment:** Human-only. Suppression is automatic; recovery is human.

**Emitted AC:** see §5 ERR-AC2.

---

### E4 — model-gibberish / malformed
**Trigger:** Feed or model returns unexpected data — missing required fields, wrong types, `confidenceScore == null` with `sapSyncAge ≤ 30` (fresh sync window but no score).

**User experience:** Component cannot determine a valid state. Falls to error state via `hasError = true`.

**Design-layer response:** Input validation at the component boundary. AC1 handles the `confidenceScore == null` case explicitly. The API client handles all other malformed-response cases by setting `hasError = true`.

**HITL assignment:** Agent-led error detection → component renders error state → Human-only recovery.

**Emitted AC:** see §5 ERR-AC3.

---

## 5 — Emitted AI-AC clauses

### HITL clauses

**HITL-AC1 — No autonomous commitment**
WHEN the availability estimate is displayed (agent-led state),
THEN the component MUST NOT make any commitment on behalf of the user — no auto-hold, no auto-redirect, no action without explicit user tap.

**HITL-AC2 — Confirm-then-act gate**
WHEN the user taps "Request pickup" (fresh or low-confidence state),
THEN `PickupConfirmationModal` MUST appear before any hold action is queued.
The no-guarantee disclosure ("This is not a guaranteed hold — the item may sell before you arrive.") MUST appear before the confirm button, not after.

**HITL-AC3 — Human-only gate for untrustworthy data**
WHEN `sapSyncAge > 30` OR `hasError == true` OR output would imply certainty at any confidence level,
THEN the component MUST NOT offer any AI-generated action.
The only forward path MUST be a human contact (store phone number).

### Error-state clauses

**ERR-AC1 — model-slow timeout**
WHEN `isLoading` duration exceeds 4s without a response,
THEN the API client MUST set `hasError = true`.
THEN the component renders error state: "Something went wrong checking availability for this store." + store phone + "Try again ›".
No partial estimate is shown.
No automatic retry occurs without explicit user action.

**ERR-AC2 — model-refusing / unsafe output**
WHEN `confidenceScore > 0.95` OR the feed returns output containing certainty-implying content ("In stock", confidence == 1.0, or any value that would trigger the no-green rule),
THEN suppress the output; do not render the availability estimate.
THEN render error state with phone path.
No automatic retry.
*0.95 ceiling is a placeholder — confirm threshold with product (O-4) before build.*

**ERR-AC3 — model-gibberish / malformed**
WHEN `confidenceScore == null` AND `sapSyncAge ≤ 30`,
THEN render error state (same trigger as `hasError == true`).
WHEN the feed response is missing required fields or contains unexpected types,
THEN the API client MUST set `hasError = true` before the response reaches the component.
The component MUST NOT attempt to render from a malformed payload.

**ERR-AC4 — model-wrong (detection, not prevention)**
The component CANNOT detect model-wrong at render time.
WHEN the user taps the `content-clear` icon button (`onFeedback(false)`) on the post-pickup FeedbackPrompt,
THEN log `{ store_id, sku, confidence_score, sap_sync_age, timestamp }` — no PII fields.
This log is the sole design-layer signal for calibration failure rate.
The negative AC (no guarantee, no firm hold promise, freshness inline) is the design-layer guard.

---

## 6 — Prototype-state revision notes

These are K 3.D.7 states that passed structural parity but need follow-up evidence before the prototype can fully support build handoff.

| State / gap | K 3.D.7 status | Follow-up needed | Owner |
|---|---|---|---|
| `confidenceScore == null` → error state | ⚠️ runtime — no distinct state in prototype | Add a s2-null variant that demonstrates null score → error state path. Currently s5 covers `hasError == true` but not the null-score sub-case. | Engineering / QA |
| Confidence ceiling (> 0.95) → suppression | ⚠️ runtime — not demonstrable in static HTML | Add a s5-ceiling variant or interaction annotation showing the suppression trigger. Currently the prototype does not show what a ceiling-triggered refusal looks like. | Design / Engineering |
| 4s timeout → error state (API client trigger) | ⚠️ runtime — API client must set `hasError = true` | An interaction prototype or test spec should show the timer mechanism. Static prototype shows s5 as the outcome state but not the trigger path. | Engineering |
| FeedbackPrompt trigger (post-pickup event) | ⚠️ trigger event needs product confirmation (O-5) | The event source ("pickup completed") is unconfirmed. Prototype shows FeedbackPrompt as an extension state but cannot demonstrate what fires it. Confirm with Product + Backend before build. | Product / Backend |
| Stale state with simultaneous `hasError` | Not tested — priority order in prototype | State priority (`error > stale > low-confidence > fresh > loading`) is declared in parity checklist §1 but not tested. Add a test case where both `sapSyncAge > 30` and `hasError == true` are true simultaneously — should render error, not stale. | Engineering |

No new prototype states are required to unblock handoff. These are runtime-and-confirmation gaps; the existing 5 states cover all visible user-facing scenarios. Add unit tests before build for the first three items.

---

## 7 — AI risk register

**Likelihood scale:** 1 = rare · 2 = low · 3 = medium · 4 = high · 5 = almost certain
**Impact scale:** 1 = trivial · 2 = minor · 3 = moderate · 4 = high (user harm / trust damage) · 5 = critical (legal / regulatory)

| # | Risk | L | I | L×I | Mitigation | Owner | Escalate? |
|---|---|---|---|---|---|---|---|
| R1 | **Model-wrong:** fresh estimate shown; item not at store when shopper arrives | 3 | 4 | 12 | No-green rule; no firm hold; freshness inline; feedback log (`onFeedback(false)`) is the detection signal. Review calibration drift post-launch. | Data / Product (Sarah Chen) | No — by design. Escalate if confirmed false-positive rate exceeds agreed threshold post-launch. |
| R2 | **Threshold miscalibrated:** 0.70 cutoff misaligned with real SAP sync-window variance | 3 | 4 | 12 | Validate 0.70 threshold against real SAP sync-window data before launch (O-8). Treat all design decisions depending on this threshold as provisional. | Data / Product (Sarah Chen) | Yes — launch blocker (O-8). |
| R3 | **EU AI Act misclassification:** feature launched without legal clearance; classified as high-risk post-launch | 2 | 5 | 10 | Legal review required before production launch (O-7). Design may proceed; build may not ship without sign-off. | Legal / Compliance | Yes — launch blocker (O-7). |
| R4 | **Silent staleness failure:** SAP sync fails without updating `sapSyncAge`; stale detection trigger does not fire | 2 | 4 | 8 | `sapSyncAge > 30` trigger removes badge and CTA; stale copy names reason. If detection mechanism is unreliable, the `sapSyncAge` calculation itself must be validated at the backend layer. | Backend / Data | Yes — if staleness detection is not guaranteed to update on sync failure. |
| R5 | **Copy drift:** availability-state copy edited after governance review; certainty language ("In stock", "Guaranteed") re-introduced | 2 | 4 | 8 | Content-governance line (K 3.D.2) lists forbidden phrases. Copy owner must review all availability-state copy changes before shipping. Review is triggered by: confidence threshold change, SAP sync architecture change, hold-queue behaviour change. | UX Writer / Content Designer | No — governed by content review trigger. |
| R6 | **Feedback log PII leak:** `onFeedback` payload inadvertently includes session ID, user identity, or order reference | 2 | 4 | 8 | AC6 negative AC explicitly bans PII from log payload. Enforce at API layer — component cannot guarantee what the calling layer appends. Backend must validate payload schema before logging. | Backend | No — enforce at API layer; confirm with backend (O-6). |
| R7 | **Timeout not enforced:** API client does not fire `hasError = true` after 4s; skeleton persists indefinitely | 2 | 3 | 6 | ERR-AC1 assigns ownership to API client. Runtime test required — not demonstrable in static prototype. | Backend / Engineering | No — assigned to engineering; test before launch. |
| R8 | **FeedbackPrompt never fires:** "pickup completed" event not implemented; ground-truth signal absent; model-wrong rate invisible | 3 | 2 | 6 | Confirm event source with Product + Backend before build (O-5). Without this event, calibration improvement loop is broken but the feature still functions. | Product / Backend | No — pre-production check (O-5). Escalate if event cannot be implemented — calibration loop has no substitute. |

**Risk register owner:** Sarah Chen (Head of CX / Product Owner, per K 3.D.2 governance verdict). Signs off on R1–R2 thresholds and R3–R4 launch-blocker clearance.

---

## Carry-forward to K 3.D.9 (Evaluation + Feedback Loop)

- Feedback log schema (`{ store_id, sku, confidence_score, sap_sync_age, timestamp }`) feeds directly into the evaluation loop — this is the ground-truth signal for calibration assessment.
- R1 and R2 define the evaluation criteria: false-positive rate (model-wrong frequency) and threshold accuracy (0.70 vs real variance). Both need post-launch measurement plans.
- ERR-AC4 (feedback log as model-wrong detection) is the design-layer contribution to the eval loop — K 3.D.9 should define what happens after a negative signal is logged.
- R8 (FeedbackPrompt not firing) means the eval loop has no data if O-5 is unresolved — K 3.D.9 should name the fallback data source if the pickup event cannot be implemented.
