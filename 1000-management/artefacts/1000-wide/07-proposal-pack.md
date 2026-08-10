---
kata: 10.W.8
consumes: 00-rfp.md, 01-qualification.md, 02-solution.md, 02-review.md, 03-staffing.md, 04-estimate.md, 05-plan.md, 06-ai-native.md, M100-M900 carry-forwards
date: 2026-08-10
version: 1.0 — reconciled; open items logged below
---

# Proposal Pack — Meridian Unified ATP System
## RFP-2026-ATP

---

## EXECUTIVE SUMMARY

Meridian Retail Group faces a single, well-defined problem: 22 country inventory systems
do not share a live view of stock, and shoppers arrive at stores for orders that cannot
be fulfilled. We propose an **AI-powered unified Available-to-Promise (ATP) layer** that
integrates all 22 systems via an event-driven architecture, surfaces a three-tier
confidence verdict (Available / Low stock / Uncertain) to shoppers at C&C checkout, and
eliminates the phantom-stock cancellations driving an estimated ≥7% order loss rate.

**Why we win:**
1. **Pre-built compliance and security baseline** — BOLA ownership-verification middleware,
   GDPR-compliant data pipeline design, and EU AI Act responsible-AI artefacts are already
   documented and tested; competitors start these from scratch.
2. **Auditable architecture-spike methodology** — our Phase 1 spike produces a C4-driven
   ADR with named entry/exit criteria that MRG can independently review before committing
   to the full build; no other bidder at this stage will offer a gated, verifiable scope
   commitment.
3. **AI-native delivery with measurable evidence** — per-phase L2–L3 maturity targets
   with denominated metrics and version-controlled artefacts, not "we'll use AI."

**Commercial model:** Fixed-price with a two-stage gate — fixed-fee spike (Phase 1,
€80,000) contracted alone; fixed-price full build (Phases 2–4, €2,765,250) locked only
after the spike ADR is independently reviewed and go/no-go is signed.

**Top risk and mitigation:** EU AI Act reclassification of the confidence scorer from
Limited Risk to High Risk (Annex III) — realistic timeline impact 12–20 weeks if it
occurs. Mitigation: preliminary Annex III / Article 6 analysis completed before this
oral presentation; finding shared with MRG DPO at M0 contract sign.

**Total one-time: €2,845,250 | Annual run: €180,000 | Payback (base case): ~6 months (sourced M100 `06-roi.md`)**

---

## 1. RFP Response Matrix

| Criterion | Weight | How we meet it | Evidence |
|---|---|---|---|
| C1 Solution fit & technical approach | 30 | 4-phase solution with named entry/exit criteria; event-driven architecture (Kafka + Redis, ADR-001) proven on Meridian's existing stack; 22-country API abstraction via Phase 1 spike before full-build commitment | `02-solution.md` §2 phases; M400 `04-adr-001.md`; M400 `02-containers.mmd` |
| C2 Price & commercial terms | 25 | Fixed-price €2,845,250 one-time, within M100 base-case envelope (€2.85M); two-stage gate protects MRG from full commitment before scope is confirmed; contingency (15%) held separate from margin (12%) | `04-estimate.md` §6 price summary; `00-rfp.md` constraint table |
| C3 Team, references & delivery track record | 20 | Named Architecture Lead (Phase 1) and Delivery Lead (full engagement); ≥1 EU omnichannel reference — **open item OI-04** (see §5) | `03-staffing.md` Tab 2 Balanced; `01-qualification.md` §2 win themes |
| C4 AI governance & responsible AI | 10 | Three-tier confidence verdict design (Available / Low stock / Uncertain) with degraded mode; preliminary EU AI Act Annex III analysis before bid defence; per-phase L1–L3 maturity targets; 6 named human-owned decisions | `06-ai-native.md`; M200 `01-vision.md`; M200 `06-prd.md` Decision Memory DM-200-001 |
| C5 Security & GDPR compliance | 10 | BOLA ownership-verification middleware (5/5 pytest tests, M900 commit 3b729d6); GDPR data-pipeline with Bird & Bird LLP legal review across 22 jurisdictions; DPO engaged from kick-off; SOC 2 CC6.1 control documented | M900 `04-evidence.md`; M900 `controls/cart_ownership_check.py`; `02-solution.md` §3 |
| C6 Delivery risk management | 5 | 5-row risk register with active mitigations; contingency sized bottom-up from register (15% = €336K); bounded assumption register (AS1–AS5); no unmitigated rows | `04-estimate.md` §3 risk register; `04-estimate.md` §7 assumptions |

