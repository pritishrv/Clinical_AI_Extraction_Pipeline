import os
import json
import re
import base64
import time
from pathlib import Path
from tqdm import tqdm
import anthropic
from config import ANTHROPIC_API_KEY

# Configure Claude
client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
MODEL_NAME = "claude-3-haiku-20240307" # High-speed vision model

# Configuration
IMAGE_DIR = Path("v5_version_1/output/images")
JSON_RAW_DIR = Path("v5_version_1/output/json_raw_claude")
STORE_PATH = Path("v5_version_1/output/longitudinal_store_claude.json")

def call_claude_vision(image_path):
    """Sends the case image to Claude 3 Haiku for clinical extraction with UPDATED schema."""
    
    with open(image_path, "rb") as f:
        image_data = base64.b64encode(f.read()).decode("utf-8")
        
    prompt = """
    You are a Skeptical Clinical Auditor. Examine this MDT proforma image and extract data into the FIXED JSON SCHEMA.

    ### MANDATORY RULES:
    1. NO HALLUCINATIONS: If a field is blank, return null.
    2. VERBATIM: Extract 'clinical_details' and 'mdt_outcome' text verbatim.
    3. DATE: The MDT Meeting Date is in the bold header at the very top.
    4. TARGET: If '62 DAY TARGET' is blank, pathway = '31-day' and target = [MDT Date + 31 days].

    ### TARGET JSON SCHEMA:
    {
        "mdt_meeting_date": "DD/MM/YYYY",
        "patient_details": {
            "hospital_number": "string",
            "nhs_number": "string",
            "name": "string",
            "gender": "string",
            "dob": "date",
            "age": "string"
        },
        "cancer_target_dates": {
            "extracted_62_day_target": "date",
            "pathway_type": "62-day or 31-day",
            "calculated_target_date": "DD/MM/YYYY"
        },
        "staging_and_diagnosis": {
            "diagnosis": "string",
            "icd10_code": "string",
            "differentiation": "string",
            "staging": "raw text",
            "integrated_tnm_stage": "string",
            "dukes": "string"
        },
        "clinical_details": "verbatim text",
        "mdt_outcome": "verbatim text"
    }

    Return ONLY the valid JSON object.
    """
    
    try:
        message = client.messages.create(
            model=MODEL_NAME,
            max_tokens=4096,
            temperature=0,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": "image/png",
                                "data": image_data,
                            },
                        },
                        {
                            "type": "text",
                            "text": prompt
                        }
                    ],
                }
            ],
        )
        raw_text = message.content[0].text
        clean_json = re.sub(r'```json\n|\n```', '', raw_text).strip()
        return json.loads(clean_json)
        
    except Exception as e:
        print(f"\nError for {image_path.name}: {e}")
        if "429" in str(e):
            print("Rate limit hit. Sleeping 60s...")
            time.sleep(60)
        return None

def update_longitudinal_store(data, case_index):
    """Saves individual result and updates the longitudinal store."""
    if not os.path.exists(JSON_RAW_DIR): os.makedirs(JSON_RAW_DIR)
    with open(JSON_RAW_DIR / f"case_{case_index:03d}.json", "w") as f:
        json.dump(data, f, indent=4)

    if not os.path.exists(STORE_PATH):
        store = {"patients": {}}
    else:
        with open(STORE_PATH, "r") as f:
            store = json.load(f)
            
    p_node = data.get("patient_details", {})
    nhs = str(p_node.get("nhs_number", "UNKNOWN")).replace(" ", "")
    nhs = re.sub(r'\(d\).*', '', nhs).strip()
    
    mdt_date = str(data.get("mdt_meeting_date", "UNKNOWN_DATE")).replace("/", "-")
    
    if nhs not in store["patients"]:
        store["patients"][nhs] = {}
        
    if mdt_date not in store["patients"][nhs]:
        store["patients"][nhs][mdt_date] = []
        
    store["patients"][nhs][mdt_date].append(data)
    
    with open(STORE_PATH, "w") as f:
        json.dump(store, f, indent=4)

def main():
    image_files = sorted([f for f in os.listdir(IMAGE_DIR) if f.endswith(".png")])
    if not os.path.exists(JSON_RAW_DIR): os.makedirs(JSON_RAW_DIR)
    
    # We clear previous outputs to ensure schema consistency
    print("Clearing old outputs for new schema...")
    for f in os.listdir(JSON_RAW_DIR):
        if f.startswith("case_"): os.remove(JSON_RAW_DIR / f)
    if os.path.exists(STORE_PATH): os.remove(STORE_PATH)

    print(f"Claude 3 Haiku Vision (Corrected Schema) | Total: {len(image_files)}")
    
    for f_name in tqdm(image_files):
        idx = int(f_name.split("_")[1].split(".")[0])
        image_path = IMAGE_DIR / f_name
        
        result = call_claude_vision(image_path)
        if result:
            update_longitudinal_store(result, idx)
        
        time.sleep(5)

if __name__ == "__main__":
    main()
