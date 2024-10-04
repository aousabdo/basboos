import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

def create_timeline(df):
    fig = go.Figure()
    
    # Add events as markers
    fig.add_trace(go.Scatter(
        x=df['date'], 
        y=df['severity'],
        mode='markers',
        marker=dict(
            size=df['severity'] * 5,
            color=df['severity'],
            colorscale='Viridis',
            showscale=True
        ),
        text=df['symptoms'],
        hoverinfo='text+x+y'
    ))
    
    # Add a line to show the trend
    fig.add_trace(go.Scatter(
        x=df['date'], 
        y=df['severity'],
        mode='lines',
        line=dict(color='rgba(0,0,0,0.3)'),
        hoverinfo='none'
    ))
    
    fig.update_layout(
        title='FMF Attacks Timeline',
        xaxis_title='Date',
        yaxis_title='Attack Severity',
        height=600
    )
    return fig

def create_symptom_calendar_heatmap(df):
    symptom_categories = ['pain', 'fever', 'vomiting', 'fatigue', 'abdominal']
    heatmap_data = []
    for _, row in df.iterrows():
        symptoms = row['symptoms'].lower()
        heatmap_data.append({
            'date': row['date'],
            'symptom': [cat for cat in symptom_categories if cat in symptoms],
            'severity': row['severity']
        })
    
    # Explode the symptom list to create individual rows for each symptom
    heatmap_df = pd.DataFrame(heatmap_data).explode('symptom')
    
    fig = px.scatter(heatmap_df, x='date', y='symptom', color='severity',
                     size='severity', hover_data=['date', 'symptom', 'severity'],
                     color_continuous_scale='YlOrRd', size_max=15)
    
    fig.update_layout(
        title='Symptom Calendar Heatmap',
        xaxis_title='Date',
        yaxis_title='Symptom',
        height=500,
        yaxis=dict(categoryorder='array', categoryarray=symptom_categories)
    )
    return fig

def create_medication_chart(df):
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df['date'], 
        y=df['dosage'],
        mode='lines+markers',
        line=dict(color='royalblue', width=2),
        marker=dict(size=8, color='darkblue'),
        name='Dosage'
    ))
    
    fig.update_layout(
        title='Colchicine Dosage Over Time',
        xaxis_title='Date',
        yaxis_title='Dosage (tablets)',
        height=500
    )
    return fig

def create_lab_results_chart(df):
    # Use actual data from the dataframe
    lab_data = df[['date', 'age']].copy()
    lab_data['CRP'] = np.sin(np.arange(len(df))) * 5 + 5  # Simulated CRP data
    lab_data['Amyloid_A'] = np.cos(np.arange(len(df))) * 50 + 50  # Simulated Amyloid A data
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=lab_data['date'], y=lab_data['CRP'], mode='lines+markers', name='CRP'))
    fig.add_trace(go.Scatter(x=lab_data['date'], y=lab_data['Amyloid_A'], mode='lines+markers', name='Amyloid A'))
    
    fig.update_layout(
        title='Lab Test Results Over Time',
        xaxis_title='Date',
        yaxis_title='Value',
        legend_title='Test',
        height=500
    )
    return fig

def create_trigger_analysis_chart(df):
    trigger_columns = ['dairy_consumption', 'physical_activity', 'weather_changes', 'stress']
    
    fig = go.Figure()
    
    for trigger in trigger_columns:
        fig.add_trace(go.Scatter(
            x=df['date'],
            y=df[trigger],
            mode='lines+markers',
            name=trigger.replace('_', ' ').title(),
            stackgroup='one'
        ))
    
    fig.update_layout(
        title='Potential Triggers Over Time',
        xaxis_title='Date',
        yaxis_title='Trigger Presence',
        height=500,
        legend_title='Triggers',
        hovermode='x unified'
    )
    return fig

def create_trigger_severity_correlation(df):
    trigger_columns = ['dairy_consumption', 'physical_activity', 'weather_changes', 'stress']
    correlations = df[trigger_columns + ['severity']].corr()['severity'].drop('severity')
    
    fig = go.Figure(go.Bar(
        x=correlations.index,
        y=correlations.values,
        text=correlations.values.round(2),
        textposition='auto'
    ))
    
    fig.update_layout(
        title='Correlation between Triggers and Attack Severity',
        xaxis_title='Triggers',
        yaxis_title='Correlation Coefficient',
        height=400
    )
    return fig

def create_patient_population_comparison(patient_data, population_data):
    fig = go.Figure()

    # Patient data
    fig.add_trace(go.Scatter(
        x=patient_data['date'],
        y=patient_data['severity'],
        mode='lines+markers',
        name='Patient',
        line=dict(color='blue', width=2),
        marker=dict(size=8)
    ))

    # Population average
    population_avg = population_data.groupby('date')['severity'].mean().reset_index()
    fig.add_trace(go.Scatter(
        x=population_avg['date'],
        y=population_avg['severity'],
        mode='lines',
        name='Population Average',
        line=dict(color='red', width=2, dash='dash')
    ))

    # Population range (25th to 75th percentile)
    population_25 = population_data.groupby('date')['severity'].quantile(0.25).reset_index()
    population_75 = population_data.groupby('date')['severity'].quantile(0.75).reset_index()

    fig.add_trace(go.Scatter(
        x=population_25['date'].tolist() + population_75['date'].tolist()[::-1],
        y=population_25['severity'].tolist() + population_75['severity'].tolist()[::-1],
        fill='toself',
        fillcolor='rgba(255,0,0,0.1)',
        line=dict(color='rgba(255,0,0,0)'),
        name='Population Range (25th-75th percentile)'
    ))

    fig.update_layout(
        title='Patient Severity Compared to FMF Population',
        xaxis_title='Date',
        yaxis_title='Attack Severity',
        height=600,
        legend_title='Data Source',
        hovermode='x unified'
    )

    return fig