---

## 2. Solution (summary — full detail in `02-solution.md`)

Four phases with contractual gates:

| Phase | Duration | Exit criterion |
|---|---|---|
| 1 — Architecture Spike | 4 weeks | ADR confirming ≤12m/≤€4.1M; GDPR data-flow map ≥3 jurisdictions; independent estimator review of ADR (OI-01) |
| 2 — Foundation & Integration | Months 1–4 | 22-country event-driven integration live in staging; ≥18/22 DPA addenda signed; integration tests against live country APIs (OI-02) |
| 3 — AI Predictor & Shopper UI | Months 4–8 | Confidence scorer ≥90% precision on Available verdicts in UAT; EU AI Act classification filed; fairness review complete |
| 4 — Hardening & Go-Live | Months 8–12 | Load test 2× peak RPS passed; 3-country pilot ≥2 weeks stable; all 22 DPA countries resolved; full go-live |

Outsourced capability: GDPR legal review (Bird & Bird LLP) — jurisdiction map by Phase 1
week 2; DPA negotiations through Phase 2 exit; retainer for Article 13 advisory in Phase 3.
Compliance shape: **Turn-key** (EPAM pre-approved tools + EPAM Data Classification Matrix;
PII/PHI triggers compliance assessment + DPO sign-off).

---

## 3. Staffing (summary — full detail in `03-staffing.md`)

**Recommended variant: Balanced** — 25% on / 45% near / 30% off-shore; ~111 FTE-months;
blended rate €15,950/FTE-month.

| Variant | FTE-months | On/near/off | Go-live vs plan | Key risk |
|---|---|---|---|---|
| Lean | ~92 | 15/25/60 | +4 weeks | Integration quality, coordination latency |
| **Balanced (recommended)** | **~111** | **25/45/30** | **On plan** | **Phase 3–4 DPA tail** |
| Fast | ~130 | 45/35/20 | −3–4 weeks | Parallel workstream merge, senior burn rate |

Switch trigger: Balanced → Fast if Phase 1 spike confirms <5 distinct API patterns or hard
go-live deadline confirmed. Balanced → Lean if spike revised cost estimate exceeds €3.5M.

---

## 4. Estimate (summary — full detail in `04-estimate.md`)

*Reconciliation note: Phase 1 spike base effort in the estimate table is €31,900
(2 FTE-months × blended rate). The commercial section prices the spike at €80,000
all-in, which includes delivery overhead, partial Bird & Bird Phase 1 engagement
(~€20,000), contingency, and margin on the spike phase. No contradiction — the table
shows base effort only; the commercial recommendation shows the all-in fixed fee.*

| Line | Amount |
|---|---|
| Base effort (~111 FTE-months, Balanced) | €1,770,450 |
| Delivery impacts (ramp + dependency wait + Bird & Bird + AI tooling) | €470,000 |
| Adjusted base | €2,240,450 |
| Contingency (15%, sized from risk register) | €336,000 |
| Margin (12%) | €268,800 |
| **One-time total** | **€2,845,250** |
| Annual run cost (sourced M800) | €180,000/yr |

Commercial model: **fixed-price with spike gate** — spike contracted alone (€80,000);
full build (€2,765,250) locked at Phase 1 go/no-go.

---

## 5. Plan (summary — full detail in `05-plan.md` + `05-timeline.md`)

Milestones: M0 contract (2026-10-10) → M1 spike complete (2026-11-07) → M2 go/no-go
(2026-11-10) → M3 integration complete (2027-03-10) → M4 predictor UAT (2027-07-10)
→ M5 pilot stable (2027-10-25) → M6 full go-live (2027-11-10).

