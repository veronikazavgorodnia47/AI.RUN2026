---
kata: 10.W.7
consumes: 01-qualification.md, 02-solution.md, M500-engineering, M600-qa-report, M800-gateway-logs
date: 2026-08-10
---

# AI-Native Delivery Section — Meridian Unified ATP System

## Per-Phase Maturity Table

*Target maturity graded L1–L3 against the AI-SDLC Maturity Framework.
Metrics include a defined denominator — "AI use is high" is not a metric.*

| SDLC Phase | Target maturity | By month | Adoption metric (with denominator) | Tooling baseline | Named risk |
|---|---|---|---|---|---|
| **Intake** | L2 | Month 3 | ≥70% of GNG-submitted qualification memos include an AI-drafted risk register and win-theme analysis, reviewed and approved by a senior delivery lead before submission (denominator: all opportunities entering GNG review in the quarter) | DIAL — allow-listed; Claude — allow-listed | AI-drafted qualification memos may miss deal-specific context a senior reviewer would catch; quality depends on prompt discipline, not just tool access |
| **Plan** | L2 | Month 6 | ≥75% of sprint user stories have an AI-assisted draft AC reviewed and approved by the BA before sprint start (denominator: all stories in sprint backlog at planning) | DIAL, GitHub Copilot — both allow-listed | AI-drafted ACs may be technically correct but miss shopper-journey nuance from M200 personas (Clara / Ben); BA ownership of the AC is non-negotiable |
| **Build** | L2 → L3 | L2 by month 6; L3 by month 9 | ≥80% of merged PRs include an AI-assisted first-pass code review before the human reviewer signs off (denominator: all PRs merged in the sprint on the integration and ML branches) | GitHub Copilot — allow-listed; DIAL — allow-listed | AI code review may miss SAP integration edge cases specific to undocumented 22-country API variants; L3 requires prompt/rule library version-controlled in repo, not shared informally |
| **Validate** | L2 | Month 9 | ≥80% of test cases in each sprint test plan have an AI-generated first draft reviewed by the QA lead before execution (denominator: all test cases in the sprint test plan) | DIAL — allow-listed; Claude — allow-listed | AI-generated test cases are unlikely to cover the SAP staleness edge cases that produced DEFECT-03 (M600); QA lead must manually add guard tests GT-01–03 (M600 §4) to the regression suite — these cannot be AI-generated without a human who has read the RCA |
| **Handoff** | L2 | Month 12 | ≥90% of runbook sections have an AI-drafted first version reviewed and signed off by the ops lead before handover (denominator: all sections in the handover pack delivered to Lena Park's team) | DIAL — allow-listed | AI-drafted runbooks may not reflect operational decisions made during Phase 4 hardening; each section needs a named reviewer who was present in Phase 4 |
| **Learn** | L3 | Month 9 | 100% of retrospectives produce ≥1 version-controlled artefact committed to the delivery repo (denominator: all retros run on the engagement from month 3 onward) | DIAL for retro clustering and analysis — allow-listed | AI retro clustering may group symptoms without surfacing root causes; human facilitation is required for psychological safety; a retro that produces only a DIAL summary is not L3 |

---

## What is NOT automated — human-owned decisions

The following decisions stay with named humans and are never delegated to an AI agent,
regardless of maturity level:

- **Scope changes and contract amendments** — any change to the fixed-price scope baseline requires written sign-off from MRG Head of Omnichannel and Delivery Lead; AI may draft the change-request document, but the approval is human
- **Phase gate go/no-go** — each of M1–M6 is signed by the named human owner in `05-plan.md`; AI may prepare the gate-review pack, but the decision is not delegated
- **EU AI Act risk classification sign-off** — DPO owns the classification decision; AI (including DIAL) may assist with the Annex III checklist, but the signed filing is the DPO's artefact
- **Ship-readiness call at M6** — delivery lead and Head of Omnichannel sign off; the M600 test report HOLD status and M900 residual-risk contract must be resolved by named humans before go-live
- **Performance conversations and team resourcing** — delivery lead owns these; no AI agent surfaces or acts on performance signals
- **Client escalations** — P1 defects in production, DPA negotiation outcomes, and budget-overrun notifications are communicated by the delivery lead directly; AI may draft the communication, but the delivery lead sends it

---

## Measurement plan (source of truth per metric)

| Phase | Source of truth |
|---|---|
| Intake | DIAL usage telemetry (per-team tenant) + qualification memo version history in repo |
| Plan | Jira story labels (`ai-draft-ac`) + BA sign-off timestamp at sprint planning |
| Build | GitHub PR labels (`ai-reviewed`) + DIAL session log (per-team tenant, M800 gateway) |
| Validate | Test-plan Markdown commit history in repo + QA lead sign-off in PR description |
| Handoff | Runbook repo commit history + ops lead review comments on each section PR |
| Learn | Retro artefact commit count in delivery repo (one file per retro, tagged `retro-YYYY-MM-DD`) |
