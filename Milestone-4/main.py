# main.py - EHR Imaging Documentation System API
# This file integrates all modules into a unified web API
import uvicorn
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import numpy as np
import cv2
from typing import Optional, List, Dict
import base64
import io
from PIL import Image
import json
import os
from contextlib import asynccontextmanager

# Import our custom modules
# Module 1: Image Enhancement
from image_enhancement import enhance_image, compare_image_quality
# Module 2: Clinical Note Generation & ICD-10 Coding
from clinical_note_generator import generate_clinical_note, extract_icd_codes
# Module 3: Database Operations
from database import get_db_session, PatientRecord, ClinicalNote, ImageStudy, create_tables
# Configuration
from config import settings

# Lifespan event handler - MODERN APPROACH
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code
    create_tables()
    print("Database tables created successfully")
    yield
    # Shutdown code would go here

# Create FastAPI app with lifespan
app = FastAPI(
    title="EHR Imaging Documentation System",
    description="Unified system for medical image enhancement, clinical note generation, and ICD-10 coding",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PatientData(BaseModel):
    patient_id: str
    patient_name: str
    age: int
    gender: str
    medical_history: Optional[str] = ""
    current_symptoms: Optional[str] = ""
    study_type: str

class ProcessingResponse(BaseModel):
    success: bool
    enhanced_image: Optional[str] = None
    clinical_note: Optional[str] = None
    icd_codes: Optional[List[Dict]] = None
    patient_record_id: Optional[int] = None
    image_study_id: Optional[int] = None
    quality_metrics: Optional[Dict] = None
    message: Optional[str] = None

def preprocess_image(image_bytes: bytes) -> np.ndarray:
    """Convert uploaded image to numpy array for processing"""
    try:
        image = Image.open(io.BytesIO(image_bytes))
        if image.mode != 'RGB':
            image = image.convert('RGB')
        return np.array(image)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid image file: {str(e)}")

def image_to_base64(image_array: np.ndarray) -> str:
    """Convert numpy array to base64 string for API response"""
    try:
        if len(image_array.shape) == 2:
            image_pil = Image.fromarray(image_array.astype('uint8'))
        else:
            image_pil = Image.fromarray(cv2.cvtColor(image_array, cv2.COLOR_BGR2RGB))
        
        buffer = io.BytesIO()
        image_pil.save(buffer, format="PNG")
        return base64.b64encode(buffer.getvalue()).decode('utf-8')
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Image encoding failed: {str(e)}")

@app.post("/process-medical-image", response_model=ProcessingResponse)
async def process_medical_image(
    patient_data: PatientData,
    image_file: UploadFile = File(...)
):
    """
    Unified endpoint that processes medical images through the complete pipeline:
    
    MODULE INTEGRATION FLOW:
    1. IMAGE ENHANCEMENT MODULE:
       - Receives uploaded medical image
       - Applies CLAHE, noise reduction, sharpening, and normalization
       - Outputs enhanced image for better diagnostic quality
    
    2. CLINICAL NOTE GENERATION MODULE:
       - Takes patient data and enhanced image analysis
       - Generates structured clinical note with findings and impressions
       - Outputs human-readable radiology report
    
    3. ICD-10 CODING MODULE:
       - Analyzes clinical note content
       - Extracts relevant ICD-10 diagnostic codes
       - Outputs standardized medical codes for billing/coding
    
    4. DATABASE STORAGE:
       - Stores patient record, enhanced image, and clinical documentation
       - Maintains relational links between all data components
       - Provides audit trail of processing steps
    """
    try:
        if not image_file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        image_bytes = await image_file.read()
        
        if len(image_bytes) > settings.MAX_IMAGE_SIZE:
            raise HTTPException(status_code=400, detail="Image file too large")
        
        original_image = preprocess_image(image_bytes)
        
        print("Enhancing image...")
        enhanced_image = enhance_image(original_image)
        quality_metrics = compare_image_quality(original_image, enhanced_image)
        
        clinical_data = {
            "patient_info": {
                "patient_id": patient_data.patient_id,
                "name": patient_data.patient_name,
                "age": patient_data.age,
                "gender": patient_data.gender
            },
            "medical_history": patient_data.medical_history,
            "current_symptoms": patient_data.current_symptoms,
            "study_type": patient_data.study_type,
            "image_analysis": "Enhanced medical image available for review"
        }
        
        print("Generating clinical note...")
        clinical_note = generate_clinical_note(clinical_data)
        
        print("Extracting ICD-10 codes...")
        icd_codes = extract_icd_codes(clinical_note)
        
        print("Storing in database...")
        db = next(get_db_session())
        
        patient_record = PatientRecord(
            patient_id=patient_data.patient_id,
            patient_name=patient_data.patient_name,
            age=patient_data.age,
            gender=patient_data.gender,
            medical_history=patient_data.medical_history
        )
        db.add(patient_record)
        db.commit()
        db.refresh(patient_record)
        
        _, enhanced_buffer = cv2.imencode('.png', enhanced_image)
        enhanced_bytes = enhanced_buffer.tobytes()
        
        image_study = ImageStudy(
            patient_id=patient_record.id,
            study_type=patient_data.study_type,
            original_image=image_bytes,
            enhanced_image=enhanced_bytes
        )
        db.add(image_study)
        db.commit()
        db.refresh(image_study)
        
        clinical_note_record = ClinicalNote(
            patient_id=patient_record.id,
            image_study_id=image_study.id,
            note_text=clinical_note,
            icd_codes=json.dumps(icd_codes)
        )
        db.add(clinical_note_record)
        db.commit()
        
        response = ProcessingResponse(
            success=True,
            enhanced_image=image_to_base64(enhanced_image),
            clinical_note=clinical_note,
            icd_codes=icd_codes,
            patient_record_id=patient_record.id,
            image_study_id=image_study.id,
            quality_metrics=quality_metrics,
            message="Medical image processed successfully"
        )
        
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")

@app.get("/patient-records/{patient_id}")
async def get_patient_records(patient_id: str):
    """Retrieve patient records and associated data"""
    db = next(get_db_session())
    
    patient = db.query(PatientRecord).filter(PatientRecord.patient_id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    studies = db.query(ImageStudy).filter(ImageStudy.patient_id == patient.id).all()
    notes = db.query(ClinicalNote).filter(ClinicalNote.patient_id == patient.id).all()
    
    studies_data = []
    for study in studies:
        studies_data.append({
            "id": study.id,
            "study_type": study.study_type,
            "created_at": study.created_at.isoformat() if study.created_at else None
        })
    
    notes_data = []
    for note in notes:
        notes_data.append({
            "id": note.id,
            "note_preview": note.note_text[:100] + "..." if len(note.note_text) > 100 else note.note_text,
            "icd_codes": json.loads(note.icd_codes) if note.icd_codes else [],
            "created_at": note.created_at.isoformat() if note.created_at else None
        })
    
    return {
        "patient": {
            "id": patient.id,
            "patient_id": patient.patient_id,
            "patient_name": patient.patient_name,
            "age": patient.age,
            "gender": patient.gender,
            "medical_history": patient.medical_history
        },
        "studies": studies_data,
        "clinical_notes": notes_data
    }

@app.get("/")
async def root():
    return {"message": "EHR Imaging Documentation System API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "EHR Imaging System"}

if __name__ == "__main__":
    uvicorn.run("main:app", host=settings.APP_HOST, port=settings.APP_PORT, reload=True)