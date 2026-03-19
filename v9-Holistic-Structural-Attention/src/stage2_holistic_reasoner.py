import os
import json
import re
import torch
import pandas as pd
from pathlib import Path
from sentence_transformers import SentenceTransformer, util

# Configuration
PROJECT_ROOT = Path("/Users/joshuabhawanlall/Git Folder/Clinical_AI_Extraction_Pipeline")
INPUT_DIR = PROJECT_ROOT / "v9-Holistic-Structural-Attention/output/raw_nodes"
PROTOTYPE_WORKBOOK = PROJECT_ROOT / "data/hackathon-database-prototype.xlsx"
OUTPUT_DIR = PROJECT_ROOT / "v9-Holistic-Structural-Attention/output/mapped_facts"

def holistic_reasoning_giga(nodes, model, col_embeddings, target_columns):
    """
    Reasoning engine with ULTRA-LENIENT thresholds for maximum density.
    """
    resolved_facts = {}
    
    for node in nodes:
        text = node["text"]
        row_h = node["row_header"]
        col_h = node["col_header"]
        
        # 1. Structural Anchor Mapping (The context-boosted sweep)
        # Using a very low threshold (0.10) because the Grid context protects against leakage.
        query = f"[{row_h} | {col_h}] {text}"
        node_emb = model.encode(query, convert_to_tensor=True)
        scores = util.cos_sim(node_emb, col_embeddings)[0]
        best_score, best_idx = torch.max(scores, dim=0)
        
        if best_score > 0.10: # THE GIGA THRESHOLD
            col_name = target_columns[best_idx]
            clean_val = text.split(":", 1)[-1].strip() if ":" in text else text
            # Accumulate: priority to higher scores
            if col_name not in resolved_facts or best_score > resolved_facts[col_name]["score"]:
                resolved_facts[col_name] = {"value": clean_val, "score": float(best_score)}

        # 2. Recursive Prose Miner (Extreme recall for Row 7+)
        if node["row"] >= 7:
            # Aggressive split to find every clinical marker
            frags = re.split(r"[:\-\u2013|]|\s{2,}", text)
            for frag in frags:
                f_text = frag.strip()
                if len(f_text) < 2: continue
                
                f_query = f"[Clinical Narrative] {f_text}"
                f_emb = model.encode(f_query, convert_to_tensor=True)
                f_scores = util.cos_sim(f_emb, col_embeddings)[0]
                fs, fi = torch.max(f_scores, dim=0)
                
                if fs > 0.15: # Extreme leniency for narrative facts
                    f_col = target_columns[fi]
                    if f_col not in resolved_facts:
                        resolved_facts[f_col] = {"value": f_text, "score": float(fs)}

    return {k: v["value"] for k, v in resolved_facts.items()}

def main():
    if not os.path.exists(OUTPUT_DIR): os.makedirs(OUTPUT_DIR)
    print("Loading Semantic Model (v9 GIGA-Threshold Mode)...")
    model = SentenceTransformer('all-MiniLM-L6-v2')
    df_proto = pd.read_excel(PROTOTYPE_WORKBOOK)
    target_columns = [str(c) for c in df_proto.columns]
    col_embeddings = model.encode(target_columns, convert_to_tensor=True)
    
    files = sorted([f for f in os.listdir(INPUT_DIR) if f.endswith(".json")])
    for f in files:
        with open(INPUT_DIR / f, "r") as j: case_data = json.load(j)
        print(f"Giga-Mapping Case {case_data['case_index']}...")
        facts = holistic_reasoning_giga(case_data["nodes"], model, col_embeddings, target_columns)
        
        output_data = {
            "case_index": case_data["case_index"],
            "nhs": case_data["nhs"],
            "resolved_facts": facts
        }
        with open(OUTPUT_DIR / f.replace("_nodes.json", "_facts.json"), "w") as out:
            json.dump(output_data, out, indent=4)
            
    print(f"Giga-Threshold Resolution complete.")

if __name__ == "__main__":
    main()
