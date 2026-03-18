import os
import json
import re
from docx import Document
from pathlib import Path

# Configuration
PROJECT_ROOT = Path("/Users/joshuabhawanlall/Git Folder/Clinical_AI_Extraction_Pipeline")
DOCX_PATH = PROJECT_ROOT / "data/hackathon-mdt-outcome-proformas.docx"
OUTPUT_DIR = PROJECT_ROOT / "OCR-NER-Pipeline-v3/output/raw_harvest"

def harvest_case_v1_greedy_final(table):
    candidates = []
    # 1. Exhaustive Text Capture
    all_cells = []
    for row in table.rows:
        for cell in row.cells:
            t = cell.text.strip()
            if t and t not in all_cells: all_cells.append(t)
    full_case = " ".join(all_cells)
    
    # 2. Sequential Fact Miner (Recursive Split)
    for line in all_cells:
        # Split by typical clinical delimiters
        parts = re.split(r"[:\-\u2013|]|\s{2,}", line)
        for i, p in enumerate(parts):
            if i < len(parts) - 1:
                k, v = p.strip(), parts[i+1].strip()
                if len(k) > 1 and len(v) > 0:
                    candidates.append({"type": "kv", "key": k, "value": v, "evidence": line})
            # Also treat parts as standalone keys for semantic mapping
            candidates.append({"type": "kv", "key": parts[i].strip(), "value": parts[i].strip(), "evidence": line})

    # 3. Dense Regex Mine
    regex_map = {
        "Baseline CT: T(h)": r"\bT[0-4][a-d]?\b",
        "Baseline CT: N(h)": r"\bN[0-3][a-c]?\b",
        "Baseline MRI: mrT(h)": r"mrT[0-4][a-d]?",
        "mrTRG": r"TRG\s*[1-5]",
        "Chemotherapy: Drugs": r"FOLFOX|CAPOX|capecitabine|5-FU|Oxaliplatin",
        "CEA: Value": r"CEA\s*[:\-\u2013]?\s*([\d\.]+)"
    }
    for col, pat in regex_map.items():
        for m in re.finditer(pat, full_case, re.I):
            val = m.group(0)
            if "(" in pat and len(m.groups()) > 0: val = m.group(1)
            candidates.append({"type": "kv", "key": col, "value": val, "evidence": val})

    return candidates

def main():
    if not os.path.exists(OUTPUT_DIR): os.makedirs(OUTPUT_DIR)
    doc = Document(DOCX_PATH)
    for i, table in enumerate(doc.tables):
        harvested = harvest_case_v1_greedy_final(table)
        with open(OUTPUT_DIR / f"case_{i:03d}_harvest.json", "w") as f:
            json.dump({"case_index": i, "candidates": harvested}, f, indent=4)
    print(f"Diamond V1 GREEDY Harvester Restored.")

if __name__ == "__main__":
    main()
