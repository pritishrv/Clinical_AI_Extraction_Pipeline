import os
import json
import spacy
from pathlib import Path
from medspacy.ner import TargetMatcher, TargetRule
from medspacy.context import ConText

# Configuration
PROJECT_ROOT = Path("/Users/joshuabhawanlall/Git Folder/Clinical_AI_Extraction_Pipeline")
INPUT_DIR = PROJECT_ROOT / "OCR-NER-Pipeline-v3/output/json_raw_v2"
OUTPUT_DIR = PROJECT_ROOT / "OCR-NER-Pipeline-v3/output/json_ner_v4"

def setup_nlp():
    nlp = spacy.blank("en")
    nlp.add_pipe("sentencizer")
    matcher = nlp.add_pipe("medspacy_target_matcher")
    
    rules = [
        # Staging (Improved)
        TargetRule(r"\bT[0-4]([a-d]|sm\d)?\b", "T_STAGE"),
        TargetRule(r"\bN[0-3][a-c]?\b", "N_STAGE"),
        TargetRule(r"\bM[0-1][a-c]?\b", "M_STAGE"),
        TargetRule(r"\bmrT[0-4]\b", "MR_T_STAGE"),
        TargetRule(r"\bmrN[0-3]\b", "MR_N_STAGE"),
        TargetRule(r"EMVI\s*(positive|negative|clear|unsafe|\+|-)", "EMVI"),
        TargetRule(r"CRM\s*(clear|unsafe|threatened|involved|negative)", "CRM"),
        TargetRule(r"PSW\s*(clear|unsafe|\+|-)", "PSW"),
        
        # Procedures & Imaging
        TargetRule(r"colonoscopy", "PROCEDURE"),
        TargetRule(r"flexi\s*sig", "PROCEDURE"),
        TargetRule(r"sigmoidoscopy", "PROCEDURE"),
        TargetRule(r"CT\s*TAP", "IMAGING"),
        TargetRule(r"CT\s*abdomen", "IMAGING"),
        TargetRule(r"CT\s*thorax", "IMAGING"),
        TargetRule(r"MRI\s*rectum", "IMAGING"),
        TargetRule(r"MRI\s*pelvis", "IMAGING"),
        TargetRule(r"PET\s*CT", "IMAGING"),
        
        # Treatment
        TargetRule(r"chemotherapy", "TREATMENT"),
        TargetRule(r"radiotherapy", "TREATMENT"),
        TargetRule(r"CRT", "TREATMENT"),
        TargetRule(r"FOLFOX", "CHEMO_AGENT"),
        TargetRule(r"CAPOX", "CHEMO_AGENT"),
        TargetRule(r"capecitabine", "CHEMO_AGENT"),
        TargetRule(r"resection", "SURGERY"),
        TargetRule(r"hemicolectomy", "SURGERY"),
        TargetRule(r"surgery", "SURGERY"),
        
        # Pathology
        TargetRule(r"Adenocarcinoma", "DIAGNOSIS"),
        TargetRule(r"carcinoma", "DIAGNOSIS"),
        TargetRule(r"polyp", "DIAGNOSIS"),
        
        # Identifiers
        TargetRule(r"NHS\s*Number\s*[:\-\u2013]?\s*\d+", "NHS_NUMBER"),
        TargetRule(r"Hospital\s*Number\s*[:\-\u2013]?\s*\d+", "MRN"),
        TargetRule(r"DOB\s*[:\-\u2013]?\s*\d{1,2}[/\-\.]\d{1,2}[/\-\.]\d{2,4}", "DOB"),
        
        # MMR
        TargetRule(r"MMR\s+deficient", "MMR_STATUS"),
        TargetRule(r"MMR\s+proficient", "MMR_STATUS")
    ]
    matcher.add(rules)
    nlp.add_pipe("medspacy_context")
    return nlp

def extract_case_entities(nlp, case_data):
    table_text = " | ".join([row["text"] for row in case_data["table_rows"]])
    para_text = " | ".join(case_data["context_paragraphs"])
    full_text = table_text + " || " + para_text
    doc = nlp(full_text)
    entities = []
    for ent in doc.ents:
        entities.append({
            "text": ent.text,
            "label": ent.label_,
            "start": ent.start_char,
            "end": ent.end_char,
            "negated": ent._.is_negated
        })
    return entities, full_text

def main():
    if not os.path.exists(OUTPUT_DIR): os.makedirs(OUTPUT_DIR)
    nlp = setup_nlp()
    raw_files = sorted([f for f in os.listdir(INPUT_DIR) if f.endswith(".json")])
    for raw_file in raw_files:
        with open(INPUT_DIR / raw_file, "r") as f: case_data = json.load(f)
        print(f"Processing NER v4 for {raw_file}...")
        entities, full_text = extract_case_entities(nlp, case_data)
        processed_data = {"case_index": case_data["case_index"], "entities": entities, "full_text": full_text}
        output_file = OUTPUT_DIR / raw_file.replace("_raw.json", "_ner_v4.json")
        with open(output_file, "w") as f: json.dump(processed_data, f, indent=4)

if __name__ == "__main__":
    main()
