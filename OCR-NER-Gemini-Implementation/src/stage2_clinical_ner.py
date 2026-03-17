import os
import json
import spacy
import medspacy
from medspacy.visualization import visualize_ent

# Configuration
INPUT_DIR = "output/json_raw"
OUTPUT_DIR = "output/json_verified"

# Attempt to load medspacy
try:
    nlp = medspacy.load()
    print("MedSPaCy loaded successfully.")
except Exception as e:
    print(f"Error loading MedSPaCy: {e}")
    print("Falling back to standard spacy model...")
    try:
        nlp = spacy.load("en_core_sci_lg")
    except:
        print("Standard scientific model not found. Using en_core_web_sm.")
        nlp = spacy.load("en_core_web_sm")

def extract_entities(text):
    """
    Extract clinical entities using NER.
    """
    doc = nlp(text)
    entities = []
    for ent in doc.ents:
        entities.append({
            "text": ent.text,
            "label": ent.label_,
            "start": ent.start_char,
            "end": ent.end_char
        })
    return entities

def process_raw_json():
    """
    Read each raw JSON, perform NER, and save as verified JSON.
    """
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    raw_files = sorted([f for f in os.listdir(INPUT_DIR) if f.endswith(".json")])
    
    for raw_file in raw_files:
        print(f"Processing NER for {raw_file}...")
        with open(os.path.join(INPUT_DIR, raw_file), "r") as f:
            raw_data = json.load(f)
        
        entities = extract_entities(raw_data["raw_text"])
        
        # Simplified mapping (Stage 2 implementation)
        # This will be refined as the project evolves
        verified_data = {
            "case_index": raw_data["case_index"],
            "raw_text": raw_data["raw_text"],
            "entities": entities,
            "mapped_fields": {
                # Placeholder for normalized field mapping logic
                "diagnosis": [e["text"] for e in entities if e["label"] in ["CONDITION", "DIAGNOSIS"]],
                "dates": [e["text"] for e in entities if e["label"] == "DATE"],
                "procedures": [e["text"] for e in entities if e["label"] == "PROCEDURE"]
            }
        }
        
        output_file = raw_file.replace("_raw.json", "_verified.json")
        with open(os.path.join(OUTPUT_DIR, output_file), "w") as f:
            json.dump(verified_data, f, indent=4)
        
        print(f"Saved NER output to {output_file}")

if __name__ == "__main__":
    # Ensure relative paths work from the script location
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    os.chdir("..")
    
    if not os.path.exists(INPUT_DIR):
        print(f"Error: {INPUT_DIR} not found. Run Stage 1 first.")
    else:
        process_raw_json()
