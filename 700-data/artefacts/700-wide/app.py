import duckdb
import pandas as pd
import plotly.express as px

con = duckdb.connect()

sales = con.execute("SELECT * FROM 'gold/daily_sales_by_category.parquet'").fetchdf()
returns = con.execute("SELECT * FROM 'gold/returns_rate.parquet'").fetchdf()

fig1 = px.bar(
    sales.groupby(['region', 'product_category'])['total_revenue'].sum().reset_index(),
    x='region',
    y='total_revenue',
    color='product_category',
    title='Total Revenue by Region',
    labels={'total_revenue': 'Revenue (€)', 'region': 'Region'}
)
fig1.show()

fig2 = px.line(
    returns.sort_values('order_date'),
    x='order_date',
    y='returns_rate_pct',
    title='Returns Rate Over Time (%)',
    labels={'returns_rate_pct': 'Returns Rate (%)', 'order_date': 'Date'}
)
fig2.show()

total_revenue = sales['total_revenue'].sum()
avg_returns = returns['returns_rate_pct'].mean()
last_date = returns['order_date'].max()

print(f"Total Revenue:       €{total_revenue:,.2f}")
print(f"Avg Returns Rate:    {avg_returns:.2f}%")
print(f"Data last updated:   {last_date}")
