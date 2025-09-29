# Step 2 – Clinical Notes Generation using Azure AI

This step demonstrates generating structured clinical notes from patient data using **Azure AI** in two ways:  
1. **Azure AI Playground (UI-based demo)**  
2. **Azure Cloud Shell + Python client app (code-based demo)**  

---

## 🔹 Part 1: Azure AI Playground Demo

🎥 **Video Demo:** [Playground Chat Demo](https://drive.google.com/file/d/1Pcwgs0aAYjCImLn_9D5RVzhq17FGXYLA/view?usp=sharing)

### Steps Followed:

### 1. Azure AI Foundry Project
   **Resource Creation**  
- Deploy **GPT-4o** model in your Azure AI Foundry project.
- Record **resource name, subscription, region, and deployment name**.
- Copy the **project endpoint** from the Overview page.

---

### 2. **Playground Setup**  
   - Opened Azure AI Playground → Chat.  
   - In **System Prompt**, entered:  
     ```
     You are a clinical documentation assistant. Generate structured clinical notes from patient details in the format:

     Patient: <age, gender>
     Presenting Complaints: <symptoms>
     Past Medical History: <if available>
     Assessment: <likely diagnosis>
     Include ICD-10 code
     Plan: <next steps, investigations, treatment, monitoring>
     ```
 ### 3. **Sample Inputs & Outputs**
  ```
**Input 1:**
Patient: 45-year-old male
Presenting Complaints: fever, cough, shortness of breath
Past Medical History: Hypertension
Allergies: Penicillin
Assessment: Possible pneumonia
ICD-10 Code: J18.9

**Output 1:**
Patient: 45-year-old male
Presenting Complaints: fever, cough, shortness of breath
Past Medical History: Hypertension
Allergies: Penicillin
Assessment: Possible pneumonia
ICD-10 Code: J18.9
Plan:
-Order chest X-ray to confirm diagnosis.
-Perform blood tests, including complete blood count (CBC) and inflammatory markers.
-Initiate empiric antibiotic therapy with a non-pencillin-based regimen, considering the patient's allergy.
-Monitor oxygen saturation and consider supplementa oxygen if levels are low.
-Educate the patient about signs of worsening symptoms and when to seek immediate medical attention.
-Follow up in 48-72 hours or sooner if symptoms worsen.
```
```
**Input 2:**
Patient: 53-year-old female
Presenting Complaints: severe headache, seizures, confusion
Past Medical History: None reported
Assessment: Malignant brain tumor
ICD-0 code: C71.9

**Output 2:**
Patient: 53-year-old female
Presenting Complaints: severe headache, seizures, confusion
Past Medical History: None reported
Assessment: Suspected migraine
ICD-10 Code: C71.9
Plan:
-Order an MRI of the brain with contrast to identify the location, size, and characteristics of the tumor.
-Schedule a neurosurgical consultation for possible biopsy and/ or surgical management.
-Refer to oncology for further evaluation and treatment planning, including options such as chemotherapy and radiation therapy.
-Initiate seizure management with antiepileptic medication (e.g., levetiracetam).
-Monitor and manage symptoms, including headache (e.g., corticosteroids for cerebral edema and analgesics for pain).
-Evaluate for any signs of increased intracranial pressure and manage accordingly.
-Provide psychological support and counseling for the patient and family.
-Arrange follow-up for multidisciplinary team coordination and further care planning.
```


---

## 🔹 Part 2: Azure Cloud Shell Demo

🎥 **Video Demo:** [Cloud Shell Demo](https://drive.google.com/file/d/1TfGcU3MCoynUm8JxWPUSqSRrnokHdaIm/view?usp=sharing)

### Steps Followed:

1. **Get Endpoint and Keys**
   - Go to **Azure AI Foundry → Project Overview**  
   - Copy **Project Endpoint**  

2. **Launch Cloud Shell**
   - Open [Azure Portal](https://portal.azure.com)  
   - Start **Cloud Shell (PowerShell)** → Switch to Classic editor version  

3. **Clone Repo & Setup**
     ```bash
     rm -r mslearn-ai-foundry -f
     git clone https://github.com/microsoftlearning/mslearn-ai-studio mslearn-ai-foundry
     cd mslearn-ai-foundry/labfiles/chat-app/python


Created and activated a virtual environment, then installed all required dependencies including Azure and OpenAI packages.
   
    ```
    
    python -m venv labenv
    ./labenv/bin/Activate.ps1
    pip install -r requirements.txt azure-identity azure-ai-projects openai


  4. **Configure .env File**

  ```

  project_endpoint = https://<your-endpoint>.openai.azure.com/

  model_deployment = gpt-4o

  ```

  5. **Modify chat-app.py**

  Add system prompt for clinical documentation:

    ```
    
    prompt = [
    {"role": "system", "content": "You are a clinical documentation assistant. Generate structured clinical notes from patient details in the format: Patient / Presenting Complaints / Assessment / Plan"}
    ]

    ```

  6. **Run the App**

      ```
      az login
      python chat-app.py


7. **Test Input**

```
Patient: 60-year-old female 
Presenting Complaints: chest pain, nausea, sweating
Past Medical History: Diabetes Mellitus (Type 2)
Assessment: Suspected acute myocardial infarction
ICD-10 code: I21.9
```
 8. **Expected Output:**
```
Patient: 60-year-old female
Presenting Complaints: chest pain, nausea, sweating
Assessment: Suspected acute myocardial infarction
ICD-10 code: I21.9
Plan:
- Perform ECG and cardiac enzyme tests
- Admit to ICU if unstable
- Start oxygen and IV access
- Consult cardiology
```
