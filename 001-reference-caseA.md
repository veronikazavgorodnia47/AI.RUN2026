---
type: reference-cases
created: 2026-05-22
tags: [reference-cases]
status: draft
title: Reference Cases
description:
- Case A: Omnichannel Commerce Platform for a Global Retailer. Meridian Retail Group unifies 22 regional e-commerce stacks into one headless platform—shared identity, cart, loyalty, and cross-channel inventory across 1,400 stores—over 18 months ($42M), strangler cutover only, no acceptable downtime.
---

## Case A — Omnichannel Commerce Platform for a Global Retailer

> **Meridian Retail Group is unifying 22 country sites, 12 mobile apps, and 1,400 in-store POS systems into a single headless commerce platform with shared identity, cart, and loyalty — 18 months, $42M, no Big Bang cutover.**

### Client snapshot

| | |
|---|---|
| Name | Meridian Retail Group (MRG) |
| Industry | Multi-category retail — home goods, electronics, fashion |
| Footprint | 1,400 stores across 22 countries (EU, APAC, North America) |
| Headcount | 12,000 employees |
| Revenue | $8.2B annual |
| Digital share | 31% of revenue, growing 18% YoY |

### The project

MRG grew through acquisitions: each region runs its own e-commerce stack (some Shopify, some bespoke .NET), its own mobile app, and its own loyalty program. There is no unified customer identity, no shared inventory view between online and store, and no shared promotions engine. The board approved an 18-month program to consolidate onto a single headless commerce platform with one customer identity, one cart, one loyalty program, and a live inventory view across channels.

Discovery wrapped two months ago. Phase 1 (unified identity + cart + checkout) is being built now. Phase 2 (loyalty + cross-channel inventory) starts in month 8. Phase 3 (ML personalization, marketing automation) starts in month 14. There is no acceptable downtime window — stores must keep selling throughout.

### Constraints

- **Budget:** $42M over 18 months, with quarterly stage gates.
- **Timeline:** Phase 1 GA in month 8; full program complete in month 18.
- **Regulatory:** GDPR (EU), CCPA (California), PCI-DSS Level 1, PSD2 SCA for EU payments, local payment-method requirements (Postepay/Satispay in Italy, PayPay in Japan, Klarna across Nordics).
- **Technical:** Must coexist with legacy SAP ERP (inventory ground truth) and 6 regional CRMs that will not be migrated in this program. Strangler-fig pattern mandated by CTO — no rip-and-replace.
- **Organizational:** Three SI partners involved (the firm running this course is one). Internal MRG product team is junior and learning the platform alongside delivery.

### Stakeholders

| Name | Role | Wants | Worries about |
|------|------|-------|---------------|
| Eva Müller | VP Digital (sponsor) | Personalization, faster release cadence | Board update visibility, regional GM resistance |
| Tomás Reyes | Lead Architect | Clean strangler-fig, no vendor lock-in | Headless platform becoming the new monolith |
| Sarah Chen | Head of CX | One customer identity, one loyalty | In-store experience regression during rollout |
| David Park | Head of Retail Ops | Stores keep selling, POS doesn't break | Store staff retraining cost, peak-season risk |
| Marco Rossi | Regional GM, Italy | Local payments, local language nuance | Italian customers churning to local competitors |
| Junichi Tanaka | Regional GM, Japan | PayPay support, native mobile UX | Westernized UX being forced on JP customers |
| Asha Sundaram | Head of Privacy & Legal | GDPR/CCPA compliance baked in | Cross-border data flows, consent management |
| Lena Park | Internal Product Lead (MRG) | Team upskilling, knowledge transfer | Being left with a platform they can't operate |

### Team

~80 people across three SIs and MRG. Six product squads (8–10 people each), one BA cell (4 people), one QA chapter (2 leads + 8 engineers), one architecture team (1 lead + 3), two PMs, one delivery manager, three embedded designers. Mixed seniority — about a third of the squad engineers are mid-level or junior.

### Current pain points

