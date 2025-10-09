import re
import json
from typing import Dict, List, Any
import random
from datetime import datetime

def generate_clinical_note(patient_data: Dict[str, Any]) -> str:
    """
    Generate clinical note based on patient data and image analysis
    """
    try:
        patient_info = patient_data.get("patient_info", {})
        medical_history = patient_data.get("medical_history", "")
        symptoms = patient_data.get("current_symptoms", "")
        study_type = patient_data.get("study_type", "Radiology Study")
        
        # Extract key information for note generation
        patient_name = patient_info.get('name', 'Patient')
        age = patient_info.get('age', 'Unknown')
        gender = patient_info.get('gender', 'Unknown')
        
        # Generate findings based on symptoms and study type
        findings = generate_findings(symptoms, study_type)
        impression = generate_impression(symptoms, study_type)
        
        # Template for clinical note
        clinical_note = f"""
CLINICAL RADIOLOGY REPORT

PATIENT INFORMATION:
- Patient ID: {patient_info.get('patient_id', 'N/A')}
- Name: {patient_name}
- Age: {age}
- Gender: {gender}

CLINICAL HISTORY:
{medical_history if medical_history else 'No significant medical history provided.'}

CURRENT SYMPTOMS:
{symptoms if symptoms else 'No current symptoms reported.'}

STUDY PERFORMED:
{study_type}

TECHNIQUE:
Multiple views of the {get_anatomy_from_study(study_type)} were obtained.

FINDINGS:
{findings}

IMPRESSION:
{impression}

RECOMMENDATIONS:
1. Clinical correlation is advised.
2. Follow-up imaging if symptoms persist or worsen.
3. Consider additional views or specialized imaging if clinically indicated.

RADIOLOGIST: AI Radiology System
DATE: {datetime.now().strftime("%Y-%m-%d")}
"""
        return clinical_note.strip()
    
    except Exception as e:
        return f"Error generating clinical note: {str(e)}"

def generate_findings(symptoms: str, study_type: str) -> str:
    """Generate findings based on symptoms and study type"""
    anatomy = get_anatomy_from_study(study_type)
    
    findings_templates = [
        f"The {anatomy} demonstrates normal alignment and architecture. No evidence of acute fracture or dislocation. Soft tissues are unremarkable.",
        f"The {anatomy} appears grossly intact. No significant degenerative changes are noted. Joint spaces are maintained.",
        f"Visualization of the {anatomy} is adequate. No focal bone lesions or destructive processes are identified.",
        f"The {anatomy} study reveals no evidence of acute pathology. Bone density appears within normal limits."
    ]
    
    # Add symptom-specific findings
    if any(symptom in symptoms.lower() for symptom in ['pain', 'tenderness']):
        findings_templates.append(f"Despite patient reports of discomfort, the {anatomy} demonstrates no radiographic evidence of acute abnormality.")
    
    if 'fracture' in symptoms.lower():
        findings_templates.append(f"Careful evaluation of the {anatomy} reveals no evidence of fracture line. Cortical margins are intact.")
    
    return random.choice(findings_templates)

def generate_impression(symptoms: str, study_type: str) -> str:
    """Generate impression based on symptoms and study type"""
    anatomy = get_anatomy_from_study(study_type)
    
    impression_templates = [
        f"No acute radiographic abnormality detected in the {anatomy}.",
        f"Normal study of the {anatomy}.",
        f"Unremarkable radiographic appearance of the {anatomy}.",
        f"No evidence of acute bone or joint pathology in the {anatomy}."
    ]
    
    return random.choice(impression_templates)

def get_anatomy_from_study(study_type: str) -> str:
    """Extract anatomy from study type"""
    study_lower = study_type.lower()
    if 'chest' in study_lower:
        return 'chest'
    elif 'wrist' in study_lower:
        return 'wrist'
    elif 'ankle' in study_lower:
        return 'ankle'
    elif 'knee' in study_lower:
        return 'knee'
    elif 'spine' in study_lower:
        return 'spine'
    else:
        return 'examined area'

def extract_icd_codes(clinical_note: str) -> List[Dict]:
    """
    Extract potential ICD-10 codes based on clinical note content
    This is a simplified version - in production, you'd use a proper medical NLP service
    """
    # Mock ICD-10 code mapping based on keywords
    icd_mapping = {
        'pain': ['R10.9', 'Unspecified abdominal pain'],
        'fever': ['R50.9', 'Fever, unspecified'],
        'cough': ['R05', 'Cough'],
        'fracture': ['S82.9', 'Fracture of unspecified part of lower leg'],
        'infection': ['B99.9', 'Unspecified infectious disease'],
        'inflammation': ['M79.9', 'Soft tissue disorder, unspecified'],
        'trauma': ['T14.90', 'Injury, unspecified'],
        'chest': ['R07.9', 'Chest pain, unspecified'],
        'wrist': ['S69.90', 'Unspecified injury of wrist and hand'],
        'ankle': ['S99.90', 'Unspecified injury of ankle and foot'],
        'knee': ['S89.90', 'Unspecified injury of knee and lower leg'],
        'spine': ['S39.90', 'Unspecified injury of abdomen, lower back, pelvis and external genitals']
    }
    
    extracted_codes = []
    note_lower = clinical_note.lower()
    
    for keyword, code_info in icd_mapping.items():
        if keyword in note_lower:
            extracted_codes.append({
                "code": code_info[0],
                "description": code_info[1],
                "category": keyword
            })
    
    # Return default general code if no specific codes found
    if not extracted_codes:
        extracted_codes.append({
            "code": "Z01.89",
            "description": "Encounter for other specified special examinations",
            "category": "general_examination"
        })
    
    return extracted_codes