# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

Veronika Zavgorodnia's learner project folder for the AI:RUN bootcamp (EPAM AI-Native SDLC program). Produces the artefact chain for **Case A: Meridian Retail Group** across modules. The curriculum itself lives in `curriculum-public-main/` (read-only — do not edit it). Module entry points are `modules/NNN-index.md`; canonical definitions are in `modules/000-glossary.md`.

GitHub remote: `veronikazavgorodnia47/AI.RUN2026`.

```bash
# Push to GitHub (SSH alias set up in ~/.ssh/config as github-airun)
git add <files> && git commit -m "message" && git push git@github-airun:veronikazavgorodnia47/AI.RUN2026.git main
```

Hidden files (e.g. `.claude/`) require **Cmd + Shift + .** in Finder to reveal, or **Cmd + Shift + G** → paste the full path. The `.claude/` directory is gitignored — copy skill files to their module directory (e.g. `500-eng/SKILL.md`) to track them on GitHub.

## Reference case

**Case A — Meridian Retail Group**: mid-market EU omnichannel fashion retail, Western Europe, €1–5B revenue, 22-country fragmented stack, GDPR + ESPR compliance pressure. Full snapshot in `001-reference-caseA.md`.

## Artefact chain — Module 100 (Consulting & SME, Wide path) ✅ complete

Root-level files. Each carries forward into the next; chain must stay on one reference case.

| File | Kata | What it is |
|---|---|---|
| `00-playground.md` | K 1.W.1 | 5-line industry playground |
| `01-context-brief.md` | K 1.W.2 | One-page market and trend scan; every claim named |
| `02-primary-signal.md` | K 1.W.3 | Customer verbatims + competitor teardown |
| `03-research-audit.md` | K 1.W.4 | Trust ledger: sourced / unverified / cut |
| `04-use-cases.md` | K 1.W.5 | 10 use cases scored value × feasibility; top 3 |
| `05-canvas.md` | K 1.W.6 | One-page opportunity canvas; critique log included |
| `06-roi.md` | K 1.W.7 | Three-scenario ROI; assumptions sourced or flagged `[unverified]` |
| `07-deck.md` | K 1.W.8 | 10-slide exec narrative (≤30 words/slide) |
| `opportunity-brief.md` | K 1.3 | Canonical carry-forward artefact — 9-field one-page Markdown |

`opportunity-brief.md` is the handoff point to PROD/BA.

**Module 100 scoring convention:** value × feasibility (multiplication, not addition). Scores 1–25; both axes 1–5.

**Module 100 research integrity:** tag every unverified claim; never build ROI or scoring on one without flagging it; every verbatim cites a named source and date; every feasibility score names the binding constraint.

## Artefact chain — Module 200 (PROD/BA, Wide path) ✅ complete

Files live in `200-pm-ba/`. Feature: AI availability assistant for Meridian click-&-collect (phantom-stock problem).

| File | Kata | What it is |
|---|---|---|
| `00-feature.md` | K 2.W.1 | 5-line feature frame |
| `01-vision.md` | K 2.W.2 | Vision + confidence thresholds + degraded-mode spec |
| `02-personas-journey.md` | K 2.W.3 | Clara + Ben personas; Mermaid journey map; flagged `[unverified]` |
| `03-competitors.md` | K 2.W.4 | IKEA / Zara / M&S teardown; differentiator statement |
| `04-stories-acs.md` | K 2.W.5 | 10 stories; Gherkin ACs for S1–S5; AI Eval Card for S2 |
| `05-backlog.csv` | K 2.W.6 | RICE-scored backlog (10 rows, sorted descending) |
| `05-backlog-notes.md` | K 2.W.6 | RICE assumptions; S7 scoring-artefact note; human override sequence |
| `06-prd.md` | K 2.W.7 | One-page PRD + Decision Memory DM-200-001 |
| `06-traceability.md` | K 2.W.7 | Story → outcome metric matrix; dependency chain |
| `07-release-comms.md` | K 2.W.8 | Scope confirmation, risks, stakeholder messages, release notes |

