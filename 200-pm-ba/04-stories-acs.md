---
consumes_from: 01-vision.md, 02-personas-journey.md, 03-competitors.md
date: 2026-07-28
---

## User stories

| # | Story | Priority |
|---|---|---|
| S1 | As a click-&-collect shopper, I want to see a real-time availability verdict before I reserve, so that I don't make a wasted trip. | P1 |
| S2 | As a click-&-collect shopper, I want the verdict to reflect actual shelf probability — not just the SAP count — so that I can trust what I see. | P1 — AI story |
| S3 | As a click-&-collect shopper who receives an Uncertain verdict, I want to see the nearest store with a confirmed Available verdict, so that I can redirect rather than abandon the purchase. | P1 |
| S4 | As a click-&-collect shopper, I want the assistant to work even when live signals are unavailable, so that I'm not blocked from browsing or reserving. | P1 |
| S5 | As a click-&-collect shopper, I want the availability check to be specific to my selected size and colour, so that the verdict reflects exactly what I'm buying. | P2 |
| S6 | As a click-&-collect shopper, I want to see how fresh the availability data is, so that I can judge how much to trust the verdict. | P2 |
| S7 | As a click-&-collect shopper who receives an Uncertain verdict, I want to still be able to reserve at my preferred store, so that the feature does not block my decision. | P2 |
| S8 | As a click-&-collect shopper on mobile, I want the verdict to be readable at a glance without interpreting stock numbers, so that I can decide in under 90 seconds. | P2 |
| S9 | As a store operations manager, I want the assistant's verdicts to be auditable against actual collection outcomes, so that accuracy can be measured and improved. | P3 |
| S10 | As a Meridian product analyst, I want to see the phantom-stock cancellation rate broken down by verdict type (Available / Low stock / Uncertain), so that I can measure the feature's impact. | P3 |

---

## Acceptance criteria — top four stories

---

### S1 — Availability verdict

**Story:** As a click-&-collect shopper, I want to see an availability verdict before I reserve, so that I don't make a wasted trip.

```gherkin
# Happy path
Given a shopper is on a product page with click-&-collect available at their selected store
And they have selected both a size and a colour
When they tap "Check availability"
Then the assistant returns one of three verdicts: Available, Low stock, or Uncertain
And the verdict is displayed in plain language with no raw stock-count numbers
And the verdict appears within 5 seconds

# Error path — no size selected
Given a shopper taps "Check availability" without selecting a size
Then the assistant prompts "Select a size to check availability"
And no verdict is shown until a size is selected

# Error path — no colour selected (size selected)
Given a shopper taps "Check availability" with a size selected but no colour selected
And the product has colour variants
Then the assistant prompts "Select a colour to check availability"
And no verdict is shown until both size and colour are selected

# Error path — verdict goes stale after variant change
Given a shopper has received a verdict for size M / colour Black
When they change the size or colour
Then the verdict is cleared immediately
And a new "Check availability" tap is required before a verdict is shown again

# Error path — rapid repeated taps
Given a shopper taps "Check availability" while a request is already in flight
Then the second tap is ignored (debounced)
And only one request is made to the backend

# NFR — latency
The verdict must be returned in ≤ 5 seconds at p95 under normal load
The UI must show a loading indicator if the response takes more than 1 second

# NFR — accessibility
The verdict label and loading state must meet WCAG 2.1 AA contrast and screen-reader requirements
(Required: Meridian operates in 22 EU countries; EN 301 549 / EAA applies)
```

---

### S2 (AI story) — Multi-signal confidence scorer

**Story:** As a click-&-collect shopper, I want the verdict to reflect actual shelf probability — not just the SAP count — so that I can trust what I see.

#### AI Eval Card stub

| Field | Value |
|---|---|
| **Confidence threshold** | Score ≥ 80 → Available; score 50–79 → Low stock; score < 50 → Uncertain. Boundary values: score exactly 80 = Available; score exactly 50 = Low stock. |
| **Input signals** | SAP inventory delta since last sync; POS transaction recency at target store; store staff scan events (anonymised/aggregated — see privacy note); historical phantom-stock rate per store/SKU/size (30-day rolling window); day-of-week pickup demand at that store |
| **Signal "available" definition** | A signal counts as available only if it is both present AND fresh (SAP lag ≤ 4h; POS data within 24h rolling window; scan events within 24h). A stale signal counts as unavailable for the purposes of the 2-of-5 threshold. |
| **Refusal trigger** | If fewer than 2 of the 5 signals are available (including stale signals counted as unavailable) → do not show a verdict; fall back to degraded mode (S4). Exactly 2 signals available = full confidence path, not degraded. |
| **Latency ceiling** | Full confidence score computation ≤ 5 s at p95, including all signal queries |
| **Fallback — model failure** | If confidence model returns an error, exception, timeout, score outside 0–100, or null/NaN → display SAP count with staleness timestamp and no verdict label; do not show Available/Low stock/Uncertain |
| **Fallback — SAP also unavailable** | If model fails AND SAP is unreachable → show degraded mode message only; do not attempt to display a count |
| **Eval metric — precision** | ≥ 90% of Available verdicts confirmed on shelf at collection, within 90 days of launch. Measured via OMS cancellation reason vs. verdict at reservation time. |
| **Eval metric — recall** | ≤ 20% of actual on-shelf items returned as Uncertain (false negatives). Unconstrained recall allows gaming precision by defaulting to Uncertain — both metrics required. |
| **Privacy note** | Staff scan events must be anonymised/aggregated before use as a signal. Raw staff-scan data is employee personal data under GDPR; a DPIA is required before ingestion. |

