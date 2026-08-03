# 06 — NFR Budgets: Meridian Phase 1
**Kata:** K 4.W.7 | **Consumes:** 00-discovery-context.md, 04-adr-001/002/003.md

> 7 NFR budgets across 5 families. Each budget names its source constraint, its measurement method, and its owner. Machine-readable twin: `06-nfrs.yaml`.

---

## Summary table

| ID | Family | NFR | Target | Owner |
|---|---|---|---|---|
| NFR-01 | Latency | EU checkout end-to-end (incl. PSD2 SCA) | p95 < 3,000ms | Checkout engineering |
| NFR-02 | Latency | POS cart resolution — cache hit | p95 < 200ms | Platform engineering |
| NFR-03 | Reliability | Platform availability (web + mobile + POS) | 99.95% monthly | SRE / David Park |
| NFR-04 | Reliability | Inventory cache max staleness | 30 min under normal ops | Platform engineering |
| NFR-05 | Quality | Phantom stock cancellation rate | < 3% at 6 months post-GA | Product / Sarah Chen |
| NFR-06 | Cost | Infrastructure cost per checkout transaction | < €0.02 at peak load | Engineering / Eva Müller |
| NFR-07 | Security | PCI scope — card data containment | Zero card data outside PCI boundary | Security / Compliance |

---

## NFR-01 — EU Checkout Latency (Latency)

**Target:** p95 end-to-end checkout flow < 3,000ms for EU customers.

**Source constraint:** PSD2 Strong Customer Authentication is mandatory on every EU card transaction. The SCA challenge round-trip (bank redirect or in-app push) adds a synchronous 500–1,500ms floor that cannot be removed. Total checkout latency budget = platform processing + SCA. Non-EU flows have a tighter target of p95 < 1,500ms (no SCA floor).

**Measurement:** Synthetic canary transactions fired every 5 minutes from EU AWS regions (eu-west-1, eu-central-1). Real-user p95 sampled from Checkout Service traces in Datadog/Honeycomb. Breached if p95 > 3,000ms for two consecutive 5-minute windows.

**What breaks the budget:** Synchronous SAP reads on the checkout path (ADR-001 prohibits this). Shared payment adapter thread exhaustion without bulkhead isolation (ADR-003).

**Owner:** Checkout engineering; escalation to architecture lead.

---

## NFR-02 — POS Cart Resolution Latency (Latency)

**Target:** `resolveCustomerCart` query p95 < 200ms on cache hit; p95 < 1,000ms on SAP fallback (cache miss). Degraded-mode response (SAP unreachable) must always be < 200ms — never block on a down SAP.

**Source constraint:** Store associates scan customer QR codes at checkout with customers waiting. A response > 1 second on the cache-hit path is perceptible; a response > 3 seconds during a SAP outage is operationally unacceptable at 1,400 stores. (ADR-001, ADR-002.)

**Measurement:** POS client instruments the GraphQL round-trip via OpenTelemetry. p95 sampled per store cluster. Circuit breaker trip events on the SAP adapter are logged and alerted separately.

