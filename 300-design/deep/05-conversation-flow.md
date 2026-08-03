# 05 — Conversational Flow: Happy + Sad Paths
**Kata K 3.D.5 | Consumes:** `deep/04-concept-and-audit.md`, `deep/03-prompt-rules.md`, Wide `04-ai-ac.md`

---

## Happy path — product page → estimate → next action

| Step | User action | System response | Copy / UI state |
|---|---|---|---|
| 1 | Opens product page for a specific item | Page loads; availability card initialises | Card skeleton visible — `[UUI: Skeleton]` fills card |
| 2 | Waits for estimate | Confidence score computed server-side from SAP sync | Skeleton holds for up to 1.5s (p95); see latency note below |
| 3 | Reads availability estimate | Card renders with badge + store + freshness | "Likely available at Oak Street · Stock data updated 8 min ago" |
| 4 | Taps info icon | Disclosure tooltip expands | "Estimated from store data — not a guarantee." |
| 5 | Taps "Request pickup" | Confirmation modal appears | "You're requesting pickup at Oak Street. This is not a guaranteed hold — item may sell before you arrive." + Confirm / Cancel |
| 6 | Confirms request | Soft hold queued; confirmation screen shown | "Pickup requested at Oak Street. Bring your order number. Hold not guaranteed." |
| 7 | Arrives at store; collects item | Post-pickup feedback prompt shown | "Was the item available when you arrived?" + notification-done / content-clear [UUI Asset: confirmed ✅] |

**Latency note (from Wide AI-AC3):**
- 0 → 1.5s: skeleton holds — no estimate shown yet, no message
- 1.5s → 4s: skeleton continues — do not show partial data
- > 4s: trigger fallback — "We're having trouble checking availability. Call Oak Street: +44 20 7946 0958"

---

## Sad path 1 — Stale data (SAP sync > 30 min)

**Trigger:** `sap_sync_age > 30 minutes` OR `confidence_data == null`

**Flow:**
1. User opens product page
2. Card renders — no badge shown
3. Reason message + manual path displayed in place of estimate

**User-facing copy:**
> *We can't confirm stock right now — our store data hasn't refreshed in a while.*
> *Call Oak Street to check before travelling: +44 20 7946 0958*

**What changes vs happy path:**
- Badge removed entirely — no amber label shown
- "Request pickup" CTA removed — no offer when data is untrustworthy
- Recovery path (phone number) is the only action
- No freshness timestamp shown (there is nothing to timestamp)

**HITL point:** Human-only. When data is stale, the assistant cannot estimate. No AI-led action is offered. The only forward path is a human store associate via phone.

**Latency and recovery copy (if stale state itself loads slowly):**
> *Checking store data… having trouble getting a fresh result. Call Oak Street: +44 20 7946 0958*

**Emitted AI-AC — SP1:**
> WHEN `sap_sync_age > 30 min` OR `confidence_data == null`,
> THEN hide the availability badge, display reason copy naming the data issue, show store phone number, and remove the "Request pickup" CTA.
> The assistant MUST NOT show "Check in store" without naming why.

---

## Sad path 2 — Low confidence (conf < 0.7)

**Trigger:** `confidence_score < 0.70`, SAP sync within threshold

**Flow:**
1. User opens product page
2. Card renders with low-confidence badge
3. Recovery path is prominently displayed — not deferred to a fallback state
4. User can still request pickup, but CTA is secondary (less visual weight)

**User-facing copy:**
> *Limited availability at Oak Street*
> *Stock data updated 12 min ago.*
> *We'd recommend calling ahead before making the trip.*
> *+44 20 7946 0958*

**What changes vs happy path:**
- Badge variant: "Limited availability" (amber darker) instead of "Likely available"
- Recovery path moved above the CTA and shown in Medium weight
- CTA downgraded to secondary button — still available, but less dominant
- Feedback control remains — low-confidence outcomes are especially important to log

**HITL point:** Confirm-then-act. User must explicitly tap the secondary "Request pickup" button. The assistant does not auto-submit or nudge toward pickup when confidence is low. The recovery path (call ahead) is offered as the primary recommended action.

