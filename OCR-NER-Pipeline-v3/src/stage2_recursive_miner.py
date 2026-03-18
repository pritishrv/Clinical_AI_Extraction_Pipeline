import os
import json
import re
from pathlib import Path

# Configuration
PROJECT_ROOT = Path("/Users/joshuabhawanlall/Git Folder/Clinical_AI_Extraction_Pipeline")
INPUT_DIR = PROJECT_ROOT / "OCR-NER-Pipeline-v3/output/grid_raw"
OUTPUT_DIR = PROJECT_ROOT / "OCR-NER-Pipeline-v3/output/grid_mined"

# Aggressive Clinical Map
MINE_MAP = {
    r"\bT[0-4][a-d]?\b": "Baseline CT: T(h)",
    r"\bN[0-3][a-c]?\b": "Baseline CT: N(h)",
    r"\bM[01][a-c]?\b": "Baseline CT: M(h)",
    r"mrT[0-4][a-d]?": "Baseline MRI: mrT(h)",
    r"mrN[0-3][a-c]?": "Baseline MRI: mrN(h)",
    r"Adenocarcinoma|carcinoma": "Histology: Biopsy result(g)",
    r"Dukes\s*[A-D]": "Dukes:",
    r"MMR\s+deficient|MMR\s+proficient": "Histology: \nMMR status(g/h)",
    r"FOLFOX|CAPOX|capecitabine": "Chemotherapy: Drugs",
    r"CEA\s*[:\-\u2013]?\s*([\d\.]+)": "CEA: Value"
}

def mine_case_platinum(grid_data):
    mined = {}
    
    # 1. Demographics
    r1 = grid_data.get("demographics_row", "")
    full = grid_data.get("full_text", "")
    text = r1 if r1 else full
    
    nhs = re.search(r"NHS Number:\s*(\d+)", text, re.I)
    mrn = re.search(r"Hospital Number:\s*(\d+)", text, re.I)
    dob = re.search(r"(\d{1,2}/\d{1,2}/\d{4})\(a\)", text)
    if nhs: mined["Demographics: \nNHS number(d)"] = nhs.group(1)
    if mrn: mined["Demographics: MRN(c)"] = mrn.group(1)
    if dob: mined["Demographics: \nDOB(a)"] = dob.group(1)

    # 2. Outcome Mine (The Gold Mine)
    r7 = grid_data.get("outcome_row", "")
    mined["MDT (after 6 week: Decision "] = r7.replace("\n", " ")
    
    # RECURSIVE PATTERN MATCHING
    for pattern, column in MINE_MAP.items():
        matches = re.finditer(pattern, r7 + text, re.I)
        for i, m in enumerate(matches):
            val = m.group(0)
            if "(" in pattern and len(m.groups()) > 0: val = m.group(1)
            
            # Smart slotting: if 1st slot taken, look for related
            if not mined.get(column):
                mined[column] = val
            elif "MRI" in column:
                mined["2nd MRI: mrT"] = val # Simple drift
                
    # 3. Date Mining
    dates = re.findall(r"(\d{1,2}/\d{1,2}/\d{4})", r7 + text)
    if dates:
        mined["1st MDT: date(i)"] = dates[-1]
        if len(dates) > 1: mined["Baseline CT: Date(h)"] = dates[0]
        if len(dates) > 2: mined["Baseline MRI: date(h)"] = dates[1]

    return mined

def main():
    if not os.path.exists(OUTPUT_DIR): os.makedirs(OUTPUT_DIR)
    grid_files = sorted([f for f in os.listdir(INPUT_DIR) if f.endswith(".json")])
    for f in grid_files:
        with open(INPUT_DIR / f) as j: grid_data = json.load(j)
        print(f"Platinum Mining Case {grid_data['case_index']} Grid...")
        facts = mine_case_platinum(grid_data)
        with open(OUTPUT_DIR / f.replace("_grid.json", "_mined.json"), "w") as out:
            json.dump({"case_index": grid_data["case_index"], "mined_facts": facts}, out, indent=4)
    print(f"\nPlatinum Recursive Mining complete.")

if __name__ == "__main__":
    main()
