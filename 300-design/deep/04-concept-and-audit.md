# 04 — Behavioural Concept + Audit
**Kata K 3.D.4 | Consumes:** `deep/03-prompt-rules.md`, `deep/02-synthesis-and-governance.md`

---

## Concept generation prompt used

```
Create two compact UI concepts for Meridian's availability assistant.

The screen must show: item name, nearby store, availability estimate, freshness cue,
request-hold action, feedback control, and a manual fallback. Use UUI-style component
names where possible. Include low-confidence and stale-data states; do not show a firm
hold promise.
```

---

## Direction 1 — Inline badge (minimal integration)

**Layout:** Availability estimate lives inline on the product page, directly below the price line. Compact — one row for the badge + store name, one row for the freshness timestamp, one row for the CTA.

**Key UI blocks and Promptframe notes:**

| Region | Component (UUI) | Prompt note |
|---|---|---|
| Availability label | `Badge` (amber fill, caption text) | "Likely available" or "Limited availability" — no green, no "In stock" |
| Store name | `Text` (body-regular) | Nearest store name, tap to change |
| Freshness cue | `Text` (caption, neutral-500) | "Stock data updated X min ago" — always inline, never tooltip-only |
| Info icon | `IconButton` (info, neutral-400) | Taps to `Tooltip`: "Estimated from store data — not a guarantee." |
| CTA | `Button` (primary) | "Request pickup" — not "Add to cart", not "Reserve" |
| Fallback | `Text` (body-regular, neutral-600) | Replaces badge entirely when stale: reason + phone number |
| Feedback | Deferred to post-pickup confirmation screen | Thumbs-up/down — not on product page |

**Stale state:** Badge disappears. Replaced by: "We can't confirm stock right now — call Oak Street: +44 20 7946 0958."

**Strategy:** Minimise disruption to the existing product page. Availability slots into the existing layout hierarchy — price → availability → CTA.

---

## Direction 2 — Dedicated assistant card (explicit trust surface)

**Layout:** A distinct card below the price block and above the add-to-cart button. The card contains all availability information in one bounded surface: estimate, store selector, freshness, disclosure, CTA, and fallback. Recovery path is always visible — not triggered only on failure.

**Key UI blocks and Promptframe notes:**

| Region | Component (UUI) | Prompt note |
|---|---|---|
| Card container | `Panel` (`FlexCol`, border, rounded) | Bounded surface — separates AI-generated content from product data |
| Availability label | `Badge` (amber fill, caption text) | "Likely available" / "Limited availability" — same rules as Direction 1 |
| Store selector | `Text` link + `IconButton` (chevron) | "Checking Oak Street — change store" |
| Freshness cue | `Text` (caption, neutral-500) | "Stock data updated X min ago" — inline in card header |
| Info icon + disclosure | `IconButton` + `Tooltip` | "Estimated from store data — not a guarantee." |
| Recovery path | `Text` link (body-regular) | Always visible below estimate: "Prefer to call ahead? Oak Street: +44 20 7946 0958" — not triggered by failure only |
| CTA | `Button` (primary) | "Request pickup" |
| Feedback control | `IconButton` pair (thumbs up / thumbs down, caption label) | Below CTA, visible after estimate is shown |
| Fallback | Replaces badge + recovery with explicit reason | "We can't confirm stock right now — data hasn't refreshed. Call Oak Street." |
| Loading / skeleton | `Skeleton` rows (confirm against UUI) | Fills card while estimate is fetching |

**Stale state:** Badge + recovery text replaced by reason + phone. Card frame stays — user sees a contained message, not a broken layout.

**Strategy:** Create a dedicated trust surface. More visual weight, but all information — estimate, caveat, recovery — is visible together without user action. Directly addresses Theme 2 (recovery path always present, not just on failure).

---

## Behavioural state matrix

Both directions must survive all five states. Red = missing in concept.

| State | Trigger | UI obligation | Direction 1 | Direction 2 |
|---|---|---|---|---|
| Loading | Request sent | Show skeleton without certainty | Inline skeleton row | Card skeleton — confirm against UUI |
| Fresh estimate | confidence ≥ 0.7, sync age ≤ 30 min | "Likely available" + freshness inline | ✅ | ✅ |
| Low confidence | confidence < 0.7, sync age ≤ 30 min | "Limited availability" + hedge + recovery | ⚠️ Recovery not always visible — appears only in fallback trigger | ✅ Recovery always visible |
| Stale estimate | sync age > 30 min | Hide badge; lead with caveat; name the reason; offer manual path | ✅ Badge replaced, reason + phone shown | ✅ Card updates in place |
| Refusal / error | Feed unavailable or model cannot answer | Name issue; offer manual path; no empty state | ⚠️ No distinct error state — falls back to stale copy | ✅ Distinct error copy in card |

---

## Four-criteria audit

### User value
- Direction 1: present. Estimate visible at a glance; low friction.
- Direction 2: present. More context per load; recovery path reduces wasted trips.
- **Winner: Direction 2** — directly addresses the drop-off (Step 6, journey map). Direction 1 reduces label over-trust but does not change the recovery experience.

### Trust clarity
- Direction 1: freshness inline ✅, info icon ✅, no green ✅. Recovery path only in fallback state — not in low-confidence state.
- Direction 2: freshness inline ✅, info icon ✅, no green ✅, recovery path visible at all times ✅.
- **Winner: Direction 2** — trust artefacts are visible before the user needs them, not only after a failure trigger. Consistent with overfitting note in K 3.D.2: recovery design matters more than extra disclosure mechanics.

### Design-system parity
- Direction 1: `Badge`, `Text`, `IconButton`, `Button`, `Tooltip` — all likely real UUI components. Skeleton confirm needed.
- Direction 2: same components + `Panel` container + `Skeleton`. "Panel" and "Skeleton" names need UUI library confirmation.
- **Gap for both:** skeleton/loading component name unconfirmed. Mark as condition for K 3.D.7 parity checklist.
- **Roughly equal** — Direction 2 has one more unconfirmed name but uses no invented components.

### State coverage
- Direction 1: missing a distinct error state; low-confidence recovery path not always visible. **4/5 states adequately covered.**
- Direction 2: all five states covered; card frame holds across all states. **5/5 states covered.**
- **Winner: Direction 2.**

---

## Decision

**Keep Direction 2 (dedicated assistant card).**

Rationale: Direction 2 is the only concept that covers all five behavioural states and makes the recovery path visible before a failure occurs. This directly addresses the highest-priority finding from synthesis (Theme 2 — no recovery path). Direction 1 is cleaner and lower-friction, but it fails the state coverage criterion and buries recovery in the fallback trigger.

**Change list before Direction 2 feeds conversation and handoff work:**
1. Confirm `Panel` and `Skeleton` names against the UUI library — do not proceed to SPEC with invented names.
2. Rebuild "ConfidenceChip" if any generator used that name — it is not a real UUI component; use `Badge` with amber token.
3. Feedback control (thumbs up/down) needs a UUI component name — likely `IconButton` pair; confirm against library.
4. Recovery path copy ("Prefer to call ahead?") — review against Rule 4 (trust language rules) before handoff. Current phrasing implies choice; may reduce uptake in low-confidence state where a call is genuinely advisable.
5. Store selector interaction (change store) — out of scope for this kata; flag for product owner before building.

**Discard:** Direction 1 as a separate track. Its inline badge pattern may be reused for the fresh-estimate state within the Direction 2 card, but the concept as a standalone direction does not meet state coverage requirements.
