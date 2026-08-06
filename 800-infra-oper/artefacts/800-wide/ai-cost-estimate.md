# AI cost estimate — `cart-api` summarise step

**Service:** `cart-api` · **Feature:** "Summarise my cart" (AI step via EPAM DIAL)  
**Source:** `05-cost-estimate.md` (K 8.W.5)  
**Date:** 2026-08-06

---

## Cost model inputs

| Parameter | Value | Source |
|---|---|---|
| AI input tokens / call | 1,200 tokens (system prompt + cart contents) | K 8.W.5 |
| AI output tokens / call | 200 tokens (cart summary text) | K 8.W.5 |
| AI calls / month | 3,000,000 (baseline traffic) | K 8.W.5 |
| Model price — input | $2.50 per 1M tokens | K 8.W.5 |
| Model price — output | $10.00 per 1M tokens | K 8.W.5 |
| Cloud rent (flat) | $1,500 / month | K 8.W.5 |

---

## Monthly cost breakdown

| Line | Calculation | Cost |
|---|---|---|
| Cloud rent | Flat (3 pods + Postgres + Redis + LB) | **$1,500** |
| AI input meter | 3,000,000 × 1,200 tokens × $2.50 / 1,000,000 | **$9,000** |
| AI output meter | 3,000,000 × 200 tokens × $10.00 / 1,000,000 | **$6,000** |
| **AI meter subtotal** | $9,000 + $6,000 | **$15,000** |
| **Total** | $1,500 + $15,000 | **$16,500** |

**Spot-check (AI input):** 3,000,000 × 1,200 = 3.6 × 10⁹ tokens ÷ 1,000,000 × $2.50 = **$9,000** ✓

---

## Cost split

| Bucket | Amount | % of total | Behaviour |
|---|---|---|---|
| Cloud rent | $1,500 | 9% | Sticky — flat whether busy or idle |
| AI meter | $15,000 | 91% | Variable — scales linearly with call volume |

**The AI meter is the bill.** A retry loop with no cap (K 8.W.3 Gap 2 — `retry_cap` not set in CI workflow) could spike the meter 2–4× within minutes.

---

## Attribution

| Owner | Budget line | Amount |
|---|---|---|
| **Platform / Ops team** | Cloud rent | $1,500 / month |
| **Checkout / cart-api feature team** | AI meter | $15,000 / month |

The AI meter charges against the **Checkout feature team's P&L**. The platform team enforces the cap at the DIAL gateway; the feature team owns the cost decision and must explicitly accept the $15,000 / month line before launch.

---

## DIAL cost caps

| Signal | Value | Unit | Rationale |
|---|---|---|---|
| Alert threshold | $12,000 | / month | 80% of expected meter — fires in time to investigate before breach |
| Hard cap | $18,000 | / month | 120% of expected — allows traffic variance; hard-refuses calls above this |
| Daily burst alert | $1,200 | / day | 2× the $600/day equivalent — indicates a loop, not organic growth |

Caps set at **feature / tenant level** (Checkout team) in DIAL — a breach on `cart-api` does not block other teams' AI calls.

---

## Threshold check (gate criterion)

| Check | Result |
|---|---|
| Threshold stated? | ✅ Yes — $18,000 / month hard cap, $12,000 alert |
| Attribution owner named? | ✅ Yes — Checkout feature team P&L |
| Model named? | ✅ Yes — language model via EPAM DIAL gateway (pricing: $2.50 input / $10.00 output per 1M tokens) |
| Runaway risk identified? | ✅ Yes — retry loop without `retry_cap` can compound the meter (K 8.W.3 Gap 2) |

All four gate criteria met. This estimate may be shared with the Checkout P&L owner for sign-off.

---

## Escalation boundary

**Human-owned decisions (agent does not make these):**

- Accepting or rejecting the $15,000 / month AI meter as a product budget line
- Raising the DIAL hard cap above $18,000 / month
- Changing the cost attribution (which team's P&L)
- SLO-linked cost budgeting (no SLO currently ratified — see `slo/slo.md`)
