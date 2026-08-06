# K 8.W.5 — Monthly cost estimate + DIAL cap: `cart-api`

**Reference case:** Meridian Retail Group — Case A

---

## Cost profile (input)

| Item | Value |
|---|---|
| Cloud rent | 3 pods + 1 Postgres + 1 Redis + 1 load balancer ≈ $1,500 / month (flat) |
| AI input tokens / call | 1,200 (system prompt + cart contents) |
| AI output tokens / call | 200 (summary text) |
| AI calls / month | 3,000,000 |
| AI price | $2.50 / M input · $10.00 / M output |

---

## Line-by-line breakdown

| Line | Calculation | Monthly cost |
|---|---|---|
| **Cloud rent** | Flat — 3 pods + Postgres + Redis + LB | **$1,500** |
| **AI input** | 3,000,000 calls × 1,200 tokens × $2.50 / 1,000,000 | **$9,000** |
| **AI output** | 3,000,000 calls × 200 tokens × $10.00 / 1,000,000 | **$6,000** |
| **AI meter subtotal** | $9,000 + $6,000 | **$15,000** |
| **Monthly total** | $1,500 + $15,000 | **$16,500** |

**Manual spot-check (AI input line):** 3,000,000 × 1,200 = 3,600,000,000 tokens ÷ 1,000,000 × $2.50 = **$9,000** ✓

---

## Cost split

| Bucket | Amount | % of total | Behaviour |
|---|---|---|---|
| **Cloud rent** | $1,500 | 9% | Sticky — flat whether busy or idle; reduced only by rightsizing or scaling down |
| **AI meter** | $15,000 | 91% | Scales with traffic — doubles if call volume doubles; a runaway loop compounds it further |

**The AI meter is the bill.** Cloud rent is predictable; the AI summarise step at 3M calls/month is where cost lives and where surprises come from.

---

## Attribution

| Owner | What they own |
|---|---|
| **Platform / Ops team** | Cloud rent ($1,500) — compute, storage, network |
| **Checkout / cart-api feature team** | AI meter ($15,000) — the "summarise my cart" step, its call volume, and its token count |

The AI meter charges against the **Checkout feature team's P&L**, not the platform budget. The platform team enforces the cap at the gateway; the feature team owns the cost decision.

---

## Recommendation

**Ship-with-mitigation.** The AI meter ($15,000/month) is within a plausible product budget for a feature at 3M calls/month, but:

1. The DIAL hard cap must be in place **before** launch — without it, a loop or traffic spike recreates the Team A scenario from Wide Theory ($18,000 discovered on the invoice).
2. The Checkout feature team's P&L owner must explicitly accept the $15,000/month AI line.
3. A retry loop on the summarise step (no retry cap — see K 8.W.3 Gap 2) could spike the meter 2–4× in minutes.

---

## DIAL cost cap

| Signal | Value | Rationale |
|---|---|---|
| **Alert threshold** | $12,000 / month AI spend | 80% of expected meter — fires in time to investigate before breach |
| **Hard cap** | $18,000 / month AI spend | 120% of expected — allows traffic variance; hard-refuses calls above this, logs and pages the feature team budget owner |

Set at the **feature / tenant level** in DIAL (Checkout team), not at the gateway global level, so a cap breach on `cart-api` does not block other teams' AI calls.

**Daily equivalent cap** (for burst detection): $18,000 / 30 = $600/day. A single day exceeding $1,200 (2×) should page the budget owner immediately — it indicates a loop, not traffic growth.
