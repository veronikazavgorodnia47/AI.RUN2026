# Parity Checklist — K 3.D.7
**Against:** `deep/06-spec-and-ac.md` | **Prototype:** `07-code-prototype/index.html`

Legend: ✅ pass · ⚠️ runtime-only (not demonstrable in static HTML) · 🔲 open (needs external confirmation) · ❌ fail / gap

---

## 1 — State model (5 states)

| State | Trigger condition | In prototype | Copy matches SPEC | Status |
|---|---|---|---|---|
| `loading` | `isLoading == true` | s1 — 4 animated Skeleton rows | "Checking availability…" ✅ | ✅ |
| `fresh` | `isLoading==false`, `confidenceScore >= 0.70`, `sapSyncAge ≤ 30` | s2 — Badge amber-500 + freshness + recovery + primary CTA | "Likely available" · "Stock data updated 8 min ago" · "Prefer to call ahead?" · "Request pickup" ✅ | ✅ |
| `low-confidence` | `isLoading==false`, `confidenceScore < 0.70`, `sapSyncAge ≤ 30` | s3 — Badge amber-700 + recovery above CTA (Medium) + secondary CTA | "Limited availability" · "We'd recommend calling ahead…" ✅ | ✅ |
| `stale` | `isLoading==false`, `sapSyncAge > 30` | s4 — no Badge, reason + phone, no CTA | "We can't confirm stock right now — our store data hasn't refreshed in a while." ✅ | ✅ |
| `error` | `isLoading==false`, `hasError == true` | s5 — no Badge, error copy + phone + retry link, no CTA | "Something went wrong checking availability for this store." ✅ | ✅ |

State priority order (`error > stale > low-confidence > fresh > loading`) is enforced via `data-state` attribute — implementer must wire prop priority in logic. ⚠️ runtime

---

## 2 — Props coverage

| Prop | Type | Represented in prototype | Note |
|---|---|---|---|
| `confidenceScore` | `number \| null` (0.0–1.0) | s2 (0.82), s3 (0.55); null case → error state (s5) | ✅ |
| `sapSyncAge` | `number` (minutes) | s2 (8), s3 (12), s4 (38) | ✅ |
| `storeName` | `string` | "Oak Street" in all states | ✅ |
| `storePhone` | `string` | "+44 20 7946 0958" in s2–s5 | ✅ |
| `isLoading` | `boolean` | `true` in s1; `false` in s2–s5 | ✅ |
| `hasError` | `boolean` | `true` in s5 | ✅ (setter ownership assigned to API client — see AC3) |
| `onRequestPickup` | `() => void` | Callback fires on "Request pickup" tap | ⚠️ runtime; linked to modal (see §5) |
| `onFeedback` | `(positive: boolean) => void` | CheckmarkOutline / CloseOutline in s2 + s3; post-collection in FeedbackPrompt | ⚠️ runtime |

---

## 3 — Design token coverage

| Token (SPEC name) | CSS variable | Used on | Hex (verify against UUI) | Status |
|---|---|---|---|---|
| `color.amber-500` | `--color-amber-500` | Badge fill — s2 fresh | `#F59E0B` | ✅ (confirm UUI value) |
| `color.amber-700` | `--color-amber-700` | Badge fill — s3 low-confidence | `#B45309` | ✅ (confirm UUI value) |
| `color.neutral-600` | `--color-neutral-600` | Body text s4/s5 reason copy | `#525252` | ✅ (confirm UUI value) |
| `color.neutral-500` | `--color-neutral-500` | Caption text, state labels | `#737373` | ✅ (confirm UUI value) |
| `color.neutral-200` | `--color-neutral-200` | Skeleton fill | `#E5E5E5` | ✅ (confirm UUI value) |

All 5 SPEC tokens present. Hex values are approximations — must be replaced with UUI library values before build.

---

## 4 — Component coverage

