import os
import json
import re
import io
import time
import requests
import base64
from pathlib import Path
from PIL import Image

# Configuration
IMAGE_PATH = Path("v5_version_1/output/images/case01.png")
OUT_FILE = Path("v5_version_1/output/json_raw/test_case_01.json")
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "minicpm-v"

def test_single_extraction():
    if not os.path.exists(OUT_FILE.parent): os.makedirs(OUT_FILE.parent)
    
    try:
        with Image.open(IMAGE_PATH) as img:
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
        
        response = requests.post(OLLAMA_URL, json=payload, timeout=None)
        
        if response.status_code == 200:
            result = response.json()
            data = json.loads(result["response"])
            with open(OUT_FILE, "w") as f:
                json.dump(data, f, indent=4)
            print(f"Result saved to {OUT_FILE}")
        else:
            print(f"Error: {response.status_code}")
            
    except Exception as e:
        print(f"Test failed: {e}")

if __name__ == "__main__":
    test_single_extraction()
