# 05 — Placed Pattern Catalog: Meridian Phase 1
**Kata:** K 4.W.6 | **Consumes:** 00-discovery-context.md, 02-containers.mmd, 04-adr-001/002/003.md

> Each pattern is placed — named component, named constraint, named risk if omitted. No abstract descriptions.

| Pattern | Placed at | Constraint addressed | Risk if omitted |
|---|---|---|---|
| Strangler Fig | Apollo Gateway + per-region routing | No rip-and-replace; 22 divergent legacy stacks | Big-bang cutover; store downtime during rollout |
| Outbox | Cart Service + Checkout Service | Dual-write atomicity to PostgreSQL + Kafka | Silent event loss on crash; phantom stock worsens |
| Bulkhead | Checkout Service — per payment adapter | Multi-provider payments; PSD2 SCA on EU flows | One slow provider exhausts shared threads globally |
| Circuit Breaker | Checkout (per provider) + Cart (SAP fallback) | Provider outages must not cascade; SAP not on hot path | Timeout storm under load; repeat of 2024 EU outage |
| BFF | Apollo Gateway — Web / Mobile / POS query shaping | Three surfaces with different data needs | Clients exposed to internal topology; POS over-fetches |

---

## 1. Strangler Fig

**Where placed:** Apollo GraphQL Gateway + per-region traffic routing layer, applied at each regional cutover.

**Meridian constraint it addresses:** The CTO mandated no rip-and-replace. 22 country stacks (Shopify Plus, custom .NET, Magento 2, on-prem Oracle) cannot be migrated simultaneously. Each has its own release cadence (Italy weekly, Japan monthly, US bi-weekly).

**How it works here:** The Apollo Gateway acts as the strangler facade. For each region, traffic is incrementally re-routed from the legacy stack to the new platform service by service (identity first, then cart, then checkout). The legacy stack continues serving un-migrated regions until the platform is ready. The routing rule per region is a feature flag / DNS switch — not a code change.

**Risk if omitted:** A big-bang cutover of all 22 regions simultaneously would require a coordinated freeze across all SI partners and regional teams, a single acceptable downtime window across all stacks, and would void David Park's "no store downtime during rollout" constraint. A single rollback would revert all regions.

**Referenced in:** `00-discovery-context.md` (engineering layer — "strangler-fig mandated by CTO"), `01-context.mmd` (Meridian Platform as single system boundary), `02-containers.mmd` (Apollo Gateway as single entry point).

---

## 2. Outbox

**Where placed:** Cart Service and Checkout Service — transactional event publishing to the Kafka Order Event Bus.

**Meridian constraint it addresses:** Cart state and order records are written to PostgreSQL; `OrderCreated` and `CartMerged` events must be published to Kafka. If a service publishes to Kafka in the same transaction as the database write and then crashes before commit, or commits the DB write but fails the Kafka publish, the system is left in an inconsistent state — an order exists in the DB but downstream consumers (inventory update, email notification) never see it.

**How it works here:** Cart Service and Checkout Service write events to an `outbox` table in PostgreSQL as part of the same local transaction as the business data write. A separate outbox relay process (or Debezium connector) reads the outbox table and publishes to Kafka. Once Kafka acknowledges, the row is marked as published. The relay provides at-least-once delivery; consumers must be idempotent on `OrderCreated`.

**Risk if omitted:** Dual writes (DB + Kafka in sequence without outbox) create a race condition. Under load or partial failure, events are lost silently. Inventory cache never gets the `StockUpdated` signal; click-and-collect availability diverges from reality — directly worsening the phantom-stock cancellation rate that Phase 1 exists to reduce.

**Referenced in:** `02-containers.mmd` (`ContainerQueue(eventBus)`, `Rel(checkoutService, eventBus, "Publishes OrderCreated")`), `04-adr-001.md` (Kafka hydration path for inventory cache).

---

## 3. Bulkhead

**Where placed:** Checkout Service — per payment provider adapter isolation (Stripe EU, Stripe US, Klarna, Postepay, PayPay each have independent thread pools and connection pools).

**Meridian constraint it addresses:** 22-country multi-provider payment landscape with PSD2 SCA on EU flows. A Klarna degradation in the Nordics must not exhaust shared connection threads and starve Stripe payments in Germany or PayPay in Japan. (See ADR-003.)

