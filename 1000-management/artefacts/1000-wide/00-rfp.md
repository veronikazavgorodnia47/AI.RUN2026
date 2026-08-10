---
buyer: Meridian Retail Group
project: AI-Enabled Click-and-Collect Availability Predictor — Unified ATP Layer
date: 2026-08-10
version: 1.0
---

# Request for Proposal — Unified Available-to-Promise System

## 1. Buyer and Decision

**Buyer:** Meridian Retail Group (MRG) — mid-market EU omnichannel fashion retailer,
€1–5B revenue, operating across 22 countries in Western Europe.

**Issuing authority:** Head of Omnichannel / VP E-Commerce, Meridian Retail Group.

**Decision being made:** Select a delivery partner to design, build, and deploy a
unified **Available-to-Promise (ATP)** signal layer that integrates 22 country-level
inventory systems and surfaces an AI-powered availability prediction to shoppers at
click-and-collect (C&C) checkout — eliminating phantom-stock cancellations where a
customer arrives at a store to find their reserved item unavailable.

---

## 2. Objective

Reduce the Meridian click-and-collect cancellation rate caused by stock discrepancies
between country inventory systems by ≥30% within 12 months of go-live, recovering
annualised C&C order value and protecting repeat purchase rate across the EU store
network.

The partner is expected to:

- Integrate with ≥3 representative country inventory stacks in a 4-week architecture
  spike, then scale to all 22 in full build.
- Deliver an AI confidence predictor that surfaces differentiated availability signals
  ("confirmed" / "likely available" / "low confidence") — never a binary promise on
  sparse SKUs.
- Hand off a production-ready, GDPR-compliant system with documented runbooks,
  monitoring, and store-staff tooling.

---

## 3. Scope

### In scope

- Unified event-driven inventory integration layer (22 country systems via API
  abstraction)
- AI/ML availability predictor: training pipeline, confidence-interval output,
  model monitoring
- Shopper-facing availability indicator on C&C checkout (web and app)
- Store associate at-risk alert dashboard
- GDPR-compliant data pipeline and cross-border data flow architecture
- Integration with Meridian's existing SAP/OMS stack and Apollo Gateway (cart-api)
- Security controls including BOLA ownership-verification middleware and anomaly
  detection
- UAT support, load testing, and go-live handover

### Out of scope

- Replacement of any country-level inventory or ERP system
- Automated cancellation or re-routing logic (all fulfillment decisions remain with
  store staff)
- Loyalty or personalisation features
- Warehouse management or supply chain optimisation
- Mobile app native development (integration via existing web-view approach)

---

## 4. Constraints

| Constraint | Detail |
|---|---|
| Timeline | Architecture spike complete by 2026-10-10; full system go-live by 2027-08-10 (12 months) |
| Budget envelope | One-time cost ≤€4.1M; annual run ≤€500K (pessimistic ceiling from ROI brief) |
| Regulatory | GDPR compliance mandatory; cross-border stock data flows require per-jurisdiction legal review; EU AI Act risk classification required before launch |
| Data residency | Country-level stock data must not be stored outside the originating jurisdiction without explicit DPA addendum |
| Human oversight | No automated cancellation, re-routing, or stock-allocation decision at MVP stage; all fulfillment decisions remain with store staff |
| Fairness | Availability model must not systematically disadvantage smaller or lower-revenue stores; pre-launch fairness review required |
| Architecture spike gate | No go to full build without spike confirming 22-stack integration is achievable within timeline and cost envelope |
| AI tooling | Supplier must confirm all AI development tools against Meridian's Data Classification Matrix before kick-off; PII/PHI processing triggers DPO sign-off |

---

## 5. Evaluation Criteria

Proposals will be scored against the following weighted criteria. Weights sum to 100.
A proposal that does not address all six criteria will be disqualified.

