import os
import json
import re
import torch
import pandas as pd
from pathlib import Path
from sentence_transformers import SentenceTransformer, util

# Configuration
PROJECT_ROOT = Path("/Users/joshuabhawanlall/Git Folder/Clinical_AI_Extraction_Pipeline")
INPUT_DIR = PROJECT_ROOT / "v6-Spatial-Reasoning-Implementation/output/spatial_nodes"
PROTOTYPE_WORKBOOK = PROJECT_ROOT / "data/hackathon-database-prototype.xlsx"
OUTPUT_DIR = PROJECT_ROOT / "v6-Spatial-Reasoning-Implementation/output/spatial_facts"

def clean_val_v6(text):
    """Surgical cleaning to prevent label bleed while maintaining density."""
    text = text.strip()
    # Remove common prefix labels found inside cells
    text = re.sub(r"^(NHS Number|DOB|Gender|MRN|Hospital Number|Diagnosis|Staging):?\s*", "", text, flags=re.I)
    # Trim trailing bleed
    for cleanup in ["DOB", "NHS", "MRN", "Gender", "Decision", "Date"]:
        if text.upper().endswith(cleanup.upper()) and len(text) > len(cleanup):
            text = text[: -len(cleanup)].strip()
    return text.strip()

def main():
    if not os.path.exists(OUTPUT_DIR): os.makedirs(OUTPUT_DIR)
    print("Loading Semantic Model (v6 Giga-Spatial Mode)...")
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    df_proto = pd.read_excel(PROTOTYPE_WORKBOOK)
    target_columns = [str(c) for c in df_proto.columns]
    col_embeddings = model.encode(target_columns, convert_to_tensor=True)
    
    node_files = sorted([f for f in os.listdir(INPUT_DIR) if f.endswith(".json")])
    for f in node_files:
        with open(INPUT_DIR / f, "r") as j: case_data = json.load(j)
        
        print(f"Giga-Spatial Mining Case {case_data['case_index']}...")
        mapped_facts = {}
        
        # PROCESS EVERY CELL IN THE GRID INDIVIDUALLY
        for node in case_data["nodes"]:
            raw_text = node["text"]
            # 1. Clean the cell content (Remove internal labels)
            val = clean_val_v6(raw_text)
            if not val or len(val) < 1: continue
            
            # 2. Semantic Mapping per Cell (Grid-Aware)
            # This prevents Cell A (Male) from bleeding into Cell B (DOB)
            # because they are mapped as two separate operations.
            node_emb = model.encode(raw_text, convert_to_tensor=True)
            scores = util.cos_sim(node_emb, col_embeddings)[0]
            best_score, best_idx = torch.max(scores, dim=0)
            
            # Use a low threshold (0.2) because we are Grid-Protected
            if best_score > 0.20:
                col = target_columns[best_idx]
                # Store value if slot is empty or if this is a high-confidence match
                if col not in mapped_facts or best_score > 0.5:
                    mapped_facts[col] = val
                    
            # 3. RECURSIVE MINE FOR ROW 7 (The Outcome Cell)
            # If we are in the large outcome cell, split it by common delimiters
            if node["row"] >= 7:
                frags = re.split(r"[:\-\u2013|]|\s{2,}", raw_text)
                for frag in frags:
                    if len(frag.strip()) > 2:
                        frag_emb = model.encode(frag.strip(), convert_to_tensor=True)
                        f_scores = util.cos_sim(frag_emb, col_embeddings)[0]
                        f_best_score, f_best_idx = torch.max(f_scores, dim=0)
                        if f_best_score > 0.3:
                            f_col = target_columns[f_best_idx]
                            if f_col not in mapped_facts:
                                mapped_facts[f_col] = frag.strip()

        output_data = {
            "case_index": case_data["case_index"],
            "patient_nhs": case_data["patient_nhs"],
            "spatial_facts": mapped_facts
        }
        with open(OUTPUT_DIR / f.replace("_nodes.json", "_facts.json"), "w") as out:
            json.dump(output_data, out, indent=4)
            
    print(f"Giga-Spatial Reasoning complete.")

if __name__ == "__main__":
    main()
