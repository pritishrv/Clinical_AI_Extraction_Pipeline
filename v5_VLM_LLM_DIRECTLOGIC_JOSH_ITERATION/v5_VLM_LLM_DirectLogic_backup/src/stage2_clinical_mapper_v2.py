import os
import json
import re
import pandas as pd
from pathlib import Path
from tqdm import tqdm
import anthropic
import time
from config import ANTHROPIC_API_KEY

# Configure Claude 3 Haiku (Latest Available for this key)
client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
MODEL_NAME = "claude-3-haiku-20240307"

# Configuration
JSON_DIR = Path("v5_version_1/output/json_raw_claude")
EXCEL_TEMPLATE = Path("data/hackathon-database-prototype.xlsx")
OUTPUT_PATH = Path("v5_version_1/output/hackathon_output.xlsx")

def map_json_to_row(patient_json, column_list):
    """Makes one LLM call to map JSON to Excel columns."""
    
    prompt = f"""
    You are a JSON generator. Map the given patient JSON into a flat dictionary where keys match the TARGET COLUMNS exactly.
    
    Rules:
    1. Use ONLY information present in the JSON.
    2. If a field is not present → return null.
    3. No conversation. No markdown formatting. Return ONLY the raw JSON object.
    4. For Initials → derive from name.
    5. Clean values (remove markers like (a), (b)).

    TARGET COLUMNS:
    {json.dumps(column_list)}

    PATIENT JSON:
    {json.dumps(patient_json)}
    """
    
    try:
        # Using the system parameter for stricter instruction following
        message = client.messages.create(
            model=MODEL_NAME,
            max_tokens=4096,
            temperature=0,
            system="You are a Clinical Data Transformer. You output ONLY valid JSON objects. No preamble, no explanation, no markdown.",
            messages=[{"role": "user", "content": prompt}]
        )
        raw_text = message.content[0].text.strip()
        
        # Robust JSON cleaning
        # Remove any leading/trailing text outside the first { and last }
        start_idx = raw_text.find('{')
        end_idx = raw_text.rfind('}')
        if start_idx != -1 and end_idx != -1:
            clean_json = raw_text[start_idx:end_idx+1]
        else:
            clean_json = raw_text

        return json.loads(clean_json)
    except Exception as e:
        print(f"\nError mapping record: {e}")
        if 'raw_text' in locals():
            print(f"Raw Output Snippet: {raw_text[:100]}...")
        return None

def main():
    # 1. Load Excel Schema
    print("Loading Excel schema...")
    df_template = pd.read_excel(EXCEL_TEMPLATE)
    column_list = list(df_template.columns)
    print(f"Captured {len(column_list)} columns.")

    # 2. Process Each JSON File
    json_files = sorted([f for f in os.listdir(JSON_DIR) if f.endswith(".json")])
    print(f"Found {len(json_files)} patient records.")
    
    all_rows = []
    for f_name in tqdm(json_files):
        with open(JSON_DIR / f_name, "r") as f:
            patient_data = json.load(f)
            
        # One JSON -> One LLM Call -> One Row
        row = map_json_to_row(patient_data, column_list)
        
        if row:
            # Step 4: Post-Process (Ensure all columns exist)
            final_row = {col: row.get(col) for col in column_list}
            all_rows.append(final_row)
            
        # Basic rate limiting for safety
        time.sleep(1)

    # 5. Save Output
    print(f"Combining {len(all_rows)} rows...")
    df_final = pd.DataFrame(all_rows)
    
    # 6. Validation
    print("Validating schema integrity...")
    missing_cols = set(column_list) - set(df_final.columns)
    extra_cols = set(df_final.columns) - set(column_list)
    
    if not missing_cols and not extra_cols:
        print("Validation Passed: All headers match exactly.")
    else:
        if missing_cols: print(f"WARNING: Missing columns: {missing_cols}")
        if extra_cols: print(f"WARNING: Extra columns found: {extra_cols}")

    # Ensure final column order matches template
    df_final = df_final[column_list]
    
    df_final.to_excel(OUTPUT_PATH, index=False)
    print(f"Done! Final database saved to: {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
