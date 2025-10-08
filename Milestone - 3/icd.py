import pandas as pd
import os


# Load ICD-10 Lookup Table

lookup_table = pd.read_csv("icd_lookup_table.csv")
lookup_table.columns = [col.strip().lower().replace(" ", "_") for col in lookup_table.columns]
lookup_table["keywords"] = lookup_table["keywords"].fillna("")


# Load Clinical Notes

with open("clinical_notes.txt", "r", encoding="utf-8") as f:
    notes = f.read().split("\n---\n")  # each patient note separated by ---

clinical_df = pd.DataFrame({"clinical_note": notes})


# Assign ICD-10 Codes Based on Keywords

def assign_icd(note, lookup_df):
    note_lower = note.lower()
    for _, row in lookup_df.iterrows():
        for kw in row["keywords"].split(","):
            if kw.strip().lower() in note_lower:
                return row["icd_code"], row["condition"]
    return None, None

clinical_df[["ICD_Code", "Diagnosis"]] = clinical_df["clinical_note"].apply(
    lambda x: pd.Series(assign_icd(x, lookup_table))
)


# Save Outputs

os.makedirs("outputs", exist_ok=True)

# CSV
clinical_df.to_csv("outputs/final_with_icd.csv", index=False)

# JSON
clinical_df.to_json("outputs/final_with_icd.json", orient="records", indent=2)

# TXT (neatly formatted)
with open("outputs/final_with_icd.txt", "w", encoding="utf-8") as f:
    for idx, row in clinical_df.iterrows():
        f.write(f"Patient Note #{idx+1}\n")
        f.write(f"ICD_Code: {row['ICD_Code']}\n")
        f.write(f"Diagnosis: {row['Diagnosis']}\n")
        f.write("Clinical Note:\n")
        f.write(row['clinical_note'].strip() + "\n")
        f.write("-"*80 + "\n")


