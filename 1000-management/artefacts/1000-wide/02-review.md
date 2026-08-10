---
kata: 10.W.3
review-type: fresh-session adversarial (sceptical bid-review director)
date: 2026-08-10
patch-applied: Critique 2 (DPA gap uncosted + ML training data GDPR contradiction)
---

# Adversarial Review — 02-solution.md

*Conducted in a fresh session with no prior context. Prompt:*

> You are a sceptical bid-review director. Attack this solution outline. Name the 3
> sharpest concerns — phase boundaries with hidden scope, governance the sub-vendor will
> exploit, assumptions the client will dispute. No praise.

---

## Critique 1 — Phase 1 is a self-certified green light into €4.1M

The Phase 1 exit criterion reads: "ADR published confirming 22-system integration is
achievable ≤12 months and ≤€4.1M." That ADR is authored by the engagement's own
Architecture Lead and countersigned by MRG's Head of Engineering — who is reviewing
a document written by the team asking to be hired. There is no independent technical
estimator, no client-side SME review of the ADR methodology, and no mechanism for MRG
to challenge the cost estimate. The fixed-fee spike is positioned as low-risk optionality,
but its only output is a document the vendor controls. If the Architecture Lead has any
incentive to find the project achievable, the gate is structureless.

**What a buyer will hear at bid defence:** "You're asking us to authorise a multi-million
full-build based on an ADR your own team wrote. Who independently validates the estimate?"

**Status:** Accepted — open item for proposal assembly. Mitigation to add: Phase 1 exit
review includes an independent cost-estimator review (MRG internal or third-party) of the
ADR's integration assumptions before the go/no-go is signed. Added to open-items log in
`07-proposal-pack.md`.

---

## Critique 2 — The ≥18/22 DPA gap is uncosted scope hiding in plain sight (WEAKEST — PATCHED)

Phase 2 exits with ≥18 of 22 DPA addenda signed; Phase 4 requires all 22. The four-country
gap has no budget line, no fixed Bird & Bird deliverable, and no defined owner beyond
"Bird & Bird on retainer." The escalation path names MRG's Head of Omnichannel as
decision-maker — but says nothing about who funds the additional Bird & Bird time, who
absorbs the delayed-country integration work, or whether Phase 4 budget accounts for it.
Those four countries will arrive as a change request at the Phase 3–4 boundary, when the
full team is already deployed.

**Deeper problem:** Assumption A2 requires ≥90 days of SAP + POS data from all countries
by Phase 3 start. The document never addresses whether training data from unsigned-DPA
countries can legally be used. If it cannot, the ML training set has systematic country
gaps that degrade model accuracy for those markets. If it can, that is a potential GDPR
violation. This contradiction sits unresolved between §3 and §4.

**Patch applied (see 02-solution.md §4 A2 and §3):**
- A2 now explicitly states that training data from countries without a signed DPA addendum
  is excluded from the ML training set until the addendum is signed. Model accuracy
  implications for excluded countries are flagged in Phase 3 kick-off.
- Phase 2 budget provision added: Bird & Bird late-completion retainer (estimated 4-country
  tail) is a named line item in `04-estimate.xlsx`, not absorbed in contingency silently.
- Phase 4 exit criterion updated to require a named resolution for each of the ≤4 unsigned
  countries — either signed, excluded from go-live scope, or escalated to MRG General
  Counsel with a documented risk acceptance.

---

## Critique 3 — EU AI Act reclassification is an existential schedule risk presented as a footnote

Assumption A4 classifies the confidence scorer as Limited Risk (Article 52). This is
disputed on its face: the scorer feeds a store associate operational dashboard used to make
staffing and fulfilment decisions, and directly influences consumer access to goods at
checkout. Both vectors — employment/work management (Annex III, Article 6) and consumer
access to goods and services — are categories EU regulators have flagged for High Risk
scrutiny.

The document states "≥6 weeks timeline impact" if reclassified. A genuine High Risk
conformity assessment under Article 9 requires a full technical documentation package,
a fundamental rights impact assessment, a human oversight architecture, and a notified
body or internal review process. Six weeks is not a conformity assessment; it is the time
needed to assemble the documentation checklist. Realistic impact: 12–20 weeks, potentially
collapsing the Phase 4 schedule entirely.

**What a buyer will hear at bid defence:** "Your DPO thinks this might be High Risk. You've
written '6 weeks' in a footnote. That is not a risk plan."

**Status:** Accepted — timeline impact corrected to 12–20 weeks in A4; EU AI Act
preliminary Annex III / Article 6 analysis added as a pre-submission deliverable (before
oral presentation, not Phase 3). Added to open-items log in `07-proposal-pack.md`.
