import os
import openai
import pandas as pd
import json

# Azure OpenAI Setup



# Load Clinical Notes

with open("clinical_notes.txt", "r", encoding="utf-8") as f:
    raw_notes = f.read().split("\n---\n")  # each patient separated by '---'


# Parse Notes into DataFrame

patients_data = []

for idx, note in enumerate(raw_notes, start=1):
    lines = note.strip().split("\n")
    patient_dict = {"PatientID": idx}
    for line in lines:
        if line.startswith("Age:"):
            patient_dict["Age"] = line.replace("Age:", "").strip()
        elif line.startswith("Gender:"):
            patient_dict["Gender"] = line.replace("Gender:", "").strip()
        elif line.startswith("Symptoms:"):
            patient_dict["Symptoms"] = line.replace("Symptoms:", "").strip()
        elif line.startswith("Diagnosis:"):
            patient_dict["Diagnosis"] = line.replace("Diagnosis:", "").strip()
    # The full note without Patient Name (to send to AI)
    note_text = "\n".join([l for l in lines if not l.startswith("Patient Name:")])
    patient_dict["NoteText"] = note_text
    patients_data.append(patient_dict)

patients = pd.DataFrame(patients_data)


# Function: Get ICD from AI

def get_icd_from_note(note_text):
    prompt = f"""
You are a professional medical coding assistant.
Assign the most accurate ICD-10 code for the following clinical note.

Clinical Note: {note_text}

Return ONLY JSON in this format:
{{
  "ICD_Code": "<ICD-10 code>",
  "ICD_Description": "<short description>"
}}
"""
    try:
        response = openai.ChatCompletion.create(
            engine=DEPLOYMENT_NAME,
            messages=[
                {"role": "system", "content": "You are a medical coding assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.0,
            max_tokens=150
        )
        reply = response["choices"][0]["message"]["content"].strip()
        try:
            return json.loads(reply)
        except:
            return {"ICD_Code": "Unknown", "ICD_Description": "Parsing error"}
    except Exception as e:
        return {"ICD_Code": "Unknown", "ICD_Description": f"Error: {e}"}


# Assign ICD for all patients

icd_codes = []
icd_descs = []

for _, row in patients.iterrows():
    icd_data = get_icd_from_note(row["NoteText"])
    icd_codes.append(icd_data["ICD_Code"])
    icd_descs.append(icd_data["ICD_Description"])

patients["ICD_Code"] = icd_codes
patients["ICD_Description"] = icd_descs
patients["NoteGenerated"] = patients["NoteText"]  # keep note for outputs


# Save Outputs

os.makedirs("outputs_ai", exist_ok=True)

#  CSV
patients.to_csv("outputs_ai/final_with_icd_ai.csv", index=False)

#  JSON
patients.to_json("outputs_ai/final_with_icd_ai.json", orient="records", indent=2)

#  TXT
with open("outputs_ai/final_with_icd_ai.txt", "w", encoding="utf-8") as f:
    for _, row in patients.iterrows():
        f.write(f"Patient: {row['PatientID']}, Age: {row['Age']}, Gender: {row['Gender']}\n")
        f.write(f"Symptoms: {row['Symptoms']}\n")
        f.write(f"Diagnosis: {row['Diagnosis']}\n")
        f.write(f"ICD_Code: {row['ICD_Code']}\n")
        f.write(f"ICD_Description: {row['ICD_Description']}\n")
        f.write("Clinical Note:\n")
        f.write(row['NoteGenerated'].strip() + "\n")
        f.write("-" * 80 + "\n")


