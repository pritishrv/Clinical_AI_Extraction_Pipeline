import os
import json
import re
import pandas as pd
from pathlib import Path
from tqdm import tqdm
import anthropic
import time
from config import ANTHROPIC_API_KEY

# Configure Claude
client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
MODEL_NAME = "claude-3-haiku-20240307"

# Configuration
JSON_DIR = Path("v5_version_1/output/json_raw_claude")
EXCEL_TEMPLATE = Path("data/hackathon-database-prototype.xlsx")
OUTPUT_PATH = Path("v5_version_1/output/hackathon_output_final.xlsx")

# List of columns to LEAVE EMPTY (as per user request)
EXCLUDED_COLUMNS = [
    "Chemotherapy: Treatment goals  \n(curative, palliative)", "Chemotherapy: Drugs", "Chemotherapy: Cycles", 
    "Chemotherapy: Dates", "Chemotherapy: Breaks", "Immunotherapy: Dates", "Immunotherapy",
    "Radiotheapy: Total dose", "Radiotheapy: Boost", "Radiotherapy: Dates", 
    "Radiotheapy: Concomittant chemotherapy ", "CEA: Date", "CEA: Value", "CEA: DRE date ", 
    "CEA: DRE finding", "Surgery: Defunctioned?", "Surgery: Date of surgery ",
    "2nd MRI: Date", "2nd MRI: Patient pathway status", "2nd MRI: mrT", "2nd MRI: mrN", 
    "2nd MRI: mrEMVI", "2nd MRI: mrCRM", "2nd MRI: mrPSW", "2nd MRI: mrTRG score ",
    "MDT (after 6 week: Date", "MDT (after 6 week: Decision ", 
    "12 week MRI: Date", "12 week MRI: mrT", "12 week MRI: mrN", "12 week MRI: mrEMVI", 
    "12 week MRI: mrCRM", "12 week MRI: mrPSW", "12 week MRI: mrTRG score ",
    "Flex sig: Date", "Flex sig: Fidnings ", "MDT (after 12 week): Date", "MDT (after 12 week): Decision ",
    "Watch and wait: Entered watch + wait, date of MDT ?", 
    "Watch and wait: Why did they enter wait (with what intent)", "Watch and wait: Frequency?", 
    "Watch and wait: Date of \nprogression", "Watch and wait: Site of \nprogression", "Watch and wait: Date of death",
    "MRI and flexisigmoidoscopy watch and wait dates: Date entered watch and wait",
    "MRI and flexisigmoidoscopy watch and wait dates: Flexisigmoidoscopy date ",
    "MRI and flexisigmoidoscopy watch and wait dates: Due date next ",
    "MRI and flexisigmoidoscopy watch and wait dates: Flexisigmoidoscopy date",
    "MRI and flexisigmoidoscopy watch and wait dates: Due date next .1",
    "MRI and flexisigmoidoscopy watch and wait dates: Flexisigmoidoscopy date.1",
    "MRI and flexisigmoidoscopy watch and wait dates: Due date next .2",
    "MRI and flexisigmoidoscopy watch and wait dates: Flexisigmoidoscopy date.2",
    "MRI and flexisigmoidoscopy watch and wait dates: Due date next .3",
    "MRI and flexisigmoidoscopy watch and wait dates: MRI Date",
    "MRI and flexisigmoidoscopy watch and wait dates: Due date next .4",
    "MRI and flexisigmoidoscopy watch and wait dates: MRI Date.1",
    "MRI and flexisigmoidoscopy watch and wait dates: Due date next .5",
    "MRI and flexisigmoidoscopy watch and wait dates: MRI Date.2",
    "MRI and flexisigmoidoscopy watch and wait dates: Due date next .6"
]

# Columns to fill using DETERMINISTIC logic (Python)
DETERMINISTIC_MAP = {
    "Demographics: \nDOB(a)": "patient_details.dob",
    "Demographics: MRN(c)": "patient_details.hospital_number",
    "Demographics: \nNHS number(d)": "patient_details.nhs_number",
    "Demographics: \nGender(e)": "patient_details.gender",
    "1st MDT: date(i)": "mdt_meeting_date"
}

def get_initials(name):
    if not name or name == "null": return None
    # Remove markers like (b)
    name = re.sub(r'\(.*?\)', '', name).strip()
    parts = name.split()
    return "".join([p[0].upper() for p in parts if p])

def map_with_llm(patient_json, llm_columns):
    """Ask LLM to fill only the clinical extraction fields."""
    prompt = f"""
    You are a clinical data scientist. Extract ONLY the following fields from the JSON.
    Rules:
    1. Use ONLY information present in the JSON.
    2. If missing, return null.
    3. Return valid JSON only.

    TARGET COLUMNS:
    {json.dumps(llm_columns)}

    PATIENT JSON:
    {json.dumps(patient_json)}
    """
    try:
        message = client.messages.create(
            model=MODEL_NAME,
            max_tokens=2048,
            temperature=0,
            system="You extract clinical markers into JSON. No conversation.",
            messages=[{"role": "user", "content": prompt}]
        )
        raw_text = message.content[0].text.strip()
        start_idx = raw_text.find('{')
        end_idx = raw_text.rfind('}')
        return json.loads(raw_text[start_idx:end_idx+1]) if start_idx != -1 else None
    except: return None

def main():
    df_template = pd.read_excel(EXCEL_TEMPLATE)
    all_columns = list(df_template.columns)
    
    # Identify LLM columns: anything not excluded and not deterministic
    llm_columns = [c for c in all_columns if c not in EXCLUDED_COLUMNS and c not in DETERMINISTIC_MAP and "Initials" not in c]
    
    json_files = sorted([f for f in os.listdir(JSON_DIR) if f.endswith(".json")])
    final_rows = []

    print(f"Hybrid Mapper | Patients: {len(json_files)}")
    for f_name in tqdm(json_files):
        with open(JSON_DIR / f_name, "r") as f:
            data = json.load(f)
            
        row = {col: None for col in all_columns}
        
        # 1. Deterministic Logic
        for col, path in DETERMINISTIC_MAP.items():
            parts = path.split('.')
            val = data
            for p in parts: val = val.get(p) if isinstance(val, dict) else None
            # Clean values
            if val: row[col] = re.sub(r'\(.*?\)', '', str(val)).strip()
            
        # 2. Initials Logic
        p_name = data.get("patient_details", {}).get("name")
        clean_name = re.sub(r'\(.*?\)', '', str(p_name)).strip() if p_name else None
        row["Patient Name"] = clean_name
        row["Demographics: Initials(b)"] = get_initials(p_name)
        
        # 3. LLM Logic (Only for Clinical Derivations)
        llm_data = map_with_llm(data, llm_columns)
        if llm_data:
            for col in llm_columns:
                if col in llm_data: row[col] = llm_data[col]
        
        final_rows.append(row)
        time.sleep(0.5)

    df_final = pd.DataFrame(final_rows)
    # Ensure 'Patient Name' is the first column, followed by the original columns
    cols = ["Patient Name"] + all_columns
    df_final = df_final[cols]
    
    df_final.to_excel(OUTPUT_PATH, index=False)
    print(f"\nFinal Clinical Database Created: {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
