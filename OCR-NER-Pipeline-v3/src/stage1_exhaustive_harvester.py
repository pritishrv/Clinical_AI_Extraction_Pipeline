import os
import json
import re
from docx import Document
from pathlib import Path

# Configuration
PROJECT_ROOT = Path("/Users/joshuabhawanlall/Git Folder/Clinical_AI_Extraction_Pipeline")
DOCX_PATH = PROJECT_ROOT / "data/hackathon-mdt-outcome-proformas.docx"
OUTPUT_DIR = PROJECT_ROOT / "OCR-NER-Pipeline-v3/output/raw_harvest"

# --- THE PLATINUM CLINICAL DICTIONARY ---
CLINICAL_MAP = {
    r"\bT[0-4][a-d]?\b": "Baseline CT: T(h)",
    r"\bN[0-3][a-c]?\b": "Baseline CT: N(h)",
    r"\bM[01][a-c]?\b": "Baseline CT: M(h)",
    r"mrT[0-4][a-d]?": "Baseline MRI: mrT(h)",
    r"mrN[0-3][a-c]?": "Baseline MRI: mrN(h)",
    r"mrEMVI\s*(positive|negative|\+|-)": "Baseline MRI: mrEMVI(h)",
    r"mrCRM\s*(clear|unsafe|involved)": "Baseline MRI: mrCRM(h)",
    r"mrTRG\s*([1-5])": "2nd MRI: mrTRG score ",
    
    # Path/Histo
    r"Adenocarcinoma|carcinoma": "Histology: Biopsy result(g)",
    r"(well|moderately|poorly)\s+differentiated": "Histology: Biopsy result(g)",
    r"Dukes\s*[A-D]": "Dukes:",
    r"MMR\s+deficient|MMR\s+proficient": "Histology: \nMMR status(g/h)",
    
    # Treatment
    r"FOLFOX|CAPOX|capecitabine|5-FU|Oxaliplatin": "Chemotherapy: Drugs",
    r"cycle\s*\d+": "Chemotherapy: Cycles",
    r"(\d+\s*Gy)": "Radiotheapy: Total dose",
    r"(\d+\s*fractions)": "Radiotheapy: Boost",
    r"curative|palliative": "Chemotherapy: Treatment goals  \n(curative, palliative)",
    r"resection|hemicolectomy|anterior resection": "Surgery: Intent, pre-neoadjuvant therapy",
    
    # New High-Density Markers
    r"62\s*DAY\s*TARGET:\s*(\d{1,2}/\d{1,2}/\d{4})": "Radiotherapy: Dates", # Proxy for target
    r"31\s*DAY\s*TARGET:\s*(\d{1,2}/\d{1,2}/\d{4})": "Radiotherapy: Dates",
    r"CEA\s*[:\-\u2013]?\s*([\d\.]+)": "CEA: Value",
}

def harvest_case_v5(table):
    candidates = []
    
    # 1. Structural extraction
    all_lines = []
    for row in table.rows:
        row_text = " | ".join([cell.text.strip() for cell in row.cells if cell.text.strip()])
        sub_lines = [l.strip() for l in re.split(r"[\n|]", row_text) if l.strip()]
        all_lines.extend(sub_lines)
        
    full_case_text = " ".join(all_lines)
    
    # 2. ULTIMATE SEMANTIC MINER
    for pattern, column in CLINICAL_MAP.items():
        matches = re.findall(pattern, full_case_text, re.I)
        for m in matches:
            val = m if isinstance(m, str) else m[0]
            candidates.append({"type": "kv", "key": column, "value": val.strip()})

    # 3. Structural Pairs
    for i, line in enumerate(all_lines):
        if ":" in line:
            parts = line.split(":", 1)
            candidates.append({"type": "kv", "key": parts[0].strip(), "value": parts[1].strip()})
        elif i < len(all_lines) - 1 and len(line) < 40:
            candidates.append({"type": "kv", "key": line, "value": all_lines[i+1]})
            
    # 4. Global Date Sequence Miner (Aggressive)
    dates = re.findall(r"(\d{1,2}/\d{1,2}/\d{4})", full_case_text)
    if dates:
        candidates.append({"type": "kv", "key": "1st MDT: date(i)", "value": dates[-1]})
        if len(dates) > 1: candidates.append({"type": "kv", "key": "Baseline CT: Date(h)", "value": dates[0]})
        if len(dates) > 2: candidates.append({"type": "kv", "key": "Baseline MRI: date(h)", "value": dates[1]})
        if len(dates) > 3: candidates.append({"type": "kv", "key": "2nd MRI: Date", "value": dates[2]})
        if len(dates) > 4: candidates.append({"type": "kv", "key": "12 week MRI: Date", "value": dates[3]})

    return candidates

def main():
    if not os.path.exists(OUTPUT_DIR): os.makedirs(OUTPUT_DIR)
    doc = Document(DOCX_PATH)
    for i, table in enumerate(doc.tables):
        harvested = harvest_case_v5(table)
        with open(OUTPUT_DIR / f"case_{i:03d}_harvest.json", "w") as f:
            json.dump({"case_index": i, "candidates": harvested}, f, indent=4)
    print(f"Platinum v5 Harvesting complete.")

if __name__ == "__main__":
    main()
