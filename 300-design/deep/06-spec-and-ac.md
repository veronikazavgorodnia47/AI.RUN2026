# 06 — AI-Aware SPEC + AC
**Kata K 3.D.6 | Consumes:** `deep/03–05`, Wide `06-context.md` / `06-spec.md`

---

## CONTEXT — Meridian availability assistant

**Feature:** An AI availability indicator estimates whether an item is collectable at a nearby Meridian store. It shows confidence level, data freshness, and a manual fallback when data is too stale or unavailable to trust.

**Users:** Click-&-collect shoppers on the product page deciding whether the trip is worth making before requesting pickup.

**Environment:**
- Frontend: React
- Data source: SAP inventory sync (15–30 min latency); non-PII stock and store metadata only
- Confidence score computed server-side
- Design system: UUI (EPAM) — component and token names must be verified against the UUI library before build
- EU AI Act risk classification: unconfirmed — legal sign-off required before launch

**Hard constraints:**
- Must NOT show a green "In stock" state at any confidence level
- Must NOT display exact unit counts
- Must NOT promise a guaranteed hold or reservation
- Must NOT show an estimate when `sapSyncAge > 30 min`
- Must NOT show "Check in store" without naming the reason
- Customer identity and order history must not enter the AI path
- Confidence threshold (0.70) must be validated against real SAP sync-window data before launch

**Out of scope:** Reservation holds, loyalty, pricing, store associate tooling, returns, cross-store fulfilment, checkout flow.

---

## SPEC — AvailabilityAssistantCard

`AvailabilityAssistantCard` is a composed component (not a single UUI primitive). It is built from: `Panel` (confirm UUI name), `Badge`, `Text`, `IconButton`, `Button`, `Tooltip`, `Skeleton` (confirm UUI name). Do not invent component names — where unconfirmed, write `confirm against UUI`.

### Props

| Prop | Type | Purpose |
|---|---|---|
| `confidenceScore` | `number \| null` (0.0–1.0) | Server-side availability estimate |
| `sapSyncAge` | `number` (minutes) | Age of the SAP inventory sync used for this estimate |
| `storeName` | `string` | Display name of the nearest selected store |
| `storePhone` | `string` | Store phone number — shown in fallback and recovery states |
| `isLoading` | `boolean` | True while the availability request is pending |
| `hasError` | `boolean` | True when the feed is unavailable or the model cannot produce a safe response |
| `onRequestPickup` | `() => void` | Called when user confirms pickup request |
| `onFeedback` | `(positive: boolean) => void` | Called when user taps thumbs-up or thumbs-down |

### State model

| State | Trigger condition | Renders |
|---|---|---|
| `loading` | `isLoading == true` | Skeleton rows; copy: "Checking availability…" |
| `fresh` | `isLoading == false` AND `confidenceScore >= 0.70` AND `sapSyncAge ≤ 30` | `Badge` "Likely available" + store + freshness + recovery + primary CTA |
| `low-confidence` | `isLoading == false` AND `confidenceScore < 0.70` AND `sapSyncAge ≤ 30` | `Badge` "Limited availability" + store + freshness + prominent recovery + secondary CTA |
| `stale` | `isLoading == false` AND `sapSyncAge > 30` | Reason copy + store phone; no badge, no CTA |
| `error` | `isLoading == false` AND `hasError == true` | Error copy + store phone + retry link; no badge, no CTA |

State priority when multiple conditions are true: `error` > `stale` > `low-confidence` > `fresh` > `loading`.

### Tokens

| Token | Where used | Note |
|---|---|---|
| `color.amber-500` | `Badge` fill — fresh / "Likely available" state | Confirm token name against UUI |
| `color.amber-700` | `Badge` fill — low-confidence / "Limited availability" state | Confirm token name against UUI |
| `color.neutral-600` | Body text: store name, stale/error message, recovery copy | Confirm token name against UUI |
| `color.neutral-500` | Caption text: freshness timestamp, feedback label, state label | Confirm token name against UUI |
| `color.neutral-200` | Skeleton fill | Confirm token name against UUI |

