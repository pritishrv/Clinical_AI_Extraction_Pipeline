import os
import json
import pandas as pd
from pathlib import Path
from sentence_transformers import SentenceTransformer, util
import torch

# Configuration
PROJECT_ROOT = Path("/Users/joshuabhawanlall/Git Folder/Clinical_AI_Extraction_Pipeline")
INPUT_DIR = PROJECT_ROOT / "OCR-NER-Pipeline-v3/output/raw_harvest"
PROTOTYPE_WORKBOOK = PROJECT_ROOT / "data/hackathon-database-prototype.xlsx"
OUTPUT_DIR = PROJECT_ROOT / "OCR-NER-Pipeline-v3/output/mapped_harvest"

# Key synonyms to boost density
SYNONYMS = {
    "Diagnosis": "Histology: Biopsy result(g)",
    "T-Stage": "Baseline CT: T(h)",
    "N-Stage": "Baseline CT: N(h)",
    "M-Stage": "Baseline CT: M(h)",
    "Chemo": "Chemotherapy: Drugs",
    "Surgery": "Surgery: Intent, pre-neoadjuvant therapy",
    "Outcome": "MDT (after 6 week: Decision ",
    "CEA": "CEA: Value"
}

def main():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        
    print("Loading local semantic model (all-MiniLM-L6-v2)...")
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    df_proto = pd.read_excel(PROTOTYPE_WORKBOOK)
    target_columns = [str(c) for c in df_proto.columns]
    column_embeddings = model.encode(target_columns, convert_to_tensor=True)
    
    harvest_files = sorted([f for f in os.listdir(INPUT_DIR) if f.endswith(".json")])
    
    for h_file in harvest_files:
        with open(INPUT_DIR / h_file, "r") as f:
            harvest_data = json.load(f)
        
        print(f"Aggressive Semantic Mapping Case {harvest_data['case_index']}...")
        mapped_data = {}
        
        for cand in harvest_data["candidates"]:
            if cand["type"] == "kv":
                key = cand["key"]
                val = cand["value"]
                
                # Check Synonyms first
                for syn_k, target_v in SYNONYMS.items():
                    if syn_k.lower() in key.lower():
                        mapped_data[target_v] = val

                # Semantic fallback
                key_embedding = model.encode(key, convert_to_tensor=True)
                cos_scores = util.cos_sim(key_embedding, column_embeddings)[0]
                best_score, best_idx = torch.max(cos_scores, dim=0)
                
                if best_score > 0.5: # More lenient threshold for maximum density
                    target_col = target_columns[best_idx]
                    if target_col not in mapped_data or len(val) > len(str(mapped_data[target_col])):
                        mapped_data[target_col] = val

        output_file = OUTPUT_DIR / h_file.replace("_harvest.json", "_mapped.json")
        with open(output_file, "w") as f:
            json.dump({"case_index": harvest_data["case_index"], "mapped_columns": mapped_data}, f, indent=4)

    print(f"\nAggressive Mapping complete. Files saved to {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
