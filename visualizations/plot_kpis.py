import pandas as pd
import plotly.express as px
import os

# Load your data
df = pd.read_csv("data/weekly_grouped_summary.csv")

# Convert week column to datetime for proper sorting
df['actual_delivery_date'] = pd.to_datetime(df['actual_delivery_date'])
df = df.sort_values('actual_delivery_date')

# Round values for better visuals
df['avg_delivery_days'] = df['avg_delivery_days'].round(2)
df['on_time_delivery_percent'] = df['on_time_delivery_percent'].round(2)

# Create output directory for plots
os.makedirs("visualizations/plots", exist_ok=True)

# Total Orders over Time
fig_orders = px.line(
    df,
    x="actual_delivery_date",
    y="total_orders",
    title="📦 Total Orders Over Time",
    markers=True,
    labels={"actual_delivery_date": "Week", "total_orders": "Total Orders"}
)
fig_orders.write_html("visualizations/plots/total_orders_over_time.html")

# Average Delivery Days over Time
fig_avg_days = px.line(
    df,
    x="actual_delivery_date",
    y="avg_delivery_days",
    title="⏱️ Average Delivery Days Over Time",
    markers=True,
    labels={"actual_delivery_date": "Week", "avg_delivery_days": "Avg Delivery Days"}
)
fig_avg_days.write_html("visualizations/plots/avg_delivery_days_over_time.html")

# On-Time Delivery Rate over Time
fig_ontime = px.bar(
    df,
    x="actual_delivery_date",
    y="on_time_delivery_percent",
    title="✅ On-Time Delivery Rate (%) Over Time",
    labels={"actual_delivery_date": "Week", "on_time_delivery_percent": "On-Time %"},
    text="on_time_delivery_percent"
)
fig_ontime.update_traces(texttemplate='%{text:.2f}%', textposition='outside')
fig_ontime.write_html("visualizations/plots/on_time_delivery_over_time.html")

print("✅ KPI charts saved to visualizations/plots/")
