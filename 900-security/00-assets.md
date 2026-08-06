# K 9.W.1 — Asset inventory: `cart-api`

**Reference case:** Meridian Retail Group — Case A  
**Service:** `cart-api` — checkout service with AI "summarise my cart" step  
**Date:** 2026-08-06

---

## Asset inventory

| # | Asset | Rank | Rationale |
|---|---|---|---|
| 1 | Customer payment tokens (card PAN, tokenised payment method) | HIGH | Direct financial exposure if leaked; PCI DSS regulated; reuse enables fraud |
| 2 | Customer PII (name, email, delivery address, account ID) | HIGH | GDPR-regulated personal data across 22 countries; breach triggers notification obligations |
| 3 | Customer cart contents + order history | HIGH | Browsing and purchase patterns; fed verbatim into the AI summarise prompt — exposure of one user's cart to another would be a privacy breach |
| 4 | Payment-provider API credential (Stripe / Adyen key) | HIGH | Grants charge and refund capability; leaked key enables unauthorised transactions |
| 5 | AI model system prompt | MEDIUM | Contains business logic, tone rules, and constraints for the summarise step; if extracted, enables targeted prompt injection |
| 6 | Service config (feature flags, DIAL cost cap, retry settings) | MEDIUM | Tampering disables the AI kill-switch, raises the cost cap, or removes the retry guard — each a control from K 8.W.3 / K 8.W.5 |
| 7 | Aggregate order metrics and telemetry | LOW | Non-identifying operational data; low direct value to an attacker |

---

## AI-surface tag

| AI property | Present? | Where |
|---|---|---|
| **Natural-language input** | YES | Cart contents (item names, quantities, prices) are assembled into a natural-language prompt sent to the model for the "summarise my cart" step |
| **Retrieved content becomes instructions** | PARTIAL | Cart item names and descriptions are retrieved from the Orders DB and inserted verbatim into the prompt; a malicious merchant with a crafted product name could attempt prompt injection via the retrieved content |
| **Agent takes irreversible actions** | NO | The summarise step is read-only — it does not modify the cart, place orders, or charge customers |

---

## Highest-value asset

**Customer payment tokens** — direct financial exposure, PCI regulated, and the asset an attacker gains the most from targeting. The threat list in K 9.W.2 starts here, then extends to the AI surface.
