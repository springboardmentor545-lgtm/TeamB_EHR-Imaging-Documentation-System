# EHR Imaging Documentation System

A unified system that integrates medical image enhancement, clinical note generation, and ICD-10 coding into a single workflow.

## System Architecture

The system consists of three main modules that work together:

1. **Image Enhancement Module** ([image_enhancement.py](file:///c%3A/Users/anush/OneDrive/Documents/TeamB_EHR-Imaging-Documentation-System/image_enhancement.py))
   - Enhances medical images using CLAHE, noise reduction, and sharpening
   - Improves diagnostic quality of medical images

2. **Clinical Note Generation Module** ([clinical_note_generator.py](file:///c%3A/Users/anush/OneDrive/Documents/TeamB_EHR-Imaging-Documentation-System/clinical_note_generator.py))
   - Generates structured clinical notes based on patient data
   - Extracts ICD-10 diagnostic codes from clinical content

3. **Database Module** ([database.py](file:///c%3A/Users/anush/OneDrive/Documents/TeamB_EHR-Imaging-Documentation-System/database.py))
   - Stores patient records, image studies, and clinical documentation
   - Maintains relational integrity between all data components

## Integration Flow

The complete workflow is implemented in two ways:

1. **API Service** ([main.py](file:///c%3A/Users/anush/OneDrive/Documents/TeamB_EHR-Imaging-Documentation-System/main.py))
   - RESTful API with FastAPI
   - Exposes endpoint `/process-medical-image` for processing medical images
   - Provides data retrieval endpoints

2. **Direct Integration** ([integrated_system.py](file:///c%3A/Users/anush/OneDrive/Documents/TeamB_EHR-Imaging-Documentation-System/integrated_system.py))
   - Direct function calls for programmatic access
   - Can be imported and used in other Python applications

## How to Use

### Starting the API Server

```bash
python main.py
```

The API will be available at `http://localhost:8000`

### Processing Images via API

Send a POST request to `/process-medical-image` with:
- Patient data in form fields
- Medical image as file upload

### Direct Integration Usage

```python
from integrated_system import process_medical_image_pipeline

patient_data = {
    "patient_info": {
        "patient_id": "PAT001",
        "name": "John Doe",
        "age": 35,
        "gender": "Male"
    },
    "medical_history": "Asthma",
    "current_symptoms": "Chest pain",
    "study_type": "Chest X-Ray"
}

results = process_medical_image_pipeline("path/to/image.png", patient_data)
```

### Individual Module Usage

Each module can be used independently:

```python
# Image Enhancement
from image_enhancement import enhance_image
enhanced = enhance_image("path/to/image.png")

# Clinical Note Generation
from clinical_note_generator import generate_clinical_note
note = generate_clinical_note(patient_data)

# ICD-10 Coding
from clinical_note_generator import extract_icd_codes
codes = extract_icd_codes(clinical_note)
```

## Testing

Run integration tests:
```bash
python test_modules.py
```

## Dependencies

See [requirements.txt](file:///c%3A/Users/anush/OneDrive/Documents/TeamB_EHR-Imaging-Documentation-System/requirements.txt) for a complete list of dependencies.

## Database

The system uses SQLite for data storage. The database file is `ehr_system.db`.
