import pandas as pd
import os

# Load data
df = pd.read_csv('../data/synthetic_supply_chain_data.csv')
df['actual_delivery_date'] = pd.to_datetime(df['actual_delivery_date'])

# Set datetime index for resampling
df.set_index('actual_delivery_date', inplace=True)

# Resample by week and count orders
weekly_grouped = df.resample('W').agg({
    'order_id': 'count',
    'delivery_time_days': 'mean',
    'delay_status': lambda x: (x == 'On-time').mean() * 100
}).rename(columns={
    'order_id': 'total_orders',
    'delivery_time_days': 'avg_delivery_days',
    'delay_status': 'on_time_delivery_percent'
})

# Reset index to save
weekly_grouped.reset_index(inplace=True)

# Save to CSV
weekly_grouped.to_csv('../data/weekly_grouped_summary.csv', index=False)
print("✅ Weekly grouped data saved to data/weekly_grouped_summary.csv")

import pandas as pd
import os

# Load data
df = pd.read_csv('../data/synthetic_supply_chain_data.csv')
df['actual_delivery_date'] = pd.to_datetime(df['actual_delivery_date'])

# Set datetime index for resampling
df.set_index('actual_delivery_date', inplace=True)

# Resample by week and count orders
weekly_grouped = df.resample('W').agg({
    'order_id': 'count',
    'delivery_time_days': 'mean',
    'delay_status': lambda x: (x == 'On-time').mean() * 100
}).rename(columns={
    'order_id': 'total_orders',
    'delivery_time_days': 'avg_delivery_days',
    'delay_status': 'on_time_delivery_percent'
})

# Reset index to save
weekly_grouped.reset_index(inplace=True)

# Save to CSV
weekly_grouped.to_csv('../data/weekly_grouped_summary.csv', index=False)
print("✅ Weekly grouped data saved to data/weekly_grouped_summary.csv")