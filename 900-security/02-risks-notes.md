# K 9.W.3 — Risk register notes

**Reference case:** Meridian Retail Group — Case A
**Date:** 2026-08-06

---

## Severity summary

| Band | Count | Threats |
|---|---|---|
| Critical (15–25) | 6 | T05, T06, T07, T08, T10, T12 |
| High (10–14) | 4 | T01, T02, T04, T11 |
| Medium (5–9) | 2 | T03, T09 |
| Low (1–4) | 0 | — |

---

## Top critical risk — T06: Broken Object-Level Access Control (score: 16)

**Threat:** A user accesses another customer's cart summary by manipulating the cart ID in the request; the API does not verify that the authenticated user owns the requested cart.

**Why top:** Tied at 16 with T08 (DoS), but T06 is chosen as the primary because:
- Every successful exploit is a GDPR-notifiable breach (vs T08 which is financial/availability)
- BOLA is the most commonly exploited API vulnerability in the wild (OWASP API1:2023)
- No special tooling — automated enumeration scripts are freely available

**Blast radius:**
- Up to **3,000,000 cart sessions/month** are potentially enumerable (call volume from K 8.W.5)
- Each exposed cart contains: customer name, email, delivery address, item list, quantities, prices — **full PII profile**
- **22 countries** of GDPR jurisdiction — one breach triggers multi-country notification obligations
- Estimated affected records per automated scan run: **thousands of carts** within minutes (sequential ID enumeration at typical bot rates of ~100 req/s = 6,000 carts/minute)

---

## Scoring notes

- Likelihood scored on exploit availability and required access level — not on whether it has happened to Meridian before
- T12 (Repudiation) scored Likelihood 5 because it is an absence of a control, not an active attack — the gap is near-certainly present
- T08 (DoS cost amplification) scored 16 — nearly tied with T06 as top risk; both must be mitigated before launch
- No threat scored below Medium — all 12 are actionable
