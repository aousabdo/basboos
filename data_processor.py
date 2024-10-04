import pandas as pd
import numpy as np

def process_fmf_data():
    # This function would typically read from a file or database
    # For this example, we'll create a sample DataFrame based on the provided data
    data = [
        {"date": "2021-11-06", "dosage": 1.5, "symptoms": "Mild back pain, no fever", "severity": 2},
        {"date": "2021-11-30", "dosage": 1.5, "symptoms": "Very severe attack", "severity": 9},
        {"date": "2022-01-07", "dosage": 2, "symptoms": "Diarrhea and stomach pain", "severity": 5},
        {"date": "2022-03-14", "dosage": 2, "symptoms": "Mild chest pain, fever", "severity": 4},
        {"date": "2022-08-14", "dosage": 2, "symptoms": "Mild abdominal and chest pain, back pain", "severity": 3},
        {"date": "2022-09-14", "dosage": 2, "symptoms": "Severe chest pain", "severity": 8},
        {"date": "2022-09-26", "dosage": 2, "symptoms": "Severe back pain, fever", "severity": 9},
        {"date": "2022-11-18", "dosage": 2, "symptoms": "Severe stomach pain, vomiting, fever", "severity": 9},
        {"date": "2023-02-06", "dosage": 2, "symptoms": "Vomiting, abdominal pain and bloating", "severity": 7},
        {"date": "2023-02-12", "dosage": 2, "symptoms": "Abdominal pain and bloating", "severity": 5},
        {"date": "2023-03-07", "dosage": 2, "symptoms": "Body aches, persistent high fever", "severity": 8},
        {"date": "2023-03-19", "dosage": 2, "symptoms": "Fever without apparent cause", "severity": 4},
        {"date": "2023-05-06", "dosage": 2, "symptoms": "Moderate pain", "severity": 5},
        {"date": "2023-05-14", "dosage": 2, "symptoms": "Severe chest and back pain, fever", "severity": 9},
        {"date": "2023-06-14", "dosage": 2, "symptoms": "High fever, mild pain", "severity": 6},
        {"date": "2023-08-10", "dosage": 2, "symptoms": "Fever, mild fatigue", "severity": 3},
        {"date": "2023-09-19", "dosage": 2, "symptoms": "Back and chest pain", "severity": 7},
        {"date": "2023-11-19", "dosage": 2, "symptoms": "Mild fever", "severity": 2},
        {"date": "2024-02-07", "dosage": 2, "symptoms": "Fever, moderate back pain", "severity": 5},
        {"date": "2024-03-16", "dosage": 2, "symptoms": "Severe back and chest pain", "severity": 8},
        {"date": "2024-03-22", "dosage": 2, "symptoms": "Severe pain in right side of chest and back", "severity": 8},
        {"date": "2024-04-02", "dosage": 2, "symptoms": "High fever, general fatigue, abdominal pain", "severity": 7},
        {"date": "2024-05-26", "dosage": 2, "symptoms": "Chest pain, vomiting, fever", "severity": 7},
        {"date": "2024-09-16", "dosage": 2, "symptoms": "Fever, general fatigue", "severity": 4},
        {"date": "2024-09-18", "dosage": 2, "symptoms": "Mild chest pain, stomach pain", "severity": 4},
    ]
    
    df = pd.DataFrame(data)
    df['date'] = pd.to_datetime(df['date'])
    
    # Calculate age based on Osama's birthday
    birthday = pd.Timestamp("2010-03-21")
    df['age'] = ((df['date'] - birthday).dt.total_seconds() / (365.25 * 24 * 60 * 60)).astype(int)
    
    # Improved trigger identification
    df['dairy_consumption'] = df['symptoms'].str.contains('dairy|milk|cheese|yogurt', case=False, regex=True).astype(int)
    df['physical_activity'] = df['symptoms'].str.contains('physical|sports|exercise|activity', case=False, regex=True).astype(int)
    df['weather_changes'] = df['symptoms'].str.contains('weather|cold|hot|temperature', case=False, regex=True).astype(int)
    df['stress'] = df['symptoms'].str.contains('stress|anxiety|tension', case=False, regex=True).astype(int)
    
    return df

def generate_fmf_population_data(patient_data):
    """
    Generate mock FMF population data for comparison.
    """
    population_size = 1000
    date_range = pd.date_range(start=patient_data['date'].min(), end=patient_data['date'].max(), periods=population_size)
    
    population_data = pd.DataFrame({
        'date': date_range,
        'age': np.random.randint(5, 50, size=population_size),
        'severity': np.random.randint(1, 10, size=population_size),
        'dosage': np.random.choice([1, 1.5, 2, 2.5], size=population_size)
    })
    
    return population_data

def get_patient_and_population_data():
    patient_data = process_fmf_data()
    population_data = generate_fmf_population_data(patient_data)
    return patient_data, population_data
