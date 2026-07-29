---
case: A
date: 2026-07-27
consumes: 05-canvas.md
use_case: "#4 — Real-time inventory availability predictor"
---

## Assumptions and sources

| Assumption | Value used | Source |
|---|---|---|
| Total retailer revenue | €2B | unverified — midpoint of €1–5B band |
| Online share of revenue | 35% = €700M | unverified |
| Click-and-collect share of online | 10–17% | unverified — stress-tested lower in pessimistic |
| C&C revenue base | €80M–€150M | unverified — confirm with client data before exec review |
| Click-and-collect cancellation rate | 10–15% | unverified — weakest kept claim from K 1.W.4 |
| Cancellation reduction from predictor | 15–40% | unverified — depends on integration completeness and staff adoption |
| Fulfillment cost reduction | €200K–€1.5M/yr | unverified — confirm against client logistics data |

---

## Cost lines

| Line | Pessimistic | Base | Optimistic | Source |
|---|---|---|---|---|
| Build — API abstraction layer + ML model | €3.5M | €2.5M | €1.5M | unverified — confirm with architecture team; 22-system legacy integration routinely overruns |
| Change management — multi-country staff retraining | €600K | €350K | €150K | unverified |
| Annual run — infrastructure, inference, monitoring, L2 support | €500K/yr | €280K/yr | €150K/yr | unverified |
| **One-time total (build + CM)** | **€4.1M** | **€2.85M** | **€1.65M** | |

---

## Value lines

| Line | Pessimistic | Base | Optimistic | Source |
|---|---|---|---|---|
| Recovered order value (C&C revenue × cancel rate × reduction %) | €1.2M/yr | €5.4M/yr | €9M/yr | unverified baseline; formula: €80M×10%×15% / €120M×15%×30% / €150M×15%×40% |
| Fulfillment cost reduction — fewer failed pickups, re-routes | €200K/yr | €800K/yr | €1.5M/yr | unverified — confirm against client logistics data |
| **Annual value total** | **€1.4M/yr** | **€6.2M/yr** | **€10.5M/yr** | |

---

## ROI table

| Row | Pessimistic | Base | Optimistic |
|---|---|---|---|
| One-time cost (build + CM) | €4.1M | €2.85M | €1.65M |
| Annual run cost | €500K/yr | €280K/yr | €150K/yr |
| Annual value | €1.4M/yr | €6.2M/yr | €10.5M/yr |
| Net annual benefit (value − run) | €900K/yr | €5.92M/yr | €10.35M/yr |
| **Payback period** | **~51 months** | **~6 months** | **~2 months** |

---

## Sensitivity drivers

Moving each input ±20% to identify which assumptions most change the ROI conclusion:

**Driver 1 — Cancellation rate baseline (10–15%)**
At 5% actual rate, base annual value drops from €6.2M to ~€2.5M; payback extends to ~14 months.
This single assumption determines whether the business case holds.
*Flag: unverified — must be confirmed with client OMS data before exec review.*

**Driver 2 — C&C revenue baseline (€80M–€150M)**
Scales all value lines proportionally. At €60M, base annual value halves; base payback extends
to ~12 months and pessimistic case breaks even beyond 7 years.
*Flag: unverified — confirm with client e-commerce analytics.*

Build cost is less sensitive: even at pessimistic €4.1M one-time, the base value case
pays back within 6 months of go-live.

---

## Pessimistic case narrative

At worst: integration overruns to 18 months (€3.5M build), staff adoption is partial,
C&C cancellation reduction is only 15% of a 10% baseline on €80M revenue.
Annual net benefit: €900K. Payback: ~51 months.
This is a bet, not a sure thing. The pessimistic case should be presented alongside the base case
in any exec conversation.

---

## Flags for exec review

- Cancellation rate baseline (15%) — unverified; replace with client OMS data
- C&C revenue base (€120M) — unverified; replace with client e-commerce breakdown
- All cost lines — unverified; replace with architecture and delivery estimates
