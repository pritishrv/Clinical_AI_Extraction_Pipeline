import os
import json
import re
from docx import Document
from pathlib import Path

# Configuration
PROJECT_ROOT = Path("/Users/joshuabhawanlall/Git Folder/Clinical_AI_Extraction_Pipeline")
DOCX_PATH = PROJECT_ROOT / "data/hackathon-mdt-outcome-proformas.docx"
OUTPUT_DIR = PROJECT_ROOT / "v10-Multimodal-Prose-Grid-Fusion/output/multimodal_nodes"

def clean_nhs(text):
    match = re.search(r"(\d{10})", str(text))
    return match.group(1) if match else "unknown"

def get_row_text(row):
    """Concatenates unique text from all cells in a row."""
    texts = []
    seen = set()
    for cell in row.cells:
        t = cell.text.strip()
        if t and t not in seen:
            texts.append(t)
            seen.add(t)
    return " | ".join(texts)

def harvest_full_body(doc):
    all_packages = []
    
    for i, table in enumerate(doc.tables):
        # Find the NHS
        try:
            raw_demo = table.rows[1].cells[0].text
            nhs = clean_nhs(raw_demo)
        except:
            nhs = "unknown"
        
        # Capture all table nodes with coordinates
        nodes = []
        all_row_texts = []
        for r_idx, row in enumerate(table.rows):
            row_txt = get_row_text(row)
            all_row_texts.append(row_txt)
            for c_idx, cell in enumerate(row.cells):
                t = cell.text.strip()
                if t: nodes.append({"row": r_idx, "col": c_idx, "text": t})
        
        all_packages.append({
            "event_index": i,
            "nhs": nhs,
            "table_nodes": nodes,
            "raw_table_prose": " || ".join(all_row_texts)
        })
        
    return all_packages

def main():
    if not os.path.exists(OUTPUT_DIR): os.makedirs(OUTPUT_DIR)
    print(f"v10 Multimodal Harvester: Ingesting full body from {DOCX_PATH}...")
    doc = Document(DOCX_PATH)
    packages = harvest_full_body(doc)
    
    for pkg in packages:
        output_file = OUTPUT_DIR / f"event_{pkg['event_index']:03d}_multimodal.json"
        with open(output_file, "w") as f:
            json.dump(pkg, f, indent=4)
            
    print(f"Multimodal Harvesting complete. Generated {len(packages)} event packages.")

if __name__ == "__main__":
    main()
