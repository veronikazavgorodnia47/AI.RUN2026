# REFERENCE.md — Architecture agent context pack
**Bundled for:** `architecture-meridian` skill (K 4.3)
**Load when:** producing ADRs, NFRs, or pre-mortem outputs that must match established Meridian architectural decisions.

---

## Accepted ADR decisions (carry-forward — do not re-open without new evidence)

| ADR | Decision | "Do not" clause |
|---|---|---|
| ADR-001 | Inventory read from Redis cache hydrated via Kafka; SAP never on hot path | Do not query SAP synchronously on any user-facing path; fallback timeout 800ms max |
| ADR-002 | POS communicates exclusively through Apollo GraphQL Gateway | Do not add direct service-to-POS endpoints bypassing the gateway |
| ADR-003 | Per-region bulkhead + circuit breaker per payment provider in Checkout Service | Do not share a connection pool across providers or regions |
| ADR-004 | Consumer-driven contract tests in CI as merge blocker; 4-week change-freeze gate | Do not merge a breaking API change without passing contract test + architecture lead sign-off |

---

## Accepted risks (carry-forward — reopen only on named conditions)

| Ref | Risk | Owner | Reopen condition |
|---|---|---|---|
| ACC-01 | SAP outage → availability UNKNOWN platform-wide | SRE (runbook); David Park (sign-off) | Cancellation rate does not reach NFR-05 target (<3%) post-GA |
| ACC-02 | EKS autoscale lag on Black Friday — ops pre-scale accepted | SRE (calendar owner) | Pre-scale fails two consecutive years, or peak > 12,000 RPS |
| ACC-03 | Post-SAP-recovery cancellation wave — Product feature flag accepted | Sarah Chen, Head of CX | Post-outage spike > 3× NFR-05 weekly baseline |
| ACC-04 | Knowledge cliff on SI departure — arch pack as mitigation | Lena Park, MRG team lead | Second SI departure before Phase 1 GA |

---

## NFR targets (confirmed — do not change without measurement evidence)

| ID | Family | Target | Owner |
|---|---|---|---|
| NFR-01 | Latency | EU checkout p95 < 3,000ms (PSD2 SCA floor baked in) | Checkout engineering |
| NFR-02 | Latency | POS cart resolution p95 < 200ms cache hit; degraded mode always < 200ms | Platform engineering |
| NFR-03 | Reliability | 99.95% monthly availability; < 22 min downtime/month | SRE / David Park |
| NFR-04 | Reliability | Inventory cache max 30 min staleness; `volatile-ttl` eviction; 30% Redis headroom | Platform engineering |
| NFR-05 | Quality | Phantom stock cancellations < 3% at 6 months post-GA (baseline: 7%) | Sarah Chen (Head of CX) |
| NFR-06 | Cost | < €0.02 per checkout transaction at 8,000 RPS peak | Engineering leads |
| NFR-07 | Security | Zero card data outside PCI boundary; zero EU PII outside eu-west-1 / eu-central-1 | Security / Legal |

**Availability note:** 99.95% is the ceiling for Meridian — mid-market fashion retailer, strangler-fig migration, junior internal team. Five-nines (99.999%) is for emergency services. Do not commit above 99.95% without an explicit SLA justification.

---

## Key Meridian constraints (from 00-discovery-context.md)

| Constraint | Layer | Architectural implication |
|---|---|---|
| SAP ECC batch export 15–30 min cycle | Engineering | Inventory cache is structurally stale; phantom stock is reducible, not eliminable |
| Strangler-fig mandated by CTO | Engineering | No rip-and-replace; Apollo Gateway is the facade per region |
| 1,400 POS terminals; stores keep selling (David Park) | Business | Gateway and Auth0 must not be SPOFs; degraded mode always responds |
| PSD2 SCA mandatory on EU card payments | Regulatory | 500–1,500ms SCA floor on EU checkout; NFR-01 target accounts for this |
| PCI-DSS Level 1 | Regulatory | Strict trust boundary around Checkout + payment containers; no card data in logs |
| GDPR EU data residency | Regulatory | All EU PII stays in eu-west-1 / eu-central-1; no US-only routing without SCCs |
| Junior internal MRG team (Lena Park) | Business | Operational complexity is a first-class constraint; arch pack is the knowledge transfer |
| Three SI partners; no ownership matrix in brief | Engineering | SI conflict is a named risk (ADR-004); contract tests are the guard |
| $42M / 18-month program; quarterly stage gates (Eva Müller) | Business | Phase 1 GA at month 8 is a funding gate; any slip triggers board escalation |

---

## Implicit assumptions (from 00-discovery-context.md — each is a named risk)

1. SAP can serve near-real-time inventory reads — **unverified**; batch reality makes "live inventory" a misnomer.
2. Strangler-fig boundary is a single routing layer — **unverified**; 22 different legacy stacks require per-region routing strategies.
3. Auth0 handles POS authentication at 1,400-store peak throughput — **unverified**; pre-mortem S1-B1 is the failure mode.
4. Three SIs will not create integration conflicts — **unverified**; ADR-004 and pre-mortem S3-B1/B2 address this.
5. Internal MRG team can operate the platform post-handover — **unverified**; ACC-04 is the accepted risk.

---

## Forbidden patterns (verbatim — carry into every ADR and NFR)

- Synchronous SAP reads on any user-facing or POS-facing hot path
- Shared connection pools across payment providers
- Direct service-to-POS endpoints that bypass Apollo Gateway
- Breaking API changes merged without contract test + architecture lead sign-off
- Availability targets above 99.95% without explicit SLA justification
- Redis sized for current load only — must include 30% headroom and `volatile-ttl` eviction policy

---

## Human-owned decisions (never decide)

Program scope · phase boundaries · SI partner selection and ownership matrix ·
ship-readiness and go/no-go · commercial vendor decisions · regulatory sign-offs ·
team structure · knowledge transfer sign-off · whether any risk acceptance is still valid.
