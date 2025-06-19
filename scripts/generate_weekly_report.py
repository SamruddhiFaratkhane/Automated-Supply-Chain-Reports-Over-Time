import pandas as pd
from transformers import AutoTokenizer, T5ForConditionalGeneration
import torch
import os

# Load model and tokenizer
model_name = "google/flan-t5-base"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = T5ForConditionalGeneration.from_pretrained(model_name)

device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Device set to use {device}")
model = model.to(device)

# Load your weekly grouped summary CSV
df = pd.read_csv("data/weekly_grouped_summary.csv")

# Output file path
output_path = "Outputs/multi_week_summary.txt"
os.makedirs(os.path.dirname(output_path), exist_ok=True)

# Output file path
output_path = "outputs/multi_week_summary.txt"
os.makedirs(os.path.dirname(output_path), exist_ok=True)

with open(output_path, "w", encoding="utf-8") as f:
    for _, row in df.iterrows():
        week = row['actual_delivery_date']
        total_orders = int(row['total_orders'])
        avg_days = round(row['avg_delivery_days'], 2)
        on_time = round(row['on_time_delivery_percent'], 2)

        prompt = f"""
You are a supply chain analyst AI.
Analyze the weekly delivery performance and give one short actionable business insight (1-2 sentences).

- Week: {week}
- Total Orders: {total_orders}
- Average Delivery Days: {avg_days}
- On-Time Delivery Rate: {on_time}%

Insight:"""

        input_ids = tokenizer(prompt.strip(), return_tensors="pt", truncation=True).input_ids.to(device)
        output_ids = model.generate(input_ids, max_new_tokens=60)
        insight = tokenizer.decode(output_ids[0], skip_special_tokens=True).strip()

        # Write clean summary block
        f.write(f"===== Week of {week} =====\n")
        f.write("Weekly Supply Chain Summary:\n")
        f.write(f"    - Week of {week}\n")
        f.write(f"    - Total Orders: {total_orders}\n")
        f.write(f"    - Average Delivery Days: {avg_days}\n")
        f.write(f"    - On-Time Delivery Rate: {on_time}%\n\n")
        f.write(f"    Insight: {insight}\n\n")


print(f"✅ Full weekly report with insights saved to {output_path}")
