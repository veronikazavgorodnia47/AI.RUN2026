---
kata: 10.W.4
consumes: 02-solution.md, 10.W.4.draft.md (diagnosed + repaired)
date: 2026-08-10
note: Markdown stand-in for 03-staffing.xlsx — three variant tabs below
---

# Staffing Variants — Meridian Unified ATP System

## Diagnosis of provided draft

All three variants in the draft share the same failure: they differ only in headcount,
not in cost/speed/risk bet. Specific defects found:

| Defect | Detail |
|---|---|
| Identical role mix scaled by headcount | Lean/Balanced/Fast all use the same roles at the same proportions — no variant shifts the mix toward cheaper off-shore delivery or more senior on-shore acceleration |
| 100% on-shore across all three | No blended delivery model; "lean" with 100% on-shore is not lean — it is expensive |
| Month-1 full productivity | Nobody ramps in a day; a plan that assumes 100% utilisation from month 1 will miss its first sprint velocity target |
| "Pick Balanced — it's the middle option" | Not a recommendation; it is the absence of a recommendation |

---

## Repaired Variants

Phases from `02-solution.md`:
- **Phase 1 — Spike** (4 weeks / ~1 month)
- **Phase 2 — Foundation & Integration** (months 1–4)
- **Phase 3 — AI Predictor & Shopper UI** (months 4–8)
- **Phase 4 — Hardening & Go-Live** (months 8–12)

Ramp profile applied to all variants: 30% / 60% / 100% over months 1–3 of each phase
(a common planning heuristic — adjust to actual team data when available).

---

### Tab 1 — Lean

**Bet:** Minimise monthly cost by shifting integration and QA work off-shore and
accepting a slower ramp. Right when MRG's budget ceiling matters more than
time-to-market and the client can absorb higher coordination overhead.

**On / near / off-shore split: 15% / 25% / 60%**
Timeline impact: go-live pushed ~4 weeks vs. Balanced due to coordination latency.

| Role | Level | Shore | Spike | P2 M1 | P2 M2 | P2 M3 | P2 M4 | P3 M5 | P3 M6 | P3 M7 | P3 M8 | P4 M9 | P4 M10 | P4 M11 | P4 M12 | FTE-months |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Delivery Lead | Senior | On | 0.5 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 0.5 | 12.0 |
| Architecture Lead | Senior | On | 1 | 1 | 1 | 1 | 0.5 | 0.5 | 0.5 | 0.5 | 0.5 | 0.5 | 0.5 | 0.5 | 0.5 | 9.0 |
| Integration Engineers (×3) | Mid | Off | 0 | 0.9 | 1.8 | 3 | 3 | 1 | 1 | 1 | 1 | 1 | 1 | 0.5 | 0 | 15.2 |
| ML Lead | Senior | Near | 0 | 0 | 0 | 0 | 0.5 | 0.5 | 1 | 1 | 1 | 1 | 1 | 1 | 0.5 | 7.5 |
| ML Engineer (×1) | Mid | Near | 0 | 0 | 0 | 0 | 0 | 0.3 | 0.6 | 1 | 1 | 1 | 1 | 1 | 0.5 | 6.4 |
| UX/UI Engineer | Mid | Near | 0 | 0 | 0.3 | 0.6 | 1 | 1 | 1 | 1 | 0.5 | 0 | 0 | 0 | 0 | 5.4 |
| QA Engineers (×2) | Mid | Off | 0 | 0.3 | 0.6 | 2 | 2 | 0.6 | 1.2 | 2 | 2 | 2 | 2 | 2 | 1 | 19.7 |
| DevOps / Platform | Mid | Off | 0 | 0.3 | 0.6 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 10.9 |
| BA | Mid | Near | 0.5 | 0.3 | 0.6 | 1 | 1 | 1 | 1 | 0.5 | 0.5 | 0 | 0 | 0 | 0 | 6.4 |
| **Total** | | | **2.0** | **3.8** | **5.9** | **10.6** | **10.0** | **6.9** | **8.3** | **9.0** | **8.5** | **7.5** | **7.5** | **6.5** | **4.0** | **~92** |

**Recommendation note:** go-live pushed ~4 weeks vs. Balanced; risk of integration quality
issues in Phase 2 due to off-shore coordination latency on 22-country API complexity.

---

### Tab 2 — Balanced

**Bet:** Predictable delivery at mid-range cost. Near/off-shore for implementation;
on-shore for architecture and client-facing roles. Right when the 12-month timeline is
firm but MRG cannot absorb the premium of the Fast variant.

**On / near / off-shore split: 25% / 45% / 30%**