**How it works here:** Each payment provider adapter in the Checkout Service is given a bounded thread pool and connection pool (e.g., max 20 threads per adapter). If Klarna starts timing out and its pool fills up, requests queue against Klarna's pool only — they cannot borrow threads from Stripe's or PayPay's pool. Saturation of one adapter is contained within that adapter's resource limit.

**Risk if omitted:** A single slow payment provider exhausts the shared Checkout Service thread pool. All checkout requests across all regions queue behind the slow provider's threads. A Klarna SLA degradation during peak becomes a global checkout outage — the exact cascade ADR-003 was written to prevent.

**Referenced in:** `04-adr-003.md` (decision and "do not" clause), `02-containers.mmd` (`Container(checkoutService)`).

---

## 4. Circuit Breaker

**Where placed:** Two locations — (a) Checkout Service, per payment provider adapter; (b) Cart Service, on the SAP ECC synchronous fallback path.

**Meridian constraint it addresses:**
- (a) Payment: a tripped provider must fail fast and return `PAYMENT_PROVIDER_UNAVAILABLE` rather than accumulating timeouts that hold threads. (See ADR-003.)
- (b) Inventory: if SAP ECC is unreachable, the cache-miss fallback path must not hammer a down SAP with retries — it must trip and return `availability: UNKNOWN` immediately. (See ADR-001.)

**How it works here:**
- **(a) Checkout:** Circuit breaker per payment adapter trips after 5 consecutive failures (configurable). In open state, calls fail immediately with a structured error. After the half-open window (30s default), one probe request is allowed; if it succeeds, the breaker closes. Regional GM dashboards surface breaker state per provider.
- **(b) Cart / SAP fallback:** Circuit breaker on the SAP adapter client trips after 3 consecutive timeouts (800ms threshold per ADR-001). In open state, the cart service skips the SAP call and returns `availability: UNKNOWN` with `degraded: true` immediately — no 800ms wait.

**Risk if omitted:** Without circuit breakers, a failing SAP or payment provider accumulates threads waiting for timeout. Under load, this cascades to thread starvation in the calling service. A single provider failure becomes a platform-wide latency spike — the Black Friday scenario that produced the 40-minute EU outage in 2024.

**Referenced in:** `04-adr-001.md` ("do not" clause — 800ms SAP timeout), `04-adr-003.md` ("do not" clause — per-provider breaker), `03-flow-instore-cart.mmd` (SAP unreachable alt block).

---

## 5. Backend for Frontend (BFF)

**Where placed:** Apollo GraphQL Gateway acting as a query-shaping BFF for three distinct client surfaces — Web App (Next.js), Mobile App (React Native), and POS Client (Electron).

**Meridian constraint it addresses:** Three client surfaces with fundamentally different data needs. Web checkout needs full product detail + promotions + loyalty balance. Mobile needs a lightweight cart summary + push notification tokens. POS needs customer identity + cart state + per-SKU availability confidence in one low-latency round-trip on store LAN. A single generic REST API forces every client to over-fetch or make multiple requests.

**How it works here:** Apollo's resolver model allows each client to specify exactly the fields it needs in a single GraphQL query. The gateway fans out to Identity Service, Cart Service, and Inventory Cache in parallel per query — the client does not know or care how many services are involved. POS uses `resolveCustomerCart` (documented in `03-integrations.md`); web and mobile use their own query shapes against the same gateway. No separate BFF service is deployed — Apollo Gateway fulfils the BFF role without an additional deployment unit.

**Risk if omitted:** Without query shaping at the gateway, each client surface would either (a) call multiple downstream services directly — exposing internal topology to POS terminals and mobile apps — or (b) receive a single bloated response containing fields irrelevant to that surface. POS terminals on store LAN would need to know the addresses of Cart Service, Identity Service, and Inventory Cache separately, making POS logic brittle to any service topology change.

**Referenced in:** `02-containers.mmd` (Apollo Gateway as single entry point for all clients), `04-adr-002.md` (POS-to-gateway decision), `03-integrations.md` (`resolveCustomerCart` operation).
