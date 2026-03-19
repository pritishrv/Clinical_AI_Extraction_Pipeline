import os
import json
from pathlib import Path

# Configuration
JSON_RAW_DIR = Path("v5_version_1/output/json_raw_claude")
STORE_PATH = Path("v5_version_1/output/longitudinal_store_claude.json")

def fix_logic(data):
    """Applies the correction logic to a single extraction object."""
    target_node = data.get("cancer_target_dates", {})
    extracted_62 = target_node.get("extracted_62_day_target")
    
    # If 62-day target exists and is not null/empty
    if extracted_62 and str(extracted_62).lower() != "null":
        target_node["pathway_type"] = "62-day"
        target_node["calculated_target_date"] = extracted_62
        
    return data

def main():
    # 1. Fix individual JSON files
    if os.path.exists(JSON_RAW_DIR):
        print(f"Fixing individual JSON files in {JSON_RAW_DIR}...")
        for f_name in os.listdir(JSON_RAW_DIR):
            if f_name.endswith(".json"):
                f_path = JSON_RAW_DIR / f_name
                with open(f_path, "r") as f:
                    data = json.load(f)
                
                fixed_data = fix_logic(data)
                
                with open(f_path, "w") as f:
                    json.dump(fixed_data, f, indent=4)

    # 2. Fix Master Longitudinal Store
    if os.path.exists(STORE_PATH):
        print(f"Fixing master store: {STORE_PATH}...")
        with open(STORE_PATH, "r") as f:
            store = json.load(f)
            
        patients = store.get("patients", {})
        for nhs, dates in patients.items():
            for mdt_date, extractions in dates.items():
                fixed_extractions = []
                for ext in extractions:
                    fixed_extractions.append(fix_logic(ext))
                patients[nhs][mdt_date] = fixed_extractions
        
        with open(STORE_PATH, "w") as f:
            json.dump(store, f, indent=4)
            
    print("Logic correction complete.")

if __name__ == "__main__":
    main()
