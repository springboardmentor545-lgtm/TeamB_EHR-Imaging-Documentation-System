#!/usr/bin/env python3
"""
Simple test script to verify all modules work together
"""

import sys
import os

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_integration():
    """Test the integrated system"""
    print("Testing integrated system...")
    
    try:
        # Import our integrated system
        from integrated_system import test_modules_individually, process_medical_image_pipeline
        
        # Test individual modules
        if not test_modules_individually():
            print("Individual module tests failed")
            return False
            
        # Test the complete pipeline
        import time
        patient_data = {
            "patient_info": {
                "patient_id": f"TEST{int(time.time())}",
                "name": "John Doe",
                "age": 45,
                "gender": "Male"
            },
            "medical_history": "Hypertension, diabetes",
            "current_symptoms": "Chest pain and fever",
            "study_type": "Chest X-Ray"
        }
        
        # Create a sample image for testing
        import cv2
        import numpy as np
        sample_image = np.random.randint(100, 200, (300, 300), dtype=np.uint8)
        cv2.rectangle(sample_image, (50, 50), (250, 250), 50, 30)
        cv2.circle(sample_image, (150, 150), 40, 80, -1)
        cv2.imwrite("test_sample.png", sample_image)
        
        # Run the pipeline
        results = process_medical_image_pipeline("test_sample.png", patient_data)
        
        if results["success"]:
            print("✓ Integration test passed!")
            print(f"  - Patient Record ID: {results['patient_record_id']}")
            print(f"  - Image Study ID: {results['image_study_id']}")
            print(f"  - Enhanced image shape: {results['enhanced_image'].shape}")
            print(f"  - ICD codes extracted: {len(results['icd_codes'])}")
            return True
        else:
            print("✗ Integration test failed")
            return False
            
    except Exception as e:
        print(f"✗ Integration test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_integration()
    if success:
        print("\n🎉 All integration tests passed!")
        sys.exit(0)
    else:
        print("\n❌ Integration tests failed!")
        sys.exit(1)