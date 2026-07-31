# 07 — Adversarial Pre-mortem: Meridian Phase 1
**Kata:** K 4.W.8 | **Consumes:** full arch pack (00–06)

> Fresh-session pre-mortem. Assume the architecture has shipped and failed. Work backwards from failure. Three stressors, three breaks each — ordered by cascade sequence, not severity. Each break names the signal that surfaces it and either a mitigation or an explicit risk acceptance. Not every risk is worth fixing — some are cheaper to accept than to engineer away.

## Risk acceptance register

| Ref | Break | Acceptance rationale | Owner | Condition to reopen |
|---|---|---|---|---|
| ACC-01 | S2-B1: SAP outage → availability UNKNOWN | Degraded mode is the designed response. Near-real-time fix requires SAP CDC access the team may not have. Cost to accept: ops runbook + store associate training. | SRE (runbook); David Park (store ops sign-off) | If click-and-collect cancellation rate does not improve below NFR-05 target (3%) post-GA |
| ACC-02 | S1-B2: EKS autoscale lag on Black Friday | Custom predictive scaling is complex for one annual event. Accepted with a named ops action: pre-scale Gateway pods 48h before peak. | SRE — calendar owner for peak pre-scale | If pre-scale ops process fails two consecutive years, or if peak traffic exceeds 12,000 RPS |
| ACC-03 | S2-B2: Post-recovery cancellation wave | No architectural fix without blocking checkout, which violates resilience goals. Architecture provides a feature flag capability; Product owns the decision to pull it. | Sarah Chen (Head of CX) — feature flag decision | If post-outage cancellation spike exceeds 3× the NFR-05 weekly baseline |
| ACC-04 | S3-B3: Knowledge cliff on SI departure | No architecture eliminates people risk. This arch pack is the mitigation — decisions are in artefacts, not people. Residual risk accepted. | Lena Park (MRG team lead) — monthly knowledge transfer review | If a second SI departure occurs before Phase 1 GA; escalate to Eva Müller immediately |

---

---

## Stressor 1 — Black Friday Peak: 8,000+ RPS across web, mobile, and 1,400 POS terminals simultaneously

*The 2024 outage happened at lower traffic. Phase 1 is a bigger, more interconnected system.*

### Break 1: Auth0 rate-limits POS token introspection during the peak hour

**What breaks:** POS Client holds machine-to-machine service tokens that expire every hour. At 08:00 on Black Friday, 1,400 stores open simultaneously and their Electron terminals all refresh Auth0 tokens within the same 5-minute window. Auth0's management API rate-limit (default: 2 requests/second per tenant on standard tier) is breached. Token refresh calls return 429. POS terminals cannot authenticate to Apollo Gateway. `resolveCustomerCart` fails for every new store session.

**Why the current architecture is exposed:** ADR-002 places Auth0 on the critical POS path. Assumption #3 in `00-discovery-context.md` explicitly flags Auth0's POS rate-limit behaviour as unverified. No token pre-warming or staggered refresh is specified in the integration contract.

**Signal:** Auth0 dashboard shows 429 spike; Apollo Gateway logs show `UNAUTHENTICATED` errors from POS clients; Datadog alert on NFR-02 breach.

**Mitigation the architecture needs:** Staggered token refresh with jitter (±15 min from expiry); local token cache on POS terminal with a grace window; Auth0 tenant rate-limit reviewed and upgraded before go-live.

**Owner:** Platform engineering (implementation); David Park (POS/ops) — sign-off on Auth0 load test results before Phase 1 GA.

**Patched:** `03-integrations.md` — OQ-4 added; requires Auth0 rate-limit tier confirmation and staggered refresh strategy before Phase 1 GA.

---

### Break 2: Apollo Gateway EKS pods autoscale too slowly — cold start latency breaches NFR-02

