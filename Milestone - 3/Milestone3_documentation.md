# Milestone 3 – Clinical Documentation System

This milestone demonstrates how to build an **AI-assisted clinical documentation system** that generates medical notes and ICD-10 codes from structured patient data.

---

##  Folder Structure
clinical_documentation_system/
│── data/ # Input & output files
│ ├── patient_inputs.csv # Sample patient data (CSV)
│ ├── patient_inputs.json # Sample patient data (JSON)
│ ├── output.csv # Generated clinical notes + ICD-10 codes
│ ├── output_results.json # Same output in JSON format
│
│── clinical_note_generation/
│ ├── clinical_notes.txt # Example generated notes
│ ├── step2_azure_demo.md # Demo of Azure OpenAI integration
│
│── src/
│ ├── config.py # Configuration (API keys, settings)
│ ├── integration.py # Main script to generate notes + ICD-10 codes
│
│── requirements.txt # Python dependencies


---

##  Step 1: Prepare Sample Patient Data

Since we cannot use real patient data, we create **synthetic cases**.

Example patient record:

- **Age**: 45  
- **Gender**: Male  
- **Symptoms**: Fever, cough, shortness of breath  
- **Diagnosis**: Possible pneumonia  

This data is stored in both CSV and JSON formats:  
- `patient_inputs.csv`  
- `patient_inputs.json`

 At least **5–10 cases** are included.

---

##  Step 2: Clinical Note Generation (Azure OpenAI)

We use Azure OpenAI (GPT-4/3.5) to convert structured data into professional medical notes.

Example input → output:

**Input:**  

Age: 45, Male
Symptoms: Fever, cough, shortness of breath
Diagnosis: Possible pneumonia


**Generated Note:**  
Patient: 45-year-old male
Presenting complaints: Fever, cough, shortness of breath
Assessment: Likely pneumonia based on symptoms
Plan: Recommend chest X-ray and antibiotics


---

##  Step 3: ICD-10 Coding Automation

ICD-10 codes are added automatically. Two options are supported:

1. **Lookup Table (CSV/JSON):**  
Pneumonia → J18.9
Diabetes → E11.9
Hypertension → I10


2. **AI-driven:** Ask the model for the ICD-10 code.

 Output now includes both the clinical note **and** ICD-10 code.

---

##  Step 4: Integration Script

The script `integration.py` performs the following:

1. Reads patient data from CSV/JSON.  
2. Sends input to Azure OpenAI → generates a note.  
3. Maps diagnosis to ICD-10 code.  
4. Saves results into:  
- `output.csv`  
- `output_results.json`

---

##  Step 5: Outputs

Example output row in `output.csv`:

| Patient | Symptoms                  | Note Generated                                     | ICD-10 Code |
|---------|---------------------------|----------------------------------------------------|-------------|
| 1       | Fever, cough, breathless  | Patient shows signs of pneumonia… Chest X-ray…     | J18.9       |

---

##  Setup & Installation

Install dependencies:
pip install -r requirements.txt
Run the integration script:
python src/integration.py

Outputs will be saved in the data/ folder.

##  Deliverables for Milestone 3

Input files: patient_inputs.csv, patient_inputs.json

Code: integration.py, config.py

Output files: output.csv, output_results.json

Documentation: MILESTONE3.md (this file)

