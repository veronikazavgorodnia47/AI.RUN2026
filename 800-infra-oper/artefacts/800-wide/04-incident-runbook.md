# K 8.W.4 — Incident diagnosis + runbook: `cart-api` OOMKilled

**Reference case:** Meridian Retail Group — Case A

---

## Incident

**Symptom:** Half of `cart-api`'s pods are in `CrashLoopBackOff`. Events show `OOMKilled`. Crash started 20 minutes after a deploy that added the AI summarise step. Error rate is climbing; latency on healthy pods is rising as they absorb the load.

**Evidence available:** incident symptoms + deployment manifest from K 8.W.2 (no `resources` block on the container — Gap 1 from the audit).

---

## Three ranked hypotheses

### H1 — No memory limit + memory-heavy AI step (most likely)

**Evidence:**
- Manifest has no `resources.limits` or `resources.requests` (Gap 1, K 8.W.2 audit).
- `OOMKilled` means the container exceeded the node's available memory — Linux killed it.
- The crash appeared exactly 20 minutes after adding the AI summarise step, which adds a large prompt (system context + full cart contents) + model response to in-process memory per request.
- Healthy pods are now receiving redirected traffic — they will hit the same wall.

**Cheapest next step:** `kubectl describe pod <crashing-pod-name> -n meridian` — confirms `OOMKilled` in events and shows the last memory reading at crash time. No access needed beyond read on the namespace.

---

### H2 — Memory leak in the new summarise code

**Evidence:**
- Timing correlates with the new code path (20-minute delay suggests gradual accumulation, not an instant spike).
- Without resource limits, a slow leak and a legitimate high-usage step look identical until profiled.

**Cheapest next step:** `kubectl top pods -n meridian` — if memory is growing steadily across all pods (not just the ones handling the AI step), a leak is more likely than a per-request spike. Requires `metrics-server` installed.

---

### H3 — Thundering herd on the summarise endpoint at deploy time

**Evidence:**
- New feature launched to all users simultaneously; users who had carts waiting may have triggered the summarise button all at once.
- 3,000,000 AI calls/month ≈ 1.4/second average, but a launch spike could be 10–100×.
- Weaker hypothesis: `OOMKilled` is per-pod, not a latency/timeout signal — thundering herd usually shows as latency first.

**Cheapest next step:** Check observability stack for a request-rate spike on `/summarise` in the 20-minute window post-deploy. If flat, discard H3.

---

## Immediate mitigation

**Roll back the deploy:**
```bash
kubectl rollout undo deployment/cart-api -n meridian
```
This restores the pre-summarise version instantly (provided the image is pinned — if `:latest` was used, see K 8.W.3 Gap 8). Owned by **L2**.

Verify:
```bash
kubectl rollout status deployment/cart-api -n meridian
kubectl get pods -n meridian
```

---

## Durable fix

1. **Set resource limits** — the gap K 8.W.2 flagged. Profile memory use of the summarise step first:
   ```yaml
   resources:
     requests:
       memory: "256Mi"
       cpu: "250m"
     limits:
       memory: "512Mi"
       cpu: "500m"
   ```
2. **Add readiness probe** — ensures traffic only reaches pods that have warmed up, preventing load redistribution onto struggling pods.
3. **Pin the image tag** — so `kubectl rollout undo` actually restores the previous binary (K 8.W.3 Gap 8).

Owned by **L2** (limits + probe) and **L3** (profiling + code review of the summarise step if memory usage exceeds expected bounds).

---

## Reusable runbook entry

| Field | Content |
|---|---|
| **Detection signal** | Alert: `CrashLoopBackOff` on any `cart-api` pod AND `OOMKilled` in pod events (Kubernetes event exporter → alerting stack). Also: error rate > 5% on `cart-api` for > 2 minutes. |
| **Diagnosis steps** | 1. `kubectl describe pod <pod> -n meridian` — confirm `OOMKilled` + last memory reading. 2. `kubectl top pods -n meridian` — check if memory is growing (leak) or stable-high (limit too low). 3. Check observability for request-rate spike on `/summarise` at time of first crash. |
| **Fix** | If resource limit missing or too low: patch manifest with appropriate `resources.limits.memory`, re-deploy. If memory leak confirmed: roll back and open L3 ticket for code fix. |
| **Rollback** | `kubectl rollout undo deployment/cart-api -n meridian` — restores previous version in < 60 seconds. Verify with `kubectl rollout status`. Note: only reliable if image is pinned to a SHA, not `:latest`. |
| **Owning support tier** | **L2** owns detection, rollback, and manifest fix. **L3** owns root-cause investigation if memory usage exceeds expected bounds after limits are set (potential leak in AI step). |
