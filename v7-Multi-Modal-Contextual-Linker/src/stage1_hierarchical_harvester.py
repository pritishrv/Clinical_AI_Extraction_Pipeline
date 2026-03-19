import os
import json
import re
from docx import Document
from pathlib import Path

# Configuration
PROJECT_ROOT = Path("/Users/joshuabhawanlall/Git Folder/Clinical_AI_Extraction_Pipeline")
DOCX_PATH = PROJECT_ROOT / "data/hackathon-mdt-outcome-proformas.docx"
OUTPUT_DIR = PROJECT_ROOT / "v7-Multi-Modal-Contextual-Linker/output/hierarchical_nodes"

def clean_nhs(text):
    match = re.search(r"(\d{10})", str(text))
    return match.group(1) if match else "unknown"

def get_functional_block(r_idx):
    """Maps row index to a clinical functional block."""
    if r_idx <= 1: return "DEMOGRAPHICS"
    if r_idx <= 3: return "STAGING_DIAGNOSIS"
    if r_idx <= 5: return "ENDOSCOPY"
    return "OUTCOME_NARRATIVE"

def harvest_hierarchical_nodes(doc):
    all_cases = []
    for i, table in enumerate(doc.tables):
        case_nodes = []
        nhs = "unknown"
        # Pre-scan for NHS to ensure patient identity
        try:
            nhs = clean_nhs(table.rows[1].cells[0].text)
        except: pass

        for r_idx, row in enumerate(table.rows):
            block = get_functional_block(r_idx)
            # Find the header for this row (usually the first cell or a bold/specific cell)
            row_header = ""
            cells_text = [c.text.strip() for c in row.cells if c.text.strip()]
            
            # Simple heuristic: if cell ends with ':', it's likely a label
            current_labels = [c for c in cells_text if c.endswith(":")]
            
            for c_idx, cell in enumerate(row.cells):
                text = cell.text.strip()
                if not text: continue
                
                case_nodes.append({
                    "row": r_idx,
                    "col": c_idx,
                    "block": block,
                    "text": text,
                    "is_label": text.endswith(":"),
                    "context_row_text": " | ".join(list(dict.fromkeys(cells_text)))
                })
        
        all_cases.append({
            "case_index": i,
            "nhs": nhs,
            "nodes": case_nodes
        })
    return all_cases

def main():
    if not os.path.exists(OUTPUT_DIR): os.makedirs(OUTPUT_DIR)
    print(f"v7 Hierarchical Harvester: Mining from {DOCX_PATH}...")
    doc = Document(DOCX_PATH)
    cases = harvest_hierarchical_nodes(doc)
    for case in cases:
        with open(OUTPUT_DIR / f"case_{case['case_index']:03d}_hier.json", "w") as f:
            json.dump(case, f, indent=4)
    print(f"Hierarchical Harvesting complete. Generated {len(cases)} files.")

if __name__ == "__main__":
    main()
