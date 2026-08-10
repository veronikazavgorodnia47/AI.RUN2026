---
kata: 10.W.6
consumes: 02-solution.md, 03-staffing.md, M600-test-report, M800-runbooks, M900-evidence
date: 2026-08-10
---

# Implementation & Rollout Plan — Meridian Unified ATP System

## 1. Milestones

| Milestone | Date | Entry criterion | Exit criterion | Owner |
|---|---|---|---|---|
| M0 — Contract signed | 2026-10-10 | RFP award confirmed | Signed MSA + DPA framework in place | Head of Omnichannel + Delivery Lead |
| M1 — Phase 1 spike complete | 2026-11-07 | MRG grants API access to 3 country stacks; OMS data delivered | ADR published; integration feasibility confirmed ≤12m/≤€4.1M; GDPR data-flow map produced for ≥3 jurisdictions | Architecture Lead |
| M2 — Phase 1 go/no-go signed | 2026-11-10 | ADR independently reviewed | Go/no-go signed by MRG Head of Engineering + Delivery Lead; full-build contract locked | Head of Engineering + Delivery Lead |
| M3 — Phase 2 complete | 2027-03-10 | Go/no-go signed; Bird & Bird DPA work initiated | 22-country event-driven integration live; ATP signal provider green in staging; ≥18/22 DPA addenda signed | Tech Lead |
| M4 — Phase 3 complete | 2027-07-10 | Phase 2 exit confirmed; ML training data covers ≥90 days | AI confidence scorer ≥90% precision on Available verdicts in UAT; three-tier verdict live in staging; EU AI Act classification filed | ML Lead + DPO |
| M5 — Pilot rollout stable | 2027-08-01 | Phase 3 UAT signed; fairness review complete; security audit passed | 3-country pilot live ≥2 weeks with zero P1 defects open (per M600 exit criteria: zero phantom-stock cancellations on SAP inventory check) | Delivery Lead |
| M6 — Full go-live | 2027-08-10 | Pilot stable; all 22 DPA countries resolved (signed / excluded / risk-accepted) | Full 22-country rollout complete; runbooks handed to Lena Park's ops team; DIAL cost cap active | Delivery Lead + MRG Ops |

---

## 2. Governance Cadence

| Ceremony | Frequency | Attendees | Decision rights | Executive sponsor |
|---|---|---|---|---|
| Steering committee | Monthly | Head of Omnichannel, Head of Engineering Checkout, DPO, Delivery Lead, Architecture Lead | Scope changes; budget overruns >5%; go/no-go at phase gates; escalated risks (R3 EU AI Act, R1 integration scope) | **Head of Omnichannel** — written authority to unblock policy, budget, or cross-team escalation |
| Sprint review | Biweekly | Tech lead, BA, QA lead, MRG product owner | Story acceptance; defect priority; integration test sign-off | — |
| Retrospective | Biweekly | Full delivery team | Team-internal; no client decisions | — |
| Phase gate review | At each milestone | Steering committee + Bird & Bird (DPA milestone) | Phase go/no-go; contract stage unlock | Head of Omnichannel |

**Retrospective standard (L3):** every retro produces ≥1 version-controlled artefact (improvement backlog item committed to the repo). A retro that produces only a discussion is not a retro at L3.

---

## 3. Change-Management Plan

### 3.1 Resistance handling

| Resistance scenario | Who | Response pattern |
|---|---|---|
| Store associates: "Another system that will show wrong stock — we already know it doesn't work" | David Park's store ops team, Italy + DE pilots | Show the three-tier verdict design in a 30-min demo before pilot launch. Degrade intentionally in the demo to show the "Uncertain" state — proving the system admits uncertainty rather than bluffing. Let associates experience the fallback before go-live. |
| MRG DPO: "The EU AI Act exposure is too high to proceed until we see the full conformity assessment" | DPO (escalation role on R3) | Deliver the preliminary Annex III / Article 6 analysis before the oral presentation. Present the "Limited Risk" rationale with sourced Article 6 checklist. Agree a trigger condition: if DPO reclassifies after review, Phase 3 scope adds conformity assessment — with the 12–20 week impact named explicitly, not minimised. |
| SAP platform team: "We don't have bandwidth to support a CDC configuration in Phase 1" | MRG SAP team | Name the dependency at M0 contract sign. Agree a named SAP contact and a 3-day SLA for API access questions. If CDC is blocked, document batch-export fallback in Phase 1 ADR — do not wait until Phase 2 to discover the constraint. |