| Role | Level | Shore | Spike | P2 M1 | P2 M2 | P2 M3 | P2 M4 | P3 M5 | P3 M6 | P3 M7 | P3 M8 | P4 M9 | P4 M10 | P4 M11 | P4 M12 | FTE-months |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Delivery Lead | Senior | On | 0.5 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 0.5 | 12.0 |
| Architecture Lead | Senior | On | 1 | 1 | 1 | 1 | 1 | 0.5 | 0.5 | 0.5 | 0.5 | 0.5 | 0.5 | 0.5 | 0.5 | 9.5 |
| Integration Engineers (×4) | Mid | Near/Off | 0 | 1.2 | 2.4 | 4 | 4 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 0 | 18.6 |
| ML Lead | Senior | Near | 0 | 0 | 0 | 0.5 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 0.5 | 9.0 |
| ML Engineers (×2) | Mid | Near | 0 | 0 | 0 | 0.3 | 0.6 | 0.6 | 1.2 | 2 | 2 | 2 | 2 | 1 | 0.5 | 12.2 |
| UX/UI Engineer | Mid | Near | 0 | 0.3 | 0.6 | 1 | 1 | 1 | 1 | 1 | 0.5 | 0 | 0 | 0 | 0 | 6.4 |
| QA Engineers (×3) | Mid | Off | 0 | 0.3 | 0.9 | 3 | 3 | 0.9 | 1.8 | 3 | 3 | 3 | 3 | 2 | 1 | 25.9 |
| DevOps / Platform | Senior | On | 0 | 0.3 | 0.6 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 10.9 |
| BA | Mid | Near | 0.5 | 0.3 | 0.6 | 1 | 1 | 1 | 1 | 0.5 | 0.5 | 0 | 0 | 0 | 0 | 6.4 |
| **Total** | | | **2.0** | **4.4** | **7.1** | **12.8** | **13.6** | **8.0** | **9.5** | **11.0** | **10.5** | **9.5** | **9.5** | **7.5** | **4.0** | **~111** |

---

### Tab 3 — Fast

**Bet:** Accelerate by running Phase 2 integration and Phase 3 AI predictor workstreams
in parallel from month 3, and by loading senior on-shore capacity earlier. Higher monthly
burn and higher coordination risk. Right when the 12-month window is a hard commercial
deadline and MRG can absorb cost overrun but not a late go-live.

**On / near / off-shore split: 45% / 35% / 20%**
Timeline impact: parallel workstreams from month 3 bring go-live 3–4 weeks earlier vs.
Balanced, but require a named integration lead per workstream to avoid merge conflicts at
the Phase 3–4 boundary.

| Role | Level | Shore | Spike | P2 M1 | P2 M2 | P2/P3 M3 | P2/P3 M4 | P3 M5 | P3 M6 | P3 M7 | P3 M8 | P4 M9 | P4 M10 | P4 M11 | P4 M12 | FTE-months |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Delivery Lead | Senior | On | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 0.5 | 12.5 |
| Architecture Lead | Senior | On | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 0.5 | 0.5 | 0.5 | 0.5 | 0.5 | 10.5 |
| Integration Engineers (×5) | Senior/Mid | On/Near | 0 | 1.5 | 3 | 5 | 5 | 2 | 1 | 1 | 1 | 1 | 1 | 0.5 | 0 | 22.0 |
| ML Lead | Senior | On | 0 | 0 | 0.5 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 0.5 | 10.0 |
| ML Engineers (×2) | Mid | Near | 0 | 0 | 0.3 | 0.6 | 1.2 | 1.2 | 2 | 2 | 2 | 2 | 1 | 0.5 | 0 | 12.8 |
| UX/UI Engineer | Senior | On | 0 | 0.5 | 1 | 1 | 1 | 1 | 1 | 1 | 0.5 | 0 | 0 | 0 | 0 | 7.0 |
| QA Engineers (×3) | Senior | On/Near | 0 | 0.5 | 1.5 | 3 | 3 | 1.5 | 2 | 3 | 3 | 3 | 3 | 2 | 1 | 27.5 |
| DevOps / Platform (×2) | Senior | On | 0 | 0.6 | 1.2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 1.5 | 1 | 20.3 |
| BA | Senior | On | 0.5 | 0.5 | 1 | 1 | 1 | 1 | 1 | 0.5 | 0.5 | 0 | 0 | 0 | 0 | 7.0 |
| **Total** | | | **2.5** | **5.6** | **10.5** | **15.6** | **16.2** | **11.7** | **12.0** | **13.0** | **11.5** | **10.5** | **9.5** | **7.0** | **3.5** | **~130** |

---

### Tab 4 — Recommendation

**Recommend: Balanced.**

**Rationale:** The 12-month timeline is achievable with the Balanced variant without
parallel workstreams, which the Meridian internal team (Lena Park's junior ops team)
is not sized to govern across two simultaneous front-ends. Fast saves 3–4 weeks but
adds coordination risk at the Phase 2/3 boundary that would more likely extend than
compress the schedule. Lean's 60% off-shore integration team is a mismatch for 22-country
API complexity where undocumented country variants will require on-the-spot senior
judgement in Phase 2.

Balanced becomes Fast if: (a) Phase 1 spike reveals the integration is simpler than
expected (fewer than 5 distinct API patterns), or (b) MRG confirms a hard go-live
deadline that cannot move. Balanced becomes Lean if: the architecture spike reveals
the budget envelope is under pressure (e.g., Phase 1 exits with a revised one-time
cost estimate above €3.5M for contingency headroom).

| | Lean | Balanced | Fast |
|---|---|---|---|
| Total FTE-months | ~92 | ~111 | ~130 |
| On/near/off | 15/25/60 | 25/45/30 | 45/35/20 |
| Go-live vs. plan | +4 weeks | On plan | −3–4 weeks |
| Key risk | Integration quality, coordination latency | Phase 3–4 DPA tail | Parallel workstream merge, senior burn rate |
| Switch trigger | Budget >€3.5M revised in spike | Default | Hard go-live deadline confirmed |
