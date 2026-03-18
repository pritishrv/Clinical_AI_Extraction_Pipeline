import os
import json
import pandas as pd
import re
from pathlib import Path

# Configuration
PROJECT_ROOT = Path("/Users/joshuabhawanlall/Git Folder/Clinical_AI_Extraction_Pipeline")
MAPPED_DIR = PROJECT_ROOT / "OCR-NER-Pipeline-v3/output/mapped_harvest"
OUTPUT_DIR = PROJECT_ROOT / "OCR-NER-Pipeline-v3/output/longitudinal_merged"

def main():
    if not os.path.exists(OUTPUT_DIR): os.makedirs(OUTPUT_DIR)
    mapped_files = sorted([f for f in os.listdir(MAPPED_DIR) if f.endswith(".json")])
    
    # 1. Identify and group patients (The core of the Diamond standard)
    all_cases = []
    for f in mapped_files:
        with open(MAPPED_DIR / f) as j:
            data = json.load(j)
            mapped_cols = data["mapped_columns"]
            
            # Primary Key logic
            nhs = mapped_cols.get("Demographics: \nNHS number(d)", "missing")
            mrn = mapped_cols.get("Demographics: MRN(c)", "missing")
            
            # Clean scientific notation if any
            if nhs.endswith(".0"): nhs = nhs[:-2]
            if mrn.endswith(".0"): mrn = mrn[:-2]
            
            # Find identity
            patient_id = f"NHS_{nhs}" if nhs != "missing" else f"MRN_{mrn}" if mrn != "missing" else f"CASE_{data['case_index']}"
            
            all_cases.append({
                "patient_id": patient_id,
                "case_index": data["case_index"],
                "data": mapped_cols
            })
            
    # 2. Longitudinal Aggregation
    df = pd.DataFrame(all_cases)
    grouped = df.groupby("patient_id")
    print(f"Aggregating {len(df)} cases into {len(grouped)} clinical patient journeys...")
    
    for pid, group in grouped:
        master_record = {}
        # Chronological sequence
        sorted_cases = group.sort_values("case_index")
        
        # Merge logic: later cases fill follow-up columns
        for i, (_, row) in enumerate(sorted_cases.iterrows()):
            case_data = row["data"]
            if i == 0:
                # First document is the baseline
                master_record = case_data
            else:
                # Subsequent documents populate follow-up columns
                # mapping 'Baseline MRI' from doc 2 to '2nd MRI' in master
                for k, v in case_data.items():
                    if not v: continue
                    if "MRI" in k and "Baseline" in k:
                        master_record["2nd MRI: Date"] = v # Simple heuristic for hackathon
                    elif "Outcome" in k or "Decision" in k:
                        master_record["MDT (after 6 week: Decision "] = v
                    elif not master_record.get(k):
                        master_record[k] = v
        
        with open(OUTPUT_DIR / f"{pid}.json", "w") as f:
            json.dump(master_record, f, indent=4)

    print(f"Longitudinal Merging Complete.")

if __name__ == "__main__":
    main()
