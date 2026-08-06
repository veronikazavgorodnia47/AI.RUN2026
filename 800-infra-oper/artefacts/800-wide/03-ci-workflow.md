# K 8.W.3 — CI/CD workflow + fresh-session supply-chain audit: `cart-api`

**Reference case:** Meridian Retail Group — Case A  
**Pipeline ask:** Build, test, security-scan, and deploy `cart-api` as a container image on every push to `main`.

---

## Part 1 — Generated workflow (first draft)

Prompt used:
```
Write a GitHub Actions workflow that builds, tests, security-scans, and deploys
cart-api as a container image on every push to main.
```

```yaml
# .github/workflows/cart-api-ci.yml (first draft)
name: cart-api CI/CD

on:
  push:
    branches: [main]

jobs:
  build-test-deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Log in to container registry
        uses: docker/login-action@v3
        with:
          registry: registry.meridian.internal
          username: ${{ secrets.REGISTRY_USER }}
          password: ${{ secrets.REGISTRY_PASSWORD }}

      - name: Run tests
        run: |
          pip install -r requirements.txt
          pytest tests/

      - name: Scan dependencies
        uses: snyk/actions/python@v1
        with:
          args: --severity-threshold=high
        env:
          SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}

      - name: Build and push image
        uses: docker/build-push-action@v5
        with:
          push: true
          tags: registry.meridian.internal/cart-api:latest

      - name: Deploy to Kubernetes
        run: |
          kubectl set image deployment/cart-api \
            cart-api=registry.meridian.internal/cart-api:latest
        env:
          KUBECONFIG: ${{ secrets.KUBECONFIG }}
```

---

## Part 2 — Fresh-session supply-chain audit

Prompt used (new session, workflow pasted with no prior context):
```
Audit this CI/CD workflow against six supply-chain controls: pinned action versions,
OIDC short-lived credentials vs long-lived secrets, image signing/provenance,
dependency and image scanning, least-privilege token permissions, a rollback gate.
For each: present / missing / partial, and the one-line fix.
```

### Six-control audit

| # | Control | Status | Finding | One-line fix |
|---|---|---|---|---|
| 1 | **Pinned action versions** | MISSING | All 5 action references use floating tags (`@v4`, `@v3`, `@v5`, `@v1`) — a tag can be silently re-pointed to a malicious commit; the workflow runs different code without any diff | Pin every action to its full commit SHA, e.g. `actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683` |
| 2 | **OIDC short-lived credentials** | MISSING | Two long-lived secrets: `REGISTRY_USER`/`REGISTRY_PASSWORD` for the image registry and `KUBECONFIG` for kubectl — both are permanently valid if leaked | Replace registry login with `docker/login-action` OIDC provider; replace `KUBECONFIG` with `azure/k8s-set-context` or GKE Workload Identity federation (`permissions: id-token: write`) |
| 3 | **Image signing / provenance** | MISSING | Image is pushed with no signing step and no SLSA attestation; a consumer cannot verify the image was produced by this pipeline | Add `sigstore/cosign-installer@<SHA>` + `cosign sign` post-push, or set `provenance: true, sbom: true` on `docker/build-push-action` |
| 4 | **Dependency + image scanning** | PARTIAL | Snyk scans Python dependencies (good). No container image scan after build — a vulnerable base image or OS package reaches production undetected | Add `aquasecurity/trivy-action@<SHA>` scanning the built image before deploy; break on `CRITICAL` |
| 5 | **Least-privilege token scope** | MISSING | No `permissions` block at workflow or job level — GitHub defaults grant broad repo-write; a compromised step can write to branches, packages, or Actions artifacts | Add `permissions: contents: read` at workflow top; grant `packages: write` only on the push step |
| 6 | **Rollback gate** | MISSING | `kubectl set image … :latest` fires with no rollout status check — a broken image goes live and stays live; `KUBECONFIG` also means the rollback credential is the same long-lived secret | Add `kubectl rollout status deployment/cart-api --timeout=120s`; on non-zero exit, run `kubectl rollout undo deployment/cart-api` |

### Additional gaps (beyond the six controls)

| # | Gap | Finding | One-line fix |
|---|---|---|---|
| 7 | **`pip install` without hash-pinning** | `pip install -r requirements.txt` with no `--require-hashes` allows dependency-confusion substitution at install time | Use `pip install --require-hashes -r requirements.txt` with a lock file that includes hashes |
| 8 | **Mutable deploy tag** | `kubectl set image … :latest` means a forced node restart can silently re-pull a different image than what was just built and signed; compounds Gap 6 — even `kubectl rollout undo` restores `:latest`, not the prior SHA | Compute `IMAGE_SHA=$(docker inspect --format='{{index .RepoDigests 0}}' …)` and pass the digest into `kubectl set image` |

### Verdict

All 6 supply-chain controls are absent or partial. Two additional gaps compound the risk. Priority order:

- **Gap 2** (long-lived `REGISTRY_PASSWORD` + `KUBECONFIG`) — permanently valid on leak; gives registry push and cluster write access.
- **Gap 6 + 8** (silent bad deploy + mutable tag) — a broken image goes live silently, and rollback doesn't restore the prior binary.

This workflow would not pass a supply-chain security review.
