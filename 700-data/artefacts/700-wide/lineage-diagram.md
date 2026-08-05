# Lineage Record — retail pipeline

## bronze → silver → gold

```
Source: bronze/transactions_raw.csv
  (500 rows · order_id, customer_id, region, order_date, product_category, amount, quantity, status)
    │
    │  Cleaning: remove null amount (−26), deduplicate order_id (−14),
    │            standardise order_date to DATE, retain negative amounts
    ▼
silver/transactions_clean.parquet
  (460 rows · same schema, amount FLOAT, order_date DATE)
    │
    ├──► gold/daily_sales_by_category.parquet
    │      Grain: (order_date, region, product_category)
    │      Formula: total_revenue = SUM(amount) WHERE status='completed' AND amount > 0
    │               order_count  = COUNT(DISTINCT order_id) WHERE status='completed'
    │      Rows: 352
    │      Consumer: app.py — Revenue by Region chart
    │
    └──► gold/returns_rate.parquet
           Grain: order_date
           Formula: returns_rate_pct = returned_orders / (completed + returned) × 100
                    denominator excludes pending
           Rows: 252
           Consumer: app.py — Returns Rate Over Time chart
```

## Source → Consumer map

| Gold table | Source | Consumer |
|---|---|---|
| daily_sales_by_category | bronze/transactions_raw.csv | app.py dashboard (bar chart) |
| returns_rate | bronze/transactions_raw.csv | app.py dashboard (line chart) |