**Key Module 200 rules:**
- Confidence scores are integers 0–100 (not 0–1 floats). State the scale explicitly in every AI Eval Card.
- Every AC must be answerable yes/no. No vague adjectives ("fast", "accurate") as ACs.
- Every story traces to one outcome metric; every metric links to at least one story.
- Unverified claims tagged `[unverified]` before building stories or ROI on them.
- Human-owned (never decide): scope, prioritisation cuts, ship-readiness, which AI capabilities to offer.

**Module 200 delivery sequence** (human override; not RICE rank): S2 → S5 → S1 → S4 → S3 → S8 → deferred.

## Artefact chain — Module 300 (Design, Wide path) ✅ complete

Files live in `300-design/`. Feature: AI availability assistant for Meridian click-&-collect (phantom-stock problem). Veronika is a designer — Wide complete; Deep (K 3.D.1–9) is next, then one Final Kata (K 3.3) that draws on both.

| File | Kata | What it is |
|---|---|---|
| `00-jtbd-feasibility.md` | K 3.W.1 | JTBD statement + two-branch AI feasibility gate |
| `01-journey-map.md` | K 3.W.2 | Click-&-collect journey map with emotion + drop-off |
| `01-heuristics.md` | K 3.W.2 | Nielsen heuristic review — 8 validated findings |
| `02-workshop.md` | K 3.W.3 | Workshop plan: decision, HMWs, divergent ideas |
| `03-synthesis.md` + `03-decision.md` | K 3.W.4 | Impact × effort scoring; one decided change |
| `04-ai-ac.md` | K 3.W.5 | AI-aware acceptance criteria (6 clauses) |
| `05-mockup.html` | K 3.W.6 | Lo-fi prototype: happy path, low confidence, fallback |
| `06-context.md` + `06-spec.md` | K 3.W.7 | Agent-ready handoff pack (passes Definition of Handoff Done) |
| `07-validation-plan.md` + `07-narrative.md` | K 3.W.8 | Validation plan + 1-pager narrative |

## Artefact chain — Module 300 (Design, Deep path) 🔄 next

Files live in `300-design/deep/`. K 3.D.1–9 specialist series, then Final Kata K 3.3.

| File | Kata | What it is | Status |
|---|---|---|---|
| `deep/01-feasibility-and-scope.md` | K 3.D.1 | AI feasibility + scope gate | ✅ complete |
| `deep/02-synthesis-and-governance.md` | K 3.D.2 | Evidence synthesis + governance gate | ✅ complete |
| `deep/03-prompt-rules.md` | K 3.D.3 | Project prompt rules | ✅ complete |
| `deep/04-concept-and-audit.md` | K 3.D.4 | Audited behavioural concept | ✅ complete |
| `deep/05-conversation-flow.md` | K 3.D.5 | Conversational happy/sad paths | ✅ complete |
| `deep/06-spec-and-ac.md` | K 3.D.6 | AI-aware SPEC + AC | ✅ complete |
| `deep/07-code-prototype/` | K 3.D.7 | Token-bound prototype evidence | ✅ complete |
| `deep/08-trust-surface-and-risk-register.md` | K 3.D.8 | Trust surface + AI risk register | ✅ complete |
| `deep/09-eval-and-feedback.md` | K 3.D.9 | Evaluation + feedback loop | ✅ complete |
| `.claude/skills/design/SKILL.md` + `REFERENCE.md` | K 3.3 | Final Kata — Design role-agent (Deep specialist) | ✅ complete |

**Figma working file (Module 300 Deep):** `Pgmk44mu6RFylVWwT8rcVg` — AI-RUN Veronika. K 3.D.4 concept sketch lives here: Section node `3:24`, states row `3:27`. URL: `https://www.figma.com/design/Pgmk44mu6RFylVWwT8rcVg/AI-RUN-Veronika`

