# SLO — cart-api

**Status:** DRAFT — no formal SLO has been adopted for `cart-api`.  
**Owner:** UNKNOWN — no designated SLO owner confirmed (K 8.W.6, Question 2).

---

## Proposed SLI/SLO targets (not yet ratified)

| Signal | SLI | SLO target | Measurement window |
|---|---|---|---|
| Availability | % of requests returning 2xx | ≥ 99.5% | 30-day rolling |
| Latency (p95) | % of requests completing in < 500 ms | ≥ 95% | 30-day rolling |
| Error rate | % of requests returning 5xx | ≤ 1% | 30-day rolling |
| AI summarise latency (p95) | % of `/summarise` calls completing in < 10 s | ≥ 95% | 30-day rolling |

## Burn-rate alert

No burn-rate alert configured. This is a flagged gap (K 8.W.6, Question 3).  
A 1% error-rate SLO at 99.5% availability requires a burn-rate alert at 2× and 5× to detect fast burns before exhausting the error budget.

## Escalation

SLO breaches escalate to on-call — **UNKNOWN** (no on-call rotation defined; K 8.W.6, Question 2 gap).
