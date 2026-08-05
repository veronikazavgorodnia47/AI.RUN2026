# Bronze Profile — K 7.W.2

| Metric | Value |
|---|---|
| total_rows | 500 |
| null_amount | 26 |
| duplicate_order_ids | 14 |
| min_amount | -155.37 (legitimate returns — do NOT remove) |
| max_amount | 499.79 |
| distinct_statuses | 3 (completed / returned / pending) |
| distinct_date_strings | 401 (confirms mixed date formats) |

**Expected silver row count:** 500 − 26 (null amount) − 14 (duplicates) = 460
