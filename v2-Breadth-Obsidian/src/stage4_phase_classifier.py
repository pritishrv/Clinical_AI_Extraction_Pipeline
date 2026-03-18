import os
import json
import re
from pathlib import Path

# Configuration
PROJECT_ROOT = Path("/Users/joshuabhawanlall/Git Folder/Clinical_AI_Extraction_Pipeline")
INPUT_DIR = PROJECT_ROOT / "v2-Breadth-Obsidian/output/raw_harvest"
OUTPUT_DIR = PROJECT_ROOT / "v2-Breadth-Obsidian/output/phase_classified"

def classify_phase(candidates):
    full_text = " ".join([c.get("text", "") + " " + c.get("value", "") for c in candidates]).lower()
    if any(x in full_text for x in ["pathology", "resection specimen", "pT", "pN", "surgical margin"]):
        return "PHASE_2_SURGICAL"
    if any(x in full_text for x in ["12 week", "surveillance", "long term follow up"]):
        return "PHASE_3_SURVEILLANCE"
    if any(x in full_text for x in ["post-chemo", "post-rt", "restaging", "2nd mri", "trg"]):
        return "PHASE_1_RESTAGING"
    return "PHASE_0_BASELINE"

def main():
    if not os.path.exists(OUTPUT_DIR): os.makedirs(OUTPUT_DIR)
    # This is a simplified version for archival
    print("Phase Classifier restored for v2.")

if __name__ == "__main__":
    main()
