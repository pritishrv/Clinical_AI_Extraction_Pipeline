import os
import json
import re
import torch
import pandas as pd
from pathlib import Path
from sentence_transformers import SentenceTransformer, util

# Configuration
PROJECT_ROOT = Path("/Users/joshuabhawanlall/Git Folder/Clinical_AI_Extraction_Pipeline")
INPUT_DIR = PROJECT_ROOT / "v10-Multimodal-Prose-Grid-Fusion/output/multimodal_nodes"
PROTOTYPE_WORKBOOK = PROJECT_ROOT / "data/hackathon-database-prototype.xlsx"
OUTPUT_DIR = PROJECT_ROOT / "v10-Multimodal-Prose-Grid-Fusion/output/multimodal_facts"

# OBSIDIAN CLUSTER MAP (Maximizing density across journey)
CLINICAL_CLUSTERS = {
    "Staging": r"\b[TNM][0-4][a-d]?\b|mr[TNM][0-4][a-d]?\b",
    "Treatment": r"FOLFOX|CAPOX|capecitabine|5-FU|Oxaliplatin|RT|Resection|Surgery",
    "Dates": r"(\d{1,2}/\d{1,2}/\d{4})",
    "Pathology": r"Adenocarcinoma|carcinoma|Dukes\s*[A-D]",
    "Bio": r"CEA\s*[:\-\u2013]?\s*([\d\.]+)"
}

def multimodal_reasoning(event_data, model, col_embeddings, target_columns):
    """
    Mines both grid nodes and narrative prose for clinical facts.
    """
    resolved_facts = {}
    full_text = event_data["raw_table_prose"]
    
    # 1. Structural Grid Walk (High Precision)
    for node in event_data["table_nodes"]:
        text = node["text"]
        # Use semantic mapper on specific cell text
        node_emb = model.encode(text, convert_to_tensor=True)
        scores = util.cos_sim(node_emb, col_embeddings)[0]
        best_score, best_idx = torch.max(scores, dim=0)
        
        if best_score > 0.25:
            col = target_columns[best_idx]
            clean_val = text.split(":", 1)[-1].strip() if ":" in text else text
            if col not in resolved_facts or best_score > resolved_facts[col]["score"]:
                resolved_facts[col] = {"value": clean_val, "score": float(best_score)}

    # 2. Recursive Prose Miner (Extreme Density)
    # Split the entire event text into fact fragments
    fragments = re.split(r"[:\-\u2013|]|\s{2,}", full_text)
    for frag in fragments:
        f_text = frag.strip()
        if len(f_text) < 2: continue
        
        # Semantic mapping for prose bits
        f_emb = model.encode(f_text, convert_to_tensor=True)
        f_scores = util.cos_sim(f_emb, col_embeddings)[0]
        fs, fi = torch.max(f_scores, dim=0)
        
        if fs > 0.15: # Leniency for prose recall
            f_col = target_columns[fi]
            if f_col not in resolved_facts:
                resolved_facts[f_col] = {"value": f_text, "score": float(fs)}

    return {k: v["value"] for k, v in resolved_facts.items()}

def main():
    if not os.path.exists(OUTPUT_DIR): os.makedirs(OUTPUT_DIR)
    print("Loading Semantic Brain (v10 Multimodal)...")
    model = SentenceTransformer('all-MiniLM-L6-v2')
    df_proto = pd.read_excel(PROTOTYPE_WORKBOOK)
    target_columns = [str(c) for c in df_proto.columns]
    col_embeddings = model.encode(target_columns, convert_to_tensor=True)
    
    files = sorted([f for f in os.listdir(INPUT_DIR) if f.endswith(".json")])
    for f in files:
        with open(INPUT_DIR / f, "r") as j: data = json.load(j)
        print(f"Multimodal Reasoning for Event {data['event_index']}...")
        
        facts = multimodal_reasoning(data, model, col_embeddings, target_columns)
        
        output_data = {
            "event_index": data["event_index"],
            "nhs": data["nhs"],
            "resolved_facts": facts
        }
        with open(OUTPUT_DIR / f.replace("_multimodal.json", "_facts.json"), "w") as out:
            json.dump(output_data, out, indent=4)
            
    print(f"Multimodal Reasoning complete. Generated {len(files)} files.")

if __name__ == "__main__":
    main()