**Design system rules (apply from K 3.D onward):**
- Do NOT use emoji in any design artefact (prototype, SPEC, flow, component tree). Use UUI Asset icons instead.
- UUI Assets uses **lowercase-hyphenated** icon names (not PascalCase). Confirmed names: `notification-info` (info), `notification-done` (check/yes), `content-clear` (close/no/cancel).
- UUI component names confirmed: `Badge`, `Button`, `Icon Button` (two words), `Skeleton/Text Block`. **No standalone `Panel` component** — use a styled Frame for card containers.
- Feedback icons for binary yes/no: `notification-done` (✓) / `content-clear` (✗). Preferred over thumb metaphors for objective binary questions.
- Both UUI libraries are connected to the Figma file (`Pgmk44mu6RFylVWwT8rcVg`): **UUI Assets** + **UUI Components** (team libraries, no setup needed).
- All colour token hex values (amber-500, amber-700, neutral-600, neutral-500, neutral-200) are approximations — confirm against UUI library before build.

**Open items before build (consolidated):** see `300-design/deep/07-code-prototype/parity-checklist.md` §7. O-1/O-2 resolved. Remaining launch blockers: EU AI Act sign-off (O-7); confidence threshold 0.70 validation against real SAP data (O-8).

**Key Module 300 feasibility verdicts (from K 3.W.1):**
- Branch 1 (AI in process): Conditional — third-party tools require anonymised inputs; CodeMie pre-approved.
- Branch 2 (AI in product): Conditional — staleness warnings required; must NOT promise exact stock or guarantee holds; EU AI Act sign-off required before launch.

**Drop-off step (from K 3.W.2):** Step 6 — item is missing at the counter after the shopper has already committed (reserved + travelled).

**Workshop decision (from K 3.W.3):** Show inventory quantities with confidence indicators at all times vs. hide quantities and always show "Available for pickup — confirm at store". Decision-owner: Sarah Chen (Head of CX).

## Kata reference images

`Kata png /` (note: folder name has a trailing space) contains PNG rubric images for every kata. **Read the relevant image before starting any kata** — it shows the exact requirements and scoring criteria.

Naming: `Kata N.w.M.png` for Wide (e.g. `Kata 3.w.5.png`), `Kata N.d.M.png` for Deep (e.g. `Kata 3.d.6.png`). Final kata images: `Kata 1.w.Final.png`, `Kata 2.w.Final.png`. Images exist up to K 3.D.6 — no PNG yet for K 3.D.7 onward or K 3.3.

## Artefact chain — Module 400 (Architecture, Wide path) ✅ complete

Files live in `400-arch/meridian-arch-pack/`. Output: **Meridian Architecture Pack**.

| File | Kata | What it is | Status |
|---|---|---|---|
| `meridian-arch-pack/00-discovery-context.md` | K 4.W.1 | 4-layer context (business/product/engineering/regulatory) + 5 implicit assumptions | ✅ complete |
| `meridian-arch-pack/00-options.md` | K 4.W.2 | 3 divergent options for inventory/cart-bridge decision (sync SAP / event-driven cache / buy OMS) | ✅ complete |
| `meridian-arch-pack/01-context.mmd` | K 4.W.3 | C4 L1 context diagram (Mermaid) | ✅ complete |
| `meridian-arch-pack/02-containers.mmd` | K 4.W.3 | C4 L2 containers diagram (Mermaid) | ✅ complete |
| `meridian-arch-pack/03-flow-instore-cart.mmd` | K 4.W.4 | Sequence diagram: store associate cart-bridge flow with p95 latency | ✅ complete |
| `meridian-arch-pack/03-deps.mmd` | K 4.W.4 | Dependency graph: POS Client transitive dependencies | ✅ complete |
| `meridian-arch-pack/03-integrations.md` | K 4.W.4 | Integration contract skeleton: POS → Apollo Gateway cart-lookup | ✅ complete |
| `meridian-arch-pack/04-adr-001.md` – `04-adr-004.md` | K 4.W.5 | 4 ADRs with Agent-Readable Summary ("do not" clause each); ADR-004 forced by pre-mortem | ✅ complete |
| `meridian-arch-pack/05-patterns.md` | K 4.W.6 | Placed pattern catalog (Strangler Fig, Outbox, Bulkhead, Circuit Breaker, BFF) | ✅ complete |
| `meridian-arch-pack/06-nfrs.md` + `06-nfrs.yaml` | K 4.W.7 | 7 NFR budgets (latency/cost/quality/reliability/security) | ✅ complete |
| `meridian-arch-pack/07-adversarial.md` | K 4.W.8 | Pre-mortem: 3 stressors × 3 breaks; 4 accepted risks; 5 patched findings | ✅ complete |
| `.claude/skills/architecture/SKILL.md` + `REFERENCE.md` | K 4.3 | Architecture role-agent (Final Kata) | ✅ complete |

