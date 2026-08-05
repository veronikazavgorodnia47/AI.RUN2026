# Gold Verification — K 7.W.4

## Grain check — daily_sales_by_category
| total | unique_combos |
|---|---|
| 445 | 445 |

Grain confirmed: one row per (order_date, region, product_category) ✓

## Rate bounds — returns_rate
| min_rate | max_rate |
|---|---|
| 0.0 | 100.0 |

Bounds confirmed: returns_rate_pct between 0 and 100 ✓

## Manual spot-check — returns_rate formula
| order_date | total_orders | returned_orders | returns_rate_pct | silver_total | silver_returned |
|---|---|---|---|---|---|
| 2024-07-04 | 2 | 1 | 50.00 | 2 | 1 |
| 2024-04-02 | 3 | 1 | 33.33 | 3 | 1 |

Formula verified: returned_orders / (completed + returned) × 100 — matches silver source ✓
Denominator excludes pending orders ✓