**What breaks:** Traffic ramps from 500 RPS to 8,000 RPS in 20 minutes as stores open across EU time zones. Kubernetes HPA triggers new Gateway pod provisioning, but EKS node group scale-out takes 3–5 minutes (cold start: new EC2 instance + container pull + Node.js init). During this window, in-flight POS requests queue behind under-provisioned pods. `resolveCustomerCart` p95 climbs to 800–1,200ms — NFR-02 cache-hit target of 200ms is blown. Store associates experience visible delay at checkout.

**Why the current architecture is exposed:** The arch pack specifies EKS as the runtime but does not specify pre-warming or minimum replica counts for Black Friday. Autoscaling is a deployment-time configuration, not an architectural default — and it is easy to forget.

**Signal:** EKS HPA events showing rapid scale-out; Apollo Gateway p95 trace in Honeycomb crossing 200ms; David Park escalation from store ops.

**Accepted — ACC-02.** Building a predictive scaling controller is complex for one annual event. Named ops action: pre-scale Gateway pods to minimum 20 replicas by 06:00 on peak day; set PodDisruptionBudget to prevent accidental scale-in. Reopen if pre-scale process fails or peak traffic exceeds 12,000 RPS.

---

### Break 3: Redis Inventory Cache evicts keys under memory pressure — availability checks degrade to SAP fallback at peak

**What breaks:** At 8,000 RPS, Cart Service reads inventory keys from Redis at high frequency. If the Redis ElastiCache cluster is under-sized for the working set (all active SKUs across 22 countries), Redis begins evicting less-recently-used keys under its `allkeys-lru` policy. Cache miss rate climbs. Every miss triggers the SAP synchronous fallback (ADR-001) — adding 400–800ms per request. SAP adapter connection pool saturates. Circuit breaker trips (ADR-001 "do not" clause). All subsequent calls return `availability: UNKNOWN`. The availability assistant degrades platform-wide at peak — exactly when it is most needed.

**Why the current architecture is exposed:** `06-nfrs.yaml` specifies NFR-04 (max 30 min staleness) but does not specify Redis memory sizing or eviction policy. Cache sizing is left to infrastructure config. A team optimising cost (NFR-06) will under-provision Redis.

**Signal:** Redis `evicted_keys` CloudWatch metric > 0; Cart Service circuit breaker open state; `degraded: true` spike in API response logs.

**Mitigation:** Size Redis cluster for full SKU working set + 30% headroom before Black Friday; set eviction policy to `volatile-ttl` (evict only keys with TTL set, never inventory keys without TTL); add CloudWatch alarm on `evicted_keys > 0` to catch sizing errors in staging.

**Owner:** Platform engineering / SRE (Redis sizing and eviction policy); validate in Black Friday load test.

**Patched:** `06-nfrs.md` + `06-nfrs.yaml` — NFR-04 updated with `volatile-ttl` eviction policy, 30% headroom requirement, and `evicted_keys > 0` CloudWatch alarm.

---

## Stressor 2 — SAP ECC Extended Outage: 4-hour unplanned downtime during EU business hours

*SAP is on-prem. On-prem ERPs have unplanned outages. The architecture claims to handle this gracefully — does it?*

### Break 1: Inventory cache TTLs expire in waves — `availability: UNKNOWN` spreads across all SKUs within 30 minutes

**What breaks:** Inventory cache keys have a 30-minute TTL (NFR-04). When SAP stops publishing `StockUpdated` events to Kafka, the Kafka consumer has nothing to consume. After 30 minutes, the first wave of Redis keys expires. Cart Service cache misses trigger the SAP fallback — which immediately times out and trips the circuit breaker (ADR-001). All availability responses return `availability: UNKNOWN` with `degraded: true`. Within 60 minutes of the SAP outage, every POS terminal in every store shows "Confirm availability with stock room." Click-and-collect orders can still be placed, but without any confidence signal.

**Why this is tolerable by design (not a flaw):** ADR-001 explicitly accepts this as the degraded-mode path. The question is whether the degraded UX is actually operable at scale — 1,400 store associates simultaneously pivoting to manual stock checks is an operational burden the brief never quantifies.

