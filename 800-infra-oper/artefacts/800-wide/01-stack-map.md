# K 8.W.1 — Stack Map: `cart-api`

**Reference case:** Meridian Retail Group — Case A  
**Service brief:** `cart-api`, a checkout service. Runs as containers on a Kubernetes cluster behind a load balancer; reads and writes a Postgres database; caches in Redis; for the "summarise my cart" step it calls a language model through the company gateway (EPAM DIAL). ~3,000,000 AI calls/month.

---

## Component inventory

| # | Component | What it does | Owner |
|---|---|---|---|
| 1 | **Load Balancer** | Accepts HTTPS requests from clients; routes traffic to healthy pods | [ops] |
| 2 | **Kubernetes Cluster** | Pools compute, schedules container replicas, restarts crashed pods, scales under load | [ops] |
| 3 | **`cart-api` container (pod)** | Runs the checkout business logic — add/remove items, calculate totals, trigger summarise step | [mine/Product] |
| 4 | **Postgres database** | Persists cart state, order records, and customer data | [ops] |
| 5 | **Redis cache** | Caches frequently-read cart data to reduce DB load and latency | [ops] |
| 6 | **EPAM DIAL gateway** | One front door for all AI calls — routes to the language model, attributes cost per team/feature, enforces spend cap, keeps prompt-and-response audit trail | [ops] |
| 7 | **Language model (LLM)** | Generates the natural-language cart summary on demand | [ops] |
| 8 | **Observability stack** (metrics / logs / traces) | Watches all components; fires alerts; surfaces latency, error rate, cost signals | [ops] |

---

## Request flow — Mermaid diagram

```mermaid
flowchart LR
    User([User / Browser]) -->|HTTPS| LB["Load Balancer [ops]"]
    LB --> Pod["cart-api container [mine/Product] (Kubernetes pod)"]
    Pod -->|read/write| DB["Postgres DB [ops]"]
    Pod -->|read/write| Cache["Redis Cache [ops]"]
    Pod -->|AI call ~3M/month| GW["EPAM DIAL Gateway [ops]"]
    GW --> LLM["Language Model [ops]"]
    LLM --> GW
    GW --> Pod
    Pod --> LB
    LB --> User
    OBS["Observability stack [ops] (metrics, logs, traces)"] -.->|watches| LB
    OBS -.->|watches| Pod
    OBS -.->|watches| DB
    OBS -.->|watches| Cache
    OBS -.->|watches| GW
```

---

## Ownership summary

| Tag | Components |
|---|---|
| **[ops]** — platform team owns | Load Balancer, Kubernetes Cluster, Postgres DB, Redis Cache, EPAM DIAL Gateway, Language Model, Observability stack |
| **[mine/Product]** — my team owns | `cart-api` container — its behaviour, business logic, and acceptance bar |

**Key insight:** 7 of 8 components are owned by ops. My team owns one box — what the app *does*, not where it runs. An outage in any of the 7 [ops] components is not mine to fix; it *is* mine to notice and escalate.
