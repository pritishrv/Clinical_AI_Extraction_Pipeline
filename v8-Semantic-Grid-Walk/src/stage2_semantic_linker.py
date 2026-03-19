import os
import json
import re
import torch
import pandas as pd
from pathlib import Path
from sentence_transformers import SentenceTransformer, util

# Configuration
PROJECT_ROOT = Path("/Users/joshuabhawanlall/Git Folder/Clinical_AI_Extraction_Pipeline")
INPUT_DIR = PROJECT_ROOT / "v8-Semantic-Grid-Walk/output/raw_nodes"
PROTOTYPE_WORKBOOK = PROJECT_ROOT / "data/hackathon-database-prototype.xlsx"
OUTPUT_DIR = PROJECT_ROOT / "v8-Semantic-Grid-Walk/output/mapped_facts"

def walk_the_grid(nodes, model, col_embeddings, target_columns):
    """
    Autonomously walks the grid coordinates to pair labels and values.
    """
    resolved_facts = {}
    
    # Sort nodes for systematic walking
    sorted_nodes = sorted(nodes, key=lambda x: (x["row"], x["col"]))
    
    for i, node in enumerate(sorted_nodes):
        text = node["text"]
        row, col = node["row"], node["col"]
        
        # Strategy A: Label-Value split within the same cell (e.g., 'Gender: Male')
        if ":" in text:
            parts = text.split(":", 1)
            if len(parts) > 1 and parts[1].strip():
                label, value = parts[0].strip(), parts[1].strip()
                # Semantic map the COMBINED context
                query = f"{label}: {value}"
                emb = model.encode(query, convert_to_tensor=True)
                scores = util.cos_sim(emb, col_embeddings)[0]
                best_score, best_idx = torch.max(scores, dim=0)
                
                if best_score > 0.3: # Autonomous threshold
                    col_name = target_columns[best_idx]
                    resolved_facts[col_name] = value
                    continue

        # Strategy B: Spatial Neighbors (Right & Down)
        if node["is_likely_label"]:
            label = text.replace(":", "").strip()
            # 1. Look Right
            for neighbor in sorted_nodes:
                if neighbor["row"] == row and neighbor["col"] == col + 1:
                    value = neighbor["text"]
                    query = f"{label}: {value}"
                    emb = model.encode(query, convert_to_tensor=True)
                    scores = util.cos_sim(emb, col_embeddings)[0]
                    best_score, best_idx = torch.max(scores, dim=0)
                    if best_score > 0.3:
                        resolved_facts[target_columns[best_idx]] = value
            # 2. Look Down
            for neighbor in sorted_nodes:
                if neighbor["row"] == row + 1 and neighbor["col"] == col:
                    value = neighbor["text"]
                    query = f"{label}: {value}"
                    emb = model.encode(query, convert_to_tensor=True)
                    scores = util.cos_sim(emb, col_embeddings)[0]
                    best_score, best_idx = torch.max(scores, dim=0)
                    if best_score > 0.3:
                        resolved_facts[target_columns[best_idx]] = value

        # Strategy C: Narrative Miner (For Row 7 large blocks)
        if row >= 7 and len(text) > 50:
            # Recursive fragmenting for facts sitting in prose
            frags = re.split(r"[:\-\u2013|]|\s{2,}", text)
            for f in frags:
                if len(f.strip()) > 2:
                    f_emb = model.encode(f.strip(), convert_to_tensor=True)
                    f_scores = util.cos_sim(f_emb, col_embeddings)[0]
                    f_best_score, f_best_idx = torch.max(f_scores, dim=0)
                    if f_best_score > 0.4: # Higher threshold for standalone prose bits
                        resolved_facts[target_columns[f_best_idx]] = f.strip()

    return resolved_facts

def main():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        
    print("Loading Semantic Model (v8 Semantic Grid-Walk)...")
    model = SentenceTransformer('all-MiniLM-L6-v2')
    df_proto = pd.read_excel(PROTOTYPE_WORKBOOK)
    target_columns = [str(c) for c in df_proto.columns]
    col_embeddings = model.encode(target_columns, convert_to_tensor=True)
    
    node_files = sorted([f for f in os.listdir(INPUT_DIR) if f.endswith(".json")])
    for f in node_files:
        with open(INPUT_DIR / f, "r") as j:
            case_data = json.load(j)
            
        print(f"Walking the Grid for Case {case_data['case_index']}...")
        facts = walk_the_grid(case_data["nodes"], model, col_embeddings, target_columns)
        
        output_data = {
            "case_index": case_data["case_index"],
            "nhs": case_data["nhs"],
            "resolved_facts": facts
        }
        
        output_file = OUTPUT_DIR / f.replace("_nodes.json", "_facts.json")
        with open(output_file, "w") as out:
            json.dump(output_data, out, indent=4)
            
    print(f"Semantic Grid-Walk complete. Generated {len(node_files)} fact files.")

if __name__ == "__main__":
    main()
