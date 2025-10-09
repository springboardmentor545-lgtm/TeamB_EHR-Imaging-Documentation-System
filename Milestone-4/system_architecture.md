# System Architecture Diagram

```mermaid
graph TD
    A[Medical Image] --> B[Image Enhancement Module]
    C[Patient Data] --> D[Clinical Note Generator]
    B --> E[Enhanced Image]
    E --> D
    D --> F[Clinical Note + ICD-10 Codes]
    F --> G[Database Storage]
    B --> G
    C --> G
    
    style A fill:#e1f5fe
    style B fill:#f3e5f5
    style C fill:#e1f5fe
    style D fill:#f3e5f5
    style E fill:#f1f8e9
    style F fill:#f1f8e9
    style G fill:#fff3e0
```

## Data Flow Explanation

1. **Input**: Medical image and patient data are provided as inputs
2. **Image Enhancement**: The image enhancement module processes the medical image to improve diagnostic quality
3. **Clinical Documentation**: The enhanced image and patient data are used to generate clinical notes and extract ICD-10 codes
4. **Storage**: All data is stored in the database with proper relationships
5. **Output**: Enhanced results are available for clinical review and further processing