# K 8.W.2 — Deployment manifest + fresh-session audit: `cart-api`

**Reference case:** Meridian Retail Group — Case A  
**Service shape:** `cart-api` — 3 replicas, ~512Mi memory each, port 8080, `/healthz` endpoint, secrets: `DATABASE_URL`, `DIAL_API_KEY`

---

## Part 1 — Generated manifest (first draft)

Prompt used:
```
Write a Kubernetes Deployment + Service manifest for cart-api from this shape:
cart-api: 3 replicas, ~512Mi memory each, listens on port 8080, has a /healthz
endpoint, needs a DATABASE_URL and a DIAL_API_KEY.
```

```yaml
# cart-api — Deployment (first draft)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: cart-api
  namespace: meridian
spec:
  replicas: 3
  selector:
    matchLabels:
      app: cart-api
  template:
    metadata:
      labels:
        app: cart-api
    spec:
      containers:
        - name: cart-api
          image: meridian/cart-api:latest
          ports:
            - containerPort: 8080
          env:
            - name: DATABASE_URL
              value: "postgres://user:password@postgres:5432/meridian"
            - name: DIAL_API_KEY
              value: "sk-dial-abc123secretkey"
          livenessProbe:
            httpGet:
              path: /healthz
              port: 8080
            initialDelaySeconds: 10
            periodSeconds: 15
---
# cart-api — Service (first draft)
apiVersion: v1
kind: Service
metadata:
  name: cart-api
  namespace: meridian
spec:
  selector:
    app: cart-api
  ports:
    - port: 80
      targetPort: 8080
  type: ClusterIP
```

---

## Part 2 — Fresh-session audit

Prompt used (new session, manifest pasted with no prior context):
```
Audit this manifest for production-readiness. For each gap, name the control,
why it matters, and the one-line fix. Check at least: resource requests/limits,
liveness/readiness probes, rollback strategy, secret handling, replica count.
```

### Audit findings

| # | Control | Gap found | Why it matters | One-line fix |
|---|---|---|---|---|
| 1 | **Resource requests/limits** | No `resources` block on the container | Scheduler places pods blindly; one pod can OOM-kill co-located workloads; HPA has nothing to scale against | `resources: requests: {cpu: "250m", memory: "256Mi"} limits: {cpu: "500m", memory: "512Mi"}` |
| 2 | **Readiness probe** | `livenessProbe` present; `readinessProbe` absent | Kubernetes sends live traffic to pods still warming up or temporarily sick, causing 5xx on every rolling deploy | `readinessProbe: httpGet: {path: /healthz, port: 8080} initialDelaySeconds: 5 periodSeconds: 10` |
| 3 | **Secret handling** | `DATABASE_URL` and `DIAL_API_KEY` are literal plaintext `env.value` strings | Credentials visible in `kubectl get deployment -o yaml`, CI logs, and any copy of this YAML ever committed to Git | Replace both with `env.valueFrom.secretKeyRef` pointing to a Kubernetes Secret object |
| 4 | **Rollback strategy** | No `strategy` field; Kubernetes uses default `maxUnavailable: 25%` | Default can drop below the replica floor under load; no explicit `maxSurge` means a slow roll with no safety floor | `strategy: {type: RollingUpdate, maxUnavailable: 0, maxSurge: 1}` — zero-downtime roll + clean `kubectl rollout undo` |
| 5 | **Image tag** | `image: meridian/cart-api:latest` | `latest` is mutable — `kubectl rollout undo` re-pulls the same tag, not the previous binary | Pin to an immutable tag: `meridian/cart-api:v1.4.2` or `@sha256:…` |
| 6 | **PodDisruptionBudget** | 3 replicas but no PDB | A node drain evicts all pods simultaneously if the scheduler packed them on one node; 0 → 3 outage during routine maintenance | Create `PodDisruptionBudget` with `minAvailable: 2` in the same namespace |
| 7 | **Security context** | No `securityContext` on container or pod spec | Container likely runs as UID 0 (root); writable filesystem; violates least-privilege and most hardening standards | `securityContext: {runAsNonRoot: true, runAsUser: 1000, readOnlyRootFilesystem: true}` |
| 8 | **Pod anti-affinity** | No `affinity` or `topologySpreadConstraints` | All 3 replicas can land on the same node; a single node failure takes the service to 0 despite the replica count | Add `topologySpreadConstraints` with `maxSkew: 1` on `kubernetes.io/hostname`, or `podAntiAffinity` with `preferredDuringScheduling` |

### Verdict

Gaps 1–3 are blockers for any production environment. Gap 3 (plaintext credentials) is also a security incident if this YAML has ever touched a shared repo or CI log. Gaps 4–5 mean rollback is unreliable. Gaps 6–8 mean the stated "3 replicas = HA" claim is not actually true under node failure or maintenance windows.