- Customer creates an account on the web, can't use it in-store. Store staff manually retype emails into the POS to look up loyalty.
- Inventory shown online doesn't match what's in store. ~7% of "click & collect" orders are cancelled at pickup due to phantom stock.
- One customer can have 3–4 fragmented loyalty accounts across regions, with points not transferable.
- Mobile app crashes during peak — Black Friday 2024 had a 40-minute outage in the EU.
- Marketing can't run cross-channel campaigns; each region runs its own promotions, sometimes conflicting.
- Regions release at different cadences (Italy weekly, Japan monthly, US bi-weekly), making any shared change painful.

### Tech stack

- **Legacy (per region, varies):** Shopify Plus, custom .NET monoliths, Magento 2, on-prem Oracle DBs, SAP ECC for inventory and finance, region-specific CRMs (Salesforce, Hubspot, Dynamics).
- **Target platform:** commercetools (headless commerce), Apollo GraphQL gateway, microservices on AWS EKS, Kafka for eventing, React Native for mobile, Next.js for web, Auth0 for identity, Segment for CDP.
- **Data layer:** Snowflake for analytics, dbt for transformations, MRG keeps SAP as inventory ground truth (read-only sync to platform).

---


## Kata hooks per case

Each case below ends with a **Kata hooks** sub-section: a flat catalogue of role-specific tasks the case naturally surfaces. Kata authors pick from this catalogue when binding a series to the case. The hook list is suggestive, not exhaustive — add to it when a role module ships.

### Case A — Kata hooks (by role)

| Role | Kata hook |
|------|-----------|
| Consulting / SME | Score 10 candidate AI initiatives against Meridian's board-stage gates for value × feasibility |
| Consulting / SME | Draft the Meridian Constitution v0 (project context one-pager) from the discovery brief |
| PROD/BA | Write the Phase-1 PRD pack (problem, scope, anti-scope, success metrics, rollout) for unified cart |
| PROD/BA | Convert the eight stakeholder concerns into a prioritised risk register with mitigations |
| Design | Generate three accessible mobile-app flows for click-and-collect with Italian and Japanese local nuance |
| Design | Build a critique deck comparing the current EU app onboarding against a Lovable prototype |
| Architecture | Draft the headless-commerce C4 set (Context, Container, Component) for the cart microservice |
| Architecture | Write the ADR for the strangler-fig boundary between commercetools and the legacy Magento storefront |
| Engineering | (Owned by engineering team.) |
| QA | Author the end-to-end test plan for one-customer-identity rollout with cross-region session continuity |
| QA | Generate adversarial test cases for the GDPR consent layer using a fresh-session adversarial kata |
| Data | (Use Case C for data modules.) |
| Infra & Operations | Draft the AWS EKS multi-region SRE runbook for Phase-1 cart, including peak-season scale-out |
| Security | Build the PCI-DSS Level 1 evidence map for the new cart and identity service |
| Management | Generate the monthly board update from the program dashboard (RAG status, burn, top-3 risks) |

---

## Persona seeds

Every series binds to one or two **personas** — concrete people inside the case the learner is producing artefacts for. The personas below are seed identities; expand them in the module-level `0 — Role Context` section when needed.

### Case A — persona seeds

- **Eva Müller** (VP Digital, sponsor) — wants board-ready narratives every six weeks, no surprises. Reads a one-pager, asks two questions, decides. Allergic to jargon.
- **Tomás Reyes** (Lead Architect) — defends the strangler-fig boundary daily. Will read a 20-page ADR if it's clean. Hates re-litigation of settled decisions.
- **David Park** (Head of Retail Ops) — measures everything in store-uptime hours. Will flag any change that risks the POS. Trusts test plans more than promises.
- **Lena Park** (Internal Product Lead, MRG) — learning the platform alongside delivery. The post-SI handover lands on her. Cares about runnable artefacts she can operate without the SI team.

---

## Starter artefacts

Each case has a stub artefact pack at [`../resources/reference-case-artefacts/`](../resources/reference-case-artefacts/) covering the inputs a kata might ask the learner to consume (transcripts, screenshots, sample CSVs, sample emails). The packs are AI-synthesised seeds; upgrade them with real recordings once Illia signs off on the seed quality.

---