```gherkin
# Happy path
Given the confidence model has ≥ 2 of 5 fresh signals available for the target store/SKU/size
When a shopper taps "Check availability"
Then the model returns a confidence score in the range 0–100 (inclusive)
And the score maps to the correct verdict tier per the defined thresholds

# Error path — insufficient signals (including stale)
Given fewer than 2 of 5 signals are available or fresh at query time
When a shopper taps "Check availability"
Then the assistant falls back to degraded-mode display (S4 behaviour)
And no verdict label is shown

# Error path — out-of-range or null score
Given the model returns a score outside 0–100, or returns null or NaN
Then the assistant treats this as a model failure
And falls back to SAP count + staleness timestamp with no verdict label

# NFR — precision + recall
Available verdicts: ≥ 90% precision within 90 days (item confirmed on shelf)
Uncertain verdicts for actually-available items: ≤ 20% false-negative rate within 90 days
Both measured via OMS cancellation reason + post-launch audit
```

---

### S3 — Nearest alternative store

**Story:** As a click-&-collect shopper who receives an Uncertain verdict, I want to see the nearest store with a confirmed Available verdict, so that I can redirect rather than abandon the purchase.

```gherkin
# Happy path
Given a shopper has received an Uncertain verdict for their selected store
When the verdict is displayed
Then the assistant shows the nearest store (by road distance) within 25 km with an Available verdict
And the suggestion includes store name, road distance, and the Available verdict label
And if two stores are equidistant (within 100 m), the store with the higher confidence score is shown

# Error path — no alternative found within radius
Given no store within 25 km has an Available verdict for the selected SKU/size/colour
When an Uncertain verdict is displayed
Then the assistant shows "No nearby store currently shows confirmed availability"
And it does not surface a Low stock store as an alternative
And the shopper can still proceed with a reservation at their original store

# Error path — location permission denied by user
Given the shopper declines location access
When an Uncertain verdict is displayed
Then the assistant prompts for a postcode entry to find alternatives
And if the shopper also skips postcode entry, the feature completes with no alternative suggestion shown

# Error path — geolocation API technical failure (not user denial)
Given the geolocation API returns a technical error (timeout or permission error distinct from user denial)
When an Uncertain verdict is displayed
Then the assistant prompts for postcode entry as the fallback
And logs the geolocation failure for observability (not surfaced to shopper)

# Error path — nearest alternative store changes verdict before shopper acts
Given a shopper has been shown Store B as the nearest Available alternative
When the shopper taps through to Store B
Then the assistant re-queries availability for Store B at that moment
And if Store B's verdict has changed to Low stock or Uncertain, a fresh verdict is displayed before reservation

# NFR — latency
The alternative store lookup must complete within the same 5-second total budget as the primary verdict

# NFR — privacy (GDPR)
Shopper location data collected for the alternative-store lookup must have an explicit lawful basis (Article 6)
Location data must not be retained beyond the current session
A privacy notice must be shown before location permission is requested
```

---

### S4 — Degraded mode

**Story:** As a click-&-collect shopper, I want the assistant to work even when live signals are unavailable, so that I'm not blocked from browsing or reserving.

```gherkin
# Degraded trigger — stale SAP data
Given SAP sync lag at the target store exceeds 4 hours
# (lag measured from the last successful sync timestamp recorded in the sync log)
When a shopper taps "Check availability"
Then the assistant displays "Live availability check unavailable — stock data may be delayed"
And shows the last-known SAP count with staleness timestamp ("Stock count as of [time]")
And the reservation CTA remains visible and tappable

# Degraded trigger — low POS activity
Given fewer than 2 POS events have occurred at the target store in the rolling 24-hour window ending now
When a shopper taps "Check availability"
Then the same degraded-mode message and last-known count are shown

# Error path — last-known SAP count is zero
Given SAP sync lag exceeds 4 hours AND the last-known count is 0
When the degraded mode is displayed
Then the assistant shows count 0 and staleness timestamp
And the reservation CTA remains visible (the shopper may still attempt a reservation)
And no Available/Low stock/Uncertain verdict label is shown

# Error path — signal API timeout (within 5s budget)
Given the signal API returns no response within 5 seconds
Then the UI falls back to degraded mode at the 5-second mark
And the total page response time from tap to degraded-mode render is ≤ 8 seconds
And no technical error code or stack trace is shown

# Error path — recovery while shopper is viewing degraded UI
Given a shopper is viewing the degraded-mode message
When SAP sync recovers and lag drops below 4 hours
Then the degraded message does not auto-refresh to a new verdict without a fresh user tap
And on the next "Check availability" tap the fresh verdict is shown (not the cached degraded state)

# Error path — SAP and model both unavailable
Given both SAP and the confidence model are unreachable
When a shopper taps "Check availability"
Then the assistant shows only the degraded-mode message with no count and no staleness timestamp
And reservation remains accessible

# NFR — latency contract (reconciled)
Degraded mode must render within 8 seconds of a tap (inclusive of the 5-second signal timeout wait)
This 8-second ceiling applies only to degraded mode; the normal-path p95 ceiling remains 5 seconds

# NFR — observability
All degraded-mode triggers (SAP lag, POS threshold, API timeout, model failure) must be logged
Alerting must fire if degraded-mode rate across any store exceeds 10% of availability-check requests in a rolling hour
```

