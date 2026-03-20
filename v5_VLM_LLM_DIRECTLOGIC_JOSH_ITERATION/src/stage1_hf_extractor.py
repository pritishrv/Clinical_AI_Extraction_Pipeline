import os
import json
import re
import torch
from pathlib import Path
from PIL import Image
from transformers import AutoModelForCausalLM, AutoTokenizer
from tqdm import tqdm

# Configuration
IMAGE_DIR = Path("v5_version_1/output/images")
JSON_RAW_DIR = Path("v5_version_1/output/json_raw")
STORE_PATH = Path("v5_version_1/output/longitudinal_store.json")

# Model Setup (Moondream 1 - Smaller & Faster HF Download)
print("Loading Moondream 1 from Hugging Face (~1.6GB weights)...")
device = "mps" if torch.backends.mps.is_available() else "cpu"
model_id = "vikhyatk/moondream1"

model = AutoModelForCausalLM.from_pretrained(
    model_id, trust_remote_code=True
).to(device)
tokenizer = AutoTokenizer.from_pretrained(model_id)

def call_local_hf_vlm(image_path):
    """Extracts data using local Moondream 1 model."""
    image = Image.open(image_path)
    
    # Target 6 core questions for longitudinal extraction
    questions = {
        "mdt_meeting_date": "What is the MDT meeting date at the top of the image?",
        "patient_id": "What is the NHS Number of the patient?",
        "name": "What is the name of the patient?",
        "diagnosis": "What is the clinical diagnosis?",
        "target": "What is the 62 DAY TARGET date?",
        "outcome": "What is the MDT Outcome at the bottom?"
    }
    
    result = {}
    for key, q in questions.items():
        try:
            # Moondream 1 call structure
            ans = model.answer_question(model.encode_image(image), q, tokenizer)
            result[key] = ans.strip()
        except Exception as e:
            result[key] = None
            
    # Return structured fact-map
    return {
        "mdt_meeting_date": result.get("mdt_meeting_date"),
        "patient_details": {
            "nhs_number": result.get("patient_id"),
            "name": result.get("name")
        },
        "staging_and_diagnosis": {
            "diagnosis": result.get("diagnosis")
        },
        "cancer_target_dates": {
            "extracted_62_day_target": result.get("target")
        },
        "mdt_outcome": result.get("outcome")
    }

def update_longitudinal_store(data, case_index):
    """Saves individual result and updates the longitudinal master."""
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
    
    processed_indices = [int(f.split("_")[1].split(".")[0]) for f in os.listdir(JSON_RAW_DIR) if f.startswith("case_")]
    to_process = [f for i, f in enumerate(image_files) if i not in processed_indices]
    
    print(f"Hugging Face (Moondream 1) | To process: {len(to_process)}")
    
    for f_name in tqdm(to_process):
        idx = int(f_name.split("_")[1].split(".")[0])
        image_path = IMAGE_DIR / f_name
        
        result = call_local_hf_vlm(image_path)
        if result:
            update_longitudinal_store(result, idx)

if __name__ == "__main__":
    main()
