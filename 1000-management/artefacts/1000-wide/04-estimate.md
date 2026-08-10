---
kata: 10.W.5
consumes: 02-solution.md, 03-staffing.md, 00-rfp.md, M800-cost-estimate, M900-risk-register
date: 2026-08-10
note: Markdown stand-in for 04-estimate.xlsx
---

# Estimate — Meridian Unified ATP System

## Diagnosis of provided draft (four planted defects)

| # | Defect | Location in draft |
|---|---|---|
| D1 | **Contingency folded into margin** — "25% covers both our profit and any risk that materialises" — one combined line hides whether risk reserve or profit gets cut at negotiation | Margin & contingency section |
| D2 | **Risk with no active mitigation** — R1 (legacy-support expiry, L4×I5) has a dash in the mitigation column — an unmitigated high-scored risk is a complaint, not a plan | Risk register, row 1 |
| D3 | **Unbounded assumptions** — "The team will be productive" and "Client provides test data by end of Discovery" are unfalsifiable; no number, no named condition, no stop-trigger | Assumptions section |
| D4 | **Commercial model fights RFP constraint** — RFP states fixed-price preferred, 12-month hard timeline tied to legacy-support expiry; draft recommends T&M "for flexibility" | Commercial recommendation |

---

## Repaired Estimate

### 1. Base Effort (Balanced staffing variant, from 03-staffing.md)

Blended rate for 25% on / 45% near / 30% off-shore (EU market):
on-shore senior €24,200/FTE-month · near-shore mid €15,400 · off-shore mid €9,900
→ blended **€15,950 / FTE-month**

| Phase | Duration | Peak FTEs | FTE-months | Blended cost |
|---|---|---|---|---|
| Phase 1 — Architecture Spike | 1 month | 5 | 2.0 | €31,900 |
| Phase 2 — Foundation & Integration | 4 months | 14 | 38.0 | €606,100 |
| Phase 3 — AI Predictor & Shopper UI | 4 months | 13 | 40.0 | €638,000 |
| Phase 4 — Hardening & Go-Live | 4 months | 10 | 31.0 | €494,450 |
| **Base effort total** | **~12 months** | | **~111 FTE-months** | **€1,770,450** |

---

### 2. Delivery Impacts (separate lines)

| Impact | Basis | Cost |
|---|---|---|
| Ramp-up (months 1–3 of each phase, 30/60/100%) | 10% of base effort | €177,000 |
| Dependency wait (MRG API access + OMS data confirmation) | 4% of base effort | €71,000 |
| Bird & Bird LLP — GDPR legal review (outsourced, 22 jurisdictions) | Fixed-fee engagement | €150,000 |
| AI development tooling (DIAL + GitHub Copilot, ~12 team members × 12 months) | €500/person/month, sourced from M800 gateway logs | €72,000 |
| **Delivery impacts total** | | **€470,000** |

**Adjusted base (effort + impacts): €2,240,450**

---

### 3. Risk Register

*All rows require an active mitigation. An unmitigated risk is a deal-breaker, not a line item.*
*Seeded from M900 risk register (02-risks.csv) and M600 test report residual risks.*

| # | Risk | Likelihood (1–5) | Impact (1–5) | Active mitigation | Contingency sizing |
|---|---|---|---|---|---|
| R1 | 22-system integration complexity exceeds spike estimate — hidden API variants or undocumented country stacks inflate Phase 2 timeline | 3 | 5 | Contractual spike gate: no full-build commitment until Phase 1 ADR confirms scope; Phase 2 fixed-price locked only after spike exit | 6% of adjusted base → €134,000 |
| R2 | DPA 4-country tail (≤4 jurisdictions unsigned at Phase 2 exit) arrives as a change request at Phase 3–4 boundary | 3 | 3 | Named escalation path: unsigned countries excluded from Phase 2 scope; Bird & Bird late-completion retainer budgeted as a separate line; MRG Head of Omnichannel owns Phase 3 go/no-go decision | 3% → €67,000 |
| R3 | EU AI Act reclassification to High Risk (Annex III) — preliminary analysis not completed before full-build contract | 4 | 5 | Preliminary Annex III / Article 6 analysis completed before oral presentation; if High Risk, conformity assessment added to Phase 3 (12–20 weeks, potential Phase 4 collapse) | 4% → €90,000 |
| R4 | BOLA / API security vulnerability in cart-api ownership-verification layer (T06, H/H in M900) | 2 | 5 | Ownership-verification middleware (cart_ownership_check.py) implemented in Phase 2; 5/5 pytest tests passing (commit 3b729d6); anomaly alerting in Phase 3 | Covered by existing implementation |
| R5 | ML model accuracy degraded by DPA-excluded country training data (A2 gap) | 3 | 3 | Excluded-country impact documented at Phase 3 kick-off; degraded-mode fallback (S4) activates for stores in affected countries until DPA signed | 2% → €45,000 |
| **Contingency total** | | | | | **€336,000 (15% of adjusted base)** |

