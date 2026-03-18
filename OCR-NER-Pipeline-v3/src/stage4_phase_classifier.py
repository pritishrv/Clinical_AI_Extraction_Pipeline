import os
import json
import re
from pathlib import Path

# Configuration
PROJECT_ROOT = Path("/Users/joshuabhawanlall/Git Folder/Clinical_AI_Extraction_Pipeline")
INPUT_DIR = PROJECT_ROOT / "OCR-NER-Pipeline-v3/output/raw_harvest"
OUTPUT_DIR = PROJECT_ROOT / "OCR-NER-Pipeline-v3/output/phase_classified"

def classify_phase(candidates):
    """
    Heuristic classifier to determine the clinical phase of a document.
    """
    full_text = " ".join([c.get("text", "") + " " + c.get("value", "") for c in candidates]).lower()
    
    # PHASE 2: Post-Surgical (High priority keywords)
    if any(x in full_text for x in ["pathology", "resection specimen", "pT", "pN", "surgical margin"]):
        return "PHASE_2_SURGICAL"
    
    # PHASE 3: Surveillance
    if any(x in full_text for x in ["12 week", "surveillance", "long term follow up"]):
        return "PHASE_3_SURVEILLANCE"
        
    # PHASE 1: Post-Neoadjuvant
    if any(x in full_text for x in ["post-chemo", "post-rt", "restaging", "2nd mri", "response to treatment", "trg"]):
        return "PHASE_1_RESTAGING"
        
    # PHASE 0: Baseline (Default)
    return "PHASE_0_BASELINE"

def main():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        
    harvest_files = sorted([f for f in os.listdir(INPUT_DIR) if f.endswith(".json")])
    
    for f in harvest_files:
        with open(INPUT_DIR / f) as j:
            data = json.load(j)
            
        phase = classify_phase(data["candidates"])
        print(f"Case {data['case_index']}: Classified as {phase}")
        
        output_data = {
            "case_index": data["case_index"],
            "phase": phase,
            "candidates": data["candidates"]
        }
        
        output_file = OUTPUT_DIR / f.replace("_harvest.json", "_phased.json")
        with open(output_file, "w") as out:
            json.dump(output_data, out, indent=4)

    print(f"\nPhase Classification Complete. Files saved to {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
