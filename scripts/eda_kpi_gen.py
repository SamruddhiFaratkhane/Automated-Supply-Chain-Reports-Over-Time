import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Step 1: Load Data
data_path = "../data/synthetic_supply_chain_data.csv"
df = pd.read_csv(data_path)

# Step 2: Basic Cleanup & Exploration
df['actual_delivery_date'] = pd.to_datetime(df['actual_delivery_date'])
df['week'] = df['actual_delivery_date'].dt.isocalendar().week
df['year'] = df['actual_delivery_date'].dt.isocalendar().year

# Step 3: Weekly KPI Aggregation
weekly_kpis = df.groupby(['year', 'week', 'region']).agg({
    'order_id': 'count',
    'delivery_time_days': 'mean',
    'delay_status': lambda x: (x == 'On-time').mean() * 100,
    'delay_reason': lambda x: x[x != ''].value_counts().idxmax() if x[x != ''].any() else 'None'
}).reset_index()

weekly_kpis.rename(columns={
    'order_id': 'total_orders',
    'delivery_time_days': 'avg_delivery_days',
    'delay_status': 'on_time_delivery_percent',
    'delay_reason': 'top_delay_reason'
}, inplace=True)

# Step 4: Save to CSV
output_path = "../data/weekly_kpis.csv"
weekly_kpis.to_csv(output_path, index=False)
print(f"✅ Weekly KPIs saved to: {output_path}")

# (Optional) Visualization
sns.set(style="whitegrid")
plt.figure(figsize=(10, 5))
sns.lineplot(data=weekly_kpis, x='week', y='on_time_delivery_percent', hue='region')
plt.title("Weekly On-Time Delivery % by Region")
plt.savefig("../visualizations/on_time_trend.png")
plt.show()