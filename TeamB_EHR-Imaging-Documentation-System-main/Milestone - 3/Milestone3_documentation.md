
# Milestone 3 – Clinical Documentation System

## 1. Introduction
Electronic Health Records (EHRs) form the backbone of digital healthcare. However, transforming **raw patient data** into **structured clinical documentation** is time-consuming for medical staff. This milestone demonstrates how AI can automate:

- Clinical note generation  
- ICD-10 coding  
- Structured storage of patient information  

By integrating **synthetic patient datasets** with **AI-based note generation** (Azure OpenAI / local LLMs) and **ICD-10 mapping**, this prototype simulates a working clinical documentation system.

---

## 2. Objective of Milestone
The objectives of Milestone 3 are:

- To prepare **sample patient data** in CSV and JSON formats.  
- To implement **AI-driven clinical note generation** using Azure OpenAI and BioGPT.  
- To automate **ICD-10 code assignment** via lookup tables and AI fallback.  
- To integrate the full pipeline into a Python script (`integration.py`).  
- To generate structured outputs in CSV, JSON, and TXT formats.  

Ultimately, the system aims to reduce the workload of clinicians by **automating documentation and coding tasks**.

---

## 3. Methodology
The milestone was carried out in the following steps:

### Step 1: Sample Patient Data Preparation
- Created **synthetic cases** covering common diagnoses:
  - Benign & malignant tumors
  - Lung cancer subtypes (adenocarcinoma, squamous carcinoma, large cell carcinoma)
  - Pneumonia
  - Routine/normal scans
  - Other conditions (fractures, kidney stones)
- Stored in:
  - `patient_inputs.csv`
  - `patient_inputs.json`

### Step 2: Clinical Note Generation
- Used **Azure OpenAI GPT-4o** and **BioGPT (local)** to generate notes.  
- Notes follow a structured format (SOAP):

Patient: <Age, Gender>
Presenting Complaints: <Symptoms>
Assessment: <Likely Diagnosis>
ICD-10 Code: <Mapped Code>
Plan: <Investigations/Treatment>


### Step 3: ICD-10 Coding
Two approaches were implemented:
1. **Lookup Table (config.py)**  
   Example:
   - Pneumonia → J18.9  
   - Malignant tumor → C71.9  
   - Hypertension → I10  
   - Diabetes → E11.9  

2. **AI-driven Fallback**  
   If no match is found, the AI model is queried for ICD-10 code suggestions.

### Step 4: Integration Script
The `integration.py` script:
- Reads patient data from CSV/JSON  
- Sends details to AI model → generates a note  
- Maps diagnosis to ICD-10 code (lookup + AI fallback)  
- Stores results in:
  - `output.csv`
  - `output_results.json`
  - `clinical_notes.txt`

### Step 5: Azure Demo
- **Playground Demo**: Chat-based note generation  
- **Cloud Shell Demo**: Python client app using GPT-4o with structured system prompts  

---

## 4. Implementation
### Tools & Libraries
- **Python** (pandas, requests, transformers, torch)  
- **Azure OpenAI** (GPT-4o deployment)  
- **Ollama** for running `medllama2:7b` locally  
- **BioGPT** (`microsoft/BioGPT-Large`) for medical note generation  

### Folder Structure
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

### Example Input (patient_inputs.csv)
Patient_ID,Age,Gender,Symptoms,Diagnosis
8,37,Female,Fever, cough, shortness of breath,Pneumonia

shell
Copy code

### Example Output (output.csv)
Patient_ID,Symptoms,Diagnosis,Clinical_Note,ICD10_Code
8,"Fever, cough, shortness of breath","Pneumonia",
"Patient: 37-year-old female
Presenting Complaints: Fever, cough, shortness of breath
Assessment: Likely pneumonia
Plan: Recommend chest X-ray and antibiotics",J18.9


---

## 5. Results
### Clinical Notes
- Generated structured notes for all 13 patients.  
- Notes included **Assessment** and **Plan** (investigations, treatment, monitoring).  

### ICD-10 Coding
- Correct mapping for common cases (e.g., Pneumonia → J18.9, Malignant tumor → C71.9).  
- AI fallback successfully provided codes for ambiguous conditions.  

### Output Files
- **CSV (`output.csv`)**: Tabular notes + ICD-10 codes  
- **JSON (`output_results.json`)**: Structured evaluation format  
- **TXT (`clinical_notes.txt`)**: Readable notes for clinicians  

---

## 6. Conclusion
This milestone successfully demonstrated a **prototype clinical documentation system** that can:
- Transform structured patient data into professional notes.  
- Automate ICD-10 coding.  
- Output results in multiple formats for integration with EHR systems.  

The system provides a foundation for real-world clinical documentation automation, reducing clinician workload and improving standardization.

---

## 7. References
- OpenCV Documentation – https://docs.opencv.org/  
- Scikit-learn Documentation – https://scikit-learn.org/  
- Azure OpenAI Documentation – https://learn.microsoft.com/en-us/azure/ai-services/openai  
- ICD-10 Codes – https://icd10cmtool.cdc.gov/  
- BioGPT Model – https://huggingface.co/microsoft/BioGPT-Large  
- Ollama – https://ollama.ai/  

---
