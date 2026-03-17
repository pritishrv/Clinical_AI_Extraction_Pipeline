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
        # --- STAGING ---
        TargetRule(r"\bT[0-4]([a-d]|sm\d)?\b", "T_STAGE"),
        TargetRule(r"\bN[0-3][a-c]?\b", "N_STAGE"),
        TargetRule(r"\bM[0-1][a-c]?\b", "M_STAGE"),
        TargetRule(r"mrT[0-4][a-d]?", "MR_T_STAGE"),
        TargetRule(r"mrN[0-3][a-c]?", "MR_N_STAGE"),
        TargetRule(r"EMVI\s*(positive|negative|clear|unsafe|\+|-)", "EMVI"),
        TargetRule(r"CRM\s*(clear|unsafe|threatened|involved|negative)", "CRM"),
        TargetRule(r"PSW\s*(clear|unsafe|\+|-)", "PSW"),
        TargetRule(r"mrTRG\s*[1-5]", "TRG_SCORE"),
        
        # --- CHEMOTHERAPY ---
        TargetRule(r"chemotherapy", "TREATMENT"),
        TargetRule(r"FOLFOX", "CHEMO_DRUG"),
        TargetRule(r"CAPOX", "CHEMO_DRUG"),
        TargetRule(r"capecitabine", "CHEMO_DRUG"),
        TargetRule(r"Oxaliplatin", "CHEMO_DRUG"),
        TargetRule(r"5-FU", "CHEMO_DRUG"),
        TargetRule(r"Iriontecan", "CHEMO_DRUG"),
        TargetRule(r"cycle\s*\d+", "CHEMO_CYCLE"),
        TargetRule(r"break", "CHEMO_BREAK"),
        
        # --- RADIOTHERAPY ---
        TargetRule(r"radiotherapy", "TREATMENT"),
        TargetRule(r"RT", "TREATMENT"),
        TargetRule(r"CRT", "TREATMENT"),
        TargetRule(r"nCRT", "TREATMENT"),
        TargetRule(r"\d+\s*Gy", "RT_DOSE"),
        TargetRule(r"\d+\s*fractions", "RT_FRACTIONS"),
        
        # --- SURGERY ---
        TargetRule(r"resection", "SURGERY"),
        TargetRule(r"hemicolectomy", "SURGERY"),
        TargetRule(r"anterior resection", "SURGERY"),
        TargetRule(r"APR", "SURGERY"),
        TargetRule(r"Hartmann's", "SURGERY"),
        TargetRule(r"surgery", "SURGERY"),
        TargetRule(r"defunctioning", "SURGERY_DETAIL"),
        TargetRule(r"stoma", "SURGERY_DETAIL"),
        
        # --- PATHOLOGY ---
        TargetRule(r"Adenocarcinoma", "DIAGNOSIS"),
        TargetRule(r"carcinoma", "DIAGNOSIS"),
        TargetRule(r"Dukes\s*[A-D]", "DUKES"),
        TargetRule(r"(well|moderately|poorly)\s+differentiated", "DIFFERENTIATION"),
        
        # --- WATCH & WAIT ---
        TargetRule(r"watch and wait", "W_AND_W"),
        TargetRule(r"W&W", "W_AND_W"),
        
        # --- CLINICAL MARKERS ---
        TargetRule(r"62\s*DAY\s*TARGET", "TARGET_MARKER"),
        TargetRule(r"31\s*DAY\s*TARGET", "TARGET_MARKER"),
        TargetRule(r"CEA", "CEA_MARKER"),
        TargetRule(r"MDT", "MDT_MARKER"),
        TargetRule(r"curative", "INTENT"),
        TargetRule(r"palliative", "INTENT")
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
        print(f"Processing NER v4 ULTRA for {raw_file}...")
        entities, full_text = extract_case_entities(nlp, case_data)
        processed_data = {"case_index": case_data["case_index"], "entities": entities, "full_text": full_text}
        output_file = OUTPUT_DIR / raw_file.replace("_raw.json", "_ner_v4.json")
        with open(output_file, "w") as f: json.dump(processed_data, f, indent=4)

if __name__ == "__main__":
    main()
