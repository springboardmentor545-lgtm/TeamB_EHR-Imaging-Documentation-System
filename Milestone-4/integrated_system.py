#!/usr/bin/env python3
"""
Integrated System for EHR Imaging Documentation
This script demonstrates the complete workflow:
1. Image Enhancement
2. Clinical Note Generation
3. ICD-10 Coding
4. Database Storage
"""

import cv2
import numpy as np
from typing import Dict, Any
import json
import sys
import os

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import all modules
from image_enhancement import enhance_image, compare_image_quality
from clinical_note_generator import generate_clinical_note, extract_icd_codes
from database import get_db_session, PatientRecord, ClinicalNote, ImageStudy, create_tables


def load_image_from_file(file_path: str) -> np.ndarray:
    """Load an image from file path"""
    image = cv2.imread(file_path)
    if image is None:
        raise ValueError(f"Could not load image from {file_path}")
    return image


def process_medical_image_pipeline(
    image_input: str,
    patient_data: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Complete pipeline processing for medical images:
    1. Load and enhance image
    2. Generate clinical note
    3. Extract ICD-10 codes
    4. Store results in database
    
    Args:
        image_input: Path to the image file
        patient_data: Dictionary containing patient information
        
    Returns:
        Dictionary with processing results
    """
    print("Starting medical image processing pipeline...")
    
    # Step 1: Load original image
    print("1. Loading original image...")
    original_image = load_image_from_file(image_input)
    print(f"   Original image shape: {original_image.shape}")
    
    # Step 2: Enhance image
    print("2. Enhancing image...")
    enhanced_image = enhance_image(original_image)
    quality_metrics = compare_image_quality(original_image, enhanced_image)
    print(f"   Enhanced image shape: {enhanced_image.shape}")
    print(f"   Quality improvement: {quality_metrics['contrast_improvement']:.2f}")
    
    # Step 3: Generate clinical note
    print("3. Generating clinical note...")
    clinical_note = generate_clinical_note(patient_data)
    print(f"   Generated note length: {len(clinical_note)} characters")
    
    # Step 4: Extract ICD-10 codes
    print("4. Extracting ICD-10 codes...")
    icd_codes = extract_icd_codes(clinical_note)
    print(f"   Extracted {len(icd_codes)} ICD-10 codes")
    
    # Step 5: Store in database
    print("5. Storing results in database...")
    db = next(get_db_session())
    
    # Create or update patient record
    patient_record = PatientRecord(
        patient_id=patient_data["patient_info"]["patient_id"],
        patient_name=patient_data["patient_info"]["name"],
        age=patient_data["patient_info"]["age"],
        gender=patient_data["patient_info"]["gender"],
        medical_history=patient_data.get("medical_history", "")
    )
    db.add(patient_record)
    db.commit()
    db.refresh(patient_record)
    
    # Store image study
    _, enhanced_buffer = cv2.imencode('.png', enhanced_image)
    enhanced_bytes = enhanced_buffer.tobytes()
    
    _, original_buffer = cv2.imencode('.png', original_image)
    original_bytes = original_buffer.tobytes()
    
    image_study = ImageStudy(
        patient_id=patient_record.id,
        study_type=patient_data.get("study_type", "Unknown Study"),
        original_image=original_bytes,
        enhanced_image=enhanced_bytes
    )
    db.add(image_study)
    db.commit()
    db.refresh(image_study)
    
    # Store clinical note
    clinical_note_record = ClinicalNote(
        patient_id=patient_record.id,
        image_study_id=image_study.id,
        note_text=clinical_note,
        icd_codes=json.dumps(icd_codes)
    )
    db.add(clinical_note_record)
    db.commit()
    
    print("   Data successfully stored in database")
    
    # Prepare results
    results = {
        "success": True,
        "patient_record_id": patient_record.id,
        "image_study_id": image_study.id,
        "enhanced_image": enhanced_image,
        "clinical_note": clinical_note,
        "icd_codes": icd_codes,
        "quality_metrics": quality_metrics,
        "message": "Medical image processed successfully"
    }
    
    print("Pipeline completed successfully!")
    return results


def test_modules_individually():
    """Test each module individually to ensure they work"""
    print("Testing individual modules...")
    
    # Test image enhancement
    try:
        test_image = np.random.randint(0, 255, (100, 100), dtype=np.uint8)
        enhanced = enhance_image(test_image)
        print("✓ Image enhancement module working")
    except Exception as e:
        print(f"✗ Image enhancement failed: {e}")
        return False
    
    # Test clinical note generation
    try:
        test_data = {
            "patient_info": {
                "patient_id": "TEST001",
                "name": "John Doe",
                "age": 45,
                "gender": "Male"
            },
            "medical_history": "Hypertension, diabetes",
            "current_symptoms": "Chest pain and fever",
            "study_type": "Chest X-Ray"
        }
        note = generate_clinical_note(test_data)
        codes = extract_icd_codes(note)
        print("✓ Clinical note generation working")
        print("✓ ICD-10 coding working")
    except Exception as e:
        print(f"✗ Clinical note generation failed: {e}")
        return False
    
    print("All modules tested successfully!")
    return True


def main():
    """Main function demonstrating the integrated system"""
    print("EHR Imaging Documentation System - Integrated Pipeline")
    print("=" * 60)
    
    # Initialize database
    print("Initializing database...")
    create_tables()
    print("Database initialized successfully!")
    
    # Test individual modules
    if not test_modules_individually():
        print("Module testing failed. Exiting.")
        return
    
    # Example usage with sample data
    print("\nRunning example pipeline...")
    
    # Generate unique patient ID to avoid database conflicts
    import time
    unique_id = f"PAT{int(time.time())}"
    
    # Sample patient data
    patient_data = {
        "patient_info": {
            "patient_id": unique_id,
            "name": "Jane Smith",
            "age": 35,
            "gender": "Female"
        },
        "medical_history": "Asthma, Allergic rhinitis",
        "current_symptoms": "Chest pain and shortness of breath",
        "study_type": "Chest X-Ray"
    }
    
    # Try to use an existing image file or create a sample
    image_file = "sample_image.png"
    if not os.path.exists(image_file):
        # Create a sample image for testing
        print(f"Creating sample image: {image_file}")
        sample_image = np.random.randint(100, 200, (300, 300), dtype=np.uint8)
        cv2.rectangle(sample_image, (50, 50), (250, 250), 50, 30)
        cv2.circle(sample_image, (150, 150), 40, 80, -1)
        cv2.imwrite(image_file, sample_image)
    
    try:
        # Run the complete pipeline
        results = process_medical_image_pipeline(image_file, patient_data)
        
        print("\nProcessing Results:")
        print("-" * 30)
        print(f"Success: {results['success']}")
        print(f"Patient Record ID: {results['patient_record_id']}")
        print(f"Image Study ID: {results['image_study_id']}")
        print(f"Enhanced Image Shape: {results['enhanced_image'].shape}")
        print(f"Note Length: {len(results['clinical_note'])} characters")
        print(f"ICD Codes Found: {len(results['icd_codes'])}")
        print(f"Quality Improvement: {results['quality_metrics']['contrast_improvement']:.2f}")
        
        print("\nFirst 200 characters of clinical note:")
        print(results['clinical_note'][:200] + "...")
        
        print("\nExtracted ICD Codes:")
        for code in results['icd_codes']:
            print(f"  - {code['code']}: {code['description']}")
            
    except Exception as e:
        print(f"Pipeline execution failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()