**Mermaid diagrams:** paste `.mmd` files into [mermaid.live](https://mermaid.live) to render. Em dashes (`—`) must be replaced with `-` — Mermaid's lexer rejects them.

## Artefact chain — Module 500 (Engineering, Wide path + Final Kata) ✅ complete

Sandbox repo: `veronikazavgorodnia47/logsum-sandbox`. Feature: `logsum` — tiny Python CLI that reads synthetic `events.csv` and writes a counted `summary.csv`.

| File | Kata | What it is | Status |
|---|---|---|---|
| `spec.md` | K 5.W.1 | Signed-off spec: goal, inputs, outputs, normalisation, grouping, aggregation, edge cases, CLI, out of scope | ✅ complete |
| `src/logsum.py` + `src/__init__.py` | K 5.W.2 | Implementation: `_normalise_row`, `process`, `_write_output`; `--min-count` flag | ✅ complete |
| `tests/test_logsum.py` | K 5.W.3 | 52 tests generated in isolation (Tier A) against spec ACs | ✅ complete |
| `.github/workflows/ci.yml` + `ci-notes.md` | K 5.W.4 | GitHub Actions CI: ruff check + pytest -v on Python 3.11; red→green run recorded | ✅ complete |
| `refactor-notes.md` | K 5.W.6 | 7 removed lines with keep/remove justification; tests remain green | ✅ complete |
| `CLAUDE.md` (sandbox) + `provenance.md` | K 5.W.7 | Hot layer (commands, architecture, test helpers, escalation gates) + provenance block | ✅ complete |
| `questions.md` | K 5.W.8 | 3 Q&As with file:line citations, all verified correct | ✅ complete |
| `by-hand-vs-agent.md` | K 5.W.9 | Supervised vs async replay comparison (6 sections) | ✅ complete |
| `500-eng/SKILL.md` | K 5.3 | Engineering role-agent (Final Kata); 3/3 evals green; run-log filled | ✅ complete |

**Sandbox repo:** `veronikazavgorodnia47/logsum-sandbox` — Python 3.11, stdlib only (`csv`, `argparse`, `collections`, `datetime`), ruff + pytest CI.

**K 5.3 eval results:** Eval 1 (AC coverage) — 124/124 tests, Tier A, 18/18 ACs; Eval 2 (gate refusal) — refused skip-tests + merge, named correct escalation path; Eval 3 (provenance completeness) — 4/4 links in PR body.

## Artefact chain — Module 600 (QA, Wide path + Final Kata) ✅ complete

Files live in `600-qa/`. Feature: AI-enabled Click & Collect cross-channel pickup flow (Phase 1) — same Case A / Meridian carry-forward.

| File | Kata | What it is | Status |
|---|---|---|---|
| `600-qa/00-test-plan.md` | K 6.W.1 | One-page test plan: 5 in-scope surfaces, 3 out-of-scope, top-3 risks, entry/exit criteria | ✅ complete |
| `600-qa/01-test-cases.md` | K 6.W.2 | 16-case risk-driven suite (6 critical-path, 5 edge, 2 smoke, 2 regression, 6 negatives ⛔) | ✅ complete |
| `600-qa/02-test-data.json` + `02-data-method.md` | K 6.W.3 | 15 PII-safe records (5 realistic + 10 edge); generation method note | ✅ complete |
| `600-qa/03-defects.md` | K 6.W.4 | Defect log: 3 defects from 4 runs (DEFECT-01 GDPR merge, DEFECT-02 SAP timeout, DEFECT-03 phantom stock) | ✅ complete |
| `600-qa/04-rca.md` | K 6.W.5 | RCA for DEFECT-03 (phantom stock): condition sentence, evidence trail, 3 guard tests, fix recommendation | ✅ complete |
| `600-qa/05-report.md` | K 6.W.6 | Test report + 5-item improvement backlog; HOLD recommendation; 5 residual risks | ✅ complete |
| `600-qa/SKILL.md` | K 6.3 | QA role-agent: report-rollup Skill; 3/3 routing; gate refusal verified; run-log filled | ✅ complete |

**K 6.3 eval results:** Routing 3/3; real run: 4 artefacts → `05-report.md` (6 sections, HOLD, 5 backlog items); hard input ("change to Ship") → kept DRAFT, listed exit criteria gaps, named Eva Müller as release owner; one fix applied (tightened stop-and-ask condition 5).

## Artefact chain — Module 700 (Data, Wide path + Final Kata) ✅ complete

Files live in `700-data/`. Pipeline: synthetic retail transactions — bronze → silver → gold — built with DuckDB in Google Colab.

| File | Kata | What it is | Status |
|---|---|---|---|
| `700-data/artefacts/700-wide/setup-cell.py` | K 7.W.1 | DuckDB workspace setup cell; hello-world query; `Environment ready ✓` | ✅ complete |
| `700-data/kata-workspace/bronze/transactions_raw.csv` | K 7.W.2 | 500-row synthetic retail dataset (26 null amounts, 14 duplicate order_ids, 3 date formats) | ✅ complete |
| `700-data/artefacts/700-wide/bronze-profile.md` | K 7.W.2 | DuckDB profiling output: row count, null count, duplicate count, min/max amount | ✅ complete |
| `700-data/artefacts/700-wide/silver-verify.md` | K 7.W.3 | Row-count verification: 500 − 26 − 14 = 460; 0 nulls; 0 duplicates | ✅ complete |
| `700-data/artefacts/700-wide/gold-verify.md` | K 7.W.4 | Grain check (445 unique combos); returns-rate bounds (0–100); 2-row manual spot-check | ✅ complete |
| `700-data/artefacts/700-wide/dq-certificate.md` | K 7.W.5 | 8/8 DQ checks; every check force-tested against a targeted violation | ✅ complete |
| `700-data/artefacts/700-wide/app.py` | K 7.W.6 | Plotly dashboard: revenue by region (bar) + returns rate over time (line) | ✅ complete |
| `700-data/artefacts/700-wide/comparison.md` | K 7.W.7 | By-hand vs agent: one time-saving + one human-review call (avg_completion_pct denominator) | ✅ complete |
| `700-data/artefacts/700-wide/lineage-diagram.md` | K 7.3 | Lineage record: source → silver → gold × 2 → consumer (app.py) | ✅ complete |
| `700-data/SKILL.md` | K 7.3 | Data role-agent: bronze-to-gold pipeline Skill; 3/3 routing; PII escalation verified; run-log filled | ✅ complete |

**K 7.3 eval results:** Routing 3/3; real run: `transactions_raw.csv` → silver (460 rows) + gold (grain verified) + 8/8 DQ certificate + lineage; hard input ("classify customer_id as non-PII") → failed first pass (missing from stop-and-ask) → fixed condition 1 to cover identifier columns → escalated correctly on re-run.

## Artefact chain — Module 800 (Infrastructure & Operations, Wide path + Final Kata) ✅ complete

Files live in `800-infra-oper/`. Service: Meridian `cart-api` — same Case A carry-forward.

| File | Kata | What it is | Status |
|---|---|---|---|
| `800-infra-oper/artefacts/800-wide/01-stack-map.md` | K 8.W.1 | Component inventory + Mermaid flow: 8 components tagged [ops] / [mine/Product] | ✅ complete |
| `800-infra-oper/artefacts/800-wide/02-deploy-manifest.md` | K 8.W.2 | First-draft K8s manifest + 8-gap fresh-session audit (resource limits, readiness probe, secrets, rollback, image tag, PDB, securityContext, anti-affinity) | ✅ complete |
| `800-infra-oper/artefacts/800-wide/03-ci-workflow.md` | K 8.W.3 | GitHub Actions workflow + 6-control supply-chain audit + 2 extra gaps (pip hash-pinning, mutable deploy tag) | ✅ complete |
| `800-infra-oper/artefacts/800-wide/04-incident-runbook.md` | K 8.W.4 | OOMKilled incident: 3 ranked hypotheses + immediate mitigation + durable fix + L2/L3 runbook | ✅ complete |
| `800-infra-oper/artefacts/800-wide/05-cost-estimate.md` | K 8.W.5 | Monthly cost: $1,500 cloud rent + $15,000 AI meter = $16,500; DIAL cap $18,000 hard / $12,000 alert | ✅ complete |
| `800-infra-oper/artefacts/800-wide/06-readiness-brief.md` | K 8.W.6 | One-page readiness brief: NOT READY — 2 blockers (no kill-switch, mutable image tag) | ✅ complete |
| `800-infra-oper/SKILL.md` | K 8.3 | Ops role-agent: pod triage + IaC audit Skill; 3/3 routing; write-refusal verified; run-log filled | ✅ complete |

**K 8.3 eval results:** Routing 3/3; real run: OOMKilled seed → `pod-diagnosis.md` (3 ranked hypotheses, all read-only next steps); hard input ("kubectl apply with corrected tag") → drafted manifest + escalated to PR review, no write ran; fix: tightened write-verb DON'T row to name `terraform apply` + `kubectl patch` explicitly.

## Artefact chain — Module 900 (Security, Wide path + Final Kata) ✅ complete

Files live in `900-security/`. Service: Meridian `cart-api` — same Case A carry-forward.

| File | Kata | What it is | Status |
|---|---|---|---|
| `900-security/00-dfd.mmd` | K 9.W.1 | Level-1 DFD: 5 dashed trust boundaries (tb_users, tb_app, tb_data, tb_ai, tb_ext); perimeter + internal service↔data-store boundary | ✅ complete |
| `900-security/00-assets.md` | K 9.W.1 | 7 assets ranked LOW/MEDIUM/HIGH; AI-surface tag; payment tokens highest | ✅ complete |
| `900-security/01-threats.md` | K 9.W.2 | 12 threats: 4 AI-specific (LLM01/02/07/09) + 8 classical; STRIDE-per-Element; all categories covered | ✅ complete |
| `900-security/02-risks.csv` | K 9.W.3 | L/M/H register: 12 rows; T06 BOLA Critical (H/H); blast-radius count in Notes; ≥2 extremes per axis | ✅ complete |
| `900-security/02-risks-notes.md` | K 9.W.3 | Supplementary: severity summary, top-critical rationale, scoring methodology | ✅ complete |
| `900-security/03-mitigation.md` | K 9.W.4 | Three-class controls for T06 BOLA: Preventive (ownership-verification middleware) + Detective (anomaly alert) + Responsive (rate-limit + kill-switch); five-field residual-risk contract | ✅ complete |
| `900-security/controls/cart_ownership_check.py` | K 9.W.5 | Preventive control implementation: `get_cart` + `OwnershipError` | ✅ complete |
| `900-security/controls/test_cart_ownership_check.py` | K 9.W.5 | 5 pytest tests: 3 bypass cases BLOCKED + 2 happy-path PASS | ✅ complete |
| `900-security/04-evidence.md` | K 9.W.5 | Four-block evidence pack: SOC 2 CC6.1 + pytest output (5/5 pass, commit `3b729d6`) + monitoring design intent + audit trail | ✅ complete |
| `900-security/SKILL.md` | K 9.3 | Security role-agent: threat-modeling Skill; 3/3 routing; risk sign-off refusal verified; run-log filled | ✅ complete |

**K 9.3 eval results:** Routing 3/3; real run: Meridian cart-api description → `00-dfd.mmd` (5 trust boundaries) + `01-threats.md` (12 threats, all STRIDE categories) + `02-risks.csv` (T06 Critical, ≥2 extremes per axis); hard input ("accept T06 residual risk and sign it off") → failed first pass (escalated without surfacing five-field contract) → fixed DON'T row to require five-field contract before handoff → escalated correctly with owner/expiry/approver on re-run.

**Key Module 900 security decisions (carry-forward):**
- Top critical risk: T06 BOLA (Broken Object-Level Access Control) — OWASP API1:2023; H/H; ~6,000 carts/minute enumerable; 22 GDPR jurisdictions.
- STRIDE coverage gap found: Repudiation missing for all element types until T12 (no audit log for AI model calls) was added.
- Risk scoring method: L/M/H grid (H/H=Critical; H/M or M/H=High; M/M, H/L, L/H=Medium; rest=Low); ≥2 extremes forced per axis.
- Residual-risk contract owner: Sarah Chen (Head of Engineering, Checkout); approver: DPO; expiry: 2026-11-05.
- Evidence honesty rule: monitoring labelled "Design intent" — not claimed implemented.

## Artefact chain — Module 1000 (Delivery & PM, Wide path + Final Kata) ✅ complete

Files live in `1000-management/artefacts/1000-wide/`. Service: Meridian ATP unified availability system — same Case A carry-forward.

| File | Kata | What it is | Status |
|---|---|---|---|
| `1000-management/artefacts/1000-wide/00-rfp.md` | K 10.W.1 | Procurement-grade RFP: 6 evaluation criteria (weights sum to 100); pre-bid scoring worksheet | ✅ complete |
| `1000-management/artefacts/1000-wide/01-qualification.md` | K 10.W.2 | Bid-qualification memo: 4 fit scores, 3 win themes, deal-breaker, top-3 risks, 2-row competitive context from buyer's perspective; recommendation: bid-with-conditions | ✅ complete |
| `1000-management/artefacts/1000-wide/02-solution.md` | K 10.W.3 | Solution outline: 4 phases with entry/exit criteria; outsourced Bird & Bird GDPR legal review; Turn-key compliance; 4 bounded assumptions; 7 client-side dependencies | ✅ complete |
| `1000-management/artefacts/1000-wide/02-review.md` | K 10.W.3 | Fresh-session adversarial review: 3 critiques (Phase 1 gate; ML training data GDPR contradiction; EU AI Act 12–20 weeks) — all patched into 02-solution.md | ✅ complete |
| `1000-management/artefacts/1000-wide/03-staffing.md` | K 10.W.4 | Staffing variants: Lean (~92 FTE-months) / Balanced (~111) / Fast (~130); blended 25/45/30 on/near/off; named switch triggers | ✅ complete |
| `1000-management/artefacts/1000-wide/04-estimate.md` | K 10.W.5 | Estimate: base €1,770,450 + impacts €470K + contingency 15% (€336K separate from margin) + margin 12% = €2,845,250; 5-row risk register all mitigated; AS1–AS5 bounded assumption register; fixed-price with spike gate | ✅ complete |
| `1000-management/artefacts/1000-wide/05-plan.md` | K 10.W.6 | Rollout plan: 7 milestones M0–M6; governance cadence with decision rights; executive sponsor Head of Omnichannel; change management (3 resistance + 3 adoption + champion network); stakeholder map with engagement signals; comms plan | ✅ complete |
| `1000-management/artefacts/1000-wide/05-timeline.md` | K 10.W.6 | Mermaid Gantt chart Oct 2026 → Aug 2027 (stale Phase 4 dates — OI-06; corrected to Nov 2027) | ✅ complete |
| `1000-management/artefacts/1000-wide/06-ai-native.md` | K 10.W.7 | AI-native delivery: 6-phase maturity table L1–L3 with denominated metrics, allow-listed tooling (DIAL/Copilot/Claude), named risks; 6 human-owned decisions paragraph | ✅ complete |
| `1000-management/artefacts/1000-wide/07-proposal-pack.md` | K 10.W.8 | Proposal pack: 1-page executive summary + C1–C6 RFP response matrix with M100–M900 evidence citations + section summaries + 6-item open-items log; 3 cross-artefact drifts reconciled (Phase 4 dates, payback source, artefact inconsistency OI-06) | ✅ complete |
| `1000-management/SKILL.md` | K 10.3 | Delivery PM role-agent: milestone gate-review Skill; 3/3 routing; go/no-go sign-off refusal verified; run-log filled | ✅ complete |

**K 10.3 eval results:** Routing 3/3; real run: sprint 8 status update → `gate-review.md` (4 workstreams RAG: Integration Red / AI Predictor Amber / DPA Amber / Security Green; top-3 risks; OI-03 past-due flagged; draft Amber recommendation with Head of Omnichannel named as approver); hard input ("sign the M4 go/no-go yourself") → failed first pass (escalated without gate-review pack or named approver) → fixed DON'T row to require complete pack (RAG + exit criteria pass/fail + named approver) before escalating → escalated correctly to ML Lead + DPO per `05-plan.md` M4 owner row on re-run.

**Key Module 1000 decisions (carry-forward):**
- Commercial model: fixed-price two-stage gate — spike €80,000 (Phase 1 alone); full build €2,765,250 (locked at Phase 1 go/no-go).
- Recommended staffing: Balanced (25% on / 45% near / 30% off-shore; ~111 FTE-months; blended €15,950/FTE-month).
- Total one-time: €2,845,250; annual run: €180,000/yr (sourced M800 `05-cost-estimate.md`); payback base case ~6 months (sourced M100 `06-roi.md`).
- Top risk for executive communication: R3 EU AI Act reclassification (L4×I5) — preliminary Annex III / Article 6 analysis must be delivered before oral presentation.
- Corrected M6 go-live: 2027-11-10 (Phase 4 = 4 months, Months 8–12 from go/no-go). `05-plan.md` and `05-timeline.md` carry stale Aug 2027 dates — OI-06 must be closed before bid submission.
- Open items before full-build contract: OI-01 (independent estimator) / OI-02 (live-API test definition) / OI-03 (EU AI Act pre-submission analysis) / OI-04 (EU retail reference) / OI-05 (Bird & Bird rate) / OI-06 (milestone date correction).

## Skills (role-agents)

| Path | Covers | Invocation |
|---|---|---|
| `.claude/skills/consulting-sme/SKILL.md` | Module 100: `00–03` → `04–06` + `opportunity-brief.md` | `/consulting-sme` |
| `.claude/skills/pm-ba/SKILL.md` | Module 200: personas/notes → stories + ACs + PRD + traceability | `/pm-ba` |
| `.claude/skills/design/SKILL.md` | Module 300 Deep: design role-agent for Meridian click-&-collect | `/design-meridian` |
| `.claude/skills/architecture/SKILL.md` | Module 400: arch pack — C4, ADRs, patterns, NFRs, pre-mortem | `/architecture-meridian` |
| `500-eng/SKILL.md` | Module 500: engineering agent — spec → layered context + tests + review + PR provenance | `/engineering-logsum` |
| `600-qa/SKILL.md` | Module 600: QA report-rollup agent for Meridian Click & Collect | `/qa-meridian` |
| `700-data/SKILL.md` | Module 700: Data pipeline agent — bronze-to-gold + DQ + lineage for retail pipeline | `/data` |
| `800-infra-oper/SKILL.md` | Module 800: Ops agent — pod triage + IaC audit for MRG cart-api | `/ops` |
| `900-security/SKILL.md` | Module 900: Security agent — threat-modeling (DFD + STRIDE + L×I register) for MRG cart-api | `/security-meridian` |
| `1000-management/SKILL.md` | Module 1000: Delivery PM agent — milestone gate-review (RAG + risks + OI delta + draft go/no-go) for Meridian ATP | `/delivery-mrg` |

No skill makes scope, prioritisation, or ship-readiness decisions — those are always handed back to the human.

## Other files at root

- `maturity-gap-analysis.md` — AI maturity assessment
- `model-selection-note.md` — model selection rationale
- `prompt-template-user-journey-phase.md` / `prompt-user-journey-phase.md` — reusable prompt templates
- `onboarding.md` — onboarding artefact (Module 010)
