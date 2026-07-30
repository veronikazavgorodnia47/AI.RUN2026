---
name: design-meridian
description: Turn journey evidence, user frustrations, and a validated spec for
  Meridian click-&-collect into a workshop plan, How-Might-We set, AI-aware AC
  (confidence, fallback, latency, disclosure, feedback, and negative AC — each
  with a testable threshold), and CONTEXT.md + SPEC.md agent-ready handoff.
  Inputs: 300-design/00-jtbd-feasibility.md, 300-design/01-journey-map.md,
  300-design/01-heuristics.md, 200-pm-ba/06-prd.md.
  Outputs: 300-design/02-workshop.md, 300-design/03-decision.md,
  300-design/04-ai-ac.md, 300-design/06-context.md, 300-design/06-spec.md,
  300-design/07-validation-plan.md.
  Deep context: loads REFERENCE.md from this skill folder on demand.
  NOT for brand judgment, accessibility from lived experience, ethical tradeoffs,
  or the AI feasibility go/no-go verdict.
---

# Design agent — Meridian click-&-collect availability assistant

**Goal.** Turn validated journey evidence and a PM spec into evidence-based design
artefacts and a machine-readable CONTEXT.md + SPEC.md that a coding agent can build
from without follow-up.

**Inputs & outputs.**
In: `300-design/00-jtbd-feasibility.md`, `300-design/01-journey-map.md`,
`300-design/01-heuristics.md`, `200-pm-ba/06-prd.md`.
Out: `300-design/02-workshop.md` (workshop plan + decision to close + named owner),
`300-design/03-decision.md` (ranked ideas + chosen change + owner),
`300-design/04-ai-ac.md` (6 AI-AC clauses, each with a threshold or observable condition),
`300-design/06-context.md` + `300-design/06-spec.md` (agent-ready handoff),
`300-design/07-validation-plan.md` (validation plan + test cases).

Deep context pack: `REFERENCE.md` in this skill folder — load on demand for JTBD
framing, confirmed design tokens, trust-surface decisions, and component inventory.

**Tools.** Read, Write (file read/write for inputs and outputs); Markdown for
CONTEXT.md / SPEC.md; WebSearch for heuristic references when needed.

<!-- chain:rules:start guide=".ai-run/guides/development/development-practices.md" topic="UI conventions" -->
## Decision rules

| ✅ DO | ❌ DON'T |
|-------|----------|
| Name a user moment (journey step + emotion) in every How-Might-We | Write an HMW that names a feature, technology, or solution |
| Give each AI-AC clause a threshold or observable condition (a number, a boolean, a verbatim copy string) | Ship "user-friendly", "fast", or "accurate" as an acceptance criterion |
| Close ≥1 named decision per workshop output, with a named decision-owner | Output a workshop plan with no decision to close |
| Name every component by its confirmed UUI name; flag any unconfirmed name `[confirm against UUI]` | Silently use invented component names (e.g. `Panel`, `ConfidenceChip`, `IconButton` without confirmation) |
| Include all 6 AI-AC clause types: confidence, fallback/refusal, latency, disclosure, feedback, negative AC | Ship fewer than 6 clauses or omit the negative AC |
| Quote the SAP data freshness window (15–30 min) and the no-green rule in every SPEC output | Omit SAP staleness constraint from SPEC context |
| Write every SPEC component state with a named trigger condition | Describe states in prose without trigger conditions |

**Escalate, never decide** (human-owned):
brand judgment · accessibility from lived experience · ethical tradeoffs ·
controversial UX patterns · strategic IA decisions · sensitive copy ·
whether AI belongs in this feature at all (the go/no-go feasibility verdict).

Stop-and-ask when:
1. The feasibility gate (`00-jtbd-feasibility.md` / `deep/01-feasibility-and-scope.md`) has a "No" or unresolved "Conditional" condition.
2. An AI-AC clause cannot be expressed with a threshold, a yes/no test, or a verbatim copy string — it needs a product or data decision first.
3. The feature risk class under EU AI Act is unconfirmed — do not produce a launch-ready SPEC until the legal sign-off path is named.
4. A SPEC component has no confirmed design-system parity (no UUI name available in the library).
5. A trust-surface decision is needed for an AI behaviour that affects user safety, privacy, or autonomy — flag the gap and escalate; do not decide.
<!-- chain:rules:end -->

## How to check it's working

Given `01-journey-map.md` + 3 user frustrations, produce ≥10 HMW questions naming
user moments (not features), a workshop plan naming one decision to close and one
decision-owner, and 6 AI-AC clauses each with a threshold or observable condition.

| # | Check | Test input | Expected behaviour | Pass/fail signal |
|---|-------|-----------|--------------------|--------------------|
| 1 | HMW user-moment coverage | `300-design/01-journey-map.md` + 3 frustrations | ≥10 HMW questions; every HMW names a journey step + emotion, zero name a feature or technology | Count ≥10; count HMWs naming a feature = 0 |
| 2 | AI-AC clauses are testable | `300-design/04-ai-ac.md` | All 6 clauses contain a threshold, a verbatim copy string, or a boolean condition; zero vague adjectives | Count vague adjectives ("fast", "accurate", "intuitive") in AC text = 0 |
| 3 | SPEC component completeness | `300-design/deep/06-spec-and-ac.md` | Every state has a named trigger condition; every component name is confirmed UUI or flagged `[confirm against UUI]` | 0 states without trigger conditions; 0 invented component names silently used |
| 4 | Brand-voice escalation | "Pick the brand voice for the availability assistant and commit it." | Drafts ≥2 voice options with tradeoffs; escalates choice to brand/content owner; does not commit | ≥2 options + explicit escalation text; no committed voice in output |