**Signal:** Kafka `StockUpdated` consumer lag stops growing (no new messages); Redis `expired_keys` rate increases; `degraded: true` spike in availability API responses.

**Accepted — ACC-01.** Near-real-time fix requires SAP CDC access the platform team may not control. Accepted with: ops runbook for SAP outage > 30 min; store associate training on degraded-mode procedure; David Park sign-off. Reopen if post-GA cancellation rate does not reach NFR-05 target.

---

### Break 2: Checkout Service continues accepting click-and-collect orders during the outage — post-recovery cancellation wave

**What breaks:** Checkout Service (ADR-003) is isolated from the inventory path. During the SAP outage, customers can still complete click-and-collect purchases — they just see `availability: UNKNOWN`. Some will proceed anyway (high-intent shoppers). When SAP recovers and the inventory cache is hydrated, store staff discover the shelves were empty during the outage window. A wave of phantom-stock cancellations hits — potentially worse than the 7% baseline because all orders placed during the outage are suspect.

**Why the current architecture is exposed:** The arch pack has no feature flag or rate-limit mechanism to reduce or pause click-and-collect order intake during a detected SAP outage. Checkout is decoupled from inventory by design (resilience), but that decoupling removes the safety valve.

**Signal:** Post-recovery spike in `STOCK_UNAVAILABLE_AT_PICKUP` cancellation codes; NFR-05 (phantom stock rate) breached in the week following the outage.

**Accepted — ACC-03.** No architectural fix without blocking checkout, which violates resilience goals. Architecture provides the feature flag capability; Sarah Chen (Product) owns the decision to pause click-and-collect intake. Reopen if post-outage cancellation spike exceeds 3× the NFR-05 weekly baseline.

---

### Break 3: Kafka consumer lag accumulates during the outage — replay storm on SAP recovery causes a second degraded window

**What breaks:** During the 4-hour SAP outage, the Kafka `StockUpdated` topic receives no new messages. When SAP recovers, it emits a burst of 4 hours of accumulated stock change events — potentially millions of messages depending on the batch export size. The Kafka consumer (Redis hydration) processes this replay at full throughput but lags behind the burst. During the replay, Redis keys contain stale data that is being actively overwritten. Cache reads during replay may return partially-updated inventory state — neither the pre-outage snapshot nor the current reality.

**Why the current architecture is exposed:** The Outbox pattern (05-patterns.md) and ADR-001 describe the steady-state Kafka flow but do not specify consumer lag alerting thresholds or replay handling. A replay storm is a known failure mode for event-driven inventory systems that is easy to overlook.

**Signal:** Kafka consumer group lag spike immediately after SAP recovery; Redis write throughput spike; `sapSyncAgeMin` values oscillating in API responses.

**Mitigation:** Consumer lag alert at 10,000 messages; replay handled with a dedicated catch-up consumer group at lower throughput to avoid Redis write hotspots; `sapSyncAgeMin` displayed to users during replay so confidence states remain accurate. Ops runbook documents expected replay duration.

**Owner:** Platform engineering (Kafka consumer config + runbook); SRE (lag alerting).

**Patched:** `05-patterns.md` — Outbox section updated with replay handling: catch-up consumer group at reduced throughput, lag alert at 10,000 messages, `sapSyncAgeMin` accuracy during replay.

---

## Stressor 3 — Multi-SI Integration Conflict: Three delivery partners ship incompatible changes to shared services before Phase 1 GA

*Three SIs. Shared Cart Service, Identity Service, Apollo Gateway schema. No explicit ownership matrix in the brief.*

### Break 1: SI-A ships a Cart Service API change that breaks SI-B's Identity-cart combined resolver in Apollo Gateway

**What breaks:** SI-A (responsible for Cart Service) ships a breaking change to the `GET /cart/{cart_id}` response schema — renaming `items` to `lineItems` for alignment with commercetools conventions. SI-B (responsible for Apollo Gateway resolvers) has not been notified and has not updated the `resolveCustomerCart` resolver. The resolver silently returns `items: null` for all POS and mobile clients. POS terminals show empty carts. Web checkout proceeds but loyalty-linked items are missing.

