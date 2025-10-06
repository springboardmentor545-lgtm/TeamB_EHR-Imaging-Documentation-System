"""
Configuration for Clinical Documentation System - OLLAMA VERSION
"""

# Configuration structure (compatible with both, but we use Ollama)
OPENAI_CONFIG = {
    "model": "gpt-3.5-turbo",  # Not used in Ollama, but kept for compatibility
    "max_tokens": 800,
    "temperature": 0.3,
    "request_delay": 2.0  # Used for delay between requests
}

# File Paths
FILE_PATHS = {
    "input": "data/input/patient_inputs.csv",
    "output": "data/output/clinical_documentation_output.csv"
}

# Enhanced ICD-10 Mapping for your specific dataset
ICD10_MAPPING = {
    # Brain conditions
    "benign": "D49.6",  # Neoplasm of uncertain behavior of brain
    "malignant": "C71.9",  # Malignant neoplasm of brain, unspecified
    
    # Lung conditions
    "pneumonia": "J18.9",  # Pneumonia, unspecified organism
    "adenocarcinoma": "C34.90",  # Malignant neoplasm of bronchus or lung
    "large.cell.carcinoma": "C34.90",  # Malignant neoplasm of bronchus or lung
    "squamous.cell.carcinoma": "C34.90",  # Malignant neoplasm of bronchus or lung
    
    # Urinary conditions
    "stone": "N20.0",  # Calculus of kidney
    
    # Musculoskeletal conditions
    "fractured": "S02.91XA",  # Fracture of unspecified bone
    "fracture": "S02.91XA",  # Fracture of unspecified bone
    
    # Normal findings
    "normal": "Z00.00",  # General medical examination without abnormal findings
    "not fractured": "Z01.89",  # Other specified special examinations
    
    # Symptom codes (fallback)
    "headache": "R51",
    "seizures": "R56.9",
    "confusion": "R41.0",
    "vision problems": "H53.9",
    "nausea": "R11.0",
    "chest tightness": "R07.89",
    "weight loss": "R63.4",
    "chronic cough": "R05",
    "weakness": "R53.1",
    "fatigue": "R53.83",
    "chest pain": "R07.9",
    "difficulty breathing": "R06.00",
    "fever": "R50.9",
    "shortness of breath": "R06.02",
    "abdominal pain": "R10.9",
    "painful urination": "R30.9",
    "swelling": "R22.9",
    "pain": "R52",
    "difficulty in movement": "R25.8"
}