| SPEC component | UUI name | In prototype | Flag |
|---|---|---|---|
| Card container | Frame (styled) | ✅ — `.Panel` class in prototype; **no UUI `Panel` component** — build uses styled Frame | ✅ O-1 resolved |
| Availability label | `Badge` ✅ | ✅ — `Badge--amber-500` (s2) + `Badge--amber-700` (s3) | ✅ |
| Text — body | `Text` | ✅ — `.Text--body`, `.Text--caption`, `.Text--medium` | ✅ |
| Info icon | `Icon Button` + `notification-info` ✅ | ✅ — `.IconButton` with `icon-info` CSS placeholder | ✅ |
| Disclosure popup | `Tooltip` | ✅ — shown inline as `.Tooltip--inline`; note: real UUI Tooltip is on hover/tap | ✅ |
| CTA | `Button` ✅ | ✅ — `.Button--primary` (s2, modal) + `.Button--secondary` (s3, modal cancel) | ✅ |
| Skeleton rows | `Skeleton/Text Block` ✅ | ✅ — 4 rows in s1 with `animation: skeleton-pulse` | ✅ O-2 resolved |
| Feedback controls | `Icon Button` + `notification-done` / `content-clear` ✅ | ✅ — icon placeholders in s2, s3, and FeedbackPrompt | ✅ |
| Divider | (layout element) | ✅ — `.Divider` in s2–s5 | ✅ |

**UUI names verified against library.** O-1 resolved: no `Panel` component in UUI — use styled Frame. O-2 resolved: `Skeleton/Text Block` confirmed.

---

## 5 — AC coverage

| Clause | Condition | Prototype evidence | Status |
|---|---|---|---|
| **AC1** Fresh | `confidenceScore >= 0.70` + `sapSyncAge ≤ 30` → amber-500 | s2 renders Badge `--amber-500` | ✅ |
| **AC1** Low-confidence | `confidenceScore < 0.70` + `sapSyncAge ≤ 30` → amber-700 | s3 renders Badge `--amber-700` | ✅ |
| **AC1** Null score | `confidenceScore == null` + `sapSyncAge ≤ 30` → error state | No null-score state in prototype; follows s5 path | ⚠️ runtime — add to unit tests |
| **AC2** Stale fallback | `sapSyncAge > 30` → Badge hidden, reason, phone, no CTA | s4 — no Badge element, reason copy present, phone present, no Button | ✅ |
| **AC2** Error fallback | `hasError == true` → same as stale | s5 — Badge absent, error copy, phone, retry link (user-initiated), no Button | ✅ |
| **AC2** Confidence ceiling | `confidenceScore > 0.95` or `> 1.0` → treat as error | Not demonstrable in static prototype | ⚠️ runtime — add unit test; 0.95 threshold needs product sign-off |
| **AC3** Skeleton | `isLoading == true` → Skeleton rows, no partial data | s1 — 4 Skeleton rows, no estimate shown | ✅ |
| **AC3** 1.5s threshold | Skeleton holds past 1.5s without partial estimate | p95 performance target — not demonstrable in static | ⚠️ runtime — verify under load test |
| **AC3** 4s timeout | 4s without response → error state, `hasError = true` | s5 is the target state; ownership is API client layer | ⚠️ runtime — API client must set `hasError = true` |
| **AC4** Freshness inline | `fresh` or `low-confidence` → "Stock data updated [X] min ago" inline | s2 + s3 both show timestamp in caption | ✅ |
| **AC4** Tooltip on InfoOutline | User taps InfoOutline icon → Tooltip with disclaimer | Shown inline in prototype; in build: UUI Tooltip on `IconButton` tap | ✅ (inline proxy) |
| **AC4** Format rule | `< 60 min` → "X min ago"; `≥ 60 min` → "about X hours ago" | Not demonstrated (static values: 8 min, 12 min) | ⚠️ runtime — implement in display helper |
| **AC5** Feedback prompt | Post-pickup completion event → FeedbackPrompt | FeedbackPrompt shown as extension state | ✅ (trigger event 🔲 needs product confirmation) |
| **AC5** CloseOutline log | `onFeedback(false)` → log `{store_id, sku, confidence_score, sap_sync_age, timestamp}` | Annotated in FeedbackPrompt card | ⚠️ runtime — logging endpoint 🔲 needs backend confirmation |
| **AC6** No green / "In stock" | No state renders green or "In stock" | All 5 states inspected — none use green or forbidden phrase | ✅ |
| **AC6** No unit counts | No exact count shown at any state | All 5 states inspected — no count | ✅ |
| **AC6** No hold promise | No "guaranteed", "reserved", "we'll hold it" | Modal: "not a guaranteed hold" — anti-pattern absent, disclosure present | ✅ |
| **AC6** No estimate when stale | `sapSyncAge > 30` → no availability estimate | s4 renders no Badge and no CTA | ✅ |
| **AC6** "Check in store" with reason | Fallback must name reason | s4: "…data hasn't refreshed in a while" · s5: "Something went wrong…" | ✅ |
| **AC6** No auto-retry | Retry is user-initiated only | s5: "Try again ›" is a link, not automatic | ✅ |
| **AC6** No PII in AI path | Customer identity/history excluded | No customer fields in any prop or log | ✅ |
| **AC6** No PII in feedback log | `onFeedback` payload excludes identity, session ID | Annotated in FeedbackPrompt; enforced at API layer | ✅ (enforce at API layer) |