| # | Criterion | Weight |
|---|---|---|
| C1 | **Solution fit and technical approach** — quality of the proposed architecture; evidence of integration experience with fragmented legacy stacks; phased approach with named entry/exit criteria | 30 |
| C2 | **Price and commercial terms** — total cost of ownership (one-time + 3-year run); commercial model fit (fixed / T&M / hybrid) | 25 |
| C3 | **Team, references, and delivery track record** — named team leads; ≥1 EU retail or omnichannel reference; demonstrable AI delivery experience | 20 |
| C4 | **AI governance and responsible AI** — model risk management, confidence-interval design, fairness approach, EU AI Act readiness | 10 |
| C5 | **Security and GDPR compliance** — documented BOLA/API security controls, GDPR data-pipeline design, DPO engagement plan | 10 |
| C6 | **Delivery risk management** — risk register quality; contingency named separately from margin; explicit no-go conditions | 5 |

**Scoring:** Each criterion scored 1–5 by a three-person evaluation panel (Head of
Omnichannel, Head of Engineering Checkout, DPO). Final score = Σ(weight × score).
Tie-breaker: C3 (references).

**Pre-bid scoring worksheet** — fill in column D before writing a word; max possible score = 500.

| Criterion | Weight (W) | Max score | Your self-score (1–5) | Weighted (W × score) |
|---|---|---|---|---|
| C1 Solution fit & technical approach | 30 | 150 | | |
| C2 Price and commercial terms | 25 | 125 | | |
| C3 Team, references & delivery track record | 20 | 100 | | |
| C4 AI governance & responsible AI | 10 | 50 | | |
| C5 Security & GDPR compliance | 10 | 50 | | |
| C6 Delivery risk management | 5 | 25 | | |
| **Total** | **100** | **500** | | |

*Rule of thumb: a self-scored weighted total below 300 signals a borderline bid — resolve the gaps or consider a no-bid.*

---

## 6. Timeline

| Milestone | Date |
|---|---|
| RFP issued | 2026-08-10 |
| Supplier briefing session (optional, virtual) | 2026-08-22 |
| Clarification questions deadline | 2026-08-29 |
| Meridian responses to clarifications | 2026-09-05 |
| Proposal submission deadline | 2026-09-19 |
| Shortlist notification (≤3 suppliers) | 2026-09-26 |
| Oral presentations / bid defence | 2026-10-03 |
| Contract award | 2026-10-10 |
| Architecture spike start | 2026-10-13 |
| Architecture spike gate review | 2026-11-07 |
| Full-build kick-off (conditional on spike gate) | 2026-11-10 |
| Target go-live | 2027-08-10 |

---

## 7. Submission Rules

**Format:** PDF or Markdown. Maximum **25 pages** (excluding appendices and CV packs).
Executive summary: 1 page maximum. Financial tables: submitted as a separate Excel
workbook, not embedded in the narrative.

**Required sections (proposals missing any section are disqualified):**

1. Executive summary (≤1 page): value proposition, commercial model, top risk
2. Solution outline: approach, phases with entry/exit criteria, outsourced capabilities
3. Staffing plan: named team lead, role × phase matrix, on/near/off-shore split
4. Estimate: effort, rate card, contingency as a separate line from margin
5. Risk register: top 5 risks, likelihood × impact, active mitigation per row
6. AI governance section: confidence-interval design, EU AI Act classification, fairness plan
7. References: ≥1 EU retail/omnichannel reference (name, contact, scope, outcome)

**Submission channel:** Secure upload to `rfp@meridianretailgroup.eu` with subject
line `RFP-2026-ATP — [Supplier Name]`. Hard copies not accepted.

**Disqualification conditions:**

- Submission received after 17:00 CET on 2026-09-19
- Missing any required section
- Financial tables embedded in the narrative (must be separate workbook)
- No named delivery lead in the staffing section
- Proposal exceeds 25-page limit (appendices excluded)

**Confidentiality:** This RFP and all Meridian-provided materials are confidential.
Suppliers must not disclose the existence of this procurement to third parties
without written consent from Meridian's Head of Procurement.
