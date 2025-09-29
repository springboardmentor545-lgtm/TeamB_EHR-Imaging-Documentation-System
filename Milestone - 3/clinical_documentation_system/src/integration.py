#!/usr/bin/env python3
"""
Clinical Documentation Integration Script - OLLAMA VERSION
"""

import pandas as pd
import requests
import json
import os
import time
import sys
from datetime import datetime

# Import configuration
from config import OPENAI_CONFIG, FILE_PATHS, ICD10_MAPPING

class ClinicalDocumentationSystem:
    def __init__(self):
        """
        Initialize the clinical documentation system with Ollama
        """
        self.icd10_mapping = ICD10_MAPPING
        self.stats = {
            'total_processed': 0,
            'start_time': None,
            'api_errors': 0
        }
    
    def call_ollama(self, prompt, model="medllama2:7b"):
        """
        Call local Ollama model (FREE) - UPDATED PORT to 11435
        """
        url = "http://localhost:11435/api/generate"  # CHANGED FROM 11434 to 11435
        
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.3,
                "num_predict": 800
            }
        }
        
        try:
            response = requests.post(url, json=payload, timeout=120)
            if response.status_code == 200:
                return response.json()["response"]
            else:
                print(f"Ollama error: {response.status_code}")
                return None
        except Exception as e:
            print(f"Ollama connection failed: {e}")
            print("Make sure 'ollama serve' is running on port 11435!")
            return None
    
    def load_patient_data(self, file_path):
        """
        Load and validate patient data from CSV
        """
        print("📥 Loading patient data...")
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Input file not found: {file_path}")
        
        df = pd.read_csv(file_path)
        
        # Validate required columns
        required_columns = ['Patient_ID', 'Age', 'Gender', 'Symptoms', 'Diagnosis']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            raise ValueError(f"Missing columns: {missing_columns}")
        
        print(f"✅ Loaded {len(df)} patient records")
        return df
    
    def generate_clinical_note(self, patient_data):
        """
        Generate professional clinical note using Ollama
        """
        prompt = self._build_clinical_prompt(patient_data)
        
        # Try Ollama first
        print(f"  🤖 Generating AI note for Patient {patient_data['Patient_ID']}...")
        ai_note = self.call_ollama(prompt)
        
        if ai_note:
            return ai_note
        else:
            print(f"  ⚠️ Using fallback note for Patient {patient_data['Patient_ID']}")
            self.stats['api_errors'] += 1
            return self._create_fallback_note(patient_data)
    
    def _build_clinical_prompt(self, patient_data):
        """
        Build detailed prompt for clinical note generation
        """
        return f"""
        You are a medical doctor. Create a professional clinical note in SOAP format.

        PATIENT:
        - Age: {patient_data['Age']}
        - Gender: {patient_data['Gender']}
        - Symptoms: {patient_data['Symptoms']}
        - Diagnosis: {patient_data['Diagnosis']}

        Create a detailed clinical note with these sections:

        SUBJECTIVE:
        Detail the patient's chief complaint and history.

        OBJECTIVE:
        Include physical exam findings and vital signs.

        ASSESSMENT:
        Provide diagnosis and clinical impression.

        PLAN:
        Outline treatment and follow-up recommendations.

        Use medical terminology and be specific.
        """
    
    def get_icd10_code(self, diagnosis, symptoms):
        """
        Get ICD-10 code using enhanced lookup logic
        """
        diagnosis_lower = diagnosis.lower()
        symptoms_lower = symptoms.lower()
        
        # First, try exact diagnosis matches
        for condition, code in self.icd10_mapping.items():
            if condition in diagnosis_lower:
                return code
        
        # Try symptom-based coding for complex cases
        if "adenocarcinoma" in diagnosis_lower or "carcinoma" in diagnosis_lower:
            return "C34.90"  # Lung cancer
        
        if "benign" in diagnosis_lower and any(symptom in symptoms_lower for symptom in ["headache", "vision", "nausea"]):
            return "D49.6"  # Brain neoplasm
        
        if "malignant" in diagnosis_lower and any(symptom in symptoms_lower for symptom in ["headache", "seizures", "confusion"]):
            return "C71.9"  # Brain cancer
        
        # Use AI for complex cases
        return self._get_ai_icd10_code(diagnosis)
    
    def _get_ai_icd10_code(self, diagnosis):
        """
        Use AI for complex ICD-10 coding
        """
        prompt = f"Provide ONLY the ICD-10 code for '{diagnosis}'. No explanations."
        
        ai_code = self.call_ollama(prompt)
        if ai_code and len(ai_code) >= 3:
            # Clean the response - take only the code part
            code = ai_code.strip().split()[0]
            if code[0].isalpha() and any(c.isdigit() for c in code):
                return code
        return "R69"
    
    def _create_fallback_note(self, patient_data):
        """
        Create fallback note when AI fails
        """
        return f"""
CLINICAL NOTE

SUBJECTIVE:
{patient_data['Age']}-year-old {patient_data['Gender']} presents with {patient_data['Symptoms']}.

OBJECTIVE:
Comprehensive examination performed. Findings consistent with reported symptoms.

ASSESSMENT:
{patient_data['Diagnosis']}.

PLAN:
1. Appropriate treatment and monitoring
2. Patient education and follow-up
3. Specialist referral if indicated
"""
    
    def process_patient(self, patient_row):
        """
        Process a single patient record
        """
        patient_id = patient_row['Patient_ID']
        print(f"  Processing Patient {patient_id}: {patient_row['Diagnosis']}")
        
        # Generate clinical note
        clinical_note = self.generate_clinical_note(patient_row)
        
        # Get ICD-10 code
        icd10_code = self.get_icd10_code(patient_row['Diagnosis'], patient_row['Symptoms'])
        
        # Compile results
        result = {
            'Patient_ID': patient_id,
            'Age': patient_row['Age'],
            'Gender': patient_row['Gender'],
            'Symptoms': patient_row['Symptoms'],
            'Diagnosis': patient_row['Diagnosis'],
            'Clinical_Note': clinical_note,
            'ICD10_Code': icd10_code,
            'Processed_At': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        self.stats['total_processed'] += 1
        return result
    
    def save_results(self, results, output_path):
        """
        Save results to output file
        """
        # Create output directory if needed
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        output_df = pd.DataFrame(results)
        output_df.to_csv(output_path, index=False)
        return output_path
    
    def run_integration(self):
        """
        Main integration workflow
        """
        print("🚀 Starting Clinical Documentation Integration (Ollama - Port 11435)")
        self.stats['start_time'] = datetime.now()
        
        try:
            # Step 1: Load patient data
            patient_df = self.load_patient_data(FILE_PATHS["input"])
            
            # Step 2: Process all patients
            print("\n🔄 Generating clinical documentation...")
            results = []
            
            for index, row in patient_df.iterrows():
                result = self.process_patient(row)
                results.append(result)
                
                # Small delay to avoid overwhelming the system
                time.sleep(2)
            
            # Step 3: Save results
            output_path = self.save_results(results, FILE_PATHS["output"])
            
            # Step 4: Display summary
            self._display_summary(results, output_path)
            
            return pd.DataFrame(results)
            
        except Exception as e:
            print(f"❌ Integration failed: {e}")
            raise
    
    def _display_summary(self, results, output_path):
        """
        Display processing summary
        """
        duration = datetime.now() - self.stats['start_time']
        
        print("\n" + "="*60)
        print("📊 CLINICAL DOCUMENTATION SUMMARY")
        print("="*60)
        print(f"Total patients processed: {self.stats['total_processed']}")
        print(f"Output file: {output_path}")
        print(f"Processing time: {duration.total_seconds():.2f} seconds")
        print(f"AI errors: {self.stats['api_errors']}")
        
        # Show diagnosis distribution
        diagnoses = pd.DataFrame(results)['Diagnosis'].value_counts()
        print(f"\nDiagnosis Distribution:")
        for diagnosis, count in diagnoses.items():
            print(f"  - {diagnosis}: {count} patients")
        
        # Show sample output
        if results:
            sample = results[0]
            print(f"\n🔍 SAMPLE OUTPUT (Patient {sample['Patient_ID']}):")
            print(f"Diagnosis: {sample['Diagnosis']}")
            print(f"ICD-10 Code: {sample['ICD10_Code']}")
            print(f"Note Preview: {sample['Clinical_Note'][:200]}...")

def main():
    """
    Main execution function
    """
    print("="*60)
    print("🏥 CLINICAL DOCUMENTATION SYSTEM - OLLAMA VERSION")
    print("Step 4: Integration Prototype with Local AI")
    print("Using Port: 11435")
    print("="*60)
    
    try:
        # Initialize and run system
        clinical_system = ClinicalDocumentationSystem()
        results = clinical_system.run_integration()
        
        print("\n✅ Integration completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Integration failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