*Contingency sized bottom-up from risk register: R1 + R2 + R3 + R5 = €336,000 ≈ 15% of adjusted base.*

---

### 4. Margin

Separate from contingency. Contingency is the risk reserve; margin is profit.
Negotiation cuts one — you need to know which.

**Margin: 12% of adjusted base = €268,800**

*Note: margin is intentionally set below contingency here because R3 (EU AI Act reclassification)
carries a realistic 12–20 week schedule impact that could absorb the full contingency reserve.
If Phase 1 and pre-submission analysis close R3, margin can be revised upward.*

---

### 5. Annual Run Cost (recurring, post go-live)

Sourced from M800 `05-cost-estimate.md` (canonical AI-costs reference):

| Line | Monthly | Annual |
|---|---|---|
| Cloud rent (pods + Postgres + Redis + LB) | $1,500 | $18,000 |
| AI inference meter (cart-api, 3M calls/month) | $15,000 | $180,000 |
| **Run total** | **$16,500** | **$198,000 ≈ €180,000** |

DIAL hard cap: $18,000/month at feature/tenant level (Checkout team P&L).

---

### 6. Total Price Summary

| Line | Amount |
|---|---|
| Base effort | €1,770,450 |
| Delivery impacts | €470,000 |
| **Adjusted base** | **€2,240,450** |
| Contingency (15%, risk register) | €336,000 |
| Margin (12%) | €268,800 |
| **One-time total** | **€2,845,250** |
| Annual run cost (recurring) | €180,000/yr |

One-time total is within the base-case envelope (€2.85M, M100 ROI brief) and
well inside the pessimistic ceiling (€4.1M, RFP constraint).

---

### 7. Assumption Register

*Each assumption is bounded numerically or by a named condition. Unbounded assumptions protect nothing.*

| # | Assumption | Bound / falsification condition |
|---|---|---|
| AS1 | Team reaches ≥70% of planned sprint velocity by sprint 3 of each phase | If sprint 3 velocity is <70% of plan, delivery lead reviews resourcing within 5 working days; Phase timeline shifts if not resolved by sprint 4 |
| AS2 | MRG provides OMS cancellation-rate data (baseline confirmation) by Phase 1 week 1 | If not provided by Phase 1 week 1, Phase 1 exit date shifts by the number of days delayed; value hypothesis cannot be confirmed without this data |
| AS3 | SAP CDC path (Debezium) or batch export to Kafka is technically feasible for ≥3 representative stacks | Confirmed or refuted at Phase 1 exit; if batch-only, 15–30 min structural staleness is accepted as in-scope and documented in Phase 2 ADR |
| AS4 | ≥18 of 22 DPA addenda are signed and filed by Phase 2 week 10 | If <18 are signed by Phase 2 week 10, Phase 2 exit is delayed; Bird & Bird retainer extended at €15,000/week; MRG General Counsel notified |
| AS5 | One environment refresh (staging → production) is included in the price | A second refresh (e.g. emergency rollback in Phase 4) requires a named change request; estimated additional cost €15,000–€25,000 |

---

### 8. Commercial Recommendation

**Fixed-price with a two-stage gate — not T&M.**

The RFP states fixed-price preferred and the 12-month deadline is tied to a hard
constraint (legacy-support expiry equivalent: MRG's phantom-stock problem cannot wait).
A T&M recommendation at bid submission signals that the team is not confident in the
scope — which is what the qualification memo's deal-breaker is designed to manage, not
hide behind billing flexibility.

Structure:
- **Stage 1:** Fixed-fee architecture spike (Phase 1, ~€80,000). Capped. MRG signs this
  alone; no full-build commitment.
- **Stage 2:** Fixed-price full build (Phases 2–4, €2,765,250) — contracted only after
  Phase 1 exit ADR is independently reviewed and go/no-go is signed.

Who carries the risk: supplier carries delivery risk within the scope defined at Phase 1
exit. MRG carries risk on client-side dependencies (OMS data, SAP CDC access, DPA
negotiations). Change requests require written sign-off from both parties before work
begins.

**Commercial model decision matrix:**

| Model | Risk-fit | Cash-flow-fit | Buyer-fit |
|---|---|---|---|
| T&M | Supplier favoured — cost risk transfers to buyer | Buyer pays as work happens | Low — RFP prefers fixed-price; signals supplier uncertainty |
| **Fixed-price (recommended)** | **Supplier carries delivery risk within defined scope** | **Buyer has cost certainty; stage gate limits exposure** | **High — matches RFP preference; spike gate manages supplier risk** |
| Hybrid (T&M spike + fixed build) | Balanced — spike uncertainty managed; build risk defined | Moderate | Medium — acceptable if fixed-price on full build is confirmed post-spike |
