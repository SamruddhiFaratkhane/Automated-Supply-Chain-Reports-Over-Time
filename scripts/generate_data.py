import pandas as pd
import random
from datetime import datetime, timedelta
import os

regions = ['Pune', 'Mumbai', 'Nashik']
statuses = ['On-time', 'Delayed']
delay_reasons = ['Traffic', 'Weather', 'Warehouse Issue', 'Driver Unavailable', '']

data = []

start_date = datetime(2025, 1, 1)
for i in range(500):
    region = random.choice(regions)
    order_date = start_date + timedelta(days=random.randint(0, 150))
    delivery_delay = random.choice([0, 1, 2, 3])
    actual_delivery = order_date + timedelta(days=delivery_delay)
    delay_status = 'On-time' if delivery_delay <= 1 else 'Delayed'
    delay_reason = '' if delay_status == 'On-time' else random.choice(delay_reasons)
    
    data.append({
        'order_id': f'ORD{i+1:04d}',
        'region': region,
        'order_date': order_date.date(),
        'actual_delivery_date': actual_delivery.date(),
        'delivery_time_days': delivery_delay,
        'delay_status': delay_status,
        'delay_reason': delay_reason
    })

df = pd.DataFrame(data)

os.makedirs('../data', exist_ok=True)
df.to_csv('../data/synthetic_supply_chain_data.csv', index=False)
print("✅ Synthetic data generated and saved to data/synthetic_supply_chain_data.csv")
