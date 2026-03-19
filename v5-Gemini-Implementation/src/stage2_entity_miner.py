import os
import json
import re
import torch
import pandas as pd
from pathlib import Path
from sentence_transformers import SentenceTransformer, util

# Configuration
PROJECT_ROOT = Path("/Users/joshuabhawanlall/Git Folder/Clinical_AI_Extraction_Pipeline")
INPUT_JSON = PROJECT_ROOT / "v5-Gemini-Implementation/output/journey_json/master_journey_v5.json"
PROTOTYPE_WORKBOOK = PROJECT_ROOT / "data/hackathon-database-prototype.xlsx"
OUTPUT_JSON = PROJECT_ROOT / "v5-Gemini-Implementation/output/journey_json/master_journey_mined_v5.json"

# --- THE OBSIDIAN DICTIONARY (Total Recall) ---
OBSIDIAN_MAP = {
    "T-Stage": r"\bT([0-4][a-d]?)\b",
    "N-Stage": r"\bN([0-3][a-c]?)\b",
    "M-Stage": r"\bM([01][a-c]?)\b",
    "mrT": r"mrT([0-4][a-d]?)",
    "mrN": r"mrN([0-3][a-c]?)",
    "EMVI": r"EMVI\s*(positive|negative|\+|-)",
    "CRM": r"CRM\s*(clear|unsafe|involved)",
    "TRG": r"TRG\s*([1-5])",
    "CEA": r"CEA\s*[:\-\u2013]?\s*([\d\.]+)",
    "Drugs": r"FOLFOX|CAPOX|capecitabine|5-FU|Oxaliplatin|Irinotecan|Papillon",
    "Surgery": r"resection|hemicolectomy|anterior resection|Hartmann's|APR|Surgery",
    "Dukes": r"Dukes\s*([A-D])",
    "MMR": r"MMR\s*(deficient|proficient)",
    "DRE": r"DRE\s*(finding|date|digital rectal examination)",
}

def mine_total_recall(text):
    facts = []
    # 1. Broad Pattern Mine
    for k, pat in OBSIDIAN_MAP.items():
        for m in re.finditer(pat, text, re.I):
            val = m.group(1) if m.groups() else m.group(0)
            facts.append({"key": k, "value": val.strip()})
            
    # 2. Sequential Fragment Mine (Split on anything)
    frags = re.split(r"[:\-\u2013|]|\s{2,}", text)
    for i in range(len(frags) - 1):
        key, val = frags[i].strip(), frags[i+1].strip()
        if 1 < len(key) < 60 and len(val) > 0:
            facts.append({"key": key, "value": val})
            
    return facts

def main():
    print("Loading Semantic Model (v5 Obsidian Sweep)...")
    model = SentenceTransformer('all-MiniLM-L6-v2')
    df_proto = pd.read_excel(PROTOTYPE_WORKBOOK)
    target_columns = [str(c) for c in df_proto.columns]
    col_embeddings = model.encode(target_columns, convert_to_tensor=True)
    
    with open(INPUT_JSON, "r") as f: journey_store = json.load(f)
        
    for nhs, patient in journey_store.items():
        print(f"Obsidian Sweep for Patient {nhs}...")
        demo_text = patient["events"][0]["raw_prose"]
        
        # DEMOGRAPHICS
        patient["demographics"] = {
            "DOB": re.search(r"(\d{1,2}/\d{1,2}/\d{4})", demo_text).group(1) if re.search(r"(\d{1,2}/\d{1,2}/\d{4})", demo_text) else "unknown",
            "Initials": re.search(r"(?:Number:.*?|c\))\s*([A-Z\s']+)\(b\)", demo_text).group(1).strip() if re.search(r"(?:Number:.*?|c\))\s*([A-Z\s']+)\(b\)", demo_text) else "unknown",
            "MRN": re.search(r"Hospital Number:\s*(\d+)", demo_text).group(1) if re.search(r"Hospital Number:\s*(\d+)", demo_text) else "unknown"
        }
        
        for event in patient["events"]:
            cands = mine_total_recall(event["raw_prose"])
            mapped_cols = {}
            for cand in cands:
                # Ultra-low threshold for Obsidian standard
                key_emb = model.encode(cand["key"], convert_to_tensor=True)
                scores = util.cos_sim(key_emb, col_embeddings)[0]
                best_score, best_idx = torch.max(scores, dim=0)
                
                if best_score > 0.10:
                    col = target_columns[best_idx]
                    if col not in mapped_cols:
                        mapped_cols[col] = cand["value"]
                    else:
                        if cand["value"] not in mapped_cols[col]:
                            mapped_cols[col] += f" | {cand['value']}"
            
            event["mapped_data"] = mapped_cols
            
    with open(OUTPUT_JSON, "w") as f:
        json.dump(journey_store, f, indent=4)
    print(f"Obsidian Sweep Complete.")

if __name__ == "__main__":
    main()
