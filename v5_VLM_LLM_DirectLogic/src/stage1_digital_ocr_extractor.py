import os
import json
import re
import time
from docx import Document
from pathlib import Path
from tqdm import tqdm
import google.generativeai as genai
from config import GOOGLE_API_KEY

# Configure Gemini
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('models/gemini-2.0-flash')

# Configuration
DOCX_PATH = Path("data/hackathon-mdt-outcome-proformas.docx")
JSON_RAW_DIR = Path("v5_version_1/output/json_raw")
STORE_PATH = Path("v5_version_1/output/longitudinal_store.json")

def get_elements_in_order(doc):
    """Yields paragraphs and tables in order."""
    from docx.table import Table
    from docx.text.paragraph import Paragraph
    for element in doc.element.body:
        if element.tag.endswith('p'):
            yield Paragraph(element, doc)
        elif element.tag.endswith('tbl'):
            yield Table(element, doc)

def table_to_markdown(table):
    """Converts a docx table to a structured Markdown grid."""
    rows = []
    for row in table.rows:
        row_text = "| " + " | ".join(cell.text.replace('\n', ' ').strip() for cell in row.cells) + " |"
        rows.append(row_text)
    return "\n".join(rows)

def call_gemini_text(markdown_content, header_text):
    """Calls Gemini Text API with spatial markdown and fixed schema."""
    prompt = f"""
    You are a Clinical Data Auditor. Analyze the MDT Proforma provided in Markdown format.
    
    REFERENCE HEADER: {header_text}
    
    MANDATORY RULES:
    1. NO HALLUCINATIONS: If a field is blank or missing, you MUST return null. Do not invent data.
    2. SPATIAL AWARENESS: Use the table structure to correctly attribute data (e.g., Row 1 is Patient Details, Row 7 is MDT Outcome).
    3. TEMPORAL LOGIC: 
       - The MDT Meeting Date is in the REFERENCE HEADER.
       - If '62 DAY TARGET' is blank, pathway = '31-day' and target_date = [MDT Meeting Date + 31 days].
    
    TARGET JSON SCHEMA:
    {{
        "mdt_meeting_date": "DD/MM/YYYY",
        "patient_details": {{
            "hospital_number": "string",
            "nhs_number": "string",
            "name": "string",
            "gender": "string",
            "dob": "date",
            "age": "string"
        }},
        "cancer_target_dates": {{
            "extracted_62_day_target": "date or null",
            "pathway_type": "62-day or 31-day",
            "calculated_target_date": "DD/MM/YYYY"
        }},
        "staging_and_diagnosis": {{
            "diagnosis": "string",
            "icd10_code": "string",
            "differentiation": "string",
            "staging": "raw text",
            "integrated_tnm_stage": "string",
            "dukes": "string"
        }},
        "clinical_details": "Comprehensive verbatim text from Clinical Details section",
        "mdt_outcome": "Comprehensive verbatim text from MDT Outcome section"
    }}

    CONTENT:
    {markdown_content}
    """
    
    try:
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.0,
                response_mime_type="application/json",
            )
        )
        return json.loads(response.text)
    except Exception as e:
        if "429" in str(e):
            print("\nRate limit hit. Waiting 30s...")
            time.sleep(30)
            return None
        else:
            print(f"\nError: {e}")
            return None

def update_longitudinal_store(data, case_index):
    """Updates the master store and individual files."""
    if not os.path.exists(JSON_RAW_DIR): os.makedirs(JSON_RAW_DIR)
    
    # Clean NHS for unique key
    p_node = data.get("patient_details", {})
    nhs = str(p_node.get("nhs_number", "UNKNOWN")).replace(" ", "")
    nhs = re.sub(r'\(d\).*', '', nhs).strip()
    
    with open(JSON_RAW_DIR / f"case_{case_index:03d}_{nhs}.json", "w") as f:
        json.dump(data, f, indent=4)

    if not os.path.exists(STORE_PATH):
        store = {"patients": {}}
    else:
        with open(STORE_PATH, "r") as f:
            store = json.load(f)
            
    mdt_date = str(data.get("mdt_meeting_date", "UNKNOWN_DATE")).replace("/", "-")
    
    if nhs not in store["patients"]:
        store["patients"][nhs] = {}
        
    if mdt_date not in store["patients"][nhs]:
        store["patients"][nhs][mdt_date] = []
        
    store["patients"][nhs][mdt_date].append(data)
    
    with open(STORE_PATH, "w") as f:
        json.dump(store, f, indent=4)

def main():
    doc = Document(DOCX_PATH)
    elements = list(get_elements_in_order(doc))
    
    cases = []
    current_header = "Unknown MDT Date"
    for el in elements:
        if hasattr(el, 'text') and "Multidisciplinary Meeting" in el.text:
            current_header = el.text
        elif hasattr(el, 'rows'):
            cases.append({"header": current_header, "table": el})

    # Simple Resume Logic
    if not os.path.exists(JSON_RAW_DIR): os.makedirs(JSON_RAW_DIR)
    processed_count = len([f for f in os.listdir(JSON_RAW_DIR) if f.startswith("case_")])

    print(f"Gemini 2.0 Digital OCR | Total: {len(cases)} | Processed: {processed_count}")
    
    for i, case in enumerate(tqdm(cases)):
        # Skip if already in individual JSON folder
        existing = [f for f in os.listdir(JSON_RAW_DIR) if f.startswith(f"case_{i:03d}_")]
        if existing: continue
        
        md_table = table_to_markdown(case["table"])
        result = call_gemini_text(md_table, case["header"])
        
        if result:
            update_longitudinal_store(result, i)
            
        # 10s delay to be extra safe on Free Tier
        time.sleep(10)

if __name__ == "__main__":
    main()
