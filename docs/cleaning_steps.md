# Cleaning Steps

## NIH Chest X-ray Dataset

- Remove duplicate and corrupted images.
- Normalize all images to the same format and pixel scale.

## MIMIC-CXR Dataset

- Convert DICOM images into standard formats (JPG/PNG).
- Drop incomplete cases where reports or images are missing.

## MIMIC-III Clinical Notes

- Remove special characters and de-identify sensitive text.
- Standardize terminology for consistency across notes.

## ICD-10 Codes (WHO)

- Remove duplicate and deprecated codes.
- Validate all entries against the official ICD-10 index.
