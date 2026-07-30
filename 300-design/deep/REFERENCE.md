# REFERENCE.md — Design agent context pack
**Bundled for:** `design-meridian` skill (K 3.3 Deep specialist add)
**Load when:** producing SPEC, AC, or trust-surface outputs that must match the established Meridian design decisions.

---

## JTBD statement (from K 3.D.1)

> A click-&-collect shopper needs to know whether a specific item is truly collectable
> at a nearby Meridian store **before** making the trip, so they can commit or redirect
> without risk of a wasted journey.

**Not a feature request. Not "we need an availability widget."**

---

## Feasibility verdicts (carry-forward constraints)

- AI in product: **Conditional Go** — staleness warning mandatory; no green badge; EU AI Act sign-off required before launch; confidence threshold (0.70) must be validated against real SAP sync data.
- Drop-off step: Step 6 — item missing at counter after shopper has committed (reserved + travelled). This is the highest-impact failure to design against.

---

## Scope boundary

| We will | We won't |
|---|---|
| Show an availability estimate labelled as an estimate | Show a green "In stock" badge at any confidence level |
| Surface data freshness inline at all times | Display exact unit counts |
| Show fallback with named reason + phone when data is stale or missing | Promise a guaranteed hold or reservation |
| Allow user to request a soft hold (with modal no-guarantee disclosure) | Route hold through autonomous AI without human confirmation |

---

## Workshop decision (from K 3.W.3)

**Decision:** Show inventory quantities with confidence indicators at all times (amber badge + freshness timestamp), never hide them — even at high confidence.
**Decision-owner:** Sarah Chen (Head of CX)

---

## Confirmed design tokens

| Token | CSS variable | Used for |
|---|---|---|
| `color.amber-500` | `--color-amber-500` | Badge fill — fresh / "Likely available" |
| `color.amber-700` | `--color-amber-700` | Badge fill — low-confidence / "Limited availability" |
| `color.neutral-600` | `--color-neutral-600` | Body text: store name, stale/error copy |
| `color.neutral-500` | `--color-neutral-500` | Caption text: freshness timestamp, feedback label |
| `color.neutral-200` | `--color-neutral-200` | Skeleton fill |

Hex values are approximations — confirm against UUI library before build.

---

## Confirmed UUI component names

| Purpose | UUI name | Flag |
|---|---|---|
| Card container | Frame (styled) — **no standalone `Panel` in UUI** | Use Frame with card styling |
| Availability label | `Badge` | Confirmed |
| CTA | `Button` | Confirmed |
| Icon trigger | `Icon Button` (two words — not `IconButton`) | Confirmed |
| Loading rows | `Skeleton/Text Block` | Confirmed |
| Info icon | `Icon Button` + `notification-info` asset | Confirmed |
| Feedback ✓ | `Icon Button` + `notification-done` asset | Confirmed |
| Feedback ✗ | `Icon Button` + `content-clear` asset | Confirmed |

UUI Assets uses **lowercase-hyphenated** icon names — not PascalCase. Both UUI libraries are connected to the working Figma file (`Pgmk44mu6RFylVWwT8rcVg`).

---

## 5 component states

| State | Trigger | Badge | CTA |
|---|---|---|---|
| `loading` | `isLoading == true` | None — skeleton rows | None |
| `fresh` | `confidenceScore >= 0.70` AND `sapSyncAge ≤ 30` | "Likely available" amber-500 | Primary "Request pickup" |
| `low-confidence` | `confidenceScore < 0.70` AND `sapSyncAge ≤ 30` | "Limited availability" amber-700 | Secondary "Request pickup" |
| `stale` | `sapSyncAge > 30` | None | None — phone only |
| `error` | `hasError == true` | None | None — phone + retry link |

State priority: `error > stale > low-confidence > fresh > loading`

---

## Trust-surface decisions (from K 3.D.8)

- **Confidence:** Two amber states only — no green. Both use the word "available"; qualifier calibrates expectation.
- **Freshness:** Inline at all times in fresh/low-confidence states. Never tooltip-only.
- **Refusal:** Two distinct states (stale / error) with different copy. Reason always named.
- **Feedback:** Post-pickup binary ("Was item available?"). Log: `{ store_id, sku, confidence_score, sap_sync_age, timestamp }` — no PII.
- **Disclosure:** Three layers — badge copy → freshness timestamp → info tooltip. Modal adds no-guarantee clause before confirm.

---

## Forbidden content (verbatim — carry into every SPEC)

- "In stock" (binary label, no staleness signal)
- "Guaranteed" / "reserved" / "we'll hold it"
- Any green state or confirmed-availability icon
- Exact unit counts ("3 left")
- Urgency language tied to low confidence

---

## Human-owned decisions (never decide)

Scope · prioritisation cuts · ship-readiness · brand voice · accessibility judgment ·
ethical tradeoffs · EU AI Act sign-off · confidence threshold validation ·
whether AI belongs in the feature at all.