### 3.2 Adoption tracking

| Behaviour | Signal | Measurement |
|---|---|---|
| Store associates actively using the at-risk dashboard (not ignoring it) | ≥60% of pilot stores log at least 1 dashboard interaction per trading day by week 3 of pilot | Dashboard session log (M800 gateway event, per-store tenant) |
| Shoppers acting on Uncertain verdict (tapping alternative store) | ≥20% of Uncertain verdict sessions result in an alternative-store tap within 60 seconds | Shopper event log (session-level, anonymised) |
| Delivery team using AI tooling (not just licenced) | ≥75% daily active AI usage across delivery team by sprint 4 | DIAL usage telemetry (per-team tenant, sourced from M800 gateway logs) |

### 3.3 Champion network

| Champion | Role | Protected time | Responsibility |
|---|---|---|---|
| 1 per pilot region (IT, DE, FR — 3 total) | Store operations lead in each market | 20% during Phase 4 pilot | First contact for store-staff resistance; feeds usage data back to delivery team; owns local onboarding session |
| 1 AI tooling champion | Senior engineer on delivery team | 10% ongoing | Owns DIAL / GitHub Copilot adoption; maintains prompt library in version control; runs monthly AI practice session |

---

## 4. Stakeholder Map

| Stakeholder | Interest | Influence | Key concerns | Engagement signal to monitor |
|---|---|---|---|---|
| Head of Omnichannel (MRG) | ATP system delivers ≥30% cancellation reduction; protects C&C revenue and repeat purchase rate | High | Budget ceiling (€4.1M); EU AI Act liability; timeline slippage vs. competitor pressure | Steering committee attendance rate; time to sign phase gate decisions (target ≤3 working days) |
| David Park — Store Operations Director (MRG) | Store staff trust the system; no increase in complaint calls from associates | Medium | False "Available" verdicts causing wasted customer trips; staff training burden | Champion network feedback; dashboard usage rate in pilot stores (see §3.2) |
| Meridian DPO (MRG) | GDPR compliance; EU AI Act classification resolved before go-live | High | Cross-border data flows; AI Act reclassification to High Risk; fairness review adequacy | DPA addendum sign-off pace; attendance at Phase 3 AI Act filing review |
| Delivery Lead (internal) | Successful on-time delivery; reference win in EU retail | High | R3 EU AI Act schedule risk; Bird & Bird DPA tail; Meridian SAP team bandwidth | Sprint velocity vs. plan; open P1 defect count at phase gate (target: zero at M5) |

*3–4 rows is the Wide scope. A real engagement maps 5–7+ stakeholders; scale up for the live engagement.*

---

## 5. Comms Plan

Cadence derived from the stakeholder map — not politeness. Two contrasting audiences from different map quadrants.

| Audience | What they receive | Channel | Cadence | Owner |
|---|---|---|---|---|
| **Head of Omnichannel** (high influence, high interest — steering quadrant) | One-page written status memo (RAG per workstream, top 2 risks, one decision required) delivered 48h before steering committee; verbal walkthrough at the meeting | Email + steering committee (video) | Monthly (memo) + monthly (meeting) | Delivery Lead |
| **David Park — Store Operations** (medium influence, high interest — operational quadrant) | Short operational update: what changes for store staff this sprint, any pilot dates to calendar, one action required (e.g. confirm champion names) | Teams channel (#meridian-pilot-ops) | Biweekly | Champion (IT region lead) |

*The two cadences differ: Head of Omnichannel receives monthly formal memos with decision items; Store Operations receives biweekly informal updates on operational impact. Same cadence for both would either under-serve the executive or overwhelm the operations team.*
