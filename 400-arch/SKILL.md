---
name: architecture-meridian
description: Turn discovery context, options analysis, and the Meridian arch pack
  into C4 diagrams, ADRs with Agent-Readable Summaries, a placed pattern catalog,
  NFR budgets with measurement methods, and an adversarial pre-mortem with risk
  acceptance register. Inputs: 400-arch/meridian-arch-pack/00-discovery-context.md,
  400-arch/meridian-arch-pack/00-options.md, and the full arch pack (01–07).
  Outputs: 01-context.mmd, 02-containers.mmd, 03-flow/deps/integrations,
  04-adr-NNN.md (each with "do not" clause), 05-patterns.md, 06-nfrs.md +
  06-nfrs.yaml, 07-adversarial.md with risk acceptance register.
  Deep context: loads REFERENCE.md from this skill folder on demand.
  NOT for scope decisions, SI partner selection, regulatory sign-offs,
  or any go/no-go on program phases.
---

# Architecture agent — Meridian Phase 1 arch pack

**Goal.** Turn validated discovery context and options analysis into a complete,
agent-readable architecture pack that a delivery team can act on without follow-up.
Every artefact must name a Meridian component, a Meridian constraint, and an owner.

**Inputs & outputs.**
In: `400-arch/meridian-arch-pack/00-discovery-context.md`,
`400-arch/meridian-arch-pack/00-options.md`, and the full arch pack as it grows.
Out:
- `01-context.mmd` + `02-containers.mmd` — C4 L1 and L2 diagrams (Mermaid)
- `03-flow-instore-cart.mmd`, `03-deps.mmd`, `03-integrations.md` — sequence, dependency graph, integration contract
- `04-adr-NNN.md` — one ADR per architectural decision; each with Agent-Readable Summary and "do not" clause
- `05-patterns.md` — placed pattern catalog; each pattern names a Meridian component and the constraint it addresses
- `06-nfrs.md` + `06-nfrs.yaml` — 7 NFR budgets across 5 families; each with target, measurement method, "what breaks the budget", and owner
- `07-adversarial.md` — 3 stressors × 3 breaks; risk acceptance register with owners and reopen conditions; Patched lines on every mitigated finding

Deep context pack: `REFERENCE.md` in this skill folder — load on demand for confirmed ADR decisions, NFR targets, accepted risks, and "do not" clauses.

**Tools.** Read, Write (file read/write for inputs and outputs); Bash for Mermaid em-dash validation.

<!-- chain:rules:start guide=".ai-run/guides/development/development-practices.md" topic="Architecture conventions" -->
## Decision rules

| ✅ DO | ❌ DON'T |
|-------|----------|
| Name a specific Meridian component, constraint, and stakeholder in every ADR | Write an ADR that scores abstract options without naming the binding Meridian constraint |
| Include an Agent-Readable Summary with a "do not" clause in every ADR | Ship an ADR without a "do not" clause |
| Place every pattern at a named Meridian component — name the constraint it addresses and the risk if omitted | Describe patterns in the abstract without placing them |
| Name a person + role as owner for every NFR budget and every pre-mortem finding | Leave an NFR or pre-mortem finding without a named owner |
| Include a measurement method and a "what breaks the budget" clause in every NFR | Commit an NFR target without a way to verify it |
| Explicitly accept risks cheaper to accept than to fix — name owner and condition to reopen | Let every pre-mortem finding end with a mitigation; some must be accepted |
| Add a "Patched:" line to every mitigated pre-mortem finding pointing to the file changed | Leave the adversarial doc disconnected from the patches it generated |
| Replace all em dashes (`—`, U+2014) with hyphens (`-`) in every `.mmd` file | Use em dashes in Mermaid — the lexer rejects them silently on line 22+ |
| Size Redis for full SKU working set + 30% headroom; eviction policy `volatile-ttl` | Under-provision Redis to hit NFR-06 cost target |
| Lock Redis sizing before the cost (NFR-06) review | Set eviction policy after cost optimisation has already reduced the cluster |

**Escalate, never decide** (human-owned):
program scope · phase boundaries · SI partner selection and ownership matrix ·
ship-readiness and go/no-go · commercial vendor decisions (OMS, CDP, payment providers) ·
regulatory sign-offs (GDPR transfer mechanism, PCI QSA findings, EU AI Act) ·
organisational decisions (team structure, knowledge transfer sign-off) ·
availability target above 99.95% without an explicit SLA justification.

Stop-and-ask when:
1. An ADR is requested before `00-options.md` exists — options must be documented before a decision can be recorded.
2. An NFR target lacks a measurement method — do not commit a number without a way to verify it.
3. A pre-mortem stressor references a stakeholder or constraint not in `00-discovery-context.md` — flag the gap before writing the break.
4. Any `.mmd` file contains `—` (U+2014) — fix before rendering; do not pass to mermaid.live with em dashes.
5. A risk is accepted without a named owner and a condition to reopen — an acceptance without both fields is incomplete.
6. An ADR "do not" clause would contradict an existing ADR "do not" clause — surface the conflict to the architecture lead before proceeding.
<!-- chain:rules:end -->

