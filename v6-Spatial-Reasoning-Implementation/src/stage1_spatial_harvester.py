import os
import json
import re
from docx import Document
from pathlib import Path

# Configuration
PROJECT_ROOT = Path("/Users/joshuabhawanlall/Git Folder/Clinical_AI_Extraction_Pipeline")
DOCX_PATH = PROJECT_ROOT / "data/hackathon-mdt-outcome-proformas.docx"
OUTPUT_DIR = PROJECT_ROOT / "v6-Spatial-Reasoning-Implementation/output/spatial_nodes"

def clean_nhs(text):
    match = re.search(r"(\d{10})", str(text))
    return match.group(1) if match else "unknown"

def harvest_spatial_nodes(doc):
    """
    Extracts every cell as a 'Spatial Node' with (row, col) coordinates.
    """
    all_cases = []
    
    for i, table in enumerate(doc.tables):
        nodes = []
        # Find NHS number to identify the patient for this table
        # Demographics are always in row 1
        nhs = "unknown"
        try:
            demo_cell_text = table.rows[1].cells[0].text
            nhs = clean_nhs(demo_cell_text)
        except:
            pass
            
        for r_idx, row in enumerate(table.rows):
            for c_idx, cell in enumerate(row.cells):
                text = cell.text.strip()
                if text:
                    nodes.append({
                        "row": r_idx,
                        "col": c_idx,
                        "text": text
                    })
        
        all_cases.append({
            "case_index": i,
            "patient_nhs": nhs,
            "nodes": nodes
        })
        
    return all_cases

def main():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        
    print(f"v6 Spatial Reasoning: Harvesting nodes from {DOCX_PATH}...")
    doc = Document(DOCX_PATH)
    cases = harvest_spatial_nodes(doc)
    
    for case in cases:
        output_file = OUTPUT_DIR / f"case_{case['case_index']:03d}_nodes.json"
        with open(output_file, "w") as f:
            json.dump(case, f, indent=4)
            
    print(f"Spatial Harvesting complete. Generated {len(cases)} case node files.")

if __name__ == "__main__":
    main()
