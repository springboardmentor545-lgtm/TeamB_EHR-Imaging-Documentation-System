# TeamB_EHR-Imaging-Documentation-System

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

Enhancing_EHRs_with_GenAI/
│
├── data/
│ ├── images/
│ │ ├── MRI_001.png
│ │ ├── MRI_002.png
│ │ └── CT_001.png
│ │
│ ├── ehr_notes/
│ │ ├── note_001.txt
│ │ ├── note_002.txt
│ │ └── note_003.txt
│ │
│ ├── mapping.csv
│
├── docs/
│ ├── dataset_sources.md
│ ├── cleaning_steps.md
│ └── challenges.md
│
└── README.md
