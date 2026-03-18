import os
import json
import pandas as pd
import re
from pathlib import Path

# Configuration
PROJECT_ROOT = Path("/Users/joshuabhawanlall/Git Folder/Clinical_AI_Extraction_Pipeline")
MAPPED_DIR = PROJECT_ROOT / "v4-Baseline-Master/output/mapped_harvest"
OUTPUT_DIR = PROJECT_ROOT / "v4-Baseline-Master/output/longitudinal_merged"

def main():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    else:
        for f in os.listdir(OUTPUT_DIR): os.remove(OUTPUT_DIR / f)
        
    mapped_files = sorted([f for f in os.listdir(MAPPED_DIR) if f.endswith(".json")])
    
    all_cases = []
    for f in mapped_files:
        with open(MAPPED_DIR / f) as j:
            data = json.load(j)
            mapped_cols = data["mapped_columns"]
            
            # IDENTITY: Extract ONLY pure integers for NHS
            nhs_raw = str(mapped_cols.get("Demographics: \nNHS number(d)", ""))
            nhs_match = re.search(r"(\d{10})", nhs_raw)
            nhs = nhs_match.group(1) if nhs_match else "unknown"
            
            # FALLBACK MRN
            mrn_raw = str(mapped_cols.get("Demographics: MRN(c)", ""))
            mrn_match = re.search(r"([A-Z]?\d{7,8})", mrn_raw)
            mrn = mrn_match.group(1) if mrn_match else "unknown"
            
            # CLEAN PID
            if nhs != "unknown": pid = f"NHS_{nhs}"
            elif mrn != "unknown": pid = f"MRN_{mrn}"
            else: pid = f"CASE_{data['case_index']:03d}"
            
            all_cases.append({
                "patient_id": pid,
                "case_index": data["case_index"],
                "data": mapped_cols
            })
            
    df = pd.DataFrame(all_cases)
    patients = df.groupby("patient_id")
    
    print(f"Aggregating {len(df)} cases into {len(patients)} pure clinical records...")
    
    for pid, group in patients:
        master_record = {}
        sorted_group = group.sort_values("case_index")
        for i, (_, row) in enumerate(sorted_group.iterrows()):
            case_data = row["data"]
            for k, v in case_data.items():
                if not v: continue
                if not master_record.get(k):
                    master_record[k] = v
                elif "Baseline" in k:
                    fup_k = k.replace("Baseline CT", "2nd MRI").replace("Baseline MRI", "2nd MRI")
                    if not master_record.get(fup_k):
                        master_record[fup_k] = v
        
        with open(OUTPUT_DIR / f"{pid}.json", "w") as f:
            json.dump(master_record, f, indent=4)

    print(f"v4 Pure Linker complete.")

if __name__ == "__main__":
    main()