**Latency and recovery copy (while estimate loads):**
> Same skeleton as happy path — user does not know confidence level until card renders.

**Emitted AI-AC — SP2:**
> WHEN `confidence_score < 0.70` AND `sap_sync_age ≤ 30 min`,
> THEN show "Limited availability" badge (amber-dark variant), display recovery path (store phone) above the CTA in Medium weight, downgrade CTA to secondary.
> The assistant MUST NOT hide the recovery path or show it only on user request.

---

## Sad path 3 — Refusal / feed unavailable

**Trigger:** Feed error, model cannot answer, or request would produce an unsafe over-certain response

**Flow:**
1. User opens product page
2. Card renders — no badge, no estimate
3. Error message shown with manual path and retry option

**User-facing copy:**
> *Something went wrong checking availability for this store.*
> *Call Oak Street or check a nearby store: +44 20 7946 0958*
> *Try again ›*

**What changes vs happy path:**
- No badge, no freshness timestamp, no CTA
- Error message names the issue without alarming language
- Retry link available — but not auto-retried (user-initiated only)
- Recovery path (phone) is the primary forward action

**Unsafe over-promise case (special sub-path):**
If the model or upstream data would produce a response that implies certainty (e.g. a confidence score of 1.0 with no staleness check, or a response containing "In stock"), the system must suppress the response and show the refusal state instead.

> *We can't confirm availability right now.*
> *Call Oak Street to check: +44 20 7946 0958*

**HITL point:** Human-only for the over-promise sub-path. No AI-generated response is shown when the output would violate the trust boundary. Human store associate via phone is the only path.

**Latency and recovery copy:**
> If the request times out (> 4s): "We're having trouble checking availability. Call Oak Street: +44 20 7946 0958" — same as latency fallback in happy path.

**Emitted AI-AC — SP3:**
> WHEN the feed is unavailable OR the model cannot produce a safe response,
> THEN hide all estimate UI, display error copy naming the issue, show store phone and a retry link.
> The assistant MUST NOT auto-retry silently or show a partial estimate.
> WHEN a response would imply certainty at any confidence level, THEN suppress it and show refusal copy.

---

## HITL classification summary

| Action | Classification | Reason |
|---|---|---|
| Show availability estimate | Agent-led | Low consequence; user reads and decides |
| Show low-confidence badge + recovery | Agent-led | Informs user; no commitment made |
| Request pickup (happy path) | Confirm-then-act | User explicitly taps; confirmation modal adds no-guarantee disclosure |
| Request pickup (low confidence) | Confirm-then-act | Secondary CTA; recovery path shown first as recommended action |
| Hold when stale or error | Human-only | Data untrustworthy; no AI action offered |
| Unsafe over-promise suppression | Human-only | Trust boundary violated; only phone path available |
| Item missing at store | Human-only | Post-visit failure; store associate + customer service own recovery |

---

## Emitted AI-AC clauses — summary

| Clause | Sad path | Testable condition |
|---|---|---|
| SP1 | Stale data | `sap_sync_age > 30 min` → badge hidden, reason shown, CTA removed, phone shown |
| SP2 | Low confidence | `conf < 0.70` → "Limited availability", recovery above CTA (Medium weight), CTA secondary |
| SP3 | Refusal / error | Feed error or unsafe output → error copy, phone + retry, no partial estimate |

---

## Carry-forward to K 3.D.6 (SPEC + AC)

- The happy path confirmation modal introduces a new component: `PickupConfirmationModal` — needs a spec entry.
- The post-pickup feedback prompt (Step 7) must be specced separately — placement, trigger, and logging behaviour.
- The unsafe over-promise suppression rule (SP3 sub-path) must appear verbatim in the negative AC.
- Latency thresholds (1.5s / 4s) from Wide AI-AC3 are confirmed here — carry into K 3.D.6 SPEC as named props.
- HITL classification table feeds directly into K 3.D.8 (trust surface + risk register).
