"""
Integration Tests for EHR Imaging Documentation System

This file tests the complete integration of all modules:
1. Image Enhancement Module
2. Clinical Note Generation Module
3. ICD-10 Coding Module
4. Database Storage Module

The tests verify that data flows correctly between modules.
"""
import requests
import json
import base64
import cv2
import numpy as np
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_individual_modules():
    """Test each module individually"""
    print("Testing individual modules...")
    
    try:
        from image_enhancement import enhance_image
        test_image = np.random.randint(0, 255, (100, 100), dtype=np.uint8)
        enhanced = enhance_image(test_image)
        print("✓ Image enhancement module working")
        print(f"  Original shape: {test_image.shape}, Enhanced shape: {enhanced.shape}")
        
        from clinical_note_generator import generate_clinical_note, extract_icd_codes
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
        print(f"  Note length: {len(note)} characters")
        print("✓ ICD-10 coding working")
        print(f"  Extracted {len(codes)} ICD codes")
        
        return True
        
    except Exception as e:
        print(f"✗ Module testing failed: {e}")
        return False

def test_integrated_flow():
    """Test the complete integrated flow via API"""
    print("\nTesting integrated flow via API...")
    
    test_image = np.random.randint(0, 255, (200, 200), dtype=np.uint8)
    _, buffer = cv2.imencode('.png', test_image)
    image_bytes = buffer.tobytes()
    
    patient_data = {
        "patient_id": "TEST001",
        "patient_name": "John Doe",
        "age": 45,
        "gender": "Male",
        "medical_history": "Hypertension, diabetes mellitus",
        "current_symptoms": "Chest pain and persistent cough",
        "study_type": "Chest X-Ray"
    }
    
    files = {'image_file': ('test_image.png', image_bytes, 'image/png')}
    
    try:
        response = requests.post(
            "http://localhost:8000/process-medical-image",
            data=patient_data,
            files=files,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✓ Integrated flow working")
            print(f"  - Success: {result['success']}")
            print(f"  - Enhanced image generated: {result['enhanced_image'] is not None}")
            print(f"  - Clinical note generated: {len(result['clinical_note']) > 0}")
            print(f"  - ICD codes extracted: {len(result['icd_codes']) > 0}")
            print(f"  - Patient record ID: {result['patient_record_id']}")
            return True
        else:
            print(f"✗ API returned status code: {response.status_code}")
            print(f"  Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"✗ API request failed: {e}")
        print("  Make sure the server is running: python main.py")
        return False

def create_sample_image(filename="sample_image.png"):
    """Create a sample medical-like image for testing"""
    image = np.random.randint(100, 200, (300, 300), dtype=np.uint8)
    cv2.rectangle(image, (50, 50), (250, 250), 50, 30)
    cv2.circle(image, (150, 150), 40, 80, -1)
    cv2.imwrite(filename, image)
    print(f"✓ Created sample image: {filename}")
    return filename

if __name__ == "__main__":
    print("EHR System Integration Tests")
    print("=" * 50)
    
    modules_ok = test_individual_modules()
    sample_image = create_sample_image()
    
    print("\nNote: For integrated flow test, run the server first:")
    print("python main.py")
    print("Then run: python test_integration.py")
    
    choice = input("\nDo you want to test the API flow now? (y/n): ")
    if choice.lower() == 'y':
        test_integrated_flow()