*Timeline reconciliation: Phase 4 (Hardening & Go-Live) is a 4-month phase per the
estimate (31 FTE-months, months 8–12 from go/no-go). Phase 4 start = 2027-07-10; Phase 4
end = 2027-11-10. Prior artefacts 05-plan.md and 05-timeline.md carry stale dates
(M5 2027-08-01, M6 2027-08-10) that compress Phase 4 to 1 month — see OI-06.*

Governance: monthly steering committee (Head of Omnichannel as executive sponsor with
written unblock authority), biweekly sprint review, biweekly retro (≥1 version-controlled
artefact per retro).

Change management: resistance handling (store staff, DPO, SAP team), adoption tracking
(dashboard usage, shopper Uncertain-verdict tap rate, DIAL daily active use), champion
network (3 regional champions + 1 AI tooling champion, 10–20% protected time).

---

## 6. AI-Native Delivery (summary — full detail in `06-ai-native.md`)

| Phase | Target | By | Metric |
|---|---|---|---|
| Intake | L2 | Month 3 | ≥70% of GNG memos AI-drafted + reviewed (denominator: all GNG-submitted opportunities) |
| Plan | L2 | Month 6 | ≥75% of stories with AI-drafted ACs reviewed by BA (denominator: all sprint backlog stories) |
| Build | L2→L3 | L3 by month 9 | ≥80% of PRs with AI first-pass review (denominator: all merged PRs on integration + ML branches) |
| Validate | L2 | Month 9 | ≥80% of test cases AI-drafted first version (denominator: all test cases in sprint test plan) |
| Handoff | L2 | Month 12 | ≥90% of runbook sections AI-drafted + ops-lead reviewed (denominator: all handover pack sections) |
| Learn | L3 | Month 9 | 100% of retros produce ≥1 committed artefact (denominator: all retros from month 3) |

Human-owned (never automated): scope changes, phase gate go/no-go, EU AI Act
sign-off, ship-readiness call, performance conversations, client escalations.

---

## 7. Open-Items Log

Items unresolved going into bid defence. Each must be closed before full-build contract.

| ID | Item | Owner | Target close |
|---|---|---|---|
| OI-01 | Phase 1 exit ADR requires independent cost-estimator review — mechanism not yet defined. MRG must name the independent reviewer (internal SME or third party) before M2 go/no-go is signed. | MRG Head of Engineering + Delivery Lead | Before Phase 1 kick-off (2026-10-13) |
| OI-02 | Phase 2 integration test definition: "passing integration tests" at Phase 2 exit must be defined against live country API endpoints, not mocks. Test-definition document to be produced at Phase 1 exit. | Tech Lead | Phase 1 exit (2026-11-07) |
| OI-03 | EU AI Act preliminary Annex III / Article 6 analysis — to be completed and shared with MRG DPO before oral presentation (2026-10-03). If DPO reclassifies scorer as High Risk, Phase 3 scope and timeline are renegotiated before full-build contract is signed. | Delivery Lead + DPO | Before oral presentation (2026-10-03) |
| OI-04 | Named EU retail / omnichannel reference (required by C3, weight 20) — reference customer name, contact, scope, and outcome to be provided before proposal submission. Without a named reference this criterion scores below competitors who supply one. | Delivery Lead | Proposal submission (2026-09-19) |
| OI-05 | DPA 4-country tail costing — Bird & Bird late-completion retainer for the ≤4 unsigned-DPA countries is a named line item in `04-estimate.md` but the per-country rate has not been confirmed with Bird & Bird. Confirm before proposal submission. | Delivery Lead + Bird & Bird | Proposal submission (2026-09-19) |
| OI-06 | **Milestone date drift in prior artefacts** — `05-plan.md` and `05-timeline.md` show Phase 4 ending August 2027 (M5 2027-08-01, M6 2027-08-10) but Phase 4 is a 4-month phase (months 8–12 from go/no-go, 2027-07-10 → 2027-11-10 per `04-estimate.md`). Both artefacts must be corrected before bid submission; the Gantt chart in `05-timeline.md` must also be re-rendered. Corrected dates: M5 pilot stable 2027-10-25, M6 full go-live 2027-11-10. | Delivery Lead | Proposal submission (2026-09-19) |