### Components per state

**`loading`**
```
Panel [UUI: Panel — confirm name]
  Text "Checking availability…"  [UUI: Text, neutral-500]
  Skeleton × 4                   [UUI: Skeleton — confirm name]
```

**`fresh`**
```
Panel
  Row: Badge "Likely available" [color.amber-500]  +  IconButton ℹ → Tooltip "Estimated from store data — not a guarantee."
  Text "[storeName] · [distance]  ›"      [UUI: Text + IconButton — store selector]
  Text "Stock data updated [X] min ago"   [UUI: Text caption, neutral-500]  ← always inline
  Divider
  Text "Prefer to call ahead?  [storePhone]"  [UUI: Text — recovery path, always visible]
  Button "Request pickup"  [primary]
  Text "Was this helpful?  👍  👎"  [UUI: IconButton pair — feedback]
```

**`low-confidence`**
```
Panel
  Row: Badge "Limited availability" [color.amber-700]  +  IconButton ℹ → Tooltip
  Text "[storeName] · [distance]  ›"
  Text "Stock data updated [X] min ago"   [caption, neutral-500]
  Divider
  Text "We'd recommend calling ahead before making the trip. [storePhone]"  [Medium weight — prominent]
  Button "Request pickup"  [secondary]
  Text "Was this helpful?  👍  👎"
```

**`stale`**
```
Panel
  Text "We can't confirm stock right now — our store data hasn't refreshed in a while."  [neutral-600]
  Text "[storeName] · [distance]"  [neutral-500]
  Divider
  Text "Call [storeName] to check before travelling:  [storePhone]"  [Medium, neutral-900]
  ← no CTA button
```

**`error`**
```
Panel
  Text "Something went wrong checking availability for this store."  [neutral-600]
  Text "[storeName] · [distance]"  [neutral-500]
  Divider
  Text "Call [storeName] or check a nearby store:  [storePhone]"  [Medium, neutral-900]
  Text "Try again  ›"  [UUI: Text link, blue]
  ← no CTA button
```

### Fallback
WHEN `sapSyncAge > 30` OR `hasError == true`:
- Hide `Badge` entirely — no amber label of any kind
- Show reason copy naming the data issue
- Show `storePhone` as the primary action
- Remove "Request pickup" CTA

---

## SPEC — PickupConfirmationModal *(extension from K 3.D.5)*

Shown when user taps "Request pickup" in `fresh` or `low-confidence` states.

| Prop | Type | Purpose |
|---|---|---|
| `storeName` | `string` | Display name of the selected store |
| `onConfirm` | `() => void` | Called on confirm tap |
| `onCancel` | `() => void` | Called on cancel tap |

**Content:**
```
Modal
  Text "You're requesting pickup at [storeName]."
  Text "This is not a guaranteed hold — the item may sell before you arrive."  [neutral-600]
  Button "Confirm pickup"  [primary]
  Button "Cancel"  [secondary / ghost]
```

No-guarantee disclosure is mandatory in this modal. It must appear before the confirm action, not after.

---

## SPEC — FeedbackPrompt *(extension from K 3.D.5)*

Shown on post-pickup confirmation screen.

**Trigger:** Post-pickup completion screen — after the shopper has been to the store. Requires a "pickup completed" event from the order system (not the request-confirmation screen). Confirm trigger with product.

**Content:** "Was the item available when you arrived?  👍  👎"

**On 👎:** Log `{ store_id, sku, confidence_score, sap_sync_age, timestamp }` — no PII.

---

## 6 AI-AC clauses

