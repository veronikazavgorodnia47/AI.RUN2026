# 01 — AI Feasibility + Scope Gate
**Kata K 3.D.1 | Consumes:** feature brief, K 3.W.1 verdicts, Wide `06-context.md`

---

## User problem — outcome sentence

A click-&-collect shopper needs to know whether a specific item is truly collectable at a nearby Meridian store **before** making the trip, so they can commit or redirect without risk of a wasted journey.

*Not a feature request. Not "we need an availability widget."*

---

## Gate 1 — AI in the Process (delivery)

| Check | Status | Note |
|---|---|---|
| Client permits AI tools for delivery? | ✅ Yes | EPAM CodeMie Claude approved without restriction |
| Third-party AI tools permitted? | ⚠️ Conditional | Claude / GPT / Gemini require anonymised inputs only |
| Sensitive data kept out of AI inputs? | ✅ Yes | Stock + store metadata only; no customer identity, no order history, no PII |
| Approved toolset named? | ✅ Yes | CodeMie Claude, Claude, v0/Lovable for prototyping |

**AI speed/scale moment used:** Pressure-tested the brief with CodeMie Claude against two gates; kept only challenges that mapped to actual feature scope. Challenges rejected: "regulatory classification for ML model" (not the assistant's concern yet — product legal path), "automated threshold adjustment" (out of scope for this feature).

**Verdict: Conditional** — third-party tools permitted with anonymised inputs only; CodeMie pre-approved.

---

## Gate 2 — AI in the Product

| Check | Status | Note |
|---|---|---|
| Stock data ready and fresh enough? | ⚠️ Conditional | SAP sync is 15–30 min stale; no real-time shelf scan exists |
| Worst-case user harm understood? | ✅ Yes | Shopper travels to store; item is gone. Wasted trip + trust damage. |
| Regulatory framework clear? | ⚠️ Conditional | EU AI Act risk classification unconfirmed; legal sign-off required before launch |
| Privacy / consent surface clear? | ✅ Yes | Non-PII stock + store metadata only; GDPR applies to any personalised layer |
| No guarantee of hold? | ✅ Mandatory | The assistant is an estimate, not a reservation system |

**Verdict: Conditional** — availability assistant may ship, subject to:
1. Staleness warning shown whenever data is shown (no silent estimate).
2. No green "In stock" state at any confidence level.
3. EU AI Act sign-off obtained before launch.
4. Confidence threshold validated against actual SAP sync-window data before launch.

*One-liner for a product owner to read aloud:* "We can show availability estimates, but only if we always flag data age and never promise a hold — until legal clears the EU AI Act question."

---

## Data, consent, and sensitivity check

| Dimension | Status | Detail |
|---|---|---|
| Data source | SAP inventory sync | 15–30 min latency; treated as estimate, not ground truth |
| Freshness window | 15–30 min | Must be surfaced to user at all times — not hidden in tooltip |
| User-visible consequence of a false answer | High | Shopper travels to store, item is not there |
| PII / sensitive data in AI path | None | Stock count and store metadata only |
| GDPR scope | Applies | Any personalised surface (e.g. location-based store sort) triggers consent layer |
| EU AI Act | Unresolved | Risk category unconfirmed; legal review required before launch |

---

## Overall verdict

> **Conditional Go**
>
> AI belongs in this feature. The conditions — staleness disclosure, no-green-badge rule, no-firm-hold rule, EU AI Act legal clearance — must be met before the assistant is production-ready. Features may proceed to design and prototype with these conditions recorded.

---

## Scope boundary — we will / we won't

| We will | We won't |
|---|---|
| Show an availability estimate labelled as an estimate | Show a green "In stock" badge at any confidence level |
| Surface data freshness ("updated X min ago") inline | Display exact unit counts |
| Show a fallback ("Check in store" + phone) when data is stale or missing | Promise a guaranteed hold or reservation |
| Allow the user to request a hold (as a confirmed non-firm soft-hold) | Route the hold through an autonomous AI agent without human confirmation |
| Use AI to generate design and copy assets during delivery | Paste live order IDs, customer records, or proprietary store data into non-approved tools |

---

## AI-native escalation flags

The following would move this feature out of the Practitioner bridge into AI-native territory and must be escalated:

| Scenario | Escalation route |
|---|---|
| The model begins autonomously adjusting confidence thresholds or hold logic (OODA loop becomes self-driving) | Architecture + Product Owner |
| The assistant is extended to make multi-step decisions across user sessions without HITL | AI-native architecture review |
| EU AI Act classification lands as high-risk | Legal + Compliance sign-off before further design work |
| Customer identity or purchase history enters the AI path | Privacy + GDPR review |

---

## Service sketch — three key steps

Four rows: **User Actions → Frontstage UI → Backstage Systems → Support Processes**

| | Step 1: Check availability | Step 2: Request soft hold | Step 3: Arrive at store |
|---|---|---|---|
| **User Actions** | Opens product page; selects nearby store | Taps "Request hold" after seeing estimate | Arrives at counter; collects or is told item is gone |
| **Frontstage UI** | AvailabilityBadge (amber: Likely / Limited); freshness timestamp; fallback if stale | Hold request confirmation modal; no-guarantee disclosure | Pickup confirmation; feedback prompt ("Was the item available?") |
| **Backstage Systems** | SAP inventory sync (15–30 min); confidence score computed server-side; SAP sync age check | Hold queue (separate workstream — not AI-owned) | Feedback log (store + SKU + timestamp → model improvement) |
| **Support Processes** | Store associate sees hold notification (out of scope here) | Manual override if hold queue fails | Associate handles mismatch; support ticket path |

**OODA check:** the model's loop is Observe (SAP sync) → Orient (confidence score) → Display (badge). It does not Decide autonomously (no self-adjusting thresholds) and does not Act independently (no hold placed without user action). This stays **inside** the Practitioner bridge. If the loop closes end-to-end without a human confirmation step for holds, escalate.

---

## Carry-forward constraints for K 3.D.2+

- Staleness disclosure is mandatory on every displayed estimate — not a tooltip; inline.
- No green badge, no exact count, no firm hold at any fidelity level.
- EU AI Act sign-off is a launch gate, not a design gate — design may proceed.
- Confidence threshold (0.7 amber split) is an assumption — must be validated against real sync data.
- Data freshness window (15–30 min) is the key risk variable for all subsequent synthesis and trust work.
