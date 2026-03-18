import os
import json
import re
from docx import Document
from pathlib import Path

# Configuration
PROJECT_ROOT = Path("/Users/joshuabhawanlall/Git Folder/Clinical_AI_Extraction_Pipeline")
DOCX_PATH = PROJECT_ROOT / "data/hackathon-mdt-outcome-proformas.docx"
OUTPUT_DIR = PROJECT_ROOT / "v4-Baseline-Master/output/raw_harvest"

def clean_val_precision(v):
    # Specialized cleaning to prevent label bleed
    v = v.strip()
    for l in ["DOB", "NHS", "MRN", "Gender", "Decision", "Date", "Outcome", "Diagnosis"]:
        if v.upper().endswith(l.upper()) and len(v) > len(l):
            v = v[: -len(l)].strip()
    return v

def harvest_case_v4_final(table):
    candidates = []
    lines = []
    # Deduplicate merged cells
    for row in table.rows:
        row_txt = []
        for cell in row.cells:
            t = cell.text.strip()
            if t and t not in row_txt: row_txt.append(t)
        if row_txt: lines.append(" | ".join(row_txt))
    
    full_text = " ".join(lines)
    
    # 1. Structural Miner (Split by delimiters)
    for line in lines:
        parts = re.split(r"[:\-\u2013|]|\s{2,}", line)
        for i in range(len(parts) - 1):
            k, v = parts[i].strip(), parts[i+1].strip()
            if len(k) > 1 and len(v) > 0:
                candidates.append({"type": "kv", "key": k, "value": clean_val_precision(v), "evidence": line})
        # Standalone keys for semantic mapping
        for p in parts:
            if len(p.strip()) > 2:
                candidates.append({"type": "kv", "key": p.strip(), "value": p.strip(), "evidence": line})

    # 2. Targeted Clinical Entities
    patterns = {
        "Baseline CT: T(h)": r"\bT[0-4][a-d]?\b",
        "Baseline CT: N(h)": r"\bN[0-3][a-c]?\b",
        "mrT": r"mrT[0-4][a-d]?",
        "TRG": r"TRG\s*[1-5]",
        "Drugs": r"FOLFOX|CAPOX|capecitabine|5-FU|Oxaliplatin",
        "CEA": r"CEA\s*[:\-\u2013]?\s*([\d\.]+)"
    }
    for col, pat in patterns.items():
        for m in re.finditer(pat, full_text, re.I):
            val = m.group(0)
            if "(" in pat and len(m.groups()) > 0: val = m.group(1)
            candidates.append({"type": "kv", "key": col, "value": val, "evidence": val})

    return candidates

def main():
    if not os.path.exists(OUTPUT_DIR): os.makedirs(OUTPUT_DIR)
    doc = Document(DOCX_PATH)
    for i, table in enumerate(doc.tables):
        harvested = harvest_case_v4_final(table)
        with open(OUTPUT_DIR / f"case_{i:03d}_harvest.json", "w") as f:
            json.dump({"case_index": i, "candidates": harvested}, f, indent=4)
    print(f"v4 Final Harvester complete.")

if __name__ == "__main__":
    main()
