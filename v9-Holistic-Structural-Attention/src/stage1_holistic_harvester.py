import os
import json
import re
from docx import Document
from pathlib import Path

# Configuration
PROJECT_ROOT = Path("/Users/joshuabhawanlall/Git Folder/Clinical_AI_Extraction_Pipeline")
DOCX_PATH = PROJECT_ROOT / "data/hackathon-mdt-outcome-proformas.docx"
OUTPUT_DIR = PROJECT_ROOT / "v9-Holistic-Structural-Attention/output/raw_nodes"

def clean_nhs(text):
    match = re.search(r"(\d{10})", str(text))
    return match.group(1) if match else "unknown"

def extract_holistic_grid(doc):
    all_cases = []
    for i, table in enumerate(doc.tables):
        nodes = []
        # Find NHS for identity
        nhs = "unknown"
        
        # Pre-capture headers for every coordinate
        row_headers = {}
        for r_idx, row in enumerate(table.rows):
            # First cell with text in row is usually the label
            for cell in row.cells:
                if cell.text.strip():
                    row_headers[r_idx] = cell.text.strip()
                    break
        
        for r_idx, row in enumerate(table.rows):
            for c_idx, cell in enumerate(row.cells):
                text = cell.text.strip()
                if not text: continue
                
                if nhs == "unknown":
                    nhs = clean_nhs(text)
                
                nodes.append({
                    "row": r_idx,
                    "col": c_idx,
                    "text": text,
                    "row_header": row_headers.get(r_idx, ""),
                    # Column header is usually Row 0 or 2 depending on the form
                    "col_header": table.rows[0].cells[c_idx].text.strip() if len(table.rows) > 0 else ""
                })
        
        all_cases.append({
            "case_index": i,
            "nhs": nhs,
            "nodes": nodes
        })
    return all_cases

def main():
    if not os.path.exists(OUTPUT_DIR): os.makedirs(OUTPUT_DIR)
    print(f"v9 Holistic Harvester: Mining global anchors from {DOCX_PATH}...")
    doc = Document(DOCX_PATH)
    cases = extract_holistic_grid(doc)
    for case in cases:
        with open(OUTPUT_DIR / f"case_{case['case_index']:03d}_nodes.json", "w") as f:
            json.dump(case, f, indent=4)
    print(f"Holistic Harvesting complete. Generated {len(cases)} files.")

if __name__ == "__main__":
    main()
