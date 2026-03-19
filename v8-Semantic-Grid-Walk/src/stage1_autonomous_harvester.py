import os
import json
import re
from docx import Document
from pathlib import Path

# Configuration
PROJECT_ROOT = Path("/Users/joshuabhawanlall/Git Folder/Clinical_AI_Extraction_Pipeline")
DOCX_PATH = PROJECT_ROOT / "data/hackathon-mdt-outcome-proformas.docx"
OUTPUT_DIR = PROJECT_ROOT / "v8-Semantic-Grid-Walk/output/raw_nodes"

def clean_nhs(text):
    match = re.search(r"(\d{10})", str(text))
    return match.group(1) if match else "unknown"

def extract_autonomous_grid(doc):
    all_cases = []
    
    for i, table in enumerate(doc.tables):
        nodes = []
        # Identity Resolve (Always Row 1 for this dataset, but we check all cells)
        nhs = "unknown"
        
        for r_idx, row in enumerate(table.rows):
            # Capture row-level context
            row_text = " | ".join(list(dict.fromkeys([c.text.strip() for c in row.cells if c.text.strip()])))
            
            for c_idx, cell in enumerate(row.cells):
                text = cell.text.strip()
                if not text: continue
                
                if nhs == "unknown":
                    nhs = clean_nhs(text)
                
                # Autonomous Label Detection
                # A label is likely if it's short and ends with a colon or specific marker
                is_likely_label = False
                if ":" in text and len(text) < 40:
                    is_likely_label = True
                
                nodes.append({
                    "row": r_idx,
                    "col": c_idx,
                    "text": text,
                    "is_likely_label": is_likely_label,
                    "row_context": row_text
                })
        
        all_cases.append({
            "case_index": i,
            "nhs": nhs,
            "nodes": nodes
        })
        
    return all_cases

def main():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        
    print(f"v8 Autonomous Harvester: Mining structural grid from {DOCX_PATH}...")
    doc = Document(DOCX_PATH)
    cases = extract_autonomous_grid(doc)
    
    for case in cases:
        output_file = OUTPUT_DIR / f"case_{case['case_index']:03d}_nodes.json"
        with open(output_file, "w") as f:
            json.dump(case, f, indent=4)
            
    print(f"Autonomous Harvesting complete. Generated {len(cases)} case node files.")

if __name__ == "__main__":
    main()
