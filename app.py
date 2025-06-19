import streamlit as st
import pandas as pd
import plotly.express as px
from transformers import pipeline, set_seed
from datetime import datetime
import os
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet

# Set up
st.set_page_config(page_title="📦 Supply Chain Insights", layout="wide")
st.title("📦 Automated Supply Chain Reports Over Time")
st.caption("Using Time-Aware LLMs for Dynamic Business Intelligence")

# Load model
@st.cache_resource
def load_model():
    model_name = "google/flan-t5-base"
    return pipeline("text2text-generation", model=model_name)

summarizer = load_model()
set_seed(42)

# Upload CSV
uploaded_file = st.file_uploader("📂 Upload Weekly KPI CSV", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    df['actual_delivery_date'] = pd.to_datetime(df['actual_delivery_date'])
    df.sort_values("actual_delivery_date", inplace=True)

    # Section: Week Selector
    st.subheader("📅 Select Week to Analyze")
    weeks = df['actual_delivery_date'].dt.strftime("%Y-%m-%d").tolist()
    selected_week = st.selectbox("Choose a Week", weeks)
    selected_row = df[df['actual_delivery_date'].dt.strftime("%Y-%m-%d") == selected_week].iloc[0]

    # Section: KPI Summary
    st.subheader("📊 Weekly KPI Summary")
    col1, col2, col3 = st.columns(3)
    col1.metric("📦 Total Orders", int(selected_row['total_orders']))
    col2.metric("🕒 Avg Delivery Days", round(selected_row['avg_delivery_days'], 2))
    col3.metric("✅ On-Time Delivery %", f"{round(selected_row['on_time_delivery_percent'], 2)}%")

    # Section: Insight Generation
    st.subheader("🧠 Weekly Insight")
    prompt = f"""
    Weekly Supply Chain Summary:
    - Week of {selected_row['actual_delivery_date'].date()}
    - Total Orders: {selected_row['total_orders']}
    - Average Delivery Days: {selected_row['avg_delivery_days']}
    - On-Time Delivery Rate: {selected_row['on_time_delivery_percent']}%

    Insight:
    """
    if st.button("Generate Insight"):
        with st.spinner("Generating summary..."):
            insight = summarizer(prompt, max_length=100)[0]['generated_text']
        st.success(insight)
    else:
        insight = ""

    # Section: KPI Plots
    st.subheader("📈 KPI Visualizations")

    # Plot 1: Total Orders
    fig1 = px.line(df, x='actual_delivery_date', y='total_orders', title="📦 Total Orders Over Time")
    fig1.add_scatter(x=[selected_row['actual_delivery_date']], y=[selected_row['total_orders']], mode='markers+text',
                     marker=dict(color='red', size=10), text=["Selected"], textposition="top center")
    st.plotly_chart(fig1, use_container_width=True)

    # Plot 2: On-Time Delivery
    fig2 = px.line(df, x='actual_delivery_date', y='on_time_delivery_percent', title="✅ On-Time Delivery Rate (%)")
    fig2.add_scatter(x=[selected_row['actual_delivery_date']], y=[selected_row['on_time_delivery_percent']],
                     mode='markers+text', marker=dict(color='red', size=10), text=["Selected"], textposition="top center")
    st.plotly_chart(fig2, use_container_width=True)

    # Plot 3: Avg Delivery Days
    fig3 = px.bar(df, x='actual_delivery_date', y='avg_delivery_days', title="🕒 Average Delivery Days Per Week")
    fig3.add_scatter(x=[selected_row['actual_delivery_date']], y=[selected_row['avg_delivery_days']],
                     mode='markers+text', marker=dict(color='red', size=10), text=["Selected"], textposition="top center")
    st.plotly_chart(fig3, use_container_width=True)

    # Save plots as PNG
    os.makedirs("temp_plots", exist_ok=True)
    fig1.write_image("temp_plots/total_orders.png")
    fig2.write_image("temp_plots/on_time_delivery.png")
    fig3.write_image("temp_plots/avg_delivery.png")

    # Section: Export Report
    st.subheader("📤 Export Report")

    def generate_pdf_report():
        file_path = f"SupplyChain_Report_{selected_week}.pdf"
        doc = SimpleDocTemplate(file_path, pagesize=A4)
        styles = getSampleStyleSheet()
        story = []

        story.append(Paragraph("📦 Automated Supply Chain Report", styles["Title"]))
        story.append(Spacer(1, 12))

        # Metrics
        story.append(Paragraph(f"Week: {selected_week}", styles["Normal"]))
        story.append(Paragraph(f"Total Orders: {int(selected_row['total_orders'])}", styles["Normal"]))
        story.append(Paragraph(f"Avg Delivery Days: {round(selected_row['avg_delivery_days'], 2)}", styles["Normal"]))
        story.append(Paragraph(f"On-Time Delivery %: {round(selected_row['on_time_delivery_percent'], 2)}%", styles["Normal"]))
        story.append(Spacer(1, 12))

        if insight:
            story.append(Paragraph("📝 Insight", styles["Heading2"]))
            story.append(Paragraph(insight, styles["Normal"]))
            story.append(Spacer(1, 12))

        # Plots
        for plot_path in ["temp_plots/total_orders.png", "temp_plots/on_time_delivery.png", "temp_plots/avg_delivery.png"]:
            story.append(Image(plot_path, width=450, height=250))
            story.append(Spacer(1, 12))

        doc.build(story)
        return file_path

    if st.button("📄 Download Full Report as PDF"):
        with st.spinner("Generating PDF..."):
            pdf_path = generate_pdf_report()
        with open(pdf_path, "rb") as f:
            st.download_button("📥 Click to Download PDF", f, file_name=pdf_path, mime="application/pdf")

    # Footer
    st.markdown("---")
    st.markdown("🔧 Developed by *Sakshi Patil* and *Samruddhi Faratkhane* | 🤖 Powered by FLAN-T5 & Streamlit")

else:
    st.info("Please upload a weekly KPI CSV (like weekly_grouped_summary.csv) to begin.")