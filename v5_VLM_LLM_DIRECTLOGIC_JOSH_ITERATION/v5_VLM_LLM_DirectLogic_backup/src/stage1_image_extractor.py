import os
import json
import re
import io
import time
import requests
import base64
from pathlib import Path
from PIL import Image
from tqdm import tqdm

# Configuration
IMAGE_DIR = Path("v5_version_1/output/images")
JSON_RAW_DIR = Path("v5_version_1/output/json_raw")
STORE_PATH = Path("v5_version_1/output/longitudinal_store.json")
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "minicpm-v" # The tiny OCR specialist

def call_local_vlm(image_path):
    """Sends the case image to local MiniCPM-V via Ollama."""
    try:
        # Resize for speed/memory (1024px is sweet spot for MiniCPM)
        with Image.open(image_path) as img:
            new_width = 1024
            new_height = int((new_width / img.width) * img.height)
            img_resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            buffered = io.BytesIO()
            img_resized.save(buffered, format="PNG")
            img_b64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
            
        prompt = """
        Analyze this clinical MDT proforma image. Extract data into the JSON SCHEMA.
        
        MANDATORY RULES:
        1. NO HALLUCINATIONS: If a field is blank, return null.
        2. VERBATIM: Extract 'clinical_details' and 'mdt_outcome' verbatim.
        3. DATE: The Meeting Date is in the bold header at the top.
        4. TARGET: If '62 DAY TARGET' is blank, pathway = '31-day' and target = [MDT Date + 31 days].

        JSON SCHEMA:
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
                "pathway_type": "62-day or 31-day",
                "calculated_target_date": "DD/MM/YYYY"
            },
            "staging_and_diagnosis": {
                "diagnosis": "string",
                "integrated_tnm_stage": "string",
                "dukes": "string"
            },
            "clinical_details": "text",
            "mdt_outcome": "text"
        }
        """
        
        payload = {
            "model": MODEL_NAME,
            "prompt": prompt,
            "format": "json",
            "stream": False,
            "images": [img_b64],
            "options": {"temperature": 0.0}
        }
        
        response = requests.post(OLLAMA_URL, json=payload, timeout=300)
        if response.status_code != 200: return None
            
        result = response.json()
        raw_response = result.get("response", "").strip()
        
        # Clean potential markdown markers
        clean_json = re.sub(r'```json\n|\n```', '', raw_response).strip()
        return json.loads(clean_json)
        
    except Exception as e:
        print(f"\nError for {image_path.name}: {e}")
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
    processed_indices = []
    if os.path.exists(JSON_RAW_DIR):
        processed_indices = [int(f.split("_")[1].split(".")[0]) for f in os.listdir(JSON_RAW_DIR) if f.startswith("case_")]
    
    to_process = [f for i, f in enumerate(image_files) if i not in processed_indices]
    print(f"Local VLM: {MODEL_NAME} | Total: {len(image_files)} | To process: {len(to_process)}")
    
    for f_name in tqdm(to_process):
        idx = int(f_name.split("_")[1].split(".")[0])
        image_path = IMAGE_DIR / f_name
        
        result = call_local_vlm(image_path)
        if result:
            update_longitudinal_store(result, idx)
        
        time.sleep(0.5)

if __name__ == "__main__":
    main()
