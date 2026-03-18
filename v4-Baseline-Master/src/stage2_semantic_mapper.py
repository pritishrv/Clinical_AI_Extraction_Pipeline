import os
import json
import pandas as pd
from pathlib import Path
from sentence_transformers import SentenceTransformer, util
import torch

# Configuration
PROJECT_ROOT = Path("/Users/joshuabhawanlall/Git Folder/Clinical_AI_Extraction_Pipeline")
INPUT_DIR = PROJECT_ROOT / "v4-Baseline-Master/output/raw_harvest"
PROTOTYPE_WORKBOOK = PROJECT_ROOT / "data/hackathon-database-prototype.xlsx"
OUTPUT_DIR = PROJECT_ROOT / "v4-Baseline-Master/output/mapped_harvest"

def main():
    if not os.path.exists(OUTPUT_DIR): os.makedirs(OUTPUT_DIR)
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    df_proto = pd.read_excel(PROTOTYPE_WORKBOOK)
    target_columns = [str(c) for c in df_proto.columns]
    column_embeddings = model.encode(target_columns, convert_to_tensor=True)
    
    harvest_files = sorted([f for f in os.listdir(INPUT_DIR) if f.endswith(".json")])
    for h_file in harvest_files:
        with open(INPUT_DIR / h_file, "r") as f: data = json.load(f)
        
        print(f"v4 High-Res Mapping Case {data['case_index']}...")
        mapped = {}
        for cand in data["candidates"]:
            key, val = cand["key"], cand["value"]
            if not val: continue
            
            # Semantic Mapping with 0.2 threshold for maximum clinical recall
            key_emb = model.encode(key, convert_to_tensor=True)
            scores = util.cos_sim(key_emb, column_embeddings)[0]
            best_score, best_idx = torch.max(scores, dim=0)
            
            if best_score > 0.2: 
                col = target_columns[best_idx]
                if col not in mapped or best_score > mapped[col]["score"]:
                    mapped[col] = {"value": val, "score": float(best_score)}

        final_mapped = {k: v["value"] for k, v in mapped.items()}
        with open(OUTPUT_DIR / h_file.replace("_harvest.json", "_mapped.json"), "w") as f:
            json.dump({"case_index": data["case_index"], "mapped_columns": final_mapped}, f, indent=4)

    print(f"\nv4 High-Res Semantic Mapping complete.")

if __name__ == "__main__":
    main()
