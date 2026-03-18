import os
import json
import pandas as pd
from pathlib import Path

# Configuration
PROJECT_ROOT = Path("/Users/joshuabhawanlall/Git Folder/Clinical_AI_Extraction_Pipeline")
MAPPED_DIR = PROJECT_ROOT / "OCR-NER-Pipeline-v3/output/mapped_harvest"
OUTPUT_DIR = PROJECT_ROOT / "OCR-NER-Pipeline-v3/output/longitudinal_merged"

def main():
    if not os.path.exists(OUTPUT_DIR): os.makedirs(OUTPUT_DIR)
    mapped_files = sorted([f for f in os.listdir(MAPPED_DIR) if f.endswith(".json")])
    
    all_cases = []
    for f in mapped_files:
        with open(MAPPED_DIR / f) as j:
            data = json.load(j)
            mapped_cols = data["mapped_columns"]
            nhs = mapped_cols.get("Demographics: \nNHS number(d)", "unknown").replace(".0", "")
            mrn = mapped_cols.get("Demographics: MRN(c)", "unknown").replace(".0", "")
            all_cases.append({
                "patient_id": f"NHS_{nhs}_MRN_{mrn}",
                "case_index": data["case_index"],
                "data": mapped_cols
            })
            
    df = pd.DataFrame(all_cases)
    patients = df.groupby("patient_id")
    
    for pid, group in patients:
        master_record = {}
        # ADDITIVE MERGE: Take every unique data point found across all documents
        sorted_group = group.sort_values("case_index")
        
        for _, row in sorted_group.iterrows():
            case_data = row["data"]
            for k, v in case_data.items():
                if not v: continue
                
                # If slot is empty, fill it
                if not master_record.get(k):
                    master_record[k] = v
                # If slot is full but this is a different journey phase, 
                # drift to follow-up columns (Drift Logic)
                elif "Baseline" in k:
                    fup_k = k.replace("Baseline CT", "2nd MRI").replace("Baseline MRI", "2nd MRI")
                    if not master_record.get(fup_k):
                        master_record[fup_k] = v
        
        with open(OUTPUT_DIR / f"{pid}.json", "w") as f:
            json.dump(master_record, f, indent=4)

    print(f"Diamond V1 Additive Linker Restored. Groups: {len(patients)}")

if __name__ == "__main__":
    main()
