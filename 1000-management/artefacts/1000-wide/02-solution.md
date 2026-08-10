---
kata: 10.W.3
consumes: 00-rfp.md, 01-qualification.md, M200-prd, M300-spec, M400-adr-001, M500-spec
date: 2026-08-10
version: 1.1 (patched after fresh-session review — see 02-review.md)
---

# Solution Outline — Meridian Unified ATP System

## 1. High-Level Approach

Build a unified Available-to-Promise (ATP) signal layer on top of Meridian's existing
SAP / Apollo Gateway / cart-api stack using an event-driven read model (Kafka + Redis,
per ADR-001). An AI confidence scorer combines five inventory signals to return a
three-tier plain-language verdict (Available / Low stock / Uncertain) at C&C checkout
— eliminating the binary SAP count that causes phantom-stock cancellations.

The engagement runs in four phases gated by explicit entry/exit criteria. Phase 1 is a
fixed-fee architecture spike; no full-build commitment is made until Phase 1 exits.
GDPR legal review across all 22 jurisdictions is outsourced to a specialist EU privacy
law firm; that outsourced workstream is governed by a named gate and a named escalation
path (see §4).

---

## 2. Phases

| Phase | Entry criterion | Exit criterion | Duration | Owner role |
|---|---|---|---|---|
| **1 — Architecture Spike** | Contract signed; MRG grants read access to 3 representative country inventory APIs | ADR published confirming 22-system integration is achievable ≤12 months and ≤€4.1M; GDPR data-flow map produced for ≥3 jurisdictions; go/no-go signed by MRG Head of Engineering | 4 weeks |Architecture Lead |
| **2 — Foundation & Integration** | Phase 1 go/no-go signed; SAP CDC or batch-export path confirmed; DPA addenda initiated for all 22 jurisdictions | Event-driven inventory layer live for all 22 country stacks; ATP signal provider passing integration tests; ≥18 of 22 DPA addenda signed and filed | Months 1–4 | Tech Lead + DPO (outsourced) |
| **3 — AI Predictor & Shopper UI** | Phase 2 exit confirmed; ≥2 of 5 signals fresh in staging; ML training dataset covers ≥90 days of historical SAP + POS data | AI confidence scorer at ≥90% precision on Available verdicts in UAT; three-tier verdict live in staging (web + app); store associate dashboard deployed to ≥3 pilot stores; EU AI Act risk classification filed | Months 4–8 | ML Lead + UX Lead |
| **4 — Hardening & Go-Live** | Phase 3 UAT signed off; EU AI Act sign-off received; fairness review completed; all 22 DPA addenda signed | Load test at 2× peak Black Friday RPS passed; security audit complete (BOLA + OWASP API Top 10); pilot rollout (3 countries) ≥2 weeks stable; each of the ≤4 unsigned-DPA countries has a named resolution (signed, excluded from go-live scope, or escalated to MRG General Counsel with documented risk acceptance); full 22-country go-live (or agreed reduced scope); runbooks handed over | Months 8–12 | Delivery Lead + MRG Ops |

---

## 3. Outsourced Capability — GDPR Legal Review (Bird & Bird LLP)

**Gap:** The delivery team does not hold EU privacy law expertise across 22 jurisdictions.
Cross-border stock data flows under GDPR require per-country Data Processing Agreements
(DPAs) and, in some jurisdictions, local data-residency confirmations. Getting this wrong
delays architecture decisions and creates regulatory liability.

**Outsource to:** Bird & Bird LLP (EU privacy practice) — engaged as a named sub-vendor
from Phase 1 through Phase 2 exit.

**Integration into delivery:**
- Phase 1: Bird & Bird produces a jurisdiction-by-jurisdiction data-flow map and flags
  which countries require DPA addenda before data can flow cross-border.
- Phase 2: Bird & Bird drafts and negotiates DPA addenda; Meridian's DPO countersigns.
  The Phase 2 exit criterion requires ≥18 of 22 addenda signed.
