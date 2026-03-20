import os
import json
import re
import pandas as pd
from pathlib import Path
from tqdm import tqdm
import anthropic
from config import ANTHROPIC_API_KEY

# Configure Claude 3 Haiku for Mapping
client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
MODEL_NAME = "claude-3-haiku-20240307"

# Configuration
STORE_PATH = Path("v5_version_1/output/longitudinal_store_claude.json")
PROTOTYPE_PATH = Path("data/hackathon-database-prototype.xlsx")
OUTPUT_PATH = Path("v5_version_1/output/final_clinical_database.xlsx")

# Target Schema (Extracted from prototype)
TARGET_COLUMNS = [
    "Demographics: DOB(a)", "Demographics: Initials(b)", "Demographics: MRN(c)", 
    "Demographics: NHS number(d)", "Demographics: Gender(e)", 
    "Demographics: Previous cancer (y, n) if yes, where(f)", 
    "Demographics: State site of previous cancer(f)", "Endoscopy: date(f)", 
    "Endosopy type: flexi sig, incomplete colonoscopy, colonoscopy complete(f)", 
    "Endoscopy: Findings(f)", "Histology: Biopsy result(g)", "Histology: Biopsy date(g)", 
    "Histology: MMR status(g/h)", "Baseline MRI: date(h)", "Baseline MRI: mrT(h)", 
    "Baseline MRI: mrN(h)", "Baseline MRI: mrEMVI(h)", "Baseline MRI: mrCRM(h)", 
    "Baseline MRI: mrPSW(h)", "Baseline CT: Date(h)", "Baseline CT: T(h)", 
    "Baseline CT: N(h)", "Baseline CT: EMVI(h)", "Baseline CT: M(h)", 
    "Baseline CT: Incidental findings requiring follow up? Y/N(h)", 
    "Baseline CT: Detail incidental finding(h)", "1st MDT: date(i)", 
    "1st MDT: Treatment approach (TNT, downstaging chemo, Papillon, etc.)(h)", 
    "Chemotherapy: Treatment goals (curative, palliative)", "Chemotherapy: Drugs", 
    "Chemotherapy: Cycles", "Chemotherapy: Dates", "Chemotherapy: Breaks", 
    "Immunotherapy: Dates", "Immunotherapy", "Radiotheapy: Total dose", 
    "Radiotheapy: Boost", "Radiotherapy: Dates", "Radiotheapy: Concomittant chemotherapy", 
    "CEA: Date", "CEA: Value", "CEA: DRE date", "CEA: DRE finding", 
    "Surgery: Defunctioned?", "Surgery: Date of surgery", "Surgery: Intent, pre-neoadjuvant therapy", 
    "2nd MRI: Date", "2nd MRI: Patient pathway status", "2nd MRI: mrT", 
    "2nd MRI: mrN", "2nd MRI: mrEMVI", "2nd MRI: mrCRM", "2nd MRI: mrPSW", 
    "2nd MRI: mrTRG score", "MDT (after 6 week: Date", "MDT (after 6 week: Decision", 
    "12 week MRI: Date", "12 week MRI: mrT", "12 week MRI: mrN", 
    "12 week MRI: mrEMVI", "12 week MRI: mrCRM", "12 week MRI: mrPSW", 
    "12 week MRI: mrTRG score", "Flex sig: Date", "Flex sig: Findings", 
    "MDT (after 12 week): Date", "MDT (after 12 week): Decision", 
    "Watch and wait: Entered watch + wait, date of MDT?", 
    "Watch and wait: Why did they enter wait (with what intent)", 
    "Watch and wait: Frequency?", "Watch and wait: Date of progression", 
    "Watch and wait: Site of progression", "Watch and wait: Date of death"
]

def map_patient_journey(patient_id, journey_data):
    """Uses Claude to map multiple MDT events into the 88-column timeline."""
    
    events_summary = ""
    for date, extractions in journey_data.items():
        for ext in extractions:
            events_summary += f"\n--- MDT DATE: {date} ---\n"
            events_summary += f"Staging: {ext.get('staging_and_diagnosis')}\n"
            events_summary += f"Clinical: {ext.get('clinical_details')}\n"
            events_summary += f"Outcome: {ext.get('mdt_outcome')}\n"

    prompt = f"""
    You are a Consultant Clinical Data Scientist. Your task is to map a patient's longitudinal journey into a structured database row.
    
    PATIENT JOURNEY DATA:
    {events_summary}
    
    TARGET COLUMNS:
    {json.dumps(TARGET_COLUMNS)}
    
    RULES:
    1. Fill as many columns as possible based on the evidence.
    2. CHRONOLOGICAL ROUTING: 
       - The 1st MRI found should go to 'Baseline MRI'.
       - Subsequent MRIs go to '2nd MRI' and '12 week MRI' in order.
       - The 1st MDT outcome goes to '1st MDT'.
    3. NO HALLUCINATIONS: If no data exists for a column, return null.
    4. DATA NORMALIZATION: 
       - TNM stages should be clean (e.g., T3c, N1, M0).
       - Dates should be DD/MM/YYYY.
    
    Return a JSON object where keys match the TARGET COLUMNS exactly.
    """
    
    try:
        message = client.messages.create(
            model=MODEL_NAME,
            max_tokens=4096,
            temperature=0,
            messages=[{"role": "user", "content": prompt}]
        )
        raw_text = message.content[0].text
        clean_json = re.sub(r'```json\n|\n```', '', raw_text).strip()
        return json.loads(clean_json)
    except Exception as e:
        print(f"Error mapping patient {patient_id}: {e}")
        return None

def main():
    with open(STORE_PATH, "r") as f:
        store = json.load(f)
        
    patients = store.get("patients", {})
    all_rows = []
    
    print(f"Mapping {len(patients)} patient journeys into the final schema...")
    
    for nhs, journey in tqdm(patients.items()):
        row_data = map_patient_journey(nhs, journey)
        if row_data:
            all_rows.append(row_data)
            
    # Convert to DataFrame
    df = pd.DataFrame(all_rows)
    # Ensure column order matches prototype
    df = df.reindex(columns=TARGET_COLUMNS)
    
    # Save to Excel
    df.to_excel(OUTPUT_PATH, index=False)
    print(f"\nFinal Database Created: {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
