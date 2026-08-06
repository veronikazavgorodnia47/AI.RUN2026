# K 9.W.4 — Mitigation design: T06 BOLA

**Reference case:** Meridian Retail Group — Case A
**Service:** `cart-api`
**Date:** 2026-08-06

---

## Top critical risk (from 02-risks.csv)

| # | Element | Category | Threat | Likelihood | Impact | Severity |
|---|---|---|---|---|---|---|
| T06 | Cart Service (process) | Classical — BOLA | A user accesses another customer's cart summary by manipulating the cart ID because the API does not verify ownership. | H | H | **Critical** |

**Blast radius:** ~6,000 carts/minute enumerable at 100 req/s bot rate; each cart = name + email + delivery address + full item list; 22 GDPR jurisdictions; notification obligation per breach.

---

## Three-class control design

### Preventive — ownership-verification middleware

**What it does:** Adds a guard in the Cart Service that compares the authenticated user's ID (from the JWT session token) against the `owner_id` field on the requested cart record before returning any data. Any request where `cart.owner_id ≠ authenticated_user_id` is rejected with HTTP 403.

**Threat property closed:** Removes the ability to enumerate cart IDs — without matching ownership, a manipulated cart ID returns nothing.

**Why it matches STRIDE:** Closes the **Elevation of Privilege (E)** threat — the control prevents an attacker from escalating their session's access rights to resources owned by a different user; without matching ownership, no cart data is reachable across the authorisation boundary.

**Owner:** Lead Backend Engineer, Checkout team (Alex Novak)
**Deadline:** 2026-09-05 (30 days — project risk policy default for Critical residual risk)

---

### Detective — anomaly alert on cart-access enumeration

**What it does:** Logs every cart access event with `{user_id, cart_id, timestamp}` to a tamper-evident audit log (addresses T12 Repudiation in parallel). Fires an alert to the Security Champion when a single `user_id` accesses more than 5 distinct `cart_id` values within 60 seconds — the signature of automated BOLA enumeration.

**Threat property closed:** Surfaces enumeration attempts that slip past the ownership check (e.g., a bypass for store associates or an admin endpoint not covered by the middleware).

**Why it matches STRIDE:** Surfaces the **Information Disclosure (I)** threat in progress — the access pattern of one user reading many distinct carts is the signature of unauthorised data extraction; the audit log also closes the **Repudiation (R)** gap from T12, providing the evidence trail required for GDPR breach notification.

**Owner:** Security Champion, Meridian Platform team (Eva Müller)
**Deadline:** 2026-09-05 (30 days)

---

### Responsive — automatic rate-limit and account flag on enumeration signal

**What it does:** When the detective alert fires (>5 distinct cart IDs / 60 s from one user token), automatically rate-limits that token to 1 request per 5 seconds and flags the account for Security review. The Security Champion can suspend the account immediately via the admin console (kill-switch). Limits exposure to ≤12 additional carts between alert and intervention at typical response times.

**Threat property closed:** Caps the blast radius once an enumeration attempt is detected — prevents an attacker from enumerating thousands of carts before being stopped.

**Why it matches STRIDE:** Limits the **Information Disclosure (I)** blast radius — once the Elevation of Privilege attempt is detected, throttling and suspension cap how many additional cart records the attacker can read before being stopped.

**Owner:** Platform / DevOps team (on-call rotation, primary: Tomás Herrera)
**Deadline:** 2026-09-05 (30 days)

---

## Five-field residual-risk acceptance contract

| Field | Content |
|---|---|
| **Risk statement** | *Cause:* The ownership-verification middleware may have implementation gaps (e.g., exception for store-associate endpoints or internal service-to-service calls not covered by the guard). *Event:* An attacker enumerates cart IDs via an uncovered endpoint. *Consequence:* Customer PII and cart contents are exposed without authorisation, triggering GDPR notification obligations across up to 22 countries. |
| **Named owner** | Head of Engineering, Checkout team — Sarah Chen |
| **Expiry date** | 2026-11-05 (90 days — re-evaluate after first pen test covers the Cart Service) |
| **Re-evaluation triggers** | Any new API endpoint added to Cart Service; any change to authentication or session middleware; a BOLA-adjacent finding in a pen test or bug bounty; any GDPR audit covering the checkout flow |
| **Approver** | Data Protection Officer (DPO) — required given GDPR Art. 5(1)(f) integrity and confidentiality obligation across 22 jurisdictions |
