# Silver Verification — K 7.W.3

| Metric | Value |
|---|---|
| silver_rows | 460 |
| null_amount | 0 |
| duplicate_order_ids | 0 |

**Row-count math:** 500 (bronze) − 26 (null amount) − 14 (duplicate order_ids) = 460 ✓

**Cleaning applied:**
- Removed rows where amount IS NULL
- Deduplicated by order_id (kept highest customer_id)
- Standardised order_date to DATE (3 formats: YYYY-MM-DD, DD/MM/YYYY, Mon DD YYYY)
- Negative amounts retained (legitimate returns)