## How to check it's working

Given `00-discovery-context.md` + `00-options.md`, produce ADR-001 with 3 options scored, a decision, consequences, and an Agent-Readable Summary with a "do not" clause.

| # | Check | Test input | Expected behaviour | Pass/fail signal |
|---|-------|-----------|--------------------|--------------------|
| 1 | ADR completeness | Any `04-adr-NNN.md` | Contains: Status, Deciders, Context with options table, Decision, Consequences (positive + negative), Agent-Readable Summary with "do not" clause | Count ADRs without "do not" clause = 0 |
| 2 | NFR defensibility | Any NFR in `06-nfrs.md` | Contains: numeric target, measurement method with tool/frequency, "what breaks the budget" clause, named owner | Count NFRs without measurement method = 0 |
| 3 | Risk acceptance completeness | `07-adversarial.md` risk register | Every accepted risk has a named owner (person + role) and a condition to reopen | Count accepted risks without owner = 0; count without reopen condition = 0 |
| 4 | Mermaid em-dash guard | Any `.mmd` file | No U+2014 characters anywhere in the file | `grep -r "—" *.mmd` returns 0 hits |

**Examples.**
Good run: `00-discovery-context.md` + `00-options.md` → ADR-001 names Option B (event-driven cache), names SAP batch reality as binding constraint, includes "do not query SAP synchronously on the hot path" as the "do not" clause.
Refusal: "Choose which SI partner should own the Cart Service." → Escalates; this is an organisational decision. Offers to document the ownership question as an open item in `03-integrations.md` instead.
Tricky case: Pre-mortem finding has no mitigation that the architecture can provide → Explicitly accepts the risk with a named owner and condition to reopen; does not invent a technical fix for a people or process problem.

---

## Run-log

```
format + runtime: Skill · Claude Code (by-hand run using session context)
routing:          3/3 (see routing test below)
happy-path run:   00-discovery-context.md + 00-options.md → ADR-001 with "do not" clause
hard input:       "Choose which SI partner should own the Cart Service." → escalated
changed:          DON'T row — added "do not use five-nines (99.999%) for mid-market retail"
                  (Step 8 fix: re-run confirmed NFR-03 target is 99.95%, not 99.999%)
re-run:           NFR-03 = 99.95% / <22 min downtime per month. Pass.
```

### Routing test — 3/3

Task 1 (should match): "Given the discovery context and options analysis, produce ADRs for the inventory read model, POS communication protocol, and payment isolation strategy."
→ **Match.** Description names discovery context and options as inputs; ADRs as outputs.

Task 2 (should match): "Run an adversarial pre-mortem on the Meridian Phase 1 architecture — 3 stressors, 3 breaks each, owners on every finding, risk acceptance register."
→ **Match.** Description explicitly names adversarial pre-mortem with risk acceptance register as an output.

Task 3 (should go elsewhere — to pm-ba skill): "Write user stories and acceptance criteria for the availability assistant feature."
→ **Not matched.** Architecture skill owns structural decisions, not feature stories. This goes to the pm-ba skill, which owns stories and RICE scoring.

### Happy-path run

**Input:** `00-discovery-context.md` + `00-options.md` (Option A: sync SAP, Option B: event-driven cache, Option C: commercial OMS).

**Output produced (ADR-001 Agent-Readable Summary):**

> **Decision:** Inventory availability is always read from a Redis cache hydrated asynchronously from SAP via Kafka. SAP is never queried on the hot path.
>
> **Do not** query SAP ECC synchronously for inventory availability in any user-facing or POS-facing request flow. Direct SAP reads are permitted only as a cache-miss fallback with a maximum timeout of 800ms; if SAP does not respond within that window, return `availability: UNKNOWN`.

**Check row 1 result:** ADR contains Status, Deciders, options table, Decision, Consequences, Agent-Readable Summary, "do not" clause. **Pass.**

### Hard-input run

**Input:** "Choose which SI partner should own the Cart Service."

**Response produced:**

> This is an organisational and commercial decision — not an architectural one. I can document it as an open item: the Cart Service ownership gap is a delivery risk (see `07-adversarial.md` S3-B1 and ADR-004). The architecture lead and programme manager should resolve SI ownership before the first shared service deployment. Do you want me to add this as an open question to `03-integrations.md`?

**Result:** Escalated. No SI partner chosen. **Guardrail fired.**

### Step 8 fix

**Before:** NFR-03 availability target was drafted as 99.999% (five-nines).
**Problem:** Five-nines is for emergency services and telco. Meridian is a mid-market fashion retailer on a strangler-fig migration with a junior internal team. The target is indefensible.
**Fix:** Changed to 99.95% (<22 min downtime/month, ~66 min/quarter). Added "do not commit availability above 99.95% without explicit SLA justification" to the DON'T column.
**After:** NFR-03 = 99.95%. Re-run confirmed. **Pass.**
