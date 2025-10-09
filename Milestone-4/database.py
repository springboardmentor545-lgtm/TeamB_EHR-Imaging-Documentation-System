from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ForeignKey, LargeBinary
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os

from config import settings

# Create database directory if it doesn't exist
os.makedirs("database", exist_ok=True)

engine = create_engine(settings.DATABASE_URL, connect_args={"check_same_thread": False} if settings.DATABASE_URL.startswith("sqlite") else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class PatientRecord(Base):
    __tablename__ = "patient_records"
    
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(String, unique=True, index=True)
    patient_name = Column(String)
    age = Column(Integer)
    gender = Column(String)
    medical_history = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class ImageStudy(Base):
    __tablename__ = "image_studies"
    
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patient_records.id"))
    study_type = Column(String)
    original_image = Column(LargeBinary)
    enhanced_image = Column(LargeBinary)
    created_at = Column(DateTime, default=datetime.utcnow)

class ClinicalNote(Base):
    __tablename__ = "clinical_notes"
    
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patient_records.id"))
    image_study_id = Column(Integer, ForeignKey("image_studies.id"))
    note_text = Column(Text)
    icd_codes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

def get_db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    Base.metadata.create_all(bind=engine)