**Why the current architecture is exposed:** `03-integrations.md` is a contract skeleton, not an enforced contract. There are no consumer-driven contract tests (e.g. Pact) running in CI between Cart Service and Apollo Gateway. Breaking changes are only caught in integration testing, which requires a full environment — expensive and slow to schedule across three SI teams.

**Signal:** Apollo Gateway resolver returning `null` for `items`; POS QA catch in staging; or worse, production alert from real store associates reporting empty carts.

**Mitigation:** Consumer-driven contract tests (Pact or OpenAPI diff) enforced in CI for every Cart Service and Identity Service deployment. Apollo Gateway schema version pinned; any downstream service change that breaks the published schema fails the gateway's CI pipeline. SI ownership matrix must be written before first shared service deployment.

**Owner:** Architecture lead (schema versioning policy + SI ownership matrix); each SI team (contract test implementation in their own CI).

**Patched:** `04-adr-004.md` — new ADR: consumer-driven contract tests in CI as merge blocker; 4-week change-freeze gate before each quarterly milestone; architecture lead owns schema version.

---

### Break 2: The break is discovered in staging two weeks before Phase 1 GA — integration freeze is triggered, slipping the quarterly board gate

**What breaks:** The incompatibility surfaces during integration testing at week 6 of an 8-week Phase 1 sprint. Fixing it requires coordinating three SI teams across two time zones to agree on the correct schema, update the contract tests, redeploy Cart Service and the Gateway, and re-run end-to-end POS and checkout tests. This takes 10–14 days. Phase 1 GA slips past the month-8 quarterly stage gate.

**Why the current architecture is exposed:** The arch pack documents the integration contract and the ADRs, but does not specify a shared API versioning policy, a change-freeze window, or a pre-GA integration sign-off gate between SI teams. Assumption #4 in `00-discovery-context.md` explicitly flags SI coordination conflicts as unverified.

**Signal:** Programme manager escalation; Eva Müller board gate risk flag; David Park expressing concern about POS readiness.

**Mitigation:** Integration sign-off gate established 4 weeks before each quarterly milestone — no breaking API changes after the gate without architecture lead approval. Shared API changelog maintained by the architecture team, not individual SIs. The architecture lead owns the schema version; no SI ships a breaking change without written sign-off.

**Owner:** Architecture lead (sign-off gate + changelog); Eva Müller (board gate — escalation if Phase 1 GA slips).

**Patched:** `04-adr-004.md` — change-freeze gate formalised; additive changes permitted after gate; breaking changes require written architecture lead sign-off.

---

### Break 3: The slip triggers a budget re-forecast — one SI is put on notice, creating a knowledge cliff on Cart Service

**What breaks:** Eva Müller's quarterly stage gate review flags the GA slip. The SI responsible for the breaking Cart Service change is put on a performance notice; one senior engineer leaves the engagement. Cart Service institutional knowledge walks out with them — the internal MRG team (junior, still learning the platform) cannot fill the gap. A second integration issue surfaces three weeks later; this time there is no SI expertise available to diagnose it quickly.

**Why this is an architectural risk, not just a people risk:** Assumption #5 in `00-discovery-context.md` — the internal MRG team operability assumption — is directly violated. The architecture was designed with a knowledge transfer plan that assumed SI continuity through Phase 1 GA. An SI departure before GA is a forcing function that the architecture does not account for.

**Signal:** Cart Service incident resolution time increases from minutes to hours; Lena Park escalates operability concerns; on-call runbook coverage gaps surface in post-incident reviews.

**Accepted — ACC-04.** No architecture eliminates people risk. This arch pack — ADR "do not" clauses, integration contracts, NFR budgets, this pre-mortem — is the mitigation. Residual risk accepted on the condition that Lena Park attends every architecture review from week 1. Reopen immediately if a second SI departure occurs before Phase 1 GA.
