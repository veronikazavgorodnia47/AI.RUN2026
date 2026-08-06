# Agent bounds — `cart-api` AI summarise step

**Agent role:** AI summarise step inside `cart-api` — calls EPAM DIAL gateway to produce a natural-language cart summary on user request  
**Source:** `05-cost-estimate.md`, `03-ci-workflow.md` (Gap 2 — retry not capped), `04-incident-runbook.md` (OOMKilled root cause)  
**Date:** 2026-08-06

---

## Runtime bounds (all values: number + unit)

| Bound | Value | Unit | Rationale |
|---|---|---|---|
| `retry_cap` | ≤ 4 | retries per request | Without a cap, a DIAL timeout loop re-queues the same call indefinitely — K 8.W.3 Gap 2. 4 retries provides resilience against transient network failures while bounding worst-case token spend at 5× the nominal call cost. |
| `retry_cooldown` | ≥ 30 | seconds between retries | Exponential backoff with a 30 s floor prevents thundering-herd retry storms. Shorter cooldowns compound the OOMKilled scenario: retries pile up, each holding a prompt object in heap. |
| `timeout_per_call` | ≤ 10 | seconds | Covers model response time at p95 for a 1,200-token input + 200-token output call. A hung call beyond 10 s must be aborted — not retried without the cooldown. |
| `token_budget_input` | ≤ 1,500 | tokens per call | Based on observed maximum (1,512 tokens in `logs.txt`). A hard ceiling prevents a malformed cart from inflating the AI meter and contributing to memory pressure. |
| `token_budget_output` | ≤ 250 | tokens per call | Cart summaries are short natural-language descriptions. 250 tokens = ~180 words — sufficient for any cart. Enforced at the DIAL layer via `max_tokens` parameter. |
| `max_concurrent_calls` | ≤ 10 | per pod instance | At 512 Mi memory limit (Gap 1 fix) and ~50 Mi per in-flight prompt object, 10 concurrent calls = ~500 Mi — within the limit with 12 Mi headroom. Exceeding 10 risks OOMKilled recurrence under burst load. |
| `memory_limit_container` | ≤ 512 | Mi | Set in deployment manifest `resources.limits.memory` (required fix from Gate 1, `gate-report.md`). This is the ceiling enforced by the Kubernetes node — must be in place before any agent-bound reasoning about call concurrency holds. |
| `cost_cap_monthly` | ≤ 18,000 | USD / month | DIAL hard cap at the Checkout tenant level. Requests above this threshold are hard-refused. Source: `05-cost-estimate.md`. |
| `cost_alert_monthly` | 12,000 | USD / month | DIAL alert threshold — 80% of expected meter. Pages the Checkout feature team budget owner. Does not block calls. |
| `cost_cap_daily_burst` | ≤ 600 | USD / day | Equivalent of the $18,000/month cap spread across 30 days. A single day exceeding $1,200 (2× the daily equivalent) pages the budget owner — indicates a loop, not traffic growth. |

---

## Bound-to-incident mapping

| Incident risk | Bound that mitigates it | Source evidence |
|---|---|---|
| OOMKilled from concurrent AI calls | `max_concurrent_calls ≤ 10`, `memory_limit_container ≤ 512 Mi` | `describe.txt` (Limits: <none>), `logs.txt` (heap growing) |
| Runaway retry loop inflating meter 2–4× | `retry_cap ≤ 4`, `retry_cooldown ≥ 30 s` | `03-ci-workflow.md` Gap 2 — no retry cap in CI pipeline |
| Hung call blocking pod memory indefinitely | `timeout_per_call ≤ 10 s` | Standard DIAL p95 call latency target |
| Oversized prompt inflating memory + cost | `token_budget_input ≤ 1,500 tokens` | `logs.txt` max observed: 1,512 tokens |
| Daily cost spike indicating a loop | `cost_cap_daily_burst ≤ 600 USD/day` (page at $1,200) | `05-cost-estimate.md` burst detection rationale |

---

## What this agent does not decide

The following require human approval — this spec documents bounds, not authority:

| Decision | Owner |
|---|---|
| Raising `retry_cap` above 4 | Checkout eng lead + ops review |
| Raising `cost_cap_monthly` above $18,000 | Checkout P&L owner + ops team |
| Raising `max_concurrent_calls` above 10 | Ops + profiling evidence (must revalidate memory model) |
| Changing `memory_limit_container` | L2/L3 + PR review + CI/CD deploy |
| Adjusting DIAL gateway policy (tenant scope, routing) | Ops team — never via this agent |

---

## Pre-launch checklist (bounds in effect check)

| # | Check | Status |
|---|---|---|
| 1 | `resources.limits.memory: 512Mi` present in manifest | ❌ Blocked — Gap 5 (mutable image tag) blocks reliable deploy; Gap 3 (plaintext secrets) is a security blocker. See `gate-report.md`. |
| 2 | DIAL hard cap set to $18,000/month at Checkout tenant | Pending human action — Checkout P&L owner must configure in DIAL console |
| 3 | `retry_cap` enforced in application code | Pending — K 8.W.3 Gap 2 (no retry cap in CI); code fix required |
| 4 | Kill-switch / feature flag for AI summarise step | ❌ UNKNOWN — K 8.W.6 Question 5 gap; no kill-switch defined |
| 5 | `timeout_per_call` configured in DIAL client | Pending verification against application code |

**None of these checks are performed by this agent. Each requires a human owner to verify and sign off.**
