"""
Configuration Module for EHR Imaging Documentation System

This module centralizes all configuration settings for the integrated system,
providing a single source of truth for database connections, API settings,
and processing parameters used across all modules.
"""
import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # Database Configuration
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./ehr_system.db")
    
    # External Service API Keys (for future expansion)
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    
    # Web Application Settings
    APP_HOST = os.getenv("APP_HOST", "0.0.0.0")
    APP_PORT = int(os.getenv("APP_PORT", 8000))
    
    # Image Processing Limits
    MAX_IMAGE_SIZE = int(os.getenv("MAX_IMAGE_SIZE", 10485760))  # 10MB

# Global settings instance used throughout the integrated system
settings = Settings()