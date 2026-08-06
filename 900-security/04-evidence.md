# K 9.W.5 — Evidence pack: T06 BOLA ownership-verification control

**Reference case:** Meridian Retail Group — Case A
**Service:** `cart-api`
**Date:** 2026-08-06

---

## Block 1 — Control identity

| Field | Value |
|---|---|
| **Control name** | Cart ownership-verification middleware |
| **Framework mapping** | SOC 2 CC6.1 — Logical and physical access controls: the entity implements logical access security software, infrastructure, and architectures over protected information assets |
| **Plain-language description** | Before returning any cart data, the Cart Service verifies that the authenticated user's ID (from the JWT session token) matches the `owner_id` field stored on the requested cart record. Any request where they do not match is rejected with HTTP 403 and an `OwnershipError`. This closes the BOLA vector where an attacker increments a cart ID in the request path to read another customer's cart. |
| **Scope** | All read and write operations on `/cart/{cart_id}` in the Cart Service; applies to web, mobile, and POS request paths through the Apollo GraphQL Gateway |
| **Named owner** | Alex Novak — Lead Backend Engineer, Checkout team (from K 9.W.4) |

---

## Block 2 — Test method

**Control path:** Path 1 — Input validation / access control

**Bypass case tested:** User B attempts to read User A's cart by passing `cart_id=cart-001` while authenticated as `user-B`.

**Verbatim test procedure:**
```bash
cd 900-security/controls
python3 -m pytest test_cart_ownership_check.py -v
```

**Test output (recorded 2026-08-06):**
```
============================= test session starts ==============================
platform darwin -- Python 3.9.6, pytest-8.4.2, pluggy-1.6.0
collected 5 items

test_cart_ownership_check.py::test_user_b_cannot_access_user_a_cart PASSED
test_cart_ownership_check.py::test_unknown_user_cannot_access_any_cart PASSED
test_cart_ownership_check.py::test_empty_user_id_is_rejected          PASSED
test_cart_ownership_check.py::test_owner_can_access_own_cart          PASSED
test_cart_ownership_check.py::test_unknown_cart_id_raises_key_error   PASSED

============================== 5 passed in 0.01s ===============================
```

**Bypass cases confirmed blocked:** 3/3 — user-B rejected from user-A's cart; unknown user rejected; empty user_id rejected (not treated as wildcard).

**Commit SHA:** `3b729d6`
**Branch:** `security/t06-ownership-check`
**Log file path:** `900-security/controls/` (pytest output above; no separate log file — kata artefact)
**Test date:** 2026-08-06

---

## Block 3 — Monitoring

**Design intent** — the following monitoring has not yet been implemented in production. Auditors prefer honest design intent over false claims of coverage.

| Field | Value |
|---|---|
| **Alert metric** | Count of distinct `cart_id` values accessed by a single `user_id` within a 60-second window (enumeration pattern from K 9.W.4 detective control) |
| **Alert threshold** | > 5 distinct `cart_id` values per `user_id` per 60 seconds |
| **Secondary metric** | Rate of HTTP 403 responses on `/cart/{cart_id}` — a spike indicates active BOLA probing |
| **Who gets paged** | Security Champion (Eva Müller) via the alerting stack; escalates to on-call rotation (Tomás Herrera) if rate exceeds 50 blocked requests / minute |
| **Implementation status** | Design intent — alerting rules and the tamper-evident audit log (T12 control) must be wired before launch |

---

## Block 4 — Audit trail

| Field | Value |
|---|---|
| **Log location** | Application logs for Cart Service, routed to the centralised observability stack (Meridian Platform); each cart access event logs `{user_id, cart_id, timestamp, outcome: allowed/blocked}` |
| **Retention period** | 12 months minimum — legal basis: GDPR Art. 5(2) accountability obligation; retention period aligns with the SOC 2 audit window |
| **Immutability mechanism** | None — kata artefact; in production, logs must be written to an append-only log store (e.g., AWS CloudWatch Logs with log-group policy `retention + no-delete`) to satisfy the Repudiation control (T12) |
| **Access control** | Read access restricted to Security Champion and on-call rotation; no developer self-service read on production audit logs |
