import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_extras.metric_cards import style_metric_cards
from data_processor import get_patient_and_population_data
from visualizations import (
    create_timeline,
    create_symptom_calendar_heatmap,
    create_medication_chart,
    create_lab_results_chart,
    create_trigger_analysis_chart,
    create_trigger_severity_correlation,
    create_patient_population_comparison
)
from utils import translate_text

# Set page config
st.set_page_config(page_title="Osama Abdo's FMF Case Analysis", layout="wide")

# Load and process data
df, population_df = get_patient_and_population_data()

# Sidebar
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Overview", "Timeline", "Symptoms", "Medication", "Lab Results", "Trigger Analysis", "Population Comparison", "Printable Report", "Doctor's Summary"])

# Date range selection
min_date = df['date'].min().date()
max_date = df['date'].max().date()
start_date, end_date = st.sidebar.date_input(
    "Select date range",
    [min_date, max_date],
    min_value=min_date,
    max_value=max_date,
    key="date_range"
)

# Reset button
if st.sidebar.button('Reset Filters'):
    start_date = min_date
    end_date = max_date

# Filter data based on selected date range
df_filtered = df[(df['date'].dt.date >= start_date) & (df['date'].dt.date <= end_date)]
population_df_filtered = population_df[(population_df['date'].dt.date >= start_date) & (population_df['date'].dt.date <= end_date)]

# Main content
st.title("Osama Abdo's FMF Case Analysis Dashboard")

if page == "Overview":
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Patient Name", "Osama Abdo")
    with col2:
        current_age = (pd.Timestamp.now() - pd.Timestamp("2010-03-21")).days // 365
        st.metric("Current Age", f"{current_age} years")
    style_metric_cards()

    st.subheader("Quick Stats")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Attacks", len(df_filtered))
    with col2:
        st.metric("Average Severity", f"{df_filtered['severity'].mean():.2f}")
    with col3:
        st.metric("Current Dosage", f"{df_filtered['dosage'].iloc[-1]:.1f} tablets")
    style_metric_cards()

    st.plotly_chart(create_symptom_calendar_heatmap(df_filtered), use_container_width=True)
    st.plotly_chart(create_medication_chart(df_filtered), use_container_width=True)

elif page == "Timeline":
    st.subheader("FMF Attacks Timeline")
    st.plotly_chart(create_timeline(df_filtered), use_container_width=True)

elif page == "Symptoms":
    st.subheader("Symptom Analysis")
    st.plotly_chart(create_symptom_calendar_heatmap(df_filtered), use_container_width=True)

elif page == "Medication":
    st.subheader("Medication History")
    st.plotly_chart(create_medication_chart(df_filtered), use_container_width=True)

elif page == "Lab Results":
    st.subheader("Lab Test Results")
    st.plotly_chart(create_lab_results_chart(df_filtered), use_container_width=True)

elif page == "Trigger Analysis":
    st.subheader("Potential Trigger Analysis")
    st.plotly_chart(create_trigger_analysis_chart(df_filtered), use_container_width=True)
    st.plotly_chart(create_trigger_severity_correlation(df_filtered), use_container_width=True)

elif page == "Population Comparison":
    st.subheader("Patient vs. FMF Population Comparison")
    st.plotly_chart(create_patient_population_comparison(df_filtered, population_df_filtered), use_container_width=True)
    
    avg_severity = df_filtered['severity'].mean()
    pop_avg_severity = population_df_filtered['severity'].mean()
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Patient's Average Severity", f"{avg_severity:.2f}")
    with col2:
        st.metric("Population Average Severity", f"{pop_avg_severity:.2f}")
    
    style_metric_cards()
    
    st.write(f"Osama's average attack severity is {'higher' if avg_severity > pop_avg_severity else 'lower'} than the population average.")

elif page == "Printable Report":
    st.subheader("Printable FMF History Report")
    
    current_age = (pd.Timestamp.now() - pd.Timestamp("2010-03-21")).days // 365
    
    # Patient Information
    st.write("### Patient Information")
    st.write(f"**Name:** Osama Abdo")
    st.write(f"**Current Age:** {current_age} years")
    st.write(f"**Report Period:** {start_date} to {end_date}")
    
    # Summary Statistics
    st.write("### Summary Statistics")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Attacks", len(df_filtered))
    with col2:
        st.metric("Average Severity", f"{df_filtered['severity'].mean():.2f}")
    with col3:
        st.metric("Current Dosage", f"{df_filtered['dosage'].iloc[-1]:.1f} tablets")
    style_metric_cards()
    
    # Attack History
    st.write("### Attack History")
    attack_history = df_filtered[['date', 'severity', 'symptoms']].sort_values('date', ascending=False)
    st.dataframe(attack_history)
    
    # Medication Changes
    st.write("### Medication History")
    medication_changes = df_filtered[['date', 'dosage']].drop_duplicates().sort_values('date')
    st.dataframe(medication_changes)
    
    # Visualizations
    st.write("### Visualizations")
    st.plotly_chart(create_timeline(df_filtered), use_container_width=True)
    st.plotly_chart(create_symptom_calendar_heatmap(df_filtered), use_container_width=True)
    st.plotly_chart(create_medication_chart(df_filtered), use_container_width=True)
    
    # Trigger Analysis
    st.write("### Potential Triggers")
    st.plotly_chart(create_trigger_severity_correlation(df_filtered), use_container_width=True)
    
    # Population Comparison
    st.write("### Population Comparison")
    st.plotly_chart(create_patient_population_comparison(df_filtered, population_df_filtered), use_container_width=True)
    
    # Print Instructions
    st.write("### Print Instructions")
    st.write("To print this report:")
    st.write("1. Use your browser's print function (usually Ctrl+P or Cmd+P)")
    st.write("2. Set the destination to 'Save as PDF' if you want a digital copy")
    st.write("3. In the print settings, enable 'Background Graphics' to include all visualizations")
    st.write("4. Click 'Print' or 'Save' to generate the report")

elif page == "Doctor's Summary":
    st.subheader("FMF Case Summary for Medical Professionals")
    
    current_age = (pd.Timestamp.now() - pd.Timestamp("2010-03-21")).days // 365
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Patient", "Osama Abdo")
        st.metric("Age", f"{current_age} years")
    with col2:
        st.metric("Total Attacks", len(df_filtered))
        st.metric("Avg. Severity", f"{df_filtered['severity'].mean():.2f}")
    
    st.write("### Key Observations")
    st.write("1. Attack Frequency:", len(df_filtered) / ((end_date - start_date).days / 365), "per year")
    st.write("2. Most Common Symptoms:", ", ".join(df_filtered['symptoms'].str.split().explode().value_counts().nlargest(3).index))
    st.write("3. Current Medication: Colchicine", df_filtered['dosage'].iloc[-1], "tablets daily")
    
    st.write("### Recent Attacks")
    st.dataframe(df_filtered[['date', 'severity', 'symptoms']].sort_values('date', ascending=False).head())
    
    st.write("### Severity Trend")
    st.plotly_chart(create_timeline(df_filtered), use_container_width=True)
    
    st.write("### Trigger Analysis")
    st.plotly_chart(create_trigger_severity_correlation(df_filtered), use_container_width=True)

# Footer
st.markdown("---")
st.markdown(f"Dashboard created for analyzing Osama Abdo's FMF case. Data range: {start_date} to {end_date}")
