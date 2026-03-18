import os
import json
import re
from docx import Document
from pathlib import Path

# Configuration
PROJECT_ROOT = Path("/Users/joshuabhawanlall/Git Folder/Clinical_AI_Extraction_Pipeline")
DOCX_PATH = PROJECT_ROOT / "data/hackathon-mdt-outcome-proformas.docx"
OUTPUT_DIR = PROJECT_ROOT / "OCR-NER-Pipeline-v3/output/grid_raw"

def get_row_text(row):
    """
    Concatenates text from all cells in a row, deduplicating merged cell content.
    """
    texts = []
    seen = set()
    for cell in row.cells:
        t = cell.text.strip()
        if t and t not in seen:
            texts.append(t)
            seen.add(t)
    return " | ".join(texts)

def extract_grid(table):
    """
    Extracts data from specific table coordinates (Deterministic Grid).
    """
    grid_data = {
        "demographics_row": "",
        "pathology_row": "",
        "endoscopy_row": "",
        "outcome_row": ""
    }
    
    # MDT proformas have a consistent 8-row structure
    if len(table.rows) >= 8:
        grid_data["demographics_row"] = get_row_text(table.rows[1])
        grid_data["pathology_row"] = get_row_text(table.rows[3])
        grid_data["endoscopy_row"] = get_row_text(table.rows[5])
        grid_data["outcome_row"] = get_row_text(table.rows[7])
    else:
        # Fallback if table is non-standard
        grid_data["full_text"] = " || ".join([get_row_text(r) for r in table.rows])
        
    return grid_data

def main():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        
    print(f"Grid-based Extraction from {DOCX_PATH}...")
    doc = Document(DOCX_PATH)
    
    for i, table in enumerate(doc.tables):
        print(f"Drilling into Case {i} Grid...")
        data = extract_grid(table)
        data["case_index"] = i
        
        output_file = OUTPUT_DIR / f"case_{i:03d}_grid.json"
        with open(output_file, "w") as f:
            json.dump(data, f, indent=4)

    print(f"\nGrid Extraction complete. Files saved to {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
