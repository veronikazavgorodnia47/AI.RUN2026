---
kata: 10.W.2
consumes: 00-rfp.md, opportunity-brief.md (M100)
date: 2026-08-10
---

# Qualification Memo — Meridian RFP-2026-ATP

## 1. Fit Scores

| Dimension | Score (1–5) | Rationale |
|---|---|---|
| **Capability** | 4 | Pre-built BOLA middleware, SAP/Apollo Gateway integration patterns, event-driven architecture ADRs, and GDPR-compliant data pipeline (M400/M900) reduce the novel risk to the 22-system abstraction layer — the one genuinely unsolved piece. |
| **Delivery** | 3 | 12-month timeline is achievable if the architecture spike (3 stacks, 4 weeks) confirms integration cost; 22-country scope at this fragmentation level has no confirmed precedent in our portfolio — conditional pass, not a strong pass. |
| **Commercial** | 3 | Base ROI payback ~6 months if cancellation baseline holds; but the 15% baseline is unverified and the €80–150M C&C revenue estimate is unconfirmed — the deal looks attractive but the pricing risk is high until OMS data is in hand. |
| **Strategic** | 4 | EU omnichannel retail + AI-native delivery + GDPR/EU AI Act depth is core to our positioning; a successful Meridian reference would open mid-market EU fashion as a repeatable segment. |

**Aggregate read:** strong on capability and strategy; conditional on delivery and commercial. Bid is justified only with explicit conditions.

---

## 2. Win Themes

1. **Pre-built compliance and security depth** — BOLA ownership-verification middleware, GDPR data-pipeline design, and EU AI Act responsible-AI artefacts are already documented (M900/M400); competitors start from scratch on these, we start from a tested baseline.

2. **Named architecture-spike methodology** — our C4-driven integration approach with explicit ADRs and pre-mortem (M400) means the spike produces a decision artefact the client can audit, not just a verbal assurance; this directly addresses MRG's binding feasibility gate.

3. **AI-native delivery with measurable maturity evidence** — we commit to per-phase L1–L3 maturity targets with denominated metrics and documented version-controlled artefacts (M500/M600/M700), not "we'll use AI" — a claim no other bidder at this stage will back with evidence.

---

## 3. Deal-Breaker

**Architecture spike must confirm ≤12-month, ≤€4.1M integration** — if the spike (3 representative country stacks, 4 weeks) shows that full 22-system integration requires >12 months or >€4.1M one-time cost, the pessimistic ROI scenario breaks beyond executive tolerance and the deal should be declined before the full proposal is priced.

*This deal-breaker is already the client's stated no-go line (M100 §9). Naming it in our bid signals we have read and accepted the same constraint — and that we will not bid optimistically past it.*

---

## 4. Top-Three Risks

| # | Risk | Likelihood (1–5) | Impact (1–5) | Active mitigation |
|---|---|---|---|---|
| R1 | 22-system integration complexity exceeds spike estimate — hidden API inconsistencies or undocumented country variants inflate timeline and cost beyond envelope | 3 | 5 | Contractual spike gate: no full-build commitment until spike confirms scope; fixed-price only after spike results |
| R2 | Cancellation rate baseline unverified — ROI hypothesis (≥30% reduction) built on 15% sector figure with no client OMS confirmation; actual rate may be ≤5%, invalidating the value case | 4 | 4 | Require client OMS data as week-1 deliverable; include falsification clause in contract (stop trigger if actual rate ≤5%) |
| R3 | GDPR cross-border stock data flows — 22-jurisdiction data residency rules may require per-country DPA addenda that delay architecture decisions and increase legal cost | 3 | 3 | Phase 1 legal review as a named deliverable; DPO engaged from kick-off; data-residency map produced in spike window |

---

## 5. Recommendation

**Bid with conditions.**

The opportunity is strategically strong, technically well-matched, and commercially attractive at the base case. Two conditions must be met before the full proposal is priced and submitted:

1. **Spike gate commitment** — the proposal is structured as a two-stage contract: fixed-fee architecture spike (4 weeks, capped cost), then a go/no-go before the full-build price is locked. We do not submit a fixed-price full-build estimate without spike results.

2. **OMS data by proposal defence** — MRG provides actual C&C cancellation rate and revenue base from their OMS before the oral presentation (2026-10-03). If actual cancellation rate is ≤5%, we revise the value hypothesis or withdraw.

If both conditions are met at bid defence, proceed to full proposal. If either is blocked, no-bid.

---

## 6. Competitive Context

| Competitor | Win theme they will pitch to MRG | Why the buyer will find it compelling |
|---|---|---|
| Accenture / large global SI | "We have delivered SAP omnichannel integration at this scale across 20+ countries — here are three named retail clients and the go-live dates. No other bidder can show you that track record." | MRG's Head of Omnichannel has one shot at this; a named reference at scale removes the biggest delivery fear and justifies a higher price tag in the steering committee |
| iO / mid-market EU digital consultancy | "We are EU-native, GDPR-fluent, and we will staff this with senior people — not offshore juniors. Our day-rate is 30% lower than the global SIs and you will always know who is on your account." | MRG is cost-pressured and has had bad experiences with large-SI bait-and-switch staffing; a lean, named, local team speaks directly to that scar tissue |
