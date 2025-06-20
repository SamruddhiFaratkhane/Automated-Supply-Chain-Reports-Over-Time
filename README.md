# 📦 Automated Supply Chain Reports Over Time

This project leverages **LLMs** (Language Models) and **interactive visualizations** to generate weekly executive insights from supply chain data. It includes data processing, time-aware summarization using HuggingFace models, KPI trend plotting, and a user-friendly Streamlit interface with PDF report export.

---

## 🧠 Features

- ✅ **LLM-powered weekly insights** using FLAN-T5
- 📊 **Dynamic visualizations** of supply chain KPIs using Plotly
- 🗂️ Week selector with summary view
- 📁 Upload your own CSV to generate reports
- 📄 Export complete report (KPI + Insight + Graphs) as PDF
- 💡 Clean UI using Streamlit
- 🧪 Built with modular and extensible structure

---

## 📁 Project Structure

```edit
📦 Automated-Supply-Chain-Reports-Over-Time/
├── app.py # Streamlit App
├── data/
│ ├── synthetic_supply_chain_data.csv
│ ├── weekly_kpis.csv
│ └── weekly_grouped_summary.csv
├── outputs/
│ └── multi_week_summary.txt # LLM-generated insights
├── scripts/
│ ├── generate_data.py
│ ├── eda_and_kpi_generator.py
│ ├── group_by_week.py
│ └── generate_weekly_report.py # FLAN-T5 weekly insight generator
├── visualizations/
│ ├── plot_kpis.py
│ └── plots/
│ ├── total_orders_over_time.html
│ ├── avg_delivery_days_over_time.html
│ └── on_time_delivery_over_time.html
├── requirements.txt
└── README.md
```
---

## 🚀 How to Run

1. Clone the Repo
git clone https://github.com/SamruddhiFaratkhane/Automated-Supply-Chain-Reports-Over-Time.git

2. Install Requirements
pip install -r requirements.txt

3. Run the App
streamlit run app.py

## 📚 Models Used

google/flan-t5-base (from HuggingFace Transformers)

## 🛠️ Dependencies

transformers
streamlit
pandas
plotly
reportlab

## ✍️ Developed By

**Sakshi Patil**
🎓 AI & DS, AISSMS IOIT
🌍 Pune, India

**Samruddhi Faratkhane**
🎓 AI & DS, AISSMS IOIT
🌍 Pune, India