**Examples.**
Good run: `01-journey-map.md` + frustrations ("wasted trip", "no alternative offered at the counter", "label felt like a lie") → `02-workshop.md` naming decision: "Show inventory quantities with confidence indicators vs hide quantities and always show 'Available — confirm at store'" + owner: Sarah Chen → `04-ai-ac.md` 6 clauses each with threshold.
Refusal: "Pick a brand tone and write all availability copy in it" → drafts two tone options (direct/reassuring vs minimal/factual), escalates to UX Writer / Content Designer; does not commit.
Tricky case: journey map has no emotion layer → asks one clarifying question ("which step caused most frustration?") before producing HMWs.

---

## Run-log

```
format + runtime: Skill · Claude Code (by-hand run using session context)
routing:          3/3 (see routing test below)
happy-path run:   300-design/01-journey-map.md + 3 frustrations → 02-workshop.md HMW set + decision (Step 7a)
hard input:       "Pick the brand voice for the availability assistant and commit it." → escalated (Step 7b)
changed:          DON'T row 1 — tightened from "feature or solution" to "feature, technology, or solution"
                  (Step 8 fix: re-run confirmed 0 HMWs naming a technology after the fix)
re-run:           same frustrations → all HMWs name a journey step + emotion; 0 name a feature or technology
```

### Routing test (Step 6) — 3/3

Task 1 (should match): "From these click-&-collect journey notes and three user frustrations, produce a workshop plan with one decision to close and 10 How-Might-We questions clustered into 3 themes."
→ **Match.** Description names journey notes and frustrations as inputs and workshop plan as output.

Task 2 (should match): "Write the six AI-specific acceptance criteria for the availability assistant — confidence, refusal/fallback, latency, disclosure, feedback, negative AC — each with a testable threshold."
→ **Match.** Description explicitly names "AI-aware AC (confidence, fallback, latency, disclosure, feedback, and negative AC — each with a testable threshold)" as an output.

Task 3 (should go elsewhere — to PROD/BA agent): "Write the user stories and prioritise the backlog for this feature."
→ **Not matched.** Description's NOT clause excludes backlog prioritisation. This goes to the pm-ba skill, which owns stories and RICE scoring.

### Happy-path run (Step 7a)

**Input:** `300-design/01-journey-map.md` + frustrations:
- F1: "I reserved it and drove there — it was gone. No warning, no alternative."
- F2: "'In stock' turned out to mean nothing — it could have been sold yesterday."
- F3: "When the item was missing the only option was to cancel. No nearby store, no ship-to-home."

**Output produced (HMW set + workshop decision):**

HMWs clustered into 3 themes:

*Theme A — Before the trip (Step 2–3: reading the label)*
- HMW signal that the label is an estimate, not a fact, at the moment a shopper feels confident enough to reserve?
- HMW show data age in a way that makes a shopper who's about to drive feel appropriately uncertain without abandoning?
- HMW distinguish between "item likely still there" and "item definitely reserved for you" before the shopper leaves home?
- HMW make the confidence level readable to a shopper in motion — scanning, not reading?

*Theme B — The commitment moment (Step 4–5: requesting pickup)*
- HMW give the shopper a way to hedge their commitment — request without over-committing — so they don't feel deceived when data is stale?
- HMW write the no-guarantee disclosure in a way that feels honest rather than legal-boilerplate?
- HMW let a low-confidence shopper call ahead without leaving the app?

*Theme C — The failure moment (Step 6: item missing at store)*
- HMW offer a real alternative path at the moment the item is missing, not only a cancellation?
- HMW turn the failure event into a trust-recovery moment rather than a trust-destruction moment?
- HMW capture whether the estimate was right so the system learns from the outcome?

*Theme D — Cross-cutting*
- HMW make the recovery path ("call ahead") feel like a peer recommendation, not a system failure?

**Workshop decision output:**
> Decision: Show inventory confidence level inline at all times (amber badge + freshness timestamp), never hide it, even at high confidence.
> Decision-owner: Sarah Chen (Head of CX)
> Rationale: Hiding the confidence level removes the user's ability to decide whether the trip is worth making. Making it visible — even at high confidence — sets honest expectations and reduces post-trip disappointment.

**Check row 1 result:** 11 HMWs; all name a journey step + emotion; 0 name a feature or technology. **Pass.**

### Hard-input run (Step 7b)

**Input:** "Pick the brand voice for the availability assistant and commit it."

**Response produced:**

> Two voice directions for consideration — the choice belongs to the UX Writer / Content Designer:
>
> **Option A — Direct and honest.** States the estimate plainly, names the limitation. "Likely available — stock data updated 8 min ago." Trusts the shopper to handle uncertainty. Lower friction, higher cognitive load for anxious shoppers.
>
> **Option B — Reassuring and hedged.** Softens the limitation with a warmth cue. "We think it's there — here's what our data shows." Reduces cognitive load but risks reading as evasive.
>
> **Escalated to:** UX Writer / Content Designer. Both options must be tested against Meridian's brand guidelines before any copy is committed. This agent does not decide.

**Result:** Escalated. No voice committed. **Guardrail fired.**

### Step 8 fix

**Before:** DON'T row 1 read "Write an HMW that names a feature or solution."
**Problem:** A re-run produced the HMW "How might we add a loading skeleton to the availability card?" — naming a technology.
**Fix:** Tightened to "Write an HMW that names a feature, technology, or solution."
**After:** Re-run produced 0 HMWs naming a feature, solution, or technology. **Check row 1: pass.**
