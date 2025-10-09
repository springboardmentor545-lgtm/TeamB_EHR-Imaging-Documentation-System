# TeamB_EHR-Imaging-Documentation-System

# Milestone 1:

## Steps to Prepare the Dataset

1. **Collect datasets**

   - Search open sources like Kaggle, PhysioNet, NIH.
   - Download MRI, CT, and EHR datasets that are openly licensed.

2. **Organize into folders**

   - Create a root project folder.
   - Inside it, keep two main folders: `images` and `ehr_notes`.
   - Name files properly (for example: `MRI_001.png`, `CT_002.png`, `note_001.txt`).

3. **Create mapping file**

   - Use Excel or Google Sheets to make a structured dataset mapping.
   - Columns: `filename`, `modality`, `diagnosis`, `ICD10_code`.
   - Fill in rows according to each file.
   - Export as `mapping.csv`.

4. **Document everything**
   - `docs/dataset_sources.md`: Mention where datasets came from (with links).
   - `docs/cleaning_steps.md`: Record what cleaning you did (renaming, removing duplicates, converting formats).
   - `docs/challenges.md`: Note difficulties faced (for example, missing labels).
   - `README.md`: Explain folder structure and how data is linked.

## Project Folder Structure

TeamB_EHR-Imaging-Documentation-System/

├──  data/

│    ├── images/

│    │      ├── MRI_001.png

│    │      ├── MRI_002.png

│    │      └── CT_001.png

│    ├──    ehr_notes/

│           ├── note_001.txt

│           ├── note_002.txt

│           └── note_003.txt

│    └── mapping.csv

├──    docs/

│      ├── dataset_sources.md

│      ├── cleaning_steps.md

│      └── challenges.md

└── README.md




# Milestone 2: Medical Imaging Enhancement

**Project Overview**  
This milestone focuses on enhancing medical images (X-rays, MRIs, CT scans) using **SRCNN (Super-Resolution Convolutional Neural Network)**.  
The goal is to improve image clarity, remove blur/noise, and provide healthcare professionals with diagnostic-quality visuals before storing them in Electronic Health Records (EHRs).

## Steps Completed in Milestone 2

### Dataset Preparation

- Used sample medical images stored in `data/images/`.
- Mapping done via `mapping.csv` for easier identification.
- Generated **HQ–LQ paired datasets** by applying Gaussian blur.
- Extracted patches (e.g., 32×32) for efficient training.

### Preprocessing

- Converted to grayscale when needed.
- Normalized pixel values to range `[0, 1]`.
- Created train/test splits.

### Enhancement Technique Applied

- **SRCNN (Super-Resolution Convolutional Neural Network):**
  - Input → Low-quality (blurred) image patches.
  - Output → Reconstructed high-quality patches.
  - Model trained on HQ–LQ patch pairs.
  - Saved best weights for reconstruction.

### Validation

- Compared **Original vs Blurred vs Enhanced** images visually.
- Calculated **PSNR (Peak Signal-to-Noise Ratio)** and **SSIM (Structural Similarity Index)**.

## Challenges Faced

- Training required GPU (Colab used).
- Some results initially blurred; patch extraction improved learning.
- Handling large image sets was time-consuming.

## Results

- **Visual Improvement:**  
  Enhanced images show clearer details compared to blurred inputs.

- **Quantitative Improvement:**
  - **PSNR:** Increased, showing better image quality.
  - **SSIM:** Higher values, closer to original HQ images.

## Conclusion

- Successfully implemented **SRCNN-based medical image enhancement**.
- Results demonstrated clear improvements in visibility and diagnostic usefulness.
- Enhanced images will strengthen the reliability of medical data stored in EHR systems.

## Folder Structure

Milestone-2/

├── Preprocessed/

├── dataset/

├── test/

├── train/

├── Enhancement_Techniques/

├── Validation/

├── Challenges_Faced/

├──   images_for_doc/

│     ├── T1.jpeg

│     ├── T2.jpeg

│     ├── T3.jpeg

│     ├── T4.jpeg

│     └── T5.jpeg

├── milestone2_documentation.md

└── Tasks_Distribution_for_Milestone-2/

Milestone 3: Clinical Documentation System
==========================================

Project Overview
----------------
This milestone focuses on automating clinical documentation using AI. The system takes patient data, generates structured clinical notes, assigns ICD-10 codes, and outputs results in multiple formats (CSV, JSON, TXT). This reduces clinician workload and improves standardization in Electronic Health Records (EHRs).

Steps Completed in Milestone 3
------------------------------

### 1. Sample Patient Data Preparation
- Created synthetic patient cases covering common diagnoses:
  - Benign & malignant tumors
  - Lung cancer subtypes (adenocarcinoma, squamous carcinoma, large cell carcinoma)
  - Pneumonia
  - Routine/normal scans
  - Other conditions (fractures, kidney stones)
- Stored data in:
  - `data/patient_inputs.csv`
  - `data/patient_inputs.json`

### 2. Clinical Note Generation
- Used **Azure OpenAI GPT-4o** and **BioGPT (local)** to generate structured clinical notes in SOAP format:
Patient: <Age, Gender>
Presenting Complaints:
Assessment:
ICD-10 Code:
Plan: <Investigations/Treatment>

### 3. ICD-10 Coding
- **Lookup Table Approach:** Configured in `src/config.py` for common diagnoses.
- Example: Pneumonia → J18.9, Malignant tumor → C71.9
- **AI-driven Fallback:** For unknown cases, the AI model suggests ICD-10 codes.

### 4. Integration Script
- `src/integration.py` performs the full pipeline:
1. Reads patient data from CSV/JSON.
2. Generates AI-driven clinical notes.
3. Assigns ICD-10 codes using lookup + AI fallback.
4. Saves results in:
   - `data/output.csv`
   - `data/output_results.json`
   - `clinical_note_generation/clinical_notes.txt`

### 5. Azure Demo
- Playground: Chat-based note generation
- Cloud Shell: Python client app using GPT-4o with structured prompts

Results
-------
- Generated structured notes for 13 patients including Assessment and Plan.
- Accurate ICD-10 coding; AI fallback handled ambiguous cases.
- Outputs are ready for integration with EHR systems.

Conclusion
----------
- Successfully automated clinical documentation and ICD-10 coding.
- Outputs available in multiple formats for real-world adoption.
- Reduces clinician workload and improves standardization.

Folder Structure
----------------
Milestone-3/

clinical_documentation_system/
├── data/

│ ├── patient_inputs.csv

│ ├── patient_inputs.json

│ ├── output.csv

│ └── output_results.json

├── clinical_note_generation/

│ ├── clinical_notes.txt

│ └── step2_azure_demo.md

├── src/

│ ├── config.py

│ └── integration.py

├── requirements.txt

└── README.md
