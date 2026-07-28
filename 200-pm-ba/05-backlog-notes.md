---
consumes_from: 04-stories-acs.md
date: 2026-07-28
---

## RICE scoring assumptions

| Parameter | Definition used |
|---|---|
| Reach | Estimated unique C&C shoppers per month affected by this story, relative to ~10,000 monthly availability-check sessions on a representative Meridian product page. `[unverified — actual session volume needs OMS confirmation]` |
| Impact | 1 minimal / 2 low / 3 medium / 4 high / 5 massive — on phantom-stock cancellation rate or channel trust |
| Confidence | Constrained to {10%, 50%, 80%, 100%}. Reflects how well we understand both reach estimate and impact claim. |
| Effort | Person-weeks for a cross-functional squad (1 FE, 1 BE, 1 data/ML, 0.5 QA). Includes integration, test, and AC review but not discovery. |

---

## AI critique

### Highest-score row — S7 (Reserve despite Uncertain verdict, RICE 6,000)

S7 tops the table because effort is near-zero (non-blocking is the default; you have to actively build a blocker). This is a **scoring artefact, not a delivery signal**. S7 is a guardrail that belongs inside S1's acceptance criteria — specifically the "shopper may still proceed to reserve" clause already written in the Uncertain verdict AC. It should be merged into S1 rather than treated as a standalone story. Carrying it as a separate row inflates its apparent priority and creates a risk that a developer delivers "the reserve button stays visible" as a discrete ticket while the verdict display (S1) slips.

**Decision:** S7 is merged into S1's ACs. It is removed from the delivery backlog as an independent story.

### Lowest-confidence rows — S2 (50%) and S6 (50%)

**S2 — Multi-signal confidence scorer (50% confidence):** The 50% reflects genuine technical uncertainty. Signal data quality across 1,400 stores is unproven. The DPIA for staff scan events (employee personal data) may block one of the five signals. The model needs historical phantom-stock outcome data from the OMS that may not be cleanly labelled. At 21 person-weeks of effort, committing to full delivery without a technical spike is high risk.

**Recommendation:** Run a 2-week signal-availability spike in 3 pilot stores before committing to full build. The spike should confirm: (a) SAP delta and POS data are available at SKU+size+store level, (b) staff scan events can be anonymised within GDPR constraints, (c) sufficient historical phantom-stock labelling exists to train the model. If the spike fails, the fallback is a rules-based heuristic (SAP count + staleness threshold only) — lower precision but shippable.

**S6 — Data freshness indicator (50% confidence):** No user research supports the assumption that shoppers notice or act on freshness cues. The personas show they want a trustworthy verdict, not necessarily transparency about the underlying data pipeline. There is a plausible counter-argument that showing "data as of 2h ago" undermines confidence rather than building it.

**Recommendation:** Defer S6 until post-launch. Use the 90-day precision measurement period to determine whether shoppers who see degraded-mode messages convert differently — that data will answer whether freshness transparency is worth building.

---

## Human override note

The RICE framework ranked S7 #1. The human decision is: **S7 is not a deliverable — it is a constraint embedded in S1.** The actual delivery sequence is:

1. **S2** — Signal integrations + confidence model (dependency for everything else; spike first)
2. **S5** — Size/colour-level scoring (model design already accommodates this; low marginal cost)
3. **S1** — Verdict display UI (depends on S2 being at least partially live)
4. **S4** — Degraded mode (ships with S1 as a launch gate)
5. **S3** — Nearest alternative store (first differentiating feature; requires S1+S2 stable)
6. **S8** — Mobile optimisation (UI polish; can follow S1 in a subsequent sprint)
7. **S6, S9, S10** — Deferred post-launch

The framework produced the ranked list. This note is the decision.