- Phase 3 onward: Bird & Bird on retainer for Article 13 (AI transparency) advisory only.

**Governance:**
- Bird & Bird delivers a signed jurisdiction map by end of week 2 (Phase 1).
- Gate: if Bird & Bird's map identifies ≥3 jurisdictions where cross-border flow cannot
  be made compliant within the 12-month envelope, the delivery lead escalates to MRG's
  General Counsel and the Head of Omnichannel within 48 hours — this is a project-level
  blocker, not a legal detail.
- **Escalation path (patched after review):** if a jurisdiction's DPA addendum is not
  signed by Phase 2 week 6, that country is excluded from the Phase 2 integration scope
  and flagged as a named open item in the Phase 2 exit report. MRG Head of Omnichannel
  decides whether to proceed to Phase 3 without that country or extend Phase 2.
  The delivery lead does not make this call unilaterally.

---

## 4. Key Assumptions

| # | Assumption | Bound |
|---|---|---|
| A1 | SAP ECC can be configured for CDC (Debezium) or batch export to Kafka in ≥3 representative stacks within Phase 1 | Confirmed or refuted at Phase 1 exit; if batch-only, 15–30 min structural staleness accepted in scope |
| A2 | MRG provides ≥90 days of historical SAP + POS data for ML training by Phase 3 start; training data from countries without a signed DPA addendum is excluded from the ML training set until the addendum is signed | Delivery lead flags at Phase 2 week 6 if data is not confirmed; model accuracy implications for excluded countries documented at Phase 3 kick-off; Phase 3 start date shifts if data is not met |
| A3 | Team utilisation reaches ≥70% by sprint 3 of each phase | Ramp profile modelled at 30/60/100% across months 1–3; if sprint 3 velocity is <70% of plan, resourcing reviewed |
| A4 | EU AI Act risk classification for the confidence scorer is **Limited Risk** (Article 52, transparency obligation) — preliminary Annex III / Article 6 analysis to be completed before proposal submission | Filed in Phase 3; if DPO or legal review reclassifies as High Risk (Annex III vectors: store associate operational use + consumer access to goods), Phase 4 adds a full conformity assessment — realistic timeline impact **12–20 weeks**, not 6; this is an existential Phase 4 schedule risk and must be resolved before full-build contract is signed |

---

## 5. Client-Side Dependencies

| Dependency | Owner at MRG | Required by |
|---|---|---|
| Read access to 3 representative country inventory APIs | Head of Engineering Checkout | Phase 1 day 1 |
| SAP CDC configuration or batch-export confirmation | SAP platform team | Phase 1 week 2 |
| OMS cancellation-rate data for baseline confirmation | Operations analytics | Phase 1 week 1 |
| DPO engagement and DPA negotiation authority | Meridian DPO | Phase 2 kick-off |
| ≥90 days historical SAP + POS data for ML training | Data engineering | Phase 2 week 10 |
| EU AI Act risk classification sign-off | DPO + legal | Phase 3 week 6 |
| Fairness review participation (store sample across revenue bands) | Store operations | Phase 3 week 8 |

---

## 6. Out of Scope

- Replacement of any country-level ERP or inventory system
- Automated cancellation, re-routing, or stock-allocation decisions
- Loyalty, personalisation, or marketing features
- Warehouse management or supply chain optimisation
- Native mobile app development
- Countries not yet integrated into the Meridian SAP landscape

---

## 7. Compliance Shape

**Turn-key (EPAM-delivered solution).**

MRG's 22-country stock data contains cross-border personal-data flows that trigger GDPR
Article 44+ obligations. The engagement will use EPAM pre-approved AI tools (DIAL,
GitHub Copilot) plus any tools cleared by the EPAM Data Classification Matrix. PII and
commercially sensitive stock data trigger a compliance assessment and DPO sign-off before
any AI tool processes them. Bird & Bird's DPA work operates on anonymised data schemas
only until addenda are signed.
