import os
import json
import re
import torch
import pandas as pd
from pathlib import Path
from sentence_transformers import SentenceTransformer, util

# Configuration
PROJECT_ROOT = Path("/Users/joshuabhawanlall/Git Folder/Clinical_AI_Extraction_Pipeline")
INPUT_DIR = PROJECT_ROOT / "v7-Multi-Modal-Contextual-Linker/output/hierarchical_nodes"
PROTOTYPE_WORKBOOK = PROJECT_ROOT / "data/hackathon-database-prototype.xlsx"
OUTPUT_DIR = PROJECT_ROOT / "v7-Multi-Modal-Contextual-Linker/output/contextual_facts"

# OBSIDIAN ENTITY MAP (Max Density)
ENTITIES = {
    "T": r"\bT([0-4][a-d]?)\b",
    "N": r"\bN([0-3][a-c]?)\b",
    "M": r"\bM([01][a-c]?)\b",
    "mrT": r"mrT([0-4][a-d]?)",
    "mrN": r"mrN([0-3][a-c]?)",
    "TRG": r"TRG\s*([1-5])",
    "CEA": r"CEA\s*[:\-\u2013]?\s*([\d\.]+)",
    "Drugs": r"FOLFOX|CAPOX|capecitabine|5-FU|Oxaliplatin",
    "Surgery": r"resection|hemicolectomy|anterior resection|Hartmann's|APR"
}

def clean_val(text):
    text = text.strip()
    for l in ["DOB", "NHS", "MRN", "Gender", "Decision", "Date"]:
        if text.upper().endswith(l.upper()) and len(text) > len(l):
            text = text[: -len(l)].strip()
    return text

def main():
    if not os.path.exists(OUTPUT_DIR): os.makedirs(OUTPUT_DIR)
    model = SentenceTransformer('all-MiniLM-L6-v2')
    df_proto = pd.read_excel(PROTOTYPE_WORKBOOK)
    target_columns = [str(c) for c in df_proto.columns]
    col_embeddings = model.encode(target_columns, convert_to_tensor=True)
    
    files = sorted([f for f in os.listdir(INPUT_DIR) if f.endswith(".json")])
    for f in files:
        with open(INPUT_DIR / f, "r") as j: case_data = json.load(j)
        print(f"Obsidian Optimization for Case {case_data['case_index']}...")
        resolved = {}
        
        # 1. Hierarchical Block Scan (Strict Precision)
        for node in case_data["nodes"]:
            text, block = node["text"], node["block"]
            # Multi-Modal Query: Combine visual coordinate data with text
            query = f"[{block}] {text}"
            node_emb = model.encode(query, convert_to_tensor=True)
            scores = util.cos_sim(node_emb, col_embeddings)[0]
            best_score, best_idx = torch.max(scores, dim=0)
            
            # If in narrative block, be more elastic
            threshold = 0.15 if block == "OUTCOME_NARRATIVE" else 0.30
            if best_score > threshold:
                col = target_columns[best_idx]
                val = clean_val(text)
                if col not in resolved or best_score > resolved[col]["score"]:
                    resolved[col] = {"value": val, "score": float(best_score)}

        # 2. RECURSIVE PROSE MINER (Max Density)
        # Pull every possible clinical marker from the full case text
        full_blob = " || ".join([n["text"] for n in case_data["nodes"]])
        for ent_key, pat in ENTITIES.items():
            for m in re.finditer(pat, full_blob, re.I):
                val = m.group(1) if m.groups() else m.group(0)
                # Use clinical logic to map entities to columns
                ent_emb = model.encode(ent_key, convert_to_tensor=True)
                e_scores = util.cos_sim(ent_emb, col_embeddings)[0]
                e_best_score, e_best_idx = torch.max(e_scores, dim=0)
                if e_best_score > 0.1:
                    e_col = target_columns[e_best_idx]
                    if e_col not in resolved:
                        resolved[e_col] = {"value": val, "score": 0.5}

        # 3. DATE SEQUENCE (Chronological Anchors)
        dates = re.findall(r"(\d{1,2}/\d{1,2}/\d{4})", full_blob)
        for i, d in enumerate(dates):
            resolved[f"Date_Sequence_{i}"] = {"value": d, "score": 1.0}

        final_facts = {k: v["value"] for k, v in resolved.items()}
        output_data = {"case_index": case_data["case_index"], "nhs": case_data["nhs"], "resolved_facts": final_facts}
        with open(OUTPUT_DIR / f.replace("_hier.json", "_facts.json"), "w") as out:
            json.dump(output_data, out, indent=4)
            
    print(f"Obsidian Resolution complete.")

if __name__ == "__main__":
    main()
