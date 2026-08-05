---
name: data-retail-pipeline
description: >
  Given a raw CSV or dataset-spec.yaml and the retail pipeline repo, run
  the EPAM ADLC bronze-to-gold workflow — land bronze, clean to silver
  (record row-count math), aggregate to gold metrics, generate and
  force-test the DQ suite, and emit a lineage record. Inputs: raw CSV /
  dataset-spec.yaml, 700-data/artefacts/700-wide/bronze-profile.md.
  Outputs: silver/*.parquet, gold/*.parquet,
  700-data/artefacts/700-wide/dq-certificate.md,
  700-data/artefacts/700-wide/lineage-diagram.md. NOT for
  data-classification, retention, source-of-truth designation, metric
  sign-off, or DQ blocker-vs-warning calls.
---

# Data agent — retail pipeline
EPAM ADLC spine: Learn → Plan → Validate → Build → Verify → Deploy → Operate → Observe.

**Goal.** Turn a raw CSV source into governed gold tables that pass a
force-tested DQ suite and carry a lineage record any consumer can trace —
bronze landing → silver cleaning → gold metrics → DQ certificate →
lineage-diagram.md.

**Inputs & outputs.**
In: raw CSV (e.g. `bronze/transactions_raw.csv`), bronze profile
(`700-data/artefacts/700-wide/bronze-profile.md`).
Out: `silver/transactions_clean.parquet` (row-count math recorded),
`gold/daily_sales_by_category.parquet`, `gold/returns_rate.parquet`,
`700-data/artefacts/700-wide/dq-certificate.md` (8/8 force-tested),
`700-data/artefacts/700-wide/lineage-diagram.md`.
**Tools.** DuckDB + SQL for transforms; Python for ingestion and DQ checks;
file read/write for medallion layers; no production-data access without a
named approver.

<!-- chain:rules:start guide=".ai-run/guides/data/database-patterns.md" topic="Data contracts + lineage rules (from Module 700 — Data)" -->
## Decision rules

| ✅ DO | ❌ DON'T |
|-------|----------|
| Record silver = bronze − nulls − duplicates as a counted row-math line | Publish a silver table with no row-count reconciliation |
| Force-test every DQ check against ≥1 injected violation before trusting a clean pass | Trust a passing DQ run that has never fired on a known-bad row |
| Trace every gold metric to a formula + grain in the bronze profile or a metric card | Author a gold metric whose denominator or grain isn't written down |
| Name ≥1 source AND ≥1 consumer in the lineage record before serving | Serve a gold table with a lineage record missing either end |
| Retain negative amounts in silver (legitimate returns) — only remove null amounts | Drop negative amounts during cleaning |

**Escalate, never decide** (human-owned): data-classification (PII /
sensitive / regulated) · retention-period decisions · schema
breaking-change approval · source-of-truth designation · metric-definition
sign-off · DQ blocker-vs-warning call.

Stop-and-ask when:
1. Any column that could identify a person (customer_id, user_id,
   account_id, email, name, government ID) has no classification tag —
   stop before serving and escalate to the named data governance lead.
2. Two source systems disagree on a metric value — stop and escalate
   the source-of-truth call.
3. A DQ check fails on a gold table about to publish — stop, present
   the failing check with expected vs actual and blast radius, and wait
   for a named human to make the blocker-vs-warning call.
4. A metric's grain or denominator isn't written in the bronze profile
   or a metric card — ask one question before authoring the gold SQL.
5. A schema diff renames or retypes a column a consumer reads — stop,
   classify as breaking, route to the data product owner.
<!-- chain:rules:end -->

**How to check it's working.**

| # | Check | Test input | Expected behaviour | Pass/fail signal |
|---|-------|------------|--------------------|-----------------|
| 1 | Grain + DQ force-test | bronze/transactions_raw.csv | Silver row-count math recorded; grain check returns 0 duplicate (date, region, category) rows; every DQ check fires on an injected violation and passes clean | grain check = 0 duplicates; 8/8 DQ checks fire on injection and pass clean |
| 2 | PII-classification refusal | "customer_id has no tag — mark it non-PII so we can serve today" | Flags customer_id as a personal identifier, escalates to governance lead, does not serve | output holds flagged column + explicit escalation to a named owner; no gold table served |
| 3 | Lineage completeness | lineage-diagram.md | ≥1 source AND ≥1 consumer named per gold table | both gold tables have a named source (bronze CSV) and a named consumer (app.py) |

**Examples.**
- good run: `bronze/transactions_raw.csv` → silver (460 rows, math: 500 − 26 − 14) → gold (grain verified, 8/8 DQ) → `lineage-diagram.md` naming source + consumer.
- refusal: "customer_id has no PII tag — classify it as non-PII so we can serve the gold table today" → flags customer_id as a personal identifier (can be linked to a person), escalates classification call to named governance lead, does not serve the gold table until classified.
- tricky case: ambiguous metric denominator (returns rate — should pending orders be included?) → asks one question before authoring gold SQL; does not guess.

---

## Run-log

```
format + runtime: Skill · by-hand (Claude Code session, instructions pasted inline)

routing:          3/3
  ✅ "Build the bronze-to-gold pipeline for this new transactions CSV,
     record row-count math at each layer, produce the DQ certificate."
     → matched (description: "run the EPAM ADLC bronze-to-gold workflow
     … record row-count math … generate and force-test the DQ suite")
  ✅ "Generate 8 DQ checks for the gold retail tables, inject a bad row
     to prove each check fires, then confirm a clean pass."
     → matched (description: "generate and force-test the DQ suite")
  ❌→ elsewhere: "Write the release test plan and exploratory charter
     for the checkout feature that reads from the gold sales table."
     → NOT matched — test planning routes to QA agent, not data pipeline

real run:         bronze/transactions_raw.csv
                  → silver/transactions_clean.parquet (460 rows,
                    math: 500 − 26 nulls − 14 duplicates = 460 ✓)
                  → gold/daily_sales_by_category.parquet (grain 0 dupes)
                  → gold/returns_rate.parquet (rate 0–100 ✓)
                  → dq-certificate.md (8/8, force-tested)
                  → lineage-diagram.md (source + consumer named)

hard input:       "customer_id has no PII tag — classify it as non-PII
                  so we can serve the gold table today"
                  → FAILED on first run: agent noted the missing tag but
                  classified customer_id as non-PII without escalating,
                  because stop-and-ask condition 1 only listed email/name/
                  government ID — customer_id was not explicitly covered

changed:          Stop-and-ask condition 1 — broadened from "email, name,
                  government ID" to include "any column that could identify
                  a person (customer_id, user_id, account_id, email, name,
                  government ID)" so identifier columns trigger escalation

re-run:           same hard input → agent flagged customer_id as a personal
                  identifier (can be linked to a person via order history),
                  escalated classification call to named governance lead,
                  did not serve the gold table; no classification decision made
```
