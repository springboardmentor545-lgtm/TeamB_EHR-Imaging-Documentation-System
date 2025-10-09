# test_api.py - CORRECTED VERSION
import requests
import json
import os

print("Testing EHR Imaging System API...")
print("=" * 50)

# Prepare patient data
patient_data = {
    "patient_id": "TEST001",
    "patient_name": "John Doe",
    "age": 45,
    "gender": "Male",
    "medical_history": "Hypertension",
    "current_symptoms": "Chest pain and cough",
    "study_type": "Chest X-Ray"
}

print("Patient Data:")
print(json.dumps(patient_data, indent=2))
print()

# Check if image file exists
if not os.path.exists('800wm.jpeg'):
    print("Creating test image...")
    import numpy as np
    import cv2
    img = np.random.randint(100, 180, (400, 400), dtype=np.uint8)
    cv2.rectangle(img, (50, 50), (350, 350), 60, 20)
    cv2.circle(img, (200, 200), 50, 80, -1)
    cv2.imwrite('800wm.jpeg', img)
    print("✅ Test image created: 800wm.jpeg")

# Send the request - CORRECTED: Send patient_data as JSON in the request body
try:
    print("Sending request to API...")
    
    with open('800wm.jpeg', 'rb') as image_file:
        # Create the multipart form data
        files = {'image_file': ('800wm.jpeg', image_file, 'image/jpeg')}
        
        # Send patient_data as JSON string in the form data
        response = requests.post(
            "http://localhost:8000/process-medical-image",
            data={"patient_data": json.dumps(patient_data)},  # Send as JSON string
            files=files
        )
    
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print("✅ SUCCESS! API Response:")
        print(f"  - Success: {result['success']}")
        print(f"  - Clinical note generated: {len(result['clinical_note']) > 0}")
        print(f"  - ICD codes found: {len(result['icd_codes'])}")
        print(f"  - Patient record ID: {result['patient_record_id']}")
        print(f"  - Image study ID: {result['image_study_id']}")
        print(f"  - Message: {result['message']}")
        print()
        print("Clinical Note Preview:")
        print(result['clinical_note'][:200] + "...")
        print()
        print("ICD Codes:")
        for code in result['icd_codes']:
            print(f"  - {code['code']}: {code['description']}")
            
        # Test retrieving the patient record
        print("\n" + "="*50)
        print("Testing patient record retrieval...")
        get_response = requests.get(f"http://localhost:8000/patient-records/TEST001")
        if get_response.status_code == 200:
            patient_record = get_response.json()
            print("✅ Patient record retrieved successfully!")
            print(f"  - Patient: {patient_record['patient']['patient_name']}")
            print(f"  - Studies: {len(patient_record['studies'])}")
            print(f"  - Notes: {len(patient_record['clinical_notes'])}")
        else:
            print(f"❌ Failed to retrieve patient record: {get_response.text}")
            
    else:
        print(f"❌ Error: {response.text}")
        
except Exception as e:
    print(f"❌ Request failed: {e}")
    print("Make sure the server is running: python main.py")