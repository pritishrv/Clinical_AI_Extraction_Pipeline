import os
import json
import re
import spacy
from pathlib import Path

# medspacy components
from medspacy.ner import TargetMatcher, TargetRule
from medspacy.context import ConText

# Configuration
PROJECT_ROOT = Path("/Users/joshuabhawanlall/Git Folder/Clinical_AI_Extraction_Pipeline")
INPUT_DIR = PROJECT_ROOT / "OCR-NER-Pipeline-v3/output/json_raw"
OUTPUT_DIR = PROJECT_ROOT / "OCR-NER-Pipeline-v3/output/json_ner"

def setup_nlp():
    # Use a blank model to avoid conflicts with existing pipes
    nlp = spacy.blank("en")
    
    # Add a simple sentencizer
    nlp.add_pipe("sentencizer")
    
    # Add TargetMatcher
    matcher = nlp.add_pipe("medspacy_target_matcher")
    
    # Define custom rules for clinical entities
    rules = [
        # Staging
        TargetRule(r"\bT[0-4]([a-d]|sm\d)?\b", "T_STAGE"),
        TargetRule(r"\bN[0-3][a-c]?\b", "N_STAGE"),
        TargetRule(r"\bM[0-1][a-c]?\b", "M_STAGE"),
        TargetRule(r"EMVI\s*(positive|negative|clear|unsafe|\+|-)", "EMVI"),
        TargetRule(r"CRM\s*(clear|unsafe|threatened|involved)", "CRM"),
        TargetRule(r"PSW\s*(clear|unsafe|\+|-)", "PSW"),
        
        # Procedures
        TargetRule(r"colonoscopy", "PROCEDURE"),
        TargetRule(r"flexi\s*sig", "PROCEDURE"),
        TargetRule(r"sigmoidoscopy", "PROCEDURE"),
        TargetRule(r"CT\s*TAP", "IMAGING"),
        TargetRule(r"CT\s*abdomen", "IMAGING"),
        TargetRule(r"CT\s*pelvis", "IMAGING"),
        TargetRule(r"CT\s*thorax", "IMAGING"),
        TargetRule(r"CT\s*chest", "IMAGING"),
        TargetRule(r"MRI\s*rectum", "IMAGING"),
        TargetRule(r"MRI\s*pelvis", "IMAGING"),
        TargetRule(r"PET\s*CT", "IMAGING"),
        
        # Treatment
        TargetRule(r"chemotherapy", "TREATMENT"),
        TargetRule(r"radiotherapy", "TREATMENT"),
        TargetRule(r"CRT", "TREATMENT"),
        TargetRule(r"nCRT", "TREATMENT"),
        TargetRule(r"FOLFOX", "CHEMO_AGENT"),
        TargetRule(r"CAPOX", "CHEMO_AGENT"),
        TargetRule(r"capecitabine", "CHEMO_AGENT"),
        TargetRule(r"surgery", "PROCEDURE"),
        TargetRule(r"hemicolectomy", "PROCEDURE"),
        TargetRule(r"anterior\s*resection", "PROCEDURE"),
        
        # Clinical Identifiers
        TargetRule(r"NHS\s*Number\s*[:\-\u2013]?\s*\d+", "NHS_NUMBER"),
        TargetRule(r"Hospital\s*Number\s*[:\-\u2013]?\s*\d+", "MRN"),
        TargetRule(r"DOB\s*[:\-\u2013]?\s*\d{1,2}[/\-\.]\d{1,2}[/\-\.]\d{2,4}", "DOB"),
        
        # MMR
        TargetRule(r"MMR\s+deficient", "MMR_STATUS"),
        TargetRule(r"MMR\s+proficient", "MMR_STATUS")
    ]
    matcher.add(rules)
    
    # Add ConText for negation
    nlp.add_pipe("medspacy_context")
    
    print("NLP Pipeline setup complete with blank model + TargetMatcher + ConText.")
    return nlp

def extract_case_entities(nlp, case_data):
    # Combine rows but keep row info for provenance
    full_text = ""
    row_offsets = []
    for row in case_data["rows"]:
        start = len(full_text)
        full_text += row["text"] + " | "
        end = len(full_text)
        row_offsets.append({"start": start, "end": end, "row_index": row["row_index"]})
    
    doc = nlp(full_text)
    
    entities = []
    for ent in doc.ents:
        # Determine which row this entity came from
        source_row = -1
        for offset in row_offsets:
            if ent.start_char >= offset["start"] and ent.end_char <= offset["end"]:
                source_row = offset["row_index"]
                break
        
        entities.append({
            "text": ent.text,
            "label": ent.label_,
            "start": ent.start_char,
            "end": ent.end_char,
            "negated": ent._.is_negated,
            "source_row": source_row
        })
    
    return entities

def main():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        
    nlp = setup_nlp()
    
    raw_files = sorted([f for f in os.listdir(INPUT_DIR) if f.endswith(".json")])
    for raw_file in raw_files:
        with open(INPUT_DIR / raw_file, "r") as f:
            case_data = json.load(f)
        
        print(f"Processing NER for {raw_file}...")
        entities = extract_case_entities(nlp, case_data)
        
        processed_data = {
            "case_index": case_data["case_index"],
            "entities": entities,
            "rows": case_data["rows"]
        }
        
        output_file = OUTPUT_DIR / raw_file.replace("_raw.json", "_ner.json")
        with open(output_file, "w") as f:
            json.dump(processed_data, f, indent=4)

if __name__ == "__main__":
    main()