**AC1 — Confidence**
WHEN `confidenceScore >= 0.70` AND `sapSyncAge ≤ 30`,
THEN render `Badge` "Likely available" with fill `color.amber-500`.
WHEN `confidenceScore < 0.70` AND `sapSyncAge ≤ 30`,
THEN render `Badge` "Limited availability" with fill `color.amber-700`.
WHEN `confidenceScore == null` AND `sapSyncAge ≤ 30`,
THEN render error state (same as `hasError == true`).
No green state, no "In stock" label, no exact unit count at any confidence value.

**AC2 — Fallback / refusal**
WHEN `sapSyncAge > 30 min` OR `hasError == true`,
THEN hide `Badge`, display reason copy, show `storePhone`, remove "Request pickup" CTA.
WHEN `confidenceScore > 0.95` OR `confidenceScore > 1.0` (near-certain or out-of-range),
THEN treat as `hasError = true` and render error state.
*Note: 0.95 upper ceiling is a placeholder — confirm the threshold with product before build.*
The component MUST NOT show "Check in store" without naming the reason.

**AC3 — Latency**
WHEN `isLoading == true`,
THEN show `Skeleton` rows; do not show partial data.
WHEN `isLoading` duration exceeds 1.5s (p95 performance target — verify under load, not only in unit tests),
THEN continue skeleton — do not show a partial estimate.
WHEN `isLoading` duration exceeds 4s,
THEN render error state with copy: "Something went wrong checking availability for this store."
*Ownership: the API client layer MUST set `hasError = true` after 4s without a response — the component cannot set its own props.*

**AC4 — Disclosure**
WHEN state is `fresh` OR `low-confidence`,
THEN display "Stock data updated [X] min ago" inline at all times — not in a tooltip only.
Format rule: `[X]` = integer minutes rounded down; `< 60 min` → "X min ago"; `≥ 60 min` → "about X hours ago". If `sapSyncAge` is unavailable, omit the timestamp and show "Stock data freshness unknown."
WHEN user taps info icon (`IconButton ℹ`),
THEN show `Tooltip`: "Estimated from store data — not a guarantee."

**AC5 — Feedback**
WHEN the post-pickup completion screen is shown (pickup marked as collected),
THEN render `FeedbackPrompt`: "Was the item available when you arrived? 👍 👎"
*Trigger clarification: this fires AFTER the shopper has been to the store — NOT at request confirmation (Step 6). Requires a "pickup completed" event from the order/fulfilment system — confirm trigger with product before build.*
WHEN user taps 👎,
THEN log `{ store_id, sku, confidence_score, sap_sync_age, timestamp }` — no PII fields.
*Logging destination: confirm analytics endpoint with backend before build.*

**AC6 — Negative AC (verbatim)**
The `AvailabilityAssistantCard` MUST NOT:
- Show a green or "In stock" state at any `confidenceScore` value
- Display exact unit counts
- Promise a guaranteed hold or reservation
- Show an availability estimate when `sapSyncAge > 30 min`
- Show "Check in store" without naming the reason for the fallback
- Auto-retry a failed request without explicit user action
- Pass customer identity or purchase history into any AI path
- Include customer identity, session ID, or any PII in the `onFeedback` log payload

*The negative AC appears verbatim in both CONTEXT and SPEC. Engineering and Quality must treat it as a build constraint, not a design note.*

---

## Definition of SPEC Done — self-check

| Check | Status |
|---|---|
| Every state has a named trigger condition | ✅ |
| Every component uses a named UUI component or "confirm against UUI" | ✅ (Panel, Skeleton flagged) |
| Every threshold is named (0.70, 30 min, 4s, 1.5s) | ✅ |
| Negative AC appears verbatim in SPEC | ✅ |
| Every AC clause is answerable pass/fail | ✅ (revised: 9 testability gaps patched after critique) |
| Out-of-scope is explicit | ✅ |
| Privacy constraint (no PII in AI path) is named | ✅ |
| New components from conversation flow are addressed | ✅ (PickupConfirmationModal, FeedbackPrompt) |
| Token names flagged for UUI confirmation before build | ✅ |
| EU AI Act sign-off gate is named | ✅ (in CONTEXT) |