---

## Adversarial pass — fresh session critique log

57 issues identified. Patched in top 4 stories: issues 1–4, 5–6, 7–8, 13–14, 16, 23, 28, 33–36, 45–46, 52. Remaining open issues carried forward as known backlog debt.

### (A) Missing edge cases — patched
- **1** Boundary at exactly 80% and 50% → defined: 80 = Available, 50 = Low stock
- **2** Colour not selected but size is → added error path in S1
- **3** Verdict goes stale after variant change → added clear-on-change AC in S1
- **4** Rapid repeated taps → debounce requirement added in S1
- **5** Last-known count = 0 in degraded mode → error path added in S4
- **6** Recovery from degraded mode → no-auto-refresh AC added in S4
- **7** Score outside 0–100 or null → out-of-range guard added in S2 Eval Card
- **8** Logically impossible signal value → flagged as open; requires data validation layer (backlog)

### (A) Missing edge cases — open (backlog)
- **9** Nearest alternative store changes verdict before shopper acts → patched in S3
- **10** Two equidistant stores → tiebreaker (higher confidence score) added in S3
- **11** Phantom-stock rate time window undefined → defined as 30-day rolling in Eval Card
- **12** C&C availability changes between page load and tap → open; requires event-driven cache invalidation design

### (B) Missing error paths — patched
- **13** SAP lag 1–4h window (between normal and degraded) → clarified: SAP counts as "available" signal if lag ≤ 4h; stale = unavailable
- **14** Geolocation API technical failure → added as separate error path in S3
- **15** SAP also unavailable on model failure → double-failure path added in S2 Eval Card and S4
- **16** Exactly 2 signals = full path, not degraded → clarified in Eval Card

### (B) Missing error paths — open (backlog)
- **17** Network connectivity lost mid-request → open
- **18** Signal API returns HTTP 200 with malformed payload → open; signal treated as unavailable
- **19** No store at any distance has Available → open; "no radius" now defined as 25 km
- **20** Store does not support C&C for specific SKU → open

### (C) Missing NFRs — patched
- **23** Recall metric missing → ≤20% false-negative rate added to S2 Eval Card
- **25** WCAG accessibility → added to S1
- **28** 5s vs 8s latency conflict → reconciled in S4 with explicit note
- **30** Observability → logging + alerting NFR added to S4

### (C) Missing NFRs — open (backlog)
- **21** No uptime/SLA → open
- **22** No peak-load / concurrency requirement → open
- **24** No remediation SLA if 90-day metric missed → open
- **26** No localisation requirement → open (22-country scope)
- **27** No cache TTL for verdicts → open
- **29** No verdict consistency tolerance → open
- **31** No rate-limiting per session → open

### (D) Ambiguous language — patched
- **33** "signals available" — stale signals now explicitly counted as unavailable
- **35** SAP lag measurement — defined as "from last successful sync timestamp"
- **36** POS 24h window — defined as rolling 24h ending now
- **37/38** "nearest" and "radius" — defined as road distance, 25 km radius, 100 m equidistant tiebreaker

### (D) Ambiguous language — open (backlog)
- **32** "real-time" in title → renamed to "availability verdict" (removed "real-time")
- **34** "model failure" scope → partially addressed; full enumeration deferred to engineering spec
- **39–44** Remaining ambiguities → open; to address in PRD scope boundary (K 2.W.7)

### (E) Security / privacy — patched
- **45–46** GDPR lawful basis + retention for location data → GDPR NFR added to S3
- **52** Staff scan events as employee personal data → privacy note + DPIA requirement added to S2 Eval Card

### (E) Security / privacy — open (backlog)
- **47** Logging of shopper queries against user identifiers → open; requires data-privacy review
- **48** SAP count + staleness exposed in fallback payload → open; requires API response review
- **49** No auth on signal APIs → open; security architecture decision
- **50** Input validation on parameters → open; security requirement for engineering
- **51** Rate-limiting on availability check → open
- **53** TLS requirement not stated → open
- **54** CDN cache cross-session risk → open
- **55** EU AI Act transparency obligations → open; legal review required
- **56** ESPR compliance coupling → open; out of feature scope but flagged for product counsel
- **57** Location data if permission revoked mid-session → open
