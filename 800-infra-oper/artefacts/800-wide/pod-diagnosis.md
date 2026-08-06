# Pod diagnosis — `cart-api` OOMKilled

**Service:** `cart-api` · **Namespace:** `meridian`  
**Signal source:** `cluster-state/failure-1/describe.txt` + `cluster-state/failure-1/logs.txt`  
**Date:** 2026-08-06

---

## Observed symptoms (from seed files)

| Source | Evidence |
|---|---|
| `describe.txt` line `Last State: Terminated / Reason: OOMKilled / Exit Code: 137` | Pod terminated by the Linux OOM killer — process exceeded available node memory |
| `describe.txt` line `Restart Count: 4` | Pod has crashed and restarted 4 times in ~20 minutes |
| `describe.txt` lines `Limits: <none> / Requests: <none>` | No `resources` block on the container — scheduler placed the pod with no memory ceiling |
| `describe.txt` event `Warning OOMKilled 2m (x4 over 20m)` | First crash ~20 minutes ago — timing aligns with the AI summarise deploy |
| `logs.txt` lines `WARN heap growing: 402MB … 501MB … 547MB` | Heap grows steadily over the last 7 seconds before signal:killed — not a single spike |
| `logs.txt` multiple `POST /cart/summarise tokens_in=1184–1512` | Concurrent summarise requests, each holding a large prompt in memory simultaneously |

---

## Three ranked hypotheses

### H1 — No memory limit + AI step memory spike per request
**Confidence: HIGH**

**Reasoning:** `describe.txt` confirms `Limits: <none>` — the container has no memory ceiling (Gap 1, `02-deploy-manifest.md` audit). The AI summarise step adds a system prompt + full cart contents (~1,200 tokens) + model response to in-process memory for every concurrent request. With no limit, once concurrent requests accumulate enough heap, Linux kills the process at the node level.

**Evidence chain:**
- `describe.txt`: `Limits: <none>` → no ceiling
- `logs.txt`: 9 concurrent summarise calls, each holding ~1,200-token prompt objects
- `logs.txt`: `heap growing: 402MB → 501MB → 547MB` over 7 s → steady growth under concurrent load
- `describe.txt` event: first OOMKilled ~20 m after deploy adding AI step

**Read-only next command:**
```bash
kubectl describe pod cart-api-7d9b6b7c9-xk2p8 -n meridian
```
Confirms `Limits: <none>` and shows the memory reading at the moment of last crash (in `Last State` block). No write access required beyond `get`/`describe` on the namespace.

---

### H2 — Memory leak in the new summarise code
**Confidence: MEDIUM**

**Reasoning:** The 20-minute delay between deploy and first crash (not immediate) is consistent with gradual memory accumulation rather than a single-request spike. Without resource limits, a slow leak and legitimate high-usage are indistinguishable without profiling.

**Evidence:** `logs.txt` shows heap growing across successive requests (`402MB → 501MB → 547MB`), but this could be either accumulation from held references (leak) or concurrent in-flight requests that haven't been GC'd yet. Cannot distinguish from logs alone.

**Read-only next command:**
```bash
kubectl top pods -n meridian
```
If all pods (not just the one handling AI calls) show steadily increasing memory across their uptime, a leak is more likely than a per-request ceiling breach. Requires `metrics-server` to be installed in the cluster.

---

### H3 — Thundering herd on the summarise endpoint at launch
**Confidence: LOW**

**Reasoning:** New feature released to all users simultaneously — users with existing carts may have triggered summarise all at once, creating a short burst far above the 1.4 calls/second average (3M/month). However: `OOMKilled` (exit code 137) is a per-pod memory signal, not a latency or timeout signal. A true thundering herd typically surfaces as latency degradation or connection-queue exhaustion first. The `logs.txt` pattern (steady heap growth over 7 s across 9 calls) does not show a sudden spike.

**Evidence against:** logs show 9 requests over ~23 seconds (0.4/s) — below average rate, not a spike. Weakens thundering-herd explanation.

**Read-only next command:**
```bash
# Check observability stack for request-rate on /summarise in the 20-minute post-deploy window
kubectl logs deployment/cart-api -n meridian --since=30m | grep "POST /cart/summarise"
```
If request rate was flat or below average in the window, discard H3. If rate was 10–100× average, H3 becomes plausible.

---

## Recommended confirmation sequence

1. `kubectl describe pod <crashing-pod> -n meridian` → confirm `Limits: <none>` (H1 blocker)
2. `kubectl top pods -n meridian` → memory growth pattern (H1 vs H2)
3. `kubectl logs deployment/cart-api -n meridian --since=30m | grep summarise` → request rate (discard/confirm H3)

**Do not proceed to mitigation until step 1 is confirmed.**

---

## Escalation boundary

**This agent does not act on the following — escalate to the named owner:**

| Action | Escalation path |
|---|---|
| `kubectl rollout undo deployment/cart-api -n meridian` | L2 on-call (runbook `04-incident-runbook.md`) |
| Patch manifest with `resources.limits` | L2 → PR review → CI/CD deploy |
| `kubectl delete pod` / `kubectl apply` | L2 on-call — signed change management |
| SLO redefinition | Human P&L/SRE owner (`slo/slo.md` — currently DRAFT, no owner) |
