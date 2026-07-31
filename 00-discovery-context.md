# 00 — Discovery Context: Meridian Retail Group
**Kata:** K 4.W.1 | **Source:** Case A reference brief

---

## Business layer

- **Revenue & scale:** $8.2B annual revenue; 31% digital share growing 18% YoY — digital is the primary growth vector for the next 3 years.
- **Program driver:** Board-approved $42M / 18-month consolidation of 22 country stacks acquired over years; quarterly stage gates with board visibility (Eva Müller). Failure to hit Phase 1 GA (month 8) risks program funding.
- **Success measure:** One customer identity + one cart + one loyalty program across all channels and 22 countries; live inventory view across channels; no store downtime during rollout.
- **Stakeholder pressure:** Regional GMs (Marco Rossi, Junichi Tanaka) will resist any rollout that drops local payment methods or imposes a Westernised UX; David Park will block any change that risks POS uptime during peak season. Both are veto-equivalent stakeholders.
- **Three SI partners** involved (including the delivery firm); internal MRG product team is junior and learning the platform alongside delivery — knowledge transfer is an explicit delivery constraint, not an afterthought.

## Product layer

- **Customer-facing surfaces:** 22 country web storefronts (Next.js target), 12 mobile apps (React Native target), 1,400 in-store POS systems.
- **Phase 1 scope:** Unified identity + cart + checkout. Phase 2 (month 8): loyalty + cross-channel inventory. Phase 3 (month 14): ML personalisation + marketing automation.
- **Critical user moments:** (1) Customer creates account on web, uses it in-store — currently broken (staff retype emails into POS). (2) Click-and-collect — currently ~7% cancellation rate at pickup due to phantom stock. (3) Cross-region loyalty — customers hold 3–4 fragmented accounts with non-transferable points.
- **Mobile reliability gap:** Black Friday 2024 — 40-minute EU outage. Phase 1 must not repeat this.
- **Regional release cadences diverge:** Italy weekly, Japan monthly, US bi-weekly — any shared infrastructure change must tolerate these cadences without forcing a lockstep release.

## Engineering layer

- **Target stack (chosen):** commercetools (headless), Apollo GraphQL gateway, AWS EKS microservices, Kafka eventing, Auth0 identity, Next.js web, React Native mobile, Segment CDP, Snowflake + dbt analytics.
- **Legacy coexistence (hard constraints):** SAP ECC remains inventory and finance ground truth — read-only sync to platform; it is not being migrated. Six regional CRMs (Salesforce, HubSpot, Dynamics mix) stay in place throughout the program.
- **Cutover pattern:** Strangler-fig mandated by CTO — no rip-and-replace; new platform routes traffic progressively per region. No acceptable downtime window.
- **Team structure:** ~80 people; one-third of squad engineers are mid or junior level; architecture team is 1 lead + 3. Mixed SI and MRG staffing. Operational complexity must stay within what the junior internal team can own post-handover.
- **Legacy variance:** Per-region stacks vary (Shopify Plus, custom .NET, Magento 2, on-prem Oracle); there is no single legacy-side interface to strangle against — each regional cutover is a distinct migration.

## Regulatory layer

- **GDPR (EU):** All EU customer data must stay within approved borders; consent management required; cross-border data flows need legal basis. Architectural implication: EU data residency controls on the platform's data layer; no EU PII routed through US-only services without a transfer mechanism.
- **CCPA (California):** Opt-out rights for CA residents; data deletion pipeline required. Implication: per-region data-deletion hooks in the identity and cart services.
- **PCI-DSS Level 1:** Highest card-data compliance tier. Implication: strict trust boundary around the checkout and payment containers; no card data outside the PCI scope; network segmentation; annual QSA audit.
- **PSD2 SCA (EU):** Strong Customer Authentication required on every EU card payment. Implication: a synchronous SCA challenge round-trip (typically 500–1500ms) is embedded in every EU checkout flow — it cannot be removed and sets the floor on EU checkout latency.
- **Local payment methods:** Postepay / Satispay (Italy), PayPay (Japan), Klarna (Nordics). Implication: checkout service must support per-region payment-method routing; a payment provider outage in one region must not cascade to others — bulkhead isolation is required.

---

## Five implicit assumptions the brief never states

1. **SAP ECC can serve near-real-time inventory reads.**
   > *Brief hint:* "SAP ECC for inventory ground truth" + "live inventory view across channels."
   > *Assumption:* The platform assumes SAP can feed inventory updates fast enough to support a near-real-time cache. In practice, SAP ECC batch jobs typically run on 15–30-minute cycles. If the cache is hydrated from batch exports, "live inventory" is a misnomer — it is stale-by-design, which directly affects the phantom-stock cancellation problem.
   > *What breaks if wrong:* The inventory cache delivers false confidence; click-and-collect cancellation rate does not meaningfully improve.

2. **The strangler-fig boundary is a single, well-defined routing layer.**
   > *Brief hint:* "Strangler-fig pattern mandated by CTO — no rip-and-replace."
   > *Assumption:* The brief implies a clean proxy or gateway routes requests to old vs. new platform. In practice, with 22 different legacy stacks (Shopify, .NET monoliths, Magento), there is no single facade — each regional cutover requires its own routing strategy. The Apollo Gateway may need per-region routing logic that accumulates technical debt as regions migrate at different paces.
   > *What breaks if wrong:* The "strangler" becomes a bloated multi-region routing monolith before the last region migrates.

3. **Auth0 can handle POS authentication at POS transaction throughput.**
   > *Brief hint:* "Auth0 for identity" + "stores must keep selling" + "1,400 stores."
   > *Assumption:* Auth0 is positioned as the identity provider for both web/mobile and in-store POS. POS authentication patterns (clerk login, customer loyalty lookup) differ significantly from browser-based OAuth flows. Auth0's SLA and rate limits at 1,400 stores × concurrent transactions during peak have not been stated.
   > *What breaks if wrong:* POS authentication becomes a single point of failure during peak; David Park's "stores keep selling" constraint fails.

4. **The three SI partners will not create integration conflicts on shared platform components.**
   > *Brief hint:* "Three SI partners involved" + "six product squads" + "one architecture team."
   > *Assumption:* The brief treats the three SIs as a coordinated delivery team with clear ownership boundaries. In practice, three SIs working on shared services (cart, identity, checkout) without explicit API contracts and versioning discipline will create integration conflicts. The brief names no ownership matrix.
   > *What breaks if wrong:* Shared services (Apollo Gateway, Cart Service) become integration conflict zones; Phase 1 GA slips.

5. **The internal MRG product team can operate the platform independently after SI handover.**
   > *Brief hint:* "Internal MRG product team is junior and learning the platform alongside delivery" + Lena Park "cares about runnable artefacts she can operate without the SI team."
   > *Assumption:* The brief implies a smooth knowledge transfer. But the platform (commercetools, Kafka, Auth0, EKS) is a high-complexity stack. A junior internal team absorbing it in 18 months while also delivering Phase 1–3 is an optimistic assumption. Operational complexity of the architecture is a first-class constraint — not a training problem.
   > *What breaks if wrong:* Post-handover operational incidents, unmitigated incidents, and cost overruns as MRG re-engages SI support.
