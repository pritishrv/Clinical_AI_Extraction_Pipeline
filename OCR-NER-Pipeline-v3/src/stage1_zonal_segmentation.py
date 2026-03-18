import os
import json
import re
from pathlib import Path

# Configuration
PROJECT_ROOT = Path("/Users/joshuabhawanlall/Git Folder/Clinical_AI_Extraction_Pipeline")
INPUT_DIR = PROJECT_ROOT / "OCR-NER-Pipeline-v3/output/json_raw_v2"
OUTPUT_DIR = PROJECT_ROOT / "OCR-NER-Pipeline-v3/output/json_zonal"

def segment_text(full_text):
    zones = {
        "REFERRAL": "",
        "BASELINE": "",
        "PRIMARY_TREATMENT": "",
        "FOLLOW_UP": ""
    }
    
    # 1. REFERRAL Zone (Start to Staging)
    staging_match = re.search(r"Staging & Diagnosis\(g\)", full_text, re.I)
    if staging_match:
        zones["REFERRAL"] = full_text[:staging_match.start()].strip()
        remainder = full_text[staging_match.start():]
    else:
        zones["REFERRAL"] = full_text
        return zones

    # 2. BASELINE Zone (Staging to Outcome)
    outcome_match = re.search(r"MDT Outcome\(h\)", remainder, re.I)
    if outcome_match:
        zones["BASELINE"] = remainder[:outcome_match.start()].strip()
        outcome_block = remainder[outcome_match.start():]
    else:
        zones["BASELINE"] = remainder
        return zones

    # 3. TREATMENT & FOLLOW_UP (Parsing the Outcome block)
    # If the outcome mentions follow-up markers, split it
    followup_markers = ["2nd MRI", "12 week", "Rediscuss", "Follow up MRI"]
    
    # Heuristic: split by "Outcome:" if there are multiple, or search for follow-up keywords
    if any(marker in outcome_block for marker in followup_markers):
        # Find the first mention of a follow-up marker to split
        min_pos = len(outcome_block)
        for marker in followup_markers:
            pos = outcome_block.find(marker)
            if pos != -1 and pos < min_pos:
                min_pos = pos
        
        zones["PRIMARY_TREATMENT"] = outcome_block[:min_pos].strip()
        zones["FOLLOW_UP"] = outcome_block[min_pos:].strip()
    else:
        zones["PRIMARY_TREATMENT"] = outcome_block
        
    return zones

def main():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        
    raw_files = sorted([f for f in os.listdir(INPUT_DIR) if f.endswith(".json")])
    for raw_file in raw_files:
        with open(INPUT_DIR / raw_file, "r") as f:
            case_data = json.load(f)
        
        # Combine table rows and paragraphs for a full view
        table_text = " | ".join([r["text"] for r in case_data["table_rows"]])
        para_text = " || ".join(case_data["context_paragraphs"])
        full_text = table_text + " ||| " + para_text
        
        print(f"Segmenting Case {case_data['case_index']}...")
        zonal_data = segment_text(full_text)
        zonal_data["case_index"] = case_data["case_index"]
        
        output_file = OUTPUT_DIR / raw_file.replace("_raw.json", "_zonal.json")
        with open(output_file, "w") as f:
            json.dump(zonal_data, f, indent=4)

    print(f"\nZonal Segmentation complete. Files saved to {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
