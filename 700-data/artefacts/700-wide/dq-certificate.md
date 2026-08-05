# DQ Certificate — K 7.W.5

## Clean data — 8/8 passed
All checks passed on clean gold tables before any injection.

## Force-test: one targeted violation per check

| # | Check | Injected violation | Fired? | Post-cleanup |
|---|---|---|---|---|
| 1 | No null key columns in daily_sales | `order_date = NULL` | 1 violation ✓ | clean ✓ |
| 2 | total_revenue > 0 | `total_revenue = -999.99` | 1 violation ✓ | clean ✓ |
| 3 | order_count > 0 | `order_count = 0` | 1 violation ✓ | clean ✓ |
| 4 | No duplicate grain (order_date, region, product_category) | duplicate of first grain row | 1 violation ✓ | clean ✓ |
| 5 | No null order_date in returns_rate | `order_date = NULL` | 1 violation ✓ | clean ✓ |
| 6 | returns_rate_pct between 0.0 and 100.0 | `returns_rate_pct = 150.0` | 1 violation ✓ | clean ✓ |
| 7 | returned_orders <= total_orders | `returned_orders = 5, total_orders = 1` | 1 violation ✓ | clean ✓ |
| 8 | order_date spans at least 30 days | rows trimmed to 5-day window | 1 violation ✓ | clean ✓ |

## Result: 8/8 ✓
Every check fired on its targeted violation and returned clean after removal.

## Parquet outputs confirmed
| File | Rows |
|---|---|
| silver/transactions_clean.parquet | 460 |
| gold/daily_sales_by_category.parquet | 352 |
| gold/returns_rate.parquet | 252 |

Break-and-verify complete — checks are trusted gates, not decorative assertions.