---

## 6 — Copy accuracy (verbatim check)

| State | SPEC copy | Prototype copy | Match |
|---|---|---|---|
| loading | "Checking availability…" | "Checking availability…" | ✅ |
| fresh badge | "Likely available" | "Likely available" | ✅ |
| fresh freshness | "Stock data updated [X] min ago" | "Stock data updated 8 min ago" | ✅ |
| fresh tooltip | "Estimated from store data — not a guarantee." | In `title` attribute + inline proxy | ✅ |
| fresh recovery | "Prefer to call ahead?  [storePhone]" | "Prefer to call ahead?  +44 20 7946 0958" | ✅ |
| fresh CTA | "Request pickup" | "Request pickup" | ✅ |
| low-confidence badge | "Limited availability" | "Limited availability" | ✅ |
| low-confidence recovery | "We'd recommend calling ahead before making the trip. [storePhone]" | ✅ | ✅ |
| stale reason | "We can't confirm stock right now — our store data hasn't refreshed in a while." | ✅ | ✅ |
| stale manual path | "Call [storeName] to check before travelling:  [storePhone]" | ✅ | ✅ |
| error reason | "Something went wrong checking availability for this store." | ✅ | ✅ |
| error manual path | "Call [storeName] or check a nearby store:  [storePhone]" | ✅ | ✅ |
| error retry | "Try again ›" | "Try again ›" | ✅ |
| modal disclosure | "This is not a guaranteed hold — the item may sell before you arrive." | ✅ | ✅ |
| feedback prompt | Text "Was the item available when you arrived?" + CheckmarkOutline / CloseOutline | ✅ | ✅ |

All 15 copy strings match SPEC verbatim.

---

## 7 — Open items before build

| # | Item | Owner | Blocking |
|---|---|---|---|
| O-1 | ~~Confirm `Panel` UUI component name~~ | ~~Design / UUI library~~ | ✅ **Resolved** — no `Panel` in UUI; use styled Frame |
| O-2 | ~~Confirm `Skeleton` UUI component name~~ | ~~Design / UUI library~~ | ✅ **Resolved** — confirmed as `Skeleton/Text Block` |
| O-3 | Confirm all 5 token hex values against UUI library | Design / UUI library | Yes — colours must match system |
| O-4 | Confirm AC2 confidence ceiling (0.95 placeholder) | Product (Sarah Chen) | Yes — threshold is a product decision |
| O-5 | Confirm "pickup completed" event source for AC5 / FeedbackPrompt trigger | Product + Backend | Yes — FeedbackPrompt has no trigger without this |
| O-6 | Confirm analytics endpoint for CloseOutline feedback log | Backend | Yes — logging destination unspecified |
| O-7 | EU AI Act risk classification | Legal | Launch blocker — sign-off required before production |
| O-8 | Validate 0.70 confidence threshold against real SAP sync-window data | Data / Product | Launch blocker — threshold is unvalidated |

---

## Verdict

**Prototype passes structural and static parity.** All 5 states render the correct components, tokens, copy, and AC conditions. 6 AC clauses are runtime-only (latency, null score, confidence ceiling, format rule, feedback trigger, log endpoint) — not demonstrable in static HTML; all are annotated and mapped to owners above.

O-1 and O-2 resolved. Build is unblocked from a component-name perspective. Remaining launch blockers: O-7 (EU AI Act sign-off) and O-8 (confidence threshold validation). Open items O-3 through O-6 are pre-production checks.
