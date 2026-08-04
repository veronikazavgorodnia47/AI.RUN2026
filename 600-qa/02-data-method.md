---
case: Meridian Retail Group — Click & Collect
kata: K 6.W.3
date: 2026-08-04
author: Veronika Zavgorodnia
---

# Test Data Generation Method

**Tool:** Claude Sonnet 4.6 (claude.ai/code session) — prompted to generate fictional but culturally realistic records per country/market band.

**Fields obfuscated:** customer name (fictional, culturally realistic per country); email (`.invalid` TLD per RFC 2606 — guaranteed non-resolving); payment tokens (test-mode prefixes + masked suffix, never real card numbers or IBANs); loyalty numbers (fictional numeric IDs with country prefix).

**Variety dimensions exercised:** country band (IT, DE, JP, GB, FR, ES, AE); payment method (Postepay, Klarna split-pay, PayPay, Satispay, Visa debit/credit, Mastercard); loyalty tier (Gold, Silver, Bronze, null/inactive); identity-merge state (single clean account, dual-region IT+JP, inactive card); character set (Latin, Latin-extended ß/accented, Japanese kana, Arabic RTL); order size (1 item, 3 items with one out-of-stock); pickup window position (standard, 47h59m boundary).

**PII approach:** no real Meridian customer data used; names drawn from public cultural name lists (not real individuals); all emails non-resolvable; payment tokens follow test-mode format documented in Meridian QA environment setup guide. GDPR Article 30 compliance: synthetic dataset, no derivation from production records.

**SAP staleness scenarios (TC-08, TC-16):** no customer record change needed — staleness is configured at the SAP sandbox stub level (timestamp returned by stub set to 30s or 45s old). Any realistic record (e.g., CUS-FR-00712) can be used as the customer input.

**What is intentionally missing:** regions not yet onboarded to Phase 1 (outside 22 in-scope countries); Phase 2 cross-channel inventory reservation patterns; PayPay SCA variant for JP market (out of scope per `00-test-plan.md`).

**Cross-reference:** every edge record includes a `test_cases` field mapping it to the relevant cases in `01-test-cases.md`.
