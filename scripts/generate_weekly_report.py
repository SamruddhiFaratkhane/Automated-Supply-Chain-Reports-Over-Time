import pandas as pd
from transformers import pipeline, set_seed, AutoTokenizer, T5ForConditionalGeneration

# Load model and tokenizer
model_name = "google/flan-t5-base"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = T5ForConditionalGeneration.from_pretrained(model_name)

# Set up generation pipeline and seed
generator = pipeline("text-generation", model=model, tokenizer=tokenizer)
set_seed(42)

# Load weekly data CSV
df = pd.read_csv("C:\\Users\\Admin\\Desktop\\Automated-Supply-Chain\\data\\weekly_grouped_summary.csv")

# Initialize list to store all weekly summaries
weekly_reports = []

# Loop through each week's row
for _, row in df.iterrows():
    prompt = f"""
    Weekly Supply Chain Summary:
    - Week of {row['actual_delivery_date']}
    - Total Orders: {row['total_orders']}
    - Average Delivery Days: {row['avg_delivery_days']}
    - On-Time Delivery Rate: {row['on_time_delivery_percent']}%

    Insight:
    """

    result = generator(prompt, max_length=100, num_return_sequences=1)[0]['generated_text']

    # Clean output and store
    weekly_reports.append(f"===== Week of {row['actual_delivery_date']} =====\n{result.strip()}\n\n")

# Save to file
output_path = "C:\\Users\\Admin\\Desktop\\Automated-Supply-Chain\\weekly_report.txt"
with open(output_path, "w", encoding="utf-8") as f:
    f.writelines(weekly_reports)

print(f"✅ All weekly reports saved to: {output_path}")
