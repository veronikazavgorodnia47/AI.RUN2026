# K 8.W.6 — Cloud Operations & Support Pack: `cart-api`

**Reference case:** Meridian Retail Group — Case A  
**Service:** `cart-api` — checkout service with AI "summarise my cart" step  
**Date:** 2026-08-06

---

## Six readiness questions

| # | Question | Answer | Source |
|---|---|---|---|
| 1 | **How does it deploy and roll back?** | Rolling update via GitHub Actions CI/CD (build → test → scan → deploy). Rollback: `kubectl rollout undo deployment/cart-api -n meridian`. **Caveat:** rollback is only reliable if image is pinned to a SHA — currently `:latest` (K 8.W.3 Gap 8, unresolved). | K 8.W.2, K 8.W.3 |
| 2 | **Who gets paged?** | `UNKNOWN — owner needed.` Alert rules exist for CrashLoopBackOff + OOMKilled and error rate > 5%, but no on-call rotation or escalation contact has been defined for `cart-api`. | K 8.W.4 |
| 3 | **What is monitored?** | Observability stack watches all 7 [ops] components (metrics, logs, traces). DIAL gateway adds per-request AI cost + response signal. Pod events alert on `OOMKilled`. **Gap:** no SLO defined; no burn-rate alert. | K 8.W.1, K 8.W.4 |
| 4 | **What does it cost per month, and what is the cap?** | $16,500/month total — $1,500 cloud rent (flat) + $15,000 AI meter (91%, scales with traffic). DIAL hard cap: $18,000/month (Checkout tenant). Alert fires at $12,000. Daily burst alert at $1,200/day. | K 8.W.5 |
| 5 | **What is the kill-switch?** | `UNKNOWN — owner needed.` No feature flag or kill-switch for the AI summarise step has been specified. Disabling the feature currently requires a code change and redeploy. | — |
| 6 | **Which support tier owns the top ticket types?** | OOMKilled / CrashLoopBackOff → **L2** (rollback + resource-limit fix, follows runbook K 8.W.4). Memory leak in summarise step → **L3** (code investigation). AI summarise returning empty/wrong → **L2** (DIAL logs review) escalating to **L3** if model behaviour change. | K 8.W.4 |

---

## Top failure + runbook headline

**Incident:** `OOMKilled` after deploy adding AI summarise step — half of pods in `CrashLoopBackOff`.  
**Root cause:** No `resources.limits` on container (manifest Gap 1) + memory-heavy prompt per call.  
**Mitigation:** `kubectl rollout undo` (< 60 s). **Fix:** set `resources.limits.memory: 512Mi`, add readiness probe, pin image tag.  
**Runbook:** `04-incident-runbook.md` — detection → diagnosis → fix → rollback, owned L2/L3.

---

## L1–L3 support handover

| Ticket type | Resolving tier | Playbook / runbook |
|---|---|---|
| Pod crashes / CrashLoopBackOff | **L2** | `04-incident-runbook.md` — confirm OOMKilled, rollback, patch limits |
| AI summarise step returns empty or wrong output | **L2 → L3** | L2: check DIAL logs for model errors, retry; if systematic, escalate to L3 for prompt/code review |

---

## Maturity gap (EPAM AI SDLC ladder)

| Dimension | Current level | Gap |
|---|---|---|
| AI Capabilities | L2 (assisted) | No ops agents running (autoscaler, cost-guardian, incident commander) |
| Reusability | L2 (shared) | Runbook exists but not in a versioned playbook library; no shared agent specs |
| Performance Tracking | L1→L2 | DIAL cap is being set; cost not yet tracked per-sprint or reviewed regularly |
| AI Champions | UNKNOWN | No designated champion confirmed for this service |
| Daily Active Users | UNKNOWN | Not measured for the ops/support function |

---

## Verdict

**NOT READY to operate and support as-is.**

Two blockers before launch:

1. **No kill-switch** (Question 5 — UNKNOWN). Disabling the AI summarise step requires a code change and redeploy. If the model returns harmful or nonsensical output, there is no fast path to disable the feature without impacting the full service.
2. **Mutable image tag** (`:latest`). `kubectl rollout undo` does not reliably restore the previous binary — a bad deploy cannot be safely reversed until the image is pinned to a SHA.

These two gaps must be resolved before the app is safe to hand to an on-call rotation.