**What breaks the budget:** Auth0 token introspection latency spike on POS (assumption #3 from `00-discovery-context.md`). Apollo Gateway cold start on EKS pod scale-out during peak.

**Owner:** Platform engineering; David Park (POS/ops) as business stakeholder.

---

## NFR-03 — Platform Availability (Reliability)

**Target:** 99.95% monthly availability across web storefront, mobile app, and POS cart-bridge. Equates to < 22 minutes downtime per month (~66 minutes per quarter). Degraded-mode (availability data absent, checkout still functional) does not count as downtime.

**Source constraint:** Black Friday 2024 produced a 40-minute EU outage. David Park's "stores keep selling" constraint is a hard veto on any architecture choice that introduces a single point of failure across all POS terminals. (00-discovery-context.md — product layer.)

**Measurement:** Synthetic uptime probes (web checkout, mobile cart add, POS `resolveCustomerCart`) every 60 seconds from three AWS regions. Incident declared if two consecutive probes fail from two or more regions simultaneously. Monthly availability calculated as (total minutes - downtime minutes) / total minutes.

**What breaks the budget:** Apollo Gateway as a single EKS deployment without multi-AZ pod distribution. Auth0 rate-limit breach during POS peak login (assumption #3). SAP ECC outage propagating to POS without a degraded-mode fallback.

**Owner:** SRE team; David Park as business escalation.

---

## NFR-04 — Inventory Cache Staleness (Reliability)

**Target:** Inventory cache (`inventoryCache` Redis) maximum staleness of 30 minutes under normal SAP batch export operations. Staleness age must be surfaced to users via `sapSyncAgeMin` on every availability response — never hidden.

**Source constraint:** SAP ECC batch export cycles run every 15–30 minutes (assumption #1 from `00-discovery-context.md`). This is a structural floor — the platform cannot guarantee fresher data without a CDC path to SAP. The click-and-collect AI availability assistant (Phase 2) depends on this field to render the correct confidence state (`stale` threshold = 30 min per K 3.D.6 spec).

**Measurement:** Kafka consumer lag on the `StockUpdated` topic monitored in real time. Redis key TTL set to 1,800 seconds (30 min); a TTL expiry without a Kafka refresh triggers an alert. `sapSyncAgeMin` field in API responses is sampled and p95 staleness reported per SKU cluster.

**What breaks the budget:** Kafka consumer group falling behind (consumer lag > 5,000 messages). SAP batch export job failing silently without a dead-letter alert. Redis eviction under memory pressure expiring keys before Kafka refresh arrives.

**Redis sizing and eviction policy (added from adversarial pre-mortem S1-B3):** Redis ElastiCache cluster must be sized for the full active SKU working set across all 22 countries plus 30% headroom. Eviction policy must be set to `volatile-ttl` — evict only keys with a TTL, never bare inventory keys. A CloudWatch alarm on `evicted_keys > 0` must be active in staging before Black Friday load test. A team optimising for NFR-06 (cost) will under-provision Redis; sizing must be locked before the cost review, not after.

**Owner:** Platform engineering; escalation path to SAP/integration team for batch export failures.

---

## NFR-05 — Phantom Stock Cancellation Rate (Quality)

**Target:** Click-and-collect cancellation rate due to phantom stock < 3% at 6 months post-Phase 1 GA (down from current 7% baseline). Interim milestone: < 5% at 3 months post-GA.

**Source constraint:** 7% cancellation rate is named in the brief as a critical business failure mode — the primary product motivation for the AI availability assistant and the inventory cache architecture. A reduction to < 3% is the measurable outcome that justifies the Phase 2 investment. (00-discovery-context.md — product layer; opportunity-brief.md.)

**Measurement:** Order Management System cancellation reason codes tagged `STOCK_UNAVAILABLE_AT_PICKUP`. Calculated monthly as (STOCK_UNAVAILABLE_AT_PICKUP cancellations / total click-and-collect orders). Baseline established from SAP ECC historical data before Phase 1 GA.

**What breaks the budget:** Inventory cache staleness exceeding NFR-04 target (stale data produces false "Likely available" responses). Soft-hold logic not implemented (customers reserve items that are simultaneously reserved by in-store shoppers). Phase 2 AI availability assistant not shipped on time.

**Owner:** Product (Sarah Chen, Head of CX); architecture is an enabling constraint, not the owner of this outcome.

---

## NFR-06 — Infrastructure Cost per Checkout Transaction (Cost)

**Target:** < €0.02 per completed checkout transaction at peak load (8,000 RPS sustained for 2 hours — Black Friday simulation). Includes EKS compute, Kafka MSK, Redis ElastiCache, RDS PostgreSQL, and data transfer. Excludes payment provider fees (Stripe/Klarna pricing is pass-through).

**Source constraint:** $42M / 18-month program budget with quarterly stage gates (Eva Müller). Infrastructure cost at scale must not erode program margin. At 8,000 RPS, a €0.05/transaction cost would produce €400/second in infrastructure spend during peak — unsustainable. (00-discovery-context.md — business layer.)

**Measurement:** AWS Cost Explorer tagged per service. Load test at 8,000 RPS using k6 or Gatling; infrastructure cost during the 2-hour test window divided by completed transactions. Reported at each quarterly stage gate.

**What breaks the budget:** Over-provisioned EKS node groups left running after peak. Kafka retention set too high (TB-scale log accumulation). Redis cluster sized for peak without auto-scaling down. Uncompressed Snowflake event streams from Segment CDP.

**Owner:** Engineering leads; Eva Müller (board) as financial escalation.

---

## NFR-07 — PCI Scope and Data Residency (Security)

**Target (PCI):** Zero card data (PANs, CVVs, track data) outside the PCI-segmented checkout and payment containers. No card data in application logs, tracing spans, or analytics pipelines under any circumstances.

**Target (Data residency):** Zero EU customer PII routed through or persisted in AWS regions outside `eu-west-1` and `eu-central-1` without an approved GDPR transfer mechanism. CCPA deletion requests processed within 30 days via per-region deletion pipeline hooks in Identity Service and Cart Service.

**Source constraint:** PCI-DSS Level 1 (highest tier) — annual QSA audit. GDPR EU data residency requirement. CCPA opt-out and deletion rights for California residents. (00-discovery-context.md — regulatory layer.)

**Measurement:**
- PCI: automated secret-scanning and log-scanning pipeline (e.g., Nightfall or AWS Macie) runs on every deployment. QSA audit annually.
- GDPR/CCPA: deletion pipeline SLA tracked in incident management system. EU PII data flow map reviewed at each quarterly stage gate.

**What breaks the budget:** Checkout Service logging request payloads at DEBUG level (card data in logs). Segment CDP routing EU user events to a US-only endpoint without SCCs. Identity Service not implementing per-region deletion hooks before Phase 1 GA.

**Owner:** Security team + Legal/Compliance; architecture lead owns the trust boundary design.
