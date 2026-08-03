# 00 — Architectural Options: Inventory / Cart-Bridge Read Model
**Kata:** K 4.W.2 | **Consumes:** 00-discovery-context.md
**Decision:** How does the Meridian platform read inventory and bridge the online/in-store cart while SAP ECC remains the source of truth?

> Three options. No choice yet — that is K 4.W.5's job.

---

## Option A — Synchronous reads direct from SAP ECC (boring option)

**Core idea:**
- The platform queries SAP ECC directly, synchronously, on every inventory availability check and cart-bridge operation.
- No intermediate cache or event bus — SAP is called inline per request.
- Apollo Gateway routes inventory/cart calls through a SAP adapter service.

**Optimises for:** Simplicity and data accuracy — no cache to keep fresh, no event pipeline to operate; inventory is always point-in-time current from the source.

**Sacrifices:** Latency and resilience — SAP ECC inline reads are 200–600ms p95; a 2-hour SAP outage stops all inventory checks and in-store cart lookups platform-wide; SAP cannot handle the concurrent read load of 1,400 stores + online traffic at peak.

**Meridian constraint that pressures it hardest:** Black Friday peak load. SAP ECC is an on-prem ERP not designed as a high-concurrency API backend. At 8,000+ RPS during peak, SAP would saturate and cascade failures to the POS. David Park's "stores keep selling" constraint directly contradicts this option at scale.

---

## Option B — Event-driven read model hydrated from SAP via Kafka (recommended baseline)

**Core idea:**
- SAP ECC publishes stock events (via batch export or CDC/Debezium) to a Kafka topic on a 15–30-minute cycle.
- A dedicated Inventory Read Cache (Redis) is hydrated from Kafka asynchronously; the cache is the platform's inventory source.
- Synchronous SAP calls are used only as a fallback on cache miss, with a degraded-mode path ("stock unknown — confirm with staff") if SAP is unreachable.

**Optimises for:** Read performance and resilience — Redis reads at ~1–5ms p95; platform survives SAP outages with a degraded-mode response; peak load is absorbed by the cache layer, not SAP.

**Sacrifices:** Data freshness — the cache is stale by the SAP batch cycle (15–30 min minimum); this is the root cause of phantom-stock cancellations and cannot be fully eliminated without a CDC path to SAP, which requires SAP configuration access. Adds Kafka + CDC/Debezium operational burden.

**Meridian constraint that pressures it hardest:** SAP batch-update reality (assumption #1 from 00-discovery-context.md). If MRG cannot configure SAP for CDC, the cache is hydrated from batch exports only — staleness is structural, not solvable by the platform team alone.

---

## Option C — Buy a cross-channel inventory service (commercial OMS layer)

**Core idea:**
- A commercial Order Management / Inventory Visibility platform (e.g., Fluent Commerce, OneStock, or Manhattan Active) is inserted between SAP and the headless platform.
- The OMS owns inventory aggregation, cross-channel reservation, and soft-hold logic; it connects to SAP via a vendor-managed integration.
- The platform queries the OMS for availability; SAP is abstracted behind the vendor.

**Optimises for:** Capability richness and speed-to-feature — soft holds, cross-channel reservations, per-store allocation rules, and regional inventory policies are table-stakes features of these platforms; building them from scratch on Kafka/Redis would take months.

**Sacrifices:** Vendor dependency, cost, and integration complexity — a commercial OMS adds €200–400k/year licensing plus a 3–6 month integration project before Phase 1 can use it. The junior MRG team must now operate a second complex vendor alongside commercetools. Tomás Reyes' "headless platform becoming the new monolith" worry applies — an OMS layer can quietly absorb scope that belonged in the platform.

**Meridian constraint that pressures it hardest:** 18-month / $42M budget with quarterly stage gates. A 3–6 month OMS integration competes directly with Phase 1 GA at month 8. The junior internal team operability constraint also applies — two complex vendor platforms (commercetools + OMS) to learn simultaneously is a high knowledge-transfer risk for Lena Park's team.

---

## Load-bearing dimension summary

| Dimension | Option A (Sync SAP) | Option B (Event-driven cache) | Option C (Buy OMS) |
|---|---|---|---|
| Inventory latency | 200–600ms (SAP inline) | 1–5ms (Redis cache) | 10–50ms (OMS API) |
| SAP outage impact | Platform-wide failure | Degraded mode only | Depends on OMS SLA |
| Phantom stock risk | Zero (real-time) | Structural (batch staleness) | Low (OMS manages holds) |
| Team operability | Low complexity | Medium (Kafka + CDC) | High (2 vendor platforms) |
| Phase 1 fit (month 8) | Fast to build | Moderate build time | Risky — 3–6 month integration |
| Cost | Low | Low–medium (infra only) | High (licensing + integration) |
