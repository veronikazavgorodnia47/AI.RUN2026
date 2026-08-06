# IaC PR Gate Report — `cart-api` deployment manifest

**PR diff source:** `800-infra-oper/iac-pr.diff`  
**Evidence base:** `02-deploy-manifest.md` (8-gap audit) + `03-ci-workflow.md` (6-control supply-chain audit)  
**Reviewer:** Ops agent (read-only — no `kubectl apply` / `terraform apply`)  
**Date:** 2026-08-06

---

## Verdict: BLOCK

**5 of 8 manifest gaps remain open. 2 are production blockers.**  
This PR must not be merged until Gap 3 (plaintext credentials) and Gap 5 (mutable image tag) are resolved.

---

## Manifest gap audit (source: `02-deploy-manifest.md`)

| # | Control | PR status | Finding | Required action |
|---|---|---|---|---|
| 1 | **Resource requests/limits** | ✅ FIXED | PR adds `resources.requests` + `resources.limits` (memory 512Mi, cpu 500m) — matches the one-line fix from the audit | No further action |
| 2 | **Readiness probe** | ✅ FIXED | PR adds `readinessProbe` on `/healthz` with `initialDelaySeconds: 5, periodSeconds: 10` — exact match to audit recommendation | No further action |
| 3 | **Secret handling** | 🔴 BLOCKER — OPEN | `DATABASE_URL` and `DIAL_API_KEY` remain as `env.value` plaintext strings in the diff (lines unchanged). `DIAL_API_KEY: sk-dial-abc123secretkey` is visible in the PR diff. | Replace both with `env.valueFrom.secretKeyRef` pointing to a Kubernetes Secret. This is also a **security incident** if this diff has been posted to a shared repo, CI log, or Slack thread — credential rotation may be required independently of this PR. |
| 4 | **Rollback strategy** | ✅ FIXED | PR adds `strategy: {type: RollingUpdate, maxUnavailable: 0, maxSurge: 1}` — zero-downtime roll, clean `kubectl rollout undo` path | No further action |
| 5 | **Image tag** | 🔴 BLOCKER — OPEN | Image line `registry.meridian.internal/cart-api:latest` is unchanged. PR comment confirms: "NOT changed in this PR." `kubectl rollout undo` will re-pull `:latest`, not the prior binary. | Pin to an immutable tag: `registry.meridian.internal/cart-api:v<semver>` or `@sha256:<digest>`. Required before this manifest is used in any rollback scenario. |
| 6 | **PodDisruptionBudget** | ⚠️ NOT ADDRESSED | No PDB added. A node drain can evict all 3 pods simultaneously if the scheduler co-located them. | Create `PodDisruptionBudget` with `minAvailable: 2` in the `meridian` namespace. Non-blocking for this PR if Gap 3 + 5 are fixed first, but required before any planned node maintenance. |
| 7 | **Security context** | ✅ FIXED | PR adds `securityContext: {runAsNonRoot: true, runAsUser: 1000, readOnlyRootFilesystem: true}` — matches audit recommendation | No further action |
| 8 | **Pod anti-affinity** | ⚠️ NOT ADDRESSED | No `affinity` or `topologySpreadConstraints` added. All 3 replicas can still land on one node. | Add `topologySpreadConstraints: maxSkew: 1` on `kubernetes.io/hostname`. Non-blocking for this PR but required before the "3 replicas = HA" claim can be made. |

---

## Supply-chain control audit (source: `03-ci-workflow.md`)

The PR diff covers only the deployment manifest. The CI/CD workflow (`03-ci-workflow.md`) was **not changed** by this PR. All 6 supply-chain gaps remain open in the pipeline.

| # | Control | Status | Severity |
|---|---|---|---|
| 1 | Pinned action versions | ❌ OPEN (not in this PR's scope) | Medium |
| 2 | OIDC short-lived credentials | ❌ OPEN — `KUBECONFIG` long-lived secret remains | **High** |
| 3 | Image signing / provenance | ❌ OPEN | Medium |
| 4 | Dependency + image scanning | ⚠️ PARTIAL (Snyk only, no image scan) | Medium |
| 5 | Least-privilege token scope | ❌ OPEN — no `permissions` block | Medium |
| 6 | Rollback gate | ❌ OPEN — no `kubectl rollout status` check | **High** |

**Note:** Gap 2 (long-lived `KUBECONFIG`) means that even with a correctly tagged image in the manifest, the deploy pipeline can be used to push an arbitrary image to production using a stolen secret. This should be tracked as a separate PR/ticket, not deferred.

---

## Gate summary

| Category | Gaps fixed by this PR | Gaps remaining |
|---|---|---|
| Manifest (8 gaps) | 4 of 8 (Gaps 1, 2, 4, 7) | 4 of 8 (Gaps 3🔴, 5🔴, 6⚠️, 8⚠️) |
| Supply-chain (6 controls) | 0 of 6 | 6 of 6 (out of scope for this PR) |

**Merge condition:** resolve Gap 3 (credential rotation + secretKeyRef) and Gap 5 (pin image tag to SHA) before merge. Gaps 6 and 8 must be tracked in the backlog with owners named before the next planned maintenance window.

---

## Escalation boundary

This gate report is read-only. The following require human approval:

| Action | Owner |
|---|---|
| Merge this PR | PR reviewer + eng lead |
| Rotate `DIAL_API_KEY` / `DATABASE_URL` | Secrets owner / security team |
| `terraform apply` for PDB or RBAC changes | Ops team + signed change management |
| Update DIAL gateway policy (cost cap or token scope) | Ops + Checkout P&L owner |
